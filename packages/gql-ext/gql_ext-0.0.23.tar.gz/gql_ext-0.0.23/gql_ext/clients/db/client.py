from abc import ABC
from logging import getLogger
from typing import Mapping, Optional

from .utils import Con, create_db_pool

logger = getLogger(__name__)


class DBRequest(ABC):
    pool: Con

    def __get__(self, instance, owner):
        if instance is None:
            return self
        self.pool = instance.pool
        return self

    def __init__(self, operations):
        self.operations = operations

    async def __call__(self, **kwargs):
        if isinstance(self.operations, dict):
            return {k: await v(self.pool, **kwargs) for k, v in self.operations.items()}
        return await self.operations(self.pool, **kwargs)


class DBApi:
    def __init__(self, pool: Con):
        self.pool = pool

    @classmethod
    async def create(cls, dsn, endpoints: Optional[Mapping[str, DBRequest]] = None, **kwargs):
        pool = await create_db_pool(dsn, **kwargs)
        res = cls(pool)
        if endpoints:
            res.set_req_methods(endpoints)
        return res

    async def close(self):
        await self.pool.close()

    def set_req_methods(self, endpoints: Mapping[str, DBRequest]):
        for endpoint_name, endpoint in endpoints.items() or []:
            endpoint.pool = self.pool
            setattr(self, endpoint_name, endpoint)
