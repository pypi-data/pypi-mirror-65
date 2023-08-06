"""
Main interface for codeguruprofiler service.

Usage::

    import boto3
    from mypy_boto3.codeguruprofiler import (
        Client,
        CodeGuruProfilerClient,
        ListProfileTimesPaginator,
        )

    session = boto3.Session()

    client: CodeGuruProfilerClient = boto3.client("codeguruprofiler")
    session_client: CodeGuruProfilerClient = session.client("codeguruprofiler")

    list_profile_times_paginator: ListProfileTimesPaginator = client.get_paginator("list_profile_times")
"""
from mypy_boto3_codeguruprofiler.client import (
    CodeGuruProfilerClient as Client,
    CodeGuruProfilerClient,
)
from mypy_boto3_codeguruprofiler.paginator import ListProfileTimesPaginator


__all__ = ("Client", "CodeGuruProfilerClient", "ListProfileTimesPaginator")
