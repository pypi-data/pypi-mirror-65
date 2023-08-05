import abc
import os
from functools import partial
from inspect import isclass, isabstract
from logging import getLogger
from typing import Mapping

from aiohttp import ClientSession, web
from aiohttp.abc import Request
from aiohttp.web_response import Response
from tartiflette import Engine, Scalar

from .clients import ApiRequest
from .clients import HttpApi, DBApi, DBRequest
from .config import Config
from .graphiql import set_graphiql_handler
from .resolvers import set_resolver
from .utils import parse_conf, import_from_module, resolve_paths, ScalarDefinition, import_by_full_path
from .view import create_endpoint, options_handler

logger = getLogger(__name__)


def mount_rest_service_to_app(app, service_name, base_url, endpoints, proxy_headers):
    endpoints_ = {k: ApiRequest(method=(v.get('method') or 'GET'), path_template=v['path'])
                  for k, v in endpoints.items() or []}

    async def start_rest(app_):
        session = ClientSession(raise_for_status=True)
        if not hasattr(app_, 'rest'):
            app_.rest = {}
        if app_.rest.get(service_name):
            raise RuntimeError(f'This name of REST service is already in use {service_name}')

        app_.rest[service_name] = await HttpApi.create(base_url, session=session,
                                                       proxy_headers=proxy_headers,
                                                       endpoints=endpoints_)

        async def shutdown(app__):
            await session.close()

        app_.on_shutdown.append(shutdown)

    app.on_startup.append(start_rest)


def mount_db_service_to_app(app, endpoints, service_name, db_params):
    endpoints_ = {}
    for name, val in endpoints.items():
        if isinstance(val, dict):
            for k, v in val.items():
                val[k] = import_from_module(v)
        if isinstance(val, str):
            val = import_from_module(val)
        endpoints_[name] = DBRequest(val)

    async def start_db(app_):
        if not hasattr(app_, 'db'):
            app_.db = {}
        app_.db[service_name] = await DBApi.create(**db_params, endpoints=endpoints_)

        async def shutdown(app__):
            await app__.db[service_name].close()

        app_.on_shutdown.append(shutdown)

    app.on_startup.append(start_db)


class GqlExt(abc.ABC):
    config: Config

    rest_description = []
    db_description = []
    resolvers_description = []

    def __init__(self, app, path_to_init_file, base_path):
        self.config = Config()
        self.app = app
        self.base_path = base_path
        self.initial_config = parse_conf(path_to_init_file)

        self.schemas = self.initial_config.get('schemas') or {}

    def mount_app(self):
        for rest_file_paths in (self.initial_config.get('rest') or []):
            rest_data = parse_conf(os.path.join(self.base_path, rest_file_paths))
            self.set_rest_service(rest_data)

        for db_file_paths in (self.initial_config.get('db') or []):
            db_data = parse_conf(os.path.join(self.base_path, db_file_paths))
            self.set_db_service(db_data)

        for schema_name, schema_description in self.schemas.items():
            self.handle_schema(schema_name, schema_description)

        if self.config.allow_cors:
            self.allow_cors()

    def handle_schema(self, schema_name, schema_description):
        resolvers_description_file_path = os.path.join(self.base_path, schema_description.get('resolvers'))
        resolvers_description = parse_conf(resolvers_description_file_path)
        self.set_resolvers(resolvers_description, schema_name)

        sdl_paths = [os.path.join(self.base_path, sdl) for sdl in schema_description.get('sdl') or []]
        sdl_paths = resolve_paths(sdl_paths)

        middlewares = [import_from_module(path) for path in schema_description.get('middlewares') or []]

        types_paths = [os.path.join(self.base_path, types) for types in schema_description.get('types') or []]
        types_paths = resolve_paths(types_paths)
        for types_path in types_paths:
            if types_path.endswith('.graphql'):
                sdl_paths.append(types_path)
            if types_path.endswith('.py'):
                self.set_type(types_path, schema_name)

        self.mount_endpoint(schema_name, sdl_paths, schema_description.get('modules'),
                            url=schema_description.get('url'), middlewares=middlewares)

    @staticmethod
    def set_type(types_path, schema_name):
        module = import_by_full_path(types_path)
        for k, v in module.__dict__.items():
            if not isclass(v) or isabstract(v) or v is ScalarDefinition:
                continue
            if issubclass(v, ScalarDefinition):
                Scalar(k, schema_name=schema_name)(v)

    def allow_cors(self):
        async def on_prepare(req: Request, res: Response):
            if req.headers.get('ORIGIN'):
                res.headers['Access-Control-Allow-Origin'] = req.headers.get('ORIGIN')
            res.headers['Access-Control-Allow-Credentials'] = 'true'

        self.app.on_response_prepare.append(on_prepare)

    def set_rest_service(self, rest_description):
        for rest_service_name, endpoints in rest_description.items():
            service_base_url = self.config.get_rest(rest_service_name)
            if not service_base_url:
                raise RuntimeError(f'You must specify the base address of the service for {rest_service_name}')
            proxy_headers = self.config.proxy_headers
            mount_rest_service_to_app(self.app, rest_service_name, service_base_url, endpoints, proxy_headers)

    def set_db_service(self, db_config: Mapping):
        for db_service, endpoints in db_config.items():
            db_params = self.config.get_db(db_service)
            if not db_params:
                raise RuntimeError(f'You must specify dsn of the service for {db_service}')
            mount_db_service_to_app(self.app, endpoints, db_service, db_params)

    def set_resolvers(self, resolvers: dict, schema: str):
        for resolver_name, args in resolvers.items():
            endpoint = args.get('endpoint')
            if endpoint and len(resolver_name.split('.')) == 2:
                args['endpoint'] = f'{self.config.default_service}.{endpoint}'
            set_resolver(resolver_name, schema, args)

    def mount_endpoint(self, schema, sdl, modules, url=None, middlewares=None):
        if middlewares is None:
            middlewares = []
        allow_cors = self.config.allow_cors
        if not url:
            url = f'/graphql/{schema}'

        async def start(app_, engine=None):
            if engine is None:
                engine = Engine()

            await engine.cook(sdl=sdl, schema_name=schema, modules=modules)
            app_.add_routes([web.post(url, create_endpoint(engine, *middlewares))])
            set_graphiql_handler(app_, True, {'endpoint': url}, url, ['POST'], None)

            if allow_cors:
                handler = partial(options_handler, proxy_headers=list(self.config.proxy_headers))
                app_.add_routes([web.options(url, handler)])

            logger.debug(f'{schema} schema has been initialized')

        self.app.on_startup.append(start)
