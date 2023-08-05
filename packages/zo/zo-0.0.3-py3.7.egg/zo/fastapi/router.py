import io
import pathlib
from PIL import Image

from fastapi import APIRouter, UploadFile
from zo.aa import get_env, HostInfo, calc_hash
from .response import resp, RespDict
from .error import abort_if, ValidationErrorMessage


def r_home(router: APIRouter):
    @router.get("/", name="Home", include_in_schema=False)
    async def _():
        env = get_env()
        server = HostInfo() if env.debug else ''
        return resp({'project': env.title, 'version': env.version, 'server': server})


def r_demo_resp(router: APIRouter):
    @router.get("/demo/resp", name="Demo Resp", tags=['Demo'],
                responses={
                    200: {
                        "description": "Successs",
                        "content": {
                            "application/json": {
                                "example": {
                                    "message": "ok",
                                    "result": {
                                        "id": "bar",
                                        "value": "The bar tenders",
                                        "description": 'This is example'
                                    },
                                    "detail": {}
                                }
                            }
                        },
                    },
                    400: {'model': ValidationErrorMessage},
                    422: {'model': ValidationErrorMessage},
                    500: {'model': ValidationErrorMessage},
                })
    async def _():
        return resp()


async def r_upload_image(file: UploadFile) -> str:
    allow_content_type = {'image/png': 'png', 'image/jpg': 'jpg', 'image/jpeg': 'jpg'}
    abort_if(file.content_type not in allow_content_type, f'file_type error {file.content_type} (Only PNG/JPG)')
    contents = await file.read()
    abort_if(len(contents) / 1024 / 1024 > 10, f'file_size Limit = 1MB ({int(len(contents) / 1024 / 1024)}MB)')
    # save
    sha1 = calc_hash(contents)
    file_suffix = 'png' if file.filename.endswith(".png") else 'jpg'
    im = Image.open(io.BytesIO(contents))
    path = pathlib.Path(f'static/upload/image/{sha1[:2]}/{sha1}.{file_suffix}')
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        if file_suffix == 'png':
            im = im.convert('P')
        im.save(path, optimize=True, format='PNG' if file_suffix == 'png' else 'JPEG')
    return f'/{path}'
