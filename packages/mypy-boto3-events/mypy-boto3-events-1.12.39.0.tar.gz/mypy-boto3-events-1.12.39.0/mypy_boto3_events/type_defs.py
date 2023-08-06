"""
Main interface for events service type definitions.

Usage::

    from mypy_boto3.events.type_defs import ConditionTypeDef

    data: ConditionTypeDef = {...}
"""
from datetime import datetime
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
    "ConditionTypeDef",
    "CreateEventBusResponseTypeDef",
    "CreatePartnerEventSourceResponseTypeDef",
    "DescribeEventBusResponseTypeDef",
    "DescribeEventSourceResponseTypeDef",
    "DescribePartnerEventSourceResponseTypeDef",
    "DescribeRuleResponseTypeDef",
    "EventBusTypeDef",
    "ListEventBusesResponseTypeDef",
    "EventSourceTypeDef",
    "ListEventSourcesResponseTypeDef",
    "PartnerEventSourceAccountTypeDef",
    "ListPartnerEventSourceAccountsResponseTypeDef",
    "PartnerEventSourceTypeDef",
    "ListPartnerEventSourcesResponseTypeDef",
    "ListRuleNamesByTargetResponseTypeDef",
    "RuleTypeDef",
    "ListRulesResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "BatchArrayPropertiesTypeDef",
    "BatchRetryStrategyTypeDef",
    "BatchParametersTypeDef",
    "AwsVpcConfigurationTypeDef",
    "NetworkConfigurationTypeDef",
    "EcsParametersTypeDef",
    "InputTransformerTypeDef",
    "KinesisParametersTypeDef",
    "RunCommandTargetTypeDef",
    "RunCommandParametersTypeDef",
    "SqsParametersTypeDef",
    "TargetTypeDef",
    "ListTargetsByRuleResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutEventsRequestEntryTypeDef",
    "PutEventsResultEntryTypeDef",
    "PutEventsResponseTypeDef",
    "PutPartnerEventsRequestEntryTypeDef",
    "PutPartnerEventsResultEntryTypeDef",
    "PutPartnerEventsResponseTypeDef",
    "PutRuleResponseTypeDef",
    "PutTargetsResultEntryTypeDef",
    "PutTargetsResponseTypeDef",
    "RemoveTargetsResultEntryTypeDef",
    "RemoveTargetsResponseTypeDef",
    "TestEventPatternResponseTypeDef",
)

ConditionTypeDef = TypedDict("ConditionTypeDef", {"Type": str, "Key": str, "Value": str})

CreateEventBusResponseTypeDef = TypedDict(
    "CreateEventBusResponseTypeDef", {"EventBusArn": str}, total=False
)

CreatePartnerEventSourceResponseTypeDef = TypedDict(
    "CreatePartnerEventSourceResponseTypeDef", {"EventSourceArn": str}, total=False
)

DescribeEventBusResponseTypeDef = TypedDict(
    "DescribeEventBusResponseTypeDef", {"Name": str, "Arn": str, "Policy": str}, total=False
)

DescribeEventSourceResponseTypeDef = TypedDict(
    "DescribeEventSourceResponseTypeDef",
    {
        "Arn": str,
        "CreatedBy": str,
        "CreationTime": datetime,
        "ExpirationTime": datetime,
        "Name": str,
        "State": Literal["PENDING", "ACTIVE", "DELETED"],
    },
    total=False,
)

DescribePartnerEventSourceResponseTypeDef = TypedDict(
    "DescribePartnerEventSourceResponseTypeDef", {"Arn": str, "Name": str}, total=False
)

DescribeRuleResponseTypeDef = TypedDict(
    "DescribeRuleResponseTypeDef",
    {
        "Name": str,
        "Arn": str,
        "EventPattern": str,
        "ScheduleExpression": str,
        "State": Literal["ENABLED", "DISABLED"],
        "Description": str,
        "RoleArn": str,
        "ManagedBy": str,
        "EventBusName": str,
    },
    total=False,
)

EventBusTypeDef = TypedDict(
    "EventBusTypeDef", {"Name": str, "Arn": str, "Policy": str}, total=False
)

ListEventBusesResponseTypeDef = TypedDict(
    "ListEventBusesResponseTypeDef",
    {"EventBuses": List[EventBusTypeDef], "NextToken": str},
    total=False,
)

