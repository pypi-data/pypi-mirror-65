"""
Main interface for transfer service client paginators.

Usage::

    import boto3
    from mypy_boto3.transfer import (
        ListServersPaginator,
    )

    client: TransferClient = boto3.client("transfer")

    list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import Iterator, TYPE_CHECKING
from botocore.paginate import Paginator as Boto3Paginator
from mypy_boto3_transfer.type_defs import ListServersResponseTypeDef, PaginatorConfigTypeDef


__all__ = ("ListServersPaginator",)


class ListServersPaginator(Boto3Paginator):
    """
    [Paginator.ListServers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/transfer.html#Transfer.Paginator.ListServers)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListServersResponseTypeDef]:
        """
        [ListServers.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/transfer.html#Transfer.Paginator.ListServers.paginate)
        """
