"""
Main interface for kinesisanalyticsv2 service type definitions.

Usage::

    from mypy_boto3.kinesisanalyticsv2.type_defs import CloudWatchLoggingOptionDescriptionTypeDef

    data: CloudWatchLoggingOptionDescriptionTypeDef = {...}
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
    "CloudWatchLoggingOptionDescriptionTypeDef",
    "AddApplicationCloudWatchLoggingOptionResponseTypeDef",
    "InputLambdaProcessorDescriptionTypeDef",
    "InputProcessingConfigurationDescriptionTypeDef",
    "AddApplicationInputProcessingConfigurationResponseTypeDef",
    "InputParallelismTypeDef",
    "InputStartingPositionConfigurationTypeDef",
    "KinesisFirehoseInputDescriptionTypeDef",
    "KinesisStreamsInputDescriptionTypeDef",
    "RecordColumnTypeDef",
    "CSVMappingParametersTypeDef",
    "JSONMappingParametersTypeDef",
    "MappingParametersTypeDef",
    "RecordFormatTypeDef",
    "SourceSchemaTypeDef",
    "InputDescriptionTypeDef",
    "AddApplicationInputResponseTypeDef",
    "DestinationSchemaTypeDef",
    "KinesisFirehoseOutputDescriptionTypeDef",
    "KinesisStreamsOutputDescriptionTypeDef",
    "LambdaOutputDescriptionTypeDef",
    "OutputDescriptionTypeDef",
    "AddApplicationOutputResponseTypeDef",
    "S3ReferenceDataSourceDescriptionTypeDef",
    "ReferenceDataSourceDescriptionTypeDef",
    "AddApplicationReferenceDataSourceResponseTypeDef",
    "VpcConfigurationDescriptionTypeDef",
    "AddApplicationVpcConfigurationResponseTypeDef",
    "S3ContentLocationTypeDef",
    "CodeContentTypeDef",
    "ApplicationCodeConfigurationTypeDef",
    "ApplicationSnapshotConfigurationTypeDef",
    "PropertyGroupTypeDef",
    "EnvironmentPropertiesTypeDef",
    "CheckpointConfigurationTypeDef",
    "MonitoringConfigurationTypeDef",
    "ParallelismConfigurationTypeDef",
    "FlinkApplicationConfigurationTypeDef",
    "InputLambdaProcessorTypeDef",
    "InputProcessingConfigurationTypeDef",
    "KinesisFirehoseInputTypeDef",
    "KinesisStreamsInputTypeDef",
    "InputTypeDef",
    "KinesisFirehoseOutputTypeDef",
    "KinesisStreamsOutputTypeDef",
    "LambdaOutputTypeDef",
    "OutputTypeDef",
    "S3ReferenceDataSourceTypeDef",
    "ReferenceDataSourceTypeDef",
    "SqlApplicationConfigurationTypeDef",
    "VpcConfigurationTypeDef",
    "ApplicationConfigurationTypeDef",
    "S3ContentLocationUpdateTypeDef",
    "CodeContentUpdateTypeDef",
    "ApplicationCodeConfigurationUpdateTypeDef",
    "ApplicationSnapshotConfigurationUpdateTypeDef",
    "EnvironmentPropertyUpdatesTypeDef",
    "CheckpointConfigurationUpdateTypeDef",
    "MonitoringConfigurationUpdateTypeDef",
    "ParallelismConfigurationUpdateTypeDef",
    "FlinkApplicationConfigurationUpdateTypeDef",
    "InputParallelismUpdateTypeDef",
    "InputLambdaProcessorUpdateTypeDef",
    "InputProcessingConfigurationUpdateTypeDef",
    "InputSchemaUpdateTypeDef",
    "KinesisFirehoseInputUpdateTypeDef",
    "KinesisStreamsInputUpdateTypeDef",
    "InputUpdateTypeDef",
    "KinesisFirehoseOutputUpdateTypeDef",
    "KinesisStreamsOutputUpdateTypeDef",
    "LambdaOutputUpdateTypeDef",
    "OutputUpdateTypeDef",
    "S3ReferenceDataSourceUpdateTypeDef",
    "ReferenceDataSourceUpdateTypeDef",
    "SqlApplicationConfigurationUpdateTypeDef",
    "VpcConfigurationUpdateTypeDef",
    "ApplicationConfigurationUpdateTypeDef",
    "CloudWatchLoggingOptionTypeDef",
    "CloudWatchLoggingOptionUpdateTypeDef",
    "S3ApplicationCodeLocationDescriptionTypeDef",
    "CodeContentDescriptionTypeDef",
    "ApplicationCodeConfigurationDescriptionTypeDef",
    "ApplicationSnapshotConfigurationDescriptionTypeDef",
    "EnvironmentPropertyDescriptionsTypeDef",
    "CheckpointConfigurationDescriptionTypeDef",
    "MonitoringConfigurationDescriptionTypeDef",
    "ParallelismConfigurationDescriptionTypeDef",
    "FlinkApplicationConfigurationDescriptionTypeDef",
    "ApplicationRestoreConfigurationTypeDef",
    "RunConfigurationDescriptionTypeDef",
    "SqlApplicationConfigurationDescriptionTypeDef",
    "ApplicationConfigurationDescriptionTypeDef",
    "ApplicationDetailTypeDef",
    "CreateApplicationResponseTypeDef",
    "DeleteApplicationCloudWatchLoggingOptionResponseTypeDef",
    "DeleteApplicationInputProcessingConfigurationResponseTypeDef",
    "DeleteApplicationOutputResponseTypeDef",
    "DeleteApplicationReferenceDataSourceResponseTypeDef",
    "DeleteApplicationVpcConfigurationResponseTypeDef",
    "DescribeApplicationResponseTypeDef",
    "SnapshotDetailsTypeDef",
    "DescribeApplicationSnapshotResponseTypeDef",
    "DiscoverInputSchemaResponseTypeDef",
    "ListApplicationSnapshotsResponseTypeDef",
    "ApplicationSummaryTypeDef",
    "ListApplicationsResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "FlinkRunConfigurationTypeDef",
    "SqlRunConfigurationTypeDef",
    "RunConfigurationTypeDef",
    "RunConfigurationUpdateTypeDef",
    "S3ConfigurationTypeDef",
    "UpdateApplicationResponseTypeDef",
)

_RequiredCloudWatchLoggingOptionDescriptionTypeDef = TypedDict(
    "_RequiredCloudWatchLoggingOptionDescriptionTypeDef", {"LogStreamARN": str}
)
_OptionalCloudWatchLoggingOptionDescriptionTypeDef = TypedDict(
    "_OptionalCloudWatchLoggingOptionDescriptionTypeDef",
    {"CloudWatchLoggingOptionId": str, "RoleARN": str},
    total=False,
)


class CloudWatchLoggingOptionDescriptionTypeDef(
    _RequiredCloudWatchLoggingOptionDescriptionTypeDef,
    _OptionalCloudWatchLoggingOptionDescriptionTypeDef,
):
    pass


AddApplicationCloudWatchLoggingOptionResponseTypeDef = TypedDict(
    "AddApplicationCloudWatchLoggingOptionResponseTypeDef",
    {
        "ApplicationARN": str,
        "ApplicationVersionId": int,
        "CloudWatchLoggingOptionDescriptions": List[CloudWatchLoggingOptionDescriptionTypeDef],
    },
    total=False,
)

_RequiredInputLambdaProcessorDescriptionTypeDef = TypedDict(
    "_RequiredInputLambdaProcessorDescriptionTypeDef", {"ResourceARN": str}
)
_OptionalInputLambdaProcessorDescriptionTypeDef = TypedDict(
    "_OptionalInputLambdaProcessorDescriptionTypeDef", {"RoleARN": str}, total=False
)


class InputLambdaProcessorDescriptionTypeDef(
    _RequiredInputLambdaProcessorDescriptionTypeDef, _OptionalInputLambdaProcessorDescriptionTypeDef
):
    pass


InputProcessingConfigurationDescriptionTypeDef = TypedDict(
    "InputProcessingConfigurationDescriptionTypeDef",
    {"InputLambdaProcessorDescription": InputLambdaProcessorDescriptionTypeDef},
    total=False,
)

AddApplicationInputProcessingConfigurationResponseTypeDef = TypedDict(
    "AddApplicationInputProcessingConfigurationResponseTypeDef",
    {
        "ApplicationARN": str,
        "ApplicationVersionId": int,
        "InputId": str,
        "InputProcessingConfigurationDescription": InputProcessingConfigurationDescriptionTypeDef,
    },
    total=False,
)

InputParallelismTypeDef = TypedDict("InputParallelismTypeDef", {"Count": int}, total=False)

InputStartingPositionConfigurationTypeDef = TypedDict(
    "InputStartingPositionConfigurationTypeDef",
    {"InputStartingPosition": Literal["NOW", "TRIM_HORIZON", "LAST_STOPPED_POINT"]},
    total=False,
)

_RequiredKinesisFirehoseInputDescriptionTypeDef = TypedDict(
    "_RequiredKinesisFirehoseInputDescriptionTypeDef", {"ResourceARN": str}
)
_OptionalKinesisFirehoseInputDescriptionTypeDef = TypedDict(
    "_OptionalKinesisFirehoseInputDescriptionTypeDef", {"RoleARN": str}, total=False
)


class KinesisFirehoseInputDescriptionTypeDef(
    _RequiredKinesisFirehoseInputDescriptionTypeDef, _OptionalKinesisFirehoseInputDescriptionTypeDef
):
    pass


_RequiredKinesisStreamsInputDescriptionTypeDef = TypedDict(
    "_RequiredKinesisStreamsInputDescriptionTypeDef", {"ResourceARN": str}
)
_OptionalKinesisStreamsInputDescriptionTypeDef = TypedDict(
    "_OptionalKinesisStreamsInputDescriptionTypeDef", {"RoleARN": str}, total=False
)


class KinesisStreamsInputDescriptionTypeDef(
    _RequiredKinesisStreamsInputDescriptionTypeDef, _OptionalKinesisStreamsInputDescriptionTypeDef
):
    pass


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


_RequiredSourceSchemaTypeDef = TypedDict(
    "_RequiredSourceSchemaTypeDef",
    {"RecordFormat": RecordFormatTypeDef, "RecordColumns": List[RecordColumnTypeDef]},
)
_OptionalSourceSchemaTypeDef = TypedDict(
    "_OptionalSourceSchemaTypeDef", {"RecordEncoding": str}, total=False
)


class SourceSchemaTypeDef(_RequiredSourceSchemaTypeDef, _OptionalSourceSchemaTypeDef):
    pass


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

AddApplicationInputResponseTypeDef = TypedDict(
    "AddApplicationInputResponseTypeDef",
    {
        "ApplicationARN": str,
        "ApplicationVersionId": int,
        "InputDescriptions": List[InputDescriptionTypeDef],
    },
    total=False,
)

DestinationSchemaTypeDef = TypedDict(
    "DestinationSchemaTypeDef", {"RecordFormatType": Literal["JSON", "CSV"]}
)

_RequiredKinesisFirehoseOutputDescriptionTypeDef = TypedDict(
    "_RequiredKinesisFirehoseOutputDescriptionTypeDef", {"ResourceARN": str}
)
_OptionalKinesisFirehoseOutputDescriptionTypeDef = TypedDict(
    "_OptionalKinesisFirehoseOutputDescriptionTypeDef", {"RoleARN": str}, total=False
)


class KinesisFirehoseOutputDescriptionTypeDef(
    _RequiredKinesisFirehoseOutputDescriptionTypeDef,
    _OptionalKinesisFirehoseOutputDescriptionTypeDef,
):
    pass


_RequiredKinesisStreamsOutputDescriptionTypeDef = TypedDict(
    "_RequiredKinesisStreamsOutputDescriptionTypeDef", {"ResourceARN": str}
)
_OptionalKinesisStreamsOutputDescriptionTypeDef = TypedDict(
    "_OptionalKinesisStreamsOutputDescriptionTypeDef", {"RoleARN": str}, total=False
)


class KinesisStreamsOutputDescriptionTypeDef(
    _RequiredKinesisStreamsOutputDescriptionTypeDef, _OptionalKinesisStreamsOutputDescriptionTypeDef
):
    pass


_RequiredLambdaOutputDescriptionTypeDef = TypedDict(
    "_RequiredLambdaOutputDescriptionTypeDef", {"ResourceARN": str}
)
_OptionalLambdaOutputDescriptionTypeDef = TypedDict(
    "_OptionalLambdaOutputDescriptionTypeDef", {"RoleARN": str}, total=False
)


class LambdaOutputDescriptionTypeDef(
    _RequiredLambdaOutputDescriptionTypeDef, _OptionalLambdaOutputDescriptionTypeDef
):
    pass


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

AddApplicationOutputResponseTypeDef = TypedDict(
    "AddApplicationOutputResponseTypeDef",
    {
        "ApplicationARN": str,
        "ApplicationVersionId": int,
        "OutputDescriptions": List[OutputDescriptionTypeDef],
    },
    total=False,
)

_RequiredS3ReferenceDataSourceDescriptionTypeDef = TypedDict(
    "_RequiredS3ReferenceDataSourceDescriptionTypeDef", {"BucketARN": str, "FileKey": str}
)
_OptionalS3ReferenceDataSourceDescriptionTypeDef = TypedDict(
    "_OptionalS3ReferenceDataSourceDescriptionTypeDef", {"ReferenceRoleARN": str}, total=False
)


class S3ReferenceDataSourceDescriptionTypeDef(
    _RequiredS3ReferenceDataSourceDescriptionTypeDef,
    _OptionalS3ReferenceDataSourceDescriptionTypeDef,
):
    pass


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


AddApplicationReferenceDataSourceResponseTypeDef = TypedDict(
    "AddApplicationReferenceDataSourceResponseTypeDef",
    {
        "ApplicationARN": str,
        "ApplicationVersionId": int,
        "ReferenceDataSourceDescriptions": List[ReferenceDataSourceDescriptionTypeDef],
    },
    total=False,
)

VpcConfigurationDescriptionTypeDef = TypedDict(
    "VpcConfigurationDescriptionTypeDef",
    {
        "VpcConfigurationId": str,
        "VpcId": str,
        "SubnetIds": List[str],
        "SecurityGroupIds": List[str],
    },
)

AddApplicationVpcConfigurationResponseTypeDef = TypedDict(
    "AddApplicationVpcConfigurationResponseTypeDef",
    {
        "ApplicationARN": str,
        "ApplicationVersionId": int,
        "VpcConfigurationDescription": VpcConfigurationDescriptionTypeDef,
    },
    total=False,
)

_RequiredS3ContentLocationTypeDef = TypedDict(
    "_RequiredS3ContentLocationTypeDef", {"BucketARN": str, "FileKey": str}
)
_OptionalS3ContentLocationTypeDef = TypedDict(
    "_OptionalS3ContentLocationTypeDef", {"ObjectVersion": str}, total=False
)


class S3ContentLocationTypeDef(
    _RequiredS3ContentLocationTypeDef, _OptionalS3ContentLocationTypeDef
):
    pass


CodeContentTypeDef = TypedDict(
    "CodeContentTypeDef",
    {
        "TextContent": str,
        "ZipFileContent": Union[bytes, IO],
        "S3ContentLocation": S3ContentLocationTypeDef,
    },
    total=False,
)

_RequiredApplicationCodeConfigurationTypeDef = TypedDict(
    "_RequiredApplicationCodeConfigurationTypeDef",
    {"CodeContentType": Literal["PLAINTEXT", "ZIPFILE"]},
)
_OptionalApplicationCodeConfigurationTypeDef = TypedDict(
    "_OptionalApplicationCodeConfigurationTypeDef", {"CodeContent": CodeContentTypeDef}, total=False
)


class ApplicationCodeConfigurationTypeDef(
    _RequiredApplicationCodeConfigurationTypeDef, _OptionalApplicationCodeConfigurationTypeDef
):
    pass


ApplicationSnapshotConfigurationTypeDef = TypedDict(
    "ApplicationSnapshotConfigurationTypeDef", {"SnapshotsEnabled": bool}
)

PropertyGroupTypeDef = TypedDict(
    "PropertyGroupTypeDef", {"PropertyGroupId": str, "PropertyMap": Dict[str, str]}
)

EnvironmentPropertiesTypeDef = TypedDict(
    "EnvironmentPropertiesTypeDef", {"PropertyGroups": List[PropertyGroupTypeDef]}
)

_RequiredCheckpointConfigurationTypeDef = TypedDict(
    "_RequiredCheckpointConfigurationTypeDef", {"ConfigurationType": Literal["DEFAULT", "CUSTOM"]}
)
_OptionalCheckpointConfigurationTypeDef = TypedDict(
    "_OptionalCheckpointConfigurationTypeDef",
    {"CheckpointingEnabled": bool, "CheckpointInterval": int, "MinPauseBetweenCheckpoints": int},
    total=False,
)


class CheckpointConfigurationTypeDef(
    _RequiredCheckpointConfigurationTypeDef, _OptionalCheckpointConfigurationTypeDef
):
    pass


_RequiredMonitoringConfigurationTypeDef = TypedDict(
    "_RequiredMonitoringConfigurationTypeDef", {"ConfigurationType": Literal["DEFAULT", "CUSTOM"]}
)
_OptionalMonitoringConfigurationTypeDef = TypedDict(
    "_OptionalMonitoringConfigurationTypeDef",
    {
        "MetricsLevel": Literal["APPLICATION", "TASK", "OPERATOR", "PARALLELISM"],
        "LogLevel": Literal["INFO", "WARN", "ERROR", "DEBUG"],
    },
    total=False,
)


class MonitoringConfigurationTypeDef(
    _RequiredMonitoringConfigurationTypeDef, _OptionalMonitoringConfigurationTypeDef
):
    pass


_RequiredParallelismConfigurationTypeDef = TypedDict(
    "_RequiredParallelismConfigurationTypeDef", {"ConfigurationType": Literal["DEFAULT", "CUSTOM"]}
)
_OptionalParallelismConfigurationTypeDef = TypedDict(
    "_OptionalParallelismConfigurationTypeDef",
    {"Parallelism": int, "ParallelismPerKPU": int, "AutoScalingEnabled": bool},
    total=False,
)


class ParallelismConfigurationTypeDef(
    _RequiredParallelismConfigurationTypeDef, _OptionalParallelismConfigurationTypeDef
):
    pass


FlinkApplicationConfigurationTypeDef = TypedDict(
    "FlinkApplicationConfigurationTypeDef",
    {
        "CheckpointConfiguration": CheckpointConfigurationTypeDef,
        "MonitoringConfiguration": MonitoringConfigurationTypeDef,
        "ParallelismConfiguration": ParallelismConfigurationTypeDef,
    },
    total=False,
)

InputLambdaProcessorTypeDef = TypedDict("InputLambdaProcessorTypeDef", {"ResourceARN": str})

InputProcessingConfigurationTypeDef = TypedDict(
    "InputProcessingConfigurationTypeDef", {"InputLambdaProcessor": InputLambdaProcessorTypeDef}
)

KinesisFirehoseInputTypeDef = TypedDict("KinesisFirehoseInputTypeDef", {"ResourceARN": str})

KinesisStreamsInputTypeDef = TypedDict("KinesisStreamsInputTypeDef", {"ResourceARN": str})

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


KinesisFirehoseOutputTypeDef = TypedDict("KinesisFirehoseOutputTypeDef", {"ResourceARN": str})

KinesisStreamsOutputTypeDef = TypedDict("KinesisStreamsOutputTypeDef", {"ResourceARN": str})

LambdaOutputTypeDef = TypedDict("LambdaOutputTypeDef", {"ResourceARN": str})

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
    "S3ReferenceDataSourceTypeDef", {"BucketARN": str, "FileKey": str}, total=False
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


SqlApplicationConfigurationTypeDef = TypedDict(
    "SqlApplicationConfigurationTypeDef",
    {
        "Inputs": List[InputTypeDef],
        "Outputs": List[OutputTypeDef],
        "ReferenceDataSources": List[ReferenceDataSourceTypeDef],
    },
    total=False,
)

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef", {"SubnetIds": List[str], "SecurityGroupIds": List[str]}
)

_RequiredApplicationConfigurationTypeDef = TypedDict(
    "_RequiredApplicationConfigurationTypeDef",
    {"ApplicationCodeConfiguration": ApplicationCodeConfigurationTypeDef},
)
_OptionalApplicationConfigurationTypeDef = TypedDict(
    "_OptionalApplicationConfigurationTypeDef",
    {
        "SqlApplicationConfiguration": SqlApplicationConfigurationTypeDef,
        "FlinkApplicationConfiguration": FlinkApplicationConfigurationTypeDef,
        "EnvironmentProperties": EnvironmentPropertiesTypeDef,
        "ApplicationSnapshotConfiguration": ApplicationSnapshotConfigurationTypeDef,
        "VpcConfigurations": List[VpcConfigurationTypeDef],
    },
    total=False,
)


class ApplicationConfigurationTypeDef(
    _RequiredApplicationConfigurationTypeDef, _OptionalApplicationConfigurationTypeDef
):
    pass


S3ContentLocationUpdateTypeDef = TypedDict(
    "S3ContentLocationUpdateTypeDef",
    {"BucketARNUpdate": str, "FileKeyUpdate": str, "ObjectVersionUpdate": str},
    total=False,
)

CodeContentUpdateTypeDef = TypedDict(
    "CodeContentUpdateTypeDef",
    {
        "TextContentUpdate": str,
        "ZipFileContentUpdate": Union[bytes, IO],
        "S3ContentLocationUpdate": S3ContentLocationUpdateTypeDef,
    },
    total=False,
)

ApplicationCodeConfigurationUpdateTypeDef = TypedDict(
    "ApplicationCodeConfigurationUpdateTypeDef",
    {
        "CodeContentTypeUpdate": Literal["PLAINTEXT", "ZIPFILE"],
        "CodeContentUpdate": CodeContentUpdateTypeDef,
    },
    total=False,
)

ApplicationSnapshotConfigurationUpdateTypeDef = TypedDict(
    "ApplicationSnapshotConfigurationUpdateTypeDef", {"SnapshotsEnabledUpdate": bool}
)

EnvironmentPropertyUpdatesTypeDef = TypedDict(
    "EnvironmentPropertyUpdatesTypeDef", {"PropertyGroups": List[PropertyGroupTypeDef]}
)

CheckpointConfigurationUpdateTypeDef = TypedDict(
    "CheckpointConfigurationUpdateTypeDef",
    {
        "ConfigurationTypeUpdate": Literal["DEFAULT", "CUSTOM"],
        "CheckpointingEnabledUpdate": bool,
        "CheckpointIntervalUpdate": int,
        "MinPauseBetweenCheckpointsUpdate": int,
    },
    total=False,
)

MonitoringConfigurationUpdateTypeDef = TypedDict(
    "MonitoringConfigurationUpdateTypeDef",
    {
        "ConfigurationTypeUpdate": Literal["DEFAULT", "CUSTOM"],
        "MetricsLevelUpdate": Literal["APPLICATION", "TASK", "OPERATOR", "PARALLELISM"],
        "LogLevelUpdate": Literal["INFO", "WARN", "ERROR", "DEBUG"],
    },
    total=False,
)

ParallelismConfigurationUpdateTypeDef = TypedDict(
    "ParallelismConfigurationUpdateTypeDef",
    {
        "ConfigurationTypeUpdate": Literal["DEFAULT", "CUSTOM"],
        "ParallelismUpdate": int,
        "ParallelismPerKPUUpdate": int,
        "AutoScalingEnabledUpdate": bool,
    },
    total=False,
)

FlinkApplicationConfigurationUpdateTypeDef = TypedDict(
    "FlinkApplicationConfigurationUpdateTypeDef",
    {
        "CheckpointConfigurationUpdate": CheckpointConfigurationUpdateTypeDef,
        "MonitoringConfigurationUpdate": MonitoringConfigurationUpdateTypeDef,
        "ParallelismConfigurationUpdate": ParallelismConfigurationUpdateTypeDef,
    },
    total=False,
)

InputParallelismUpdateTypeDef = TypedDict("InputParallelismUpdateTypeDef", {"CountUpdate": int})

InputLambdaProcessorUpdateTypeDef = TypedDict(
    "InputLambdaProcessorUpdateTypeDef", {"ResourceARNUpdate": str}
)

InputProcessingConfigurationUpdateTypeDef = TypedDict(
    "InputProcessingConfigurationUpdateTypeDef",
    {"InputLambdaProcessorUpdate": InputLambdaProcessorUpdateTypeDef},
)

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
    "KinesisFirehoseInputUpdateTypeDef", {"ResourceARNUpdate": str}
)

KinesisStreamsInputUpdateTypeDef = TypedDict(
    "KinesisStreamsInputUpdateTypeDef", {"ResourceARNUpdate": str}
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


KinesisFirehoseOutputUpdateTypeDef = TypedDict(
    "KinesisFirehoseOutputUpdateTypeDef", {"ResourceARNUpdate": str}
)

KinesisStreamsOutputUpdateTypeDef = TypedDict(
    "KinesisStreamsOutputUpdateTypeDef", {"ResourceARNUpdate": str}
)

LambdaOutputUpdateTypeDef = TypedDict("LambdaOutputUpdateTypeDef", {"ResourceARNUpdate": str})

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
    {"BucketARNUpdate": str, "FileKeyUpdate": str},
    total=False,
)

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


SqlApplicationConfigurationUpdateTypeDef = TypedDict(
    "SqlApplicationConfigurationUpdateTypeDef",
    {
        "InputUpdates": List[InputUpdateTypeDef],
        "OutputUpdates": List[OutputUpdateTypeDef],
        "ReferenceDataSourceUpdates": List[ReferenceDataSourceUpdateTypeDef],
    },
    total=False,
)

_RequiredVpcConfigurationUpdateTypeDef = TypedDict(
    "_RequiredVpcConfigurationUpdateTypeDef", {"VpcConfigurationId": str}
)
_OptionalVpcConfigurationUpdateTypeDef = TypedDict(
    "_OptionalVpcConfigurationUpdateTypeDef",
    {"SubnetIdUpdates": List[str], "SecurityGroupIdUpdates": List[str]},
    total=False,
)


class VpcConfigurationUpdateTypeDef(
    _RequiredVpcConfigurationUpdateTypeDef, _OptionalVpcConfigurationUpdateTypeDef
):
    pass


ApplicationConfigurationUpdateTypeDef = TypedDict(
    "ApplicationConfigurationUpdateTypeDef",
    {
        "SqlApplicationConfigurationUpdate": SqlApplicationConfigurationUpdateTypeDef,
        "ApplicationCodeConfigurationUpdate": ApplicationCodeConfigurationUpdateTypeDef,
        "FlinkApplicationConfigurationUpdate": FlinkApplicationConfigurationUpdateTypeDef,
        "EnvironmentPropertyUpdates": EnvironmentPropertyUpdatesTypeDef,
        "ApplicationSnapshotConfigurationUpdate": ApplicationSnapshotConfigurationUpdateTypeDef,
        "VpcConfigurationUpdates": List[VpcConfigurationUpdateTypeDef],
    },
    total=False,
)

CloudWatchLoggingOptionTypeDef = TypedDict("CloudWatchLoggingOptionTypeDef", {"LogStreamARN": str})

_RequiredCloudWatchLoggingOptionUpdateTypeDef = TypedDict(
    "_RequiredCloudWatchLoggingOptionUpdateTypeDef", {"CloudWatchLoggingOptionId": str}
)
_OptionalCloudWatchLoggingOptionUpdateTypeDef = TypedDict(
    "_OptionalCloudWatchLoggingOptionUpdateTypeDef", {"LogStreamARNUpdate": str}, total=False
)


class CloudWatchLoggingOptionUpdateTypeDef(
    _RequiredCloudWatchLoggingOptionUpdateTypeDef, _OptionalCloudWatchLoggingOptionUpdateTypeDef
):
    pass


_RequiredS3ApplicationCodeLocationDescriptionTypeDef = TypedDict(
    "_RequiredS3ApplicationCodeLocationDescriptionTypeDef", {"BucketARN": str, "FileKey": str}
)
_OptionalS3ApplicationCodeLocationDescriptionTypeDef = TypedDict(
    "_OptionalS3ApplicationCodeLocationDescriptionTypeDef", {"ObjectVersion": str}, total=False
)


class S3ApplicationCodeLocationDescriptionTypeDef(
    _RequiredS3ApplicationCodeLocationDescriptionTypeDef,
    _OptionalS3ApplicationCodeLocationDescriptionTypeDef,
):
    pass


CodeContentDescriptionTypeDef = TypedDict(
    "CodeContentDescriptionTypeDef",
    {
        "TextContent": str,
        "CodeMD5": str,
        "CodeSize": int,
        "S3ApplicationCodeLocationDescription": S3ApplicationCodeLocationDescriptionTypeDef,
    },
    total=False,
)

_RequiredApplicationCodeConfigurationDescriptionTypeDef = TypedDict(
    "_RequiredApplicationCodeConfigurationDescriptionTypeDef",
    {"CodeContentType": Literal["PLAINTEXT", "ZIPFILE"]},
)
_OptionalApplicationCodeConfigurationDescriptionTypeDef = TypedDict(
    "_OptionalApplicationCodeConfigurationDescriptionTypeDef",
    {"CodeContentDescription": CodeContentDescriptionTypeDef},
    total=False,
)


class ApplicationCodeConfigurationDescriptionTypeDef(
    _RequiredApplicationCodeConfigurationDescriptionTypeDef,
    _OptionalApplicationCodeConfigurationDescriptionTypeDef,
):
    pass


ApplicationSnapshotConfigurationDescriptionTypeDef = TypedDict(
    "ApplicationSnapshotConfigurationDescriptionTypeDef", {"SnapshotsEnabled": bool}
)

EnvironmentPropertyDescriptionsTypeDef = TypedDict(
    "EnvironmentPropertyDescriptionsTypeDef",
    {"PropertyGroupDescriptions": List[PropertyGroupTypeDef]},
    total=False,
)

CheckpointConfigurationDescriptionTypeDef = TypedDict(
    "CheckpointConfigurationDescriptionTypeDef",
    {
        "ConfigurationType": Literal["DEFAULT", "CUSTOM"],
        "CheckpointingEnabled": bool,
        "CheckpointInterval": int,
        "MinPauseBetweenCheckpoints": int,
    },
    total=False,
)

MonitoringConfigurationDescriptionTypeDef = TypedDict(
    "MonitoringConfigurationDescriptionTypeDef",
    {
        "ConfigurationType": Literal["DEFAULT", "CUSTOM"],
        "MetricsLevel": Literal["APPLICATION", "TASK", "OPERATOR", "PARALLELISM"],
        "LogLevel": Literal["INFO", "WARN", "ERROR", "DEBUG"],
    },
    total=False,
)

ParallelismConfigurationDescriptionTypeDef = TypedDict(
    "ParallelismConfigurationDescriptionTypeDef",
    {
        "ConfigurationType": Literal["DEFAULT", "CUSTOM"],
        "Parallelism": int,
        "ParallelismPerKPU": int,
        "CurrentParallelism": int,
        "AutoScalingEnabled": bool,
    },
    total=False,
)

FlinkApplicationConfigurationDescriptionTypeDef = TypedDict(
    "FlinkApplicationConfigurationDescriptionTypeDef",
    {
        "CheckpointConfigurationDescription": CheckpointConfigurationDescriptionTypeDef,
        "MonitoringConfigurationDescription": MonitoringConfigurationDescriptionTypeDef,
        "ParallelismConfigurationDescription": ParallelismConfigurationDescriptionTypeDef,
        "JobPlanDescription": str,
    },
    total=False,
)

_RequiredApplicationRestoreConfigurationTypeDef = TypedDict(
    "_RequiredApplicationRestoreConfigurationTypeDef",
    {
        "ApplicationRestoreType": Literal[
            "SKIP_RESTORE_FROM_SNAPSHOT",
            "RESTORE_FROM_LATEST_SNAPSHOT",
            "RESTORE_FROM_CUSTOM_SNAPSHOT",
        ]
    },
)
_OptionalApplicationRestoreConfigurationTypeDef = TypedDict(
    "_OptionalApplicationRestoreConfigurationTypeDef", {"SnapshotName": str}, total=False
)


class ApplicationRestoreConfigurationTypeDef(
    _RequiredApplicationRestoreConfigurationTypeDef, _OptionalApplicationRestoreConfigurationTypeDef
):
    pass


RunConfigurationDescriptionTypeDef = TypedDict(
    "RunConfigurationDescriptionTypeDef",
    {"ApplicationRestoreConfigurationDescription": ApplicationRestoreConfigurationTypeDef},
    total=False,
)

SqlApplicationConfigurationDescriptionTypeDef = TypedDict(
    "SqlApplicationConfigurationDescriptionTypeDef",
    {
        "InputDescriptions": List[InputDescriptionTypeDef],
        "OutputDescriptions": List[OutputDescriptionTypeDef],
        "ReferenceDataSourceDescriptions": List[ReferenceDataSourceDescriptionTypeDef],
    },
    total=False,
)

ApplicationConfigurationDescriptionTypeDef = TypedDict(
    "ApplicationConfigurationDescriptionTypeDef",
    {
        "SqlApplicationConfigurationDescription": SqlApplicationConfigurationDescriptionTypeDef,
        "ApplicationCodeConfigurationDescription": ApplicationCodeConfigurationDescriptionTypeDef,
        "RunConfigurationDescription": RunConfigurationDescriptionTypeDef,
        "FlinkApplicationConfigurationDescription": FlinkApplicationConfigurationDescriptionTypeDef,
        "EnvironmentPropertyDescriptions": EnvironmentPropertyDescriptionsTypeDef,
        "ApplicationSnapshotConfigurationDescription": ApplicationSnapshotConfigurationDescriptionTypeDef,
        "VpcConfigurationDescriptions": List[VpcConfigurationDescriptionTypeDef],
    },
    total=False,
)

_RequiredApplicationDetailTypeDef = TypedDict(
    "_RequiredApplicationDetailTypeDef",
    {
        "ApplicationARN": str,
        "ApplicationName": str,
        "RuntimeEnvironment": Literal["SQL-1_0", "FLINK-1_6", "FLINK-1_8"],
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
        "ServiceExecutionRole": str,
        "CreateTimestamp": datetime,
        "LastUpdateTimestamp": datetime,
        "ApplicationConfigurationDescription": ApplicationConfigurationDescriptionTypeDef,
        "CloudWatchLoggingOptionDescriptions": List[CloudWatchLoggingOptionDescriptionTypeDef],
    },
    total=False,
)


class ApplicationDetailTypeDef(
    _RequiredApplicationDetailTypeDef, _OptionalApplicationDetailTypeDef
):
    pass


CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef", {"ApplicationDetail": ApplicationDetailTypeDef}
)

DeleteApplicationCloudWatchLoggingOptionResponseTypeDef = TypedDict(
    "DeleteApplicationCloudWatchLoggingOptionResponseTypeDef",
    {
        "ApplicationARN": str,
        "ApplicationVersionId": int,
        "CloudWatchLoggingOptionDescriptions": List[CloudWatchLoggingOptionDescriptionTypeDef],
    },
    total=False,
)

DeleteApplicationInputProcessingConfigurationResponseTypeDef = TypedDict(
    "DeleteApplicationInputProcessingConfigurationResponseTypeDef",
    {"ApplicationARN": str, "ApplicationVersionId": int},
    total=False,
)

DeleteApplicationOutputResponseTypeDef = TypedDict(
    "DeleteApplicationOutputResponseTypeDef",
    {"ApplicationARN": str, "ApplicationVersionId": int},
    total=False,
)

DeleteApplicationReferenceDataSourceResponseTypeDef = TypedDict(
    "DeleteApplicationReferenceDataSourceResponseTypeDef",
    {"ApplicationARN": str, "ApplicationVersionId": int},
    total=False,
)

DeleteApplicationVpcConfigurationResponseTypeDef = TypedDict(
    "DeleteApplicationVpcConfigurationResponseTypeDef",
    {"ApplicationARN": str, "ApplicationVersionId": int},
    total=False,
)

DescribeApplicationResponseTypeDef = TypedDict(
    "DescribeApplicationResponseTypeDef", {"ApplicationDetail": ApplicationDetailTypeDef}
)

_RequiredSnapshotDetailsTypeDef = TypedDict(
    "_RequiredSnapshotDetailsTypeDef",
    {
        "SnapshotName": str,
        "SnapshotStatus": Literal["CREATING", "READY", "DELETING", "FAILED"],
        "ApplicationVersionId": int,
    },
)
_OptionalSnapshotDetailsTypeDef = TypedDict(
    "_OptionalSnapshotDetailsTypeDef", {"SnapshotCreationTimestamp": datetime}, total=False
)


class SnapshotDetailsTypeDef(_RequiredSnapshotDetailsTypeDef, _OptionalSnapshotDetailsTypeDef):
    pass


DescribeApplicationSnapshotResponseTypeDef = TypedDict(
    "DescribeApplicationSnapshotResponseTypeDef", {"SnapshotDetails": SnapshotDetailsTypeDef}
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

ListApplicationSnapshotsResponseTypeDef = TypedDict(
    "ListApplicationSnapshotsResponseTypeDef",
    {"SnapshotSummaries": List[SnapshotDetailsTypeDef], "NextToken": str},
    total=False,
)

ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "ApplicationName": str,
        "ApplicationARN": str,
        "ApplicationStatus": Literal[
            "DELETING", "STARTING", "STOPPING", "READY", "RUNNING", "UPDATING"
        ],
        "ApplicationVersionId": int,
        "RuntimeEnvironment": Literal["SQL-1_0", "FLINK-1_6", "FLINK-1_8"],
    },
)

_RequiredListApplicationsResponseTypeDef = TypedDict(
    "_RequiredListApplicationsResponseTypeDef",
    {"ApplicationSummaries": List[ApplicationSummaryTypeDef]},
)
_OptionalListApplicationsResponseTypeDef = TypedDict(
    "_OptionalListApplicationsResponseTypeDef", {"NextToken": str}, total=False
)


class ListApplicationsResponseTypeDef(
    _RequiredListApplicationsResponseTypeDef, _OptionalListApplicationsResponseTypeDef
):
    pass


_RequiredTagTypeDef = TypedDict("_RequiredTagTypeDef", {"Key": str})
_OptionalTagTypeDef = TypedDict("_OptionalTagTypeDef", {"Value": str}, total=False)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

FlinkRunConfigurationTypeDef = TypedDict(
    "FlinkRunConfigurationTypeDef", {"AllowNonRestoredState": bool}, total=False
)

SqlRunConfigurationTypeDef = TypedDict(
    "SqlRunConfigurationTypeDef",
    {
        "InputId": str,
        "InputStartingPositionConfiguration": InputStartingPositionConfigurationTypeDef,
    },
)

RunConfigurationTypeDef = TypedDict(
    "RunConfigurationTypeDef",
    {
        "FlinkRunConfiguration": FlinkRunConfigurationTypeDef,
        "SqlRunConfigurations": List[SqlRunConfigurationTypeDef],
        "ApplicationRestoreConfiguration": ApplicationRestoreConfigurationTypeDef,
    },
    total=False,
)

RunConfigurationUpdateTypeDef = TypedDict(
    "RunConfigurationUpdateTypeDef",
    {
        "FlinkRunConfiguration": FlinkRunConfigurationTypeDef,
        "ApplicationRestoreConfiguration": ApplicationRestoreConfigurationTypeDef,
    },
    total=False,
)

S3ConfigurationTypeDef = TypedDict("S3ConfigurationTypeDef", {"BucketARN": str, "FileKey": str})

UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef", {"ApplicationDetail": ApplicationDetailTypeDef}
)
