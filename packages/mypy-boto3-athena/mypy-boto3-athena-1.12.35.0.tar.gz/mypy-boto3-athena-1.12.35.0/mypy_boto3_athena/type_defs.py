"""
Main interface for athena service type definitions.

Usage::

    from mypy_boto3.athena.type_defs import NamedQueryTypeDef

    data: NamedQueryTypeDef = {...}
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
    "NamedQueryTypeDef",
    "UnprocessedNamedQueryIdTypeDef",
    "BatchGetNamedQueryOutputTypeDef",
    "QueryExecutionContextTypeDef",
    "QueryExecutionStatisticsTypeDef",
    "QueryExecutionStatusTypeDef",
    "EncryptionConfigurationTypeDef",
    "ResultConfigurationTypeDef",
    "QueryExecutionTypeDef",
    "UnprocessedQueryExecutionIdTypeDef",
    "BatchGetQueryExecutionOutputTypeDef",
    "CreateNamedQueryOutputTypeDef",
    "GetNamedQueryOutputTypeDef",
    "GetQueryExecutionOutputTypeDef",
    "ColumnInfoTypeDef",
    "ResultSetMetadataTypeDef",
    "DatumTypeDef",
    "RowTypeDef",
    "ResultSetTypeDef",
    "GetQueryResultsOutputTypeDef",
    "WorkGroupConfigurationTypeDef",
    "WorkGroupTypeDef",
    "GetWorkGroupOutputTypeDef",
    "ListNamedQueriesOutputTypeDef",
    "ListQueryExecutionsOutputTypeDef",
    "TagTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "WorkGroupSummaryTypeDef",
    "ListWorkGroupsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "StartQueryExecutionOutputTypeDef",
    "ResultConfigurationUpdatesTypeDef",
    "WorkGroupConfigurationUpdatesTypeDef",
)

_RequiredNamedQueryTypeDef = TypedDict(
    "_RequiredNamedQueryTypeDef", {"Name": str, "Database": str, "QueryString": str}
)
_OptionalNamedQueryTypeDef = TypedDict(
    "_OptionalNamedQueryTypeDef",
    {"Description": str, "NamedQueryId": str, "WorkGroup": str},
    total=False,
)


class NamedQueryTypeDef(_RequiredNamedQueryTypeDef, _OptionalNamedQueryTypeDef):
    pass


UnprocessedNamedQueryIdTypeDef = TypedDict(
    "UnprocessedNamedQueryIdTypeDef",
    {"NamedQueryId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

BatchGetNamedQueryOutputTypeDef = TypedDict(
    "BatchGetNamedQueryOutputTypeDef",
    {
        "NamedQueries": List[NamedQueryTypeDef],
        "UnprocessedNamedQueryIds": List[UnprocessedNamedQueryIdTypeDef],
    },
    total=False,
)

QueryExecutionContextTypeDef = TypedDict(
    "QueryExecutionContextTypeDef", {"Database": str}, total=False
)

QueryExecutionStatisticsTypeDef = TypedDict(
    "QueryExecutionStatisticsTypeDef",
    {
        "EngineExecutionTimeInMillis": int,
        "DataScannedInBytes": int,
        "DataManifestLocation": str,
        "TotalExecutionTimeInMillis": int,
        "QueryQueueTimeInMillis": int,
        "QueryPlanningTimeInMillis": int,
        "ServiceProcessingTimeInMillis": int,
    },
    total=False,
)

QueryExecutionStatusTypeDef = TypedDict(
    "QueryExecutionStatusTypeDef",
    {
        "State": Literal["QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "CANCELLED"],
        "StateChangeReason": str,
        "SubmissionDateTime": datetime,
        "CompletionDateTime": datetime,
    },
    total=False,
)

_RequiredEncryptionConfigurationTypeDef = TypedDict(
    "_RequiredEncryptionConfigurationTypeDef",
    {"EncryptionOption": Literal["SSE_S3", "SSE_KMS", "CSE_KMS"]},
)
_OptionalEncryptionConfigurationTypeDef = TypedDict(
    "_OptionalEncryptionConfigurationTypeDef", {"KmsKey": str}, total=False
)


class EncryptionConfigurationTypeDef(
    _RequiredEncryptionConfigurationTypeDef, _OptionalEncryptionConfigurationTypeDef
):
    pass


ResultConfigurationTypeDef = TypedDict(
    "ResultConfigurationTypeDef",
    {"OutputLocation": str, "EncryptionConfiguration": EncryptionConfigurationTypeDef},
    total=False,
)

QueryExecutionTypeDef = TypedDict(
    "QueryExecutionTypeDef",
    {
        "QueryExecutionId": str,
        "Query": str,
        "StatementType": Literal["DDL", "DML", "UTILITY"],
        "ResultConfiguration": ResultConfigurationTypeDef,
        "QueryExecutionContext": QueryExecutionContextTypeDef,
        "Status": QueryExecutionStatusTypeDef,
        "Statistics": QueryExecutionStatisticsTypeDef,
        "WorkGroup": str,
    },
    total=False,
)

UnprocessedQueryExecutionIdTypeDef = TypedDict(
    "UnprocessedQueryExecutionIdTypeDef",
    {"QueryExecutionId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

BatchGetQueryExecutionOutputTypeDef = TypedDict(
    "BatchGetQueryExecutionOutputTypeDef",
    {
        "QueryExecutions": List[QueryExecutionTypeDef],
        "UnprocessedQueryExecutionIds": List[UnprocessedQueryExecutionIdTypeDef],
    },
    total=False,
)

CreateNamedQueryOutputTypeDef = TypedDict(
    "CreateNamedQueryOutputTypeDef", {"NamedQueryId": str}, total=False
)

GetNamedQueryOutputTypeDef = TypedDict(
    "GetNamedQueryOutputTypeDef", {"NamedQuery": NamedQueryTypeDef}, total=False
)

GetQueryExecutionOutputTypeDef = TypedDict(
    "GetQueryExecutionOutputTypeDef", {"QueryExecution": QueryExecutionTypeDef}, total=False
)

_RequiredColumnInfoTypeDef = TypedDict("_RequiredColumnInfoTypeDef", {"Name": str, "Type": str})
_OptionalColumnInfoTypeDef = TypedDict(
    "_OptionalColumnInfoTypeDef",
    {
        "CatalogName": str,
        "SchemaName": str,
        "TableName": str,
        "Label": str,
        "Precision": int,
        "Scale": int,
        "Nullable": Literal["NOT_NULL", "NULLABLE", "UNKNOWN"],
        "CaseSensitive": bool,
    },
    total=False,
)


class ColumnInfoTypeDef(_RequiredColumnInfoTypeDef, _OptionalColumnInfoTypeDef):
    pass


ResultSetMetadataTypeDef = TypedDict(
    "ResultSetMetadataTypeDef", {"ColumnInfo": List[ColumnInfoTypeDef]}, total=False
)

DatumTypeDef = TypedDict("DatumTypeDef", {"VarCharValue": str}, total=False)

RowTypeDef = TypedDict("RowTypeDef", {"Data": List[DatumTypeDef]}, total=False)

ResultSetTypeDef = TypedDict(
    "ResultSetTypeDef",
    {"Rows": List[RowTypeDef], "ResultSetMetadata": ResultSetMetadataTypeDef},
    total=False,
)

GetQueryResultsOutputTypeDef = TypedDict(
    "GetQueryResultsOutputTypeDef",
    {"UpdateCount": int, "ResultSet": ResultSetTypeDef, "NextToken": str},
    total=False,
)

WorkGroupConfigurationTypeDef = TypedDict(
    "WorkGroupConfigurationTypeDef",
    {
        "ResultConfiguration": ResultConfigurationTypeDef,
        "EnforceWorkGroupConfiguration": bool,
        "PublishCloudWatchMetricsEnabled": bool,
        "BytesScannedCutoffPerQuery": int,
        "RequesterPaysEnabled": bool,
    },
    total=False,
)

_RequiredWorkGroupTypeDef = TypedDict("_RequiredWorkGroupTypeDef", {"Name": str})
_OptionalWorkGroupTypeDef = TypedDict(
    "_OptionalWorkGroupTypeDef",
    {
        "State": Literal["ENABLED", "DISABLED"],
        "Configuration": WorkGroupConfigurationTypeDef,
        "Description": str,
        "CreationTime": datetime,
    },
    total=False,
)


class WorkGroupTypeDef(_RequiredWorkGroupTypeDef, _OptionalWorkGroupTypeDef):
    pass


GetWorkGroupOutputTypeDef = TypedDict(
    "GetWorkGroupOutputTypeDef", {"WorkGroup": WorkGroupTypeDef}, total=False
)

ListNamedQueriesOutputTypeDef = TypedDict(
    "ListNamedQueriesOutputTypeDef", {"NamedQueryIds": List[str], "NextToken": str}, total=False
)

ListQueryExecutionsOutputTypeDef = TypedDict(
    "ListQueryExecutionsOutputTypeDef",
    {"QueryExecutionIds": List[str], "NextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str}, total=False)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef", {"Tags": List[TagTypeDef], "NextToken": str}, total=False
)

WorkGroupSummaryTypeDef = TypedDict(
    "WorkGroupSummaryTypeDef",
    {
        "Name": str,
        "State": Literal["ENABLED", "DISABLED"],
        "Description": str,
        "CreationTime": datetime,
    },
    total=False,
)

ListWorkGroupsOutputTypeDef = TypedDict(
    "ListWorkGroupsOutputTypeDef",
    {"WorkGroups": List[WorkGroupSummaryTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

StartQueryExecutionOutputTypeDef = TypedDict(
    "StartQueryExecutionOutputTypeDef", {"QueryExecutionId": str}, total=False
)

ResultConfigurationUpdatesTypeDef = TypedDict(
    "ResultConfigurationUpdatesTypeDef",
    {
        "OutputLocation": str,
        "RemoveOutputLocation": bool,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "RemoveEncryptionConfiguration": bool,
    },
    total=False,
)

WorkGroupConfigurationUpdatesTypeDef = TypedDict(
    "WorkGroupConfigurationUpdatesTypeDef",
    {
        "EnforceWorkGroupConfiguration": bool,
        "ResultConfigurationUpdates": ResultConfigurationUpdatesTypeDef,
        "PublishCloudWatchMetricsEnabled": bool,
        "BytesScannedCutoffPerQuery": int,
        "RemoveBytesScannedCutoffPerQuery": bool,
        "RequesterPaysEnabled": bool,
    },
    total=False,
)
