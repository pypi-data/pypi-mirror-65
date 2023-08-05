"""
Main interface for codebuild service client paginators.

Usage::

    import boto3
    from mypy_boto3.codebuild import (
        ListBuildsPaginator,
        ListBuildsForProjectPaginator,
        ListProjectsPaginator,
    )

    client: CodeBuildClient = boto3.client("codebuild")

    list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
    list_builds_for_project_paginator: ListBuildsForProjectPaginator = client.get_paginator("list_builds_for_project")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Iterator, TYPE_CHECKING
from botocore.paginate import Paginator as Boto3Paginator
from mypy_boto3_codebuild.type_defs import (
    ListBuildsForProjectOutputTypeDef,
    ListBuildsOutputTypeDef,
    ListProjectsOutputTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ListBuildsPaginator", "ListBuildsForProjectPaginator", "ListProjectsPaginator")


class ListBuildsPaginator(Boto3Paginator):
    """
    [Paginator.ListBuilds documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codebuild.html#CodeBuild.Paginator.ListBuilds)
    """

    def paginate(
        self,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListBuildsOutputTypeDef]:
        """
        [ListBuilds.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codebuild.html#CodeBuild.Paginator.ListBuilds.paginate)
        """


class ListBuildsForProjectPaginator(Boto3Paginator):
    """
    [Paginator.ListBuildsForProject documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildsForProject)
    """

    def paginate(
        self,
        projectName: str,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListBuildsForProjectOutputTypeDef]:
        """
        [ListBuildsForProject.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildsForProject.paginate)
        """


class ListProjectsPaginator(Boto3Paginator):
    """
    [Paginator.ListProjects documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codebuild.html#CodeBuild.Paginator.ListProjects)
    """

    def paginate(
        self,
        sortBy: Literal["NAME", "CREATED_TIME", "LAST_MODIFIED_TIME"] = None,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListProjectsOutputTypeDef]:
        """
        [ListProjects.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/codebuild.html#CodeBuild.Paginator.ListProjects.paginate)
        """
