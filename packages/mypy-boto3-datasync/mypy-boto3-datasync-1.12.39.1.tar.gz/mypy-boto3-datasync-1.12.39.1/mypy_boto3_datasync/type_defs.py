"""
Main interface for datasync service type definitions.

Usage::

    from mypy_boto3.datasync.type_defs import CreateAgentResponseTypeDef

    data: CreateAgentResponseTypeDef = {...}
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
    "CreateAgentResponseTypeDef",
    "CreateLocationEfsResponseTypeDef",
    "CreateLocationFsxWindowsResponseTypeDef",
    "CreateLocationNfsResponseTypeDef",
    "CreateLocationS3ResponseTypeDef",
    "CreateLocationSmbResponseTypeDef",
    "CreateTaskResponseTypeDef",
    "PrivateLinkConfigTypeDef",
    "DescribeAgentResponseTypeDef",
    "Ec2ConfigTypeDef",
    "DescribeLocationEfsResponseTypeDef",
    "DescribeLocationFsxWindowsResponseTypeDef",
    "NfsMountOptionsTypeDef",
    "OnPremConfigTypeDef",
    "DescribeLocationNfsResponseTypeDef",
    "S3ConfigTypeDef",
    "DescribeLocationS3ResponseTypeDef",
    "SmbMountOptionsTypeDef",
    "DescribeLocationSmbResponseTypeDef",
    "FilterRuleTypeDef",
    "OptionsTypeDef",
    "TaskExecutionResultDetailTypeDef",
    "DescribeTaskExecutionResponseTypeDef",
    "TaskScheduleTypeDef",
    "DescribeTaskResponseTypeDef",
    "AgentListEntryTypeDef",
    "ListAgentsResponseTypeDef",
    "LocationListEntryTypeDef",
    "ListLocationsResponseTypeDef",
    "TagListEntryTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TaskExecutionListEntryTypeDef",
    "ListTaskExecutionsResponseTypeDef",
    "TaskListEntryTypeDef",
    "ListTasksResponseTypeDef",
    "PaginatorConfigTypeDef",
    "StartTaskExecutionResponseTypeDef",
)

CreateAgentResponseTypeDef = TypedDict("CreateAgentResponseTypeDef", {"AgentArn": str}, total=False)

CreateLocationEfsResponseTypeDef = TypedDict(
    "CreateLocationEfsResponseTypeDef", {"LocationArn": str}, total=False
)

CreateLocationFsxWindowsResponseTypeDef = TypedDict(
    "CreateLocationFsxWindowsResponseTypeDef", {"LocationArn": str}, total=False
)

CreateLocationNfsResponseTypeDef = TypedDict(
    "CreateLocationNfsResponseTypeDef", {"LocationArn": str}, total=False
)

CreateLocationS3ResponseTypeDef = TypedDict(
    "CreateLocationS3ResponseTypeDef", {"LocationArn": str}, total=False
)

CreateLocationSmbResponseTypeDef = TypedDict(
    "CreateLocationSmbResponseTypeDef", {"LocationArn": str}, total=False
)

CreateTaskResponseTypeDef = TypedDict("CreateTaskResponseTypeDef", {"TaskArn": str}, total=False)

PrivateLinkConfigTypeDef = TypedDict(
    "PrivateLinkConfigTypeDef",
    {
        "VpcEndpointId": str,
        "PrivateLinkEndpoint": str,
        "SubnetArns": List[str],
        "SecurityGroupArns": List[str],
    },
    total=False,
)

DescribeAgentResponseTypeDef = TypedDict(
    "DescribeAgentResponseTypeDef",
    {
        "AgentArn": str,
        "Name": str,
        "Status": Literal["ONLINE", "OFFLINE"],
        "LastConnectionTime": datetime,
        "CreationTime": datetime,
        "EndpointType": Literal["PUBLIC", "PRIVATE_LINK", "FIPS"],
        "PrivateLinkConfig": PrivateLinkConfigTypeDef,
    },
    total=False,
)

Ec2ConfigTypeDef = TypedDict("Ec2ConfigTypeDef", {"SubnetArn": str, "SecurityGroupArns": List[str]})

DescribeLocationEfsResponseTypeDef = TypedDict(
    "DescribeLocationEfsResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "Ec2Config": Ec2ConfigTypeDef,
        "CreationTime": datetime,
    },
    total=False,
)

DescribeLocationFsxWindowsResponseTypeDef = TypedDict(
    "DescribeLocationFsxWindowsResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "SecurityGroupArns": List[str],
        "CreationTime": datetime,
        "User": str,
        "Domain": str,
    },
    total=False,
)

NfsMountOptionsTypeDef = TypedDict(
    "NfsMountOptionsTypeDef",
    {"Version": Literal["AUTOMATIC", "NFS3", "NFS4_0", "NFS4_1"]},
    total=False,
)

OnPremConfigTypeDef = TypedDict("OnPremConfigTypeDef", {"AgentArns": List[str]})

DescribeLocationNfsResponseTypeDef = TypedDict(
    "DescribeLocationNfsResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "OnPremConfig": OnPremConfigTypeDef,
        "MountOptions": NfsMountOptionsTypeDef,
        "CreationTime": datetime,
    },
    total=False,
)

S3ConfigTypeDef = TypedDict("S3ConfigTypeDef", {"BucketAccessRoleArn": str})

DescribeLocationS3ResponseTypeDef = TypedDict(
    "DescribeLocationS3ResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "S3StorageClass": Literal[
            "STANDARD",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ],
        "S3Config": S3ConfigTypeDef,
        "CreationTime": datetime,
    },
    total=False,
)

SmbMountOptionsTypeDef = TypedDict(
    "SmbMountOptionsTypeDef", {"Version": Literal["AUTOMATIC", "SMB2", "SMB3"]}, total=False
)

DescribeLocationSmbResponseTypeDef = TypedDict(
    "DescribeLocationSmbResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "AgentArns": List[str],
        "User": str,
        "Domain": str,
        "MountOptions": SmbMountOptionsTypeDef,
        "CreationTime": datetime,
    },
    total=False,
)

FilterRuleTypeDef = TypedDict(
    "FilterRuleTypeDef", {"FilterType": Literal["SIMPLE_PATTERN"], "Value": str}, total=False
)

OptionsTypeDef = TypedDict(
    "OptionsTypeDef",
    {
        "VerifyMode": Literal["POINT_IN_TIME_CONSISTENT", "ONLY_FILES_TRANSFERRED", "NONE"],
        "OverwriteMode": Literal["ALWAYS", "NEVER"],
        "Atime": Literal["NONE", "BEST_EFFORT"],
        "Mtime": Literal["NONE", "PRESERVE"],
        "Uid": Literal["NONE", "INT_VALUE", "NAME", "BOTH"],
        "Gid": Literal["NONE", "INT_VALUE", "NAME", "BOTH"],
        "PreserveDeletedFiles": Literal["PRESERVE", "REMOVE"],
        "PreserveDevices": Literal["NONE", "PRESERVE"],
        "PosixPermissions": Literal["NONE", "PRESERVE"],
        "BytesPerSecond": int,
        "TaskQueueing": Literal["ENABLED", "DISABLED"],
        "LogLevel": Literal["OFF", "BASIC", "TRANSFER"],
    },
    total=False,
)

TaskExecutionResultDetailTypeDef = TypedDict(
    "TaskExecutionResultDetailTypeDef",
    {
        "PrepareDuration": int,
        "PrepareStatus": Literal["PENDING", "SUCCESS", "ERROR"],
        "TotalDuration": int,
        "TransferDuration": int,
        "TransferStatus": Literal["PENDING", "SUCCESS", "ERROR"],
        "VerifyDuration": int,
        "VerifyStatus": Literal["PENDING", "SUCCESS", "ERROR"],
        "ErrorCode": str,
        "ErrorDetail": str,
    },
    total=False,
)

DescribeTaskExecutionResponseTypeDef = TypedDict(
    "DescribeTaskExecutionResponseTypeDef",
    {
        "TaskExecutionArn": str,
        "Status": Literal[
            "QUEUED", "LAUNCHING", "PREPARING", "TRANSFERRING", "VERIFYING", "SUCCESS", "ERROR"
        ],
        "Options": OptionsTypeDef,
        "Excludes": List[FilterRuleTypeDef],
        "Includes": List[FilterRuleTypeDef],
        "StartTime": datetime,
        "EstimatedFilesToTransfer": int,
        "EstimatedBytesToTransfer": int,
        "FilesTransferred": int,
        "BytesWritten": int,
        "BytesTransferred": int,
        "Result": TaskExecutionResultDetailTypeDef,
    },
    total=False,
)

TaskScheduleTypeDef = TypedDict("TaskScheduleTypeDef", {"ScheduleExpression": str})

DescribeTaskResponseTypeDef = TypedDict(
    "DescribeTaskResponseTypeDef",
    {
        "TaskArn": str,
        "Status": Literal["AVAILABLE", "CREATING", "QUEUED", "RUNNING", "UNAVAILABLE"],
        "Name": str,
        "CurrentTaskExecutionArn": str,
        "SourceLocationArn": str,
        "DestinationLocationArn": str,
        "CloudWatchLogGroupArn": str,
        "SourceNetworkInterfaceArns": List[str],
        "DestinationNetworkInterfaceArns": List[str],
        "Options": OptionsTypeDef,
        "Excludes": List[FilterRuleTypeDef],
        "Schedule": TaskScheduleTypeDef,
        "ErrorCode": str,
        "ErrorDetail": str,
        "CreationTime": datetime,
    },
    total=False,
)

AgentListEntryTypeDef = TypedDict(
    "AgentListEntryTypeDef",
    {"AgentArn": str, "Name": str, "Status": Literal["ONLINE", "OFFLINE"]},
    total=False,
)

ListAgentsResponseTypeDef = TypedDict(
    "ListAgentsResponseTypeDef",
    {"Agents": List[AgentListEntryTypeDef], "NextToken": str},
    total=False,
)

LocationListEntryTypeDef = TypedDict(
    "LocationListEntryTypeDef", {"LocationArn": str, "LocationUri": str}, total=False
)

ListLocationsResponseTypeDef = TypedDict(
    "ListLocationsResponseTypeDef",
    {"Locations": List[LocationListEntryTypeDef], "NextToken": str},
    total=False,
)

_RequiredTagListEntryTypeDef = TypedDict("_RequiredTagListEntryTypeDef", {"Key": str})
_OptionalTagListEntryTypeDef = TypedDict(
    "_OptionalTagListEntryTypeDef", {"Value": str}, total=False
)


class TagListEntryTypeDef(_RequiredTagListEntryTypeDef, _OptionalTagListEntryTypeDef):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {"Tags": List[TagListEntryTypeDef], "NextToken": str},
    total=False,
)

TaskExecutionListEntryTypeDef = TypedDict(
    "TaskExecutionListEntryTypeDef",
    {
        "TaskExecutionArn": str,
        "Status": Literal[
            "QUEUED", "LAUNCHING", "PREPARING", "TRANSFERRING", "VERIFYING", "SUCCESS", "ERROR"
        ],
    },
    total=False,
)

ListTaskExecutionsResponseTypeDef = TypedDict(
    "ListTaskExecutionsResponseTypeDef",
    {"TaskExecutions": List[TaskExecutionListEntryTypeDef], "NextToken": str},
    total=False,
)

TaskListEntryTypeDef = TypedDict(
    "TaskListEntryTypeDef",
    {
        "TaskArn": str,
        "Status": Literal["AVAILABLE", "CREATING", "QUEUED", "RUNNING", "UNAVAILABLE"],
        "Name": str,
    },
    total=False,
)

ListTasksResponseTypeDef = TypedDict(
    "ListTasksResponseTypeDef", {"Tasks": List[TaskListEntryTypeDef], "NextToken": str}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

StartTaskExecutionResponseTypeDef = TypedDict(
    "StartTaskExecutionResponseTypeDef", {"TaskExecutionArn": str}, total=False
)
