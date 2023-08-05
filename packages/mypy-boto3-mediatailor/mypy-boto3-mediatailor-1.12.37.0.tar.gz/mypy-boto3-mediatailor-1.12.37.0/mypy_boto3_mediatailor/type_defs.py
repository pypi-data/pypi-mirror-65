"""
Main interface for mediatailor service type definitions.

Usage::

    from mypy_boto3.mediatailor.type_defs import CdnConfigurationTypeDef

    data: CdnConfigurationTypeDef = {...}
"""
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
    "CdnConfigurationTypeDef",
    "DashConfigurationForPutTypeDef",
    "DashConfigurationTypeDef",
    "HlsConfigurationTypeDef",
    "LivePreRollConfigurationTypeDef",
    "GetPlaybackConfigurationResponseTypeDef",
    "PlaybackConfigurationTypeDef",
    "ListPlaybackConfigurationsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutPlaybackConfigurationResponseTypeDef",
)

CdnConfigurationTypeDef = TypedDict(
    "CdnConfigurationTypeDef",
    {"AdSegmentUrlPrefix": str, "ContentSegmentUrlPrefix": str},
    total=False,
)

DashConfigurationForPutTypeDef = TypedDict(
    "DashConfigurationForPutTypeDef",
    {"MpdLocation": str, "OriginManifestType": Literal["SINGLE_PERIOD", "MULTI_PERIOD"]},
    total=False,
)

DashConfigurationTypeDef = TypedDict(
    "DashConfigurationTypeDef",
    {
        "ManifestEndpointPrefix": str,
        "MpdLocation": str,
        "OriginManifestType": Literal["SINGLE_PERIOD", "MULTI_PERIOD"],
    },
    total=False,
)

HlsConfigurationTypeDef = TypedDict(
    "HlsConfigurationTypeDef", {"ManifestEndpointPrefix": str}, total=False
)

LivePreRollConfigurationTypeDef = TypedDict(
    "LivePreRollConfigurationTypeDef",
    {"AdDecisionServerUrl": str, "MaxDurationSeconds": int},
    total=False,
)

GetPlaybackConfigurationResponseTypeDef = TypedDict(
    "GetPlaybackConfigurationResponseTypeDef",
    {
        "AdDecisionServerUrl": str,
        "CdnConfiguration": CdnConfigurationTypeDef,
        "DashConfiguration": DashConfigurationTypeDef,
        "HlsConfiguration": HlsConfigurationTypeDef,
        "LivePreRollConfiguration": LivePreRollConfigurationTypeDef,
        "Name": str,
        "PersonalizationThresholdSeconds": int,
        "PlaybackConfigurationArn": str,
        "PlaybackEndpointPrefix": str,
        "SessionInitializationEndpointPrefix": str,
        "SlateAdUrl": str,
        "Tags": Dict[str, str],
        "TranscodeProfileName": str,
        "VideoContentSourceUrl": str,
    },
    total=False,
)

PlaybackConfigurationTypeDef = TypedDict(
    "PlaybackConfigurationTypeDef",
    {
        "AdDecisionServerUrl": str,
        "CdnConfiguration": CdnConfigurationTypeDef,
        "DashConfiguration": DashConfigurationTypeDef,
        "HlsConfiguration": HlsConfigurationTypeDef,
        "Name": str,
        "PlaybackConfigurationArn": str,
        "PlaybackEndpointPrefix": str,
        "SessionInitializationEndpointPrefix": str,
        "SlateAdUrl": str,
        "Tags": Dict[str, str],
        "TranscodeProfileName": str,
        "PersonalizationThresholdSeconds": int,
        "VideoContentSourceUrl": str,
    },
    total=False,
)

ListPlaybackConfigurationsResponseTypeDef = TypedDict(
    "ListPlaybackConfigurationsResponseTypeDef",
    {"Items": List[PlaybackConfigurationTypeDef], "NextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutPlaybackConfigurationResponseTypeDef = TypedDict(
    "PutPlaybackConfigurationResponseTypeDef",
    {
        "AdDecisionServerUrl": str,
        "CdnConfiguration": CdnConfigurationTypeDef,
        "DashConfiguration": DashConfigurationTypeDef,
        "HlsConfiguration": HlsConfigurationTypeDef,
        "LivePreRollConfiguration": LivePreRollConfigurationTypeDef,
        "Name": str,
        "PersonalizationThresholdSeconds": int,
        "PlaybackConfigurationArn": str,
        "PlaybackEndpointPrefix": str,
        "SessionInitializationEndpointPrefix": str,
        "SlateAdUrl": str,
        "Tags": Dict[str, str],
        "TranscodeProfileName": str,
        "VideoContentSourceUrl": str,
    },
    total=False,
)
