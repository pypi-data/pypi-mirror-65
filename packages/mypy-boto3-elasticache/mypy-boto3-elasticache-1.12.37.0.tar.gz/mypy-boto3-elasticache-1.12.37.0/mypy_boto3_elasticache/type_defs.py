"""
Main interface for elasticache service type definitions.

Usage::

    from mypy_boto3.elasticache.type_defs import AllowedNodeTypeModificationsMessageTypeDef

    data: AllowedNodeTypeModificationsMessageTypeDef = {...}
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
    "AllowedNodeTypeModificationsMessageTypeDef",
    "EC2SecurityGroupTypeDef",
    "CacheSecurityGroupTypeDef",
    "AuthorizeCacheSecurityGroupIngressResultTypeDef",
    "EndpointTypeDef",
    "CacheNodeTypeDef",
    "CacheParameterGroupStatusTypeDef",
    "CacheSecurityGroupMembershipTypeDef",
    "NotificationConfigurationTypeDef",
    "PendingModifiedValuesTypeDef",
    "SecurityGroupMembershipTypeDef",
    "CacheClusterTypeDef",
    "CacheClusterMessageTypeDef",
    "CacheEngineVersionTypeDef",
    "CacheEngineVersionMessageTypeDef",
    "CacheNodeTypeSpecificValueTypeDef",
    "CacheNodeTypeSpecificParameterTypeDef",
    "ParameterTypeDef",
    "CacheParameterGroupDetailsTypeDef",
    "CacheParameterGroupNameMessageTypeDef",
    "CacheParameterGroupTypeDef",
    "CacheParameterGroupsMessageTypeDef",
    "CacheSecurityGroupMessageTypeDef",
    "AvailabilityZoneTypeDef",
    "SubnetTypeDef",
    "CacheSubnetGroupTypeDef",
    "CacheSubnetGroupMessageTypeDef",
    "GlobalReplicationGroupInfoTypeDef",
    "NodeGroupMemberTypeDef",
    "NodeGroupTypeDef",
    "SlotMigrationTypeDef",
    "ReshardingStatusTypeDef",
    "ReplicationGroupPendingModifiedValuesTypeDef",
    "ReplicationGroupTypeDef",
    "CompleteMigrationResponseTypeDef",
    "ConfigureShardTypeDef",
    "NodeGroupConfigurationTypeDef",
    "NodeSnapshotTypeDef",
    "SnapshotTypeDef",
    "CopySnapshotResultTypeDef",
    "CreateCacheClusterResultTypeDef",
    "CreateCacheParameterGroupResultTypeDef",
    "CreateCacheSecurityGroupResultTypeDef",
    "CreateCacheSubnetGroupResultTypeDef",
    "GlobalNodeGroupTypeDef",
    "GlobalReplicationGroupMemberTypeDef",
    "GlobalReplicationGroupTypeDef",
    "CreateGlobalReplicationGroupResultTypeDef",
    "CreateReplicationGroupResultTypeDef",
    "CreateSnapshotResultTypeDef",
    "CustomerNodeEndpointTypeDef",
    "DecreaseNodeGroupsInGlobalReplicationGroupResultTypeDef",
    "DecreaseReplicaCountResultTypeDef",
    "DeleteCacheClusterResultTypeDef",
    "DeleteGlobalReplicationGroupResultTypeDef",
    "DeleteReplicationGroupResultTypeDef",
    "DeleteSnapshotResultTypeDef",
    "EngineDefaultsTypeDef",
    "DescribeEngineDefaultParametersResultTypeDef",
    "DescribeGlobalReplicationGroupsResultTypeDef",
    "DescribeSnapshotsListMessageTypeDef",
    "DisassociateGlobalReplicationGroupResultTypeDef",
    "EventTypeDef",
    "EventsMessageTypeDef",
    "FailoverGlobalReplicationGroupResultTypeDef",
    "IncreaseNodeGroupsInGlobalReplicationGroupResultTypeDef",
    "IncreaseReplicaCountResultTypeDef",
    "ModifyCacheClusterResultTypeDef",
    "ModifyCacheSubnetGroupResultTypeDef",
    "ModifyGlobalReplicationGroupResultTypeDef",
    "ModifyReplicationGroupResultTypeDef",
    "ModifyReplicationGroupShardConfigurationResultTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterNameValueTypeDef",
    "RecurringChargeTypeDef",
    "ReservedCacheNodeTypeDef",
    "PurchaseReservedCacheNodesOfferingResultTypeDef",
    "RebalanceSlotsInGlobalReplicationGroupResultTypeDef",
    "RebootCacheClusterResultTypeDef",
    "ReshardingConfigurationTypeDef",
    "RegionalConfigurationTypeDef",
    "ReplicationGroupMessageTypeDef",
    "ReservedCacheNodeMessageTypeDef",
    "ReservedCacheNodesOfferingTypeDef",
    "ReservedCacheNodesOfferingMessageTypeDef",
    "RevokeCacheSecurityGroupIngressResultTypeDef",
    "ServiceUpdateTypeDef",
    "ServiceUpdatesMessageTypeDef",
    "StartMigrationResponseTypeDef",
    "TagTypeDef",
    "TagListMessageTypeDef",
    "TestFailoverResultTypeDef",
    "TimeRangeFilterTypeDef",
    "ProcessedUpdateActionTypeDef",
    "UnprocessedUpdateActionTypeDef",
    "UpdateActionResultsMessageTypeDef",
    "CacheNodeUpdateStatusTypeDef",
    "NodeGroupMemberUpdateStatusTypeDef",
    "NodeGroupUpdateStatusTypeDef",
    "UpdateActionTypeDef",
    "UpdateActionsMessageTypeDef",
    "WaiterConfigTypeDef",
)

AllowedNodeTypeModificationsMessageTypeDef = TypedDict(
    "AllowedNodeTypeModificationsMessageTypeDef",
    {"ScaleUpModifications": List[str], "ScaleDownModifications": List[str]},
    total=False,
)

EC2SecurityGroupTypeDef = TypedDict(
    "EC2SecurityGroupTypeDef",
    {"Status": str, "EC2SecurityGroupName": str, "EC2SecurityGroupOwnerId": str},
    total=False,
)

CacheSecurityGroupTypeDef = TypedDict(
    "CacheSecurityGroupTypeDef",
    {
        "OwnerId": str,
        "CacheSecurityGroupName": str,
        "Description": str,
        "EC2SecurityGroups": List[EC2SecurityGroupTypeDef],
    },
    total=False,
)

AuthorizeCacheSecurityGroupIngressResultTypeDef = TypedDict(
    "AuthorizeCacheSecurityGroupIngressResultTypeDef",
    {"CacheSecurityGroup": CacheSecurityGroupTypeDef},
    total=False,
)

EndpointTypeDef = TypedDict("EndpointTypeDef", {"Address": str, "Port": int}, total=False)

CacheNodeTypeDef = TypedDict(
    "CacheNodeTypeDef",
    {
        "CacheNodeId": str,
        "CacheNodeStatus": str,
        "CacheNodeCreateTime": datetime,
        "Endpoint": EndpointTypeDef,
        "ParameterGroupStatus": str,
        "SourceCacheNodeId": str,
        "CustomerAvailabilityZone": str,
    },
    total=False,
)

CacheParameterGroupStatusTypeDef = TypedDict(
    "CacheParameterGroupStatusTypeDef",
    {
        "CacheParameterGroupName": str,
        "ParameterApplyStatus": str,
        "CacheNodeIdsToReboot": List[str],
    },
    total=False,
)

CacheSecurityGroupMembershipTypeDef = TypedDict(
    "CacheSecurityGroupMembershipTypeDef",
    {"CacheSecurityGroupName": str, "Status": str},
    total=False,
)

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef", {"TopicArn": str, "TopicStatus": str}, total=False
)

PendingModifiedValuesTypeDef = TypedDict(
    "PendingModifiedValuesTypeDef",
    {
        "NumCacheNodes": int,
        "CacheNodeIdsToRemove": List[str],
        "EngineVersion": str,
        "CacheNodeType": str,
        "AuthTokenStatus": Literal["SETTING", "ROTATING"],
    },
    total=False,
)

SecurityGroupMembershipTypeDef = TypedDict(
    "SecurityGroupMembershipTypeDef", {"SecurityGroupId": str, "Status": str}, total=False
)

CacheClusterTypeDef = TypedDict(
    "CacheClusterTypeDef",
    {
        "CacheClusterId": str,
        "ConfigurationEndpoint": EndpointTypeDef,
        "ClientDownloadLandingPage": str,
        "CacheNodeType": str,
        "Engine": str,
        "EngineVersion": str,
        "CacheClusterStatus": str,
        "NumCacheNodes": int,
        "PreferredAvailabilityZone": str,
        "CacheClusterCreateTime": datetime,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": PendingModifiedValuesTypeDef,
        "NotificationConfiguration": NotificationConfigurationTypeDef,
        "CacheSecurityGroups": List[CacheSecurityGroupMembershipTypeDef],
        "CacheParameterGroup": CacheParameterGroupStatusTypeDef,
        "CacheSubnetGroupName": str,
        "CacheNodes": List[CacheNodeTypeDef],
        "AutoMinorVersionUpgrade": bool,
        "SecurityGroups": List[SecurityGroupMembershipTypeDef],
        "ReplicationGroupId": str,
        "SnapshotRetentionLimit": int,
        "SnapshotWindow": str,
        "AuthTokenEnabled": bool,
        "AuthTokenLastModifiedDate": datetime,
        "TransitEncryptionEnabled": bool,
        "AtRestEncryptionEnabled": bool,
    },
    total=False,
)

CacheClusterMessageTypeDef = TypedDict(
    "CacheClusterMessageTypeDef",
    {"Marker": str, "CacheClusters": List[CacheClusterTypeDef]},
    total=False,
)

CacheEngineVersionTypeDef = TypedDict(
    "CacheEngineVersionTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "CacheParameterGroupFamily": str,
        "CacheEngineDescription": str,
        "CacheEngineVersionDescription": str,
    },
    total=False,
)

CacheEngineVersionMessageTypeDef = TypedDict(
    "CacheEngineVersionMessageTypeDef",
    {"Marker": str, "CacheEngineVersions": List[CacheEngineVersionTypeDef]},
    total=False,
)

CacheNodeTypeSpecificValueTypeDef = TypedDict(
    "CacheNodeTypeSpecificValueTypeDef", {"CacheNodeType": str, "Value": str}, total=False
)

CacheNodeTypeSpecificParameterTypeDef = TypedDict(
    "CacheNodeTypeSpecificParameterTypeDef",
    {
        "ParameterName": str,
        "Description": str,
        "Source": str,
        "DataType": str,
        "AllowedValues": str,
        "IsModifiable": bool,
        "MinimumEngineVersion": str,
        "CacheNodeTypeSpecificValues": List[CacheNodeTypeSpecificValueTypeDef],
        "ChangeType": Literal["immediate", "requires-reboot"],
    },
    total=False,
)

ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "ParameterName": str,
        "ParameterValue": str,
        "Description": str,
        "Source": str,
        "DataType": str,
        "AllowedValues": str,
        "IsModifiable": bool,
        "MinimumEngineVersion": str,
        "ChangeType": Literal["immediate", "requires-reboot"],
    },
    total=False,
)

CacheParameterGroupDetailsTypeDef = TypedDict(
    "CacheParameterGroupDetailsTypeDef",
    {
        "Marker": str,
        "Parameters": List[ParameterTypeDef],
        "CacheNodeTypeSpecificParameters": List[CacheNodeTypeSpecificParameterTypeDef],
    },
    total=False,
)

CacheParameterGroupNameMessageTypeDef = TypedDict(
    "CacheParameterGroupNameMessageTypeDef", {"CacheParameterGroupName": str}, total=False
)

CacheParameterGroupTypeDef = TypedDict(
    "CacheParameterGroupTypeDef",
    {
        "CacheParameterGroupName": str,
        "CacheParameterGroupFamily": str,
        "Description": str,
        "IsGlobal": bool,
    },
    total=False,
)

CacheParameterGroupsMessageTypeDef = TypedDict(
    "CacheParameterGroupsMessageTypeDef",
    {"Marker": str, "CacheParameterGroups": List[CacheParameterGroupTypeDef]},
    total=False,
)

CacheSecurityGroupMessageTypeDef = TypedDict(
    "CacheSecurityGroupMessageTypeDef",
    {"Marker": str, "CacheSecurityGroups": List[CacheSecurityGroupTypeDef]},
    total=False,
)

AvailabilityZoneTypeDef = TypedDict("AvailabilityZoneTypeDef", {"Name": str}, total=False)

SubnetTypeDef = TypedDict(
    "SubnetTypeDef",
    {"SubnetIdentifier": str, "SubnetAvailabilityZone": AvailabilityZoneTypeDef},
    total=False,
)

CacheSubnetGroupTypeDef = TypedDict(
    "CacheSubnetGroupTypeDef",
    {
        "CacheSubnetGroupName": str,
        "CacheSubnetGroupDescription": str,
        "VpcId": str,
        "Subnets": List[SubnetTypeDef],
    },
    total=False,
)

CacheSubnetGroupMessageTypeDef = TypedDict(
    "CacheSubnetGroupMessageTypeDef",
    {"Marker": str, "CacheSubnetGroups": List[CacheSubnetGroupTypeDef]},
    total=False,
)

GlobalReplicationGroupInfoTypeDef = TypedDict(
    "GlobalReplicationGroupInfoTypeDef",
    {"GlobalReplicationGroupId": str, "GlobalReplicationGroupMemberRole": str},
    total=False,
)

NodeGroupMemberTypeDef = TypedDict(
    "NodeGroupMemberTypeDef",
    {
        "CacheClusterId": str,
        "CacheNodeId": str,
        "ReadEndpoint": EndpointTypeDef,
        "PreferredAvailabilityZone": str,
        "CurrentRole": str,
    },
    total=False,
)

NodeGroupTypeDef = TypedDict(
    "NodeGroupTypeDef",
    {
        "NodeGroupId": str,
        "Status": str,
        "PrimaryEndpoint": EndpointTypeDef,
        "ReaderEndpoint": EndpointTypeDef,
        "Slots": str,
        "NodeGroupMembers": List[NodeGroupMemberTypeDef],
    },
    total=False,
)

SlotMigrationTypeDef = TypedDict("SlotMigrationTypeDef", {"ProgressPercentage": float}, total=False)

ReshardingStatusTypeDef = TypedDict(
    "ReshardingStatusTypeDef", {"SlotMigration": SlotMigrationTypeDef}, total=False
)

ReplicationGroupPendingModifiedValuesTypeDef = TypedDict(
    "ReplicationGroupPendingModifiedValuesTypeDef",
    {
        "PrimaryClusterId": str,
        "AutomaticFailoverStatus": Literal["enabled", "disabled"],
        "Resharding": ReshardingStatusTypeDef,
        "AuthTokenStatus": Literal["SETTING", "ROTATING"],
    },
    total=False,
)

ReplicationGroupTypeDef = TypedDict(
    "ReplicationGroupTypeDef",
    {
        "ReplicationGroupId": str,
        "Description": str,
        "GlobalReplicationGroupInfo": GlobalReplicationGroupInfoTypeDef,
        "Status": str,
        "PendingModifiedValues": ReplicationGroupPendingModifiedValuesTypeDef,
        "MemberClusters": List[str],
        "NodeGroups": List[NodeGroupTypeDef],
        "SnapshottingClusterId": str,
        "AutomaticFailover": Literal["enabled", "disabled", "enabling", "disabling"],
        "ConfigurationEndpoint": EndpointTypeDef,
        "SnapshotRetentionLimit": int,
        "SnapshotWindow": str,
        "ClusterEnabled": bool,
        "CacheNodeType": str,
        "AuthTokenEnabled": bool,
        "AuthTokenLastModifiedDate": datetime,
        "TransitEncryptionEnabled": bool,
        "AtRestEncryptionEnabled": bool,
        "KmsKeyId": str,
    },
    total=False,
)

CompleteMigrationResponseTypeDef = TypedDict(
    "CompleteMigrationResponseTypeDef", {"ReplicationGroup": ReplicationGroupTypeDef}, total=False
)

_RequiredConfigureShardTypeDef = TypedDict(
    "_RequiredConfigureShardTypeDef", {"NodeGroupId": str, "NewReplicaCount": int}
)
_OptionalConfigureShardTypeDef = TypedDict(
    "_OptionalConfigureShardTypeDef", {"PreferredAvailabilityZones": List[str]}, total=False
)


class ConfigureShardTypeDef(_RequiredConfigureShardTypeDef, _OptionalConfigureShardTypeDef):
    pass


NodeGroupConfigurationTypeDef = TypedDict(
    "NodeGroupConfigurationTypeDef",
    {
        "NodeGroupId": str,
        "Slots": str,
        "ReplicaCount": int,
        "PrimaryAvailabilityZone": str,
        "ReplicaAvailabilityZones": List[str],
    },
    total=False,
)

NodeSnapshotTypeDef = TypedDict(
    "NodeSnapshotTypeDef",
    {
        "CacheClusterId": str,
        "NodeGroupId": str,
        "CacheNodeId": str,
        "NodeGroupConfiguration": NodeGroupConfigurationTypeDef,
        "CacheSize": str,
        "CacheNodeCreateTime": datetime,
        "SnapshotCreateTime": datetime,
    },
    total=False,
)

SnapshotTypeDef = TypedDict(
    "SnapshotTypeDef",
    {
        "SnapshotName": str,
        "ReplicationGroupId": str,
        "ReplicationGroupDescription": str,
        "CacheClusterId": str,
        "SnapshotStatus": str,
        "SnapshotSource": str,
        "CacheNodeType": str,
        "Engine": str,
        "EngineVersion": str,
        "NumCacheNodes": int,
        "PreferredAvailabilityZone": str,
        "CacheClusterCreateTime": datetime,
        "PreferredMaintenanceWindow": str,
        "TopicArn": str,
        "Port": int,
        "CacheParameterGroupName": str,
        "CacheSubnetGroupName": str,
        "VpcId": str,
        "AutoMinorVersionUpgrade": bool,
        "SnapshotRetentionLimit": int,
        "SnapshotWindow": str,
        "NumNodeGroups": int,
        "AutomaticFailover": Literal["enabled", "disabled", "enabling", "disabling"],
        "NodeSnapshots": List[NodeSnapshotTypeDef],
        "KmsKeyId": str,
    },
    total=False,
)

CopySnapshotResultTypeDef = TypedDict(
    "CopySnapshotResultTypeDef", {"Snapshot": SnapshotTypeDef}, total=False
)

CreateCacheClusterResultTypeDef = TypedDict(
    "CreateCacheClusterResultTypeDef", {"CacheCluster": CacheClusterTypeDef}, total=False
)

CreateCacheParameterGroupResultTypeDef = TypedDict(
    "CreateCacheParameterGroupResultTypeDef",
    {"CacheParameterGroup": CacheParameterGroupTypeDef},
    total=False,
)

CreateCacheSecurityGroupResultTypeDef = TypedDict(
    "CreateCacheSecurityGroupResultTypeDef",
    {"CacheSecurityGroup": CacheSecurityGroupTypeDef},
    total=False,
)

CreateCacheSubnetGroupResultTypeDef = TypedDict(
    "CreateCacheSubnetGroupResultTypeDef",
    {"CacheSubnetGroup": CacheSubnetGroupTypeDef},
    total=False,
)

GlobalNodeGroupTypeDef = TypedDict(
    "GlobalNodeGroupTypeDef", {"GlobalNodeGroupId": str, "Slots": str}, total=False
)

GlobalReplicationGroupMemberTypeDef = TypedDict(
    "GlobalReplicationGroupMemberTypeDef",
    {
        "ReplicationGroupId": str,
        "ReplicationGroupRegion": str,
        "Role": str,
        "AutomaticFailover": Literal["enabled", "disabled", "enabling", "disabling"],
        "Status": str,
    },
    total=False,
)

GlobalReplicationGroupTypeDef = TypedDict(
    "GlobalReplicationGroupTypeDef",
    {
        "GlobalReplicationGroupId": str,
        "GlobalReplicationGroupDescription": str,
        "Status": str,
        "CacheNodeType": str,
        "Engine": str,
        "EngineVersion": str,
        "Members": List[GlobalReplicationGroupMemberTypeDef],
        "ClusterEnabled": bool,
        "GlobalNodeGroups": List[GlobalNodeGroupTypeDef],
        "AuthTokenEnabled": bool,
        "TransitEncryptionEnabled": bool,
        "AtRestEncryptionEnabled": bool,
    },
    total=False,
)

CreateGlobalReplicationGroupResultTypeDef = TypedDict(
    "CreateGlobalReplicationGroupResultTypeDef",
    {"GlobalReplicationGroup": GlobalReplicationGroupTypeDef},
    total=False,
)

CreateReplicationGroupResultTypeDef = TypedDict(
    "CreateReplicationGroupResultTypeDef",
    {"ReplicationGroup": ReplicationGroupTypeDef},
    total=False,
)

CreateSnapshotResultTypeDef = TypedDict(
    "CreateSnapshotResultTypeDef", {"Snapshot": SnapshotTypeDef}, total=False
)

CustomerNodeEndpointTypeDef = TypedDict(
    "CustomerNodeEndpointTypeDef", {"Address": str, "Port": int}, total=False
)

DecreaseNodeGroupsInGlobalReplicationGroupResultTypeDef = TypedDict(
    "DecreaseNodeGroupsInGlobalReplicationGroupResultTypeDef",
    {"GlobalReplicationGroup": GlobalReplicationGroupTypeDef},
    total=False,
)

DecreaseReplicaCountResultTypeDef = TypedDict(
    "DecreaseReplicaCountResultTypeDef", {"ReplicationGroup": ReplicationGroupTypeDef}, total=False
)

DeleteCacheClusterResultTypeDef = TypedDict(
    "DeleteCacheClusterResultTypeDef", {"CacheCluster": CacheClusterTypeDef}, total=False
)

DeleteGlobalReplicationGroupResultTypeDef = TypedDict(
    "DeleteGlobalReplicationGroupResultTypeDef",
    {"GlobalReplicationGroup": GlobalReplicationGroupTypeDef},
    total=False,
)

DeleteReplicationGroupResultTypeDef = TypedDict(
    "DeleteReplicationGroupResultTypeDef",
    {"ReplicationGroup": ReplicationGroupTypeDef},
    total=False,
)

DeleteSnapshotResultTypeDef = TypedDict(
    "DeleteSnapshotResultTypeDef", {"Snapshot": SnapshotTypeDef}, total=False
)

EngineDefaultsTypeDef = TypedDict(
    "EngineDefaultsTypeDef",
    {
        "CacheParameterGroupFamily": str,
        "Marker": str,
        "Parameters": List[ParameterTypeDef],
        "CacheNodeTypeSpecificParameters": List[CacheNodeTypeSpecificParameterTypeDef],
    },
    total=False,
)

DescribeEngineDefaultParametersResultTypeDef = TypedDict(
    "DescribeEngineDefaultParametersResultTypeDef",
    {"EngineDefaults": EngineDefaultsTypeDef},
    total=False,
)

DescribeGlobalReplicationGroupsResultTypeDef = TypedDict(
    "DescribeGlobalReplicationGroupsResultTypeDef",
    {"Marker": str, "GlobalReplicationGroups": List[GlobalReplicationGroupTypeDef]},
    total=False,
)

DescribeSnapshotsListMessageTypeDef = TypedDict(
    "DescribeSnapshotsListMessageTypeDef",
    {"Marker": str, "Snapshots": List[SnapshotTypeDef]},
    total=False,
)

DisassociateGlobalReplicationGroupResultTypeDef = TypedDict(
    "DisassociateGlobalReplicationGroupResultTypeDef",
    {"GlobalReplicationGroup": GlobalReplicationGroupTypeDef},
    total=False,
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": Literal[
            "cache-cluster",
            "cache-parameter-group",
            "cache-security-group",
            "cache-subnet-group",
            "replication-group",
        ],
        "Message": str,
        "Date": datetime,
    },
    total=False,
)

EventsMessageTypeDef = TypedDict(
    "EventsMessageTypeDef", {"Marker": str, "Events": List[EventTypeDef]}, total=False
)

FailoverGlobalReplicationGroupResultTypeDef = TypedDict(
    "FailoverGlobalReplicationGroupResultTypeDef",
    {"GlobalReplicationGroup": GlobalReplicationGroupTypeDef},
    total=False,
)

IncreaseNodeGroupsInGlobalReplicationGroupResultTypeDef = TypedDict(
    "IncreaseNodeGroupsInGlobalReplicationGroupResultTypeDef",
    {"GlobalReplicationGroup": GlobalReplicationGroupTypeDef},
    total=False,
)

IncreaseReplicaCountResultTypeDef = TypedDict(
    "IncreaseReplicaCountResultTypeDef", {"ReplicationGroup": ReplicationGroupTypeDef}, total=False
)

ModifyCacheClusterResultTypeDef = TypedDict(
    "ModifyCacheClusterResultTypeDef", {"CacheCluster": CacheClusterTypeDef}, total=False
)

ModifyCacheSubnetGroupResultTypeDef = TypedDict(
    "ModifyCacheSubnetGroupResultTypeDef",
    {"CacheSubnetGroup": CacheSubnetGroupTypeDef},
    total=False,
)

ModifyGlobalReplicationGroupResultTypeDef = TypedDict(
    "ModifyGlobalReplicationGroupResultTypeDef",
    {"GlobalReplicationGroup": GlobalReplicationGroupTypeDef},
    total=False,
)

ModifyReplicationGroupResultTypeDef = TypedDict(
    "ModifyReplicationGroupResultTypeDef",
    {"ReplicationGroup": ReplicationGroupTypeDef},
    total=False,
)

ModifyReplicationGroupShardConfigurationResultTypeDef = TypedDict(
    "ModifyReplicationGroupShardConfigurationResultTypeDef",
    {"ReplicationGroup": ReplicationGroupTypeDef},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

ParameterNameValueTypeDef = TypedDict(
    "ParameterNameValueTypeDef", {"ParameterName": str, "ParameterValue": str}, total=False
)

RecurringChargeTypeDef = TypedDict(
    "RecurringChargeTypeDef",
    {"RecurringChargeAmount": float, "RecurringChargeFrequency": str},
    total=False,
)

ReservedCacheNodeTypeDef = TypedDict(
    "ReservedCacheNodeTypeDef",
    {
        "ReservedCacheNodeId": str,
        "ReservedCacheNodesOfferingId": str,
        "CacheNodeType": str,
        "StartTime": datetime,
        "Duration": int,
        "FixedPrice": float,
        "UsagePrice": float,
        "CacheNodeCount": int,
        "ProductDescription": str,
        "OfferingType": str,
        "State": str,
        "RecurringCharges": List[RecurringChargeTypeDef],
        "ReservationARN": str,
    },
    total=False,
)

PurchaseReservedCacheNodesOfferingResultTypeDef = TypedDict(
    "PurchaseReservedCacheNodesOfferingResultTypeDef",
    {"ReservedCacheNode": ReservedCacheNodeTypeDef},
    total=False,
)

RebalanceSlotsInGlobalReplicationGroupResultTypeDef = TypedDict(
    "RebalanceSlotsInGlobalReplicationGroupResultTypeDef",
    {"GlobalReplicationGroup": GlobalReplicationGroupTypeDef},
    total=False,
)

RebootCacheClusterResultTypeDef = TypedDict(
    "RebootCacheClusterResultTypeDef", {"CacheCluster": CacheClusterTypeDef}, total=False
)

ReshardingConfigurationTypeDef = TypedDict(
    "ReshardingConfigurationTypeDef",
    {"NodeGroupId": str, "PreferredAvailabilityZones": List[str]},
    total=False,
)

RegionalConfigurationTypeDef = TypedDict(
    "RegionalConfigurationTypeDef",
    {
        "ReplicationGroupId": str,
        "ReplicationGroupRegion": str,
        "ReshardingConfiguration": List[ReshardingConfigurationTypeDef],
    },
)

ReplicationGroupMessageTypeDef = TypedDict(
    "ReplicationGroupMessageTypeDef",
    {"Marker": str, "ReplicationGroups": List[ReplicationGroupTypeDef]},
    total=False,
)

ReservedCacheNodeMessageTypeDef = TypedDict(
    "ReservedCacheNodeMessageTypeDef",
    {"Marker": str, "ReservedCacheNodes": List[ReservedCacheNodeTypeDef]},
    total=False,
)

ReservedCacheNodesOfferingTypeDef = TypedDict(
    "ReservedCacheNodesOfferingTypeDef",
    {
        "ReservedCacheNodesOfferingId": str,
        "CacheNodeType": str,
        "Duration": int,
        "FixedPrice": float,
        "UsagePrice": float,
        "ProductDescription": str,
        "OfferingType": str,
        "RecurringCharges": List[RecurringChargeTypeDef],
    },
    total=False,
)

ReservedCacheNodesOfferingMessageTypeDef = TypedDict(
    "ReservedCacheNodesOfferingMessageTypeDef",
    {"Marker": str, "ReservedCacheNodesOfferings": List[ReservedCacheNodesOfferingTypeDef]},
    total=False,
)

RevokeCacheSecurityGroupIngressResultTypeDef = TypedDict(
    "RevokeCacheSecurityGroupIngressResultTypeDef",
    {"CacheSecurityGroup": CacheSecurityGroupTypeDef},
    total=False,
)

ServiceUpdateTypeDef = TypedDict(
    "ServiceUpdateTypeDef",
    {
        "ServiceUpdateName": str,
        "ServiceUpdateReleaseDate": datetime,
        "ServiceUpdateEndDate": datetime,
        "ServiceUpdateSeverity": Literal["critical", "important", "medium", "low"],
        "ServiceUpdateRecommendedApplyByDate": datetime,
        "ServiceUpdateStatus": Literal["available", "cancelled", "expired"],
        "ServiceUpdateDescription": str,
        "ServiceUpdateType": Literal["security-update"],
        "Engine": str,
        "EngineVersion": str,
        "AutoUpdateAfterRecommendedApplyByDate": bool,
        "EstimatedUpdateTime": str,
    },
    total=False,
)

ServiceUpdatesMessageTypeDef = TypedDict(
    "ServiceUpdatesMessageTypeDef",
    {"Marker": str, "ServiceUpdates": List[ServiceUpdateTypeDef]},
    total=False,
)

StartMigrationResponseTypeDef = TypedDict(
    "StartMigrationResponseTypeDef", {"ReplicationGroup": ReplicationGroupTypeDef}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str}, total=False)

TagListMessageTypeDef = TypedDict(
    "TagListMessageTypeDef", {"TagList": List[TagTypeDef]}, total=False
)

TestFailoverResultTypeDef = TypedDict(
    "TestFailoverResultTypeDef", {"ReplicationGroup": ReplicationGroupTypeDef}, total=False
)

TimeRangeFilterTypeDef = TypedDict(
    "TimeRangeFilterTypeDef", {"StartTime": datetime, "EndTime": datetime}, total=False
)

ProcessedUpdateActionTypeDef = TypedDict(
    "ProcessedUpdateActionTypeDef",
    {
        "ReplicationGroupId": str,
        "CacheClusterId": str,
        "ServiceUpdateName": str,
        "UpdateActionStatus": Literal[
            "not-applied", "waiting-to-start", "in-progress", "stopping", "stopped", "complete"
        ],
    },
    total=False,
)

UnprocessedUpdateActionTypeDef = TypedDict(
    "UnprocessedUpdateActionTypeDef",
    {
        "ReplicationGroupId": str,
        "CacheClusterId": str,
        "ServiceUpdateName": str,
        "ErrorType": str,
        "ErrorMessage": str,
    },
    total=False,
)

UpdateActionResultsMessageTypeDef = TypedDict(
    "UpdateActionResultsMessageTypeDef",
    {
        "ProcessedUpdateActions": List[ProcessedUpdateActionTypeDef],
        "UnprocessedUpdateActions": List[UnprocessedUpdateActionTypeDef],
    },
    total=False,
)

CacheNodeUpdateStatusTypeDef = TypedDict(
    "CacheNodeUpdateStatusTypeDef",
    {
        "CacheNodeId": str,
        "NodeUpdateStatus": Literal[
            "not-applied", "waiting-to-start", "in-progress", "stopping", "stopped", "complete"
        ],
        "NodeDeletionDate": datetime,
        "NodeUpdateStartDate": datetime,
        "NodeUpdateEndDate": datetime,
        "NodeUpdateInitiatedBy": Literal["system", "customer"],
        "NodeUpdateInitiatedDate": datetime,
        "NodeUpdateStatusModifiedDate": datetime,
    },
    total=False,
)

NodeGroupMemberUpdateStatusTypeDef = TypedDict(
    "NodeGroupMemberUpdateStatusTypeDef",
    {
        "CacheClusterId": str,
        "CacheNodeId": str,
        "NodeUpdateStatus": Literal[
            "not-applied", "waiting-to-start", "in-progress", "stopping", "stopped", "complete"
        ],
        "NodeDeletionDate": datetime,
        "NodeUpdateStartDate": datetime,
        "NodeUpdateEndDate": datetime,
        "NodeUpdateInitiatedBy": Literal["system", "customer"],
        "NodeUpdateInitiatedDate": datetime,
        "NodeUpdateStatusModifiedDate": datetime,
    },
    total=False,
)

NodeGroupUpdateStatusTypeDef = TypedDict(
    "NodeGroupUpdateStatusTypeDef",
    {"NodeGroupId": str, "NodeGroupMemberUpdateStatus": List[NodeGroupMemberUpdateStatusTypeDef]},
    total=False,
)

UpdateActionTypeDef = TypedDict(
    "UpdateActionTypeDef",
    {
        "ReplicationGroupId": str,
        "CacheClusterId": str,
        "ServiceUpdateName": str,
        "ServiceUpdateReleaseDate": datetime,
        "ServiceUpdateSeverity": Literal["critical", "important", "medium", "low"],
        "ServiceUpdateStatus": Literal["available", "cancelled", "expired"],
        "ServiceUpdateRecommendedApplyByDate": datetime,
        "ServiceUpdateType": Literal["security-update"],
        "UpdateActionAvailableDate": datetime,
        "UpdateActionStatus": Literal[
            "not-applied", "waiting-to-start", "in-progress", "stopping", "stopped", "complete"
        ],
        "NodesUpdated": str,
        "UpdateActionStatusModifiedDate": datetime,
        "SlaMet": Literal["yes", "no", "n/a"],
        "NodeGroupUpdateStatus": List[NodeGroupUpdateStatusTypeDef],
        "CacheNodeUpdateStatus": List[CacheNodeUpdateStatusTypeDef],
        "EstimatedUpdateTime": str,
        "Engine": str,
    },
    total=False,
)

UpdateActionsMessageTypeDef = TypedDict(
    "UpdateActionsMessageTypeDef",
    {"Marker": str, "UpdateActions": List[UpdateActionTypeDef]},
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
