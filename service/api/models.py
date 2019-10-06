# pylint:disable=too-few-public-methods
from typing import List
from pydantic import BaseModel, validator


class AssignmentRequest(BaseModel):

    class Datacenter(BaseModel):
        name: str
        servers: int

        @validator('name')
        def validate_name(cls, val):  # noqa pylint: disable=no-self-argument,no-self-use
            if not val:
                raise ValueError('must be not empty')
            return val

        @validator('servers')
        def validate_servers(cls, val):  # noqa pylint: disable=no-self-argument,no-self-use
            if not val > 0:
                raise ValueError('must be greater then 0')
            return val

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