EventSourceTypeDef = TypedDict(
    "EventSourceTypeDef",
    {
        "Arn": str,
        "CreatedBy": str,
        "CreationTime": datetime,
        "ExpirationTime": datetime,
        "Name": str,
        "State": Literal["PENDING", "ACTIVE", "DELETED"],
    },
    total=False,
)

ListEventSourcesResponseTypeDef = TypedDict(
    "ListEventSourcesResponseTypeDef",
    {"EventSources": List[EventSourceTypeDef], "NextToken": str},
    total=False,
)

PartnerEventSourceAccountTypeDef = TypedDict(
    "PartnerEventSourceAccountTypeDef",
    {
        "Account": str,
        "CreationTime": datetime,
        "ExpirationTime": datetime,
        "State": Literal["PENDING", "ACTIVE", "DELETED"],
    },
    total=False,
)

ListPartnerEventSourceAccountsResponseTypeDef = TypedDict(
    "ListPartnerEventSourceAccountsResponseTypeDef",
    {"PartnerEventSourceAccounts": List[PartnerEventSourceAccountTypeDef], "NextToken": str},
    total=False,
)

PartnerEventSourceTypeDef = TypedDict(
    "PartnerEventSourceTypeDef", {"Arn": str, "Name": str}, total=False
)

ListPartnerEventSourcesResponseTypeDef = TypedDict(
    "ListPartnerEventSourcesResponseTypeDef",
    {"PartnerEventSources": List[PartnerEventSourceTypeDef], "NextToken": str},
    total=False,
)

ListRuleNamesByTargetResponseTypeDef = TypedDict(
    "ListRuleNamesByTargetResponseTypeDef", {"RuleNames": List[str], "NextToken": str}, total=False
)

RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "Name": str,
        "Arn": str,
        "EventPattern": str,
        "State": Literal["ENABLED", "DISABLED"],
        "Description": str,
        "ScheduleExpression": str,
        "RoleArn": str,
        "ManagedBy": str,
        "EventBusName": str,
    },
    total=False,
)

ListRulesResponseTypeDef = TypedDict(
    "ListRulesResponseTypeDef", {"Rules": List[RuleTypeDef], "NextToken": str}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef]}, total=False
)

BatchArrayPropertiesTypeDef = TypedDict("BatchArrayPropertiesTypeDef", {"Size": int}, total=False)

BatchRetryStrategyTypeDef = TypedDict("BatchRetryStrategyTypeDef", {"Attempts": int}, total=False)

_RequiredBatchParametersTypeDef = TypedDict(
    "_RequiredBatchParametersTypeDef", {"JobDefinition": str, "JobName": str}
)
_OptionalBatchParametersTypeDef = TypedDict(
    "_OptionalBatchParametersTypeDef",
    {"ArrayProperties": BatchArrayPropertiesTypeDef, "RetryStrategy": BatchRetryStrategyTypeDef},
    total=False,
)


class BatchParametersTypeDef(_RequiredBatchParametersTypeDef, _OptionalBatchParametersTypeDef):
    pass


_RequiredAwsVpcConfigurationTypeDef = TypedDict(
    "_RequiredAwsVpcConfigurationTypeDef", {"Subnets": List[str]}
)
_OptionalAwsVpcConfigurationTypeDef = TypedDict(
    "_OptionalAwsVpcConfigurationTypeDef",
    {"SecurityGroups": List[str], "AssignPublicIp": Literal["ENABLED", "DISABLED"]},
    total=False,
)


class AwsVpcConfigurationTypeDef(
    _RequiredAwsVpcConfigurationTypeDef, _OptionalAwsVpcConfigurationTypeDef
):
    pass


NetworkConfigurationTypeDef = TypedDict(
    "NetworkConfigurationTypeDef", {"awsvpcConfiguration": AwsVpcConfigurationTypeDef}, total=False
)

_RequiredEcsParametersTypeDef = TypedDict(
    "_RequiredEcsParametersTypeDef", {"TaskDefinitionArn": str}
)
_OptionalEcsParametersTypeDef = TypedDict(
    "_OptionalEcsParametersTypeDef",
    {
        "TaskCount": int,
        "LaunchType": Literal["EC2", "FARGATE"],
        "NetworkConfiguration": NetworkConfigurationTypeDef,
        "PlatformVersion": str,
        "Group": str,
    },
    total=False,
)


