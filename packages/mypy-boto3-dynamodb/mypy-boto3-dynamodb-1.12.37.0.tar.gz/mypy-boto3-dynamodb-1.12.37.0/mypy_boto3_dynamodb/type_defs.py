"""
Main interface for dynamodb service type definitions.

Usage::

    from mypy_boto3.dynamodb.type_defs import AttributeDefinitionTypeDef

    data: AttributeDefinitionTypeDef = {...}
"""
from datetime import datetime
from decimal import Decimal
import sys
from typing import Any, Dict, List, Set, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AttributeDefinitionTypeDef",
    "AttributeValueUpdateTypeDef",
    "AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef",
    "AutoScalingPolicyUpdateTypeDef",
    "AutoScalingSettingsUpdateTypeDef",
    "CapacityTypeDef",
    "ConsumedCapacityTypeDef",
    "KeysAndAttributesTypeDef",
    "BatchGetItemOutputTypeDef",
    "ItemCollectionMetricsTypeDef",
    "DeleteRequestTypeDef",
    "PutRequestTypeDef",
    "WriteRequestTypeDef",
    "BatchWriteItemOutputTypeDef",
    "ConditionTypeDef",
    "BackupDetailsTypeDef",
    "CreateBackupOutputTypeDef",
    "ProvisionedThroughputOverrideTypeDef",
    "ReplicaGlobalSecondaryIndexDescriptionTypeDef",
    "ReplicaDescriptionTypeDef",
    "GlobalTableDescriptionTypeDef",
    "CreateGlobalTableOutputTypeDef",
    "ArchivalSummaryTypeDef",
    "BillingModeSummaryTypeDef",
    "KeySchemaElementTypeDef",
    "ProjectionTypeDef",
    "ProvisionedThroughputDescriptionTypeDef",
    "GlobalSecondaryIndexDescriptionTypeDef",
    "LocalSecondaryIndexDescriptionTypeDef",
    "RestoreSummaryTypeDef",
    "SSEDescriptionTypeDef",
    "StreamSpecificationTypeDef",
    "TableDescriptionTypeDef",
    "CreateTableOutputTypeDef",
    "ProvisionedThroughputTypeDef",
    "SourceTableDetailsTypeDef",
    "GlobalSecondaryIndexInfoTypeDef",
    "LocalSecondaryIndexInfoTypeDef",
    "TimeToLiveDescriptionTypeDef",
    "SourceTableFeatureDetailsTypeDef",
    "BackupDescriptionTypeDef",
    "DeleteBackupOutputTypeDef",
    "DeleteItemOutputTypeDef",
    "DeleteTableOutputTypeDef",
    "DescribeBackupOutputTypeDef",
    "PointInTimeRecoveryDescriptionTypeDef",
    "ContinuousBackupsDescriptionTypeDef",
    "DescribeContinuousBackupsOutputTypeDef",
    "FailureExceptionTypeDef",
    "DescribeContributorInsightsOutputTypeDef",
    "EndpointTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "DescribeGlobalTableOutputTypeDef",
    "AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef",
    "AutoScalingPolicyDescriptionTypeDef",
    "AutoScalingSettingsDescriptionTypeDef",
    "ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef",
    "ReplicaSettingsDescriptionTypeDef",
    "DescribeGlobalTableSettingsOutputTypeDef",
    "DescribeLimitsOutputTypeDef",
    "DescribeTableOutputTypeDef",
    "ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef",
    "ReplicaAutoScalingDescriptionTypeDef",
    "TableAutoScalingDescriptionTypeDef",
    "DescribeTableReplicaAutoScalingOutputTypeDef",
    "DescribeTimeToLiveOutputTypeDef",
    "ExpectedAttributeValueTypeDef",
    "GetItemOutputTypeDef",
    "GlobalSecondaryIndexAutoScalingUpdateTypeDef",
    "GlobalSecondaryIndexTypeDef",
    "CreateGlobalSecondaryIndexActionTypeDef",
    "DeleteGlobalSecondaryIndexActionTypeDef",
    "UpdateGlobalSecondaryIndexActionTypeDef",
    "GlobalSecondaryIndexUpdateTypeDef",
    "GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef",
    "BackupSummaryTypeDef",
    "ListBackupsOutputTypeDef",
    "ContributorInsightsSummaryTypeDef",
    "ListContributorInsightsOutputTypeDef",
    "ReplicaTypeDef",
    "GlobalTableTypeDef",
    "ListGlobalTablesOutputTypeDef",
    "ListTablesOutputTypeDef",
    "TagTypeDef",
    "ListTagsOfResourceOutputTypeDef",
    "LocalSecondaryIndexTypeDef",
    "PaginatorConfigTypeDef",
    "PointInTimeRecoverySpecificationTypeDef",
    "PutItemOutputTypeDef",
    "QueryOutputTypeDef",
    "ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef",
    "ReplicaAutoScalingUpdateTypeDef",
    "ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef",
    "ReplicaSettingsUpdateTypeDef",
    "CreateReplicaActionTypeDef",
    "DeleteReplicaActionTypeDef",
    "ReplicaUpdateTypeDef",
    "ReplicaGlobalSecondaryIndexTypeDef",
    "CreateReplicationGroupMemberActionTypeDef",
    "DeleteReplicationGroupMemberActionTypeDef",
    "UpdateReplicationGroupMemberActionTypeDef",
    "ReplicationGroupUpdateTypeDef",
    "RestoreTableFromBackupOutputTypeDef",
    "RestoreTableToPointInTimeOutputTypeDef",
    "SSESpecificationTypeDef",
    "ScanOutputTypeDef",
    "TimeToLiveSpecificationTypeDef",
    "GetTypeDef",
    "TransactGetItemTypeDef",
    "ItemResponseTypeDef",
    "TransactGetItemsOutputTypeDef",
    "ConditionCheckTypeDef",
    "DeleteTypeDef",
    "PutTypeDef",
    "UpdateTypeDef",
    "TransactWriteItemTypeDef",
    "TransactWriteItemsOutputTypeDef",
    "UpdateContinuousBackupsOutputTypeDef",
    "UpdateContributorInsightsOutputTypeDef",
    "UpdateGlobalTableOutputTypeDef",
    "UpdateGlobalTableSettingsOutputTypeDef",
    "UpdateItemOutputTypeDef",
    "UpdateTableOutputTypeDef",
    "UpdateTableReplicaAutoScalingOutputTypeDef",
    "UpdateTimeToLiveOutputTypeDef",
    "WaiterConfigTypeDef",
)

AttributeDefinitionTypeDef = TypedDict(
    "AttributeDefinitionTypeDef", {"AttributeName": str, "AttributeType": Literal["S", "N", "B"]}
)

