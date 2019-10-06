import logging

from fastapi import APIRouter

from .models import AssignmentRequest, AssignmentResponse

log = logging.getLogger(__name__)   # pylint: disable=invalid-name
router = APIRouter()  # pylint: disable=invalid-name


@router.post('/api/assignment', response_model=AssignmentResponse)
async def assignment(item: AssignmentRequest):
    log.info(item)
    return AssignmentResponse()
