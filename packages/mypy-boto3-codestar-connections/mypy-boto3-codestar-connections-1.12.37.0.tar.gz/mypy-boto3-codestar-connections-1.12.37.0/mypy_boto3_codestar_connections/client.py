"""
Main interface for codestar-connections service client

Usage::

    import boto3
    from mypy_boto3.codestar_connections import CodeStarconnectionsClient

    session = boto3.Session()

    client: CodeStarconnectionsClient = boto3.client("codestar-connections")
    session_client: CodeStarconnectionsClient = session.client("codestar-connections")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, TYPE_CHECKING, Type
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_codestar_connections.type_defs import (
    CreateConnectionOutputTypeDef,
    GetConnectionOutputTypeDef,
    ListConnectionsOutputTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CodeStarconnectionsClient",)


class Exceptions:
    ClientError: Type[Boto3ClientError]
    LimitExceededException: Type[Boto3ClientError]
    ResourceNotFoundException: Type[Boto3ClientError]


class CodeStarconnectionsClient:
    """
    [CodeStarconnections.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codestar-connections.html#CodeStarconnections.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codestar-connections.html#CodeStarconnections.Client.can_paginate)
        """

    def create_connection(
        self, ProviderType: Literal["Bitbucket"], ConnectionName: str
    ) -> CreateConnectionOutputTypeDef:
        """
        [Client.create_connection documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codestar-connections.html#CodeStarconnections.Client.create_connection)
        """

    def delete_connection(self, ConnectionArn: str) -> Dict[str, Any]:
        """
        [Client.delete_connection documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codestar-connections.html#CodeStarconnections.Client.delete_connection)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codestar-connections.html#CodeStarconnections.Client.generate_presigned_url)
        """

    def get_connection(self, ConnectionArn: str) -> GetConnectionOutputTypeDef:
        """
        [Client.get_connection documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codestar-connections.html#CodeStarconnections.Client.get_connection)
        """

    def list_connections(
        self,
        ProviderTypeFilter: Literal["Bitbucket"] = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ListConnectionsOutputTypeDef:
        """
        [Client.list_connections documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codestar-connections.html#CodeStarconnections.Client.list_connections)
        """
