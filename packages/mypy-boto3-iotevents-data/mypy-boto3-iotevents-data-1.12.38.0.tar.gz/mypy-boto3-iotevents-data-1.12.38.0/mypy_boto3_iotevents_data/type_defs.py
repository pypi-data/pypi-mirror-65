"""
Main interface for iotevents-data service type definitions.

Usage::

    from mypy_boto3.iotevents_data.type_defs import BatchPutMessageErrorEntryTypeDef

    data: BatchPutMessageErrorEntryTypeDef = {...}
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
    "BatchPutMessageErrorEntryTypeDef",
    "BatchPutMessageResponseTypeDef",
    "BatchUpdateDetectorErrorEntryTypeDef",
    "BatchUpdateDetectorResponseTypeDef",
    "TimerTypeDef",
    "VariableTypeDef",
    "DetectorStateTypeDef",
    "DetectorTypeDef",
    "DescribeDetectorResponseTypeDef",
    "DetectorStateSummaryTypeDef",
    "DetectorSummaryTypeDef",
    "ListDetectorsResponseTypeDef",
    "MessageTypeDef",
    "TimerDefinitionTypeDef",
    "VariableDefinitionTypeDef",
    "DetectorStateDefinitionTypeDef",
    "UpdateDetectorRequestTypeDef",
)

BatchPutMessageErrorEntryTypeDef = TypedDict(
    "BatchPutMessageErrorEntryTypeDef",
    {
        "messageId": str,
        "errorCode": Literal[
            "ResourceNotFoundException",
            "InvalidRequestException",
            "InternalFailureException",
            "ServiceUnavailableException",
            "ThrottlingException",
        ],
        "errorMessage": str,
    },
    total=False,
)

BatchPutMessageResponseTypeDef = TypedDict(
    "BatchPutMessageResponseTypeDef",
    {"BatchPutMessageErrorEntries": List[BatchPutMessageErrorEntryTypeDef]},
    total=False,
)

BatchUpdateDetectorErrorEntryTypeDef = TypedDict(
    "BatchUpdateDetectorErrorEntryTypeDef",
    {
        "messageId": str,
        "errorCode": Literal[
            "ResourceNotFoundException",
            "InvalidRequestException",
            "InternalFailureException",
            "ServiceUnavailableException",
            "ThrottlingException",
        ],
        "errorMessage": str,
    },
    total=False,
)

BatchUpdateDetectorResponseTypeDef = TypedDict(
    "BatchUpdateDetectorResponseTypeDef",
    {"batchUpdateDetectorErrorEntries": List[BatchUpdateDetectorErrorEntryTypeDef]},
    total=False,
)

TimerTypeDef = TypedDict("TimerTypeDef", {"name": str, "timestamp": datetime})

VariableTypeDef = TypedDict("VariableTypeDef", {"name": str, "value": str})

DetectorStateTypeDef = TypedDict(
    "DetectorStateTypeDef",
    {"stateName": str, "variables": List[VariableTypeDef], "timers": List[TimerTypeDef]},
)

DetectorTypeDef = TypedDict(
    "DetectorTypeDef",
    {
        "detectorModelName": str,
        "keyValue": str,
        "detectorModelVersion": str,
        "state": DetectorStateTypeDef,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

DescribeDetectorResponseTypeDef = TypedDict(
    "DescribeDetectorResponseTypeDef", {"detector": DetectorTypeDef}, total=False
)

DetectorStateSummaryTypeDef = TypedDict(
    "DetectorStateSummaryTypeDef", {"stateName": str}, total=False
)

DetectorSummaryTypeDef = TypedDict(
    "DetectorSummaryTypeDef",
    {
        "detectorModelName": str,
        "keyValue": str,
        "detectorModelVersion": str,
        "state": DetectorStateSummaryTypeDef,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

ListDetectorsResponseTypeDef = TypedDict(
    "ListDetectorsResponseTypeDef",
    {"detectorSummaries": List[DetectorSummaryTypeDef], "nextToken": str},
    total=False,
)

MessageTypeDef = TypedDict(
    "MessageTypeDef", {"messageId": str, "inputName": str, "payload": Union[bytes, IO]}
)

TimerDefinitionTypeDef = TypedDict("TimerDefinitionTypeDef", {"name": str, "seconds": int})

VariableDefinitionTypeDef = TypedDict("VariableDefinitionTypeDef", {"name": str, "value": str})

DetectorStateDefinitionTypeDef = TypedDict(
    "DetectorStateDefinitionTypeDef",
    {
        "stateName": str,
        "variables": List[VariableDefinitionTypeDef],
        "timers": List[TimerDefinitionTypeDef],
    },
)

_RequiredUpdateDetectorRequestTypeDef = TypedDict(
    "_RequiredUpdateDetectorRequestTypeDef",
    {"messageId": str, "detectorModelName": str, "state": DetectorStateDefinitionTypeDef},
)
_OptionalUpdateDetectorRequestTypeDef = TypedDict(
    "_OptionalUpdateDetectorRequestTypeDef", {"keyValue": str}, total=False
)


class UpdateDetectorRequestTypeDef(
    _RequiredUpdateDetectorRequestTypeDef, _OptionalUpdateDetectorRequestTypeDef
):
    pass