AttributeValueUpdateTypeDef = TypedDict(
    "AttributeValueUpdateTypeDef",
    {
        "Value": Union[
            bytes,
            bytearray,
            str,
            int,
            Decimal,
            bool,
            Set[int],
            Set[Decimal],
            Set[str],
            Set[bytes],
            Set[bytearray],
            List[Any],
            Dict[str, Any],
            None,
        ],
        "Action": Literal["ADD", "PUT", "DELETE"],
    },
    total=False,
)

_RequiredAutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef = TypedDict(
    "_RequiredAutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef",
    {"TargetValue": float},
)
_OptionalAutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef = TypedDict(
    "_OptionalAutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef",
    {"DisableScaleIn": bool, "ScaleInCooldown": int, "ScaleOutCooldown": int},
    total=False,
)


class AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef(
    _RequiredAutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef,
    _OptionalAutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef,
):
    pass


_RequiredAutoScalingPolicyUpdateTypeDef = TypedDict(
    "_RequiredAutoScalingPolicyUpdateTypeDef",
    {
        "TargetTrackingScalingPolicyConfiguration": AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef
    },
)
_OptionalAutoScalingPolicyUpdateTypeDef = TypedDict(
    "_OptionalAutoScalingPolicyUpdateTypeDef", {"PolicyName": str}, total=False
)


class AutoScalingPolicyUpdateTypeDef(
    _RequiredAutoScalingPolicyUpdateTypeDef, _OptionalAutoScalingPolicyUpdateTypeDef
):
    pass


AutoScalingSettingsUpdateTypeDef = TypedDict(
    "AutoScalingSettingsUpdateTypeDef",
    {
        "MinimumUnits": int,
        "MaximumUnits": int,
        "AutoScalingDisabled": bool,
        "AutoScalingRoleArn": str,
        "ScalingPolicyUpdate": AutoScalingPolicyUpdateTypeDef,
    },
    total=False,
)

CapacityTypeDef = TypedDict(
    "CapacityTypeDef",
    {"ReadCapacityUnits": float, "WriteCapacityUnits": float, "CapacityUnits": float},
    total=False,
)

ConsumedCapacityTypeDef = TypedDict(
    "ConsumedCapacityTypeDef",
    {
        "TableName": str,
        "CapacityUnits": float,
        "ReadCapacityUnits": float,
        "WriteCapacityUnits": float,
        "Table": CapacityTypeDef,
        "LocalSecondaryIndexes": Dict[str, CapacityTypeDef],
        "GlobalSecondaryIndexes": Dict[str, CapacityTypeDef],
    },
    total=False,
)

_RequiredKeysAndAttributesTypeDef = TypedDict(
    "_RequiredKeysAndAttributesTypeDef",
    {
        "Keys": List[
            Dict[
                str,
                Union[
                    bytes,
                    bytearray,
                    str,
                    int,
                    Decimal,
                    bool,
                    Set[int],
                    Set[Decimal],
                    Set[str],
                    Set[bytes],
                    Set[bytearray],
                    List[Any],
                    Dict[str, Any],
                    None,
                ],
            ]
        ]
    },
)
_OptionalKeysAndAttributesTypeDef = TypedDict(
    "_OptionalKeysAndAttributesTypeDef",
    {
        "AttributesToGet": List[str],
        "ConsistentRead": bool,
        "ProjectionExpression": str,
        "ExpressionAttributeNames": Dict[str, str],
    },
    total=False,
)


class KeysAndAttributesTypeDef(
    _RequiredKeysAndAttributesTypeDef, _OptionalKeysAndAttributesTypeDef
):
    pass


BatchGetItemOutputTypeDef = TypedDict(
    "BatchGetItemOutputTypeDef",
    {
        "Responses": Dict[
            str,
            List[
                Dict[
                    str,
                    Union[
                        bytes,
                        bytearray,
                        str,
                        int,
                        Decimal,
                        bool,
                        Set[int],
                        Set[Decimal],
                        Set[str],
                        Set[bytes],
                        Set[bytearray],
                        List[Any],
                        Dict[str, Any],
                        None,
                    ],
                ]
            ],
        ],
        "UnprocessedKeys": Dict[str, KeysAndAttributesTypeDef],
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
    },
    total=False,
)

ItemCollectionMetricsTypeDef = TypedDict(
    "ItemCollectionMetricsTypeDef",
    {
        "ItemCollectionKey": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "SizeEstimateRangeGB": List[float],
    },
    total=False,
)

DeleteRequestTypeDef = TypedDict(
    "DeleteRequestTypeDef",
    {
        "Key": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ]
    },
)

PutRequestTypeDef = TypedDict(
    "PutRequestTypeDef",
    {
        "Item": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ]
    },
)

WriteRequestTypeDef = TypedDict(
    "WriteRequestTypeDef",
    {"PutRequest": PutRequestTypeDef, "DeleteRequest": DeleteRequestTypeDef},
    total=False,
)

BatchWriteItemOutputTypeDef = TypedDict(
    "BatchWriteItemOutputTypeDef",
    {
        "UnprocessedItems": Dict[str, List[WriteRequestTypeDef]],
        "ItemCollectionMetrics": Dict[str, List[ItemCollectionMetricsTypeDef]],
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
    },
    total=False,
)

_RequiredConditionTypeDef = TypedDict(
    "_RequiredConditionTypeDef",
    {
        "ComparisonOperator": Literal[
            "EQ",
            "NE",
            "IN",
            "LE",
            "LT",
            "GE",
            "GT",
            "BETWEEN",
            "NOT_NULL",
            "NULL",
            "CONTAINS",
            "NOT_CONTAINS",
            "BEGINS_WITH",
        ]
    },
)
_OptionalConditionTypeDef = TypedDict(
    "_OptionalConditionTypeDef",
    {
        "AttributeValueList": List[
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ]
        ]
    },
    total=False,
)


class ConditionTypeDef(_RequiredConditionTypeDef, _OptionalConditionTypeDef):
    pass


_RequiredBackupDetailsTypeDef = TypedDict(
    "_RequiredBackupDetailsTypeDef",
    {
        "BackupArn": str,
        "BackupName": str,
        "BackupStatus": Literal["CREATING", "DELETED", "AVAILABLE"],
        "BackupType": Literal["USER", "SYSTEM", "AWS_BACKUP"],
        "BackupCreationDateTime": datetime,
    },
)
_OptionalBackupDetailsTypeDef = TypedDict(
    "_OptionalBackupDetailsTypeDef",
    {"BackupSizeBytes": int, "BackupExpiryDateTime": datetime},
    total=False,
)


class BackupDetailsTypeDef(_RequiredBackupDetailsTypeDef, _OptionalBackupDetailsTypeDef):
    pass


