"""
Main interface for organizations service type definitions.

Usage::

    from mypy_boto3.organizations.type_defs import HandshakePartyTypeDef

    data: HandshakePartyTypeDef = {...}
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
    "HandshakePartyTypeDef",
    "HandshakeResourceTypeDef",
    "HandshakeTypeDef",
    "AcceptHandshakeResponseTypeDef",
    "CancelHandshakeResponseTypeDef",
    "CreateAccountStatusTypeDef",
    "CreateAccountResponseTypeDef",
    "CreateGovCloudAccountResponseTypeDef",
    "PolicyTypeSummaryTypeDef",
    "OrganizationTypeDef",
    "CreateOrganizationResponseTypeDef",
    "OrganizationalUnitTypeDef",
    "CreateOrganizationalUnitResponseTypeDef",
    "PolicySummaryTypeDef",
    "PolicyTypeDef",
    "CreatePolicyResponseTypeDef",
    "DeclineHandshakeResponseTypeDef",
    "AccountTypeDef",
    "DescribeAccountResponseTypeDef",
    "DescribeCreateAccountStatusResponseTypeDef",
    "EffectivePolicyTypeDef",
    "DescribeEffectivePolicyResponseTypeDef",
    "DescribeHandshakeResponseTypeDef",
    "DescribeOrganizationResponseTypeDef",
    "DescribeOrganizationalUnitResponseTypeDef",
    "DescribePolicyResponseTypeDef",
    "RootTypeDef",
    "DisablePolicyTypeResponseTypeDef",
    "EnableAllFeaturesResponseTypeDef",
    "EnablePolicyTypeResponseTypeDef",
    "HandshakeFilterTypeDef",
    "InviteAccountToOrganizationResponseTypeDef",
    "EnabledServicePrincipalTypeDef",
    "ListAWSServiceAccessForOrganizationResponseTypeDef",
    "ListAccountsForParentResponseTypeDef",
    "ListAccountsResponseTypeDef",
    "ChildTypeDef",
    "ListChildrenResponseTypeDef",
    "ListCreateAccountStatusResponseTypeDef",
    "DelegatedAdministratorTypeDef",
    "ListDelegatedAdministratorsResponseTypeDef",
    "DelegatedServiceTypeDef",
    "ListDelegatedServicesForAccountResponseTypeDef",
    "ListHandshakesForAccountResponseTypeDef",
    "ListHandshakesForOrganizationResponseTypeDef",
    "ListOrganizationalUnitsForParentResponseTypeDef",
    "ParentTypeDef",
    "ListParentsResponseTypeDef",
    "ListPoliciesForTargetResponseTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListRootsResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PolicyTargetSummaryTypeDef",
    "ListTargetsForPolicyResponseTypeDef",
    "PaginatorConfigTypeDef",
    "UpdateOrganizationalUnitResponseTypeDef",
    "UpdatePolicyResponseTypeDef",
)

HandshakePartyTypeDef = TypedDict(
    "HandshakePartyTypeDef", {"Id": str, "Type": Literal["ACCOUNT", "ORGANIZATION", "EMAIL"]}
)

HandshakeResourceTypeDef = TypedDict(
    "HandshakeResourceTypeDef",
    {
        "Value": str,
        "Type": Literal[
            "ACCOUNT",
            "ORGANIZATION",
            "ORGANIZATION_FEATURE_SET",
            "EMAIL",
            "MASTER_EMAIL",
            "MASTER_NAME",
            "NOTES",
            "PARENT_HANDSHAKE",
        ],
        "Resources": List["HandshakeResourceTypeDef"],
    },
    total=False,
)

HandshakeTypeDef = TypedDict(
    "HandshakeTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Parties": List[HandshakePartyTypeDef],
        "State": Literal["REQUESTED", "OPEN", "CANCELED", "ACCEPTED", "DECLINED", "EXPIRED"],
        "RequestedTimestamp": datetime,
        "ExpirationTimestamp": datetime,
        "Action": Literal[
            "INVITE",
            "ENABLE_ALL_FEATURES",
            "APPROVE_ALL_FEATURES",
            "ADD_ORGANIZATIONS_SERVICE_LINKED_ROLE",
        ],
        "Resources": List[HandshakeResourceTypeDef],
    },
    total=False,
)

AcceptHandshakeResponseTypeDef = TypedDict(
    "AcceptHandshakeResponseTypeDef", {"Handshake": HandshakeTypeDef}, total=False
)

CancelHandshakeResponseTypeDef = TypedDict(
    "CancelHandshakeResponseTypeDef", {"Handshake": HandshakeTypeDef}, total=False
)

CreateAccountStatusTypeDef = TypedDict(
    "CreateAccountStatusTypeDef",
    {
        "Id": str,
        "AccountName": str,
        "State": Literal["IN_PROGRESS", "SUCCEEDED", "FAILED"],
        "RequestedTimestamp": datetime,
        "CompletedTimestamp": datetime,
        "AccountId": str,
        "GovCloudAccountId": str,
        "FailureReason": Literal[
            "ACCOUNT_LIMIT_EXCEEDED",
            "EMAIL_ALREADY_EXISTS",
            "INVALID_ADDRESS",
            "INVALID_EMAIL",
            "CONCURRENT_ACCOUNT_MODIFICATION",
            "INTERNAL_FAILURE",
            "GOVCLOUD_ACCOUNT_ALREADY_EXISTS",
        ],
    },
    total=False,
)

CreateAccountResponseTypeDef = TypedDict(
    "CreateAccountResponseTypeDef", {"CreateAccountStatus": CreateAccountStatusTypeDef}, total=False
)

CreateGovCloudAccountResponseTypeDef = TypedDict(
    "CreateGovCloudAccountResponseTypeDef",
    {"CreateAccountStatus": CreateAccountStatusTypeDef},
    total=False,
)

PolicyTypeSummaryTypeDef = TypedDict(
    "PolicyTypeSummaryTypeDef",
    {
        "Type": Literal["SERVICE_CONTROL_POLICY", "TAG_POLICY"],
        "Status": Literal["ENABLED", "PENDING_ENABLE", "PENDING_DISABLE"],
    },
    total=False,
)

OrganizationTypeDef = TypedDict(
    "OrganizationTypeDef",
    {
        "Id": str,
        "Arn": str,
        "FeatureSet": Literal["ALL", "CONSOLIDATED_BILLING"],
        "MasterAccountArn": str,
        "MasterAccountId": str,
        "MasterAccountEmail": str,
        "AvailablePolicyTypes": List[PolicyTypeSummaryTypeDef],
    },
    total=False,
)

CreateOrganizationResponseTypeDef = TypedDict(
    "CreateOrganizationResponseTypeDef", {"Organization": OrganizationTypeDef}, total=False
)

OrganizationalUnitTypeDef = TypedDict(
    "OrganizationalUnitTypeDef", {"Id": str, "Arn": str, "Name": str}, total=False
)

CreateOrganizationalUnitResponseTypeDef = TypedDict(
    "CreateOrganizationalUnitResponseTypeDef",
    {"OrganizationalUnit": OrganizationalUnitTypeDef},
    total=False,
)

PolicySummaryTypeDef = TypedDict(
    "PolicySummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "Type": Literal["SERVICE_CONTROL_POLICY", "TAG_POLICY"],
        "AwsManaged": bool,
    },
    total=False,
)

PolicyTypeDef = TypedDict(
    "PolicyTypeDef", {"PolicySummary": PolicySummaryTypeDef, "Content": str}, total=False
)

CreatePolicyResponseTypeDef = TypedDict(
    "CreatePolicyResponseTypeDef", {"Policy": PolicyTypeDef}, total=False
)

DeclineHandshakeResponseTypeDef = TypedDict(
    "DeclineHandshakeResponseTypeDef", {"Handshake": HandshakeTypeDef}, total=False
)

AccountTypeDef = TypedDict(
    "AccountTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Email": str,
        "Name": str,
        "Status": Literal["ACTIVE", "SUSPENDED"],
        "JoinedMethod": Literal["INVITED", "CREATED"],
        "JoinedTimestamp": datetime,
    },
    total=False,
)

DescribeAccountResponseTypeDef = TypedDict(
    "DescribeAccountResponseTypeDef", {"Account": AccountTypeDef}, total=False
)

DescribeCreateAccountStatusResponseTypeDef = TypedDict(
    "DescribeCreateAccountStatusResponseTypeDef",
    {"CreateAccountStatus": CreateAccountStatusTypeDef},
    total=False,
)

EffectivePolicyTypeDef = TypedDict(
    "EffectivePolicyTypeDef",
    {
        "PolicyContent": str,
        "LastUpdatedTimestamp": datetime,
        "TargetId": str,
        "PolicyType": Literal["TAG_POLICY"],
    },
    total=False,
)

DescribeEffectivePolicyResponseTypeDef = TypedDict(
    "DescribeEffectivePolicyResponseTypeDef",
    {"EffectivePolicy": EffectivePolicyTypeDef},
    total=False,
)

DescribeHandshakeResponseTypeDef = TypedDict(
    "DescribeHandshakeResponseTypeDef", {"Handshake": HandshakeTypeDef}, total=False
)

DescribeOrganizationResponseTypeDef = TypedDict(
    "DescribeOrganizationResponseTypeDef", {"Organization": OrganizationTypeDef}, total=False
)

DescribeOrganizationalUnitResponseTypeDef = TypedDict(
    "DescribeOrganizationalUnitResponseTypeDef",
    {"OrganizationalUnit": OrganizationalUnitTypeDef},
    total=False,
)

DescribePolicyResponseTypeDef = TypedDict(
    "DescribePolicyResponseTypeDef", {"Policy": PolicyTypeDef}, total=False
)

RootTypeDef = TypedDict(
    "RootTypeDef",
    {"Id": str, "Arn": str, "Name": str, "PolicyTypes": List[PolicyTypeSummaryTypeDef]},
    total=False,
)

DisablePolicyTypeResponseTypeDef = TypedDict(
    "DisablePolicyTypeResponseTypeDef", {"Root": RootTypeDef}, total=False
)

EnableAllFeaturesResponseTypeDef = TypedDict(
    "EnableAllFeaturesResponseTypeDef", {"Handshake": HandshakeTypeDef}, total=False
)

EnablePolicyTypeResponseTypeDef = TypedDict(
    "EnablePolicyTypeResponseTypeDef", {"Root": RootTypeDef}, total=False
)

HandshakeFilterTypeDef = TypedDict(
    "HandshakeFilterTypeDef",
    {
        "ActionType": Literal[
            "INVITE",
            "ENABLE_ALL_FEATURES",
            "APPROVE_ALL_FEATURES",
            "ADD_ORGANIZATIONS_SERVICE_LINKED_ROLE",
        ],
        "ParentHandshakeId": str,
    },
    total=False,
)

InviteAccountToOrganizationResponseTypeDef = TypedDict(
    "InviteAccountToOrganizationResponseTypeDef", {"Handshake": HandshakeTypeDef}, total=False
)

EnabledServicePrincipalTypeDef = TypedDict(
    "EnabledServicePrincipalTypeDef",
    {"ServicePrincipal": str, "DateEnabled": datetime},
    total=False,
)

ListAWSServiceAccessForOrganizationResponseTypeDef = TypedDict(
    "ListAWSServiceAccessForOrganizationResponseTypeDef",
    {"EnabledServicePrincipals": List[EnabledServicePrincipalTypeDef], "NextToken": str},
    total=False,
)

ListAccountsForParentResponseTypeDef = TypedDict(
    "ListAccountsForParentResponseTypeDef",
    {"Accounts": List[AccountTypeDef], "NextToken": str},
    total=False,
)

ListAccountsResponseTypeDef = TypedDict(
    "ListAccountsResponseTypeDef", {"Accounts": List[AccountTypeDef], "NextToken": str}, total=False
)

ChildTypeDef = TypedDict(
    "ChildTypeDef", {"Id": str, "Type": Literal["ACCOUNT", "ORGANIZATIONAL_UNIT"]}, total=False
)

ListChildrenResponseTypeDef = TypedDict(
    "ListChildrenResponseTypeDef", {"Children": List[ChildTypeDef], "NextToken": str}, total=False
)

ListCreateAccountStatusResponseTypeDef = TypedDict(
    "ListCreateAccountStatusResponseTypeDef",
    {"CreateAccountStatuses": List[CreateAccountStatusTypeDef], "NextToken": str},
    total=False,
)

DelegatedAdministratorTypeDef = TypedDict(
    "DelegatedAdministratorTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Email": str,
        "Name": str,
        "Status": Literal["ACTIVE", "SUSPENDED"],
        "JoinedMethod": Literal["INVITED", "CREATED"],
        "JoinedTimestamp": datetime,
        "DelegationEnabledDate": datetime,
    },
    total=False,
)

ListDelegatedAdministratorsResponseTypeDef = TypedDict(
    "ListDelegatedAdministratorsResponseTypeDef",
    {"DelegatedAdministrators": List[DelegatedAdministratorTypeDef], "NextToken": str},
    total=False,
)

DelegatedServiceTypeDef = TypedDict(
    "DelegatedServiceTypeDef",
    {"ServicePrincipal": str, "DelegationEnabledDate": datetime},
    total=False,
)

ListDelegatedServicesForAccountResponseTypeDef = TypedDict(
    "ListDelegatedServicesForAccountResponseTypeDef",
    {"DelegatedServices": List[DelegatedServiceTypeDef], "NextToken": str},
    total=False,
)

ListHandshakesForAccountResponseTypeDef = TypedDict(
    "ListHandshakesForAccountResponseTypeDef",
    {"Handshakes": List[HandshakeTypeDef], "NextToken": str},
    total=False,
)

ListHandshakesForOrganizationResponseTypeDef = TypedDict(
    "ListHandshakesForOrganizationResponseTypeDef",
    {"Handshakes": List[HandshakeTypeDef], "NextToken": str},
    total=False,
)

ListOrganizationalUnitsForParentResponseTypeDef = TypedDict(
    "ListOrganizationalUnitsForParentResponseTypeDef",
    {"OrganizationalUnits": List[OrganizationalUnitTypeDef], "NextToken": str},
    total=False,
)

ParentTypeDef = TypedDict(
    "ParentTypeDef", {"Id": str, "Type": Literal["ROOT", "ORGANIZATIONAL_UNIT"]}, total=False
)

ListParentsResponseTypeDef = TypedDict(
    "ListParentsResponseTypeDef", {"Parents": List[ParentTypeDef], "NextToken": str}, total=False
)

ListPoliciesForTargetResponseTypeDef = TypedDict(
    "ListPoliciesForTargetResponseTypeDef",
    {"Policies": List[PolicySummaryTypeDef], "NextToken": str},
    total=False,
)

ListPoliciesResponseTypeDef = TypedDict(
    "ListPoliciesResponseTypeDef",
    {"Policies": List[PolicySummaryTypeDef], "NextToken": str},
    total=False,
)

ListRootsResponseTypeDef = TypedDict(
    "ListRootsResponseTypeDef", {"Roots": List[RootTypeDef], "NextToken": str}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef], "NextToken": str}, total=False
)

PolicyTargetSummaryTypeDef = TypedDict(
    "PolicyTargetSummaryTypeDef",
    {
        "TargetId": str,
        "Arn": str,
        "Name": str,
        "Type": Literal["ACCOUNT", "ORGANIZATIONAL_UNIT", "ROOT"],
    },
    total=False,
)

ListTargetsForPolicyResponseTypeDef = TypedDict(
    "ListTargetsForPolicyResponseTypeDef",
    {"Targets": List[PolicyTargetSummaryTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

UpdateOrganizationalUnitResponseTypeDef = TypedDict(
    "UpdateOrganizationalUnitResponseTypeDef",
    {"OrganizationalUnit": OrganizationalUnitTypeDef},
    total=False,
)

UpdatePolicyResponseTypeDef = TypedDict(
    "UpdatePolicyResponseTypeDef", {"Policy": PolicyTypeDef}, total=False
)
