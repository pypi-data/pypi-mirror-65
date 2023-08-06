"""
Main interface for efs service type definitions.

Usage::

    from mypy_boto3.efs.type_defs import PosixUserTypeDef

    data: PosixUserTypeDef = {...}
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
    "PosixUserTypeDef",
    "CreationInfoTypeDef",
    "RootDirectoryTypeDef",
    "TagTypeDef",
    "AccessPointDescriptionTypeDef",
    "DescribeAccessPointsResponseTypeDef",
    "FileSystemSizeTypeDef",
    "FileSystemDescriptionTypeDef",
    "DescribeFileSystemsResponseTypeDef",
    "DescribeMountTargetSecurityGroupsResponseTypeDef",
    "MountTargetDescriptionTypeDef",
    "DescribeMountTargetsResponseTypeDef",
    "DescribeTagsResponseTypeDef",
    "FileSystemPolicyDescriptionTypeDef",
    "LifecyclePolicyTypeDef",
    "LifecycleConfigurationDescriptionTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
)

_RequiredPosixUserTypeDef = TypedDict("_RequiredPosixUserTypeDef", {"Uid": int, "Gid": int})
_OptionalPosixUserTypeDef = TypedDict(
    "_OptionalPosixUserTypeDef", {"SecondaryGids": List[int]}, total=False
)


class PosixUserTypeDef(_RequiredPosixUserTypeDef, _OptionalPosixUserTypeDef):
    pass


CreationInfoTypeDef = TypedDict(
    "CreationInfoTypeDef", {"OwnerUid": int, "OwnerGid": int, "Permissions": str}
)

RootDirectoryTypeDef = TypedDict(
    "RootDirectoryTypeDef", {"Path": str, "CreationInfo": CreationInfoTypeDef}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

AccessPointDescriptionTypeDef = TypedDict(
    "AccessPointDescriptionTypeDef",
    {
        "ClientToken": str,
        "Name": str,
        "Tags": List[TagTypeDef],
        "AccessPointId": str,
        "AccessPointArn": str,
        "FileSystemId": str,
        "PosixUser": PosixUserTypeDef,
        "RootDirectory": RootDirectoryTypeDef,
        "OwnerId": str,
        "LifeCycleState": Literal["creating", "available", "updating", "deleting", "deleted"],
    },
    total=False,
)

DescribeAccessPointsResponseTypeDef = TypedDict(
    "DescribeAccessPointsResponseTypeDef",
    {"AccessPoints": List[AccessPointDescriptionTypeDef], "NextToken": str},
    total=False,
)

_RequiredFileSystemSizeTypeDef = TypedDict("_RequiredFileSystemSizeTypeDef", {"Value": int})
_OptionalFileSystemSizeTypeDef = TypedDict(
    "_OptionalFileSystemSizeTypeDef",
    {"Timestamp": datetime, "ValueInIA": int, "ValueInStandard": int},
    total=False,
)


class FileSystemSizeTypeDef(_RequiredFileSystemSizeTypeDef, _OptionalFileSystemSizeTypeDef):
    pass


_RequiredFileSystemDescriptionTypeDef = TypedDict(
    "_RequiredFileSystemDescriptionTypeDef",
    {
        "OwnerId": str,
        "CreationToken": str,
        "FileSystemId": str,
        "CreationTime": datetime,
        "LifeCycleState": Literal["creating", "available", "updating", "deleting", "deleted"],
        "NumberOfMountTargets": int,
        "SizeInBytes": FileSystemSizeTypeDef,
        "PerformanceMode": Literal["generalPurpose", "maxIO"],
        "Tags": List[TagTypeDef],
    },
)
_OptionalFileSystemDescriptionTypeDef = TypedDict(
    "_OptionalFileSystemDescriptionTypeDef",
    {
        "Name": str,
        "Encrypted": bool,
        "KmsKeyId": str,
        "ThroughputMode": Literal["bursting", "provisioned"],
        "ProvisionedThroughputInMibps": float,
    },
    total=False,
)


class FileSystemDescriptionTypeDef(
    _RequiredFileSystemDescriptionTypeDef, _OptionalFileSystemDescriptionTypeDef
):
    pass


DescribeFileSystemsResponseTypeDef = TypedDict(
    "DescribeFileSystemsResponseTypeDef",
    {"Marker": str, "FileSystems": List[FileSystemDescriptionTypeDef], "NextMarker": str},
    total=False,
)

DescribeMountTargetSecurityGroupsResponseTypeDef = TypedDict(
    "DescribeMountTargetSecurityGroupsResponseTypeDef", {"SecurityGroups": List[str]}
)

_RequiredMountTargetDescriptionTypeDef = TypedDict(
    "_RequiredMountTargetDescriptionTypeDef",
    {
        "MountTargetId": str,
        "FileSystemId": str,
        "SubnetId": str,
        "LifeCycleState": Literal["creating", "available", "updating", "deleting", "deleted"],
    },
)
_OptionalMountTargetDescriptionTypeDef = TypedDict(
    "_OptionalMountTargetDescriptionTypeDef",
    {
        "OwnerId": str,
        "IpAddress": str,
        "NetworkInterfaceId": str,
        "AvailabilityZoneId": str,
        "AvailabilityZoneName": str,
    },
    total=False,
)


class MountTargetDescriptionTypeDef(
    _RequiredMountTargetDescriptionTypeDef, _OptionalMountTargetDescriptionTypeDef
):
    pass


DescribeMountTargetsResponseTypeDef = TypedDict(
    "DescribeMountTargetsResponseTypeDef",
    {"Marker": str, "MountTargets": List[MountTargetDescriptionTypeDef], "NextMarker": str},
    total=False,
)

_RequiredDescribeTagsResponseTypeDef = TypedDict(
    "_RequiredDescribeTagsResponseTypeDef", {"Tags": List[TagTypeDef]}
)
_OptionalDescribeTagsResponseTypeDef = TypedDict(
    "_OptionalDescribeTagsResponseTypeDef", {"Marker": str, "NextMarker": str}, total=False
)


class DescribeTagsResponseTypeDef(
    _RequiredDescribeTagsResponseTypeDef, _OptionalDescribeTagsResponseTypeDef
):
    pass


FileSystemPolicyDescriptionTypeDef = TypedDict(
    "FileSystemPolicyDescriptionTypeDef", {"FileSystemId": str, "Policy": str}, total=False
)

LifecyclePolicyTypeDef = TypedDict(
    "LifecyclePolicyTypeDef",
    {
        "TransitionToIA": Literal[
            "AFTER_7_DAYS", "AFTER_14_DAYS", "AFTER_30_DAYS", "AFTER_60_DAYS", "AFTER_90_DAYS"
        ]
    },
    total=False,
)

LifecycleConfigurationDescriptionTypeDef = TypedDict(
    "LifecycleConfigurationDescriptionTypeDef",
    {"LifecyclePolicies": List[LifecyclePolicyTypeDef]},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef], "NextToken": str}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
