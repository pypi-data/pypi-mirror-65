"""
Main interface for mq service type definitions.

Usage::

    from mypy_boto3.mq.type_defs import ConfigurationIdTypeDef

    data: ConfigurationIdTypeDef = {...}
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
    "ConfigurationIdTypeDef",
    "CreateBrokerResponseTypeDef",
    "ConfigurationRevisionTypeDef",
    "CreateConfigurationResponseTypeDef",
    "DeleteBrokerResponseTypeDef",
    "EngineVersionTypeDef",
    "BrokerEngineTypeTypeDef",
    "DescribeBrokerEngineTypesResponseTypeDef",
    "AvailabilityZoneTypeDef",
    "BrokerInstanceOptionTypeDef",
    "DescribeBrokerInstanceOptionsResponseTypeDef",
    "BrokerInstanceTypeDef",
    "ConfigurationsTypeDef",
    "EncryptionOptionsTypeDef",
    "PendingLogsTypeDef",
    "LogsSummaryTypeDef",
    "UserSummaryTypeDef",
    "WeeklyStartTimeTypeDef",
    "DescribeBrokerResponseTypeDef",
    "DescribeConfigurationResponseTypeDef",
    "DescribeConfigurationRevisionResponseTypeDef",
    "UserPendingChangesTypeDef",
    "DescribeUserResponseTypeDef",
    "BrokerSummaryTypeDef",
    "ListBrokersResponseTypeDef",
    "ListConfigurationRevisionsResponseTypeDef",
    "ConfigurationTypeDef",
    "ListConfigurationsResponseTypeDef",
    "ListTagsResponseTypeDef",
    "ListUsersResponseTypeDef",
    "LogsTypeDef",
    "PaginatorConfigTypeDef",
    "UpdateBrokerResponseTypeDef",
    "SanitizationWarningTypeDef",
    "UpdateConfigurationResponseTypeDef",
    "UserTypeDef",
)

ConfigurationIdTypeDef = TypedDict(
    "ConfigurationIdTypeDef", {"Id": str, "Revision": int}, total=False
)

CreateBrokerResponseTypeDef = TypedDict(
    "CreateBrokerResponseTypeDef", {"BrokerArn": str, "BrokerId": str}, total=False
)

ConfigurationRevisionTypeDef = TypedDict(
    "ConfigurationRevisionTypeDef",
    {"Created": datetime, "Description": str, "Revision": int},
    total=False,
)

CreateConfigurationResponseTypeDef = TypedDict(
    "CreateConfigurationResponseTypeDef",
    {
        "Arn": str,
        "Created": datetime,
        "Id": str,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
    },
    total=False,
)

DeleteBrokerResponseTypeDef = TypedDict(
    "DeleteBrokerResponseTypeDef", {"BrokerId": str}, total=False
)

EngineVersionTypeDef = TypedDict("EngineVersionTypeDef", {"Name": str}, total=False)

BrokerEngineTypeTypeDef = TypedDict(
    "BrokerEngineTypeTypeDef",
    {"EngineType": Literal["ACTIVEMQ"], "EngineVersions": List[EngineVersionTypeDef]},
    total=False,
)

DescribeBrokerEngineTypesResponseTypeDef = TypedDict(
    "DescribeBrokerEngineTypesResponseTypeDef",
    {"BrokerEngineTypes": List[BrokerEngineTypeTypeDef], "MaxResults": int, "NextToken": str},
    total=False,
)

AvailabilityZoneTypeDef = TypedDict("AvailabilityZoneTypeDef", {"Name": str}, total=False)

BrokerInstanceOptionTypeDef = TypedDict(
    "BrokerInstanceOptionTypeDef",
    {
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "EngineType": Literal["ACTIVEMQ"],
        "HostInstanceType": str,
        "StorageType": Literal["EBS", "EFS"],
        "SupportedDeploymentModes": List[Literal["SINGLE_INSTANCE", "ACTIVE_STANDBY_MULTI_AZ"]],
        "SupportedEngineVersions": List[str],
    },
    total=False,
)

DescribeBrokerInstanceOptionsResponseTypeDef = TypedDict(
    "DescribeBrokerInstanceOptionsResponseTypeDef",
    {
        "BrokerInstanceOptions": List[BrokerInstanceOptionTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

BrokerInstanceTypeDef = TypedDict(
    "BrokerInstanceTypeDef",
    {"ConsoleURL": str, "Endpoints": List[str], "IpAddress": str},
    total=False,
)

ConfigurationsTypeDef = TypedDict(
    "ConfigurationsTypeDef",
    {
        "Current": ConfigurationIdTypeDef,
        "History": List[ConfigurationIdTypeDef],
        "Pending": ConfigurationIdTypeDef,
    },
    total=False,
)

_RequiredEncryptionOptionsTypeDef = TypedDict(
    "_RequiredEncryptionOptionsTypeDef", {"UseAwsOwnedKey": bool}
)
_OptionalEncryptionOptionsTypeDef = TypedDict(
    "_OptionalEncryptionOptionsTypeDef", {"KmsKeyId": str}, total=False
)


class EncryptionOptionsTypeDef(
    _RequiredEncryptionOptionsTypeDef, _OptionalEncryptionOptionsTypeDef
):
    pass


PendingLogsTypeDef = TypedDict("PendingLogsTypeDef", {"Audit": bool, "General": bool}, total=False)

LogsSummaryTypeDef = TypedDict(
    "LogsSummaryTypeDef",
    {
        "Audit": bool,
        "AuditLogGroup": str,
        "General": bool,
        "GeneralLogGroup": str,
        "Pending": PendingLogsTypeDef,
    },
    total=False,
)

UserSummaryTypeDef = TypedDict(
    "UserSummaryTypeDef",
    {"PendingChange": Literal["CREATE", "UPDATE", "DELETE"], "Username": str},
    total=False,
)

WeeklyStartTimeTypeDef = TypedDict(
    "WeeklyStartTimeTypeDef",
    {
        "DayOfWeek": Literal[
            "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"
        ],
        "TimeOfDay": str,
        "TimeZone": str,
    },
    total=False,
)

DescribeBrokerResponseTypeDef = TypedDict(
    "DescribeBrokerResponseTypeDef",
    {
        "AutoMinorVersionUpgrade": bool,
        "BrokerArn": str,
        "BrokerId": str,
        "BrokerInstances": List[BrokerInstanceTypeDef],
        "BrokerName": str,
        "BrokerState": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_FAILED",
            "DELETION_IN_PROGRESS",
            "RUNNING",
            "REBOOT_IN_PROGRESS",
        ],
        "Configurations": ConfigurationsTypeDef,
        "Created": datetime,
        "DeploymentMode": Literal["SINGLE_INSTANCE", "ACTIVE_STANDBY_MULTI_AZ"],
        "EncryptionOptions": EncryptionOptionsTypeDef,
        "EngineType": Literal["ACTIVEMQ"],
        "EngineVersion": str,
        "HostInstanceType": str,
        "Logs": LogsSummaryTypeDef,
        "MaintenanceWindowStartTime": WeeklyStartTimeTypeDef,
        "PendingEngineVersion": str,
        "PendingHostInstanceType": str,
        "PendingSecurityGroups": List[str],
        "PubliclyAccessible": bool,
        "SecurityGroups": List[str],
        "StorageType": Literal["EBS", "EFS"],
        "SubnetIds": List[str],
        "Tags": Dict[str, str],
        "Users": List[UserSummaryTypeDef],
    },
    total=False,
)

DescribeConfigurationResponseTypeDef = TypedDict(
    "DescribeConfigurationResponseTypeDef",
    {
        "Arn": str,
        "Created": datetime,
        "Description": str,
        "EngineType": Literal["ACTIVEMQ"],
        "EngineVersion": str,
        "Id": str,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

DescribeConfigurationRevisionResponseTypeDef = TypedDict(
    "DescribeConfigurationRevisionResponseTypeDef",
    {"ConfigurationId": str, "Created": datetime, "Data": str, "Description": str},
    total=False,
)

UserPendingChangesTypeDef = TypedDict(
    "UserPendingChangesTypeDef",
    {
        "ConsoleAccess": bool,
        "Groups": List[str],
        "PendingChange": Literal["CREATE", "UPDATE", "DELETE"],
    },
    total=False,
)

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {
        "BrokerId": str,
        "ConsoleAccess": bool,
        "Groups": List[str],
        "Pending": UserPendingChangesTypeDef,
        "Username": str,
    },
    total=False,
)

BrokerSummaryTypeDef = TypedDict(
    "BrokerSummaryTypeDef",
    {
        "BrokerArn": str,
        "BrokerId": str,
        "BrokerName": str,
        "BrokerState": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_FAILED",
            "DELETION_IN_PROGRESS",
            "RUNNING",
            "REBOOT_IN_PROGRESS",
        ],
        "Created": datetime,
        "DeploymentMode": Literal["SINGLE_INSTANCE", "ACTIVE_STANDBY_MULTI_AZ"],
        "HostInstanceType": str,
    },
    total=False,
)

ListBrokersResponseTypeDef = TypedDict(
    "ListBrokersResponseTypeDef",
    {"BrokerSummaries": List[BrokerSummaryTypeDef], "NextToken": str},
    total=False,
)

ListConfigurationRevisionsResponseTypeDef = TypedDict(
    "ListConfigurationRevisionsResponseTypeDef",
    {
        "ConfigurationId": str,
        "MaxResults": int,
        "NextToken": str,
        "Revisions": List[ConfigurationRevisionTypeDef],
    },
    total=False,
)

ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "Arn": str,
        "Created": datetime,
        "Description": str,
        "EngineType": Literal["ACTIVEMQ"],
        "EngineVersion": str,
        "Id": str,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

ListConfigurationsResponseTypeDef = TypedDict(
    "ListConfigurationsResponseTypeDef",
    {"Configurations": List[ConfigurationTypeDef], "MaxResults": int, "NextToken": str},
    total=False,
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {"BrokerId": str, "MaxResults": int, "NextToken": str, "Users": List[UserSummaryTypeDef]},
    total=False,
)

LogsTypeDef = TypedDict("LogsTypeDef", {"Audit": bool, "General": bool}, total=False)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

UpdateBrokerResponseTypeDef = TypedDict(
    "UpdateBrokerResponseTypeDef",
    {
        "AutoMinorVersionUpgrade": bool,
        "BrokerId": str,
        "Configuration": ConfigurationIdTypeDef,
        "EngineVersion": str,
        "HostInstanceType": str,
        "Logs": LogsTypeDef,
        "SecurityGroups": List[str],
    },
    total=False,
)

SanitizationWarningTypeDef = TypedDict(
    "SanitizationWarningTypeDef",
    {
        "AttributeName": str,
        "ElementName": str,
        "Reason": Literal[
            "DISALLOWED_ELEMENT_REMOVED",
            "DISALLOWED_ATTRIBUTE_REMOVED",
            "INVALID_ATTRIBUTE_VALUE_REMOVED",
        ],
    },
    total=False,
)

UpdateConfigurationResponseTypeDef = TypedDict(
    "UpdateConfigurationResponseTypeDef",
    {
        "Arn": str,
        "Created": datetime,
        "Id": str,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
        "Warnings": List[SanitizationWarningTypeDef],
    },
    total=False,
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {"ConsoleAccess": bool, "Groups": List[str], "Password": str, "Username": str},
    total=False,
)
