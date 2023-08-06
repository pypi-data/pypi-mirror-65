"""
Main interface for codeguruprofiler service client paginators.

Usage::

    import boto3
    from mypy_boto3.codeguruprofiler import (
        ListProfileTimesPaginator,
    )

    client: CodeGuruProfilerClient = boto3.client("codeguruprofiler")

    list_profile_times_paginator: ListProfileTimesPaginator = client.get_paginator("list_profile_times")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from datetime import datetime
import sys
from typing import Iterator, TYPE_CHECKING
from botocore.paginate import Paginator as Boto3Paginator
from mypy_boto3_codeguruprofiler.type_defs import (
    ListProfileTimesResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ListProfileTimesPaginator",)


class ListProfileTimesPaginator(Boto3Paginator):
    """
    [Paginator.ListProfileTimes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.39/reference/services/codeguruprofiler.html#CodeGuruProfiler.Paginator.ListProfileTimes)
    """

    def paginate(
        self,
        endTime: datetime,
        period: Literal["P1D", "PT1H", "PT5M"],
        profilingGroupName: str,
        startTime: datetime,
        orderBy: Literal["TimestampAscending", "TimestampDescending"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListProfileTimesResponseTypeDef]:
        """
        [ListProfileTimes.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.39/reference/services/codeguruprofiler.html#CodeGuruProfiler.Paginator.ListProfileTimes.paginate)
        """