CreateBackupOutputTypeDef = TypedDict(
    "CreateBackupOutputTypeDef", {"BackupDetails": BackupDetailsTypeDef}, total=False
)

ProvisionedThroughputOverrideTypeDef = TypedDict(
    "ProvisionedThroughputOverrideTypeDef", {"ReadCapacityUnits": int}, total=False
)

ReplicaGlobalSecondaryIndexDescriptionTypeDef = TypedDict(
    "ReplicaGlobalSecondaryIndexDescriptionTypeDef",
    {"IndexName": str, "ProvisionedThroughputOverride": ProvisionedThroughputOverrideTypeDef},
    total=False,
)

ReplicaDescriptionTypeDef = TypedDict(
    "ReplicaDescriptionTypeDef",
    {
        "RegionName": str,
        "ReplicaStatus": Literal["CREATING", "CREATION_FAILED", "UPDATING", "DELETING", "ACTIVE"],
        "ReplicaStatusDescription": str,
        "ReplicaStatusPercentProgress": str,
        "KMSMasterKeyId": str,
        "ProvisionedThroughputOverride": ProvisionedThroughputOverrideTypeDef,
        "GlobalSecondaryIndexes": List[ReplicaGlobalSecondaryIndexDescriptionTypeDef],
    },
    total=False,
)

GlobalTableDescriptionTypeDef = TypedDict(
    "GlobalTableDescriptionTypeDef",
    {
        "ReplicationGroup": List[ReplicaDescriptionTypeDef],
        "GlobalTableArn": str,
        "CreationDateTime": datetime,
        "GlobalTableStatus": Literal["CREATING", "ACTIVE", "DELETING", "UPDATING"],
        "GlobalTableName": str,
    },
    total=False,
)

CreateGlobalTableOutputTypeDef = TypedDict(
    "CreateGlobalTableOutputTypeDef",
    {"GlobalTableDescription": GlobalTableDescriptionTypeDef},
    total=False,
)

ArchivalSummaryTypeDef = TypedDict(
    "ArchivalSummaryTypeDef",
    {"ArchivalDateTime": datetime, "ArchivalReason": str, "ArchivalBackupArn": str},
    total=False,
)

BillingModeSummaryTypeDef = TypedDict(
    "BillingModeSummaryTypeDef",
    {
        "BillingMode": Literal["PROVISIONED", "PAY_PER_REQUEST"],
        "LastUpdateToPayPerRequestDateTime": datetime,
    },
    total=False,
)

KeySchemaElementTypeDef = TypedDict(
    "KeySchemaElementTypeDef", {"AttributeName": str, "KeyType": Literal["HASH", "RANGE"]}
)

ProjectionTypeDef = TypedDict(
    "ProjectionTypeDef",
    {"ProjectionType": Literal["ALL", "KEYS_ONLY", "INCLUDE"], "NonKeyAttributes": List[str]},
    total=False,
)

ProvisionedThroughputDescriptionTypeDef = TypedDict(
    "ProvisionedThroughputDescriptionTypeDef",
    {
        "LastIncreaseDateTime": datetime,
        "LastDecreaseDateTime": datetime,
        "NumberOfDecreasesToday": int,
        "ReadCapacityUnits": int,
        "WriteCapacityUnits": int,
    },
    total=False,
)

GlobalSecondaryIndexDescriptionTypeDef = TypedDict(
    "GlobalSecondaryIndexDescriptionTypeDef",
    {
        "IndexName": str,
        "KeySchema": List[KeySchemaElementTypeDef],
        "Projection": ProjectionTypeDef,
        "IndexStatus": Literal["CREATING", "UPDATING", "DELETING", "ACTIVE"],
        "Backfilling": bool,
        "ProvisionedThroughput": ProvisionedThroughputDescriptionTypeDef,
        "IndexSizeBytes": int,
        "ItemCount": int,
        "IndexArn": str,
    },
    total=False,
)

LocalSecondaryIndexDescriptionTypeDef = TypedDict(
    "LocalSecondaryIndexDescriptionTypeDef",
    {
        "IndexName": str,
        "KeySchema": List[KeySchemaElementTypeDef],
        "Projection": ProjectionTypeDef,
        "IndexSizeBytes": int,
        "ItemCount": int,
        "IndexArn": str,
    },
    total=False,
)

_RequiredRestoreSummaryTypeDef = TypedDict(
    "_RequiredRestoreSummaryTypeDef", {"RestoreDateTime": datetime, "RestoreInProgress": bool}
)
_OptionalRestoreSummaryTypeDef = TypedDict(
    "_OptionalRestoreSummaryTypeDef", {"SourceBackupArn": str, "SourceTableArn": str}, total=False
)


class RestoreSummaryTypeDef(_RequiredRestoreSummaryTypeDef, _OptionalRestoreSummaryTypeDef):
    pass


SSEDescriptionTypeDef = TypedDict(
    "SSEDescriptionTypeDef",
    {
        "Status": Literal["ENABLING", "ENABLED", "DISABLING", "DISABLED", "UPDATING"],
        "SSEType": Literal["AES256", "KMS"],
        "KMSMasterKeyArn": str,
        "InaccessibleEncryptionDateTime": datetime,
    },
    total=False,
)

_RequiredStreamSpecificationTypeDef = TypedDict(
    "_RequiredStreamSpecificationTypeDef", {"StreamEnabled": bool}
)
_OptionalStreamSpecificationTypeDef = TypedDict(
    "_OptionalStreamSpecificationTypeDef",
    {"StreamViewType": Literal["NEW_IMAGE", "OLD_IMAGE", "NEW_AND_OLD_IMAGES", "KEYS_ONLY"]},
    total=False,
)


class StreamSpecificationTypeDef(
    _RequiredStreamSpecificationTypeDef, _OptionalStreamSpecificationTypeDef
):
    pass


TableDescriptionTypeDef = TypedDict(
    "TableDescriptionTypeDef",
    {
        "AttributeDefinitions": List[AttributeDefinitionTypeDef],
        "TableName": str,
        "KeySchema": List[KeySchemaElementTypeDef],
        "TableStatus": Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "ACTIVE",
            "INACCESSIBLE_ENCRYPTION_CREDENTIALS",
            "ARCHIVING",
            "ARCHIVED",
        ],
        "CreationDateTime": datetime,
        "ProvisionedThroughput": ProvisionedThroughputDescriptionTypeDef,
        "TableSizeBytes": int,
        "ItemCount": int,
        "TableArn": str,
        "TableId": str,
        "BillingModeSummary": BillingModeSummaryTypeDef,
        "LocalSecondaryIndexes": List[LocalSecondaryIndexDescriptionTypeDef],
        "GlobalSecondaryIndexes": List[GlobalSecondaryIndexDescriptionTypeDef],
        "StreamSpecification": StreamSpecificationTypeDef,
        "LatestStreamLabel": str,
        "LatestStreamArn": str,
        "GlobalTableVersion": str,
        "Replicas": List[ReplicaDescriptionTypeDef],
        "RestoreSummary": RestoreSummaryTypeDef,
        "SSEDescription": SSEDescriptionTypeDef,
        "ArchivalSummary": ArchivalSummaryTypeDef,
    },
    total=False,
)

