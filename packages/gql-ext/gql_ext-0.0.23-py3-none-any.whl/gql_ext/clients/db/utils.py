import functools
import logging
import re
from typing import Union, Mapping, List, Optional, Tuple

from asyncpg import Connection
from asyncpg.pool import Pool, create_pool
from ujson import dumps, loads

Con = Union[Pool, Connection]

logger = logging.getLogger(__name__)

__all__ = ('create_db_pool', 'fetchrow', 'fetchval', 'fetch', 'executemany', 'execute', 'Con')


async def create_db_pool(dsn, **kwargs) -> Pool:
    return await create_pool(dsn=dsn, init=_init_connection, **kwargs)


async def _init_connection(con: Connection):
    def _encoder(value):
        return b'\x01' + dumps(value).encode('utf-8')

    def _decoder(value):
        return loads(value[1:].decode('utf-8'))

    await con.set_type_codec(
        'jsonb',
        encoder=_encoder,
        decoder=_decoder,
        schema='pg_catalog',
        format='binary'
    )


@functools.lru_cache(maxsize=1024)
def prepare_query(q: str) -> (str, Tuple):
    q_params = {}

    def get_n(x):
        param = x.group(1)
        if param not in q_params:
            q_params[param] = len(q_params) + 1
        return f'${q_params[param]}'

    q = re.sub(r'(?<!:):(\w+)', get_n, q)
    return q, tuple(q_params)


def check_query_param(param_value: str) -> bool:
    return not bool(re.findall(r'[^1-9a-zA-Z_ ]', param_value))


def get_prepared_order_params(params: List[str]) -> List[str]:
    if not isinstance(params, list):
        params = [params]
    params = params[:]
    for i, param in enumerate(params):
        if not isinstance(param, str):
            raise TypeError('invalid type of order')
        if param.startswith('-'):
            params[i] = f'{param} desc'
        if not check_query_param(params[i]):
            raise ValueError('invalid value of order')
    return params


def build_order(order_params: Union[List, str, None], q: str) -> str:
    if not order_params:
        orders = ['1']
    else:
        orders = get_prepared_order_params(order_params)

    return re.sub(r'(:order)\b', ', '.join(orders), q)


def build_query(q: str, params: Mapping) -> (str, List):
    q = build_order(params.get('order'), q)
    q, q_params = prepare_query(q)
    params = [params.get(param) for param in q_params]
    logger.debug(f'QUERY:\n{q}\nARGS:{params}')
    return q, params


def fetchrow(**default_params):
    def dec(func):
        @functools.wraps(func)
        async def wrapper(con: Connection, **kwargs) -> Optional[Mapping]:
            query = func()
            params = {**default_params, **kwargs}
            query, q_params = build_query(query, params)
            return await con.fetchrow(query, *q_params)

        return wrapper

    return dec


def fetch(**default_params):
    def dec(func):
        @functools.wraps(func)
        async def wrapper(con: Connection, **kwargs) -> List[Mapping]:
            query = func()
            params = {**default_params, **kwargs}
            query, q_params = build_query(query, params)
            return await con.fetch(query, *q_params)

        return wrapper

    return dec


def fetchval(**default_params):
    def dec(func):
        @functools.wraps(func)
        async def wrapper(con: Connection, **kwargs):
            query = func()
            params = {**default_params, **kwargs}
            query, q_params = build_query(query, params)
            return await con.fetchval(query, *q_params)

        return wrapper

    return dec


def execute(**default_params):
    def dec(func):
        @functools.wraps(func)
        async def wrapper(con: Connection, **kwargs):
            query = func()
            params = {**default_params, **kwargs}
            query, q_params = build_query(query, params)
            return await con.execute(query, *q_params)

        return wrapper

    return dec


def executemany(**default_params):
    def dec(func):
        @functools.wraps(func)
        async def wrapper(con: Connection, list_of_params: List[Mapping]):
            query, q_params = prepare_query(func())

            args = []
            for row_of_params in list_of_params:
                row_of_params = {**default_params, **row_of_params}
                args.append(tuple(row_of_params.get(param_name) for param_name in q_params))
            logger.debug(f'QUERY:\n{query}\nARGS:{args}')

            return await con.executemany(query, args)

        return wrapper

    return dec
