# pylint: disable=redefined-outer-name
import pytest

from service import assignment


@pytest.fixture
def problem_paris():
    return assignment.Problem(
        dm_servers=20,
        de_servers=8,
        datacenters=(
            assignment.Datacenter(name='Paris', servers=20),
            assignment.Datacenter(name='Stockholm', servers=62),
        ),
    )


# What if we have de_servers == 0
@pytest.fixture
def problem_paris_failure():
    return assignment.Problem(
        dm_servers=20,
        de_servers=0,
        datacenters=(
            assignment.Datacenter(name='Paris', servers=20),
            assignment.Datacenter(name='Stockholm', servers=62),
        ),
    )


@pytest.fixture
def problem_stockholm():
    return assignment.Problem(
        dm_servers=6,
        de_servers=10,
        datacenters=(
            assignment.Datacenter(name='Paris', servers=30),
            assignment.Datacenter(name='Stockholm', servers=66),
        ),
    )


# What if we have dm_servers == 0
@pytest.fixture
def problem_stockholm_failure():
    return assignment.Problem(
        dm_servers=0,
        de_servers=10,
        datacenters=(
            assignment.Datacenter(name='Paris', servers=30),
            assignment.Datacenter(name='Stockholm', servers=66),
        ),
    )


@pytest.fixture
def problem_berlin():
    return assignment.Problem(
        dm_servers=12,
        de_servers=7,
        datacenters=(
            assignment.Datacenter(name='Berlin', servers=11),
            assignment.Datacenter(name='Stockholm', servers=21),
        ),
    )


def test_paris_success(problem_paris):
    solution = assignment.do(problem_paris)

    assert solution.is_success()
    assert solution.de == 8
    assert solution.dm_datacenter == 'Paris'


def test_stockholm_success(problem_stockholm):
    solution = assignment.do(problem_stockholm)

    assert solution.is_success()
    assert solution.de == 9
    assert solution.dm_datacenter == 'Stockholm'


def test_berlin_success(problem_berlin):
    solution = assignment.do(problem_berlin)

    assert solution.is_success()
    assert solution.de == 3
    assert solution.dm_datacenter == 'Berlin'


def test_paris_failure(problem_paris_failure):
    solution = assignment.do(problem_paris_failure)

    assert solution.is_failure()


# TODO Current model doesn't fail if DM_capacity is 0
# It still assigns DevOps Manager to some datacenter
# Not sure if it is OK or not
@pytest.mark.xfail
def test_stockholm_failure(problem_stockholm_failure):
    solution = assignment.do(problem_stockholm_failure)

    assert solution.is_failure()