CreateTableOutputTypeDef = TypedDict(
    "CreateTableOutputTypeDef", {"TableDescription": TableDescriptionTypeDef}, total=False
)

ProvisionedThroughputTypeDef = TypedDict(
    "ProvisionedThroughputTypeDef", {"ReadCapacityUnits": int, "WriteCapacityUnits": int}
)

_RequiredSourceTableDetailsTypeDef = TypedDict(
    "_RequiredSourceTableDetailsTypeDef",
    {
        "TableName": str,
        "TableId": str,
        "KeySchema": List[KeySchemaElementTypeDef],
        "TableCreationDateTime": datetime,
        "ProvisionedThroughput": ProvisionedThroughputTypeDef,
    },
)
_OptionalSourceTableDetailsTypeDef = TypedDict(
    "_OptionalSourceTableDetailsTypeDef",
    {
        "TableArn": str,
        "TableSizeBytes": int,
        "ItemCount": int,
        "BillingMode": Literal["PROVISIONED", "PAY_PER_REQUEST"],
    },
    total=False,
)


class SourceTableDetailsTypeDef(
    _RequiredSourceTableDetailsTypeDef, _OptionalSourceTableDetailsTypeDef
):
    pass


GlobalSecondaryIndexInfoTypeDef = TypedDict(
    "GlobalSecondaryIndexInfoTypeDef",
    {
        "IndexName": str,
        "KeySchema": List[KeySchemaElementTypeDef],
        "Projection": ProjectionTypeDef,
        "ProvisionedThroughput": ProvisionedThroughputTypeDef,
    },
    total=False,
)

LocalSecondaryIndexInfoTypeDef = TypedDict(
    "LocalSecondaryIndexInfoTypeDef",
    {"IndexName": str, "KeySchema": List[KeySchemaElementTypeDef], "Projection": ProjectionTypeDef},
    total=False,
)

TimeToLiveDescriptionTypeDef = TypedDict(
    "TimeToLiveDescriptionTypeDef",
    {
        "TimeToLiveStatus": Literal["ENABLING", "DISABLING", "ENABLED", "DISABLED"],
        "AttributeName": str,
    },
    total=False,
)

SourceTableFeatureDetailsTypeDef = TypedDict(
    "SourceTableFeatureDetailsTypeDef",
    {
        "LocalSecondaryIndexes": List[LocalSecondaryIndexInfoTypeDef],
        "GlobalSecondaryIndexes": List[GlobalSecondaryIndexInfoTypeDef],
        "StreamDescription": StreamSpecificationTypeDef,
        "TimeToLiveDescription": TimeToLiveDescriptionTypeDef,
        "SSEDescription": SSEDescriptionTypeDef,
    },
    total=False,
)

BackupDescriptionTypeDef = TypedDict(
    "BackupDescriptionTypeDef",
    {
        "BackupDetails": BackupDetailsTypeDef,
        "SourceTableDetails": SourceTableDetailsTypeDef,
        "SourceTableFeatureDetails": SourceTableFeatureDetailsTypeDef,
    },
    total=False,
)

DeleteBackupOutputTypeDef = TypedDict(
    "DeleteBackupOutputTypeDef", {"BackupDescription": BackupDescriptionTypeDef}, total=False
)

DeleteItemOutputTypeDef = TypedDict(
    "DeleteItemOutputTypeDef",
    {
        "Attributes": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ItemCollectionMetrics": ItemCollectionMetricsTypeDef,
    },
    total=False,
)

DeleteTableOutputTypeDef = TypedDict(
    "DeleteTableOutputTypeDef", {"TableDescription": TableDescriptionTypeDef}, total=False
)

DescribeBackupOutputTypeDef = TypedDict(
    "DescribeBackupOutputTypeDef", {"BackupDescription": BackupDescriptionTypeDef}, total=False
)

PointInTimeRecoveryDescriptionTypeDef = TypedDict(
    "PointInTimeRecoveryDescriptionTypeDef",
    {
        "PointInTimeRecoveryStatus": Literal["ENABLED", "DISABLED"],
        "EarliestRestorableDateTime": datetime,
        "LatestRestorableDateTime": datetime,
    },
    total=False,
)

_RequiredContinuousBackupsDescriptionTypeDef = TypedDict(
    "_RequiredContinuousBackupsDescriptionTypeDef",
    {"ContinuousBackupsStatus": Literal["ENABLED", "DISABLED"]},
)
_OptionalContinuousBackupsDescriptionTypeDef = TypedDict(
    "_OptionalContinuousBackupsDescriptionTypeDef",
    {"PointInTimeRecoveryDescription": PointInTimeRecoveryDescriptionTypeDef},
    total=False,
)


class ContinuousBackupsDescriptionTypeDef(
    _RequiredContinuousBackupsDescriptionTypeDef, _OptionalContinuousBackupsDescriptionTypeDef
):
    pass


DescribeContinuousBackupsOutputTypeDef = TypedDict(
    "DescribeContinuousBackupsOutputTypeDef",
    {"ContinuousBackupsDescription": ContinuousBackupsDescriptionTypeDef},
    total=False,
)

FailureExceptionTypeDef = TypedDict(
    "FailureExceptionTypeDef", {"ExceptionName": str, "ExceptionDescription": str}, total=False
)

DescribeContributorInsightsOutputTypeDef = TypedDict(
    "DescribeContributorInsightsOutputTypeDef",
    {
        "TableName": str,
        "IndexName": str,
        "ContributorInsightsRuleList": List[str],
        "ContributorInsightsStatus": Literal[
            "ENABLING", "ENABLED", "DISABLING", "DISABLED", "FAILED"
        ],
        "LastUpdateDateTime": datetime,
        "FailureException": FailureExceptionTypeDef,
    },
    total=False,
)

EndpointTypeDef = TypedDict("EndpointTypeDef", {"Address": str, "CachePeriodInMinutes": int})

DescribeEndpointsResponseTypeDef = TypedDict(
    "DescribeEndpointsResponseTypeDef", {"Endpoints": List[EndpointTypeDef]}
)

DescribeGlobalTableOutputTypeDef = TypedDict(
    "DescribeGlobalTableOutputTypeDef",
    {"GlobalTableDescription": GlobalTableDescriptionTypeDef},
    total=False,
)

_RequiredAutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef = TypedDict(
    "_RequiredAutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef",
    {"TargetValue": float},
)
_OptionalAutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef = TypedDict(
    "_OptionalAutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef",
    {"DisableScaleIn": bool, "ScaleInCooldown": int, "ScaleOutCooldown": int},
    total=False,
)


class AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef(
    _RequiredAutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef,
    _OptionalAutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef,
):
    pass


AutoScalingPolicyDescriptionTypeDef = TypedDict(
    "AutoScalingPolicyDescriptionTypeDef",
    {
        "PolicyName": str,
        "TargetTrackingScalingPolicyConfiguration": AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef,
    },
    total=False,
)

AutoScalingSettingsDescriptionTypeDef = TypedDict(
    "AutoScalingSettingsDescriptionTypeDef",
    {
        "MinimumUnits": int,
        "MaximumUnits": int,
        "AutoScalingDisabled": bool,
        "AutoScalingRoleArn": str,
        "ScalingPolicies": List[AutoScalingPolicyDescriptionTypeDef],
    },
    total=False,
)

_RequiredReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef = TypedDict(
    "_RequiredReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef", {"IndexName": str}
)
_OptionalReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef = TypedDict(
    "_OptionalReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef",
    {
        "IndexStatus": Literal["CREATING", "UPDATING", "DELETING", "ACTIVE"],
        "ProvisionedReadCapacityUnits": int,
        "ProvisionedReadCapacityAutoScalingSettings": AutoScalingSettingsDescriptionTypeDef,
        "ProvisionedWriteCapacityUnits": int,
        "ProvisionedWriteCapacityAutoScalingSettings": AutoScalingSettingsDescriptionTypeDef,
    },
    total=False,
)


class ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef(
    _RequiredReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef,
    _OptionalReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef,
):
    pass


_RequiredReplicaSettingsDescriptionTypeDef = TypedDict(
    "_RequiredReplicaSettingsDescriptionTypeDef", {"RegionName": str}
)
_OptionalReplicaSettingsDescriptionTypeDef = TypedDict(
    "_OptionalReplicaSettingsDescriptionTypeDef",
    {
        "ReplicaStatus": Literal["CREATING", "CREATION_FAILED", "UPDATING", "DELETING", "ACTIVE"],
        "ReplicaBillingModeSummary": BillingModeSummaryTypeDef,
        "ReplicaProvisionedReadCapacityUnits": int,
        "ReplicaProvisionedReadCapacityAutoScalingSettings": AutoScalingSettingsDescriptionTypeDef,
        "ReplicaProvisionedWriteCapacityUnits": int,
        "ReplicaProvisionedWriteCapacityAutoScalingSettings": AutoScalingSettingsDescriptionTypeDef,
        "ReplicaGlobalSecondaryIndexSettings": List[
            ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef
        ],
    },
    total=False,
)


class ReplicaSettingsDescriptionTypeDef(
    _RequiredReplicaSettingsDescriptionTypeDef, _OptionalReplicaSettingsDescriptionTypeDef
):
    pass


DescribeGlobalTableSettingsOutputTypeDef = TypedDict(
    "DescribeGlobalTableSettingsOutputTypeDef",
    {"GlobalTableName": str, "ReplicaSettings": List[ReplicaSettingsDescriptionTypeDef]},
    total=False,
)

DescribeLimitsOutputTypeDef = TypedDict(
    "DescribeLimitsOutputTypeDef",
    {
        "AccountMaxReadCapacityUnits": int,
        "AccountMaxWriteCapacityUnits": int,
        "TableMaxReadCapacityUnits": int,
        "TableMaxWriteCapacityUnits": int,
    },
    total=False,
)

DescribeTableOutputTypeDef = TypedDict(
    "DescribeTableOutputTypeDef", {"Table": TableDescriptionTypeDef}, total=False
)

ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef = TypedDict(
    "ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef",
    {
        "IndexName": str,
        "IndexStatus": Literal["CREATING", "UPDATING", "DELETING", "ACTIVE"],
        "ProvisionedReadCapacityAutoScalingSettings": AutoScalingSettingsDescriptionTypeDef,
        "ProvisionedWriteCapacityAutoScalingSettings": AutoScalingSettingsDescriptionTypeDef,
    },
    total=False,
)

ReplicaAutoScalingDescriptionTypeDef = TypedDict(
    "ReplicaAutoScalingDescriptionTypeDef",
    {
        "RegionName": str,
        "GlobalSecondaryIndexes": List[ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef],
        "ReplicaProvisionedReadCapacityAutoScalingSettings": AutoScalingSettingsDescriptionTypeDef,
        "ReplicaProvisionedWriteCapacityAutoScalingSettings": AutoScalingSettingsDescriptionTypeDef,
        "ReplicaStatus": Literal["CREATING", "CREATION_FAILED", "UPDATING", "DELETING", "ACTIVE"],
    },
    total=False,
)

TableAutoScalingDescriptionTypeDef = TypedDict(
    "TableAutoScalingDescriptionTypeDef",
    {
        "TableName": str,
        "TableStatus": Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "ACTIVE",
            "INACCESSIBLE_ENCRYPTION_CREDENTIALS",
            "ARCHIVING",
            "ARCHIVED",
        ],
        "Replicas": List[ReplicaAutoScalingDescriptionTypeDef],
    },
    total=False,
)

DescribeTableReplicaAutoScalingOutputTypeDef = TypedDict(
    "DescribeTableReplicaAutoScalingOutputTypeDef",
    {"TableAutoScalingDescription": TableAutoScalingDescriptionTypeDef},
    total=False,
)

DescribeTimeToLiveOutputTypeDef = TypedDict(
    "DescribeTimeToLiveOutputTypeDef",
    {"TimeToLiveDescription": TimeToLiveDescriptionTypeDef},
    total=False,
)

ExpectedAttributeValueTypeDef = TypedDict(
    "ExpectedAttributeValueTypeDef",
    {
        "Value": Union[
            bytes,
            bytearray,
            str,
            int,
            Decimal,
            bool,
            Set[int],
            Set[Decimal],
            Set[str],
            Set[bytes],
            Set[bytearray],
            List[Any],
            Dict[str, Any],
            None,
        ],
        "Exists": bool,
        "ComparisonOperator": Literal[
            "EQ",
            "NE",
            "IN",
            "LE",
            "LT",
            "GE",
            "GT",
            "BETWEEN",
            "NOT_NULL",
            "NULL",
            "CONTAINS",
            "NOT_CONTAINS",
            "BEGINS_WITH",
        ],
        "AttributeValueList": List[
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ]
        ],
    },
    total=False,
)

