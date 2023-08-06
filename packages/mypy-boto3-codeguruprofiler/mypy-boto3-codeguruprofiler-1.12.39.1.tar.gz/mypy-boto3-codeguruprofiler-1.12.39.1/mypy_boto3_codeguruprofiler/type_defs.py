"""
Main interface for codeguruprofiler service type definitions.

Usage::

    from mypy_boto3.codeguruprofiler.type_defs import AgentOrchestrationConfigTypeDef

    data: AgentOrchestrationConfigTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AgentOrchestrationConfigTypeDef",
    "AgentConfigurationTypeDef",
    "ConfigureAgentResponseTypeDef",
    "AggregatedProfileTimeTypeDef",
    "ProfilingStatusTypeDef",
    "ProfilingGroupDescriptionTypeDef",
    "CreateProfilingGroupResponseTypeDef",
    "DescribeProfilingGroupResponseTypeDef",
    "GetPolicyResponseTypeDef",
    "GetProfileResponseTypeDef",
    "ProfileTimeTypeDef",
    "ListProfileTimesResponseTypeDef",
    "ListProfilingGroupsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutPermissionResponseTypeDef",
    "RemovePermissionResponseTypeDef",
    "UpdateProfilingGroupResponseTypeDef",
)

AgentOrchestrationConfigTypeDef = TypedDict(
    "AgentOrchestrationConfigTypeDef", {"profilingEnabled": bool}
)

AgentConfigurationTypeDef = TypedDict(
    "AgentConfigurationTypeDef", {"periodInSeconds": int, "shouldProfile": bool}
)

ConfigureAgentResponseTypeDef = TypedDict(
    "ConfigureAgentResponseTypeDef", {"configuration": AgentConfigurationTypeDef}
)

AggregatedProfileTimeTypeDef = TypedDict(
    "AggregatedProfileTimeTypeDef",
    {"period": Literal["P1D", "PT1H", "PT5M"], "start": datetime},
    total=False,
)

ProfilingStatusTypeDef = TypedDict(
    "ProfilingStatusTypeDef",
    {
        "latestAgentOrchestratedAt": datetime,
        "latestAgentProfileReportedAt": datetime,
        "latestAggregatedProfile": AggregatedProfileTimeTypeDef,
    },
    total=False,
)

ProfilingGroupDescriptionTypeDef = TypedDict(
    "ProfilingGroupDescriptionTypeDef",
    {
        "agentOrchestrationConfig": AgentOrchestrationConfigTypeDef,
        "arn": str,
        "createdAt": datetime,
        "name": str,
        "profilingStatus": ProfilingStatusTypeDef,
        "updatedAt": datetime,
    },
    total=False,
)

CreateProfilingGroupResponseTypeDef = TypedDict(
    "CreateProfilingGroupResponseTypeDef", {"profilingGroup": ProfilingGroupDescriptionTypeDef}
)

DescribeProfilingGroupResponseTypeDef = TypedDict(
    "DescribeProfilingGroupResponseTypeDef", {"profilingGroup": ProfilingGroupDescriptionTypeDef}
)

GetPolicyResponseTypeDef = TypedDict("GetPolicyResponseTypeDef", {"policy": str, "revisionId": str})

_RequiredGetProfileResponseTypeDef = TypedDict(
    "_RequiredGetProfileResponseTypeDef", {"contentType": str, "profile": Union[bytes, IO]}
)
_OptionalGetProfileResponseTypeDef = TypedDict(
    "_OptionalGetProfileResponseTypeDef", {"contentEncoding": str}, total=False
)


class GetProfileResponseTypeDef(
    _RequiredGetProfileResponseTypeDef, _OptionalGetProfileResponseTypeDef
):
    pass


ProfileTimeTypeDef = TypedDict("ProfileTimeTypeDef", {"start": datetime}, total=False)

_RequiredListProfileTimesResponseTypeDef = TypedDict(
    "_RequiredListProfileTimesResponseTypeDef", {"profileTimes": List[ProfileTimeTypeDef]}
)
_OptionalListProfileTimesResponseTypeDef = TypedDict(
    "_OptionalListProfileTimesResponseTypeDef", {"nextToken": str}, total=False
)


class ListProfileTimesResponseTypeDef(
    _RequiredListProfileTimesResponseTypeDef, _OptionalListProfileTimesResponseTypeDef
):
    pass


_RequiredListProfilingGroupsResponseTypeDef = TypedDict(
    "_RequiredListProfilingGroupsResponseTypeDef", {"profilingGroupNames": List[str]}
)
_OptionalListProfilingGroupsResponseTypeDef = TypedDict(
    "_OptionalListProfilingGroupsResponseTypeDef",
    {"nextToken": str, "profilingGroups": List[ProfilingGroupDescriptionTypeDef]},
    total=False,
)


class ListProfilingGroupsResponseTypeDef(
    _RequiredListProfilingGroupsResponseTypeDef, _OptionalListProfilingGroupsResponseTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutPermissionResponseTypeDef = TypedDict(
    "PutPermissionResponseTypeDef", {"policy": str, "revisionId": str}
)

RemovePermissionResponseTypeDef = TypedDict(
    "RemovePermissionResponseTypeDef", {"policy": str, "revisionId": str}
)

UpdateProfilingGroupResponseTypeDef = TypedDict(
    "UpdateProfilingGroupResponseTypeDef", {"profilingGroup": ProfilingGroupDescriptionTypeDef}
)
