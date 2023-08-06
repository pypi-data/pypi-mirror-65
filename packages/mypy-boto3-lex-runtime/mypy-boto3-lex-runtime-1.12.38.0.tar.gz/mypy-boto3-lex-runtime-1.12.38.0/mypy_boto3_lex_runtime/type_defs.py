"""
Main interface for lex-runtime service type definitions.

Usage::

    from mypy_boto3.lex_runtime.type_defs import DeleteSessionResponseTypeDef

    data: DeleteSessionResponseTypeDef = {...}
"""
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
    "DeleteSessionResponseTypeDef",
    "DialogActionTypeDef",
    "IntentSummaryTypeDef",
    "GetSessionResponseTypeDef",
    "PostContentResponseTypeDef",
    "ButtonTypeDef",
    "GenericAttachmentTypeDef",
    "ResponseCardTypeDef",
    "SentimentResponseTypeDef",
    "PostTextResponseTypeDef",
    "PutSessionResponseTypeDef",
)

DeleteSessionResponseTypeDef = TypedDict(
    "DeleteSessionResponseTypeDef",
    {"botName": str, "botAlias": str, "userId": str, "sessionId": str},
    total=False,
)

_RequiredDialogActionTypeDef = TypedDict(
    "_RequiredDialogActionTypeDef",
    {"type": Literal["ElicitIntent", "ConfirmIntent", "ElicitSlot", "Close", "Delegate"]},
)
_OptionalDialogActionTypeDef = TypedDict(
    "_OptionalDialogActionTypeDef",
    {
        "intentName": str,
        "slots": Dict[str, str],
        "slotToElicit": str,
        "fulfillmentState": Literal["Fulfilled", "Failed", "ReadyForFulfillment"],
        "message": str,
        "messageFormat": Literal["PlainText", "CustomPayload", "SSML", "Composite"],
    },
    total=False,
)


class DialogActionTypeDef(_RequiredDialogActionTypeDef, _OptionalDialogActionTypeDef):
    pass


_RequiredIntentSummaryTypeDef = TypedDict(
    "_RequiredIntentSummaryTypeDef",
    {
        "dialogActionType": Literal[
            "ElicitIntent", "ConfirmIntent", "ElicitSlot", "Close", "Delegate"
        ]
    },
)
_OptionalIntentSummaryTypeDef = TypedDict(
    "_OptionalIntentSummaryTypeDef",
    {
        "intentName": str,
        "checkpointLabel": str,
        "slots": Dict[str, str],
        "confirmationStatus": Literal["None", "Confirmed", "Denied"],
        "fulfillmentState": Literal["Fulfilled", "Failed", "ReadyForFulfillment"],
        "slotToElicit": str,
    },
    total=False,
)


class IntentSummaryTypeDef(_RequiredIntentSummaryTypeDef, _OptionalIntentSummaryTypeDef):
    pass


GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "recentIntentSummaryView": List[IntentSummaryTypeDef],
        "sessionAttributes": Dict[str, str],
        "sessionId": str,
        "dialogAction": DialogActionTypeDef,
    },
    total=False,
)

PostContentResponseTypeDef = TypedDict(
    "PostContentResponseTypeDef",
    {
        "contentType": str,
        "intentName": str,
        "slots": str,
        "sessionAttributes": str,
        "sentimentResponse": str,
        "message": str,
        "messageFormat": Literal["PlainText", "CustomPayload", "SSML", "Composite"],
        "dialogState": Literal[
            "ElicitIntent",
            "ConfirmIntent",
            "ElicitSlot",
            "Fulfilled",
            "ReadyForFulfillment",
            "Failed",
        ],
        "slotToElicit": str,
        "inputTranscript": str,
        "audioStream": Union[bytes, IO],
        "sessionId": str,
    },
    total=False,
)

ButtonTypeDef = TypedDict("ButtonTypeDef", {"text": str, "value": str})

GenericAttachmentTypeDef = TypedDict(
    "GenericAttachmentTypeDef",
    {
        "title": str,
        "subTitle": str,
        "attachmentLinkUrl": str,
        "imageUrl": str,
        "buttons": List[ButtonTypeDef],
    },
    total=False,
)

ResponseCardTypeDef = TypedDict(
    "ResponseCardTypeDef",
    {
        "version": str,
        "contentType": Literal["application/vnd.amazonaws.card.generic"],
        "genericAttachments": List[GenericAttachmentTypeDef],
    },
    total=False,
)

SentimentResponseTypeDef = TypedDict(
    "SentimentResponseTypeDef", {"sentimentLabel": str, "sentimentScore": str}, total=False
)

PostTextResponseTypeDef = TypedDict(
    "PostTextResponseTypeDef",
    {
        "intentName": str,
        "slots": Dict[str, str],
        "sessionAttributes": Dict[str, str],
        "message": str,
        "sentimentResponse": SentimentResponseTypeDef,
        "messageFormat": Literal["PlainText", "CustomPayload", "SSML", "Composite"],
        "dialogState": Literal[
            "ElicitIntent",
            "ConfirmIntent",
            "ElicitSlot",
            "Fulfilled",
            "ReadyForFulfillment",
            "Failed",
        ],
        "slotToElicit": str,
        "responseCard": ResponseCardTypeDef,
        "sessionId": str,
    },
    total=False,
)

PutSessionResponseTypeDef = TypedDict(
    "PutSessionResponseTypeDef",
    {
        "contentType": str,
        "intentName": str,
        "slots": str,
        "sessionAttributes": str,
        "message": str,
        "messageFormat": Literal["PlainText", "CustomPayload", "SSML", "Composite"],
        "dialogState": Literal[
            "ElicitIntent",
            "ConfirmIntent",
            "ElicitSlot",
            "Fulfilled",
            "ReadyForFulfillment",
            "Failed",
        ],
        "slotToElicit": str,
        "audioStream": Union[bytes, IO],
        "sessionId": str,
    },
    total=False,
)
