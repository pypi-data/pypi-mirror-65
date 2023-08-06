"""
Main interface for mgh service type definitions.

Usage::

    from mypy_boto3.mgh.type_defs import CreatedArtifactTypeDef

    data: CreatedArtifactTypeDef = {...}
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
    "CreatedArtifactTypeDef",
    "DescribeApplicationStateResultTypeDef",
    "ResourceAttributeTypeDef",
    "TaskTypeDef",
    "MigrationTaskTypeDef",
    "DescribeMigrationTaskResultTypeDef",
    "DiscoveredResourceTypeDef",
    "ApplicationStateTypeDef",
    "ListApplicationStatesResultTypeDef",
    "ListCreatedArtifactsResultTypeDef",
    "ListDiscoveredResourcesResultTypeDef",
    "MigrationTaskSummaryTypeDef",
    "ListMigrationTasksResultTypeDef",
    "ProgressUpdateStreamSummaryTypeDef",
    "ListProgressUpdateStreamsResultTypeDef",
    "PaginatorConfigTypeDef",
)

_RequiredCreatedArtifactTypeDef = TypedDict("_RequiredCreatedArtifactTypeDef", {"Name": str})
_OptionalCreatedArtifactTypeDef = TypedDict(
    "_OptionalCreatedArtifactTypeDef", {"Description": str}, total=False
)


class CreatedArtifactTypeDef(_RequiredCreatedArtifactTypeDef, _OptionalCreatedArtifactTypeDef):
    pass


DescribeApplicationStateResultTypeDef = TypedDict(
    "DescribeApplicationStateResultTypeDef",
    {
        "ApplicationStatus": Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETED"],
        "LastUpdatedTime": datetime,
    },
    total=False,
)

ResourceAttributeTypeDef = TypedDict(
    "ResourceAttributeTypeDef",
    {
        "Type": Literal[
            "IPV4_ADDRESS",
            "IPV6_ADDRESS",
            "MAC_ADDRESS",
            "FQDN",
            "VM_MANAGER_ID",
            "VM_MANAGED_OBJECT_REFERENCE",
            "VM_NAME",
            "VM_PATH",
            "BIOS_ID",
            "MOTHERBOARD_SERIAL_NUMBER",
        ],
        "Value": str,
    },
)

_RequiredTaskTypeDef = TypedDict(
    "_RequiredTaskTypeDef", {"Status": Literal["NOT_STARTED", "IN_PROGRESS", "FAILED", "COMPLETED"]}
)
_OptionalTaskTypeDef = TypedDict(
    "_OptionalTaskTypeDef", {"StatusDetail": str, "ProgressPercent": int}, total=False
)


class TaskTypeDef(_RequiredTaskTypeDef, _OptionalTaskTypeDef):
    pass


MigrationTaskTypeDef = TypedDict(
    "MigrationTaskTypeDef",
    {
        "ProgressUpdateStream": str,
        "MigrationTaskName": str,
        "Task": TaskTypeDef,
        "UpdateDateTime": datetime,
        "ResourceAttributeList": List[ResourceAttributeTypeDef],
    },
    total=False,
)

DescribeMigrationTaskResultTypeDef = TypedDict(
    "DescribeMigrationTaskResultTypeDef", {"MigrationTask": MigrationTaskTypeDef}, total=False
)

_RequiredDiscoveredResourceTypeDef = TypedDict(
    "_RequiredDiscoveredResourceTypeDef", {"ConfigurationId": str}
)
_OptionalDiscoveredResourceTypeDef = TypedDict(
    "_OptionalDiscoveredResourceTypeDef", {"Description": str}, total=False
)


class DiscoveredResourceTypeDef(
    _RequiredDiscoveredResourceTypeDef, _OptionalDiscoveredResourceTypeDef
):
    pass


ApplicationStateTypeDef = TypedDict(
    "ApplicationStateTypeDef",
    {
        "ApplicationId": str,
        "ApplicationStatus": Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETED"],
        "LastUpdatedTime": datetime,
    },
    total=False,
)

ListApplicationStatesResultTypeDef = TypedDict(
    "ListApplicationStatesResultTypeDef",
    {"ApplicationStateList": List[ApplicationStateTypeDef], "NextToken": str},
    total=False,
)

ListCreatedArtifactsResultTypeDef = TypedDict(
    "ListCreatedArtifactsResultTypeDef",
    {"NextToken": str, "CreatedArtifactList": List[CreatedArtifactTypeDef]},
    total=False,
)

ListDiscoveredResourcesResultTypeDef = TypedDict(
    "ListDiscoveredResourcesResultTypeDef",
    {"NextToken": str, "DiscoveredResourceList": List[DiscoveredResourceTypeDef]},
    total=False,
)

MigrationTaskSummaryTypeDef = TypedDict(
    "MigrationTaskSummaryTypeDef",
    {
        "ProgressUpdateStream": str,
        "MigrationTaskName": str,
        "Status": Literal["NOT_STARTED", "IN_PROGRESS", "FAILED", "COMPLETED"],
        "ProgressPercent": int,
        "StatusDetail": str,
        "UpdateDateTime": datetime,
    },
    total=False,
)

ListMigrationTasksResultTypeDef = TypedDict(
    "ListMigrationTasksResultTypeDef",
    {"NextToken": str, "MigrationTaskSummaryList": List[MigrationTaskSummaryTypeDef]},
    total=False,
)

ProgressUpdateStreamSummaryTypeDef = TypedDict(
    "ProgressUpdateStreamSummaryTypeDef", {"ProgressUpdateStreamName": str}, total=False
)

ListProgressUpdateStreamsResultTypeDef = TypedDict(
    "ListProgressUpdateStreamsResultTypeDef",
    {"ProgressUpdateStreamSummaryList": List[ProgressUpdateStreamSummaryTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
