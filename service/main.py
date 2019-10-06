import logging

from fastapi import FastAPI
from starlette.responses import Response

from . import api


log = logging.getLogger(__name__)   # pylint: disable=invalid-name
app = FastAPI()  # pylint: disable=invalid-name
app.include_router(api.router)


@app.get('/', include_in_schema=False)
def index():
    return Response("I'm up", media_type='text/plain')
