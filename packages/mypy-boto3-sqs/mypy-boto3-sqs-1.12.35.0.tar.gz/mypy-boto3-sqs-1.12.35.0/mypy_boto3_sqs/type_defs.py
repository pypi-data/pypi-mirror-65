"""
Main interface for sqs service type definitions.

Usage::

    from mypy_boto3.sqs.type_defs import ChangeMessageVisibilityBatchRequestEntryTypeDef

    data: ChangeMessageVisibilityBatchRequestEntryTypeDef = {...}
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
    "ChangeMessageVisibilityBatchRequestEntryTypeDef",
    "BatchResultErrorEntryTypeDef",
    "ChangeMessageVisibilityBatchResultEntryTypeDef",
    "ChangeMessageVisibilityBatchResultTypeDef",
    "CreateQueueResultTypeDef",
    "DeleteMessageBatchRequestEntryTypeDef",
    "DeleteMessageBatchResultEntryTypeDef",
    "DeleteMessageBatchResultTypeDef",
    "GetQueueAttributesResultTypeDef",
    "GetQueueUrlResultTypeDef",
    "ListDeadLetterSourceQueuesResultTypeDef",
    "ListQueueTagsResultTypeDef",
    "ListQueuesResultTypeDef",
    "MessageAttributeValueTypeDef",
    "MessageSystemAttributeValueTypeDef",
    "MessageTypeDef",
    "ReceiveMessageResultTypeDef",
    "SendMessageBatchRequestEntryTypeDef",
    "SendMessageBatchResultEntryTypeDef",
    "SendMessageBatchResultTypeDef",
    "SendMessageResultTypeDef",
)

_RequiredChangeMessageVisibilityBatchRequestEntryTypeDef = TypedDict(
    "_RequiredChangeMessageVisibilityBatchRequestEntryTypeDef", {"Id": str, "ReceiptHandle": str}
)
_OptionalChangeMessageVisibilityBatchRequestEntryTypeDef = TypedDict(
    "_OptionalChangeMessageVisibilityBatchRequestEntryTypeDef",
    {"VisibilityTimeout": int},
    total=False,
)


class ChangeMessageVisibilityBatchRequestEntryTypeDef(
    _RequiredChangeMessageVisibilityBatchRequestEntryTypeDef,
    _OptionalChangeMessageVisibilityBatchRequestEntryTypeDef,
):
    pass


_RequiredBatchResultErrorEntryTypeDef = TypedDict(
    "_RequiredBatchResultErrorEntryTypeDef", {"Id": str, "SenderFault": bool, "Code": str}
)
_OptionalBatchResultErrorEntryTypeDef = TypedDict(
    "_OptionalBatchResultErrorEntryTypeDef", {"Message": str}, total=False
)


class BatchResultErrorEntryTypeDef(
    _RequiredBatchResultErrorEntryTypeDef, _OptionalBatchResultErrorEntryTypeDef
):
    pass


ChangeMessageVisibilityBatchResultEntryTypeDef = TypedDict(
    "ChangeMessageVisibilityBatchResultEntryTypeDef", {"Id": str}
)

ChangeMessageVisibilityBatchResultTypeDef = TypedDict(
    "ChangeMessageVisibilityBatchResultTypeDef",
    {
        "Successful": List[ChangeMessageVisibilityBatchResultEntryTypeDef],
        "Failed": List[BatchResultErrorEntryTypeDef],
    },
)

CreateQueueResultTypeDef = TypedDict("CreateQueueResultTypeDef", {"QueueUrl": str}, total=False)

DeleteMessageBatchRequestEntryTypeDef = TypedDict(
    "DeleteMessageBatchRequestEntryTypeDef", {"Id": str, "ReceiptHandle": str}
)

DeleteMessageBatchResultEntryTypeDef = TypedDict(
    "DeleteMessageBatchResultEntryTypeDef", {"Id": str}
)

DeleteMessageBatchResultTypeDef = TypedDict(
    "DeleteMessageBatchResultTypeDef",
    {
        "Successful": List[DeleteMessageBatchResultEntryTypeDef],
        "Failed": List[BatchResultErrorEntryTypeDef],
    },
)

GetQueueAttributesResultTypeDef = TypedDict(
    "GetQueueAttributesResultTypeDef",
    {
        "Attributes": Dict[
            Literal[
                "All",
                "Policy",
                "VisibilityTimeout",
                "MaximumMessageSize",
                "MessageRetentionPeriod",
                "ApproximateNumberOfMessages",
                "ApproximateNumberOfMessagesNotVisible",
                "CreatedTimestamp",
                "LastModifiedTimestamp",
                "QueueArn",
                "ApproximateNumberOfMessagesDelayed",
                "DelaySeconds",
                "ReceiveMessageWaitTimeSeconds",
                "RedrivePolicy",
                "FifoQueue",
                "ContentBasedDeduplication",
                "KmsMasterKeyId",
                "KmsDataKeyReusePeriodSeconds",
            ],
            str,
        ]
    },
    total=False,
)

GetQueueUrlResultTypeDef = TypedDict("GetQueueUrlResultTypeDef", {"QueueUrl": str}, total=False)

ListDeadLetterSourceQueuesResultTypeDef = TypedDict(
    "ListDeadLetterSourceQueuesResultTypeDef", {"queueUrls": List[str]}
)

ListQueueTagsResultTypeDef = TypedDict(
    "ListQueueTagsResultTypeDef", {"Tags": Dict[str, str]}, total=False
)

ListQueuesResultTypeDef = TypedDict(
    "ListQueuesResultTypeDef", {"QueueUrls": List[str]}, total=False
)

_RequiredMessageAttributeValueTypeDef = TypedDict(
    "_RequiredMessageAttributeValueTypeDef", {"DataType": str}
)
_OptionalMessageAttributeValueTypeDef = TypedDict(
    "_OptionalMessageAttributeValueTypeDef",
    {
        "StringValue": str,
        "BinaryValue": Union[bytes, IO],
        "StringListValues": List[str],
        "BinaryListValues": List[Union[bytes, IO]],
    },
    total=False,
)


class MessageAttributeValueTypeDef(
    _RequiredMessageAttributeValueTypeDef, _OptionalMessageAttributeValueTypeDef
):
    pass


_RequiredMessageSystemAttributeValueTypeDef = TypedDict(
    "_RequiredMessageSystemAttributeValueTypeDef", {"DataType": str}
)
_OptionalMessageSystemAttributeValueTypeDef = TypedDict(
    "_OptionalMessageSystemAttributeValueTypeDef",
    {
        "StringValue": str,
        "BinaryValue": Union[bytes, IO],
        "StringListValues": List[str],
        "BinaryListValues": List[Union[bytes, IO]],
    },
    total=False,
)


class MessageSystemAttributeValueTypeDef(
    _RequiredMessageSystemAttributeValueTypeDef, _OptionalMessageSystemAttributeValueTypeDef
):
    pass


MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "MessageId": str,
        "ReceiptHandle": str,
        "MD5OfBody": str,
        "Body": str,
        "Attributes": Dict[
            Literal[
                "SenderId",
                "SentTimestamp",
                "ApproximateReceiveCount",
                "ApproximateFirstReceiveTimestamp",
                "SequenceNumber",
                "MessageDeduplicationId",
                "MessageGroupId",
                "AWSTraceHeader",
            ],
            str,
        ],
        "MD5OfMessageAttributes": str,
        "MessageAttributes": Dict[str, MessageAttributeValueTypeDef],
    },
    total=False,
)

ReceiveMessageResultTypeDef = TypedDict(
    "ReceiveMessageResultTypeDef", {"Messages": List[MessageTypeDef]}, total=False
)

_RequiredSendMessageBatchRequestEntryTypeDef = TypedDict(
    "_RequiredSendMessageBatchRequestEntryTypeDef", {"Id": str, "MessageBody": str}
)
_OptionalSendMessageBatchRequestEntryTypeDef = TypedDict(
    "_OptionalSendMessageBatchRequestEntryTypeDef",
    {
        "DelaySeconds": int,
        "MessageAttributes": Dict[str, MessageAttributeValueTypeDef],
        "MessageSystemAttributes": Dict[
            Literal["AWSTraceHeader"], MessageSystemAttributeValueTypeDef
        ],
        "MessageDeduplicationId": str,
        "MessageGroupId": str,
    },
    total=False,
)


class SendMessageBatchRequestEntryTypeDef(
    _RequiredSendMessageBatchRequestEntryTypeDef, _OptionalSendMessageBatchRequestEntryTypeDef
):
    pass


_RequiredSendMessageBatchResultEntryTypeDef = TypedDict(
    "_RequiredSendMessageBatchResultEntryTypeDef",
    {"Id": str, "MessageId": str, "MD5OfMessageBody": str},
)
_OptionalSendMessageBatchResultEntryTypeDef = TypedDict(
    "_OptionalSendMessageBatchResultEntryTypeDef",
    {"MD5OfMessageAttributes": str, "MD5OfMessageSystemAttributes": str, "SequenceNumber": str},
    total=False,
)


class SendMessageBatchResultEntryTypeDef(
    _RequiredSendMessageBatchResultEntryTypeDef, _OptionalSendMessageBatchResultEntryTypeDef
):
    pass


SendMessageBatchResultTypeDef = TypedDict(
    "SendMessageBatchResultTypeDef",
    {
        "Successful": List[SendMessageBatchResultEntryTypeDef],
        "Failed": List[BatchResultErrorEntryTypeDef],
    },
)

SendMessageResultTypeDef = TypedDict(
    "SendMessageResultTypeDef",
    {
        "MD5OfMessageBody": str,
        "MD5OfMessageAttributes": str,
        "MD5OfMessageSystemAttributes": str,
        "MessageId": str,
        "SequenceNumber": str,
    },
    total=False,
)