GetItemOutputTypeDef = TypedDict(
    "GetItemOutputTypeDef",
    {
        "Item": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
    },
    total=False,
)

GlobalSecondaryIndexAutoScalingUpdateTypeDef = TypedDict(
    "GlobalSecondaryIndexAutoScalingUpdateTypeDef",
    {
        "IndexName": str,
        "ProvisionedWriteCapacityAutoScalingUpdate": AutoScalingSettingsUpdateTypeDef,
    },
    total=False,
)

_RequiredGlobalSecondaryIndexTypeDef = TypedDict(
    "_RequiredGlobalSecondaryIndexTypeDef",
    {"IndexName": str, "KeySchema": List[KeySchemaElementTypeDef], "Projection": ProjectionTypeDef},
)
_OptionalGlobalSecondaryIndexTypeDef = TypedDict(
    "_OptionalGlobalSecondaryIndexTypeDef",
    {"ProvisionedThroughput": ProvisionedThroughputTypeDef},
    total=False,
)


class GlobalSecondaryIndexTypeDef(
    _RequiredGlobalSecondaryIndexTypeDef, _OptionalGlobalSecondaryIndexTypeDef
):
    pass


_RequiredCreateGlobalSecondaryIndexActionTypeDef = TypedDict(
    "_RequiredCreateGlobalSecondaryIndexActionTypeDef",
    {"IndexName": str, "KeySchema": List[KeySchemaElementTypeDef], "Projection": ProjectionTypeDef},
)
_OptionalCreateGlobalSecondaryIndexActionTypeDef = TypedDict(
    "_OptionalCreateGlobalSecondaryIndexActionTypeDef",
    {"ProvisionedThroughput": ProvisionedThroughputTypeDef},
    total=False,
)


class CreateGlobalSecondaryIndexActionTypeDef(
    _RequiredCreateGlobalSecondaryIndexActionTypeDef,
    _OptionalCreateGlobalSecondaryIndexActionTypeDef,
):
    pass


DeleteGlobalSecondaryIndexActionTypeDef = TypedDict(
    "DeleteGlobalSecondaryIndexActionTypeDef", {"IndexName": str}
)

UpdateGlobalSecondaryIndexActionTypeDef = TypedDict(
    "UpdateGlobalSecondaryIndexActionTypeDef",
    {"IndexName": str, "ProvisionedThroughput": ProvisionedThroughputTypeDef},
)

GlobalSecondaryIndexUpdateTypeDef = TypedDict(
    "GlobalSecondaryIndexUpdateTypeDef",
    {
        "Update": UpdateGlobalSecondaryIndexActionTypeDef,
        "Create": CreateGlobalSecondaryIndexActionTypeDef,
        "Delete": DeleteGlobalSecondaryIndexActionTypeDef,
    },
    total=False,
)

_RequiredGlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef = TypedDict(
    "_RequiredGlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef", {"IndexName": str}
)
_OptionalGlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef = TypedDict(
    "_OptionalGlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef",
    {
        "ProvisionedWriteCapacityUnits": int,
        "ProvisionedWriteCapacityAutoScalingSettingsUpdate": AutoScalingSettingsUpdateTypeDef,
    },
    total=False,
)


class GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef(
    _RequiredGlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef,
    _OptionalGlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef,
):
    pass


BackupSummaryTypeDef = TypedDict(
    "BackupSummaryTypeDef",
    {
        "TableName": str,
        "TableId": str,
        "TableArn": str,
        "BackupArn": str,
        "BackupName": str,
        "BackupCreationDateTime": datetime,
        "BackupExpiryDateTime": datetime,
        "BackupStatus": Literal["CREATING", "DELETED", "AVAILABLE"],
        "BackupType": Literal["USER", "SYSTEM", "AWS_BACKUP"],
        "BackupSizeBytes": int,
    },
    total=False,
)

ListBackupsOutputTypeDef = TypedDict(
    "ListBackupsOutputTypeDef",
    {"BackupSummaries": List[BackupSummaryTypeDef], "LastEvaluatedBackupArn": str},
    total=False,
)

ContributorInsightsSummaryTypeDef = TypedDict(
    "ContributorInsightsSummaryTypeDef",
    {
        "TableName": str,
        "IndexName": str,
        "ContributorInsightsStatus": Literal[
            "ENABLING", "ENABLED", "DISABLING", "DISABLED", "FAILED"
        ],
    },
    total=False,
)

ListContributorInsightsOutputTypeDef = TypedDict(
    "ListContributorInsightsOutputTypeDef",
    {"ContributorInsightsSummaries": List[ContributorInsightsSummaryTypeDef], "NextToken": str},
    total=False,
)

ReplicaTypeDef = TypedDict("ReplicaTypeDef", {"RegionName": str}, total=False)

GlobalTableTypeDef = TypedDict(
    "GlobalTableTypeDef",
    {"GlobalTableName": str, "ReplicationGroup": List[ReplicaTypeDef]},
    total=False,
)

ListGlobalTablesOutputTypeDef = TypedDict(
    "ListGlobalTablesOutputTypeDef",
    {"GlobalTables": List[GlobalTableTypeDef], "LastEvaluatedGlobalTableName": str},
    total=False,
)

