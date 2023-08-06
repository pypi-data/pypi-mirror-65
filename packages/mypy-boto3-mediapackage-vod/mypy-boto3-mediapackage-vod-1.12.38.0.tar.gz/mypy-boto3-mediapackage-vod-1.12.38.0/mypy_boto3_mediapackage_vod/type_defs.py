"""
Main interface for mediapackage-vod service type definitions.

Usage::

    from mypy_boto3.mediapackage_vod.type_defs import SpekeKeyProviderTypeDef

    data: SpekeKeyProviderTypeDef = {...}
"""
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
    "SpekeKeyProviderTypeDef",
    "CmafEncryptionTypeDef",
    "StreamSelectionTypeDef",
    "HlsManifestTypeDef",
    "CmafPackageTypeDef",
    "EgressEndpointTypeDef",
    "CreateAssetResponseTypeDef",
    "DashEncryptionTypeDef",
    "DashManifestTypeDef",
    "DashPackageTypeDef",
    "HlsEncryptionTypeDef",
    "HlsPackageTypeDef",
    "MssEncryptionTypeDef",
    "MssManifestTypeDef",
    "MssPackageTypeDef",
    "CreatePackagingConfigurationResponseTypeDef",
    "CreatePackagingGroupResponseTypeDef",
    "DescribeAssetResponseTypeDef",
    "DescribePackagingConfigurationResponseTypeDef",
    "DescribePackagingGroupResponseTypeDef",
    "AssetShallowTypeDef",
    "ListAssetsResponseTypeDef",
    "PackagingConfigurationTypeDef",
    "ListPackagingConfigurationsResponseTypeDef",
    "PackagingGroupTypeDef",
    "ListPackagingGroupsResponseTypeDef",
    "PaginatorConfigTypeDef",
)

SpekeKeyProviderTypeDef = TypedDict(
    "SpekeKeyProviderTypeDef", {"RoleArn": str, "SystemIds": List[str], "Url": str}
)

CmafEncryptionTypeDef = TypedDict(
    "CmafEncryptionTypeDef", {"SpekeKeyProvider": SpekeKeyProviderTypeDef}
)

StreamSelectionTypeDef = TypedDict(
    "StreamSelectionTypeDef",
    {
        "MaxVideoBitsPerSecond": int,
        "MinVideoBitsPerSecond": int,
        "StreamOrder": Literal["ORIGINAL", "VIDEO_BITRATE_ASCENDING", "VIDEO_BITRATE_DESCENDING"],
    },
    total=False,
)

HlsManifestTypeDef = TypedDict(
    "HlsManifestTypeDef",
    {
        "AdMarkers": Literal["NONE", "SCTE35_ENHANCED", "PASSTHROUGH"],
        "IncludeIframeOnlyStream": bool,
        "ManifestName": str,
        "ProgramDateTimeIntervalSeconds": int,
        "RepeatExtXKey": bool,
        "StreamSelection": StreamSelectionTypeDef,
    },
    total=False,
)

_RequiredCmafPackageTypeDef = TypedDict(
    "_RequiredCmafPackageTypeDef", {"HlsManifests": List[HlsManifestTypeDef]}
)
_OptionalCmafPackageTypeDef = TypedDict(
    "_OptionalCmafPackageTypeDef",
    {"Encryption": CmafEncryptionTypeDef, "SegmentDurationSeconds": int},
    total=False,
)


class CmafPackageTypeDef(_RequiredCmafPackageTypeDef, _OptionalCmafPackageTypeDef):
    pass


EgressEndpointTypeDef = TypedDict(
    "EgressEndpointTypeDef", {"PackagingConfigurationId": str, "Url": str}, total=False
)

CreateAssetResponseTypeDef = TypedDict(
    "CreateAssetResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": str,
        "EgressEndpoints": List[EgressEndpointTypeDef],
        "Id": str,
        "PackagingGroupId": str,
        "ResourceId": str,
        "SourceArn": str,
        "SourceRoleArn": str,
    },
    total=False,
)

DashEncryptionTypeDef = TypedDict(
    "DashEncryptionTypeDef", {"SpekeKeyProvider": SpekeKeyProviderTypeDef}
)

DashManifestTypeDef = TypedDict(
    "DashManifestTypeDef",
    {
        "ManifestLayout": Literal["FULL", "COMPACT"],
        "ManifestName": str,
        "MinBufferTimeSeconds": int,
        "Profile": Literal["NONE", "HBBTV_1_5"],
        "StreamSelection": StreamSelectionTypeDef,
    },
    total=False,
)

_RequiredDashPackageTypeDef = TypedDict(
    "_RequiredDashPackageTypeDef", {"DashManifests": List[DashManifestTypeDef]}
)
_OptionalDashPackageTypeDef = TypedDict(
    "_OptionalDashPackageTypeDef",
    {
        "Encryption": DashEncryptionTypeDef,
        "PeriodTriggers": List[Literal["ADS"]],
        "SegmentDurationSeconds": int,
        "SegmentTemplateFormat": Literal[
            "NUMBER_WITH_TIMELINE", "TIME_WITH_TIMELINE", "NUMBER_WITH_DURATION"
        ],
    },
    total=False,
)


class DashPackageTypeDef(_RequiredDashPackageTypeDef, _OptionalDashPackageTypeDef):
    pass


