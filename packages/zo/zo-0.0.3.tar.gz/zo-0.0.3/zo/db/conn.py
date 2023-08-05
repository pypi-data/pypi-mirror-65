from ssdb import Client as DbClient
from ..aa import get_env


def conn_db(host: str = None, port: int = None) -> DbClient:
    if host or port:
        return DbClient(host, port)
    else:
        env = get_env()
        return DbClient(env.db_host, env.db_port)