ListTablesOutputTypeDef = TypedDict(
    "ListTablesOutputTypeDef", {"TableNames": List[str], "LastEvaluatedTableName": str}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ListTagsOfResourceOutputTypeDef = TypedDict(
    "ListTagsOfResourceOutputTypeDef", {"Tags": List[TagTypeDef], "NextToken": str}, total=False
)

LocalSecondaryIndexTypeDef = TypedDict(
    "LocalSecondaryIndexTypeDef",
    {"IndexName": str, "KeySchema": List[KeySchemaElementTypeDef], "Projection": ProjectionTypeDef},
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PointInTimeRecoverySpecificationTypeDef = TypedDict(
    "PointInTimeRecoverySpecificationTypeDef", {"PointInTimeRecoveryEnabled": bool}
)

PutItemOutputTypeDef = TypedDict(
    "PutItemOutputTypeDef",
    {
        "Attributes": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ItemCollectionMetrics": ItemCollectionMetricsTypeDef,
    },
    total=False,
)

QueryOutputTypeDef = TypedDict(
    "QueryOutputTypeDef",
    {
        "Items": List[
            Dict[
                str,
                Union[
                    bytes,
                    bytearray,
                    str,
                    int,
                    Decimal,
                    bool,
                    Set[int],
                    Set[Decimal],
                    Set[str],
                    Set[bytes],
                    Set[bytearray],
                    List[Any],
                    Dict[str, Any],
                    None,
                ],
            ]
        ],
        "Count": int,
        "ScannedCount": int,
        "LastEvaluatedKey": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
    },
    total=False,
)

ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef = TypedDict(
    "ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef",
    {
        "IndexName": str,
        "ProvisionedReadCapacityAutoScalingUpdate": AutoScalingSettingsUpdateTypeDef,
    },
    total=False,
)

_RequiredReplicaAutoScalingUpdateTypeDef = TypedDict(
    "_RequiredReplicaAutoScalingUpdateTypeDef", {"RegionName": str}
)
_OptionalReplicaAutoScalingUpdateTypeDef = TypedDict(
    "_OptionalReplicaAutoScalingUpdateTypeDef",
    {
        "ReplicaGlobalSecondaryIndexUpdates": List[
            ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef
        ],
        "ReplicaProvisionedReadCapacityAutoScalingUpdate": AutoScalingSettingsUpdateTypeDef,
    },
    total=False,
)


class ReplicaAutoScalingUpdateTypeDef(
    _RequiredReplicaAutoScalingUpdateTypeDef, _OptionalReplicaAutoScalingUpdateTypeDef
):
    pass


_RequiredReplicaGlobalSecondaryIndexSettingsUpdateTypeDef = TypedDict(
    "_RequiredReplicaGlobalSecondaryIndexSettingsUpdateTypeDef", {"IndexName": str}
)
_OptionalReplicaGlobalSecondaryIndexSettingsUpdateTypeDef = TypedDict(
    "_OptionalReplicaGlobalSecondaryIndexSettingsUpdateTypeDef",
    {
        "ProvisionedReadCapacityUnits": int,
        "ProvisionedReadCapacityAutoScalingSettingsUpdate": AutoScalingSettingsUpdateTypeDef,
    },
    total=False,
)


class ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef(
    _RequiredReplicaGlobalSecondaryIndexSettingsUpdateTypeDef,
    _OptionalReplicaGlobalSecondaryIndexSettingsUpdateTypeDef,
):
    pass


_RequiredReplicaSettingsUpdateTypeDef = TypedDict(
    "_RequiredReplicaSettingsUpdateTypeDef", {"RegionName": str}
)
_OptionalReplicaSettingsUpdateTypeDef = TypedDict(
    "_OptionalReplicaSettingsUpdateTypeDef",
    {
        "ReplicaProvisionedReadCapacityUnits": int,
        "ReplicaProvisionedReadCapacityAutoScalingSettingsUpdate": AutoScalingSettingsUpdateTypeDef,
        "ReplicaGlobalSecondaryIndexSettingsUpdate": List[
            ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef
        ],
    },
    total=False,
)


class ReplicaSettingsUpdateTypeDef(
    _RequiredReplicaSettingsUpdateTypeDef, _OptionalReplicaSettingsUpdateTypeDef
):
    pass


CreateReplicaActionTypeDef = TypedDict("CreateReplicaActionTypeDef", {"RegionName": str})

DeleteReplicaActionTypeDef = TypedDict("DeleteReplicaActionTypeDef", {"RegionName": str})

ReplicaUpdateTypeDef = TypedDict(
    "ReplicaUpdateTypeDef",
    {"Create": CreateReplicaActionTypeDef, "Delete": DeleteReplicaActionTypeDef},
    total=False,
)

_RequiredReplicaGlobalSecondaryIndexTypeDef = TypedDict(
    "_RequiredReplicaGlobalSecondaryIndexTypeDef", {"IndexName": str}
)
_OptionalReplicaGlobalSecondaryIndexTypeDef = TypedDict(
    "_OptionalReplicaGlobalSecondaryIndexTypeDef",
    {"ProvisionedThroughputOverride": ProvisionedThroughputOverrideTypeDef},
    total=False,
)


class ReplicaGlobalSecondaryIndexTypeDef(
    _RequiredReplicaGlobalSecondaryIndexTypeDef, _OptionalReplicaGlobalSecondaryIndexTypeDef
):
    pass


_RequiredCreateReplicationGroupMemberActionTypeDef = TypedDict(
    "_RequiredCreateReplicationGroupMemberActionTypeDef", {"RegionName": str}
)
_OptionalCreateReplicationGroupMemberActionTypeDef = TypedDict(
    "_OptionalCreateReplicationGroupMemberActionTypeDef",
    {
        "KMSMasterKeyId": str,
        "ProvisionedThroughputOverride": ProvisionedThroughputOverrideTypeDef,
        "GlobalSecondaryIndexes": List[ReplicaGlobalSecondaryIndexTypeDef],
    },
    total=False,
)


class CreateReplicationGroupMemberActionTypeDef(
    _RequiredCreateReplicationGroupMemberActionTypeDef,
    _OptionalCreateReplicationGroupMemberActionTypeDef,
):
    pass


DeleteReplicationGroupMemberActionTypeDef = TypedDict(
    "DeleteReplicationGroupMemberActionTypeDef", {"RegionName": str}
)

_RequiredUpdateReplicationGroupMemberActionTypeDef = TypedDict(
    "_RequiredUpdateReplicationGroupMemberActionTypeDef", {"RegionName": str}
)
_OptionalUpdateReplicationGroupMemberActionTypeDef = TypedDict(
    "_OptionalUpdateReplicationGroupMemberActionTypeDef",
    {
        "KMSMasterKeyId": str,
        "ProvisionedThroughputOverride": ProvisionedThroughputOverrideTypeDef,
        "GlobalSecondaryIndexes": List[ReplicaGlobalSecondaryIndexTypeDef],
    },
    total=False,
)


class UpdateReplicationGroupMemberActionTypeDef(
    _RequiredUpdateReplicationGroupMemberActionTypeDef,
    _OptionalUpdateReplicationGroupMemberActionTypeDef,
):
    pass


ReplicationGroupUpdateTypeDef = TypedDict(
    "ReplicationGroupUpdateTypeDef",
    {
        "Create": CreateReplicationGroupMemberActionTypeDef,
        "Update": UpdateReplicationGroupMemberActionTypeDef,
        "Delete": DeleteReplicationGroupMemberActionTypeDef,
    },
    total=False,
)

RestoreTableFromBackupOutputTypeDef = TypedDict(
    "RestoreTableFromBackupOutputTypeDef",
    {"TableDescription": TableDescriptionTypeDef},
    total=False,
)

RestoreTableToPointInTimeOutputTypeDef = TypedDict(
    "RestoreTableToPointInTimeOutputTypeDef",
    {"TableDescription": TableDescriptionTypeDef},
    total=False,
)

SSESpecificationTypeDef = TypedDict(
    "SSESpecificationTypeDef",
    {"Enabled": bool, "SSEType": Literal["AES256", "KMS"], "KMSMasterKeyId": str},
    total=False,
)

ScanOutputTypeDef = TypedDict(
    "ScanOutputTypeDef",
    {
        "Items": List[
            Dict[
                str,
                Union[
                    bytes,
                    bytearray,
                    str,
                    int,
                    Decimal,
                    bool,
                    Set[int],
                    Set[Decimal],
                    Set[str],
                    Set[bytes],
                    Set[bytearray],
                    List[Any],
                    Dict[str, Any],
                    None,
                ],
            ]
        ],
        "Count": int,
        "ScannedCount": int,
        "LastEvaluatedKey": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
    },
    total=False,
)

TimeToLiveSpecificationTypeDef = TypedDict(
    "TimeToLiveSpecificationTypeDef", {"Enabled": bool, "AttributeName": str}
)

_RequiredGetTypeDef = TypedDict(
    "_RequiredGetTypeDef",
    {
        "Key": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "TableName": str,
    },
)
_OptionalGetTypeDef = TypedDict(
    "_OptionalGetTypeDef",
    {"ProjectionExpression": str, "ExpressionAttributeNames": Dict[str, str]},
    total=False,
)


class GetTypeDef(_RequiredGetTypeDef, _OptionalGetTypeDef):
    pass


TransactGetItemTypeDef = TypedDict("TransactGetItemTypeDef", {"Get": GetTypeDef})

ItemResponseTypeDef = TypedDict(
    "ItemResponseTypeDef",
    {
        "Item": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ]
    },
    total=False,
)

TransactGetItemsOutputTypeDef = TypedDict(
    "TransactGetItemsOutputTypeDef",
    {"ConsumedCapacity": List[ConsumedCapacityTypeDef], "Responses": List[ItemResponseTypeDef]},
    total=False,
)

_RequiredConditionCheckTypeDef = TypedDict(
    "_RequiredConditionCheckTypeDef",
    {
        "Key": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "TableName": str,
        "ConditionExpression": str,
    },
)
_OptionalConditionCheckTypeDef = TypedDict(
    "_OptionalConditionCheckTypeDef",
    {
        "ExpressionAttributeNames": Dict[str, str],
        "ExpressionAttributeValues": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ReturnValuesOnConditionCheckFailure": Literal["ALL_OLD", "NONE"],
    },
    total=False,
)


class ConditionCheckTypeDef(_RequiredConditionCheckTypeDef, _OptionalConditionCheckTypeDef):
    pass


_RequiredDeleteTypeDef = TypedDict(
    "_RequiredDeleteTypeDef",
    {
        "Key": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "TableName": str,
    },
)
_OptionalDeleteTypeDef = TypedDict(
    "_OptionalDeleteTypeDef",
    {
        "ConditionExpression": str,
        "ExpressionAttributeNames": Dict[str, str],
        "ExpressionAttributeValues": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ReturnValuesOnConditionCheckFailure": Literal["ALL_OLD", "NONE"],
    },
    total=False,
)


class DeleteTypeDef(_RequiredDeleteTypeDef, _OptionalDeleteTypeDef):
    pass


_RequiredPutTypeDef = TypedDict(
    "_RequiredPutTypeDef",
    {
        "Item": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "TableName": str,
    },
)
_OptionalPutTypeDef = TypedDict(
    "_OptionalPutTypeDef",
    {
        "ConditionExpression": str,
        "ExpressionAttributeNames": Dict[str, str],
        "ExpressionAttributeValues": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ReturnValuesOnConditionCheckFailure": Literal["ALL_OLD", "NONE"],
    },
    total=False,
)


class PutTypeDef(_RequiredPutTypeDef, _OptionalPutTypeDef):
    pass


_RequiredUpdateTypeDef = TypedDict(
    "_RequiredUpdateTypeDef",
    {
        "Key": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "UpdateExpression": str,
        "TableName": str,
    },
)
_OptionalUpdateTypeDef = TypedDict(
    "_OptionalUpdateTypeDef",
    {
        "ConditionExpression": str,
        "ExpressionAttributeNames": Dict[str, str],
        "ExpressionAttributeValues": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ReturnValuesOnConditionCheckFailure": Literal["ALL_OLD", "NONE"],
    },
    total=False,
)


class UpdateTypeDef(_RequiredUpdateTypeDef, _OptionalUpdateTypeDef):
    pass


TransactWriteItemTypeDef = TypedDict(
    "TransactWriteItemTypeDef",
    {
        "ConditionCheck": ConditionCheckTypeDef,
        "Put": PutTypeDef,
        "Delete": DeleteTypeDef,
        "Update": UpdateTypeDef,
    },
    total=False,
)

TransactWriteItemsOutputTypeDef = TypedDict(
    "TransactWriteItemsOutputTypeDef",
    {
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
        "ItemCollectionMetrics": Dict[str, List[ItemCollectionMetricsTypeDef]],
    },
    total=False,
)

UpdateContinuousBackupsOutputTypeDef = TypedDict(
    "UpdateContinuousBackupsOutputTypeDef",
    {"ContinuousBackupsDescription": ContinuousBackupsDescriptionTypeDef},
    total=False,
)

UpdateContributorInsightsOutputTypeDef = TypedDict(
    "UpdateContributorInsightsOutputTypeDef",
    {
        "TableName": str,
        "IndexName": str,
        "ContributorInsightsStatus": Literal[
            "ENABLING", "ENABLED", "DISABLING", "DISABLED", "FAILED"
        ],
    },
    total=False,
)

UpdateGlobalTableOutputTypeDef = TypedDict(
    "UpdateGlobalTableOutputTypeDef",
    {"GlobalTableDescription": GlobalTableDescriptionTypeDef},
    total=False,
)

UpdateGlobalTableSettingsOutputTypeDef = TypedDict(
    "UpdateGlobalTableSettingsOutputTypeDef",
    {"GlobalTableName": str, "ReplicaSettings": List[ReplicaSettingsDescriptionTypeDef]},
    total=False,
)

UpdateItemOutputTypeDef = TypedDict(
    "UpdateItemOutputTypeDef",
    {
        "Attributes": Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ItemCollectionMetrics": ItemCollectionMetricsTypeDef,
    },
    total=False,
)

UpdateTableOutputTypeDef = TypedDict(
    "UpdateTableOutputTypeDef", {"TableDescription": TableDescriptionTypeDef}, total=False
)

UpdateTableReplicaAutoScalingOutputTypeDef = TypedDict(
    "UpdateTableReplicaAutoScalingOutputTypeDef",
    {"TableAutoScalingDescription": TableAutoScalingDescriptionTypeDef},
    total=False,
)

UpdateTimeToLiveOutputTypeDef = TypedDict(
    "UpdateTimeToLiveOutputTypeDef",
    {"TimeToLiveSpecification": TimeToLiveSpecificationTypeDef},
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
