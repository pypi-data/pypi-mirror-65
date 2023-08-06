"""
Main interface for kendra service type definitions.

Usage::

    from mypy_boto3.kendra.type_defs import DocumentAttributeValueTypeDef

    data: DocumentAttributeValueTypeDef = {...}
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
    "DocumentAttributeValueTypeDef",
    "DocumentAttributeTypeDef",
    "AttributeFilterTypeDef",
    "BatchDeleteDocumentResponseFailedDocumentTypeDef",
    "BatchDeleteDocumentResponseTypeDef",
    "BatchPutDocumentResponseFailedDocumentTypeDef",
    "BatchPutDocumentResponseTypeDef",
    "ClickFeedbackTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateFaqResponseTypeDef",
    "CreateIndexResponseTypeDef",
    "AclConfigurationTypeDef",
    "DataSourceToIndexFieldMappingTypeDef",
    "ColumnConfigurationTypeDef",
    "ConnectionConfigurationTypeDef",
    "DataSourceVpcConfigurationTypeDef",
    "DatabaseConfigurationTypeDef",
    "AccessControlListConfigurationTypeDef",
    "DocumentsMetadataConfigurationTypeDef",
    "S3DataSourceConfigurationTypeDef",
    "SharePointConfigurationTypeDef",
    "DataSourceConfigurationTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "S3PathTypeDef",
    "DescribeFaqResponseTypeDef",
    "RelevanceTypeDef",
    "SearchTypeDef",
    "DocumentMetadataConfigurationTypeDef",
    "FaqStatisticsTypeDef",
    "TextDocumentStatisticsTypeDef",
    "IndexStatisticsTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "DescribeIndexResponseTypeDef",
    "PrincipalTypeDef",
    "DocumentTypeDef",
    "FacetTypeDef",
    "DataSourceSyncJobTypeDef",
    "ListDataSourceSyncJobsResponseTypeDef",
    "DataSourceSummaryTypeDef",
    "ListDataSourcesResponseTypeDef",
    "FaqSummaryTypeDef",
    "ListFaqsResponseTypeDef",
    "IndexConfigurationSummaryTypeDef",
    "ListIndicesResponseTypeDef",
    "DocumentAttributeValueCountPairTypeDef",
    "FacetResultTypeDef",
    "HighlightTypeDef",
    "TextWithHighlightsTypeDef",
    "AdditionalResultAttributeValueTypeDef",
    "AdditionalResultAttributeTypeDef",
    "QueryResultItemTypeDef",
    "QueryResultTypeDef",
    "RelevanceFeedbackTypeDef",
    "StartDataSourceSyncJobResponseTypeDef",
    "TimeRangeTypeDef",
)

DocumentAttributeValueTypeDef = TypedDict(
    "DocumentAttributeValueTypeDef",
    {"StringValue": str, "StringListValue": List[str], "LongValue": int, "DateValue": datetime},
    total=False,
)

DocumentAttributeTypeDef = TypedDict(
    "DocumentAttributeTypeDef", {"Key": str, "Value": DocumentAttributeValueTypeDef}
)

AttributeFilterTypeDef = TypedDict(
    "AttributeFilterTypeDef",
    {
        "AndAllFilters": List["AttributeFilterTypeDef"],
        "OrAllFilters": List["AttributeFilterTypeDef"],
        "NotFilter": "AttributeFilterTypeDef",
        "EqualsTo": DocumentAttributeTypeDef,
        "ContainsAll": DocumentAttributeTypeDef,
        "ContainsAny": DocumentAttributeTypeDef,
        "GreaterThan": DocumentAttributeTypeDef,
        "GreaterThanOrEquals": DocumentAttributeTypeDef,
        "LessThan": DocumentAttributeTypeDef,
        "LessThanOrEquals": DocumentAttributeTypeDef,
    },
    total=False,
)

BatchDeleteDocumentResponseFailedDocumentTypeDef = TypedDict(
    "BatchDeleteDocumentResponseFailedDocumentTypeDef",
    {"Id": str, "ErrorCode": Literal["InternalError", "InvalidRequest"], "ErrorMessage": str},
    total=False,
)

BatchDeleteDocumentResponseTypeDef = TypedDict(
    "BatchDeleteDocumentResponseTypeDef",
    {"FailedDocuments": List[BatchDeleteDocumentResponseFailedDocumentTypeDef]},
    total=False,
)

BatchPutDocumentResponseFailedDocumentTypeDef = TypedDict(
    "BatchPutDocumentResponseFailedDocumentTypeDef",
    {"Id": str, "ErrorCode": Literal["InternalError", "InvalidRequest"], "ErrorMessage": str},
    total=False,
)

BatchPutDocumentResponseTypeDef = TypedDict(
    "BatchPutDocumentResponseTypeDef",
    {"FailedDocuments": List[BatchPutDocumentResponseFailedDocumentTypeDef]},
    total=False,
)

ClickFeedbackTypeDef = TypedDict("ClickFeedbackTypeDef", {"ResultId": str, "ClickTime": datetime})

CreateDataSourceResponseTypeDef = TypedDict("CreateDataSourceResponseTypeDef", {"Id": str})

CreateFaqResponseTypeDef = TypedDict("CreateFaqResponseTypeDef", {"Id": str}, total=False)

CreateIndexResponseTypeDef = TypedDict("CreateIndexResponseTypeDef", {"Id": str}, total=False)

AclConfigurationTypeDef = TypedDict("AclConfigurationTypeDef", {"AllowedGroupsColumnName": str})

_RequiredDataSourceToIndexFieldMappingTypeDef = TypedDict(
    "_RequiredDataSourceToIndexFieldMappingTypeDef",
    {"DataSourceFieldName": str, "IndexFieldName": str},
)
_OptionalDataSourceToIndexFieldMappingTypeDef = TypedDict(
    "_OptionalDataSourceToIndexFieldMappingTypeDef", {"DateFieldFormat": str}, total=False
)


class DataSourceToIndexFieldMappingTypeDef(
    _RequiredDataSourceToIndexFieldMappingTypeDef, _OptionalDataSourceToIndexFieldMappingTypeDef
):
    pass


_RequiredColumnConfigurationTypeDef = TypedDict(
    "_RequiredColumnConfigurationTypeDef",
    {
        "DocumentIdColumnName": str,
        "DocumentDataColumnName": str,
        "ChangeDetectingColumns": List[str],
    },
)
_OptionalColumnConfigurationTypeDef = TypedDict(
    "_OptionalColumnConfigurationTypeDef",
    {"DocumentTitleColumnName": str, "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef]},
    total=False,
)


class ColumnConfigurationTypeDef(
    _RequiredColumnConfigurationTypeDef, _OptionalColumnConfigurationTypeDef
):
    pass


ConnectionConfigurationTypeDef = TypedDict(
    "ConnectionConfigurationTypeDef",
    {
        "DatabaseHost": str,
        "DatabasePort": int,
        "DatabaseName": str,
        "TableName": str,
        "SecretArn": str,
    },
)

DataSourceVpcConfigurationTypeDef = TypedDict(
    "DataSourceVpcConfigurationTypeDef", {"SubnetIds": List[str], "SecurityGroupIds": List[str]}
)

_RequiredDatabaseConfigurationTypeDef = TypedDict(
    "_RequiredDatabaseConfigurationTypeDef",
    {
        "DatabaseEngineType": Literal[
            "RDS_AURORA_MYSQL", "RDS_AURORA_POSTGRESQL", "RDS_MYSQL", "RDS_POSTGRESQL"
        ],
        "ConnectionConfiguration": ConnectionConfigurationTypeDef,
        "ColumnConfiguration": ColumnConfigurationTypeDef,
    },
)
_OptionalDatabaseConfigurationTypeDef = TypedDict(
    "_OptionalDatabaseConfigurationTypeDef",
    {
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
        "AclConfiguration": AclConfigurationTypeDef,
    },
    total=False,
)


class DatabaseConfigurationTypeDef(
    _RequiredDatabaseConfigurationTypeDef, _OptionalDatabaseConfigurationTypeDef
):
    pass


AccessControlListConfigurationTypeDef = TypedDict(
    "AccessControlListConfigurationTypeDef", {"KeyPath": str}, total=False
)

DocumentsMetadataConfigurationTypeDef = TypedDict(
    "DocumentsMetadataConfigurationTypeDef", {"S3Prefix": str}, total=False
)

_RequiredS3DataSourceConfigurationTypeDef = TypedDict(
    "_RequiredS3DataSourceConfigurationTypeDef", {"BucketName": str}
)
_OptionalS3DataSourceConfigurationTypeDef = TypedDict(
    "_OptionalS3DataSourceConfigurationTypeDef",
    {
        "InclusionPrefixes": List[str],
        "ExclusionPatterns": List[str],
        "DocumentsMetadataConfiguration": DocumentsMetadataConfigurationTypeDef,
        "AccessControlListConfiguration": AccessControlListConfigurationTypeDef,
    },
    total=False,
)


class S3DataSourceConfigurationTypeDef(
    _RequiredS3DataSourceConfigurationTypeDef, _OptionalS3DataSourceConfigurationTypeDef
):
    pass


_RequiredSharePointConfigurationTypeDef = TypedDict(
    "_RequiredSharePointConfigurationTypeDef",
    {"SharePointVersion": Literal["SHAREPOINT_ONLINE"], "Urls": List[str], "SecretArn": str},
)
_OptionalSharePointConfigurationTypeDef = TypedDict(
    "_OptionalSharePointConfigurationTypeDef",
    {
        "CrawlAttachments": bool,
        "UseChangeLog": bool,
        "InclusionPatterns": List[str],
        "ExclusionPatterns": List[str],
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
        "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef],
        "DocumentTitleFieldName": str,
    },
    total=False,
)


class SharePointConfigurationTypeDef(
    _RequiredSharePointConfigurationTypeDef, _OptionalSharePointConfigurationTypeDef
):
    pass


DataSourceConfigurationTypeDef = TypedDict(
    "DataSourceConfigurationTypeDef",
    {
        "S3Configuration": S3DataSourceConfigurationTypeDef,
        "SharePointConfiguration": SharePointConfigurationTypeDef,
        "DatabaseConfiguration": DatabaseConfigurationTypeDef,
    },
    total=False,
)

DescribeDataSourceResponseTypeDef = TypedDict(
    "DescribeDataSourceResponseTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Name": str,
        "Type": Literal["S3", "SHAREPOINT", "DATABASE"],
        "Configuration": DataSourceConfigurationTypeDef,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Description": str,
        "Status": Literal["CREATING", "DELETING", "FAILED", "UPDATING", "ACTIVE"],
        "Schedule": str,
        "RoleArn": str,
        "ErrorMessage": str,
    },
    total=False,
)

S3PathTypeDef = TypedDict("S3PathTypeDef", {"Bucket": str, "Key": str})

DescribeFaqResponseTypeDef = TypedDict(
    "DescribeFaqResponseTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Name": str,
        "Description": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "S3Path": S3PathTypeDef,
        "Status": Literal["CREATING", "UPDATING", "ACTIVE", "DELETING", "FAILED"],
        "RoleArn": str,
        "ErrorMessage": str,
    },
    total=False,
)

RelevanceTypeDef = TypedDict(
    "RelevanceTypeDef",
    {
        "Freshness": bool,
        "Importance": int,
        "Duration": str,
        "RankOrder": Literal["ASCENDING", "DESCENDING"],
        "ValueImportanceMap": Dict[str, int],
    },
    total=False,
)

SearchTypeDef = TypedDict(
    "SearchTypeDef", {"Facetable": bool, "Searchable": bool, "Displayable": bool}, total=False
)

_RequiredDocumentMetadataConfigurationTypeDef = TypedDict(
    "_RequiredDocumentMetadataConfigurationTypeDef",
    {"Name": str, "Type": Literal["STRING_VALUE", "STRING_LIST_VALUE", "LONG_VALUE", "DATE_VALUE"]},
)
_OptionalDocumentMetadataConfigurationTypeDef = TypedDict(
    "_OptionalDocumentMetadataConfigurationTypeDef",
    {"Relevance": RelevanceTypeDef, "Search": SearchTypeDef},
    total=False,
)


class DocumentMetadataConfigurationTypeDef(
    _RequiredDocumentMetadataConfigurationTypeDef, _OptionalDocumentMetadataConfigurationTypeDef
):
    pass


FaqStatisticsTypeDef = TypedDict("FaqStatisticsTypeDef", {"IndexedQuestionAnswersCount": int})

TextDocumentStatisticsTypeDef = TypedDict(
    "TextDocumentStatisticsTypeDef", {"IndexedTextDocumentsCount": int}
)

IndexStatisticsTypeDef = TypedDict(
    "IndexStatisticsTypeDef",
    {
        "FaqStatistics": FaqStatisticsTypeDef,
        "TextDocumentStatistics": TextDocumentStatisticsTypeDef,
    },
)

ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef", {"KmsKeyId": str}, total=False
)

DescribeIndexResponseTypeDef = TypedDict(
    "DescribeIndexResponseTypeDef",
    {
        "Name": str,
        "Id": str,
        "RoleArn": str,
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "Status": Literal["CREATING", "ACTIVE", "DELETING", "FAILED", "SYSTEM_UPDATING"],
        "Description": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "DocumentMetadataConfigurations": List[DocumentMetadataConfigurationTypeDef],
        "IndexStatistics": IndexStatisticsTypeDef,
        "ErrorMessage": str,
    },
    total=False,
)

PrincipalTypeDef = TypedDict(
    "PrincipalTypeDef",
    {"Name": str, "Type": Literal["USER", "GROUP"], "Access": Literal["ALLOW", "DENY"]},
)

_RequiredDocumentTypeDef = TypedDict("_RequiredDocumentTypeDef", {"Id": str})
_OptionalDocumentTypeDef = TypedDict(
    "_OptionalDocumentTypeDef",
    {
        "Title": str,
        "Blob": Union[bytes, IO],
        "S3Path": S3PathTypeDef,
        "Attributes": List[DocumentAttributeTypeDef],
        "AccessControlList": List[PrincipalTypeDef],
        "ContentType": Literal["PDF", "HTML", "MS_WORD", "PLAIN_TEXT", "PPT"],
    },
    total=False,
)


class DocumentTypeDef(_RequiredDocumentTypeDef, _OptionalDocumentTypeDef):
    pass


FacetTypeDef = TypedDict("FacetTypeDef", {"DocumentAttributeKey": str}, total=False)

DataSourceSyncJobTypeDef = TypedDict(
    "DataSourceSyncJobTypeDef",
    {
        "ExecutionId": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "Status": Literal["FAILED", "SUCCEEDED", "SYNCING", "INCOMPLETE", "STOPPING", "ABORTED"],
        "ErrorMessage": str,
        "ErrorCode": Literal["InternalError", "InvalidRequest"],
        "DataSourceErrorCode": str,
    },
    total=False,
)

ListDataSourceSyncJobsResponseTypeDef = TypedDict(
    "ListDataSourceSyncJobsResponseTypeDef",
    {"History": List[DataSourceSyncJobTypeDef], "NextToken": str},
    total=False,
)

DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Type": Literal["S3", "SHAREPOINT", "DATABASE"],
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Status": Literal["CREATING", "DELETING", "FAILED", "UPDATING", "ACTIVE"],
    },
    total=False,
)

ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {"SummaryItems": List[DataSourceSummaryTypeDef], "NextToken": str},
    total=False,
)

FaqSummaryTypeDef = TypedDict(
    "FaqSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": Literal["CREATING", "UPDATING", "ACTIVE", "DELETING", "FAILED"],
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
    },
    total=False,
)

ListFaqsResponseTypeDef = TypedDict(
    "ListFaqsResponseTypeDef",
    {"NextToken": str, "FaqSummaryItems": List[FaqSummaryTypeDef]},
    total=False,
)

_RequiredIndexConfigurationSummaryTypeDef = TypedDict(
    "_RequiredIndexConfigurationSummaryTypeDef",
    {
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Status": Literal["CREATING", "ACTIVE", "DELETING", "FAILED", "SYSTEM_UPDATING"],
    },
)
_OptionalIndexConfigurationSummaryTypeDef = TypedDict(
    "_OptionalIndexConfigurationSummaryTypeDef", {"Name": str, "Id": str}, total=False
)


class IndexConfigurationSummaryTypeDef(
    _RequiredIndexConfigurationSummaryTypeDef, _OptionalIndexConfigurationSummaryTypeDef
):
    pass


ListIndicesResponseTypeDef = TypedDict(
    "ListIndicesResponseTypeDef",
    {"IndexConfigurationSummaryItems": List[IndexConfigurationSummaryTypeDef], "NextToken": str},
    total=False,
)

DocumentAttributeValueCountPairTypeDef = TypedDict(
    "DocumentAttributeValueCountPairTypeDef",
    {"DocumentAttributeValue": DocumentAttributeValueTypeDef, "Count": int},
    total=False,
)

FacetResultTypeDef = TypedDict(
    "FacetResultTypeDef",
    {
        "DocumentAttributeKey": str,
        "DocumentAttributeValueCountPairs": List[DocumentAttributeValueCountPairTypeDef],
    },
    total=False,
)

_RequiredHighlightTypeDef = TypedDict(
    "_RequiredHighlightTypeDef", {"BeginOffset": int, "EndOffset": int}
)
_OptionalHighlightTypeDef = TypedDict("_OptionalHighlightTypeDef", {"TopAnswer": bool}, total=False)


class HighlightTypeDef(_RequiredHighlightTypeDef, _OptionalHighlightTypeDef):
    pass


TextWithHighlightsTypeDef = TypedDict(
    "TextWithHighlightsTypeDef", {"Text": str, "Highlights": List[HighlightTypeDef]}, total=False
)

AdditionalResultAttributeValueTypeDef = TypedDict(
    "AdditionalResultAttributeValueTypeDef",
    {"TextWithHighlightsValue": TextWithHighlightsTypeDef},
    total=False,
)

AdditionalResultAttributeTypeDef = TypedDict(
    "AdditionalResultAttributeTypeDef",
    {
        "Key": str,
        "ValueType": Literal["TEXT_WITH_HIGHLIGHTS_VALUE"],
        "Value": AdditionalResultAttributeValueTypeDef,
    },
)

QueryResultItemTypeDef = TypedDict(
    "QueryResultItemTypeDef",
    {
        "Id": str,
        "Type": Literal["DOCUMENT", "QUESTION_ANSWER", "ANSWER"],
        "AdditionalAttributes": List[AdditionalResultAttributeTypeDef],
        "DocumentId": str,
        "DocumentTitle": TextWithHighlightsTypeDef,
        "DocumentExcerpt": TextWithHighlightsTypeDef,
        "DocumentURI": str,
        "DocumentAttributes": List[DocumentAttributeTypeDef],
    },
    total=False,
)

QueryResultTypeDef = TypedDict(
    "QueryResultTypeDef",
    {
        "QueryId": str,
        "ResultItems": List[QueryResultItemTypeDef],
        "FacetResults": List[FacetResultTypeDef],
        "TotalNumberOfResults": int,
    },
    total=False,
)

RelevanceFeedbackTypeDef = TypedDict(
    "RelevanceFeedbackTypeDef",
    {"ResultId": str, "RelevanceValue": Literal["RELEVANT", "NOT_RELEVANT"]},
)

StartDataSourceSyncJobResponseTypeDef = TypedDict(
    "StartDataSourceSyncJobResponseTypeDef", {"ExecutionId": str}, total=False
)

TimeRangeTypeDef = TypedDict(
    "TimeRangeTypeDef", {"StartTime": datetime, "EndTime": datetime}, total=False
)
