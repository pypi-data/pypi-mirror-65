"""
Main interface for transfer service type definitions.

Usage::

    from mypy_boto3.transfer.type_defs import CreateServerResponseTypeDef

    data: CreateServerResponseTypeDef = {...}
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
    "CreateServerResponseTypeDef",
    "CreateUserResponseTypeDef",
    "EndpointDetailsTypeDef",
    "IdentityProviderDetailsTypeDef",
    "TagTypeDef",
    "DescribedServerTypeDef",
    "DescribeServerResponseTypeDef",
    "HomeDirectoryMapEntryTypeDef",
    "SshPublicKeyTypeDef",
    "DescribedUserTypeDef",
    "DescribeUserResponseTypeDef",
    "ImportSshPublicKeyResponseTypeDef",
    "ListedServerTypeDef",
    "ListServersResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListedUserTypeDef",
    "ListUsersResponseTypeDef",
    "PaginatorConfigTypeDef",
    "TestIdentityProviderResponseTypeDef",
    "UpdateServerResponseTypeDef",
    "UpdateUserResponseTypeDef",
)

CreateServerResponseTypeDef = TypedDict("CreateServerResponseTypeDef", {"ServerId": str})

CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef", {"ServerId": str, "UserName": str}
)

EndpointDetailsTypeDef = TypedDict(
    "EndpointDetailsTypeDef",
    {"AddressAllocationIds": List[str], "SubnetIds": List[str], "VpcEndpointId": str, "VpcId": str},
    total=False,
)

IdentityProviderDetailsTypeDef = TypedDict(
    "IdentityProviderDetailsTypeDef", {"Url": str, "InvocationRole": str}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

_RequiredDescribedServerTypeDef = TypedDict("_RequiredDescribedServerTypeDef", {"Arn": str})
_OptionalDescribedServerTypeDef = TypedDict(
    "_OptionalDescribedServerTypeDef",
    {
        "EndpointDetails": EndpointDetailsTypeDef,
        "EndpointType": Literal["PUBLIC", "VPC", "VPC_ENDPOINT"],
        "HostKeyFingerprint": str,
        "IdentityProviderDetails": IdentityProviderDetailsTypeDef,
        "IdentityProviderType": Literal["SERVICE_MANAGED", "API_GATEWAY"],
        "LoggingRole": str,
        "ServerId": str,
        "State": Literal[
            "OFFLINE", "ONLINE", "STARTING", "STOPPING", "START_FAILED", "STOP_FAILED"
        ],
        "Tags": List[TagTypeDef],
        "UserCount": int,
    },
    total=False,
)


class DescribedServerTypeDef(_RequiredDescribedServerTypeDef, _OptionalDescribedServerTypeDef):
    pass


DescribeServerResponseTypeDef = TypedDict(
    "DescribeServerResponseTypeDef", {"Server": DescribedServerTypeDef}
)

HomeDirectoryMapEntryTypeDef = TypedDict(
    "HomeDirectoryMapEntryTypeDef", {"Entry": str, "Target": str}
)

SshPublicKeyTypeDef = TypedDict(
    "SshPublicKeyTypeDef",
    {"DateImported": datetime, "SshPublicKeyBody": str, "SshPublicKeyId": str},
)

_RequiredDescribedUserTypeDef = TypedDict("_RequiredDescribedUserTypeDef", {"Arn": str})
_OptionalDescribedUserTypeDef = TypedDict(
    "_OptionalDescribedUserTypeDef",
    {
        "HomeDirectory": str,
        "HomeDirectoryMappings": List[HomeDirectoryMapEntryTypeDef],
        "HomeDirectoryType": Literal["PATH", "LOGICAL"],
        "Policy": str,
        "Role": str,
        "SshPublicKeys": List[SshPublicKeyTypeDef],
        "Tags": List[TagTypeDef],
        "UserName": str,
    },
    total=False,
)


class DescribedUserTypeDef(_RequiredDescribedUserTypeDef, _OptionalDescribedUserTypeDef):
    pass


DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef", {"ServerId": str, "User": DescribedUserTypeDef}
)

ImportSshPublicKeyResponseTypeDef = TypedDict(
    "ImportSshPublicKeyResponseTypeDef", {"ServerId": str, "SshPublicKeyId": str, "UserName": str}
)

_RequiredListedServerTypeDef = TypedDict("_RequiredListedServerTypeDef", {"Arn": str})
_OptionalListedServerTypeDef = TypedDict(
    "_OptionalListedServerTypeDef",
    {
        "IdentityProviderType": Literal["SERVICE_MANAGED", "API_GATEWAY"],
        "EndpointType": Literal["PUBLIC", "VPC", "VPC_ENDPOINT"],
        "LoggingRole": str,
        "ServerId": str,
        "State": Literal[
            "OFFLINE", "ONLINE", "STARTING", "STOPPING", "START_FAILED", "STOP_FAILED"
        ],
        "UserCount": int,
    },
    total=False,
)


class ListedServerTypeDef(_RequiredListedServerTypeDef, _OptionalListedServerTypeDef):
    pass


_RequiredListServersResponseTypeDef = TypedDict(
    "_RequiredListServersResponseTypeDef", {"Servers": List[ListedServerTypeDef]}
)
_OptionalListServersResponseTypeDef = TypedDict(
    "_OptionalListServersResponseTypeDef", {"NextToken": str}, total=False
)


class ListServersResponseTypeDef(
    _RequiredListServersResponseTypeDef, _OptionalListServersResponseTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {"Arn": str, "NextToken": str, "Tags": List[TagTypeDef]},
    total=False,
)

_RequiredListedUserTypeDef = TypedDict("_RequiredListedUserTypeDef", {"Arn": str})
_OptionalListedUserTypeDef = TypedDict(
    "_OptionalListedUserTypeDef",
    {
        "HomeDirectory": str,
        "HomeDirectoryType": Literal["PATH", "LOGICAL"],
        "Role": str,
        "SshPublicKeyCount": int,
        "UserName": str,
    },
    total=False,
)


class ListedUserTypeDef(_RequiredListedUserTypeDef, _OptionalListedUserTypeDef):
    pass


_RequiredListUsersResponseTypeDef = TypedDict(
    "_RequiredListUsersResponseTypeDef", {"ServerId": str, "Users": List[ListedUserTypeDef]}
)
_OptionalListUsersResponseTypeDef = TypedDict(
    "_OptionalListUsersResponseTypeDef", {"NextToken": str}, total=False
)


class ListUsersResponseTypeDef(
    _RequiredListUsersResponseTypeDef, _OptionalListUsersResponseTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

_RequiredTestIdentityProviderResponseTypeDef = TypedDict(
    "_RequiredTestIdentityProviderResponseTypeDef", {"StatusCode": int, "Url": str}
)
_OptionalTestIdentityProviderResponseTypeDef = TypedDict(
    "_OptionalTestIdentityProviderResponseTypeDef", {"Response": str, "Message": str}, total=False
)


class TestIdentityProviderResponseTypeDef(
    _RequiredTestIdentityProviderResponseTypeDef, _OptionalTestIdentityProviderResponseTypeDef
):
    pass


UpdateServerResponseTypeDef = TypedDict("UpdateServerResponseTypeDef", {"ServerId": str})

UpdateUserResponseTypeDef = TypedDict(
    "UpdateUserResponseTypeDef", {"ServerId": str, "UserName": str}
)
