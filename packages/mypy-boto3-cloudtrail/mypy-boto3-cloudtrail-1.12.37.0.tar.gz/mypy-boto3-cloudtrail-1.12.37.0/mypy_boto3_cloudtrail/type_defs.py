"""
Main interface for cloudtrail service type definitions.

Usage::

    from mypy_boto3.cloudtrail.type_defs import CreateTrailResponseTypeDef

    data: CreateTrailResponseTypeDef = {...}
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
    "CreateTrailResponseTypeDef",
    "TrailTypeDef",
    "DescribeTrailsResponseTypeDef",
    "DataResourceTypeDef",
    "EventSelectorTypeDef",
    "GetEventSelectorsResponseTypeDef",
    "InsightSelectorTypeDef",
    "GetInsightSelectorsResponseTypeDef",
    "GetTrailResponseTypeDef",
    "GetTrailStatusResponseTypeDef",
    "PublicKeyTypeDef",
    "ListPublicKeysResponseTypeDef",
    "TagTypeDef",
    "ResourceTagTypeDef",
    "ListTagsResponseTypeDef",
    "TrailInfoTypeDef",
    "ListTrailsResponseTypeDef",
    "LookupAttributeTypeDef",
    "ResourceTypeDef",
    "EventTypeDef",
    "LookupEventsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutEventSelectorsResponseTypeDef",
    "PutInsightSelectorsResponseTypeDef",
    "UpdateTrailResponseTypeDef",
)

CreateTrailResponseTypeDef = TypedDict(
    "CreateTrailResponseTypeDef",
    {
        "Name": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "SnsTopicName": str,
        "SnsTopicARN": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "TrailARN": str,
        "LogFileValidationEnabled": bool,
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "KmsKeyId": str,
        "IsOrganizationTrail": bool,
    },
    total=False,
)

TrailTypeDef = TypedDict(
    "TrailTypeDef",
    {
        "Name": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "SnsTopicName": str,
        "SnsTopicARN": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "HomeRegion": str,
        "TrailARN": str,
        "LogFileValidationEnabled": bool,
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "KmsKeyId": str,
        "HasCustomEventSelectors": bool,
        "HasInsightSelectors": bool,
        "IsOrganizationTrail": bool,
    },
    total=False,
)

DescribeTrailsResponseTypeDef = TypedDict(
    "DescribeTrailsResponseTypeDef", {"trailList": List[TrailTypeDef]}, total=False
)

DataResourceTypeDef = TypedDict(
    "DataResourceTypeDef", {"Type": str, "Values": List[str]}, total=False
)

EventSelectorTypeDef = TypedDict(
    "EventSelectorTypeDef",
    {
        "ReadWriteType": Literal["ReadOnly", "WriteOnly", "All"],
        "IncludeManagementEvents": bool,
        "DataResources": List[DataResourceTypeDef],
        "ExcludeManagementEventSources": List[str],
    },
    total=False,
)

GetEventSelectorsResponseTypeDef = TypedDict(
    "GetEventSelectorsResponseTypeDef",
    {"TrailARN": str, "EventSelectors": List[EventSelectorTypeDef]},
    total=False,
)

InsightSelectorTypeDef = TypedDict(
    "InsightSelectorTypeDef", {"InsightType": Literal["ApiCallRateInsight"]}, total=False
)

GetInsightSelectorsResponseTypeDef = TypedDict(
    "GetInsightSelectorsResponseTypeDef",
    {"TrailARN": str, "InsightSelectors": List[InsightSelectorTypeDef]},
    total=False,
)

GetTrailResponseTypeDef = TypedDict("GetTrailResponseTypeDef", {"Trail": TrailTypeDef}, total=False)

GetTrailStatusResponseTypeDef = TypedDict(
    "GetTrailStatusResponseTypeDef",
    {
        "IsLogging": bool,
        "LatestDeliveryError": str,
        "LatestNotificationError": str,
        "LatestDeliveryTime": datetime,
        "LatestNotificationTime": datetime,
        "StartLoggingTime": datetime,
        "StopLoggingTime": datetime,
        "LatestCloudWatchLogsDeliveryError": str,
        "LatestCloudWatchLogsDeliveryTime": datetime,
        "LatestDigestDeliveryTime": datetime,
        "LatestDigestDeliveryError": str,
        "LatestDeliveryAttemptTime": str,
        "LatestNotificationAttemptTime": str,
        "LatestNotificationAttemptSucceeded": str,
        "LatestDeliveryAttemptSucceeded": str,
        "TimeLoggingStarted": str,
        "TimeLoggingStopped": str,
    },
    total=False,
)

PublicKeyTypeDef = TypedDict(
    "PublicKeyTypeDef",
    {
        "Value": Union[bytes, IO],
        "ValidityStartTime": datetime,
        "ValidityEndTime": datetime,
        "Fingerprint": str,
    },
    total=False,
)

ListPublicKeysResponseTypeDef = TypedDict(
    "ListPublicKeysResponseTypeDef",
    {"PublicKeyList": List[PublicKeyTypeDef], "NextToken": str},
    total=False,
)

_RequiredTagTypeDef = TypedDict("_RequiredTagTypeDef", {"Key": str})
_OptionalTagTypeDef = TypedDict("_OptionalTagTypeDef", {"Value": str}, total=False)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


ResourceTagTypeDef = TypedDict(
    "ResourceTagTypeDef", {"ResourceId": str, "TagsList": List[TagTypeDef]}, total=False
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {"ResourceTagList": List[ResourceTagTypeDef], "NextToken": str},
    total=False,
)

TrailInfoTypeDef = TypedDict(
    "TrailInfoTypeDef", {"TrailARN": str, "Name": str, "HomeRegion": str}, total=False
)

ListTrailsResponseTypeDef = TypedDict(
    "ListTrailsResponseTypeDef", {"Trails": List[TrailInfoTypeDef], "NextToken": str}, total=False
)

LookupAttributeTypeDef = TypedDict(
    "LookupAttributeTypeDef",
    {
        "AttributeKey": Literal[
            "EventId",
            "EventName",
            "ReadOnly",
            "Username",
            "ResourceType",
            "ResourceName",
            "EventSource",
            "AccessKeyId",
        ],
        "AttributeValue": str,
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef", {"ResourceType": str, "ResourceName": str}, total=False
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "EventId": str,
        "EventName": str,
        "ReadOnly": str,
        "AccessKeyId": str,
        "EventTime": datetime,
        "EventSource": str,
        "Username": str,
        "Resources": List[ResourceTypeDef],
        "CloudTrailEvent": str,
    },
    total=False,
)

LookupEventsResponseTypeDef = TypedDict(
    "LookupEventsResponseTypeDef", {"Events": List[EventTypeDef], "NextToken": str}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutEventSelectorsResponseTypeDef = TypedDict(
    "PutEventSelectorsResponseTypeDef",
    {"TrailARN": str, "EventSelectors": List[EventSelectorTypeDef]},
    total=False,
)

PutInsightSelectorsResponseTypeDef = TypedDict(
    "PutInsightSelectorsResponseTypeDef",
    {"TrailARN": str, "InsightSelectors": List[InsightSelectorTypeDef]},
    total=False,
)

UpdateTrailResponseTypeDef = TypedDict(
    "UpdateTrailResponseTypeDef",
    {
        "Name": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "SnsTopicName": str,
        "SnsTopicARN": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "TrailARN": str,
        "LogFileValidationEnabled": bool,
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "KmsKeyId": str,
        "IsOrganizationTrail": bool,
    },
    total=False,
)
