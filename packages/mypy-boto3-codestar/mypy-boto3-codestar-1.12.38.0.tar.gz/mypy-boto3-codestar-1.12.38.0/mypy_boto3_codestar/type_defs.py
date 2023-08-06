"""
Main interface for codestar service type definitions.

Usage::

    from mypy_boto3.codestar.type_defs import AssociateTeamMemberResultTypeDef

    data: AssociateTeamMemberResultTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateTeamMemberResultTypeDef",
    "CodeCommitCodeDestinationTypeDef",
    "GitHubCodeDestinationTypeDef",
    "CodeDestinationTypeDef",
    "S3LocationTypeDef",
    "CodeSourceTypeDef",
    "CodeTypeDef",
    "CreateProjectResultTypeDef",
    "CreateUserProfileResultTypeDef",
    "DeleteProjectResultTypeDef",
    "DeleteUserProfileResultTypeDef",
    "ProjectStatusTypeDef",
    "DescribeProjectResultTypeDef",
    "DescribeUserProfileResultTypeDef",
    "ProjectSummaryTypeDef",
    "ListProjectsResultTypeDef",
    "ResourceTypeDef",
    "ListResourcesResultTypeDef",
    "ListTagsForProjectResultTypeDef",
    "TeamMemberTypeDef",
    "ListTeamMembersResultTypeDef",
    "UserProfileSummaryTypeDef",
    "ListUserProfilesResultTypeDef",
    "PaginatorConfigTypeDef",
    "TagProjectResultTypeDef",
    "ToolchainSourceTypeDef",
    "ToolchainTypeDef",
    "UpdateTeamMemberResultTypeDef",
    "UpdateUserProfileResultTypeDef",
)

AssociateTeamMemberResultTypeDef = TypedDict(
    "AssociateTeamMemberResultTypeDef", {"clientRequestToken": str}, total=False
)

CodeCommitCodeDestinationTypeDef = TypedDict("CodeCommitCodeDestinationTypeDef", {"name": str})

_RequiredGitHubCodeDestinationTypeDef = TypedDict(
    "_RequiredGitHubCodeDestinationTypeDef",
    {
        "name": str,
        "type": str,
        "owner": str,
        "privateRepository": bool,
        "issuesEnabled": bool,
        "token": str,
    },
)
_OptionalGitHubCodeDestinationTypeDef = TypedDict(
    "_OptionalGitHubCodeDestinationTypeDef", {"description": str}, total=False
)


class GitHubCodeDestinationTypeDef(
    _RequiredGitHubCodeDestinationTypeDef, _OptionalGitHubCodeDestinationTypeDef
):
    pass


CodeDestinationTypeDef = TypedDict(
    "CodeDestinationTypeDef",
    {"codeCommit": CodeCommitCodeDestinationTypeDef, "gitHub": GitHubCodeDestinationTypeDef},
    total=False,
)

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef", {"bucketName": str, "bucketKey": str}, total=False
)

CodeSourceTypeDef = TypedDict("CodeSourceTypeDef", {"s3": S3LocationTypeDef})

CodeTypeDef = TypedDict(
    "CodeTypeDef", {"source": CodeSourceTypeDef, "destination": CodeDestinationTypeDef}
)

_RequiredCreateProjectResultTypeDef = TypedDict(
    "_RequiredCreateProjectResultTypeDef", {"id": str, "arn": str}
)
_OptionalCreateProjectResultTypeDef = TypedDict(
    "_OptionalCreateProjectResultTypeDef",
    {"clientRequestToken": str, "projectTemplateId": str},
    total=False,
)


class CreateProjectResultTypeDef(
    _RequiredCreateProjectResultTypeDef, _OptionalCreateProjectResultTypeDef
):
    pass


_RequiredCreateUserProfileResultTypeDef = TypedDict(
    "_RequiredCreateUserProfileResultTypeDef", {"userArn": str}
)
_OptionalCreateUserProfileResultTypeDef = TypedDict(
    "_OptionalCreateUserProfileResultTypeDef",
    {
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
    },
    total=False,
)


class CreateUserProfileResultTypeDef(
    _RequiredCreateUserProfileResultTypeDef, _OptionalCreateUserProfileResultTypeDef
):
    pass


DeleteProjectResultTypeDef = TypedDict(
    "DeleteProjectResultTypeDef", {"stackId": str, "projectArn": str}, total=False
)

DeleteUserProfileResultTypeDef = TypedDict("DeleteUserProfileResultTypeDef", {"userArn": str})

_RequiredProjectStatusTypeDef = TypedDict("_RequiredProjectStatusTypeDef", {"state": str})
_OptionalProjectStatusTypeDef = TypedDict(
    "_OptionalProjectStatusTypeDef", {"reason": str}, total=False
)


class ProjectStatusTypeDef(_RequiredProjectStatusTypeDef, _OptionalProjectStatusTypeDef):
    pass


DescribeProjectResultTypeDef = TypedDict(
    "DescribeProjectResultTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "description": str,
        "clientRequestToken": str,
        "createdTimeStamp": datetime,
        "stackId": str,
        "projectTemplateId": str,
        "status": ProjectStatusTypeDef,
    },
    total=False,
)

_RequiredDescribeUserProfileResultTypeDef = TypedDict(
    "_RequiredDescribeUserProfileResultTypeDef",
    {"userArn": str, "createdTimestamp": datetime, "lastModifiedTimestamp": datetime},
)
_OptionalDescribeUserProfileResultTypeDef = TypedDict(
    "_OptionalDescribeUserProfileResultTypeDef",
    {"displayName": str, "emailAddress": str, "sshPublicKey": str},
    total=False,
)


class DescribeUserProfileResultTypeDef(
    _RequiredDescribeUserProfileResultTypeDef, _OptionalDescribeUserProfileResultTypeDef
):
    pass


ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef", {"projectId": str, "projectArn": str}, total=False
)

_RequiredListProjectsResultTypeDef = TypedDict(
    "_RequiredListProjectsResultTypeDef", {"projects": List[ProjectSummaryTypeDef]}
)
_OptionalListProjectsResultTypeDef = TypedDict(
    "_OptionalListProjectsResultTypeDef", {"nextToken": str}, total=False
)


class ListProjectsResultTypeDef(
    _RequiredListProjectsResultTypeDef, _OptionalListProjectsResultTypeDef
):
    pass


ResourceTypeDef = TypedDict("ResourceTypeDef", {"id": str})

ListResourcesResultTypeDef = TypedDict(
    "ListResourcesResultTypeDef",
    {"resources": List[ResourceTypeDef], "nextToken": str},
    total=False,
)

ListTagsForProjectResultTypeDef = TypedDict(
    "ListTagsForProjectResultTypeDef", {"tags": Dict[str, str], "nextToken": str}, total=False
)

_RequiredTeamMemberTypeDef = TypedDict(
    "_RequiredTeamMemberTypeDef", {"userArn": str, "projectRole": str}
)
_OptionalTeamMemberTypeDef = TypedDict(
    "_OptionalTeamMemberTypeDef", {"remoteAccessAllowed": bool}, total=False
)


class TeamMemberTypeDef(_RequiredTeamMemberTypeDef, _OptionalTeamMemberTypeDef):
    pass


_RequiredListTeamMembersResultTypeDef = TypedDict(
    "_RequiredListTeamMembersResultTypeDef", {"teamMembers": List[TeamMemberTypeDef]}
)
_OptionalListTeamMembersResultTypeDef = TypedDict(
    "_OptionalListTeamMembersResultTypeDef", {"nextToken": str}, total=False
)


class ListTeamMembersResultTypeDef(
    _RequiredListTeamMembersResultTypeDef, _OptionalListTeamMembersResultTypeDef
):
    pass


UserProfileSummaryTypeDef = TypedDict(
    "UserProfileSummaryTypeDef",
    {"userArn": str, "displayName": str, "emailAddress": str, "sshPublicKey": str},
    total=False,
)

_RequiredListUserProfilesResultTypeDef = TypedDict(
    "_RequiredListUserProfilesResultTypeDef", {"userProfiles": List[UserProfileSummaryTypeDef]}
)
_OptionalListUserProfilesResultTypeDef = TypedDict(
    "_OptionalListUserProfilesResultTypeDef", {"nextToken": str}, total=False
)


class ListUserProfilesResultTypeDef(
    _RequiredListUserProfilesResultTypeDef, _OptionalListUserProfilesResultTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

TagProjectResultTypeDef = TypedDict(
    "TagProjectResultTypeDef", {"tags": Dict[str, str]}, total=False
)

ToolchainSourceTypeDef = TypedDict("ToolchainSourceTypeDef", {"s3": S3LocationTypeDef})

_RequiredToolchainTypeDef = TypedDict(
    "_RequiredToolchainTypeDef", {"source": ToolchainSourceTypeDef}
)
_OptionalToolchainTypeDef = TypedDict(
    "_OptionalToolchainTypeDef", {"roleArn": str, "stackParameters": Dict[str, str]}, total=False
)


class ToolchainTypeDef(_RequiredToolchainTypeDef, _OptionalToolchainTypeDef):
    pass


UpdateTeamMemberResultTypeDef = TypedDict(
    "UpdateTeamMemberResultTypeDef",
    {"userArn": str, "projectRole": str, "remoteAccessAllowed": bool},
    total=False,
)

_RequiredUpdateUserProfileResultTypeDef = TypedDict(
    "_RequiredUpdateUserProfileResultTypeDef", {"userArn": str}
)
_OptionalUpdateUserProfileResultTypeDef = TypedDict(
    "_OptionalUpdateUserProfileResultTypeDef",
    {
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
    },
    total=False,
)


class UpdateUserProfileResultTypeDef(
    _RequiredUpdateUserProfileResultTypeDef, _OptionalUpdateUserProfileResultTypeDef
):
    pass
