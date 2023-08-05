"""
Main interface for kinesisanalyticsv2 service client paginators.

Usage::

    import boto3
    from mypy_boto3.kinesisanalyticsv2 import (
        ListApplicationSnapshotsPaginator,
        ListApplicationsPaginator,
    )

    client: KinesisAnalyticsV2Client = boto3.client("kinesisanalyticsv2")

    list_application_snapshots_paginator: ListApplicationSnapshotsPaginator = client.get_paginator("list_application_snapshots")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import Iterator, TYPE_CHECKING
from botocore.paginate import Paginator as Boto3Paginator
from mypy_boto3_kinesisanalyticsv2.type_defs import (
    ListApplicationSnapshotsResponseTypeDef,
    ListApplicationsResponseTypeDef,
    PaginatorConfigTypeDef,
)


__all__ = ("ListApplicationSnapshotsPaginator", "ListApplicationsPaginator")


class ListApplicationSnapshotsPaginator(Boto3Paginator):
    """
    [Paginator.ListApplicationSnapshots documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Paginator.ListApplicationSnapshots)
    """

    def paginate(
        self, ApplicationName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListApplicationSnapshotsResponseTypeDef]:
        """
        [ListApplicationSnapshots.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Paginator.ListApplicationSnapshots.paginate)
        """


class ListApplicationsPaginator(Boto3Paginator):
    """
    [Paginator.ListApplications documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Paginator.ListApplications)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListApplicationsResponseTypeDef]:
        """
        [ListApplications.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Paginator.ListApplications.paginate)
        """
