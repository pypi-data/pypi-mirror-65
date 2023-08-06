"""
Main interface for iotevents service type definitions.

Usage::

    from mypy_boto3.iotevents.type_defs import DetectorModelConfigurationTypeDef

    data: DetectorModelConfigurationTypeDef = {...}
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
    "DetectorModelConfigurationTypeDef",
    "CreateDetectorModelResponseTypeDef",
    "InputConfigurationTypeDef",
    "CreateInputResponseTypeDef",
    "ClearTimerActionTypeDef",
    "FirehoseActionTypeDef",
    "IotEventsActionTypeDef",
    "IotTopicPublishActionTypeDef",
    "LambdaActionTypeDef",
    "ResetTimerActionTypeDef",
    "SNSTopicPublishActionTypeDef",
    "SetTimerActionTypeDef",
    "SetVariableActionTypeDef",
    "SqsActionTypeDef",
    "ActionTypeDef",
    "EventTypeDef",
    "OnEnterLifecycleTypeDef",
    "OnExitLifecycleTypeDef",
    "TransitionEventTypeDef",
    "OnInputLifecycleTypeDef",
    "StateTypeDef",
    "DetectorModelDefinitionTypeDef",
    "DetectorModelTypeDef",
    "DescribeDetectorModelResponseTypeDef",
    "AttributeTypeDef",
    "InputDefinitionTypeDef",
    "InputTypeDef",
    "DescribeInputResponseTypeDef",
    "DetectorDebugOptionTypeDef",
    "LoggingOptionsTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "DetectorModelVersionSummaryTypeDef",
    "ListDetectorModelVersionsResponseTypeDef",
    "DetectorModelSummaryTypeDef",
    "ListDetectorModelsResponseTypeDef",
    "InputSummaryTypeDef",
    "ListInputsResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateDetectorModelResponseTypeDef",
    "UpdateInputResponseTypeDef",
)

DetectorModelConfigurationTypeDef = TypedDict(
    "DetectorModelConfigurationTypeDef",
    {
        "detectorModelName": str,
        "detectorModelVersion": str,
        "detectorModelDescription": str,
        "detectorModelArn": str,
        "roleArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": Literal[
            "ACTIVE", "ACTIVATING", "INACTIVE", "DEPRECATED", "DRAFT", "PAUSED", "FAILED"
        ],
        "key": str,
        "evaluationMethod": Literal["BATCH", "SERIAL"],
    },
    total=False,
)

CreateDetectorModelResponseTypeDef = TypedDict(
    "CreateDetectorModelResponseTypeDef",
    {"detectorModelConfiguration": DetectorModelConfigurationTypeDef},
    total=False,
)

_RequiredInputConfigurationTypeDef = TypedDict(
    "_RequiredInputConfigurationTypeDef",
    {
        "inputName": str,
        "inputArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": Literal["CREATING", "UPDATING", "ACTIVE", "DELETING"],
    },
)
_OptionalInputConfigurationTypeDef = TypedDict(
    "_OptionalInputConfigurationTypeDef", {"inputDescription": str}, total=False
)


class InputConfigurationTypeDef(
    _RequiredInputConfigurationTypeDef, _OptionalInputConfigurationTypeDef
):
    pass


CreateInputResponseTypeDef = TypedDict(
    "CreateInputResponseTypeDef", {"inputConfiguration": InputConfigurationTypeDef}, total=False
)

ClearTimerActionTypeDef = TypedDict("ClearTimerActionTypeDef", {"timerName": str})

_RequiredFirehoseActionTypeDef = TypedDict(
    "_RequiredFirehoseActionTypeDef", {"deliveryStreamName": str}
)
_OptionalFirehoseActionTypeDef = TypedDict(
    "_OptionalFirehoseActionTypeDef", {"separator": str}, total=False
)


class FirehoseActionTypeDef(_RequiredFirehoseActionTypeDef, _OptionalFirehoseActionTypeDef):
    pass


IotEventsActionTypeDef = TypedDict("IotEventsActionTypeDef", {"inputName": str})

IotTopicPublishActionTypeDef = TypedDict("IotTopicPublishActionTypeDef", {"mqttTopic": str})

LambdaActionTypeDef = TypedDict("LambdaActionTypeDef", {"functionArn": str})

ResetTimerActionTypeDef = TypedDict("ResetTimerActionTypeDef", {"timerName": str})

SNSTopicPublishActionTypeDef = TypedDict("SNSTopicPublishActionTypeDef", {"targetArn": str})

_RequiredSetTimerActionTypeDef = TypedDict("_RequiredSetTimerActionTypeDef", {"timerName": str})
_OptionalSetTimerActionTypeDef = TypedDict(
    "_OptionalSetTimerActionTypeDef", {"seconds": int, "durationExpression": str}, total=False
)


class SetTimerActionTypeDef(_RequiredSetTimerActionTypeDef, _OptionalSetTimerActionTypeDef):
    pass


SetVariableActionTypeDef = TypedDict(
    "SetVariableActionTypeDef", {"variableName": str, "value": str}
)

_RequiredSqsActionTypeDef = TypedDict("_RequiredSqsActionTypeDef", {"queueUrl": str})
_OptionalSqsActionTypeDef = TypedDict("_OptionalSqsActionTypeDef", {"useBase64": bool}, total=False)


class SqsActionTypeDef(_RequiredSqsActionTypeDef, _OptionalSqsActionTypeDef):
    pass


ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "setVariable": SetVariableActionTypeDef,
        "sns": SNSTopicPublishActionTypeDef,
        "iotTopicPublish": IotTopicPublishActionTypeDef,
        "setTimer": SetTimerActionTypeDef,
        "clearTimer": ClearTimerActionTypeDef,
        "resetTimer": ResetTimerActionTypeDef,
        "lambda": LambdaActionTypeDef,
        "iotEvents": IotEventsActionTypeDef,
        "sqs": SqsActionTypeDef,
        "firehose": FirehoseActionTypeDef,
    },
    total=False,
)

_RequiredEventTypeDef = TypedDict("_RequiredEventTypeDef", {"eventName": str})
_OptionalEventTypeDef = TypedDict(
    "_OptionalEventTypeDef", {"condition": str, "actions": List[ActionTypeDef]}, total=False
)


class EventTypeDef(_RequiredEventTypeDef, _OptionalEventTypeDef):
    pass


OnEnterLifecycleTypeDef = TypedDict(
    "OnEnterLifecycleTypeDef", {"events": List[EventTypeDef]}, total=False
)

OnExitLifecycleTypeDef = TypedDict(
    "OnExitLifecycleTypeDef", {"events": List[EventTypeDef]}, total=False
)

_RequiredTransitionEventTypeDef = TypedDict(
    "_RequiredTransitionEventTypeDef", {"eventName": str, "condition": str, "nextState": str}
)
_OptionalTransitionEventTypeDef = TypedDict(
    "_OptionalTransitionEventTypeDef", {"actions": List[ActionTypeDef]}, total=False
)


class TransitionEventTypeDef(_RequiredTransitionEventTypeDef, _OptionalTransitionEventTypeDef):
    pass


OnInputLifecycleTypeDef = TypedDict(
    "OnInputLifecycleTypeDef",
    {"events": List[EventTypeDef], "transitionEvents": List[TransitionEventTypeDef]},
    total=False,
)

_RequiredStateTypeDef = TypedDict("_RequiredStateTypeDef", {"stateName": str})
_OptionalStateTypeDef = TypedDict(
    "_OptionalStateTypeDef",
    {
        "onInput": OnInputLifecycleTypeDef,
        "onEnter": OnEnterLifecycleTypeDef,
        "onExit": OnExitLifecycleTypeDef,
    },
    total=False,
)


class StateTypeDef(_RequiredStateTypeDef, _OptionalStateTypeDef):
    pass


DetectorModelDefinitionTypeDef = TypedDict(
    "DetectorModelDefinitionTypeDef", {"states": List[StateTypeDef], "initialStateName": str}
)

DetectorModelTypeDef = TypedDict(
    "DetectorModelTypeDef",
    {
        "detectorModelDefinition": DetectorModelDefinitionTypeDef,
        "detectorModelConfiguration": DetectorModelConfigurationTypeDef,
    },
    total=False,
)

DescribeDetectorModelResponseTypeDef = TypedDict(
    "DescribeDetectorModelResponseTypeDef", {"detectorModel": DetectorModelTypeDef}, total=False
)

AttributeTypeDef = TypedDict("AttributeTypeDef", {"jsonPath": str})

InputDefinitionTypeDef = TypedDict("InputDefinitionTypeDef", {"attributes": List[AttributeTypeDef]})

InputTypeDef = TypedDict(
    "InputTypeDef",
    {"inputConfiguration": InputConfigurationTypeDef, "inputDefinition": InputDefinitionTypeDef},
    total=False,
)

DescribeInputResponseTypeDef = TypedDict(
    "DescribeInputResponseTypeDef", {"input": InputTypeDef}, total=False
)

_RequiredDetectorDebugOptionTypeDef = TypedDict(
    "_RequiredDetectorDebugOptionTypeDef", {"detectorModelName": str}
)
_OptionalDetectorDebugOptionTypeDef = TypedDict(
    "_OptionalDetectorDebugOptionTypeDef", {"keyValue": str}, total=False
)


class DetectorDebugOptionTypeDef(
    _RequiredDetectorDebugOptionTypeDef, _OptionalDetectorDebugOptionTypeDef
):
    pass


_RequiredLoggingOptionsTypeDef = TypedDict(
    "_RequiredLoggingOptionsTypeDef",
    {"roleArn": str, "level": Literal["ERROR", "INFO", "DEBUG"], "enabled": bool},
)
_OptionalLoggingOptionsTypeDef = TypedDict(
    "_OptionalLoggingOptionsTypeDef",
    {"detectorDebugOptions": List[DetectorDebugOptionTypeDef]},
    total=False,
)


class LoggingOptionsTypeDef(_RequiredLoggingOptionsTypeDef, _OptionalLoggingOptionsTypeDef):
    pass


DescribeLoggingOptionsResponseTypeDef = TypedDict(
    "DescribeLoggingOptionsResponseTypeDef", {"loggingOptions": LoggingOptionsTypeDef}, total=False
)

DetectorModelVersionSummaryTypeDef = TypedDict(
    "DetectorModelVersionSummaryTypeDef",
    {
        "detectorModelName": str,
        "detectorModelVersion": str,
        "detectorModelArn": str,
        "roleArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": Literal[
            "ACTIVE", "ACTIVATING", "INACTIVE", "DEPRECATED", "DRAFT", "PAUSED", "FAILED"
        ],
        "evaluationMethod": Literal["BATCH", "SERIAL"],
    },
    total=False,
)

ListDetectorModelVersionsResponseTypeDef = TypedDict(
    "ListDetectorModelVersionsResponseTypeDef",
    {"detectorModelVersionSummaries": List[DetectorModelVersionSummaryTypeDef], "nextToken": str},
    total=False,
)

DetectorModelSummaryTypeDef = TypedDict(
    "DetectorModelSummaryTypeDef",
    {"detectorModelName": str, "detectorModelDescription": str, "creationTime": datetime},
    total=False,
)

ListDetectorModelsResponseTypeDef = TypedDict(
    "ListDetectorModelsResponseTypeDef",
    {"detectorModelSummaries": List[DetectorModelSummaryTypeDef], "nextToken": str},
    total=False,
)

InputSummaryTypeDef = TypedDict(
    "InputSummaryTypeDef",
    {
        "inputName": str,
        "inputDescription": str,
        "inputArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": Literal["CREATING", "UPDATING", "ACTIVE", "DELETING"],
    },
    total=False,
)

ListInputsResponseTypeDef = TypedDict(
    "ListInputsResponseTypeDef",
    {"inputSummaries": List[InputSummaryTypeDef], "nextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"key": str, "value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": List[TagTypeDef]}, total=False
)

UpdateDetectorModelResponseTypeDef = TypedDict(
    "UpdateDetectorModelResponseTypeDef",
    {"detectorModelConfiguration": DetectorModelConfigurationTypeDef},
    total=False,
)

UpdateInputResponseTypeDef = TypedDict(
    "UpdateInputResponseTypeDef", {"inputConfiguration": InputConfigurationTypeDef}, total=False
)
