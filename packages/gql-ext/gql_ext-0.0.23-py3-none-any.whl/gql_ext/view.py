import json
from copy import copy
from functools import partial
from typing import List

from aiohttp import web
from aiohttp.web import View, Response

from .exceptions import BadRequestError


class GraphQLView(View):
    engine = None

    @staticmethod
    def handle_multipart(multipart):
        res = json.loads(multipart['operations'])
        _map = json.loads(multipart.get('map'))
        for name, mapping_variables in _map.items() or []:
            for map_var in mapping_variables:
                var_name = map_var.split('.')[1]
                if var_name not in res['variables']:
                    continue
                res['variables'][var_name] = [] if res['variables'][var_name] == [None] else res['variables'][var_name]
                if isinstance(res['variables'][var_name], list):
                    res['variables'][var_name].append(multipart.get(name))
                else:
                    res['variables'][var_name] = multipart.get(name)
        return res

    async def parse_params(self, req):
        try:
            multipart = await req.post()
            if multipart:
                req_content = self.handle_multipart(multipart)
            else:
                req_content = await req.json(loads=json.loads)
        except Exception:
            raise BadRequestError("Body should be a JSON object or multipart")

        if "query" not in req_content:
            raise BadRequestError('The mandatory "query" parameter is missing.')

        variables = None
        if "variables" in req_content and req_content["variables"] != "":
            variables = req_content["variables"]
            try:
                if isinstance(variables, str):
                    variables = json.loads(variables)
            except Exception:
                raise BadRequestError(
                    'The "variables" parameter is invalid. '
                    "A JSON mapping is expected."
                )

        return req_content["query"], variables, req_content.get("operationName")

    async def handle_query(self, req, query, query_vars, operation_name, context):
        context = copy(context)
        try:
            if not operation_name:
                operation_name = None

            return await self.engine.execute(
                query=query,
                variables=query_vars,
                context=context,
                operation_name=operation_name,
            )
        except Exception as e:
            return {"data": None, "errors": str(e)}

    async def post(self):
        if not self.engine:
            raise NotImplementedError
        user_c = {'request': self.request}
        qry, qry_vars, op_name = await self.parse_params(self.request)
        data = await self.handle_query(self.request, qry, qry_vars, op_name, user_c)
        return web.json_response(data, dumps=json.dumps)


async def options_handler(request, proxy_headers: List[str] = None):
    if proxy_headers is None:
        proxy_headers = []

    headers = ['origin', 'content-type', 'accept'] + proxy_headers
    for header in request.headers:
        if header.lower() not in headers:
            headers.append(header.lower())
    headers = {'Access-Control-Allow-Methods': 'POST',
               'Access-Control-Allow-Headers': ', '.join(headers)}
    return Response(headers=headers)


def create_endpoint(_engine, *middlewares):
    @EndpointMiddleware(middlewares)
    class Endpoint(GraphQLView):
        engine = _engine

    return Endpoint


class EndpointMiddleware:
    def __init__(self, middlewares):
        self.middlewares = middlewares

    def __call__(self, func):
        async def wrapper(request):
            res = func
            for mid in reversed(self.middlewares):
                res = partial(mid, res)
            return await res(request)

        return wrapper
