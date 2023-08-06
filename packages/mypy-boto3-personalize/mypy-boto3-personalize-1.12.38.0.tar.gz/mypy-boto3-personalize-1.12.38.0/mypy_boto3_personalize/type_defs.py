"""
Main interface for personalize service type definitions.

Usage::

    from mypy_boto3.personalize.type_defs import S3DataConfigTypeDef

    data: S3DataConfigTypeDef = {...}
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
    "S3DataConfigTypeDef",
    "BatchInferenceJobInputTypeDef",
    "BatchInferenceJobOutputTypeDef",
    "CreateBatchInferenceJobResponseTypeDef",
    "CreateCampaignResponseTypeDef",
    "CreateDatasetGroupResponseTypeDef",
    "CreateDatasetImportJobResponseTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateEventTrackerResponseTypeDef",
    "CreateSchemaResponseTypeDef",
    "CreateSolutionResponseTypeDef",
    "CreateSolutionVersionResponseTypeDef",
    "DataSourceTypeDef",
    "AlgorithmImageTypeDef",
    "DefaultCategoricalHyperParameterRangeTypeDef",
    "DefaultContinuousHyperParameterRangeTypeDef",
    "DefaultIntegerHyperParameterRangeTypeDef",
    "DefaultHyperParameterRangesTypeDef",
    "AlgorithmTypeDef",
    "DescribeAlgorithmResponseTypeDef",
    "BatchInferenceJobTypeDef",
    "DescribeBatchInferenceJobResponseTypeDef",
    "CampaignUpdateSummaryTypeDef",
    "CampaignTypeDef",
    "DescribeCampaignResponseTypeDef",
    "DatasetGroupTypeDef",
    "DescribeDatasetGroupResponseTypeDef",
    "DatasetImportJobTypeDef",
    "DescribeDatasetImportJobResponseTypeDef",
    "DatasetTypeDef",
    "DescribeDatasetResponseTypeDef",
    "EventTrackerTypeDef",
    "DescribeEventTrackerResponseTypeDef",
    "FeatureTransformationTypeDef",
    "DescribeFeatureTransformationResponseTypeDef",
    "RecipeTypeDef",
    "DescribeRecipeResponseTypeDef",
    "DatasetSchemaTypeDef",
    "DescribeSchemaResponseTypeDef",
    "AutoMLResultTypeDef",
    "AutoMLConfigTypeDef",
    "HPOObjectiveTypeDef",
    "HPOResourceConfigTypeDef",
    "CategoricalHyperParameterRangeTypeDef",
    "ContinuousHyperParameterRangeTypeDef",
    "IntegerHyperParameterRangeTypeDef",
    "HyperParameterRangesTypeDef",
    "HPOConfigTypeDef",
    "SolutionConfigTypeDef",
    "SolutionVersionSummaryTypeDef",
    "SolutionTypeDef",
    "DescribeSolutionResponseTypeDef",
    "TunedHPOParamsTypeDef",
    "SolutionVersionTypeDef",
    "DescribeSolutionVersionResponseTypeDef",
    "GetSolutionMetricsResponseTypeDef",
    "BatchInferenceJobSummaryTypeDef",
    "ListBatchInferenceJobsResponseTypeDef",
    "CampaignSummaryTypeDef",
    "ListCampaignsResponseTypeDef",
    "DatasetGroupSummaryTypeDef",
    "ListDatasetGroupsResponseTypeDef",
    "DatasetImportJobSummaryTypeDef",
    "ListDatasetImportJobsResponseTypeDef",
    "DatasetSummaryTypeDef",
    "ListDatasetsResponseTypeDef",
    "EventTrackerSummaryTypeDef",
    "ListEventTrackersResponseTypeDef",
    "RecipeSummaryTypeDef",
    "ListRecipesResponseTypeDef",
    "DatasetSchemaSummaryTypeDef",
    "ListSchemasResponseTypeDef",
    "ListSolutionVersionsResponseTypeDef",
    "SolutionSummaryTypeDef",
    "ListSolutionsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "UpdateCampaignResponseTypeDef",
)

_RequiredS3DataConfigTypeDef = TypedDict("_RequiredS3DataConfigTypeDef", {"path": str})
_OptionalS3DataConfigTypeDef = TypedDict(
    "_OptionalS3DataConfigTypeDef", {"kmsKeyArn": str}, total=False
)


class S3DataConfigTypeDef(_RequiredS3DataConfigTypeDef, _OptionalS3DataConfigTypeDef):
    pass


BatchInferenceJobInputTypeDef = TypedDict(
    "BatchInferenceJobInputTypeDef", {"s3DataSource": S3DataConfigTypeDef}
)

BatchInferenceJobOutputTypeDef = TypedDict(
    "BatchInferenceJobOutputTypeDef", {"s3DataDestination": S3DataConfigTypeDef}
)

CreateBatchInferenceJobResponseTypeDef = TypedDict(
    "CreateBatchInferenceJobResponseTypeDef", {"batchInferenceJobArn": str}, total=False
)

CreateCampaignResponseTypeDef = TypedDict(
    "CreateCampaignResponseTypeDef", {"campaignArn": str}, total=False
)

CreateDatasetGroupResponseTypeDef = TypedDict(
    "CreateDatasetGroupResponseTypeDef", {"datasetGroupArn": str}, total=False
)

CreateDatasetImportJobResponseTypeDef = TypedDict(
    "CreateDatasetImportJobResponseTypeDef", {"datasetImportJobArn": str}, total=False
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef", {"datasetArn": str}, total=False
)

CreateEventTrackerResponseTypeDef = TypedDict(
    "CreateEventTrackerResponseTypeDef", {"eventTrackerArn": str, "trackingId": str}, total=False
)

CreateSchemaResponseTypeDef = TypedDict(
    "CreateSchemaResponseTypeDef", {"schemaArn": str}, total=False
)

CreateSolutionResponseTypeDef = TypedDict(
    "CreateSolutionResponseTypeDef", {"solutionArn": str}, total=False
)

CreateSolutionVersionResponseTypeDef = TypedDict(
    "CreateSolutionVersionResponseTypeDef", {"solutionVersionArn": str}, total=False
)

DataSourceTypeDef = TypedDict("DataSourceTypeDef", {"dataLocation": str}, total=False)

_RequiredAlgorithmImageTypeDef = TypedDict("_RequiredAlgorithmImageTypeDef", {"dockerURI": str})
_OptionalAlgorithmImageTypeDef = TypedDict(
    "_OptionalAlgorithmImageTypeDef", {"name": str}, total=False
)


class AlgorithmImageTypeDef(_RequiredAlgorithmImageTypeDef, _OptionalAlgorithmImageTypeDef):
    pass


DefaultCategoricalHyperParameterRangeTypeDef = TypedDict(
    "DefaultCategoricalHyperParameterRangeTypeDef",
    {"name": str, "values": List[str], "isTunable": bool},
    total=False,
)

DefaultContinuousHyperParameterRangeTypeDef = TypedDict(
    "DefaultContinuousHyperParameterRangeTypeDef",
    {"name": str, "minValue": float, "maxValue": float, "isTunable": bool},
    total=False,
)

DefaultIntegerHyperParameterRangeTypeDef = TypedDict(
    "DefaultIntegerHyperParameterRangeTypeDef",
    {"name": str, "minValue": int, "maxValue": int, "isTunable": bool},
    total=False,
)

DefaultHyperParameterRangesTypeDef = TypedDict(
    "DefaultHyperParameterRangesTypeDef",
    {
        "integerHyperParameterRanges": List[DefaultIntegerHyperParameterRangeTypeDef],
        "continuousHyperParameterRanges": List[DefaultContinuousHyperParameterRangeTypeDef],
        "categoricalHyperParameterRanges": List[DefaultCategoricalHyperParameterRangeTypeDef],
    },
    total=False,
)

AlgorithmTypeDef = TypedDict(
    "AlgorithmTypeDef",
    {
        "name": str,
        "algorithmArn": str,
        "algorithmImage": AlgorithmImageTypeDef,
        "defaultHyperParameters": Dict[str, str],
        "defaultHyperParameterRanges": DefaultHyperParameterRangesTypeDef,
        "defaultResourceConfig": Dict[str, str],
        "trainingInputMode": str,
        "roleArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

DescribeAlgorithmResponseTypeDef = TypedDict(
    "DescribeAlgorithmResponseTypeDef", {"algorithm": AlgorithmTypeDef}, total=False
)

BatchInferenceJobTypeDef = TypedDict(
    "BatchInferenceJobTypeDef",
    {
        "jobName": str,
        "batchInferenceJobArn": str,
        "failureReason": str,
        "solutionVersionArn": str,
        "numResults": int,
        "jobInput": BatchInferenceJobInputTypeDef,
        "jobOutput": BatchInferenceJobOutputTypeDef,
        "roleArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

DescribeBatchInferenceJobResponseTypeDef = TypedDict(
    "DescribeBatchInferenceJobResponseTypeDef",
    {"batchInferenceJob": BatchInferenceJobTypeDef},
    total=False,
)

CampaignUpdateSummaryTypeDef = TypedDict(
    "CampaignUpdateSummaryTypeDef",
    {
        "solutionVersionArn": str,
        "minProvisionedTPS": int,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

CampaignTypeDef = TypedDict(
    "CampaignTypeDef",
    {
        "name": str,
        "campaignArn": str,
        "solutionVersionArn": str,
        "minProvisionedTPS": int,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "latestCampaignUpdate": CampaignUpdateSummaryTypeDef,
    },
    total=False,
)

DescribeCampaignResponseTypeDef = TypedDict(
    "DescribeCampaignResponseTypeDef", {"campaign": CampaignTypeDef}, total=False
)

DatasetGroupTypeDef = TypedDict(
    "DatasetGroupTypeDef",
    {
        "name": str,
        "datasetGroupArn": str,
        "status": str,
        "roleArn": str,
        "kmsKeyArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
    total=False,
)

DescribeDatasetGroupResponseTypeDef = TypedDict(
    "DescribeDatasetGroupResponseTypeDef", {"datasetGroup": DatasetGroupTypeDef}, total=False
)

DatasetImportJobTypeDef = TypedDict(
    "DatasetImportJobTypeDef",
    {
        "jobName": str,
        "datasetImportJobArn": str,
        "datasetArn": str,
        "dataSource": DataSourceTypeDef,
        "roleArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
    total=False,
)

DescribeDatasetImportJobResponseTypeDef = TypedDict(
    "DescribeDatasetImportJobResponseTypeDef",
    {"datasetImportJob": DatasetImportJobTypeDef},
    total=False,
)

DatasetTypeDef = TypedDict(
    "DatasetTypeDef",
    {
        "name": str,
        "datasetArn": str,
        "datasetGroupArn": str,
        "datasetType": str,
        "schemaArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef", {"dataset": DatasetTypeDef}, total=False
)

EventTrackerTypeDef = TypedDict(
    "EventTrackerTypeDef",
    {
        "name": str,
        "eventTrackerArn": str,
        "accountId": str,
        "trackingId": str,
        "datasetGroupArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

DescribeEventTrackerResponseTypeDef = TypedDict(
    "DescribeEventTrackerResponseTypeDef", {"eventTracker": EventTrackerTypeDef}, total=False
)

FeatureTransformationTypeDef = TypedDict(
    "FeatureTransformationTypeDef",
    {
        "name": str,
        "featureTransformationArn": str,
        "defaultParameters": Dict[str, str],
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "status": str,
    },
    total=False,
)

DescribeFeatureTransformationResponseTypeDef = TypedDict(
    "DescribeFeatureTransformationResponseTypeDef",
    {"featureTransformation": FeatureTransformationTypeDef},
    total=False,
)

RecipeTypeDef = TypedDict(
    "RecipeTypeDef",
    {
        "name": str,
        "recipeArn": str,
        "algorithmArn": str,
        "featureTransformationArn": str,
        "status": str,
        "description": str,
        "creationDateTime": datetime,
        "recipeType": str,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

DescribeRecipeResponseTypeDef = TypedDict(
    "DescribeRecipeResponseTypeDef", {"recipe": RecipeTypeDef}, total=False
)

DatasetSchemaTypeDef = TypedDict(
    "DatasetSchemaTypeDef",
    {
        "name": str,
        "schemaArn": str,
        "schema": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

DescribeSchemaResponseTypeDef = TypedDict(
    "DescribeSchemaResponseTypeDef", {"schema": DatasetSchemaTypeDef}, total=False
)

AutoMLResultTypeDef = TypedDict("AutoMLResultTypeDef", {"bestRecipeArn": str}, total=False)

AutoMLConfigTypeDef = TypedDict(
    "AutoMLConfigTypeDef", {"metricName": str, "recipeList": List[str]}, total=False
)

HPOObjectiveTypeDef = TypedDict(
    "HPOObjectiveTypeDef", {"type": str, "metricName": str, "metricRegex": str}, total=False
)

HPOResourceConfigTypeDef = TypedDict(
    "HPOResourceConfigTypeDef",
    {"maxNumberOfTrainingJobs": str, "maxParallelTrainingJobs": str},
    total=False,
)

CategoricalHyperParameterRangeTypeDef = TypedDict(
    "CategoricalHyperParameterRangeTypeDef", {"name": str, "values": List[str]}, total=False
)

ContinuousHyperParameterRangeTypeDef = TypedDict(
    "ContinuousHyperParameterRangeTypeDef",
    {"name": str, "minValue": float, "maxValue": float},
    total=False,
)

IntegerHyperParameterRangeTypeDef = TypedDict(
    "IntegerHyperParameterRangeTypeDef",
    {"name": str, "minValue": int, "maxValue": int},
    total=False,
)

HyperParameterRangesTypeDef = TypedDict(
    "HyperParameterRangesTypeDef",
    {
        "integerHyperParameterRanges": List[IntegerHyperParameterRangeTypeDef],
        "continuousHyperParameterRanges": List[ContinuousHyperParameterRangeTypeDef],
        "categoricalHyperParameterRanges": List[CategoricalHyperParameterRangeTypeDef],
    },
    total=False,
)

HPOConfigTypeDef = TypedDict(
    "HPOConfigTypeDef",
    {
        "hpoObjective": HPOObjectiveTypeDef,
        "hpoResourceConfig": HPOResourceConfigTypeDef,
        "algorithmHyperParameterRanges": HyperParameterRangesTypeDef,
    },
    total=False,
)

SolutionConfigTypeDef = TypedDict(
    "SolutionConfigTypeDef",
    {
        "eventValueThreshold": str,
        "hpoConfig": HPOConfigTypeDef,
        "algorithmHyperParameters": Dict[str, str],
        "featureTransformationParameters": Dict[str, str],
        "autoMLConfig": AutoMLConfigTypeDef,
    },
    total=False,
)

SolutionVersionSummaryTypeDef = TypedDict(
    "SolutionVersionSummaryTypeDef",
    {
        "solutionVersionArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
    total=False,
)

SolutionTypeDef = TypedDict(
    "SolutionTypeDef",
    {
        "name": str,
        "solutionArn": str,
        "performHPO": bool,
        "performAutoML": bool,
        "recipeArn": str,
        "datasetGroupArn": str,
        "eventType": str,
        "solutionConfig": SolutionConfigTypeDef,
        "autoMLResult": AutoMLResultTypeDef,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "latestSolutionVersion": SolutionVersionSummaryTypeDef,
    },
    total=False,
)

DescribeSolutionResponseTypeDef = TypedDict(
    "DescribeSolutionResponseTypeDef", {"solution": SolutionTypeDef}, total=False
)

TunedHPOParamsTypeDef = TypedDict(
    "TunedHPOParamsTypeDef", {"algorithmHyperParameters": Dict[str, str]}, total=False
)

SolutionVersionTypeDef = TypedDict(
    "SolutionVersionTypeDef",
    {
        "solutionVersionArn": str,
        "solutionArn": str,
        "performHPO": bool,
        "performAutoML": bool,
        "recipeArn": str,
        "eventType": str,
        "datasetGroupArn": str,
        "solutionConfig": SolutionConfigTypeDef,
        "trainingHours": float,
        "trainingMode": Literal["FULL", "UPDATE"],
        "tunedHPOParams": TunedHPOParamsTypeDef,
        "status": str,
        "failureReason": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

DescribeSolutionVersionResponseTypeDef = TypedDict(
    "DescribeSolutionVersionResponseTypeDef",
    {"solutionVersion": SolutionVersionTypeDef},
    total=False,
)

GetSolutionMetricsResponseTypeDef = TypedDict(
    "GetSolutionMetricsResponseTypeDef",
    {"solutionVersionArn": str, "metrics": Dict[str, float]},
    total=False,
)

BatchInferenceJobSummaryTypeDef = TypedDict(
    "BatchInferenceJobSummaryTypeDef",
    {
        "batchInferenceJobArn": str,
        "jobName": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
        "solutionVersionArn": str,
    },
    total=False,
)

ListBatchInferenceJobsResponseTypeDef = TypedDict(
    "ListBatchInferenceJobsResponseTypeDef",
    {"batchInferenceJobs": List[BatchInferenceJobSummaryTypeDef], "nextToken": str},
    total=False,
)

CampaignSummaryTypeDef = TypedDict(
    "CampaignSummaryTypeDef",
    {
        "name": str,
        "campaignArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
    total=False,
)

ListCampaignsResponseTypeDef = TypedDict(
    "ListCampaignsResponseTypeDef",
    {"campaigns": List[CampaignSummaryTypeDef], "nextToken": str},
    total=False,
)

DatasetGroupSummaryTypeDef = TypedDict(
    "DatasetGroupSummaryTypeDef",
    {
        "name": str,
        "datasetGroupArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
    total=False,
)

ListDatasetGroupsResponseTypeDef = TypedDict(
    "ListDatasetGroupsResponseTypeDef",
    {"datasetGroups": List[DatasetGroupSummaryTypeDef], "nextToken": str},
    total=False,
)

DatasetImportJobSummaryTypeDef = TypedDict(
    "DatasetImportJobSummaryTypeDef",
    {
        "datasetImportJobArn": str,
        "jobName": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "failureReason": str,
    },
    total=False,
)

ListDatasetImportJobsResponseTypeDef = TypedDict(
    "ListDatasetImportJobsResponseTypeDef",
    {"datasetImportJobs": List[DatasetImportJobSummaryTypeDef], "nextToken": str},
    total=False,
)

DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "name": str,
        "datasetArn": str,
        "datasetType": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

ListDatasetsResponseTypeDef = TypedDict(
    "ListDatasetsResponseTypeDef",
    {"datasets": List[DatasetSummaryTypeDef], "nextToken": str},
    total=False,
)

EventTrackerSummaryTypeDef = TypedDict(
    "EventTrackerSummaryTypeDef",
    {
        "name": str,
        "eventTrackerArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

ListEventTrackersResponseTypeDef = TypedDict(
    "ListEventTrackersResponseTypeDef",
    {"eventTrackers": List[EventTrackerSummaryTypeDef], "nextToken": str},
    total=False,
)

RecipeSummaryTypeDef = TypedDict(
    "RecipeSummaryTypeDef",
    {
        "name": str,
        "recipeArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

ListRecipesResponseTypeDef = TypedDict(
    "ListRecipesResponseTypeDef",
    {"recipes": List[RecipeSummaryTypeDef], "nextToken": str},
    total=False,
)

DatasetSchemaSummaryTypeDef = TypedDict(
    "DatasetSchemaSummaryTypeDef",
    {"name": str, "schemaArn": str, "creationDateTime": datetime, "lastUpdatedDateTime": datetime},
    total=False,
)

ListSchemasResponseTypeDef = TypedDict(
    "ListSchemasResponseTypeDef",
    {"schemas": List[DatasetSchemaSummaryTypeDef], "nextToken": str},
    total=False,
)

ListSolutionVersionsResponseTypeDef = TypedDict(
    "ListSolutionVersionsResponseTypeDef",
    {"solutionVersions": List[SolutionVersionSummaryTypeDef], "nextToken": str},
    total=False,
)

SolutionSummaryTypeDef = TypedDict(
    "SolutionSummaryTypeDef",
    {
        "name": str,
        "solutionArn": str,
        "status": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

ListSolutionsResponseTypeDef = TypedDict(
    "ListSolutionsResponseTypeDef",
    {"solutions": List[SolutionSummaryTypeDef], "nextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

UpdateCampaignResponseTypeDef = TypedDict(
    "UpdateCampaignResponseTypeDef", {"campaignArn": str}, total=False
)
