# pylint: disable=too-few-public-methods
import logging
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, validator

app = FastAPI()  # pylint: disable=invalid-name
log = logging.getLogger(__name__)   # pylint: disable=invalid-name


class AssignmentRequest(BaseModel):

    class Datacenter(BaseModel):
        name: str
        servers: int

    DM_capacity: int
    DE_capacity: int
    data_centers: List[Datacenter]

    @validator('DM_capacity', 'DE_capacity')
    def validate_capacity(cls, val):  # noqa pylint: disable=no-self-argument,no-self-use
        if not val > 0:
            raise ValueError('must be greater then 0')
        return val


class AssignmentResponse(BaseModel):
    DE: int = -1
    DM_data_center: str = ''


@app.post('/api/assignment', response_model=AssignmentResponse)
async def assignment(item: AssignmentRequest):
    log.info(item)
    return AssignmentResponse()
