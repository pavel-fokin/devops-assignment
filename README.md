[![CircleCI](https://circleci.com/gh/fokinpv/devops-assignment.svg?style=svg&circle-token=9a47e52dbe731a15b6e10bdab9a0126999ffb7ba)](https://circleci.com/gh/fokinpv/devops-assignment)
[![codecov](https://codecov.io/gh/fokinpv/devops-assignment/branch/master/graph/badge.svg)](https://codecov.io/gh/fokinpv/devops-assignment)



# devops-assignment

This is toy service to find minimal number of devops to maintain given servers.

# Problem

In this example scenario, company uses a range of data centers
for running load tests, each with a number of servers. How many
servers are needed and how they are distributed across data centers
vary over time. Servers are maintained (checked for health, restarted, rebuilt, upgraded, etc) by
the DevOps Manager (DM) and possibly other DevOps Engineers (DE) called in on-demand.
There is only one DM, but there can be many DEs.

We will assume that the DM and each DE can only work in one data center per day.
Additionally, DMs and DEs have a limitation on how many servers they can maintain during one
workday. Each server must have maintenance available at all times.

## The requirements:

For this scenario, we want to have an online service with a REST API. This API should be used
to easily retrieve the minimum number of extra DE’s we need to call in in addition to the DM in
order to maintain all servers in all currently active datacenters. We want to specify as input the
data center setup and the expected capacity of the DM/DE’s. In return we want the number of
DE’s to call in to cover the current server setup. We also want to know which datacenter is best
to place the DM in.

See the input/output example in the Appendix.

## Scope of the challenge:

Please create a Python service with a REST API that solves this problem using the
inputs/output format specified in the Appendix. Use the resources/libraries/etc you deem
suitable for the task.

For the scope of this challenge, the service need not provide any other endpoints.

## Appendix: Expected inputs and outputs

### Example 1

- Input:
```
{
DM_capacity: 20,
DE_capacity: 8,
data_centers: [
{name: “Paris”, “servers”: 20 },
{name: “Stockholm”, “servers”: 62 }
]
}
```
- Expected output
```
{
DE: 8,
DM_data_center: “Paris”
}
```

### Example 2

- Input:
```
{
DM_capacity: 6,
DE_capacity: 10,
data_centers: [
{name: “Paris”, “servers”:30 },
{name: “Stockholm”, “servers”: 66 }
]
}
```
- Expected output
```
{
DE: 9,
DM_data_center: “Stockholm”
}
```

### Example 3

- Input:
```
{
DM_capacity: 12,
DE_capacity: 7,
data_centers: [
{name: “Berlin”, “servers”: 12 },
{name: “Stockholm”, “servers”: 17 }
]
}
```
- Expected output
```
{
DE: 7,
DM_data_center: “Paris”
}
```
