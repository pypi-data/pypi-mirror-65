"""
Main interface for cognito-identity service type definitions.

Usage::

    from mypy_boto3.cognito_identity.type_defs import CognitoIdentityProviderTypeDef

    data: CognitoIdentityProviderTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CognitoIdentityProviderTypeDef",
    "UnprocessedIdentityIdTypeDef",
    "DeleteIdentitiesResponseTypeDef",
    "CredentialsTypeDef",
    "GetCredentialsForIdentityResponseTypeDef",
    "GetIdResponseTypeDef",
    "MappingRuleTypeDef",
    "RulesConfigurationTypeTypeDef",
    "RoleMappingTypeDef",
    "GetIdentityPoolRolesResponseTypeDef",
    "GetOpenIdTokenForDeveloperIdentityResponseTypeDef",
    "GetOpenIdTokenResponseTypeDef",
    "IdentityDescriptionTypeDef",
    "IdentityPoolTypeDef",
    "ListIdentitiesResponseTypeDef",
    "IdentityPoolShortDescriptionTypeDef",
    "ListIdentityPoolsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LookupDeveloperIdentityResponseTypeDef",
    "MergeDeveloperIdentitiesResponseTypeDef",
    "PaginatorConfigTypeDef",
)

CognitoIdentityProviderTypeDef = TypedDict(
    "CognitoIdentityProviderTypeDef",
    {"ProviderName": str, "ClientId": str, "ServerSideTokenCheck": bool},
    total=False,
)

UnprocessedIdentityIdTypeDef = TypedDict(
    "UnprocessedIdentityIdTypeDef",
    {"IdentityId": str, "ErrorCode": Literal["AccessDenied", "InternalServerError"]},
    total=False,
)

DeleteIdentitiesResponseTypeDef = TypedDict(
    "DeleteIdentitiesResponseTypeDef",
    {"UnprocessedIdentityIds": List[UnprocessedIdentityIdTypeDef]},
    total=False,
)

CredentialsTypeDef = TypedDict(
    "CredentialsTypeDef",
    {"AccessKeyId": str, "SecretKey": str, "SessionToken": str, "Expiration": datetime},
    total=False,
)

GetCredentialsForIdentityResponseTypeDef = TypedDict(
    "GetCredentialsForIdentityResponseTypeDef",
    {"IdentityId": str, "Credentials": CredentialsTypeDef},
    total=False,
)

GetIdResponseTypeDef = TypedDict("GetIdResponseTypeDef", {"IdentityId": str}, total=False)

MappingRuleTypeDef = TypedDict(
    "MappingRuleTypeDef",
    {
        "Claim": str,
        "MatchType": Literal["Equals", "Contains", "StartsWith", "NotEqual"],
        "Value": str,
        "RoleARN": str,
    },
)

RulesConfigurationTypeTypeDef = TypedDict(
    "RulesConfigurationTypeTypeDef", {"Rules": List[MappingRuleTypeDef]}
)

_RequiredRoleMappingTypeDef = TypedDict(
    "_RequiredRoleMappingTypeDef", {"Type": Literal["Token", "Rules"]}
)
_OptionalRoleMappingTypeDef = TypedDict(
    "_OptionalRoleMappingTypeDef",
    {
        "AmbiguousRoleResolution": Literal["AuthenticatedRole", "Deny"],
        "RulesConfiguration": RulesConfigurationTypeTypeDef,
    },
    total=False,
)


class RoleMappingTypeDef(_RequiredRoleMappingTypeDef, _OptionalRoleMappingTypeDef):
    pass


GetIdentityPoolRolesResponseTypeDef = TypedDict(
    "GetIdentityPoolRolesResponseTypeDef",
    {"IdentityPoolId": str, "Roles": Dict[str, str], "RoleMappings": Dict[str, RoleMappingTypeDef]},
    total=False,
)

GetOpenIdTokenForDeveloperIdentityResponseTypeDef = TypedDict(
    "GetOpenIdTokenForDeveloperIdentityResponseTypeDef",
    {"IdentityId": str, "Token": str},
    total=False,
)

GetOpenIdTokenResponseTypeDef = TypedDict(
    "GetOpenIdTokenResponseTypeDef", {"IdentityId": str, "Token": str}, total=False
)

IdentityDescriptionTypeDef = TypedDict(
    "IdentityDescriptionTypeDef",
    {
        "IdentityId": str,
        "Logins": List[str],
        "CreationDate": datetime,
        "LastModifiedDate": datetime,
    },
    total=False,
)

_RequiredIdentityPoolTypeDef = TypedDict(
    "_RequiredIdentityPoolTypeDef",
    {"IdentityPoolId": str, "IdentityPoolName": str, "AllowUnauthenticatedIdentities": bool},
)
_OptionalIdentityPoolTypeDef = TypedDict(
    "_OptionalIdentityPoolTypeDef",
    {
        "AllowClassicFlow": bool,
        "SupportedLoginProviders": Dict[str, str],
        "DeveloperProviderName": str,
        "OpenIdConnectProviderARNs": List[str],
        "CognitoIdentityProviders": List[CognitoIdentityProviderTypeDef],
        "SamlProviderARNs": List[str],
        "IdentityPoolTags": Dict[str, str],
    },
    total=False,
)


class IdentityPoolTypeDef(_RequiredIdentityPoolTypeDef, _OptionalIdentityPoolTypeDef):
    pass


ListIdentitiesResponseTypeDef = TypedDict(
    "ListIdentitiesResponseTypeDef",
    {"IdentityPoolId": str, "Identities": List[IdentityDescriptionTypeDef], "NextToken": str},
    total=False,
)

IdentityPoolShortDescriptionTypeDef = TypedDict(
    "IdentityPoolShortDescriptionTypeDef",
    {"IdentityPoolId": str, "IdentityPoolName": str},
    total=False,
)

ListIdentityPoolsResponseTypeDef = TypedDict(
    "ListIdentityPoolsResponseTypeDef",
    {"IdentityPools": List[IdentityPoolShortDescriptionTypeDef], "NextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

LookupDeveloperIdentityResponseTypeDef = TypedDict(
    "LookupDeveloperIdentityResponseTypeDef",
    {"IdentityId": str, "DeveloperUserIdentifierList": List[str], "NextToken": str},
    total=False,
)

MergeDeveloperIdentitiesResponseTypeDef = TypedDict(
    "MergeDeveloperIdentitiesResponseTypeDef", {"IdentityId": str}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
