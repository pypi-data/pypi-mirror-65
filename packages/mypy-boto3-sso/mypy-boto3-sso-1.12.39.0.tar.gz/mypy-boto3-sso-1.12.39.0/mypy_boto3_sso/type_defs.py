"""
Main interface for sso service type definitions.

Usage::

    from mypy_boto3.sso.type_defs import RoleCredentialsTypeDef

    data: RoleCredentialsTypeDef = {...}
"""
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "RoleCredentialsTypeDef",
    "GetRoleCredentialsResponseTypeDef",
    "RoleInfoTypeDef",
    "ListAccountRolesResponseTypeDef",
    "AccountInfoTypeDef",
    "ListAccountsResponseTypeDef",
    "PaginatorConfigTypeDef",
)

RoleCredentialsTypeDef = TypedDict(
    "RoleCredentialsTypeDef",
    {"accessKeyId": str, "secretAccessKey": str, "sessionToken": str, "expiration": int},
    total=False,
)

GetRoleCredentialsResponseTypeDef = TypedDict(
    "GetRoleCredentialsResponseTypeDef", {"roleCredentials": RoleCredentialsTypeDef}, total=False
)

RoleInfoTypeDef = TypedDict("RoleInfoTypeDef", {"roleName": str, "accountId": str}, total=False)

ListAccountRolesResponseTypeDef = TypedDict(
    "ListAccountRolesResponseTypeDef",
    {"nextToken": str, "roleList": List[RoleInfoTypeDef]},
    total=False,
)

AccountInfoTypeDef = TypedDict(
    "AccountInfoTypeDef", {"accountId": str, "accountName": str, "emailAddress": str}, total=False
)

ListAccountsResponseTypeDef = TypedDict(
    "ListAccountsResponseTypeDef",
    {"nextToken": str, "accountList": List[AccountInfoTypeDef]},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
