import logging

from fastapi import APIRouter
from starlette import status
from starlette.exceptions import HTTPException

from service import solver
from .models import AssignmentRequest, AssignmentResponse

log = logging.getLogger(__name__)   # pylint: disable=invalid-name
router = APIRouter()  # pylint: disable=invalid-name


@router.post('/api/assignment', response_model=AssignmentResponse)
async def post_assignment(request: AssignmentRequest):
    log.info(request)
    try:
        response = await solver.solve(request)
    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No solution"
        )
    log.info(response)
    return response
