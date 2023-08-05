from typing import Callable
from fastapi import FastAPI
from zo.aa import get_env
from zo.log import log


def add_start_event(app: FastAPI):
    def _(app: FastAPI) -> Callable:
        async def start_app() -> None:
            # await connect_to_db(app)
            env = get_env()
            docs = f'http://{env.app_host}:{env.app_port}{env.docs_url}' if env.docs_url else env.docs_url
            log.info(f'Start APP [{env.title} | {env.version}] docs:{docs}')

        return start_app

    app.add_event_handler("startup", _(app))


def add_stop_event(app: FastAPI):
    def _(app: FastAPI) -> Callable:
        @log.catch
        async def stop_app() -> None:
            # await close_db_connection(app)
            env = get_env()
            log.info(f'Stop APP {env.title} {env.version}')

        return stop_app

    app.add_event_handler("shutdown", _(app))