class EcsParametersTypeDef(_RequiredEcsParametersTypeDef, _OptionalEcsParametersTypeDef):
    pass


_RequiredInputTransformerTypeDef = TypedDict(
    "_RequiredInputTransformerTypeDef", {"InputTemplate": str}
)
_OptionalInputTransformerTypeDef = TypedDict(
    "_OptionalInputTransformerTypeDef", {"InputPathsMap": Dict[str, str]}, total=False
)


class InputTransformerTypeDef(_RequiredInputTransformerTypeDef, _OptionalInputTransformerTypeDef):
    pass


KinesisParametersTypeDef = TypedDict("KinesisParametersTypeDef", {"PartitionKeyPath": str})

RunCommandTargetTypeDef = TypedDict("RunCommandTargetTypeDef", {"Key": str, "Values": List[str]})

RunCommandParametersTypeDef = TypedDict(
    "RunCommandParametersTypeDef", {"RunCommandTargets": List[RunCommandTargetTypeDef]}
)

SqsParametersTypeDef = TypedDict("SqsParametersTypeDef", {"MessageGroupId": str}, total=False)

_RequiredTargetTypeDef = TypedDict("_RequiredTargetTypeDef", {"Id": str, "Arn": str})
_OptionalTargetTypeDef = TypedDict(
    "_OptionalTargetTypeDef",
    {
        "RoleArn": str,
        "Input": str,
        "InputPath": str,
        "InputTransformer": InputTransformerTypeDef,
        "KinesisParameters": KinesisParametersTypeDef,
        "RunCommandParameters": RunCommandParametersTypeDef,
        "EcsParameters": EcsParametersTypeDef,
        "BatchParameters": BatchParametersTypeDef,
        "SqsParameters": SqsParametersTypeDef,
    },
    total=False,
)


class TargetTypeDef(_RequiredTargetTypeDef, _OptionalTargetTypeDef):
    pass


ListTargetsByRuleResponseTypeDef = TypedDict(
    "ListTargetsByRuleResponseTypeDef",
    {"Targets": List[TargetTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutEventsRequestEntryTypeDef = TypedDict(
    "PutEventsRequestEntryTypeDef",
    {
        "Time": datetime,
        "Source": str,
        "Resources": List[str],
        "DetailType": str,
        "Detail": str,
        "EventBusName": str,
    },
    total=False,
)

PutEventsResultEntryTypeDef = TypedDict(
    "PutEventsResultEntryTypeDef",
    {"EventId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

PutEventsResponseTypeDef = TypedDict(
    "PutEventsResponseTypeDef",
    {"FailedEntryCount": int, "Entries": List[PutEventsResultEntryTypeDef]},
    total=False,
)

PutPartnerEventsRequestEntryTypeDef = TypedDict(
    "PutPartnerEventsRequestEntryTypeDef",
    {"Time": datetime, "Source": str, "Resources": List[str], "DetailType": str, "Detail": str},
    total=False,
)

PutPartnerEventsResultEntryTypeDef = TypedDict(
    "PutPartnerEventsResultEntryTypeDef",
    {"EventId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

PutPartnerEventsResponseTypeDef = TypedDict(
    "PutPartnerEventsResponseTypeDef",
    {"FailedEntryCount": int, "Entries": List[PutPartnerEventsResultEntryTypeDef]},
    total=False,
)

PutRuleResponseTypeDef = TypedDict("PutRuleResponseTypeDef", {"RuleArn": str}, total=False)

PutTargetsResultEntryTypeDef = TypedDict(
    "PutTargetsResultEntryTypeDef",
    {"TargetId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

PutTargetsResponseTypeDef = TypedDict(
    "PutTargetsResponseTypeDef",
    {"FailedEntryCount": int, "FailedEntries": List[PutTargetsResultEntryTypeDef]},
    total=False,
)

RemoveTargetsResultEntryTypeDef = TypedDict(
    "RemoveTargetsResultEntryTypeDef",
    {"TargetId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

RemoveTargetsResponseTypeDef = TypedDict(
    "RemoveTargetsResponseTypeDef",
    {"FailedEntryCount": int, "FailedEntries": List[RemoveTargetsResultEntryTypeDef]},
    total=False,
)

TestEventPatternResponseTypeDef = TypedDict(
    "TestEventPatternResponseTypeDef", {"Result": bool}, total=False
)
