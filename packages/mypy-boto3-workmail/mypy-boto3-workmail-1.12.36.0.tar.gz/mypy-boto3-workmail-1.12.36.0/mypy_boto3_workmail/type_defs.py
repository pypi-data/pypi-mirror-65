"""
Main interface for workmail service type definitions.

Usage::

    from mypy_boto3.workmail.type_defs import BookingOptionsTypeDef

    data: BookingOptionsTypeDef = {...}
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
    "BookingOptionsTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateResourceResponseTypeDef",
    "CreateUserResponseTypeDef",
    "DescribeGroupResponseTypeDef",
    "DescribeOrganizationResponseTypeDef",
    "DescribeResourceResponseTypeDef",
    "DescribeUserResponseTypeDef",
    "GetAccessControlEffectResponseTypeDef",
    "GetMailboxDetailsResponseTypeDef",
    "AccessControlRuleTypeDef",
    "ListAccessControlRulesResponseTypeDef",
    "ListAliasesResponseTypeDef",
    "MemberTypeDef",
    "ListGroupMembersResponseTypeDef",
    "GroupTypeDef",
    "ListGroupsResponseTypeDef",
    "PermissionTypeDef",
    "ListMailboxPermissionsResponseTypeDef",
    "OrganizationSummaryTypeDef",
    "ListOrganizationsResponseTypeDef",
    "DelegateTypeDef",
    "ListResourceDelegatesResponseTypeDef",
    "ResourceTypeDef",
    "ListResourcesResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UserTypeDef",
    "ListUsersResponseTypeDef",
    "PaginatorConfigTypeDef",
)

BookingOptionsTypeDef = TypedDict(
    "BookingOptionsTypeDef",
    {
        "AutoAcceptRequests": bool,
        "AutoDeclineRecurringRequests": bool,
        "AutoDeclineConflictingRequests": bool,
    },
    total=False,
)

CreateGroupResponseTypeDef = TypedDict("CreateGroupResponseTypeDef", {"GroupId": str}, total=False)

CreateResourceResponseTypeDef = TypedDict(
    "CreateResourceResponseTypeDef", {"ResourceId": str}, total=False
)

CreateUserResponseTypeDef = TypedDict("CreateUserResponseTypeDef", {"UserId": str}, total=False)

DescribeGroupResponseTypeDef = TypedDict(
    "DescribeGroupResponseTypeDef",
    {
        "GroupId": str,
        "Name": str,
        "Email": str,
        "State": Literal["ENABLED", "DISABLED", "DELETED"],
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

DescribeOrganizationResponseTypeDef = TypedDict(
    "DescribeOrganizationResponseTypeDef",
    {
        "OrganizationId": str,
        "Alias": str,
        "State": str,
        "DirectoryId": str,
        "DirectoryType": str,
        "DefaultMailDomain": str,
        "CompletedDate": datetime,
        "ErrorMessage": str,
        "ARN": str,
    },
    total=False,
)

DescribeResourceResponseTypeDef = TypedDict(
    "DescribeResourceResponseTypeDef",
    {
        "ResourceId": str,
        "Email": str,
        "Name": str,
        "Type": Literal["ROOM", "EQUIPMENT"],
        "BookingOptions": BookingOptionsTypeDef,
        "State": Literal["ENABLED", "DISABLED", "DELETED"],
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {
        "UserId": str,
        "Name": str,
        "Email": str,
        "DisplayName": str,
        "State": Literal["ENABLED", "DISABLED", "DELETED"],
        "UserRole": Literal["USER", "RESOURCE", "SYSTEM_USER"],
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

GetAccessControlEffectResponseTypeDef = TypedDict(
    "GetAccessControlEffectResponseTypeDef",
    {"Effect": Literal["ALLOW", "DENY"], "MatchedRules": List[str]},
    total=False,
)

GetMailboxDetailsResponseTypeDef = TypedDict(
    "GetMailboxDetailsResponseTypeDef", {"MailboxQuota": int, "MailboxSize": float}, total=False
)

AccessControlRuleTypeDef = TypedDict(
    "AccessControlRuleTypeDef",
    {
        "Name": str,
        "Effect": Literal["ALLOW", "DENY"],
        "Description": str,
        "IpRanges": List[str],
        "NotIpRanges": List[str],
        "Actions": List[str],
        "NotActions": List[str],
        "UserIds": List[str],
        "NotUserIds": List[str],
        "DateCreated": datetime,
        "DateModified": datetime,
    },
    total=False,
)

ListAccessControlRulesResponseTypeDef = TypedDict(
    "ListAccessControlRulesResponseTypeDef", {"Rules": List[AccessControlRuleTypeDef]}, total=False
)

ListAliasesResponseTypeDef = TypedDict(
    "ListAliasesResponseTypeDef", {"Aliases": List[str], "NextToken": str}, total=False
)

MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "Id": str,
        "Name": str,
        "Type": Literal["GROUP", "USER"],
        "State": Literal["ENABLED", "DISABLED", "DELETED"],
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

ListGroupMembersResponseTypeDef = TypedDict(
    "ListGroupMembersResponseTypeDef",
    {"Members": List[MemberTypeDef], "NextToken": str},
    total=False,
)

GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "Id": str,
        "Email": str,
        "Name": str,
        "State": Literal["ENABLED", "DISABLED", "DELETED"],
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef", {"Groups": List[GroupTypeDef], "NextToken": str}, total=False
)

PermissionTypeDef = TypedDict(
    "PermissionTypeDef",
    {
        "GranteeId": str,
        "GranteeType": Literal["GROUP", "USER"],
        "PermissionValues": List[Literal["FULL_ACCESS", "SEND_AS", "SEND_ON_BEHALF"]],
    },
)

ListMailboxPermissionsResponseTypeDef = TypedDict(
    "ListMailboxPermissionsResponseTypeDef",
    {"Permissions": List[PermissionTypeDef], "NextToken": str},
    total=False,
)

OrganizationSummaryTypeDef = TypedDict(
    "OrganizationSummaryTypeDef",
    {"OrganizationId": str, "Alias": str, "ErrorMessage": str, "State": str},
    total=False,
)

ListOrganizationsResponseTypeDef = TypedDict(
    "ListOrganizationsResponseTypeDef",
    {"OrganizationSummaries": List[OrganizationSummaryTypeDef], "NextToken": str},
    total=False,
)

DelegateTypeDef = TypedDict("DelegateTypeDef", {"Id": str, "Type": Literal["GROUP", "USER"]})

ListResourceDelegatesResponseTypeDef = TypedDict(
    "ListResourceDelegatesResponseTypeDef",
    {"Delegates": List[DelegateTypeDef], "NextToken": str},
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "Id": str,
        "Email": str,
        "Name": str,
        "Type": Literal["ROOM", "EQUIPMENT"],
        "State": Literal["ENABLED", "DISABLED", "DELETED"],
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

ListResourcesResponseTypeDef = TypedDict(
    "ListResourcesResponseTypeDef",
    {"Resources": List[ResourceTypeDef], "NextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef]}, total=False
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Id": str,
        "Email": str,
        "Name": str,
        "DisplayName": str,
        "State": Literal["ENABLED", "DISABLED", "DELETED"],
        "UserRole": Literal["USER", "RESOURCE", "SYSTEM_USER"],
        "EnabledDate": datetime,
        "DisabledDate": datetime,
    },
    total=False,
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef", {"Users": List[UserTypeDef], "NextToken": str}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
