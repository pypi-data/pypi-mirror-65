from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi.encoders import jsonable_encoder
import time
from zo.log import log
from .error import resp_error


def add_cors(app, allowed_hosts=None):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_hosts or ['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def add_process_time(app):
    @app.middleware('http')
    @log.catch()
    async def _add_process_time(request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            log.exception(e)
            response = resp_error(request, 'Error', 'error_code', 'Error', HTTP_500_INTERNAL_SERVER_ERROR)
        response.headers['X-Process-Time'] = f'{(time.time() - start_time) * 1000:.3f} ms'
        return response