_RequiredHlsEncryptionTypeDef = TypedDict(
    "_RequiredHlsEncryptionTypeDef", {"SpekeKeyProvider": SpekeKeyProviderTypeDef}
)
_OptionalHlsEncryptionTypeDef = TypedDict(
    "_OptionalHlsEncryptionTypeDef",
    {"ConstantInitializationVector": str, "EncryptionMethod": Literal["AES_128", "SAMPLE_AES"]},
    total=False,
)


class HlsEncryptionTypeDef(_RequiredHlsEncryptionTypeDef, _OptionalHlsEncryptionTypeDef):
    pass


_RequiredHlsPackageTypeDef = TypedDict(
    "_RequiredHlsPackageTypeDef", {"HlsManifests": List[HlsManifestTypeDef]}
)
_OptionalHlsPackageTypeDef = TypedDict(
    "_OptionalHlsPackageTypeDef",
    {
        "Encryption": HlsEncryptionTypeDef,
        "SegmentDurationSeconds": int,
        "UseAudioRenditionGroup": bool,
    },
    total=False,
)


class HlsPackageTypeDef(_RequiredHlsPackageTypeDef, _OptionalHlsPackageTypeDef):
    pass


MssEncryptionTypeDef = TypedDict(
    "MssEncryptionTypeDef", {"SpekeKeyProvider": SpekeKeyProviderTypeDef}
)

MssManifestTypeDef = TypedDict(
    "MssManifestTypeDef",
    {"ManifestName": str, "StreamSelection": StreamSelectionTypeDef},
    total=False,
)

_RequiredMssPackageTypeDef = TypedDict(
    "_RequiredMssPackageTypeDef", {"MssManifests": List[MssManifestTypeDef]}
)
_OptionalMssPackageTypeDef = TypedDict(
    "_OptionalMssPackageTypeDef",
    {"Encryption": MssEncryptionTypeDef, "SegmentDurationSeconds": int},
    total=False,
)


class MssPackageTypeDef(_RequiredMssPackageTypeDef, _OptionalMssPackageTypeDef):
    pass


CreatePackagingConfigurationResponseTypeDef = TypedDict(
    "CreatePackagingConfigurationResponseTypeDef",
    {
        "Arn": str,
        "CmafPackage": CmafPackageTypeDef,
        "DashPackage": DashPackageTypeDef,
        "HlsPackage": HlsPackageTypeDef,
        "Id": str,
        "MssPackage": MssPackageTypeDef,
        "PackagingGroupId": str,
    },
    total=False,
)

CreatePackagingGroupResponseTypeDef = TypedDict(
    "CreatePackagingGroupResponseTypeDef", {"Arn": str, "DomainName": str, "Id": str}, total=False
)

DescribeAssetResponseTypeDef = TypedDict(
    "DescribeAssetResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": str,
        "EgressEndpoints": List[EgressEndpointTypeDef],
        "Id": str,
        "PackagingGroupId": str,
        "ResourceId": str,
        "SourceArn": str,
        "SourceRoleArn": str,
    },
    total=False,
)

DescribePackagingConfigurationResponseTypeDef = TypedDict(
    "DescribePackagingConfigurationResponseTypeDef",
    {
        "Arn": str,
        "CmafPackage": CmafPackageTypeDef,
        "DashPackage": DashPackageTypeDef,
        "HlsPackage": HlsPackageTypeDef,
        "Id": str,
        "MssPackage": MssPackageTypeDef,
        "PackagingGroupId": str,
    },
    total=False,
)

DescribePackagingGroupResponseTypeDef = TypedDict(
    "DescribePackagingGroupResponseTypeDef", {"Arn": str, "DomainName": str, "Id": str}, total=False
)

AssetShallowTypeDef = TypedDict(
    "AssetShallowTypeDef",
    {
        "Arn": str,
        "CreatedAt": str,
        "Id": str,
        "PackagingGroupId": str,
        "ResourceId": str,
        "SourceArn": str,
        "SourceRoleArn": str,
    },
    total=False,
)

ListAssetsResponseTypeDef = TypedDict(
    "ListAssetsResponseTypeDef",
    {"Assets": List[AssetShallowTypeDef], "NextToken": str},
    total=False,
)

PackagingConfigurationTypeDef = TypedDict(
    "PackagingConfigurationTypeDef",
    {
        "Arn": str,
        "CmafPackage": CmafPackageTypeDef,
        "DashPackage": DashPackageTypeDef,
        "HlsPackage": HlsPackageTypeDef,
        "Id": str,
        "MssPackage": MssPackageTypeDef,
        "PackagingGroupId": str,
    },
    total=False,
)

ListPackagingConfigurationsResponseTypeDef = TypedDict(
    "ListPackagingConfigurationsResponseTypeDef",
    {"NextToken": str, "PackagingConfigurations": List[PackagingConfigurationTypeDef]},
    total=False,
)

PackagingGroupTypeDef = TypedDict(
    "PackagingGroupTypeDef", {"Arn": str, "DomainName": str, "Id": str}, total=False
)

ListPackagingGroupsResponseTypeDef = TypedDict(
    "ListPackagingGroupsResponseTypeDef",
    {"NextToken": str, "PackagingGroups": List[PackagingGroupTypeDef]},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
