"""
Main interface for forecast service type definitions.

Usage::

    from mypy_boto3.forecast.type_defs import CreateDatasetGroupResponseTypeDef

    data: CreateDatasetGroupResponseTypeDef = {...}
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
    "CreateDatasetGroupResponseTypeDef",
    "CreateDatasetImportJobResponseTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateForecastExportJobResponseTypeDef",
    "CreateForecastResponseTypeDef",
    "CreatePredictorResponseTypeDef",
    "S3ConfigTypeDef",
    "DataDestinationTypeDef",
    "DataSourceTypeDef",
    "DescribeDatasetGroupResponseTypeDef",
    "StatisticsTypeDef",
    "DescribeDatasetImportJobResponseTypeDef",
    "EncryptionConfigTypeDef",
    "SchemaAttributeTypeDef",
    "SchemaTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeForecastExportJobResponseTypeDef",
    "DescribeForecastResponseTypeDef",
    "EvaluationParametersTypeDef",
    "FeaturizationMethodTypeDef",
    "FeaturizationTypeDef",
    "FeaturizationConfigTypeDef",
    "CategoricalParameterRangeTypeDef",
    "ContinuousParameterRangeTypeDef",
    "IntegerParameterRangeTypeDef",
    "ParameterRangesTypeDef",
    "HyperParameterTuningJobConfigTypeDef",
    "SupplementaryFeatureTypeDef",
    "InputDataConfigTypeDef",
    "TestWindowSummaryTypeDef",
    "PredictorExecutionTypeDef",
    "PredictorExecutionDetailsTypeDef",
    "DescribePredictorResponseTypeDef",
    "FilterTypeDef",
    "WeightedQuantileLossTypeDef",
    "MetricsTypeDef",
    "WindowSummaryTypeDef",
    "EvaluationResultTypeDef",
    "GetAccuracyMetricsResponseTypeDef",
    "DatasetGroupSummaryTypeDef",
    "ListDatasetGroupsResponseTypeDef",
    "DatasetImportJobSummaryTypeDef",
    "ListDatasetImportJobsResponseTypeDef",
    "DatasetSummaryTypeDef",
    "ListDatasetsResponseTypeDef",
    "ForecastExportJobSummaryTypeDef",
    "ListForecastExportJobsResponseTypeDef",
    "ForecastSummaryTypeDef",
    "ListForecastsResponseTypeDef",
    "PredictorSummaryTypeDef",
    "ListPredictorsResponseTypeDef",
    "PaginatorConfigTypeDef",
)

CreateDatasetGroupResponseTypeDef = TypedDict(
    "CreateDatasetGroupResponseTypeDef", {"DatasetGroupArn": str}, total=False
)

CreateDatasetImportJobResponseTypeDef = TypedDict(
    "CreateDatasetImportJobResponseTypeDef", {"DatasetImportJobArn": str}, total=False
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef", {"DatasetArn": str}, total=False
)

CreateForecastExportJobResponseTypeDef = TypedDict(
    "CreateForecastExportJobResponseTypeDef", {"ForecastExportJobArn": str}, total=False
)

CreateForecastResponseTypeDef = TypedDict(
    "CreateForecastResponseTypeDef", {"ForecastArn": str}, total=False
)

CreatePredictorResponseTypeDef = TypedDict(
    "CreatePredictorResponseTypeDef", {"PredictorArn": str}, total=False
)

_RequiredS3ConfigTypeDef = TypedDict("_RequiredS3ConfigTypeDef", {"Path": str, "RoleArn": str})
_OptionalS3ConfigTypeDef = TypedDict("_OptionalS3ConfigTypeDef", {"KMSKeyArn": str}, total=False)


class S3ConfigTypeDef(_RequiredS3ConfigTypeDef, _OptionalS3ConfigTypeDef):
    pass


DataDestinationTypeDef = TypedDict("DataDestinationTypeDef", {"S3Config": S3ConfigTypeDef})

DataSourceTypeDef = TypedDict("DataSourceTypeDef", {"S3Config": S3ConfigTypeDef})

DescribeDatasetGroupResponseTypeDef = TypedDict(
    "DescribeDatasetGroupResponseTypeDef",
    {
        "DatasetGroupName": str,
        "DatasetGroupArn": str,
        "DatasetArns": List[str],
        "Domain": Literal[
            "RETAIL",
            "CUSTOM",
            "INVENTORY_PLANNING",
            "EC2_CAPACITY",
            "WORK_FORCE",
            "WEB_TRAFFIC",
            "METRICS",
        ],
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

StatisticsTypeDef = TypedDict(
    "StatisticsTypeDef",
    {
        "Count": int,
        "CountDistinct": int,
        "CountNull": int,
        "CountNan": int,
        "Min": str,
        "Max": str,
        "Avg": float,
        "Stddev": float,
    },
    total=False,
)

DescribeDatasetImportJobResponseTypeDef = TypedDict(
    "DescribeDatasetImportJobResponseTypeDef",
    {
        "DatasetImportJobName": str,
        "DatasetImportJobArn": str,
        "DatasetArn": str,
        "TimestampFormat": str,
        "DataSource": DataSourceTypeDef,
        "FieldStatistics": Dict[str, StatisticsTypeDef],
        "DataSize": float,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

EncryptionConfigTypeDef = TypedDict("EncryptionConfigTypeDef", {"RoleArn": str, "KMSKeyArn": str})

SchemaAttributeTypeDef = TypedDict(
    "SchemaAttributeTypeDef",
    {"AttributeName": str, "AttributeType": Literal["string", "integer", "float", "timestamp"]},
    total=False,
)

SchemaTypeDef = TypedDict(
    "SchemaTypeDef", {"Attributes": List[SchemaAttributeTypeDef]}, total=False
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "DatasetArn": str,
        "DatasetName": str,
        "Domain": Literal[
            "RETAIL",
            "CUSTOM",
            "INVENTORY_PLANNING",
            "EC2_CAPACITY",
            "WORK_FORCE",
            "WEB_TRAFFIC",
            "METRICS",
        ],
        "DatasetType": Literal["TARGET_TIME_SERIES", "RELATED_TIME_SERIES", "ITEM_METADATA"],
        "DataFrequency": str,
        "Schema": SchemaTypeDef,
        "EncryptionConfig": EncryptionConfigTypeDef,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

DescribeForecastExportJobResponseTypeDef = TypedDict(
    "DescribeForecastExportJobResponseTypeDef",
    {
        "ForecastExportJobArn": str,
        "ForecastExportJobName": str,
        "ForecastArn": str,
        "Destination": DataDestinationTypeDef,
        "Message": str,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

DescribeForecastResponseTypeDef = TypedDict(
    "DescribeForecastResponseTypeDef",
    {
        "ForecastArn": str,
        "ForecastName": str,
        "ForecastTypes": List[str],
        "PredictorArn": str,
        "DatasetGroupArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

EvaluationParametersTypeDef = TypedDict(
    "EvaluationParametersTypeDef",
    {"NumberOfBacktestWindows": int, "BackTestWindowOffset": int},
    total=False,
)

_RequiredFeaturizationMethodTypeDef = TypedDict(
    "_RequiredFeaturizationMethodTypeDef", {"FeaturizationMethodName": Literal["filling"]}
)
_OptionalFeaturizationMethodTypeDef = TypedDict(
    "_OptionalFeaturizationMethodTypeDef",
    {"FeaturizationMethodParameters": Dict[str, str]},
    total=False,
)


class FeaturizationMethodTypeDef(
    _RequiredFeaturizationMethodTypeDef, _OptionalFeaturizationMethodTypeDef
):
    pass


_RequiredFeaturizationTypeDef = TypedDict("_RequiredFeaturizationTypeDef", {"AttributeName": str})
_OptionalFeaturizationTypeDef = TypedDict(
    "_OptionalFeaturizationTypeDef",
    {"FeaturizationPipeline": List[FeaturizationMethodTypeDef]},
    total=False,
)


class FeaturizationTypeDef(_RequiredFeaturizationTypeDef, _OptionalFeaturizationTypeDef):
    pass


_RequiredFeaturizationConfigTypeDef = TypedDict(
    "_RequiredFeaturizationConfigTypeDef", {"ForecastFrequency": str}
)
_OptionalFeaturizationConfigTypeDef = TypedDict(
    "_OptionalFeaturizationConfigTypeDef",
    {"ForecastDimensions": List[str], "Featurizations": List[FeaturizationTypeDef]},
    total=False,
)


class FeaturizationConfigTypeDef(
    _RequiredFeaturizationConfigTypeDef, _OptionalFeaturizationConfigTypeDef
):
    pass


CategoricalParameterRangeTypeDef = TypedDict(
    "CategoricalParameterRangeTypeDef", {"Name": str, "Values": List[str]}
)

_RequiredContinuousParameterRangeTypeDef = TypedDict(
    "_RequiredContinuousParameterRangeTypeDef", {"Name": str, "MaxValue": float, "MinValue": float}
)
_OptionalContinuousParameterRangeTypeDef = TypedDict(
    "_OptionalContinuousParameterRangeTypeDef",
    {"ScalingType": Literal["Auto", "Linear", "Logarithmic", "ReverseLogarithmic"]},
    total=False,
)


class ContinuousParameterRangeTypeDef(
    _RequiredContinuousParameterRangeTypeDef, _OptionalContinuousParameterRangeTypeDef
):
    pass


_RequiredIntegerParameterRangeTypeDef = TypedDict(
    "_RequiredIntegerParameterRangeTypeDef", {"Name": str, "MaxValue": int, "MinValue": int}
)
_OptionalIntegerParameterRangeTypeDef = TypedDict(
    "_OptionalIntegerParameterRangeTypeDef",
    {"ScalingType": Literal["Auto", "Linear", "Logarithmic", "ReverseLogarithmic"]},
    total=False,
)


class IntegerParameterRangeTypeDef(
    _RequiredIntegerParameterRangeTypeDef, _OptionalIntegerParameterRangeTypeDef
):
    pass


ParameterRangesTypeDef = TypedDict(
    "ParameterRangesTypeDef",
    {
        "CategoricalParameterRanges": List[CategoricalParameterRangeTypeDef],
        "ContinuousParameterRanges": List[ContinuousParameterRangeTypeDef],
        "IntegerParameterRanges": List[IntegerParameterRangeTypeDef],
    },
    total=False,
)

HyperParameterTuningJobConfigTypeDef = TypedDict(
    "HyperParameterTuningJobConfigTypeDef", {"ParameterRanges": ParameterRangesTypeDef}, total=False
)

SupplementaryFeatureTypeDef = TypedDict("SupplementaryFeatureTypeDef", {"Name": str, "Value": str})

_RequiredInputDataConfigTypeDef = TypedDict(
    "_RequiredInputDataConfigTypeDef", {"DatasetGroupArn": str}
)
_OptionalInputDataConfigTypeDef = TypedDict(
    "_OptionalInputDataConfigTypeDef",
    {"SupplementaryFeatures": List[SupplementaryFeatureTypeDef]},
    total=False,
)


class InputDataConfigTypeDef(_RequiredInputDataConfigTypeDef, _OptionalInputDataConfigTypeDef):
    pass


TestWindowSummaryTypeDef = TypedDict(
    "TestWindowSummaryTypeDef",
    {"TestWindowStart": datetime, "TestWindowEnd": datetime, "Status": str, "Message": str},
    total=False,
)

PredictorExecutionTypeDef = TypedDict(
    "PredictorExecutionTypeDef",
    {"AlgorithmArn": str, "TestWindows": List[TestWindowSummaryTypeDef]},
    total=False,
)

PredictorExecutionDetailsTypeDef = TypedDict(
    "PredictorExecutionDetailsTypeDef",
    {"PredictorExecutions": List[PredictorExecutionTypeDef]},
    total=False,
)

DescribePredictorResponseTypeDef = TypedDict(
    "DescribePredictorResponseTypeDef",
    {
        "PredictorArn": str,
        "PredictorName": str,
        "AlgorithmArn": str,
        "ForecastHorizon": int,
        "PerformAutoML": bool,
        "PerformHPO": bool,
        "TrainingParameters": Dict[str, str],
        "EvaluationParameters": EvaluationParametersTypeDef,
        "HPOConfig": HyperParameterTuningJobConfigTypeDef,
        "InputDataConfig": InputDataConfigTypeDef,
        "FeaturizationConfig": FeaturizationConfigTypeDef,
        "EncryptionConfig": EncryptionConfigTypeDef,
        "PredictorExecutionDetails": PredictorExecutionDetailsTypeDef,
        "DatasetImportJobArns": List[str],
        "AutoMLAlgorithmArns": List[str],
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef", {"Key": str, "Value": str, "Condition": Literal["IS", "IS_NOT"]}
)

WeightedQuantileLossTypeDef = TypedDict(
    "WeightedQuantileLossTypeDef", {"Quantile": float, "LossValue": float}, total=False
)

MetricsTypeDef = TypedDict(
    "MetricsTypeDef",
    {"RMSE": float, "WeightedQuantileLosses": List[WeightedQuantileLossTypeDef]},
    total=False,
)

WindowSummaryTypeDef = TypedDict(
    "WindowSummaryTypeDef",
    {
        "TestWindowStart": datetime,
        "TestWindowEnd": datetime,
        "ItemCount": int,
        "EvaluationType": Literal["SUMMARY", "COMPUTED"],
        "Metrics": MetricsTypeDef,
    },
    total=False,
)

EvaluationResultTypeDef = TypedDict(
    "EvaluationResultTypeDef",
    {"AlgorithmArn": str, "TestWindows": List[WindowSummaryTypeDef]},
    total=False,
)

GetAccuracyMetricsResponseTypeDef = TypedDict(
    "GetAccuracyMetricsResponseTypeDef",
    {"PredictorEvaluationResults": List[EvaluationResultTypeDef]},
    total=False,
)

DatasetGroupSummaryTypeDef = TypedDict(
    "DatasetGroupSummaryTypeDef",
    {
        "DatasetGroupArn": str,
        "DatasetGroupName": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

ListDatasetGroupsResponseTypeDef = TypedDict(
    "ListDatasetGroupsResponseTypeDef",
    {"DatasetGroups": List[DatasetGroupSummaryTypeDef], "NextToken": str},
    total=False,
)

DatasetImportJobSummaryTypeDef = TypedDict(
    "DatasetImportJobSummaryTypeDef",
    {
        "DatasetImportJobArn": str,
        "DatasetImportJobName": str,
        "DataSource": DataSourceTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

ListDatasetImportJobsResponseTypeDef = TypedDict(
    "ListDatasetImportJobsResponseTypeDef",
    {"DatasetImportJobs": List[DatasetImportJobSummaryTypeDef], "NextToken": str},
    total=False,
)

DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "DatasetArn": str,
        "DatasetName": str,
        "DatasetType": Literal["TARGET_TIME_SERIES", "RELATED_TIME_SERIES", "ITEM_METADATA"],
        "Domain": Literal[
            "RETAIL",
            "CUSTOM",
            "INVENTORY_PLANNING",
            "EC2_CAPACITY",
            "WORK_FORCE",
            "WEB_TRAFFIC",
            "METRICS",
        ],
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {"Datasets": List[DatasetSummaryTypeDef], "NextToken": str},
    total=False,
)

ForecastExportJobSummaryTypeDef = TypedDict(
    "ForecastExportJobSummaryTypeDef",
    {
        "ForecastExportJobArn": str,
        "ForecastExportJobName": str,
        "Destination": DataDestinationTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

ListForecastExportJobsResponseTypeDef = TypedDict(
    "ListForecastExportJobsResponseTypeDef",
    {"ForecastExportJobs": List[ForecastExportJobSummaryTypeDef], "NextToken": str},
    total=False,
)

ForecastSummaryTypeDef = TypedDict(
    "ForecastSummaryTypeDef",
    {
        "ForecastArn": str,
        "ForecastName": str,
        "PredictorArn": str,
        "DatasetGroupArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

ListForecastsResponseTypeDef = TypedDict(
    "ListForecastsResponseTypeDef",
    {"Forecasts": List[ForecastSummaryTypeDef], "NextToken": str},
    total=False,
)

PredictorSummaryTypeDef = TypedDict(
    "PredictorSummaryTypeDef",
    {
        "PredictorArn": str,
        "PredictorName": str,
        "DatasetGroupArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)

ListPredictorsResponseTypeDef = TypedDict(
    "ListPredictorsResponseTypeDef",
    {"Predictors": List[PredictorSummaryTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
