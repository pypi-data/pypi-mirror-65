import abc
from logging import getLogger
from typing import Callable, Optional
from typing import Mapping

from aiohttp.abc import Request
from tartiflette import Resolver

from .dataloaders import BaseDataLoader
from .utils import import_from_module

logger = getLogger(__name__)


class BaseResolver:
    endpoint: str
    _endpoint: Optional[Callable] = None

    def get_endpoint(self, request: Request) -> Optional[Callable]:
        if self._endpoint is not None:
            return self._endpoint
        if not self.endpoint:
            return
        try:
            client, service, endpoint = self.endpoint.split('.')
            if not (client and service and endpoint):
                raise ValueError
        except ValueError as e:
            raise RuntimeError(f'error with parse endpoint name {self.endpoint}. '
                               f'use client.service.endpoint format. {e}')

        client = getattr(request.app, client, None)
        service = client.get(service)
        endpoint = getattr(service, endpoint, None)

        if not endpoint:
            raise RuntimeError(f'Cant get source method or endpoint for {self.endpoint}')

        self._endpoint = endpoint
        return endpoint

    async def __call__(self, parent, args, ctx, info):
        return await self.load(parent, args, ctx, info)

    async def load(self, parent, args, ctx, info):
        raise NotImplementedError


class BaseMutationResolver(BaseResolver):

    async def load(self, parent, args, ctx, info):
        endpoint = self.get_endpoint(ctx['request'])
        return await endpoint(**args, headers=ctx['request'].headers)


class BaseQueryResolver(BaseResolver):
    batch: bool = False
    _dataloader: Optional[Callable]

    async def load(self, parent, args, ctx, info):
        endpoint = self.get_endpoint(ctx['request'])
        dataloader = self.get_dataloader(ctx['request'], endpoint)
        return await dataloader(**args)

    def get_dataloader(self, request, endpoint) -> BaseDataLoader:
        dataloader = getattr(request, self.endpoint, None)
        if dataloader is None:
            dataloader = BaseDataLoader(endpoint=endpoint, request=request, batch=self.batch)
            setattr(request, self.endpoint, dataloader)
        return dataloader


class ResolverCreator(abc.ABCMeta):
    def __new__(mcs, name, bases, attrs, resolver_name: str = None, loader: str = None, endpoint: str = None,
                batch: bool = False, args: Mapping = None, **kwargs):
        base = BaseMutationResolver if resolver_name.startswith('Mutation.') else BaseQueryResolver

        loader = import_from_module(loader) if loader else base.load

        attrs = {'batch': batch,
                 'endpoint': endpoint,
                 'load': mcs.init_loader(args, loader)}

        cls = super().__new__(mcs, name, (base,), attrs)
        return cls

    @staticmethod
    def parse_arg(arg_value, parent, ctx):
        if not isinstance(arg_value, str):
            return arg_value
        if arg_value.startswith('parent.'):
            return parent.get(arg_value.split('.')[-1])
        if arg_value.startswith('request.'):
            return ctx['request'].get(arg_value.split('.')[-1])
        return arg_value

    @classmethod
    def parse_args(mcs, arg_value, parent, ctx):
        if isinstance(arg_value, (list, tuple)):
            return [mcs.parse_arg(arg, parent, ctx) for arg in arg_value if arg is not None]
        return mcs.parse_arg(arg_value, parent, ctx)

    @classmethod
    def init_loader(mcs, args_, loader):
        async def loader_(_item, parent, args, ctx, info):
            if args_ is not None:
                for arg_name, arg_val in args_.items():
                    args[arg_name] = mcs.parse_args(arg_val, parent, ctx)
            return await loader(_item, parent, args, ctx, info)

        return loader_


class ResolverDec(Resolver):
    def __call__(self, resolver: Callable) -> Callable:
        if issubclass(resolver, BaseResolver):
            resolver = resolver().__call__
        return super().__call__(resolver)


def set_resolver(resolver_name: str, schema: str, args: Mapping):
    @ResolverDec(resolver_name, schema_name=schema)
    class Loader(metaclass=ResolverCreator, **args, resolver_name=resolver_name):
        pass
