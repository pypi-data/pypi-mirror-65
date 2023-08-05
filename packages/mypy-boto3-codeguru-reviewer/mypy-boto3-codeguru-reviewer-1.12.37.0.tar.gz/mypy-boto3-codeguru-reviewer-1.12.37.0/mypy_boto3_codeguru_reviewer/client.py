"""
Main interface for codeguru-reviewer service client

Usage::

    import boto3
    from mypy_boto3.codeguru_reviewer import CodeGuruReviewerClient

    session = boto3.Session()

    client: CodeGuruReviewerClient = boto3.client("codeguru-reviewer")
    session_client: CodeGuruReviewerClient = session.client("codeguru-reviewer")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, List, TYPE_CHECKING, Type, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_codeguru_reviewer.paginator import ListRepositoryAssociationsPaginator
from mypy_boto3_codeguru_reviewer.type_defs import (
    AssociateRepositoryResponseTypeDef,
    DescribeRepositoryAssociationResponseTypeDef,
    DisassociateRepositoryResponseTypeDef,
    ListRepositoryAssociationsResponseTypeDef,
    RepositoryTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CodeGuruReviewerClient",)


class Exceptions:
    AccessDeniedException: Type[Boto3ClientError]
    ClientError: Type[Boto3ClientError]
    ConflictException: Type[Boto3ClientError]
    InternalServerException: Type[Boto3ClientError]
    NotFoundException: Type[Boto3ClientError]
    ThrottlingException: Type[Boto3ClientError]
    ValidationException: Type[Boto3ClientError]


class CodeGuruReviewerClient:
    """
    [CodeGuruReviewer.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client)
    """

    exceptions: Exceptions

    def associate_repository(
        self, Repository: RepositoryTypeDef, ClientRequestToken: str = None
    ) -> AssociateRepositoryResponseTypeDef:
        """
        [Client.associate_repository documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.associate_repository)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.can_paginate)
        """

    def describe_repository_association(
        self, AssociationArn: str
    ) -> DescribeRepositoryAssociationResponseTypeDef:
        """
        [Client.describe_repository_association documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.describe_repository_association)
        """

    def disassociate_repository(self, AssociationArn: str) -> DisassociateRepositoryResponseTypeDef:
        """
        [Client.disassociate_repository documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.disassociate_repository)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.generate_presigned_url)
        """

    def list_repository_associations(
        self,
        ProviderTypes: List[Literal["CodeCommit", "GitHub"]] = None,
        States: List[Literal["Associated", "Associating", "Failed", "Disassociating"]] = None,
        Names: List[str] = None,
        Owners: List[str] = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ListRepositoryAssociationsResponseTypeDef:
        """
        [Client.list_repository_associations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client.list_repository_associations)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repository_associations"]
    ) -> ListRepositoryAssociationsPaginator:
        """
        [Paginator.ListRepositoryAssociations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Paginator.ListRepositoryAssociations)
        """
