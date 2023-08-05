"""
Main interface for iam service type definitions.

Usage::

    from mypy_boto3.iam.type_defs import ContextEntryTypeDef

    data: ContextEntryTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ContextEntryTypeDef",
    "AccessKeyTypeDef",
    "CreateAccessKeyResponseTypeDef",
    "GroupTypeDef",
    "CreateGroupResponseTypeDef",
    "AttachedPermissionsBoundaryTypeDef",
    "RoleLastUsedTypeDef",
    "TagTypeDef",
    "RoleTypeDef",
    "InstanceProfileTypeDef",
    "CreateInstanceProfileResponseTypeDef",
    "LoginProfileTypeDef",
    "CreateLoginProfileResponseTypeDef",
    "CreateOpenIDConnectProviderResponseTypeDef",
    "PolicyTypeDef",
    "CreatePolicyResponseTypeDef",
    "PolicyVersionTypeDef",
    "CreatePolicyVersionResponseTypeDef",
    "CreateRoleResponseTypeDef",
    "CreateSAMLProviderResponseTypeDef",
    "CreateServiceLinkedRoleResponseTypeDef",
    "ServiceSpecificCredentialTypeDef",
    "CreateServiceSpecificCredentialResponseTypeDef",
    "UserTypeDef",
    "CreateUserResponseTypeDef",
    "VirtualMFADeviceTypeDef",
    "CreateVirtualMFADeviceResponseTypeDef",
    "DeleteServiceLinkedRoleResponseTypeDef",
    "GenerateCredentialReportResponseTypeDef",
    "GenerateOrganizationsAccessReportResponseTypeDef",
    "GenerateServiceLastAccessedDetailsResponseTypeDef",
    "AccessKeyLastUsedTypeDef",
    "GetAccessKeyLastUsedResponseTypeDef",
    "AttachedPolicyTypeDef",
    "PolicyDetailTypeDef",
    "GroupDetailTypeDef",
    "ManagedPolicyDetailTypeDef",
    "RoleDetailTypeDef",
    "UserDetailTypeDef",
    "GetAccountAuthorizationDetailsResponseTypeDef",
    "PasswordPolicyTypeDef",
    "GetAccountPasswordPolicyResponseTypeDef",
    "GetAccountSummaryResponseTypeDef",
    "GetContextKeysForPolicyResponseTypeDef",
    "GetCredentialReportResponseTypeDef",
    "GetGroupPolicyResponseTypeDef",
    "GetGroupResponseTypeDef",
    "GetInstanceProfileResponseTypeDef",
    "GetLoginProfileResponseTypeDef",
    "GetOpenIDConnectProviderResponseTypeDef",
    "AccessDetailTypeDef",
    "ErrorDetailsTypeDef",
    "GetOrganizationsAccessReportResponseTypeDef",
    "GetPolicyResponseTypeDef",
    "GetPolicyVersionResponseTypeDef",
    "GetRolePolicyResponseTypeDef",
    "GetRoleResponseTypeDef",
    "GetSAMLProviderResponseTypeDef",
    "SSHPublicKeyTypeDef",
    "GetSSHPublicKeyResponseTypeDef",
    "ServerCertificateMetadataTypeDef",
    "ServerCertificateTypeDef",
    "GetServerCertificateResponseTypeDef",
    "ServiceLastAccessedTypeDef",
    "GetServiceLastAccessedDetailsResponseTypeDef",
    "EntityInfoTypeDef",
    "EntityDetailsTypeDef",
    "GetServiceLastAccessedDetailsWithEntitiesResponseTypeDef",
    "RoleUsageTypeTypeDef",
    "DeletionTaskFailureReasonTypeTypeDef",
    "GetServiceLinkedRoleDeletionStatusResponseTypeDef",
    "GetUserPolicyResponseTypeDef",
    "GetUserResponseTypeDef",
    "AccessKeyMetadataTypeDef",
    "ListAccessKeysResponseTypeDef",
    "ListAccountAliasesResponseTypeDef",
    "ListAttachedGroupPoliciesResponseTypeDef",
    "ListAttachedRolePoliciesResponseTypeDef",
    "ListAttachedUserPoliciesResponseTypeDef",
    "PolicyGroupTypeDef",
    "PolicyRoleTypeDef",
    "PolicyUserTypeDef",
    "ListEntitiesForPolicyResponseTypeDef",
    "ListGroupPoliciesResponseTypeDef",
    "ListGroupsForUserResponseTypeDef",
    "ListGroupsResponseTypeDef",
    "ListInstanceProfilesForRoleResponseTypeDef",
    "ListInstanceProfilesResponseTypeDef",
    "MFADeviceTypeDef",
    "ListMFADevicesResponseTypeDef",
    "OpenIDConnectProviderListEntryTypeDef",
    "ListOpenIDConnectProvidersResponseTypeDef",
    "PolicyGrantingServiceAccessTypeDef",
    "ListPoliciesGrantingServiceAccessEntryTypeDef",
    "ListPoliciesGrantingServiceAccessResponseTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListPolicyVersionsResponseTypeDef",
    "ListRolePoliciesResponseTypeDef",
    "ListRoleTagsResponseTypeDef",
    "ListRolesResponseTypeDef",
    "SAMLProviderListEntryTypeDef",
    "ListSAMLProvidersResponseTypeDef",
    "SSHPublicKeyMetadataTypeDef",
    "ListSSHPublicKeysResponseTypeDef",
    "ListServerCertificatesResponseTypeDef",
    "ServiceSpecificCredentialMetadataTypeDef",
    "ListServiceSpecificCredentialsResponseTypeDef",
    "SigningCertificateTypeDef",
    "ListSigningCertificatesResponseTypeDef",
    "ListUserPoliciesResponseTypeDef",
    "ListUserTagsResponseTypeDef",
    "ListUsersResponseTypeDef",
    "ListVirtualMFADevicesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResetServiceSpecificCredentialResponseTypeDef",
    "OrganizationsDecisionDetailTypeDef",
    "PermissionsBoundaryDecisionDetailTypeDef",
    "PositionTypeDef",
    "StatementTypeDef",
    "ResourceSpecificResultTypeDef",
    "EvaluationResultTypeDef",
    "SimulatePolicyResponseTypeDef",
    "UpdateRoleDescriptionResponseTypeDef",
    "UpdateSAMLProviderResponseTypeDef",
    "UploadSSHPublicKeyResponseTypeDef",
    "UploadServerCertificateResponseTypeDef",
    "UploadSigningCertificateResponseTypeDef",
    "WaiterConfigTypeDef",
)

ContextEntryTypeDef = TypedDict(
    "ContextEntryTypeDef",
    {
        "ContextKeyName": str,
        "ContextKeyValues": List[str],
        "ContextKeyType": Literal[
            "string",
            "stringList",
            "numeric",
            "numericList",
            "boolean",
            "booleanList",
            "ip",
            "ipList",
            "binary",
            "binaryList",
            "date",
            "dateList",
        ],
    },
    total=False,
)

_RequiredAccessKeyTypeDef = TypedDict(
    "_RequiredAccessKeyTypeDef",
    {
        "UserName": str,
        "AccessKeyId": str,
        "Status": Literal["Active", "Inactive"],
        "SecretAccessKey": str,
    },
)
_OptionalAccessKeyTypeDef = TypedDict(
    "_OptionalAccessKeyTypeDef", {"CreateDate": datetime}, total=False
)


class AccessKeyTypeDef(_RequiredAccessKeyTypeDef, _OptionalAccessKeyTypeDef):
    pass


CreateAccessKeyResponseTypeDef = TypedDict(
    "CreateAccessKeyResponseTypeDef", {"AccessKey": AccessKeyTypeDef}
)

GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {"Path": str, "GroupName": str, "GroupId": str, "Arn": str, "CreateDate": datetime},
)

CreateGroupResponseTypeDef = TypedDict("CreateGroupResponseTypeDef", {"Group": GroupTypeDef})

AttachedPermissionsBoundaryTypeDef = TypedDict(
    "AttachedPermissionsBoundaryTypeDef",
    {
        "PermissionsBoundaryType": Literal["PermissionsBoundaryPolicy"],
        "PermissionsBoundaryArn": str,
    },
    total=False,
)

RoleLastUsedTypeDef = TypedDict(
    "RoleLastUsedTypeDef", {"LastUsedDate": datetime, "Region": str}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

_RequiredRoleTypeDef = TypedDict(
    "_RequiredRoleTypeDef",
    {"Path": str, "RoleName": str, "RoleId": str, "Arn": str, "CreateDate": datetime},
)
_OptionalRoleTypeDef = TypedDict(
    "_OptionalRoleTypeDef",
    {
        "AssumeRolePolicyDocument": str,
        "Description": str,
        "MaxSessionDuration": int,
        "PermissionsBoundary": AttachedPermissionsBoundaryTypeDef,
        "Tags": List[TagTypeDef],
        "RoleLastUsed": RoleLastUsedTypeDef,
    },
    total=False,
)


class RoleTypeDef(_RequiredRoleTypeDef, _OptionalRoleTypeDef):
    pass


InstanceProfileTypeDef = TypedDict(
    "InstanceProfileTypeDef",
    {
        "Path": str,
        "InstanceProfileName": str,
        "InstanceProfileId": str,
        "Arn": str,
        "CreateDate": datetime,
        "Roles": List[RoleTypeDef],
    },
)

CreateInstanceProfileResponseTypeDef = TypedDict(
    "CreateInstanceProfileResponseTypeDef", {"InstanceProfile": InstanceProfileTypeDef}
)

_RequiredLoginProfileTypeDef = TypedDict(
    "_RequiredLoginProfileTypeDef", {"UserName": str, "CreateDate": datetime}
)
_OptionalLoginProfileTypeDef = TypedDict(
    "_OptionalLoginProfileTypeDef", {"PasswordResetRequired": bool}, total=False
)


class LoginProfileTypeDef(_RequiredLoginProfileTypeDef, _OptionalLoginProfileTypeDef):
    pass


CreateLoginProfileResponseTypeDef = TypedDict(
    "CreateLoginProfileResponseTypeDef", {"LoginProfile": LoginProfileTypeDef}
)

CreateOpenIDConnectProviderResponseTypeDef = TypedDict(
    "CreateOpenIDConnectProviderResponseTypeDef", {"OpenIDConnectProviderArn": str}, total=False
)

PolicyTypeDef = TypedDict(
    "PolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyId": str,
        "Arn": str,
        "Path": str,
        "DefaultVersionId": str,
        "AttachmentCount": int,
        "PermissionsBoundaryUsageCount": int,
        "IsAttachable": bool,
        "Description": str,
        "CreateDate": datetime,
        "UpdateDate": datetime,
    },
    total=False,
)

CreatePolicyResponseTypeDef = TypedDict(
    "CreatePolicyResponseTypeDef", {"Policy": PolicyTypeDef}, total=False
)

PolicyVersionTypeDef = TypedDict(
    "PolicyVersionTypeDef",
    {"Document": str, "VersionId": str, "IsDefaultVersion": bool, "CreateDate": datetime},
    total=False,
)

CreatePolicyVersionResponseTypeDef = TypedDict(
    "CreatePolicyVersionResponseTypeDef", {"PolicyVersion": PolicyVersionTypeDef}, total=False
)

CreateRoleResponseTypeDef = TypedDict("CreateRoleResponseTypeDef", {"Role": RoleTypeDef})

CreateSAMLProviderResponseTypeDef = TypedDict(
    "CreateSAMLProviderResponseTypeDef", {"SAMLProviderArn": str}, total=False
)

CreateServiceLinkedRoleResponseTypeDef = TypedDict(
    "CreateServiceLinkedRoleResponseTypeDef", {"Role": RoleTypeDef}, total=False
)

ServiceSpecificCredentialTypeDef = TypedDict(
    "ServiceSpecificCredentialTypeDef",
    {
        "CreateDate": datetime,
        "ServiceName": str,
        "ServiceUserName": str,
        "ServicePassword": str,
        "ServiceSpecificCredentialId": str,
        "UserName": str,
        "Status": Literal["Active", "Inactive"],
    },
)

CreateServiceSpecificCredentialResponseTypeDef = TypedDict(
    "CreateServiceSpecificCredentialResponseTypeDef",
    {"ServiceSpecificCredential": ServiceSpecificCredentialTypeDef},
    total=False,
)

_RequiredUserTypeDef = TypedDict(
    "_RequiredUserTypeDef",
    {"Path": str, "UserName": str, "UserId": str, "Arn": str, "CreateDate": datetime},
)
_OptionalUserTypeDef = TypedDict(
    "_OptionalUserTypeDef",
    {
        "PasswordLastUsed": datetime,
        "PermissionsBoundary": AttachedPermissionsBoundaryTypeDef,
        "Tags": List[TagTypeDef],
    },
    total=False,
)


class UserTypeDef(_RequiredUserTypeDef, _OptionalUserTypeDef):
    pass


CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef", {"User": UserTypeDef}, total=False
)

_RequiredVirtualMFADeviceTypeDef = TypedDict(
    "_RequiredVirtualMFADeviceTypeDef", {"SerialNumber": str}
)
_OptionalVirtualMFADeviceTypeDef = TypedDict(
    "_OptionalVirtualMFADeviceTypeDef",
    {
        "Base32StringSeed": Union[bytes, IO],
        "QRCodePNG": Union[bytes, IO],
        "User": UserTypeDef,
        "EnableDate": datetime,
    },
    total=False,
)


class VirtualMFADeviceTypeDef(_RequiredVirtualMFADeviceTypeDef, _OptionalVirtualMFADeviceTypeDef):
    pass


CreateVirtualMFADeviceResponseTypeDef = TypedDict(
    "CreateVirtualMFADeviceResponseTypeDef", {"VirtualMFADevice": VirtualMFADeviceTypeDef}
)

DeleteServiceLinkedRoleResponseTypeDef = TypedDict(
    "DeleteServiceLinkedRoleResponseTypeDef", {"DeletionTaskId": str}
)

GenerateCredentialReportResponseTypeDef = TypedDict(
    "GenerateCredentialReportResponseTypeDef",
    {"State": Literal["STARTED", "INPROGRESS", "COMPLETE"], "Description": str},
    total=False,
)

GenerateOrganizationsAccessReportResponseTypeDef = TypedDict(
    "GenerateOrganizationsAccessReportResponseTypeDef", {"JobId": str}, total=False
)

GenerateServiceLastAccessedDetailsResponseTypeDef = TypedDict(
    "GenerateServiceLastAccessedDetailsResponseTypeDef", {"JobId": str}, total=False
)

AccessKeyLastUsedTypeDef = TypedDict(
    "AccessKeyLastUsedTypeDef", {"LastUsedDate": datetime, "ServiceName": str, "Region": str}
)

GetAccessKeyLastUsedResponseTypeDef = TypedDict(
    "GetAccessKeyLastUsedResponseTypeDef",
    {"UserName": str, "AccessKeyLastUsed": AccessKeyLastUsedTypeDef},
    total=False,
)

AttachedPolicyTypeDef = TypedDict(
    "AttachedPolicyTypeDef", {"PolicyName": str, "PolicyArn": str}, total=False
)

PolicyDetailTypeDef = TypedDict(
    "PolicyDetailTypeDef", {"PolicyName": str, "PolicyDocument": str}, total=False
)

GroupDetailTypeDef = TypedDict(
    "GroupDetailTypeDef",
    {
        "Path": str,
        "GroupName": str,
        "GroupId": str,
        "Arn": str,
        "CreateDate": datetime,
        "GroupPolicyList": List[PolicyDetailTypeDef],
        "AttachedManagedPolicies": List[AttachedPolicyTypeDef],
    },
    total=False,
)

ManagedPolicyDetailTypeDef = TypedDict(
    "ManagedPolicyDetailTypeDef",
    {
        "PolicyName": str,
        "PolicyId": str,
        "Arn": str,
        "Path": str,
        "DefaultVersionId": str,
        "AttachmentCount": int,
        "PermissionsBoundaryUsageCount": int,
        "IsAttachable": bool,
        "Description": str,
        "CreateDate": datetime,
        "UpdateDate": datetime,
        "PolicyVersionList": List[PolicyVersionTypeDef],
    },
    total=False,
)

RoleDetailTypeDef = TypedDict(
    "RoleDetailTypeDef",
    {
        "Path": str,
        "RoleName": str,
        "RoleId": str,
        "Arn": str,
        "CreateDate": datetime,
        "AssumeRolePolicyDocument": str,
        "InstanceProfileList": List[InstanceProfileTypeDef],
        "RolePolicyList": List[PolicyDetailTypeDef],
        "AttachedManagedPolicies": List[AttachedPolicyTypeDef],
        "PermissionsBoundary": AttachedPermissionsBoundaryTypeDef,
        "Tags": List[TagTypeDef],
        "RoleLastUsed": RoleLastUsedTypeDef,
    },
    total=False,
)

UserDetailTypeDef = TypedDict(
    "UserDetailTypeDef",
    {
        "Path": str,
        "UserName": str,
        "UserId": str,
        "Arn": str,
        "CreateDate": datetime,
        "UserPolicyList": List[PolicyDetailTypeDef],
        "GroupList": List[str],
        "AttachedManagedPolicies": List[AttachedPolicyTypeDef],
        "PermissionsBoundary": AttachedPermissionsBoundaryTypeDef,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

GetAccountAuthorizationDetailsResponseTypeDef = TypedDict(
    "GetAccountAuthorizationDetailsResponseTypeDef",
    {
        "UserDetailList": List[UserDetailTypeDef],
        "GroupDetailList": List[GroupDetailTypeDef],
        "RoleDetailList": List[RoleDetailTypeDef],
        "Policies": List[ManagedPolicyDetailTypeDef],
        "IsTruncated": bool,
        "Marker": str,
    },
    total=False,
)

PasswordPolicyTypeDef = TypedDict(
    "PasswordPolicyTypeDef",
    {
        "MinimumPasswordLength": int,
        "RequireSymbols": bool,
        "RequireNumbers": bool,
        "RequireUppercaseCharacters": bool,
        "RequireLowercaseCharacters": bool,
        "AllowUsersToChangePassword": bool,
        "ExpirePasswords": bool,
        "MaxPasswordAge": int,
        "PasswordReusePrevention": int,
        "HardExpiry": bool,
    },
    total=False,
)

GetAccountPasswordPolicyResponseTypeDef = TypedDict(
    "GetAccountPasswordPolicyResponseTypeDef", {"PasswordPolicy": PasswordPolicyTypeDef}
)

GetAccountSummaryResponseTypeDef = TypedDict(
    "GetAccountSummaryResponseTypeDef",
    {
        "SummaryMap": Dict[
            Literal[
                "Users",
                "UsersQuota",
                "Groups",
                "GroupsQuota",
                "ServerCertificates",
                "ServerCertificatesQuota",
                "UserPolicySizeQuota",
                "GroupPolicySizeQuota",
                "GroupsPerUserQuota",
                "SigningCertificatesPerUserQuota",
                "AccessKeysPerUserQuota",
                "MFADevices",
                "MFADevicesInUse",
                "AccountMFAEnabled",
                "AccountAccessKeysPresent",
                "AccountSigningCertificatesPresent",
                "AttachedPoliciesPerGroupQuota",
                "AttachedPoliciesPerRoleQuota",
                "AttachedPoliciesPerUserQuota",
                "Policies",
                "PoliciesQuota",
                "PolicySizeQuota",
                "PolicyVersionsInUse",
                "PolicyVersionsInUseQuota",
                "VersionsPerPolicyQuota",
                "GlobalEndpointTokenVersion",
            ],
            int,
        ]
    },
    total=False,
)

GetContextKeysForPolicyResponseTypeDef = TypedDict(
    "GetContextKeysForPolicyResponseTypeDef", {"ContextKeyNames": List[str]}, total=False
)

GetCredentialReportResponseTypeDef = TypedDict(
    "GetCredentialReportResponseTypeDef",
    {"Content": Union[bytes, IO], "ReportFormat": Literal["text/csv"], "GeneratedTime": datetime},
    total=False,
)

GetGroupPolicyResponseTypeDef = TypedDict(
    "GetGroupPolicyResponseTypeDef", {"GroupName": str, "PolicyName": str, "PolicyDocument": str}
)

_RequiredGetGroupResponseTypeDef = TypedDict(
    "_RequiredGetGroupResponseTypeDef", {"Group": GroupTypeDef, "Users": List[UserTypeDef]}
)
_OptionalGetGroupResponseTypeDef = TypedDict(
    "_OptionalGetGroupResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class GetGroupResponseTypeDef(_RequiredGetGroupResponseTypeDef, _OptionalGetGroupResponseTypeDef):
    pass


GetInstanceProfileResponseTypeDef = TypedDict(
    "GetInstanceProfileResponseTypeDef", {"InstanceProfile": InstanceProfileTypeDef}
)

GetLoginProfileResponseTypeDef = TypedDict(
    "GetLoginProfileResponseTypeDef", {"LoginProfile": LoginProfileTypeDef}
)

GetOpenIDConnectProviderResponseTypeDef = TypedDict(
    "GetOpenIDConnectProviderResponseTypeDef",
    {"Url": str, "ClientIDList": List[str], "ThumbprintList": List[str], "CreateDate": datetime},
    total=False,
)

_RequiredAccessDetailTypeDef = TypedDict(
    "_RequiredAccessDetailTypeDef", {"ServiceName": str, "ServiceNamespace": str}
)
_OptionalAccessDetailTypeDef = TypedDict(
    "_OptionalAccessDetailTypeDef",
    {
        "Region": str,
        "EntityPath": str,
        "LastAuthenticatedTime": datetime,
        "TotalAuthenticatedEntities": int,
    },
    total=False,
)


class AccessDetailTypeDef(_RequiredAccessDetailTypeDef, _OptionalAccessDetailTypeDef):
    pass


ErrorDetailsTypeDef = TypedDict("ErrorDetailsTypeDef", {"Message": str, "Code": str})

_RequiredGetOrganizationsAccessReportResponseTypeDef = TypedDict(
    "_RequiredGetOrganizationsAccessReportResponseTypeDef",
    {"JobStatus": Literal["IN_PROGRESS", "COMPLETED", "FAILED"], "JobCreationDate": datetime},
)
_OptionalGetOrganizationsAccessReportResponseTypeDef = TypedDict(
    "_OptionalGetOrganizationsAccessReportResponseTypeDef",
    {
        "JobCompletionDate": datetime,
        "NumberOfServicesAccessible": int,
        "NumberOfServicesNotAccessed": int,
        "AccessDetails": List[AccessDetailTypeDef],
        "IsTruncated": bool,
        "Marker": str,
        "ErrorDetails": ErrorDetailsTypeDef,
    },
    total=False,
)


class GetOrganizationsAccessReportResponseTypeDef(
    _RequiredGetOrganizationsAccessReportResponseTypeDef,
    _OptionalGetOrganizationsAccessReportResponseTypeDef,
):
    pass


GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef", {"Policy": PolicyTypeDef}, total=False
)

GetPolicyVersionResponseTypeDef = TypedDict(
    "GetPolicyVersionResponseTypeDef", {"PolicyVersion": PolicyVersionTypeDef}, total=False
)

GetRolePolicyResponseTypeDef = TypedDict(
    "GetRolePolicyResponseTypeDef", {"RoleName": str, "PolicyName": str, "PolicyDocument": str}
)

GetRoleResponseTypeDef = TypedDict("GetRoleResponseTypeDef", {"Role": RoleTypeDef})

GetSAMLProviderResponseTypeDef = TypedDict(
    "GetSAMLProviderResponseTypeDef",
    {"SAMLMetadataDocument": str, "CreateDate": datetime, "ValidUntil": datetime},
    total=False,
)

_RequiredSSHPublicKeyTypeDef = TypedDict(
    "_RequiredSSHPublicKeyTypeDef",
    {
        "UserName": str,
        "SSHPublicKeyId": str,
        "Fingerprint": str,
        "SSHPublicKeyBody": str,
        "Status": Literal["Active", "Inactive"],
    },
)
_OptionalSSHPublicKeyTypeDef = TypedDict(
    "_OptionalSSHPublicKeyTypeDef", {"UploadDate": datetime}, total=False
)


class SSHPublicKeyTypeDef(_RequiredSSHPublicKeyTypeDef, _OptionalSSHPublicKeyTypeDef):
    pass


GetSSHPublicKeyResponseTypeDef = TypedDict(
    "GetSSHPublicKeyResponseTypeDef", {"SSHPublicKey": SSHPublicKeyTypeDef}, total=False
)

_RequiredServerCertificateMetadataTypeDef = TypedDict(
    "_RequiredServerCertificateMetadataTypeDef",
    {"Path": str, "ServerCertificateName": str, "ServerCertificateId": str, "Arn": str},
)
_OptionalServerCertificateMetadataTypeDef = TypedDict(
    "_OptionalServerCertificateMetadataTypeDef",
    {"UploadDate": datetime, "Expiration": datetime},
    total=False,
)


class ServerCertificateMetadataTypeDef(
    _RequiredServerCertificateMetadataTypeDef, _OptionalServerCertificateMetadataTypeDef
):
    pass


_RequiredServerCertificateTypeDef = TypedDict(
    "_RequiredServerCertificateTypeDef",
    {"ServerCertificateMetadata": ServerCertificateMetadataTypeDef, "CertificateBody": str},
)
_OptionalServerCertificateTypeDef = TypedDict(
    "_OptionalServerCertificateTypeDef", {"CertificateChain": str}, total=False
)


class ServerCertificateTypeDef(
    _RequiredServerCertificateTypeDef, _OptionalServerCertificateTypeDef
):
    pass


GetServerCertificateResponseTypeDef = TypedDict(
    "GetServerCertificateResponseTypeDef", {"ServerCertificate": ServerCertificateTypeDef}
)

_RequiredServiceLastAccessedTypeDef = TypedDict(
    "_RequiredServiceLastAccessedTypeDef", {"ServiceName": str, "ServiceNamespace": str}
)
_OptionalServiceLastAccessedTypeDef = TypedDict(
    "_OptionalServiceLastAccessedTypeDef",
    {
        "LastAuthenticated": datetime,
        "LastAuthenticatedEntity": str,
        "TotalAuthenticatedEntities": int,
    },
    total=False,
)


class ServiceLastAccessedTypeDef(
    _RequiredServiceLastAccessedTypeDef, _OptionalServiceLastAccessedTypeDef
):
    pass


_RequiredGetServiceLastAccessedDetailsResponseTypeDef = TypedDict(
    "_RequiredGetServiceLastAccessedDetailsResponseTypeDef",
    {
        "JobStatus": Literal["IN_PROGRESS", "COMPLETED", "FAILED"],
        "JobCreationDate": datetime,
        "ServicesLastAccessed": List[ServiceLastAccessedTypeDef],
        "JobCompletionDate": datetime,
    },
)
_OptionalGetServiceLastAccessedDetailsResponseTypeDef = TypedDict(
    "_OptionalGetServiceLastAccessedDetailsResponseTypeDef",
    {"IsTruncated": bool, "Marker": str, "Error": ErrorDetailsTypeDef},
    total=False,
)


class GetServiceLastAccessedDetailsResponseTypeDef(
    _RequiredGetServiceLastAccessedDetailsResponseTypeDef,
    _OptionalGetServiceLastAccessedDetailsResponseTypeDef,
):
    pass


_RequiredEntityInfoTypeDef = TypedDict(
    "_RequiredEntityInfoTypeDef",
    {"Arn": str, "Name": str, "Type": Literal["USER", "ROLE", "GROUP"], "Id": str},
)
_OptionalEntityInfoTypeDef = TypedDict("_OptionalEntityInfoTypeDef", {"Path": str}, total=False)


class EntityInfoTypeDef(_RequiredEntityInfoTypeDef, _OptionalEntityInfoTypeDef):
    pass


_RequiredEntityDetailsTypeDef = TypedDict(
    "_RequiredEntityDetailsTypeDef", {"EntityInfo": EntityInfoTypeDef}
)
_OptionalEntityDetailsTypeDef = TypedDict(
    "_OptionalEntityDetailsTypeDef", {"LastAuthenticated": datetime}, total=False
)


class EntityDetailsTypeDef(_RequiredEntityDetailsTypeDef, _OptionalEntityDetailsTypeDef):
    pass


_RequiredGetServiceLastAccessedDetailsWithEntitiesResponseTypeDef = TypedDict(
    "_RequiredGetServiceLastAccessedDetailsWithEntitiesResponseTypeDef",
    {
        "JobStatus": Literal["IN_PROGRESS", "COMPLETED", "FAILED"],
        "JobCreationDate": datetime,
        "JobCompletionDate": datetime,
        "EntityDetailsList": List[EntityDetailsTypeDef],
    },
)
_OptionalGetServiceLastAccessedDetailsWithEntitiesResponseTypeDef = TypedDict(
    "_OptionalGetServiceLastAccessedDetailsWithEntitiesResponseTypeDef",
    {"IsTruncated": bool, "Marker": str, "Error": ErrorDetailsTypeDef},
    total=False,
)


class GetServiceLastAccessedDetailsWithEntitiesResponseTypeDef(
    _RequiredGetServiceLastAccessedDetailsWithEntitiesResponseTypeDef,
    _OptionalGetServiceLastAccessedDetailsWithEntitiesResponseTypeDef,
):
    pass


RoleUsageTypeTypeDef = TypedDict(
    "RoleUsageTypeTypeDef", {"Region": str, "Resources": List[str]}, total=False
)

DeletionTaskFailureReasonTypeTypeDef = TypedDict(
    "DeletionTaskFailureReasonTypeTypeDef",
    {"Reason": str, "RoleUsageList": List[RoleUsageTypeTypeDef]},
    total=False,
)

_RequiredGetServiceLinkedRoleDeletionStatusResponseTypeDef = TypedDict(
    "_RequiredGetServiceLinkedRoleDeletionStatusResponseTypeDef",
    {"Status": Literal["SUCCEEDED", "IN_PROGRESS", "FAILED", "NOT_STARTED"]},
)
_OptionalGetServiceLinkedRoleDeletionStatusResponseTypeDef = TypedDict(
    "_OptionalGetServiceLinkedRoleDeletionStatusResponseTypeDef",
    {"Reason": DeletionTaskFailureReasonTypeTypeDef},
    total=False,
)


class GetServiceLinkedRoleDeletionStatusResponseTypeDef(
    _RequiredGetServiceLinkedRoleDeletionStatusResponseTypeDef,
    _OptionalGetServiceLinkedRoleDeletionStatusResponseTypeDef,
):
    pass


GetUserPolicyResponseTypeDef = TypedDict(
    "GetUserPolicyResponseTypeDef", {"UserName": str, "PolicyName": str, "PolicyDocument": str}
)

GetUserResponseTypeDef = TypedDict("GetUserResponseTypeDef", {"User": UserTypeDef})

AccessKeyMetadataTypeDef = TypedDict(
    "AccessKeyMetadataTypeDef",
    {
        "UserName": str,
        "AccessKeyId": str,
        "Status": Literal["Active", "Inactive"],
        "CreateDate": datetime,
    },
    total=False,
)

_RequiredListAccessKeysResponseTypeDef = TypedDict(
    "_RequiredListAccessKeysResponseTypeDef", {"AccessKeyMetadata": List[AccessKeyMetadataTypeDef]}
)
_OptionalListAccessKeysResponseTypeDef = TypedDict(
    "_OptionalListAccessKeysResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListAccessKeysResponseTypeDef(
    _RequiredListAccessKeysResponseTypeDef, _OptionalListAccessKeysResponseTypeDef
):
    pass


_RequiredListAccountAliasesResponseTypeDef = TypedDict(
    "_RequiredListAccountAliasesResponseTypeDef", {"AccountAliases": List[str]}
)
_OptionalListAccountAliasesResponseTypeDef = TypedDict(
    "_OptionalListAccountAliasesResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListAccountAliasesResponseTypeDef(
    _RequiredListAccountAliasesResponseTypeDef, _OptionalListAccountAliasesResponseTypeDef
):
    pass


ListAttachedGroupPoliciesResponseTypeDef = TypedDict(
    "ListAttachedGroupPoliciesResponseTypeDef",
    {"AttachedPolicies": List[AttachedPolicyTypeDef], "IsTruncated": bool, "Marker": str},
    total=False,
)

ListAttachedRolePoliciesResponseTypeDef = TypedDict(
    "ListAttachedRolePoliciesResponseTypeDef",
    {"AttachedPolicies": List[AttachedPolicyTypeDef], "IsTruncated": bool, "Marker": str},
    total=False,
)

ListAttachedUserPoliciesResponseTypeDef = TypedDict(
    "ListAttachedUserPoliciesResponseTypeDef",
    {"AttachedPolicies": List[AttachedPolicyTypeDef], "IsTruncated": bool, "Marker": str},
    total=False,
)

PolicyGroupTypeDef = TypedDict(
    "PolicyGroupTypeDef", {"GroupName": str, "GroupId": str}, total=False
)

PolicyRoleTypeDef = TypedDict("PolicyRoleTypeDef", {"RoleName": str, "RoleId": str}, total=False)

PolicyUserTypeDef = TypedDict("PolicyUserTypeDef", {"UserName": str, "UserId": str}, total=False)

ListEntitiesForPolicyResponseTypeDef = TypedDict(
    "ListEntitiesForPolicyResponseTypeDef",
    {
        "PolicyGroups": List[PolicyGroupTypeDef],
        "PolicyUsers": List[PolicyUserTypeDef],
        "PolicyRoles": List[PolicyRoleTypeDef],
        "IsTruncated": bool,
        "Marker": str,
    },
    total=False,
)

_RequiredListGroupPoliciesResponseTypeDef = TypedDict(
    "_RequiredListGroupPoliciesResponseTypeDef", {"PolicyNames": List[str]}
)
_OptionalListGroupPoliciesResponseTypeDef = TypedDict(
    "_OptionalListGroupPoliciesResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListGroupPoliciesResponseTypeDef(
    _RequiredListGroupPoliciesResponseTypeDef, _OptionalListGroupPoliciesResponseTypeDef
):
    pass


_RequiredListGroupsForUserResponseTypeDef = TypedDict(
    "_RequiredListGroupsForUserResponseTypeDef", {"Groups": List[GroupTypeDef]}
)
_OptionalListGroupsForUserResponseTypeDef = TypedDict(
    "_OptionalListGroupsForUserResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListGroupsForUserResponseTypeDef(
    _RequiredListGroupsForUserResponseTypeDef, _OptionalListGroupsForUserResponseTypeDef
):
    pass


_RequiredListGroupsResponseTypeDef = TypedDict(
    "_RequiredListGroupsResponseTypeDef", {"Groups": List[GroupTypeDef]}
)
_OptionalListGroupsResponseTypeDef = TypedDict(
    "_OptionalListGroupsResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListGroupsResponseTypeDef(
    _RequiredListGroupsResponseTypeDef, _OptionalListGroupsResponseTypeDef
):
    pass


_RequiredListInstanceProfilesForRoleResponseTypeDef = TypedDict(
    "_RequiredListInstanceProfilesForRoleResponseTypeDef",
    {"InstanceProfiles": List[InstanceProfileTypeDef]},
)
_OptionalListInstanceProfilesForRoleResponseTypeDef = TypedDict(
    "_OptionalListInstanceProfilesForRoleResponseTypeDef",
    {"IsTruncated": bool, "Marker": str},
    total=False,
)


class ListInstanceProfilesForRoleResponseTypeDef(
    _RequiredListInstanceProfilesForRoleResponseTypeDef,
    _OptionalListInstanceProfilesForRoleResponseTypeDef,
):
    pass


_RequiredListInstanceProfilesResponseTypeDef = TypedDict(
    "_RequiredListInstanceProfilesResponseTypeDef",
    {"InstanceProfiles": List[InstanceProfileTypeDef]},
)
_OptionalListInstanceProfilesResponseTypeDef = TypedDict(
    "_OptionalListInstanceProfilesResponseTypeDef",
    {"IsTruncated": bool, "Marker": str},
    total=False,
)


class ListInstanceProfilesResponseTypeDef(
    _RequiredListInstanceProfilesResponseTypeDef, _OptionalListInstanceProfilesResponseTypeDef
):
    pass


MFADeviceTypeDef = TypedDict(
    "MFADeviceTypeDef", {"UserName": str, "SerialNumber": str, "EnableDate": datetime}
)

_RequiredListMFADevicesResponseTypeDef = TypedDict(
    "_RequiredListMFADevicesResponseTypeDef", {"MFADevices": List[MFADeviceTypeDef]}
)
_OptionalListMFADevicesResponseTypeDef = TypedDict(
    "_OptionalListMFADevicesResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListMFADevicesResponseTypeDef(
    _RequiredListMFADevicesResponseTypeDef, _OptionalListMFADevicesResponseTypeDef
):
    pass


OpenIDConnectProviderListEntryTypeDef = TypedDict(
    "OpenIDConnectProviderListEntryTypeDef", {"Arn": str}, total=False
)

ListOpenIDConnectProvidersResponseTypeDef = TypedDict(
    "ListOpenIDConnectProvidersResponseTypeDef",
    {"OpenIDConnectProviderList": List[OpenIDConnectProviderListEntryTypeDef]},
    total=False,
)

_RequiredPolicyGrantingServiceAccessTypeDef = TypedDict(
    "_RequiredPolicyGrantingServiceAccessTypeDef",
    {"PolicyName": str, "PolicyType": Literal["INLINE", "MANAGED"]},
)
_OptionalPolicyGrantingServiceAccessTypeDef = TypedDict(
    "_OptionalPolicyGrantingServiceAccessTypeDef",
    {"PolicyArn": str, "EntityType": Literal["USER", "ROLE", "GROUP"], "EntityName": str},
    total=False,
)


class PolicyGrantingServiceAccessTypeDef(
    _RequiredPolicyGrantingServiceAccessTypeDef, _OptionalPolicyGrantingServiceAccessTypeDef
):
    pass


ListPoliciesGrantingServiceAccessEntryTypeDef = TypedDict(
    "ListPoliciesGrantingServiceAccessEntryTypeDef",
    {"ServiceNamespace": str, "Policies": List[PolicyGrantingServiceAccessTypeDef]},
    total=False,
)

_RequiredListPoliciesGrantingServiceAccessResponseTypeDef = TypedDict(
    "_RequiredListPoliciesGrantingServiceAccessResponseTypeDef",
    {"PoliciesGrantingServiceAccess": List[ListPoliciesGrantingServiceAccessEntryTypeDef]},
)
_OptionalListPoliciesGrantingServiceAccessResponseTypeDef = TypedDict(
    "_OptionalListPoliciesGrantingServiceAccessResponseTypeDef",
    {"IsTruncated": bool, "Marker": str},
    total=False,
)


class ListPoliciesGrantingServiceAccessResponseTypeDef(
    _RequiredListPoliciesGrantingServiceAccessResponseTypeDef,
    _OptionalListPoliciesGrantingServiceAccessResponseTypeDef,
):
    pass


ListPoliciesResponseTypeDef = TypedDict(
    "ListPoliciesResponseTypeDef",
    {"Policies": List[PolicyTypeDef], "IsTruncated": bool, "Marker": str},
    total=False,
)

ListPolicyVersionsResponseTypeDef = TypedDict(
    "ListPolicyVersionsResponseTypeDef",
    {"Versions": List[PolicyVersionTypeDef], "IsTruncated": bool, "Marker": str},
    total=False,
)

_RequiredListRolePoliciesResponseTypeDef = TypedDict(
    "_RequiredListRolePoliciesResponseTypeDef", {"PolicyNames": List[str]}
)
_OptionalListRolePoliciesResponseTypeDef = TypedDict(
    "_OptionalListRolePoliciesResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListRolePoliciesResponseTypeDef(
    _RequiredListRolePoliciesResponseTypeDef, _OptionalListRolePoliciesResponseTypeDef
):
    pass


_RequiredListRoleTagsResponseTypeDef = TypedDict(
    "_RequiredListRoleTagsResponseTypeDef", {"Tags": List[TagTypeDef]}
)
_OptionalListRoleTagsResponseTypeDef = TypedDict(
    "_OptionalListRoleTagsResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListRoleTagsResponseTypeDef(
    _RequiredListRoleTagsResponseTypeDef, _OptionalListRoleTagsResponseTypeDef
):
    pass


_RequiredListRolesResponseTypeDef = TypedDict(
    "_RequiredListRolesResponseTypeDef", {"Roles": List[RoleTypeDef]}
)
_OptionalListRolesResponseTypeDef = TypedDict(
    "_OptionalListRolesResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListRolesResponseTypeDef(
    _RequiredListRolesResponseTypeDef, _OptionalListRolesResponseTypeDef
):
    pass


SAMLProviderListEntryTypeDef = TypedDict(
    "SAMLProviderListEntryTypeDef",
    {"Arn": str, "ValidUntil": datetime, "CreateDate": datetime},
    total=False,
)

ListSAMLProvidersResponseTypeDef = TypedDict(
    "ListSAMLProvidersResponseTypeDef",
    {"SAMLProviderList": List[SAMLProviderListEntryTypeDef]},
    total=False,
)

SSHPublicKeyMetadataTypeDef = TypedDict(
    "SSHPublicKeyMetadataTypeDef",
    {
        "UserName": str,
        "SSHPublicKeyId": str,
        "Status": Literal["Active", "Inactive"],
        "UploadDate": datetime,
    },
)

ListSSHPublicKeysResponseTypeDef = TypedDict(
    "ListSSHPublicKeysResponseTypeDef",
    {"SSHPublicKeys": List[SSHPublicKeyMetadataTypeDef], "IsTruncated": bool, "Marker": str},
    total=False,
)

_RequiredListServerCertificatesResponseTypeDef = TypedDict(
    "_RequiredListServerCertificatesResponseTypeDef",
    {"ServerCertificateMetadataList": List[ServerCertificateMetadataTypeDef]},
)
_OptionalListServerCertificatesResponseTypeDef = TypedDict(
    "_OptionalListServerCertificatesResponseTypeDef",
    {"IsTruncated": bool, "Marker": str},
    total=False,
)


class ListServerCertificatesResponseTypeDef(
    _RequiredListServerCertificatesResponseTypeDef, _OptionalListServerCertificatesResponseTypeDef
):
    pass


ServiceSpecificCredentialMetadataTypeDef = TypedDict(
    "ServiceSpecificCredentialMetadataTypeDef",
    {
        "UserName": str,
        "Status": Literal["Active", "Inactive"],
        "ServiceUserName": str,
        "CreateDate": datetime,
        "ServiceSpecificCredentialId": str,
        "ServiceName": str,
    },
)

ListServiceSpecificCredentialsResponseTypeDef = TypedDict(
    "ListServiceSpecificCredentialsResponseTypeDef",
    {"ServiceSpecificCredentials": List[ServiceSpecificCredentialMetadataTypeDef]},
    total=False,
)

_RequiredSigningCertificateTypeDef = TypedDict(
    "_RequiredSigningCertificateTypeDef",
    {
        "UserName": str,
        "CertificateId": str,
        "CertificateBody": str,
        "Status": Literal["Active", "Inactive"],
    },
)
_OptionalSigningCertificateTypeDef = TypedDict(
    "_OptionalSigningCertificateTypeDef", {"UploadDate": datetime}, total=False
)


class SigningCertificateTypeDef(
    _RequiredSigningCertificateTypeDef, _OptionalSigningCertificateTypeDef
):
    pass


_RequiredListSigningCertificatesResponseTypeDef = TypedDict(
    "_RequiredListSigningCertificatesResponseTypeDef",
    {"Certificates": List[SigningCertificateTypeDef]},
)
_OptionalListSigningCertificatesResponseTypeDef = TypedDict(
    "_OptionalListSigningCertificatesResponseTypeDef",
    {"IsTruncated": bool, "Marker": str},
    total=False,
)


class ListSigningCertificatesResponseTypeDef(
    _RequiredListSigningCertificatesResponseTypeDef, _OptionalListSigningCertificatesResponseTypeDef
):
    pass


_RequiredListUserPoliciesResponseTypeDef = TypedDict(
    "_RequiredListUserPoliciesResponseTypeDef", {"PolicyNames": List[str]}
)
_OptionalListUserPoliciesResponseTypeDef = TypedDict(
    "_OptionalListUserPoliciesResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListUserPoliciesResponseTypeDef(
    _RequiredListUserPoliciesResponseTypeDef, _OptionalListUserPoliciesResponseTypeDef
):
    pass


_RequiredListUserTagsResponseTypeDef = TypedDict(
    "_RequiredListUserTagsResponseTypeDef", {"Tags": List[TagTypeDef]}
)
_OptionalListUserTagsResponseTypeDef = TypedDict(
    "_OptionalListUserTagsResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListUserTagsResponseTypeDef(
    _RequiredListUserTagsResponseTypeDef, _OptionalListUserTagsResponseTypeDef
):
    pass


_RequiredListUsersResponseTypeDef = TypedDict(
    "_RequiredListUsersResponseTypeDef", {"Users": List[UserTypeDef]}
)
_OptionalListUsersResponseTypeDef = TypedDict(
    "_OptionalListUsersResponseTypeDef", {"IsTruncated": bool, "Marker": str}, total=False
)


class ListUsersResponseTypeDef(
    _RequiredListUsersResponseTypeDef, _OptionalListUsersResponseTypeDef
):
    pass


_RequiredListVirtualMFADevicesResponseTypeDef = TypedDict(
    "_RequiredListVirtualMFADevicesResponseTypeDef",
    {"VirtualMFADevices": List[VirtualMFADeviceTypeDef]},
)
_OptionalListVirtualMFADevicesResponseTypeDef = TypedDict(
    "_OptionalListVirtualMFADevicesResponseTypeDef",
    {"IsTruncated": bool, "Marker": str},
    total=False,
)


class ListVirtualMFADevicesResponseTypeDef(
    _RequiredListVirtualMFADevicesResponseTypeDef, _OptionalListVirtualMFADevicesResponseTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

ResetServiceSpecificCredentialResponseTypeDef = TypedDict(
    "ResetServiceSpecificCredentialResponseTypeDef",
    {"ServiceSpecificCredential": ServiceSpecificCredentialTypeDef},
    total=False,
)

OrganizationsDecisionDetailTypeDef = TypedDict(
    "OrganizationsDecisionDetailTypeDef", {"AllowedByOrganizations": bool}, total=False
)

PermissionsBoundaryDecisionDetailTypeDef = TypedDict(
    "PermissionsBoundaryDecisionDetailTypeDef", {"AllowedByPermissionsBoundary": bool}, total=False
)

PositionTypeDef = TypedDict("PositionTypeDef", {"Line": int, "Column": int}, total=False)

StatementTypeDef = TypedDict(
    "StatementTypeDef",
    {
        "SourcePolicyId": str,
        "SourcePolicyType": Literal[
            "user", "group", "role", "aws-managed", "user-managed", "resource", "none"
        ],
        "StartPosition": PositionTypeDef,
        "EndPosition": PositionTypeDef,
    },
    total=False,
)

_RequiredResourceSpecificResultTypeDef = TypedDict(
    "_RequiredResourceSpecificResultTypeDef",
    {
        "EvalResourceName": str,
        "EvalResourceDecision": Literal["allowed", "explicitDeny", "implicitDeny"],
    },
)
_OptionalResourceSpecificResultTypeDef = TypedDict(
    "_OptionalResourceSpecificResultTypeDef",
    {
        "MatchedStatements": List[StatementTypeDef],
        "MissingContextValues": List[str],
        "EvalDecisionDetails": Dict[str, Literal["allowed", "explicitDeny", "implicitDeny"]],
        "PermissionsBoundaryDecisionDetail": PermissionsBoundaryDecisionDetailTypeDef,
    },
    total=False,
)


class ResourceSpecificResultTypeDef(
    _RequiredResourceSpecificResultTypeDef, _OptionalResourceSpecificResultTypeDef
):
    pass


_RequiredEvaluationResultTypeDef = TypedDict(
    "_RequiredEvaluationResultTypeDef",
    {"EvalActionName": str, "EvalDecision": Literal["allowed", "explicitDeny", "implicitDeny"]},
)
_OptionalEvaluationResultTypeDef = TypedDict(
    "_OptionalEvaluationResultTypeDef",
    {
        "EvalResourceName": str,
        "MatchedStatements": List[StatementTypeDef],
        "MissingContextValues": List[str],
        "OrganizationsDecisionDetail": OrganizationsDecisionDetailTypeDef,
        "PermissionsBoundaryDecisionDetail": PermissionsBoundaryDecisionDetailTypeDef,
        "EvalDecisionDetails": Dict[str, Literal["allowed", "explicitDeny", "implicitDeny"]],
        "ResourceSpecificResults": List[ResourceSpecificResultTypeDef],
    },
    total=False,
)


class EvaluationResultTypeDef(_RequiredEvaluationResultTypeDef, _OptionalEvaluationResultTypeDef):
    pass


SimulatePolicyResponseTypeDef = TypedDict(
    "SimulatePolicyResponseTypeDef",
    {"EvaluationResults": List[EvaluationResultTypeDef], "IsTruncated": bool, "Marker": str},
    total=False,
)

UpdateRoleDescriptionResponseTypeDef = TypedDict(
    "UpdateRoleDescriptionResponseTypeDef", {"Role": RoleTypeDef}, total=False
)

UpdateSAMLProviderResponseTypeDef = TypedDict(
    "UpdateSAMLProviderResponseTypeDef", {"SAMLProviderArn": str}, total=False
)

UploadSSHPublicKeyResponseTypeDef = TypedDict(
    "UploadSSHPublicKeyResponseTypeDef", {"SSHPublicKey": SSHPublicKeyTypeDef}, total=False
)

UploadServerCertificateResponseTypeDef = TypedDict(
    "UploadServerCertificateResponseTypeDef",
    {"ServerCertificateMetadata": ServerCertificateMetadataTypeDef},
    total=False,
)

UploadSigningCertificateResponseTypeDef = TypedDict(
    "UploadSigningCertificateResponseTypeDef", {"Certificate": SigningCertificateTypeDef}
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
