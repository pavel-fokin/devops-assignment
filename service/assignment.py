from dataclasses import dataclass
from functools import lru_cache

import pulp

LRU_CACHE_SIZE = 8


@dataclass
class Datacenter:
    name: str
    servers: int

    def __hash__(self):
        return hash((self.name, self.servers))


@dataclass
class Problem:
    dm_servers: int
    de_servers: int
    datacenters: tuple

    def __hash__(self):
        return hash((self.dm_servers, self.de_servers, self.datacenters))


@dataclass
class Solution:
    de: int = -1  # pylint: disable=invalid-name
    dm_datacenter: str = ''
    status: int = 0  # pulp.LpStatusNotSolved

    def is_success(self):
        return self.status == pulp.LpStatusOptimal

    def is_failure(self):
        return self.status != pulp.LpStatusOptimal


@lru_cache(maxsize=LRU_CACHE_SIZE)
def do(  # pylint: disable=invalid-name
        problem: Problem, debug: bool = False
) -> Solution:

    # Define optimization variables
    # - number_of_de - number of devops in specific datacenter
    # - dm_to_datacenter - assign DevOps manager to specific datacenter
    number_of_de = {}
    dm_to_datacenter = {}
    for datacenter in problem.datacenters:
        number_of_de[datacenter.name] = pulp.LpVariable(
            f"number_of_de_{datacenter.name}", cat=pulp.LpInteger
        )
        dm_to_datacenter[datacenter.name] = pulp.LpVariable(
            f"dm_to_{datacenter.name}", cat=pulp.LpBinary
        )

    # We want to solve optimization problem
    # to find mininum devops across all datacenters
    model = pulp.LpProblem('DevOps Assignment', pulp.LpMinimize)
    model += sum(var for var in number_of_de.values())

    # Set constraints for the problem
    # Each server must have maintenance available at all times.
    # So we have to have equal or greater number of DevOps for all datacenters
    for datacenter in problem.datacenters:
        model += (
            problem.dm_servers * dm_to_datacenter[datacenter.name]
            + (problem.de_servers * number_of_de[datacenter.name])
            >= datacenter.servers
        )

    # DevOps Manager has to be only one
    model += (
        sum([
            dm_to_datacenter[datacenter.name]
            for datacenter in problem.datacenters
        ]) == 1
    )

    solver = pulp.PULP_CBC_CMD(msg=1 if debug else 0)
    status = model.solve(solver)

    if debug:
        model.writeLP('model.lp')

        print(pulp.LpStatus[status])
        for var in number_of_de.values():
            print(var.name, var.value())

        for var in dm_to_datacenter.values():
            print(var.name, var.value())

    # If we could not find optimal solution
    # return empty Solution
    if not status == pulp.LpStatusOptimal:
        return Solution()

    return Solution(
        de=sum(
            int(var.value()) for var in number_of_de.values()
            if var.value() > 0
        ),
        dm_datacenter=[
            name for name, var in dm_to_datacenter.items()
            if var.value() == 1
        ][0],
        status=status,
    )
