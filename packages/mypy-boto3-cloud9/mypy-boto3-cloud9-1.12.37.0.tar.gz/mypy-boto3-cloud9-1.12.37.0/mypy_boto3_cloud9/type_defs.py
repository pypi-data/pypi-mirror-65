"""
Main interface for cloud9 service type definitions.

Usage::

    from mypy_boto3.cloud9.type_defs import CreateEnvironmentEC2ResultTypeDef

    data: CreateEnvironmentEC2ResultTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CreateEnvironmentEC2ResultTypeDef",
    "EnvironmentMemberTypeDef",
    "CreateEnvironmentMembershipResultTypeDef",
    "DescribeEnvironmentMembershipsResultTypeDef",
    "DescribeEnvironmentStatusResultTypeDef",
    "EnvironmentLifecycleTypeDef",
    "EnvironmentTypeDef",
    "DescribeEnvironmentsResultTypeDef",
    "ListEnvironmentsResultTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "UpdateEnvironmentMembershipResultTypeDef",
)

CreateEnvironmentEC2ResultTypeDef = TypedDict(
    "CreateEnvironmentEC2ResultTypeDef", {"environmentId": str}, total=False
)

EnvironmentMemberTypeDef = TypedDict(
    "EnvironmentMemberTypeDef",
    {
        "permissions": Literal["owner", "read-write", "read-only"],
        "userId": str,
        "userArn": str,
        "environmentId": str,
        "lastAccess": datetime,
    },
    total=False,
)

CreateEnvironmentMembershipResultTypeDef = TypedDict(
    "CreateEnvironmentMembershipResultTypeDef",
    {"membership": EnvironmentMemberTypeDef},
    total=False,
)

DescribeEnvironmentMembershipsResultTypeDef = TypedDict(
    "DescribeEnvironmentMembershipsResultTypeDef",
    {"memberships": List[EnvironmentMemberTypeDef], "nextToken": str},
    total=False,
)

DescribeEnvironmentStatusResultTypeDef = TypedDict(
    "DescribeEnvironmentStatusResultTypeDef",
    {
        "status": Literal[
            "error", "creating", "connecting", "ready", "stopping", "stopped", "deleting"
        ],
        "message": str,
    },
    total=False,
)

EnvironmentLifecycleTypeDef = TypedDict(
    "EnvironmentLifecycleTypeDef",
    {
        "status": Literal["CREATING", "CREATED", "CREATE_FAILED", "DELETING", "DELETE_FAILED"],
        "reason": str,
        "failureResource": str,
    },
    total=False,
)

EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "type": Literal["ssh", "ec2"],
        "arn": str,
        "ownerArn": str,
        "lifecycle": EnvironmentLifecycleTypeDef,
    },
    total=False,
)

DescribeEnvironmentsResultTypeDef = TypedDict(
    "DescribeEnvironmentsResultTypeDef", {"environments": List[EnvironmentTypeDef]}, total=False
)

ListEnvironmentsResultTypeDef = TypedDict(
    "ListEnvironmentsResultTypeDef", {"nextToken": str, "environmentIds": List[str]}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

UpdateEnvironmentMembershipResultTypeDef = TypedDict(
    "UpdateEnvironmentMembershipResultTypeDef",
    {"membership": EnvironmentMemberTypeDef},
    total=False,
)
