import asyncio
from concurrent.futures import ProcessPoolExecutor

from service import assignment
from service.api.models import AssignmentRequest, AssignmentResponse

executor = None  # pylint:disable=invalid-name


def init():
    global executor  # pylint:disable=invalid-name,global-statement
    executor = ProcessPoolExecutor()


def shutdown():
    executor.shutdown()


async def solve(
        request: AssignmentRequest,
) -> AssignmentResponse:
    global executor  # pylint:disable=invalid-name,global-statement

    problem = _problem_from_request(request)

    loop = asyncio.get_running_loop()
    solution = await loop.run_in_executor(executor, assignment.do, problem)

    print(solution)
    if solution.is_failure():
        raise RuntimeError

    return _solution_as_response(solution)


def _problem_from_request(
        request: AssignmentRequest
) -> assignment.Problem:
    datacenters = [
        assignment.Datacenter(name=item.name, servers=item.servers)
        for item in request.data_centers
    ]
    return assignment.Problem(
        dm_capacity=request.DM_capacity,
        de_capacity=request.DE_capacity,
        datacenters=tuple(datacenters),
    )


def _solution_as_response(
        solution: assignment.Solution
) -> AssignmentResponse:
    return AssignmentResponse(
        DE=solution.de,
        DM_data_center=solution.dm_datacenter,
    )
