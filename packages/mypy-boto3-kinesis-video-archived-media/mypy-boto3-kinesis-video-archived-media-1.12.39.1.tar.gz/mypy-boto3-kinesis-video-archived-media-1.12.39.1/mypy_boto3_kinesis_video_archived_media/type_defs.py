"""
Main interface for kinesis-video-archived-media service type definitions.

Usage::

    from mypy_boto3.kinesis_video_archived_media.type_defs import DASHTimestampRangeTypeDef

    data: DASHTimestampRangeTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DASHTimestampRangeTypeDef",
    "DASHFragmentSelectorTypeDef",
    "TimestampRangeTypeDef",
    "FragmentSelectorTypeDef",
    "GetDASHStreamingSessionURLOutputTypeDef",
    "GetHLSStreamingSessionURLOutputTypeDef",
    "GetMediaForFragmentListOutputTypeDef",
    "HLSTimestampRangeTypeDef",
    "HLSFragmentSelectorTypeDef",
    "FragmentTypeDef",
    "ListFragmentsOutputTypeDef",
    "PaginatorConfigTypeDef",
)

DASHTimestampRangeTypeDef = TypedDict(
    "DASHTimestampRangeTypeDef", {"StartTimestamp": datetime, "EndTimestamp": datetime}, total=False
)

DASHFragmentSelectorTypeDef = TypedDict(
    "DASHFragmentSelectorTypeDef",
    {
        "FragmentSelectorType": Literal["PRODUCER_TIMESTAMP", "SERVER_TIMESTAMP"],
        "TimestampRange": DASHTimestampRangeTypeDef,
    },
    total=False,
)

TimestampRangeTypeDef = TypedDict(
    "TimestampRangeTypeDef", {"StartTimestamp": datetime, "EndTimestamp": datetime}
)

FragmentSelectorTypeDef = TypedDict(
    "FragmentSelectorTypeDef",
    {
        "FragmentSelectorType": Literal["PRODUCER_TIMESTAMP", "SERVER_TIMESTAMP"],
        "TimestampRange": TimestampRangeTypeDef,
    },
)

GetDASHStreamingSessionURLOutputTypeDef = TypedDict(
    "GetDASHStreamingSessionURLOutputTypeDef", {"DASHStreamingSessionURL": str}, total=False
)

GetHLSStreamingSessionURLOutputTypeDef = TypedDict(
    "GetHLSStreamingSessionURLOutputTypeDef", {"HLSStreamingSessionURL": str}, total=False
)

GetMediaForFragmentListOutputTypeDef = TypedDict(
    "GetMediaForFragmentListOutputTypeDef",
    {"ContentType": str, "Payload": Union[bytes, IO]},
    total=False,
)

HLSTimestampRangeTypeDef = TypedDict(
    "HLSTimestampRangeTypeDef", {"StartTimestamp": datetime, "EndTimestamp": datetime}, total=False
)

HLSFragmentSelectorTypeDef = TypedDict(
    "HLSFragmentSelectorTypeDef",
    {
        "FragmentSelectorType": Literal["PRODUCER_TIMESTAMP", "SERVER_TIMESTAMP"],
        "TimestampRange": HLSTimestampRangeTypeDef,
    },
    total=False,
)

FragmentTypeDef = TypedDict(
    "FragmentTypeDef",
    {
        "FragmentNumber": str,
        "FragmentSizeInBytes": int,
        "ProducerTimestamp": datetime,
        "ServerTimestamp": datetime,
        "FragmentLengthInMilliseconds": int,
    },
    total=False,
)

ListFragmentsOutputTypeDef = TypedDict(
    "ListFragmentsOutputTypeDef",
    {"Fragments": List[FragmentTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
