"""
Main interface for kinesisanalytics service type definitions.

Usage::

    from mypy_boto3.kinesisanalytics.type_defs import CloudWatchLoggingOptionUpdateTypeDef

    data: CloudWatchLoggingOptionUpdateTypeDef = {...}
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
    "CloudWatchLoggingOptionUpdateTypeDef",
    "InputParallelismUpdateTypeDef",
    "InputLambdaProcessorUpdateTypeDef",
    "InputProcessingConfigurationUpdateTypeDef",
    "RecordColumnTypeDef",
    "CSVMappingParametersTypeDef",
    "JSONMappingParametersTypeDef",
    "MappingParametersTypeDef",
    "RecordFormatTypeDef",
    "InputSchemaUpdateTypeDef",
    "KinesisFirehoseInputUpdateTypeDef",
    "KinesisStreamsInputUpdateTypeDef",
    "InputUpdateTypeDef",
    "DestinationSchemaTypeDef",
    "KinesisFirehoseOutputUpdateTypeDef",
    "KinesisStreamsOutputUpdateTypeDef",
    "LambdaOutputUpdateTypeDef",
    "OutputUpdateTypeDef",
    "S3ReferenceDataSourceUpdateTypeDef",
    "SourceSchemaTypeDef",
    "ReferenceDataSourceUpdateTypeDef",
    "ApplicationUpdateTypeDef",
    "CloudWatchLoggingOptionTypeDef",
    "ApplicationSummaryTypeDef",
    "CreateApplicationResponseTypeDef",
    "CloudWatchLoggingOptionDescriptionTypeDef",
    "InputParallelismTypeDef",
    "InputLambdaProcessorDescriptionTypeDef",
    "InputProcessingConfigurationDescriptionTypeDef",
    "InputStartingPositionConfigurationTypeDef",
    "KinesisFirehoseInputDescriptionTypeDef",
    "KinesisStreamsInputDescriptionTypeDef",
    "InputDescriptionTypeDef",
    "KinesisFirehoseOutputDescriptionTypeDef",
    "KinesisStreamsOutputDescriptionTypeDef",
    "LambdaOutputDescriptionTypeDef",
    "OutputDescriptionTypeDef",
    "S3ReferenceDataSourceDescriptionTypeDef",
    "ReferenceDataSourceDescriptionTypeDef",
    "ApplicationDetailTypeDef",
    "DescribeApplicationResponseTypeDef",
    "DiscoverInputSchemaResponseTypeDef",
    "InputConfigurationTypeDef",
    "InputLambdaProcessorTypeDef",
    "InputProcessingConfigurationTypeDef",
    "KinesisFirehoseInputTypeDef",
    "KinesisStreamsInputTypeDef",
    "InputTypeDef",
    "ListApplicationsResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "KinesisFirehoseOutputTypeDef",
    "KinesisStreamsOutputTypeDef",
    "LambdaOutputTypeDef",
    "OutputTypeDef",
    "S3ReferenceDataSourceTypeDef",
    "ReferenceDataSourceTypeDef",
    "S3ConfigurationTypeDef",
)

_RequiredCloudWatchLoggingOptionUpdateTypeDef = TypedDict(
    "_RequiredCloudWatchLoggingOptionUpdateTypeDef", {"CloudWatchLoggingOptionId": str}
)
_OptionalCloudWatchLoggingOptionUpdateTypeDef = TypedDict(
    "_OptionalCloudWatchLoggingOptionUpdateTypeDef",
    {"LogStreamARNUpdate": str, "RoleARNUpdate": str},
    total=False,
)


class CloudWatchLoggingOptionUpdateTypeDef(
    _RequiredCloudWatchLoggingOptionUpdateTypeDef, _OptionalCloudWatchLoggingOptionUpdateTypeDef
):
    pass


InputParallelismUpdateTypeDef = TypedDict(
    "InputParallelismUpdateTypeDef", {"CountUpdate": int}, total=False
)

InputLambdaProcessorUpdateTypeDef = TypedDict(
    "InputLambdaProcessorUpdateTypeDef",
    {"ResourceARNUpdate": str, "RoleARNUpdate": str},
    total=False,
)

InputProcessingConfigurationUpdateTypeDef = TypedDict(
    "InputProcessingConfigurationUpdateTypeDef",
    {"InputLambdaProcessorUpdate": InputLambdaProcessorUpdateTypeDef},
)

_RequiredRecordColumnTypeDef = TypedDict(
    "_RequiredRecordColumnTypeDef", {"Name": str, "SqlType": str}
)
_OptionalRecordColumnTypeDef = TypedDict(
    "_OptionalRecordColumnTypeDef", {"Mapping": str}, total=False
)


class RecordColumnTypeDef(_RequiredRecordColumnTypeDef, _OptionalRecordColumnTypeDef):
    pass


CSVMappingParametersTypeDef = TypedDict(
    "CSVMappingParametersTypeDef", {"RecordRowDelimiter": str, "RecordColumnDelimiter": str}
)

JSONMappingParametersTypeDef = TypedDict("JSONMappingParametersTypeDef", {"RecordRowPath": str})

MappingParametersTypeDef = TypedDict(
    "MappingParametersTypeDef",
    {
        "JSONMappingParameters": JSONMappingParametersTypeDef,
        "CSVMappingParameters": CSVMappingParametersTypeDef,
    },
    total=False,
)

_RequiredRecordFormatTypeDef = TypedDict(
    "_RequiredRecordFormatTypeDef", {"RecordFormatType": Literal["JSON", "CSV"]}
)
_OptionalRecordFormatTypeDef = TypedDict(
    "_OptionalRecordFormatTypeDef", {"MappingParameters": MappingParametersTypeDef}, total=False
)


class RecordFormatTypeDef(_RequiredRecordFormatTypeDef, _OptionalRecordFormatTypeDef):
    pass


InputSchemaUpdateTypeDef = TypedDict(
    "InputSchemaUpdateTypeDef",
    {
        "RecordFormatUpdate": RecordFormatTypeDef,
        "RecordEncodingUpdate": str,
        "RecordColumnUpdates": List[RecordColumnTypeDef],
    },
    total=False,
)

KinesisFirehoseInputUpdateTypeDef = TypedDict(
    "KinesisFirehoseInputUpdateTypeDef",
    {"ResourceARNUpdate": str, "RoleARNUpdate": str},
    total=False,
)

KinesisStreamsInputUpdateTypeDef = TypedDict(
    "KinesisStreamsInputUpdateTypeDef",
    {"ResourceARNUpdate": str, "RoleARNUpdate": str},
    total=False,
)

_RequiredInputUpdateTypeDef = TypedDict("_RequiredInputUpdateTypeDef", {"InputId": str})
_OptionalInputUpdateTypeDef = TypedDict(
    "_OptionalInputUpdateTypeDef",
    {
        "NamePrefixUpdate": str,
        "InputProcessingConfigurationUpdate": InputProcessingConfigurationUpdateTypeDef,
        "KinesisStreamsInputUpdate": KinesisStreamsInputUpdateTypeDef,
        "KinesisFirehoseInputUpdate": KinesisFirehoseInputUpdateTypeDef,
        "InputSchemaUpdate": InputSchemaUpdateTypeDef,
        "InputParallelismUpdate": InputParallelismUpdateTypeDef,
    },
    total=False,
)


class InputUpdateTypeDef(_RequiredInputUpdateTypeDef, _OptionalInputUpdateTypeDef):
    pass


DestinationSchemaTypeDef = TypedDict(
    "DestinationSchemaTypeDef", {"RecordFormatType": Literal["JSON", "CSV"]}
)

KinesisFirehoseOutputUpdateTypeDef = TypedDict(
    "KinesisFirehoseOutputUpdateTypeDef",
    {"ResourceARNUpdate": str, "RoleARNUpdate": str},
    total=False,
)

KinesisStreamsOutputUpdateTypeDef = TypedDict(
    "KinesisStreamsOutputUpdateTypeDef",
    {"ResourceARNUpdate": str, "RoleARNUpdate": str},
    total=False,
)

LambdaOutputUpdateTypeDef = TypedDict(
    "LambdaOutputUpdateTypeDef", {"ResourceARNUpdate": str, "RoleARNUpdate": str}, total=False
)

_RequiredOutputUpdateTypeDef = TypedDict("_RequiredOutputUpdateTypeDef", {"OutputId": str})
_OptionalOutputUpdateTypeDef = TypedDict(
    "_OptionalOutputUpdateTypeDef",
    {
        "NameUpdate": str,
        "KinesisStreamsOutputUpdate": KinesisStreamsOutputUpdateTypeDef,
        "KinesisFirehoseOutputUpdate": KinesisFirehoseOutputUpdateTypeDef,
        "LambdaOutputUpdate": LambdaOutputUpdateTypeDef,
        "DestinationSchemaUpdate": DestinationSchemaTypeDef,
    },
    total=False,
)


class OutputUpdateTypeDef(_RequiredOutputUpdateTypeDef, _OptionalOutputUpdateTypeDef):
    pass


S3ReferenceDataSourceUpdateTypeDef = TypedDict(
    "S3ReferenceDataSourceUpdateTypeDef",
    {"BucketARNUpdate": str, "FileKeyUpdate": str, "ReferenceRoleARNUpdate": str},
    total=False,
)

_RequiredSourceSchemaTypeDef = TypedDict(
    "_RequiredSourceSchemaTypeDef",
    {"RecordFormat": RecordFormatTypeDef, "RecordColumns": List[RecordColumnTypeDef]},
)
_OptionalSourceSchemaTypeDef = TypedDict(
    "_OptionalSourceSchemaTypeDef", {"RecordEncoding": str}, total=False
)


class SourceSchemaTypeDef(_RequiredSourceSchemaTypeDef, _OptionalSourceSchemaTypeDef):
    pass


_RequiredReferenceDataSourceUpdateTypeDef = TypedDict(
    "_RequiredReferenceDataSourceUpdateTypeDef", {"ReferenceId": str}
)
_OptionalReferenceDataSourceUpdateTypeDef = TypedDict(
    "_OptionalReferenceDataSourceUpdateTypeDef",
    {
        "TableNameUpdate": str,
        "S3ReferenceDataSourceUpdate": S3ReferenceDataSourceUpdateTypeDef,
        "ReferenceSchemaUpdate": SourceSchemaTypeDef,
    },
    total=False,
)


class ReferenceDataSourceUpdateTypeDef(
    _RequiredReferenceDataSourceUpdateTypeDef, _OptionalReferenceDataSourceUpdateTypeDef
):
    pass


ApplicationUpdateTypeDef = TypedDict(
    "ApplicationUpdateTypeDef",
    {
        "InputUpdates": List[InputUpdateTypeDef],
        "ApplicationCodeUpdate": str,
        "OutputUpdates": List[OutputUpdateTypeDef],
        "ReferenceDataSourceUpdates": List[ReferenceDataSourceUpdateTypeDef],
        "CloudWatchLoggingOptionUpdates": List[CloudWatchLoggingOptionUpdateTypeDef],
    },
    total=False,
)

CloudWatchLoggingOptionTypeDef = TypedDict(
    "CloudWatchLoggingOptionTypeDef", {"LogStreamARN": str, "RoleARN": str}
)

ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "ApplicationName": str,
        "ApplicationARN": str,
        "ApplicationStatus": Literal[
            "DELETING", "STARTING", "STOPPING", "READY", "RUNNING", "UPDATING"
        ],
    },
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef", {"ApplicationSummary": ApplicationSummaryTypeDef}
)

_RequiredCloudWatchLoggingOptionDescriptionTypeDef = TypedDict(
    "_RequiredCloudWatchLoggingOptionDescriptionTypeDef", {"LogStreamARN": str, "RoleARN": str}
)
_OptionalCloudWatchLoggingOptionDescriptionTypeDef = TypedDict(
    "_OptionalCloudWatchLoggingOptionDescriptionTypeDef",
    {"CloudWatchLoggingOptionId": str},
    total=False,
)


class CloudWatchLoggingOptionDescriptionTypeDef(
    _RequiredCloudWatchLoggingOptionDescriptionTypeDef,
    _OptionalCloudWatchLoggingOptionDescriptionTypeDef,
):
    pass


InputParallelismTypeDef = TypedDict("InputParallelismTypeDef", {"Count": int}, total=False)

InputLambdaProcessorDescriptionTypeDef = TypedDict(
    "InputLambdaProcessorDescriptionTypeDef", {"ResourceARN": str, "RoleARN": str}, total=False
)

InputProcessingConfigurationDescriptionTypeDef = TypedDict(
    "InputProcessingConfigurationDescriptionTypeDef",
    {"InputLambdaProcessorDescription": InputLambdaProcessorDescriptionTypeDef},
    total=False,
)

InputStartingPositionConfigurationTypeDef = TypedDict(
    "InputStartingPositionConfigurationTypeDef",
    {"InputStartingPosition": Literal["NOW", "TRIM_HORIZON", "LAST_STOPPED_POINT"]},
    total=False,
)

KinesisFirehoseInputDescriptionTypeDef = TypedDict(
    "KinesisFirehoseInputDescriptionTypeDef", {"ResourceARN": str, "RoleARN": str}, total=False
)

KinesisStreamsInputDescriptionTypeDef = TypedDict(
    "KinesisStreamsInputDescriptionTypeDef", {"ResourceARN": str, "RoleARN": str}, total=False
)

InputDescriptionTypeDef = TypedDict(
    "InputDescriptionTypeDef",
    {
        "InputId": str,
        "NamePrefix": str,
        "InAppStreamNames": List[str],
        "InputProcessingConfigurationDescription": InputProcessingConfigurationDescriptionTypeDef,
        "KinesisStreamsInputDescription": KinesisStreamsInputDescriptionTypeDef,
        "KinesisFirehoseInputDescription": KinesisFirehoseInputDescriptionTypeDef,
        "InputSchema": SourceSchemaTypeDef,
        "InputParallelism": InputParallelismTypeDef,
        "InputStartingPositionConfiguration": InputStartingPositionConfigurationTypeDef,
    },
    total=False,
)

KinesisFirehoseOutputDescriptionTypeDef = TypedDict(
    "KinesisFirehoseOutputDescriptionTypeDef", {"ResourceARN": str, "RoleARN": str}, total=False
)

KinesisStreamsOutputDescriptionTypeDef = TypedDict(
    "KinesisStreamsOutputDescriptionTypeDef", {"ResourceARN": str, "RoleARN": str}, total=False
)

LambdaOutputDescriptionTypeDef = TypedDict(
    "LambdaOutputDescriptionTypeDef", {"ResourceARN": str, "RoleARN": str}, total=False
)

OutputDescriptionTypeDef = TypedDict(
    "OutputDescriptionTypeDef",
    {
        "OutputId": str,
        "Name": str,
        "KinesisStreamsOutputDescription": KinesisStreamsOutputDescriptionTypeDef,
        "KinesisFirehoseOutputDescription": KinesisFirehoseOutputDescriptionTypeDef,
        "LambdaOutputDescription": LambdaOutputDescriptionTypeDef,
        "DestinationSchema": DestinationSchemaTypeDef,
    },
    total=False,
)

S3ReferenceDataSourceDescriptionTypeDef = TypedDict(
    "S3ReferenceDataSourceDescriptionTypeDef",
    {"BucketARN": str, "FileKey": str, "ReferenceRoleARN": str},
)

_RequiredReferenceDataSourceDescriptionTypeDef = TypedDict(
    "_RequiredReferenceDataSourceDescriptionTypeDef",
    {
        "ReferenceId": str,
        "TableName": str,
        "S3ReferenceDataSourceDescription": S3ReferenceDataSourceDescriptionTypeDef,
    },
)
_OptionalReferenceDataSourceDescriptionTypeDef = TypedDict(
    "_OptionalReferenceDataSourceDescriptionTypeDef",
    {"ReferenceSchema": SourceSchemaTypeDef},
    total=False,
)


class ReferenceDataSourceDescriptionTypeDef(
    _RequiredReferenceDataSourceDescriptionTypeDef, _OptionalReferenceDataSourceDescriptionTypeDef
):
    pass


_RequiredApplicationDetailTypeDef = TypedDict(
    "_RequiredApplicationDetailTypeDef",
    {
        "ApplicationName": str,
        "ApplicationARN": str,
        "ApplicationStatus": Literal[
            "DELETING", "STARTING", "STOPPING", "READY", "RUNNING", "UPDATING"
        ],
        "ApplicationVersionId": int,
    },
)
_OptionalApplicationDetailTypeDef = TypedDict(
    "_OptionalApplicationDetailTypeDef",
    {
        "ApplicationDescription": str,
        "CreateTimestamp": datetime,
        "LastUpdateTimestamp": datetime,
        "InputDescriptions": List[InputDescriptionTypeDef],
        "OutputDescriptions": List[OutputDescriptionTypeDef],
        "ReferenceDataSourceDescriptions": List[ReferenceDataSourceDescriptionTypeDef],
        "CloudWatchLoggingOptionDescriptions": List[CloudWatchLoggingOptionDescriptionTypeDef],
        "ApplicationCode": str,
    },
    total=False,
)


class ApplicationDetailTypeDef(
    _RequiredApplicationDetailTypeDef, _OptionalApplicationDetailTypeDef
):
    pass


DescribeApplicationResponseTypeDef = TypedDict(
    "DescribeApplicationResponseTypeDef", {"ApplicationDetail": ApplicationDetailTypeDef}
)

DiscoverInputSchemaResponseTypeDef = TypedDict(
    "DiscoverInputSchemaResponseTypeDef",
    {
        "InputSchema": SourceSchemaTypeDef,
        "ParsedInputRecords": List[List[str]],
        "ProcessedInputRecords": List[str],
        "RawInputRecords": List[str],
    },
    total=False,
)

InputConfigurationTypeDef = TypedDict(
    "InputConfigurationTypeDef",
    {"Id": str, "InputStartingPositionConfiguration": InputStartingPositionConfigurationTypeDef},
)

InputLambdaProcessorTypeDef = TypedDict(
    "InputLambdaProcessorTypeDef", {"ResourceARN": str, "RoleARN": str}
)

InputProcessingConfigurationTypeDef = TypedDict(
    "InputProcessingConfigurationTypeDef", {"InputLambdaProcessor": InputLambdaProcessorTypeDef}
)

KinesisFirehoseInputTypeDef = TypedDict(
    "KinesisFirehoseInputTypeDef", {"ResourceARN": str, "RoleARN": str}
)

KinesisStreamsInputTypeDef = TypedDict(
    "KinesisStreamsInputTypeDef", {"ResourceARN": str, "RoleARN": str}
)

_RequiredInputTypeDef = TypedDict(
    "_RequiredInputTypeDef", {"NamePrefix": str, "InputSchema": SourceSchemaTypeDef}
)
_OptionalInputTypeDef = TypedDict(
    "_OptionalInputTypeDef",
    {
        "InputProcessingConfiguration": InputProcessingConfigurationTypeDef,
        "KinesisStreamsInput": KinesisStreamsInputTypeDef,
        "KinesisFirehoseInput": KinesisFirehoseInputTypeDef,
        "InputParallelism": InputParallelismTypeDef,
    },
    total=False,
)


class InputTypeDef(_RequiredInputTypeDef, _OptionalInputTypeDef):
    pass


ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {"ApplicationSummaries": List[ApplicationSummaryTypeDef], "HasMoreApplications": bool},
)

_RequiredTagTypeDef = TypedDict("_RequiredTagTypeDef", {"Key": str})
_OptionalTagTypeDef = TypedDict("_OptionalTagTypeDef", {"Value": str}, total=False)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef]}, total=False
)

KinesisFirehoseOutputTypeDef = TypedDict(
    "KinesisFirehoseOutputTypeDef", {"ResourceARN": str, "RoleARN": str}
)

KinesisStreamsOutputTypeDef = TypedDict(
    "KinesisStreamsOutputTypeDef", {"ResourceARN": str, "RoleARN": str}
)

LambdaOutputTypeDef = TypedDict("LambdaOutputTypeDef", {"ResourceARN": str, "RoleARN": str})

_RequiredOutputTypeDef = TypedDict(
    "_RequiredOutputTypeDef", {"Name": str, "DestinationSchema": DestinationSchemaTypeDef}
)
_OptionalOutputTypeDef = TypedDict(
    "_OptionalOutputTypeDef",
    {
        "KinesisStreamsOutput": KinesisStreamsOutputTypeDef,
        "KinesisFirehoseOutput": KinesisFirehoseOutputTypeDef,
        "LambdaOutput": LambdaOutputTypeDef,
    },
    total=False,
)


class OutputTypeDef(_RequiredOutputTypeDef, _OptionalOutputTypeDef):
    pass


S3ReferenceDataSourceTypeDef = TypedDict(
    "S3ReferenceDataSourceTypeDef", {"BucketARN": str, "FileKey": str, "ReferenceRoleARN": str}
)

_RequiredReferenceDataSourceTypeDef = TypedDict(
    "_RequiredReferenceDataSourceTypeDef",
    {"TableName": str, "ReferenceSchema": SourceSchemaTypeDef},
)
_OptionalReferenceDataSourceTypeDef = TypedDict(
    "_OptionalReferenceDataSourceTypeDef",
    {"S3ReferenceDataSource": S3ReferenceDataSourceTypeDef},
    total=False,
)


class ReferenceDataSourceTypeDef(
    _RequiredReferenceDataSourceTypeDef, _OptionalReferenceDataSourceTypeDef
):
    pass


S3ConfigurationTypeDef = TypedDict(
    "S3ConfigurationTypeDef", {"RoleARN": str, "BucketARN": str, "FileKey": str}
)
