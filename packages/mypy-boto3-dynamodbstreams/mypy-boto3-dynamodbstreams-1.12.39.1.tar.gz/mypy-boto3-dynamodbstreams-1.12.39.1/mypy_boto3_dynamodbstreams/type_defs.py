"""
Main interface for dynamodbstreams service type definitions.

Usage::

    from mypy_boto3.dynamodbstreams.type_defs import KeySchemaElementTypeDef

    data: KeySchemaElementTypeDef = {...}
"""
from datetime import datetime
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
    "KeySchemaElementTypeDef",
    "SequenceNumberRangeTypeDef",
    "ShardTypeDef",
    "StreamDescriptionTypeDef",
    "DescribeStreamOutputTypeDef",
    "IdentityTypeDef",
    "AttributeValueTypeDef",
    "StreamRecordTypeDef",
    "RecordTypeDef",
    "GetRecordsOutputTypeDef",
    "GetShardIteratorOutputTypeDef",
    "StreamTypeDef",
    "ListStreamsOutputTypeDef",
)

KeySchemaElementTypeDef = TypedDict(
    "KeySchemaElementTypeDef", {"AttributeName": str, "KeyType": Literal["HASH", "RANGE"]}
)

SequenceNumberRangeTypeDef = TypedDict(
    "SequenceNumberRangeTypeDef",
    {"StartingSequenceNumber": str, "EndingSequenceNumber": str},
    total=False,
)

ShardTypeDef = TypedDict(
    "ShardTypeDef",
    {"ShardId": str, "SequenceNumberRange": SequenceNumberRangeTypeDef, "ParentShardId": str},
    total=False,
)

StreamDescriptionTypeDef = TypedDict(
    "StreamDescriptionTypeDef",
    {
        "StreamArn": str,
        "StreamLabel": str,
        "StreamStatus": Literal["ENABLING", "ENABLED", "DISABLING", "DISABLED"],
        "StreamViewType": Literal["NEW_IMAGE", "OLD_IMAGE", "NEW_AND_OLD_IMAGES", "KEYS_ONLY"],
        "CreationRequestDateTime": datetime,
        "TableName": str,
        "KeySchema": List[KeySchemaElementTypeDef],
        "Shards": List[ShardTypeDef],
        "LastEvaluatedShardId": str,
    },
    total=False,
)

DescribeStreamOutputTypeDef = TypedDict(
    "DescribeStreamOutputTypeDef", {"StreamDescription": StreamDescriptionTypeDef}, total=False
)

IdentityTypeDef = TypedDict("IdentityTypeDef", {"PrincipalId": str, "Type": str}, total=False)

AttributeValueTypeDef = TypedDict(
    "AttributeValueTypeDef",
    {
        "S": str,
        "N": str,
        "B": Union[bytes, IO],
        "SS": List[str],
        "NS": List[str],
        "BS": List[Union[bytes, IO]],
        "M": Dict[str, "AttributeValueTypeDef"],
        "L": List["AttributeValueTypeDef"],
        "NULL": bool,
        "BOOL": bool,
    },
    total=False,
)

StreamRecordTypeDef = TypedDict(
    "StreamRecordTypeDef",
    {
        "ApproximateCreationDateTime": datetime,
        "Keys": Dict[str, AttributeValueTypeDef],
        "NewImage": Dict[str, AttributeValueTypeDef],
        "OldImage": Dict[str, AttributeValueTypeDef],
        "SequenceNumber": str,
        "SizeBytes": int,
        "StreamViewType": Literal["NEW_IMAGE", "OLD_IMAGE", "NEW_AND_OLD_IMAGES", "KEYS_ONLY"],
    },
    total=False,
)

RecordTypeDef = TypedDict(
    "RecordTypeDef",
    {
        "eventID": str,
        "eventName": Literal["INSERT", "MODIFY", "REMOVE"],
        "eventVersion": str,
        "eventSource": str,
        "awsRegion": str,
        "dynamodb": StreamRecordTypeDef,
        "userIdentity": IdentityTypeDef,
    },
    total=False,
)

GetRecordsOutputTypeDef = TypedDict(
    "GetRecordsOutputTypeDef",
    {"Records": List[RecordTypeDef], "NextShardIterator": str},
    total=False,
)

GetShardIteratorOutputTypeDef = TypedDict(
    "GetShardIteratorOutputTypeDef", {"ShardIterator": str}, total=False
)

StreamTypeDef = TypedDict(
    "StreamTypeDef", {"StreamArn": str, "TableName": str, "StreamLabel": str}, total=False
)

ListStreamsOutputTypeDef = TypedDict(
    "ListStreamsOutputTypeDef",
    {"Streams": List[StreamTypeDef], "LastEvaluatedStreamArn": str},
    total=False,
)
