"""
Main interface for sagemaker service type definitions.

Usage::

    from mypy_boto3.sagemaker.type_defs import TagTypeDef

    data: TagTypeDef = {...}
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
    "TagTypeDef",
    "AddTagsOutputTypeDef",
    "MetricDefinitionTypeDef",
    "AlgorithmSpecificationTypeDef",
    "FileSystemDataSourceTypeDef",
    "S3DataSourceTypeDef",
    "DataSourceTypeDef",
    "ShuffleConfigTypeDef",
    "ChannelTypeDef",
    "OutputDataConfigTypeDef",
    "ResourceConfigTypeDef",
    "StoppingConditionTypeDef",
    "TrainingJobDefinitionTypeDef",
    "TransformS3DataSourceTypeDef",
    "TransformDataSourceTypeDef",
    "TransformInputTypeDef",
    "TransformOutputTypeDef",
    "TransformResourcesTypeDef",
    "TransformJobDefinitionTypeDef",
    "AlgorithmValidationProfileTypeDef",
    "AlgorithmValidationSpecificationTypeDef",
    "AppSpecificationTypeDef",
    "AssociateTrialComponentResponseTypeDef",
    "AutoMLS3DataSourceTypeDef",
    "AutoMLDataSourceTypeDef",
    "AutoMLChannelTypeDef",
    "AutoMLJobCompletionCriteriaTypeDef",
    "VpcConfigTypeDef",
    "AutoMLSecurityConfigTypeDef",
    "AutoMLJobConfigTypeDef",
    "AutoMLJobObjectiveTypeDef",
    "AutoMLOutputDataConfigTypeDef",
    "CheckpointConfigTypeDef",
    "ContainerDefinitionTypeDef",
    "CreateAlgorithmOutputTypeDef",
    "CreateAppResponseTypeDef",
    "CreateAutoMLJobResponseTypeDef",
    "CreateCodeRepositoryOutputTypeDef",
    "CreateCompilationJobResponseTypeDef",
    "CreateDomainResponseTypeDef",
    "CreateEndpointConfigOutputTypeDef",
    "CreateEndpointOutputTypeDef",
    "CreateExperimentResponseTypeDef",
    "CreateFlowDefinitionResponseTypeDef",
    "CreateHumanTaskUiResponseTypeDef",
    "CreateHyperParameterTuningJobResponseTypeDef",
    "CreateLabelingJobResponseTypeDef",
    "CreateModelOutputTypeDef",
    "CreateModelPackageOutputTypeDef",
    "CreateMonitoringScheduleResponseTypeDef",
    "CreateNotebookInstanceLifecycleConfigOutputTypeDef",
    "CreateNotebookInstanceOutputTypeDef",
    "CreatePresignedDomainUrlResponseTypeDef",
    "CreatePresignedNotebookInstanceUrlOutputTypeDef",
    "CreateProcessingJobResponseTypeDef",
    "CreateTrainingJobResponseTypeDef",
    "CreateTransformJobResponseTypeDef",
    "CreateTrialComponentResponseTypeDef",
    "CreateTrialResponseTypeDef",
    "CreateUserProfileResponseTypeDef",
    "CreateWorkteamResponseTypeDef",
    "CaptureContentTypeHeaderTypeDef",
    "CaptureOptionTypeDef",
    "DataCaptureConfigTypeDef",
    "DataProcessingTypeDef",
    "CollectionConfigurationTypeDef",
    "DebugHookConfigTypeDef",
    "DebugRuleConfigurationTypeDef",
    "DeleteExperimentResponseTypeDef",
    "DeleteTrialComponentResponseTypeDef",
    "DeleteTrialResponseTypeDef",
    "DeleteWorkteamResponseTypeDef",
    "AlgorithmStatusItemTypeDef",
    "AlgorithmStatusDetailsTypeDef",
    "ModelPackageContainerDefinitionTypeDef",
    "InferenceSpecificationTypeDef",
    "ChannelSpecificationTypeDef",
    "CategoricalParameterRangeSpecificationTypeDef",
    "ContinuousParameterRangeSpecificationTypeDef",
    "IntegerParameterRangeSpecificationTypeDef",
    "ParameterRangeTypeDef",
    "HyperParameterSpecificationTypeDef",
    "HyperParameterTuningJobObjectiveTypeDef",
    "TrainingSpecificationTypeDef",
    "DescribeAlgorithmOutputTypeDef",
    "ResourceSpecTypeDef",
    "DescribeAppResponseTypeDef",
    "AutoMLCandidateStepTypeDef",
    "AutoMLContainerDefinitionTypeDef",
    "FinalAutoMLJobObjectiveMetricTypeDef",
    "AutoMLCandidateTypeDef",
    "AutoMLJobArtifactsTypeDef",
    "ResolvedAttributesTypeDef",
    "DescribeAutoMLJobResponseTypeDef",
    "GitConfigTypeDef",
    "DescribeCodeRepositoryOutputTypeDef",
    "InputConfigTypeDef",
    "ModelArtifactsTypeDef",
    "OutputConfigTypeDef",
    "DescribeCompilationJobResponseTypeDef",
    "JupyterServerAppSettingsTypeDef",
    "KernelGatewayAppSettingsTypeDef",
    "SharingSettingsTypeDef",
    "TensorBoardAppSettingsTypeDef",
    "UserSettingsTypeDef",
    "DescribeDomainResponseTypeDef",
    "ProductionVariantTypeDef",
    "DescribeEndpointConfigOutputTypeDef",
    "DataCaptureConfigSummaryTypeDef",
    "DeployedImageTypeDef",
    "ProductionVariantSummaryTypeDef",
    "DescribeEndpointOutputTypeDef",
    "ExperimentSourceTypeDef",
    "UserContextTypeDef",
    "DescribeExperimentResponseTypeDef",
    "FlowDefinitionOutputConfigTypeDef",
    "HumanLoopActivationConditionsConfigTypeDef",
    "HumanLoopActivationConfigTypeDef",
    "USDTypeDef",
    "PublicWorkforceTaskPriceTypeDef",
    "HumanLoopConfigTypeDef",
    "HumanLoopRequestSourceTypeDef",
    "DescribeFlowDefinitionResponseTypeDef",
    "UiTemplateInfoTypeDef",
    "DescribeHumanTaskUiResponseTypeDef",
    "HyperParameterAlgorithmSpecificationTypeDef",
    "CategoricalParameterRangeTypeDef",
    "ContinuousParameterRangeTypeDef",
    "IntegerParameterRangeTypeDef",
    "ParameterRangesTypeDef",
    "HyperParameterTrainingJobDefinitionTypeDef",
    "FinalHyperParameterTuningJobObjectiveMetricTypeDef",
    "HyperParameterTrainingJobSummaryTypeDef",
    "ResourceLimitsTypeDef",
    "TuningJobCompletionCriteriaTypeDef",
    "HyperParameterTuningJobConfigTypeDef",
    "ParentHyperParameterTuningJobTypeDef",
    "HyperParameterTuningJobWarmStartConfigTypeDef",
    "ObjectiveStatusCountersTypeDef",
    "TrainingJobStatusCountersTypeDef",
    "DescribeHyperParameterTuningJobResponseTypeDef",
    "AnnotationConsolidationConfigTypeDef",
    "UiConfigTypeDef",
    "HumanTaskConfigTypeDef",
    "LabelCountersTypeDef",
    "LabelingJobResourceConfigTypeDef",
    "LabelingJobAlgorithmsConfigTypeDef",
    "LabelingJobDataAttributesTypeDef",
    "LabelingJobS3DataSourceTypeDef",
    "LabelingJobDataSourceTypeDef",
    "LabelingJobInputConfigTypeDef",
    "LabelingJobOutputConfigTypeDef",
    "LabelingJobOutputTypeDef",
    "LabelingJobStoppingConditionsTypeDef",
    "DescribeLabelingJobResponseTypeDef",
    "DescribeModelOutputTypeDef",
    "ModelPackageStatusItemTypeDef",
    "ModelPackageStatusDetailsTypeDef",
    "ModelPackageValidationProfileTypeDef",
    "ModelPackageValidationSpecificationTypeDef",
    "SourceAlgorithmTypeDef",
    "SourceAlgorithmSpecificationTypeDef",
    "DescribeModelPackageOutputTypeDef",
    "MonitoringExecutionSummaryTypeDef",
    "MonitoringAppSpecificationTypeDef",
    "MonitoringConstraintsResourceTypeDef",
    "MonitoringStatisticsResourceTypeDef",
    "MonitoringBaselineConfigTypeDef",
    "EndpointInputTypeDef",
    "MonitoringInputTypeDef",
    "MonitoringS3OutputTypeDef",
    "MonitoringOutputTypeDef",
    "MonitoringOutputConfigTypeDef",
    "MonitoringClusterConfigTypeDef",
    "MonitoringResourcesTypeDef",
    "MonitoringStoppingConditionTypeDef",
    "NetworkConfigTypeDef",
    "MonitoringJobDefinitionTypeDef",
    "ScheduleConfigTypeDef",
    "MonitoringScheduleConfigTypeDef",
    "DescribeMonitoringScheduleResponseTypeDef",
    "NotebookInstanceLifecycleHookTypeDef",
    "DescribeNotebookInstanceLifecycleConfigOutputTypeDef",
    "DescribeNotebookInstanceOutputTypeDef",
    "ExperimentConfigTypeDef",
    "ProcessingS3InputTypeDef",
    "ProcessingInputTypeDef",
    "ProcessingS3OutputTypeDef",
    "ProcessingOutputTypeDef",
    "ProcessingOutputConfigTypeDef",
    "ProcessingClusterConfigTypeDef",
    "ProcessingResourcesTypeDef",
    "ProcessingStoppingConditionTypeDef",
    "DescribeProcessingJobResponseTypeDef",
    "SubscribedWorkteamTypeDef",
    "DescribeSubscribedWorkteamResponseTypeDef",
    "DebugRuleEvaluationStatusTypeDef",
    "MetricDataTypeDef",
    "SecondaryStatusTransitionTypeDef",
    "TensorBoardOutputConfigTypeDef",
    "DescribeTrainingJobResponseTypeDef",
    "DescribeTransformJobResponseTypeDef",
    "TrialComponentArtifactTypeDef",
    "TrialComponentMetricSummaryTypeDef",
    "TrialComponentParameterValueTypeDef",
    "TrialComponentSourceTypeDef",
    "TrialComponentStatusTypeDef",
    "DescribeTrialComponentResponseTypeDef",
    "TrialSourceTypeDef",
    "DescribeTrialResponseTypeDef",
    "DescribeUserProfileResponseTypeDef",
    "SourceIpConfigTypeDef",
    "WorkforceTypeDef",
    "DescribeWorkforceResponseTypeDef",
    "CognitoMemberDefinitionTypeDef",
    "MemberDefinitionTypeDef",
    "NotificationConfigurationTypeDef",
    "WorkteamTypeDef",
    "DescribeWorkteamResponseTypeDef",
    "DesiredWeightAndCapacityTypeDef",
    "DisassociateTrialComponentResponseTypeDef",
    "PropertyNameSuggestionTypeDef",
    "GetSearchSuggestionsResponseTypeDef",
    "GitConfigForUpdateTypeDef",
    "AlgorithmSummaryTypeDef",
    "ListAlgorithmsOutputTypeDef",
    "AppDetailsTypeDef",
    "ListAppsResponseTypeDef",
    "AutoMLJobSummaryTypeDef",
    "ListAutoMLJobsResponseTypeDef",
    "ListCandidatesForAutoMLJobResponseTypeDef",
    "CodeRepositorySummaryTypeDef",
    "ListCodeRepositoriesOutputTypeDef",
    "CompilationJobSummaryTypeDef",
    "ListCompilationJobsResponseTypeDef",
    "DomainDetailsTypeDef",
    "ListDomainsResponseTypeDef",
    "EndpointConfigSummaryTypeDef",
    "ListEndpointConfigsOutputTypeDef",
    "EndpointSummaryTypeDef",
    "ListEndpointsOutputTypeDef",
    "ExperimentSummaryTypeDef",
    "ListExperimentsResponseTypeDef",
    "FlowDefinitionSummaryTypeDef",
    "ListFlowDefinitionsResponseTypeDef",
    "HumanTaskUiSummaryTypeDef",
    "ListHumanTaskUisResponseTypeDef",
    "HyperParameterTuningJobSummaryTypeDef",
    "ListHyperParameterTuningJobsResponseTypeDef",
    "LabelCountersForWorkteamTypeDef",
    "LabelingJobForWorkteamSummaryTypeDef",
    "ListLabelingJobsForWorkteamResponseTypeDef",
    "LabelingJobSummaryTypeDef",
    "ListLabelingJobsResponseTypeDef",
    "ModelPackageSummaryTypeDef",
    "ListModelPackagesOutputTypeDef",
    "ModelSummaryTypeDef",
    "ListModelsOutputTypeDef",
    "ListMonitoringExecutionsResponseTypeDef",
    "MonitoringScheduleSummaryTypeDef",
    "ListMonitoringSchedulesResponseTypeDef",
    "NotebookInstanceLifecycleConfigSummaryTypeDef",
    "ListNotebookInstanceLifecycleConfigsOutputTypeDef",
    "NotebookInstanceSummaryTypeDef",
    "ListNotebookInstancesOutputTypeDef",
    "ProcessingJobSummaryTypeDef",
    "ListProcessingJobsResponseTypeDef",
    "ListSubscribedWorkteamsResponseTypeDef",
    "ListTagsOutputTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobResponseTypeDef",
    "TrainingJobSummaryTypeDef",
    "ListTrainingJobsResponseTypeDef",
    "TransformJobSummaryTypeDef",
    "ListTransformJobsResponseTypeDef",
    "TrialComponentSummaryTypeDef",
    "ListTrialComponentsResponseTypeDef",
    "TrialSummaryTypeDef",
    "ListTrialsResponseTypeDef",
    "UserProfileDetailsTypeDef",
    "ListUserProfilesResponseTypeDef",
    "ListWorkteamsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RenderingErrorTypeDef",
    "RenderUiTemplateResponseTypeDef",
    "RenderableTaskTypeDef",
    "RetentionPolicyTypeDef",
    "FilterTypeDef",
    "NestedFiltersTypeDef",
    "SearchExpressionTypeDef",
    "ExperimentTypeDef",
    "TrainingJobTypeDef",
    "ParentTypeDef",
    "TrialComponentSourceDetailTypeDef",
    "TrialComponentTypeDef",
    "TrialComponentSimpleSummaryTypeDef",
    "TrialTypeDef",
    "SearchRecordTypeDef",
    "SearchResponseTypeDef",
    "PropertyNameQueryTypeDef",
    "SuggestionQueryTypeDef",
    "UiTemplateTypeDef",
    "UpdateCodeRepositoryOutputTypeDef",
    "UpdateDomainResponseTypeDef",
    "UpdateEndpointOutputTypeDef",
    "UpdateEndpointWeightsAndCapacitiesOutputTypeDef",
    "UpdateExperimentResponseTypeDef",
    "UpdateMonitoringScheduleResponseTypeDef",
    "UpdateTrialComponentResponseTypeDef",
    "UpdateTrialResponseTypeDef",
    "UpdateUserProfileResponseTypeDef",
    "UpdateWorkforceResponseTypeDef",
    "UpdateWorkteamResponseTypeDef",
    "VariantPropertyTypeDef",
    "WaiterConfigTypeDef",
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

AddTagsOutputTypeDef = TypedDict("AddTagsOutputTypeDef", {"Tags": List[TagTypeDef]}, total=False)

MetricDefinitionTypeDef = TypedDict("MetricDefinitionTypeDef", {"Name": str, "Regex": str})

_RequiredAlgorithmSpecificationTypeDef = TypedDict(
    "_RequiredAlgorithmSpecificationTypeDef", {"TrainingInputMode": Literal["Pipe", "File"]}
)
_OptionalAlgorithmSpecificationTypeDef = TypedDict(
    "_OptionalAlgorithmSpecificationTypeDef",
    {
        "TrainingImage": str,
        "AlgorithmName": str,
        "MetricDefinitions": List[MetricDefinitionTypeDef],
        "EnableSageMakerMetricsTimeSeries": bool,
    },
    total=False,
)


class AlgorithmSpecificationTypeDef(
    _RequiredAlgorithmSpecificationTypeDef, _OptionalAlgorithmSpecificationTypeDef
):
    pass


FileSystemDataSourceTypeDef = TypedDict(
    "FileSystemDataSourceTypeDef",
    {
        "FileSystemId": str,
        "FileSystemAccessMode": Literal["rw", "ro"],
        "FileSystemType": Literal["EFS", "FSxLustre"],
        "DirectoryPath": str,
    },
)

_RequiredS3DataSourceTypeDef = TypedDict(
    "_RequiredS3DataSourceTypeDef",
    {"S3DataType": Literal["ManifestFile", "S3Prefix", "AugmentedManifestFile"], "S3Uri": str},
)
_OptionalS3DataSourceTypeDef = TypedDict(
    "_OptionalS3DataSourceTypeDef",
    {
        "S3DataDistributionType": Literal["FullyReplicated", "ShardedByS3Key"],
        "AttributeNames": List[str],
    },
    total=False,
)


class S3DataSourceTypeDef(_RequiredS3DataSourceTypeDef, _OptionalS3DataSourceTypeDef):
    pass


DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {"S3DataSource": S3DataSourceTypeDef, "FileSystemDataSource": FileSystemDataSourceTypeDef},
    total=False,
)

ShuffleConfigTypeDef = TypedDict("ShuffleConfigTypeDef", {"Seed": int})

_RequiredChannelTypeDef = TypedDict(
    "_RequiredChannelTypeDef", {"ChannelName": str, "DataSource": DataSourceTypeDef}
)
_OptionalChannelTypeDef = TypedDict(
    "_OptionalChannelTypeDef",
    {
        "ContentType": str,
        "CompressionType": Literal["None", "Gzip"],
        "RecordWrapperType": Literal["None", "RecordIO"],
        "InputMode": Literal["Pipe", "File"],
        "ShuffleConfig": ShuffleConfigTypeDef,
    },
    total=False,
)


class ChannelTypeDef(_RequiredChannelTypeDef, _OptionalChannelTypeDef):
    pass


_RequiredOutputDataConfigTypeDef = TypedDict(
    "_RequiredOutputDataConfigTypeDef", {"S3OutputPath": str}
)
_OptionalOutputDataConfigTypeDef = TypedDict(
    "_OptionalOutputDataConfigTypeDef", {"KmsKeyId": str}, total=False
)


class OutputDataConfigTypeDef(_RequiredOutputDataConfigTypeDef, _OptionalOutputDataConfigTypeDef):
    pass


_RequiredResourceConfigTypeDef = TypedDict(
    "_RequiredResourceConfigTypeDef",
    {
        "InstanceType": Literal[
            "ml.m4.xlarge",
            "ml.m4.2xlarge",
            "ml.m4.4xlarge",
            "ml.m4.10xlarge",
            "ml.m4.16xlarge",
            "ml.g4dn.xlarge",
            "ml.g4dn.2xlarge",
            "ml.g4dn.4xlarge",
            "ml.g4dn.8xlarge",
            "ml.g4dn.12xlarge",
            "ml.g4dn.16xlarge",
            "ml.m5.large",
            "ml.m5.xlarge",
            "ml.m5.2xlarge",
            "ml.m5.4xlarge",
            "ml.m5.12xlarge",
            "ml.m5.24xlarge",
            "ml.c4.xlarge",
            "ml.c4.2xlarge",
            "ml.c4.4xlarge",
            "ml.c4.8xlarge",
            "ml.p2.xlarge",
            "ml.p2.8xlarge",
            "ml.p2.16xlarge",
            "ml.p3.2xlarge",
            "ml.p3.8xlarge",
            "ml.p3.16xlarge",
            "ml.p3dn.24xlarge",
            "ml.c5.xlarge",
            "ml.c5.2xlarge",
            "ml.c5.4xlarge",
            "ml.c5.9xlarge",
            "ml.c5.18xlarge",
        ],
        "InstanceCount": int,
        "VolumeSizeInGB": int,
    },
)
_OptionalResourceConfigTypeDef = TypedDict(
    "_OptionalResourceConfigTypeDef", {"VolumeKmsKeyId": str}, total=False
)


class ResourceConfigTypeDef(_RequiredResourceConfigTypeDef, _OptionalResourceConfigTypeDef):
    pass


StoppingConditionTypeDef = TypedDict(
    "StoppingConditionTypeDef",
    {"MaxRuntimeInSeconds": int, "MaxWaitTimeInSeconds": int},
    total=False,
)

_RequiredTrainingJobDefinitionTypeDef = TypedDict(
    "_RequiredTrainingJobDefinitionTypeDef",
    {
        "TrainingInputMode": Literal["Pipe", "File"],
        "InputDataConfig": List[ChannelTypeDef],
        "OutputDataConfig": OutputDataConfigTypeDef,
        "ResourceConfig": ResourceConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
    },
)
_OptionalTrainingJobDefinitionTypeDef = TypedDict(
    "_OptionalTrainingJobDefinitionTypeDef", {"HyperParameters": Dict[str, str]}, total=False
)


class TrainingJobDefinitionTypeDef(
    _RequiredTrainingJobDefinitionTypeDef, _OptionalTrainingJobDefinitionTypeDef
):
    pass


TransformS3DataSourceTypeDef = TypedDict(
    "TransformS3DataSourceTypeDef",
    {"S3DataType": Literal["ManifestFile", "S3Prefix", "AugmentedManifestFile"], "S3Uri": str},
)

TransformDataSourceTypeDef = TypedDict(
    "TransformDataSourceTypeDef", {"S3DataSource": TransformS3DataSourceTypeDef}
)

_RequiredTransformInputTypeDef = TypedDict(
    "_RequiredTransformInputTypeDef", {"DataSource": TransformDataSourceTypeDef}
)
_OptionalTransformInputTypeDef = TypedDict(
    "_OptionalTransformInputTypeDef",
    {
        "ContentType": str,
        "CompressionType": Literal["None", "Gzip"],
        "SplitType": Literal["None", "Line", "RecordIO", "TFRecord"],
    },
    total=False,
)


class TransformInputTypeDef(_RequiredTransformInputTypeDef, _OptionalTransformInputTypeDef):
    pass


_RequiredTransformOutputTypeDef = TypedDict(
    "_RequiredTransformOutputTypeDef", {"S3OutputPath": str}
)
_OptionalTransformOutputTypeDef = TypedDict(
    "_OptionalTransformOutputTypeDef",
    {"Accept": str, "AssembleWith": Literal["None", "Line"], "KmsKeyId": str},
    total=False,
)


class TransformOutputTypeDef(_RequiredTransformOutputTypeDef, _OptionalTransformOutputTypeDef):
    pass


_RequiredTransformResourcesTypeDef = TypedDict(
    "_RequiredTransformResourcesTypeDef",
    {
        "InstanceType": Literal[
            "ml.m4.xlarge",
            "ml.m4.2xlarge",
            "ml.m4.4xlarge",
            "ml.m4.10xlarge",
            "ml.m4.16xlarge",
            "ml.c4.xlarge",
            "ml.c4.2xlarge",
            "ml.c4.4xlarge",
            "ml.c4.8xlarge",
            "ml.p2.xlarge",
            "ml.p2.8xlarge",
            "ml.p2.16xlarge",
            "ml.p3.2xlarge",
            "ml.p3.8xlarge",
            "ml.p3.16xlarge",
            "ml.c5.xlarge",
            "ml.c5.2xlarge",
            "ml.c5.4xlarge",
            "ml.c5.9xlarge",
            "ml.c5.18xlarge",
            "ml.m5.large",
            "ml.m5.xlarge",
            "ml.m5.2xlarge",
            "ml.m5.4xlarge",
            "ml.m5.12xlarge",
            "ml.m5.24xlarge",
        ],
        "InstanceCount": int,
    },
)
_OptionalTransformResourcesTypeDef = TypedDict(
    "_OptionalTransformResourcesTypeDef", {"VolumeKmsKeyId": str}, total=False
)


class TransformResourcesTypeDef(
    _RequiredTransformResourcesTypeDef, _OptionalTransformResourcesTypeDef
):
    pass


_RequiredTransformJobDefinitionTypeDef = TypedDict(
    "_RequiredTransformJobDefinitionTypeDef",
    {
        "TransformInput": TransformInputTypeDef,
        "TransformOutput": TransformOutputTypeDef,
        "TransformResources": TransformResourcesTypeDef,
    },
)
_OptionalTransformJobDefinitionTypeDef = TypedDict(
    "_OptionalTransformJobDefinitionTypeDef",
    {
        "MaxConcurrentTransforms": int,
        "MaxPayloadInMB": int,
        "BatchStrategy": Literal["MultiRecord", "SingleRecord"],
        "Environment": Dict[str, str],
    },
    total=False,
)


class TransformJobDefinitionTypeDef(
    _RequiredTransformJobDefinitionTypeDef, _OptionalTransformJobDefinitionTypeDef
):
    pass


_RequiredAlgorithmValidationProfileTypeDef = TypedDict(
    "_RequiredAlgorithmValidationProfileTypeDef",
    {"ProfileName": str, "TrainingJobDefinition": TrainingJobDefinitionTypeDef},
)
_OptionalAlgorithmValidationProfileTypeDef = TypedDict(
    "_OptionalAlgorithmValidationProfileTypeDef",
    {"TransformJobDefinition": TransformJobDefinitionTypeDef},
    total=False,
)


class AlgorithmValidationProfileTypeDef(
    _RequiredAlgorithmValidationProfileTypeDef, _OptionalAlgorithmValidationProfileTypeDef
):
    pass


AlgorithmValidationSpecificationTypeDef = TypedDict(
    "AlgorithmValidationSpecificationTypeDef",
    {"ValidationRole": str, "ValidationProfiles": List[AlgorithmValidationProfileTypeDef]},
)

_RequiredAppSpecificationTypeDef = TypedDict("_RequiredAppSpecificationTypeDef", {"ImageUri": str})
_OptionalAppSpecificationTypeDef = TypedDict(
    "_OptionalAppSpecificationTypeDef",
    {"ContainerEntrypoint": List[str], "ContainerArguments": List[str]},
    total=False,
)


class AppSpecificationTypeDef(_RequiredAppSpecificationTypeDef, _OptionalAppSpecificationTypeDef):
    pass


AssociateTrialComponentResponseTypeDef = TypedDict(
    "AssociateTrialComponentResponseTypeDef",
    {"TrialComponentArn": str, "TrialArn": str},
    total=False,
)

AutoMLS3DataSourceTypeDef = TypedDict(
    "AutoMLS3DataSourceTypeDef", {"S3DataType": Literal["ManifestFile", "S3Prefix"], "S3Uri": str}
)

AutoMLDataSourceTypeDef = TypedDict(
    "AutoMLDataSourceTypeDef", {"S3DataSource": AutoMLS3DataSourceTypeDef}
)

_RequiredAutoMLChannelTypeDef = TypedDict(
    "_RequiredAutoMLChannelTypeDef",
    {"DataSource": AutoMLDataSourceTypeDef, "TargetAttributeName": str},
)
_OptionalAutoMLChannelTypeDef = TypedDict(
    "_OptionalAutoMLChannelTypeDef", {"CompressionType": Literal["None", "Gzip"]}, total=False
)


class AutoMLChannelTypeDef(_RequiredAutoMLChannelTypeDef, _OptionalAutoMLChannelTypeDef):
    pass


AutoMLJobCompletionCriteriaTypeDef = TypedDict(
    "AutoMLJobCompletionCriteriaTypeDef",
    {
        "MaxCandidates": int,
        "MaxRuntimePerTrainingJobInSeconds": int,
        "MaxAutoMLJobRuntimeInSeconds": int,
    },
    total=False,
)

VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef", {"SecurityGroupIds": List[str], "Subnets": List[str]}
)

AutoMLSecurityConfigTypeDef = TypedDict(
    "AutoMLSecurityConfigTypeDef",
    {
        "VolumeKmsKeyId": str,
        "EnableInterContainerTrafficEncryption": bool,
        "VpcConfig": VpcConfigTypeDef,
    },
    total=False,
)

AutoMLJobConfigTypeDef = TypedDict(
    "AutoMLJobConfigTypeDef",
    {
        "CompletionCriteria": AutoMLJobCompletionCriteriaTypeDef,
        "SecurityConfig": AutoMLSecurityConfigTypeDef,
    },
    total=False,
)

AutoMLJobObjectiveTypeDef = TypedDict(
    "AutoMLJobObjectiveTypeDef", {"MetricName": Literal["Accuracy", "MSE", "F1", "F1macro"]}
)

_RequiredAutoMLOutputDataConfigTypeDef = TypedDict(
    "_RequiredAutoMLOutputDataConfigTypeDef", {"S3OutputPath": str}
)
_OptionalAutoMLOutputDataConfigTypeDef = TypedDict(
    "_OptionalAutoMLOutputDataConfigTypeDef", {"KmsKeyId": str}, total=False
)


class AutoMLOutputDataConfigTypeDef(
    _RequiredAutoMLOutputDataConfigTypeDef, _OptionalAutoMLOutputDataConfigTypeDef
):
    pass


_RequiredCheckpointConfigTypeDef = TypedDict("_RequiredCheckpointConfigTypeDef", {"S3Uri": str})
_OptionalCheckpointConfigTypeDef = TypedDict(
    "_OptionalCheckpointConfigTypeDef", {"LocalPath": str}, total=False
)


class CheckpointConfigTypeDef(_RequiredCheckpointConfigTypeDef, _OptionalCheckpointConfigTypeDef):
    pass


ContainerDefinitionTypeDef = TypedDict(
    "ContainerDefinitionTypeDef",
    {
        "ContainerHostname": str,
        "Image": str,
        "Mode": Literal["SingleModel", "MultiModel"],
        "ModelDataUrl": str,
        "Environment": Dict[str, str],
        "ModelPackageName": str,
    },
    total=False,
)

CreateAlgorithmOutputTypeDef = TypedDict("CreateAlgorithmOutputTypeDef", {"AlgorithmArn": str})

CreateAppResponseTypeDef = TypedDict("CreateAppResponseTypeDef", {"AppArn": str}, total=False)

CreateAutoMLJobResponseTypeDef = TypedDict("CreateAutoMLJobResponseTypeDef", {"AutoMLJobArn": str})

CreateCodeRepositoryOutputTypeDef = TypedDict(
    "CreateCodeRepositoryOutputTypeDef", {"CodeRepositoryArn": str}
)

CreateCompilationJobResponseTypeDef = TypedDict(
    "CreateCompilationJobResponseTypeDef", {"CompilationJobArn": str}
)

CreateDomainResponseTypeDef = TypedDict(
    "CreateDomainResponseTypeDef", {"DomainArn": str, "Url": str}, total=False
)

CreateEndpointConfigOutputTypeDef = TypedDict(
    "CreateEndpointConfigOutputTypeDef", {"EndpointConfigArn": str}
)

CreateEndpointOutputTypeDef = TypedDict("CreateEndpointOutputTypeDef", {"EndpointArn": str})

CreateExperimentResponseTypeDef = TypedDict(
    "CreateExperimentResponseTypeDef", {"ExperimentArn": str}, total=False
)

CreateFlowDefinitionResponseTypeDef = TypedDict(
    "CreateFlowDefinitionResponseTypeDef", {"FlowDefinitionArn": str}
)

CreateHumanTaskUiResponseTypeDef = TypedDict(
    "CreateHumanTaskUiResponseTypeDef", {"HumanTaskUiArn": str}
)

CreateHyperParameterTuningJobResponseTypeDef = TypedDict(
    "CreateHyperParameterTuningJobResponseTypeDef", {"HyperParameterTuningJobArn": str}
)

CreateLabelingJobResponseTypeDef = TypedDict(
    "CreateLabelingJobResponseTypeDef", {"LabelingJobArn": str}
)

CreateModelOutputTypeDef = TypedDict("CreateModelOutputTypeDef", {"ModelArn": str})

CreateModelPackageOutputTypeDef = TypedDict(
    "CreateModelPackageOutputTypeDef", {"ModelPackageArn": str}
)

CreateMonitoringScheduleResponseTypeDef = TypedDict(
    "CreateMonitoringScheduleResponseTypeDef", {"MonitoringScheduleArn": str}
)

CreateNotebookInstanceLifecycleConfigOutputTypeDef = TypedDict(
    "CreateNotebookInstanceLifecycleConfigOutputTypeDef",
    {"NotebookInstanceLifecycleConfigArn": str},
    total=False,
)

CreateNotebookInstanceOutputTypeDef = TypedDict(
    "CreateNotebookInstanceOutputTypeDef", {"NotebookInstanceArn": str}, total=False
)

CreatePresignedDomainUrlResponseTypeDef = TypedDict(
    "CreatePresignedDomainUrlResponseTypeDef", {"AuthorizedUrl": str}, total=False
)

CreatePresignedNotebookInstanceUrlOutputTypeDef = TypedDict(
    "CreatePresignedNotebookInstanceUrlOutputTypeDef", {"AuthorizedUrl": str}, total=False
)

CreateProcessingJobResponseTypeDef = TypedDict(
    "CreateProcessingJobResponseTypeDef", {"ProcessingJobArn": str}
)

CreateTrainingJobResponseTypeDef = TypedDict(
    "CreateTrainingJobResponseTypeDef", {"TrainingJobArn": str}
)

CreateTransformJobResponseTypeDef = TypedDict(
    "CreateTransformJobResponseTypeDef", {"TransformJobArn": str}
)

CreateTrialComponentResponseTypeDef = TypedDict(
    "CreateTrialComponentResponseTypeDef", {"TrialComponentArn": str}, total=False
)

CreateTrialResponseTypeDef = TypedDict("CreateTrialResponseTypeDef", {"TrialArn": str}, total=False)

CreateUserProfileResponseTypeDef = TypedDict(
    "CreateUserProfileResponseTypeDef", {"UserProfileArn": str}, total=False
)

CreateWorkteamResponseTypeDef = TypedDict(
    "CreateWorkteamResponseTypeDef", {"WorkteamArn": str}, total=False
)

CaptureContentTypeHeaderTypeDef = TypedDict(
    "CaptureContentTypeHeaderTypeDef",
    {"CsvContentTypes": List[str], "JsonContentTypes": List[str]},
    total=False,
)

CaptureOptionTypeDef = TypedDict(
    "CaptureOptionTypeDef", {"CaptureMode": Literal["Input", "Output"]}
)

_RequiredDataCaptureConfigTypeDef = TypedDict(
    "_RequiredDataCaptureConfigTypeDef",
    {
        "InitialSamplingPercentage": int,
        "DestinationS3Uri": str,
        "CaptureOptions": List[CaptureOptionTypeDef],
    },
)
_OptionalDataCaptureConfigTypeDef = TypedDict(
    "_OptionalDataCaptureConfigTypeDef",
    {
        "EnableCapture": bool,
        "KmsKeyId": str,
        "CaptureContentTypeHeader": CaptureContentTypeHeaderTypeDef,
    },
    total=False,
)


class DataCaptureConfigTypeDef(
    _RequiredDataCaptureConfigTypeDef, _OptionalDataCaptureConfigTypeDef
):
    pass


DataProcessingTypeDef = TypedDict(
    "DataProcessingTypeDef",
    {"InputFilter": str, "OutputFilter": str, "JoinSource": Literal["Input", "None"]},
    total=False,
)

CollectionConfigurationTypeDef = TypedDict(
    "CollectionConfigurationTypeDef",
    {"CollectionName": str, "CollectionParameters": Dict[str, str]},
    total=False,
)

_RequiredDebugHookConfigTypeDef = TypedDict(
    "_RequiredDebugHookConfigTypeDef", {"S3OutputPath": str}
)
_OptionalDebugHookConfigTypeDef = TypedDict(
    "_OptionalDebugHookConfigTypeDef",
    {
        "LocalPath": str,
        "HookParameters": Dict[str, str],
        "CollectionConfigurations": List[CollectionConfigurationTypeDef],
    },
    total=False,
)


class DebugHookConfigTypeDef(_RequiredDebugHookConfigTypeDef, _OptionalDebugHookConfigTypeDef):
    pass


_RequiredDebugRuleConfigurationTypeDef = TypedDict(
    "_RequiredDebugRuleConfigurationTypeDef",
    {"RuleConfigurationName": str, "RuleEvaluatorImage": str},
)
_OptionalDebugRuleConfigurationTypeDef = TypedDict(
    "_OptionalDebugRuleConfigurationTypeDef",
    {
        "LocalPath": str,
        "S3OutputPath": str,
        "InstanceType": Literal[
            "ml.t3.medium",
            "ml.t3.large",
            "ml.t3.xlarge",
            "ml.t3.2xlarge",
            "ml.m4.xlarge",
            "ml.m4.2xlarge",
            "ml.m4.4xlarge",
            "ml.m4.10xlarge",
            "ml.m4.16xlarge",
            "ml.c4.xlarge",
            "ml.c4.2xlarge",
            "ml.c4.4xlarge",
            "ml.c4.8xlarge",
            "ml.p2.xlarge",
            "ml.p2.8xlarge",
            "ml.p2.16xlarge",
            "ml.p3.2xlarge",
            "ml.p3.8xlarge",
            "ml.p3.16xlarge",
            "ml.c5.xlarge",
            "ml.c5.2xlarge",
            "ml.c5.4xlarge",
            "ml.c5.9xlarge",
            "ml.c5.18xlarge",
            "ml.m5.large",
            "ml.m5.xlarge",
            "ml.m5.2xlarge",
            "ml.m5.4xlarge",
            "ml.m5.12xlarge",
            "ml.m5.24xlarge",
            "ml.r5.large",
            "ml.r5.xlarge",
            "ml.r5.2xlarge",
            "ml.r5.4xlarge",
            "ml.r5.8xlarge",
            "ml.r5.12xlarge",
            "ml.r5.16xlarge",
            "ml.r5.24xlarge",
        ],
        "VolumeSizeInGB": int,
        "RuleParameters": Dict[str, str],
    },
    total=False,
)


class DebugRuleConfigurationTypeDef(
    _RequiredDebugRuleConfigurationTypeDef, _OptionalDebugRuleConfigurationTypeDef
):
    pass


DeleteExperimentResponseTypeDef = TypedDict(
    "DeleteExperimentResponseTypeDef", {"ExperimentArn": str}, total=False
)

DeleteTrialComponentResponseTypeDef = TypedDict(
    "DeleteTrialComponentResponseTypeDef", {"TrialComponentArn": str}, total=False
)

DeleteTrialResponseTypeDef = TypedDict("DeleteTrialResponseTypeDef", {"TrialArn": str}, total=False)

DeleteWorkteamResponseTypeDef = TypedDict("DeleteWorkteamResponseTypeDef", {"Success": bool})

_RequiredAlgorithmStatusItemTypeDef = TypedDict(
    "_RequiredAlgorithmStatusItemTypeDef",
    {"Name": str, "Status": Literal["NotStarted", "InProgress", "Completed", "Failed"]},
)
_OptionalAlgorithmStatusItemTypeDef = TypedDict(
    "_OptionalAlgorithmStatusItemTypeDef", {"FailureReason": str}, total=False
)


class AlgorithmStatusItemTypeDef(
    _RequiredAlgorithmStatusItemTypeDef, _OptionalAlgorithmStatusItemTypeDef
):
    pass


AlgorithmStatusDetailsTypeDef = TypedDict(
    "AlgorithmStatusDetailsTypeDef",
    {
        "ValidationStatuses": List[AlgorithmStatusItemTypeDef],
        "ImageScanStatuses": List[AlgorithmStatusItemTypeDef],
    },
    total=False,
)

_RequiredModelPackageContainerDefinitionTypeDef = TypedDict(
    "_RequiredModelPackageContainerDefinitionTypeDef", {"Image": str}
)
_OptionalModelPackageContainerDefinitionTypeDef = TypedDict(
    "_OptionalModelPackageContainerDefinitionTypeDef",
    {"ContainerHostname": str, "ImageDigest": str, "ModelDataUrl": str, "ProductId": str},
    total=False,
)


class ModelPackageContainerDefinitionTypeDef(
    _RequiredModelPackageContainerDefinitionTypeDef, _OptionalModelPackageContainerDefinitionTypeDef
):
    pass


InferenceSpecificationTypeDef = TypedDict(
    "InferenceSpecificationTypeDef",
    {
        "Containers": List[ModelPackageContainerDefinitionTypeDef],
        "SupportedTransformInstanceTypes": List[
            Literal[
                "ml.m4.xlarge",
                "ml.m4.2xlarge",
                "ml.m4.4xlarge",
                "ml.m4.10xlarge",
                "ml.m4.16xlarge",
                "ml.c4.xlarge",
                "ml.c4.2xlarge",
                "ml.c4.4xlarge",
                "ml.c4.8xlarge",
                "ml.p2.xlarge",
                "ml.p2.8xlarge",
                "ml.p2.16xlarge",
                "ml.p3.2xlarge",
                "ml.p3.8xlarge",
                "ml.p3.16xlarge",
                "ml.c5.xlarge",
                "ml.c5.2xlarge",
                "ml.c5.4xlarge",
                "ml.c5.9xlarge",
                "ml.c5.18xlarge",
                "ml.m5.large",
                "ml.m5.xlarge",
                "ml.m5.2xlarge",
                "ml.m5.4xlarge",
                "ml.m5.12xlarge",
                "ml.m5.24xlarge",
            ]
        ],
        "SupportedRealtimeInferenceInstanceTypes": List[
            Literal[
                "ml.t2.medium",
                "ml.t2.large",
                "ml.t2.xlarge",
                "ml.t2.2xlarge",
                "ml.m4.xlarge",
                "ml.m4.2xlarge",
                "ml.m4.4xlarge",
                "ml.m4.10xlarge",
                "ml.m4.16xlarge",
                "ml.m5.large",
                "ml.m5.xlarge",
                "ml.m5.2xlarge",
                "ml.m5.4xlarge",
                "ml.m5.12xlarge",
                "ml.m5.24xlarge",
                "ml.m5d.large",
                "ml.m5d.xlarge",
                "ml.m5d.2xlarge",
                "ml.m5d.4xlarge",
                "ml.m5d.12xlarge",
                "ml.m5d.24xlarge",
                "ml.c4.large",
                "ml.c4.xlarge",
                "ml.c4.2xlarge",
                "ml.c4.4xlarge",
                "ml.c4.8xlarge",
                "ml.p2.xlarge",
                "ml.p2.8xlarge",
                "ml.p2.16xlarge",
                "ml.p3.2xlarge",
                "ml.p3.8xlarge",
                "ml.p3.16xlarge",
                "ml.c5.large",
                "ml.c5.xlarge",
                "ml.c5.2xlarge",
                "ml.c5.4xlarge",
                "ml.c5.9xlarge",
                "ml.c5.18xlarge",
                "ml.c5d.large",
                "ml.c5d.xlarge",
                "ml.c5d.2xlarge",
                "ml.c5d.4xlarge",
                "ml.c5d.9xlarge",
                "ml.c5d.18xlarge",
                "ml.g4dn.xlarge",
                "ml.g4dn.2xlarge",
                "ml.g4dn.4xlarge",
                "ml.g4dn.8xlarge",
                "ml.g4dn.12xlarge",
                "ml.g4dn.16xlarge",
                "ml.r5.large",
                "ml.r5.xlarge",
                "ml.r5.2xlarge",
                "ml.r5.4xlarge",
                "ml.r5.12xlarge",
                "ml.r5.24xlarge",
                "ml.r5d.large",
                "ml.r5d.xlarge",
                "ml.r5d.2xlarge",
                "ml.r5d.4xlarge",
                "ml.r5d.12xlarge",
                "ml.r5d.24xlarge",
                "ml.inf1.xlarge",
                "ml.inf1.2xlarge",
                "ml.inf1.6xlarge",
                "ml.inf1.24xlarge",
            ]
        ],
        "SupportedContentTypes": List[str],
        "SupportedResponseMIMETypes": List[str],
    },
)

_RequiredChannelSpecificationTypeDef = TypedDict(
    "_RequiredChannelSpecificationTypeDef",
    {
        "Name": str,
        "SupportedContentTypes": List[str],
        "SupportedInputModes": List[Literal["Pipe", "File"]],
    },
)
_OptionalChannelSpecificationTypeDef = TypedDict(
    "_OptionalChannelSpecificationTypeDef",
    {
        "Description": str,
        "IsRequired": bool,
        "SupportedCompressionTypes": List[Literal["None", "Gzip"]],
    },
    total=False,
)


class ChannelSpecificationTypeDef(
    _RequiredChannelSpecificationTypeDef, _OptionalChannelSpecificationTypeDef
):
    pass


CategoricalParameterRangeSpecificationTypeDef = TypedDict(
    "CategoricalParameterRangeSpecificationTypeDef", {"Values": List[str]}
)

ContinuousParameterRangeSpecificationTypeDef = TypedDict(
    "ContinuousParameterRangeSpecificationTypeDef", {"MinValue": str, "MaxValue": str}
)

IntegerParameterRangeSpecificationTypeDef = TypedDict(
    "IntegerParameterRangeSpecificationTypeDef", {"MinValue": str, "MaxValue": str}
)

ParameterRangeTypeDef = TypedDict(
    "ParameterRangeTypeDef",
    {
        "IntegerParameterRangeSpecification": IntegerParameterRangeSpecificationTypeDef,
        "ContinuousParameterRangeSpecification": ContinuousParameterRangeSpecificationTypeDef,
        "CategoricalParameterRangeSpecification": CategoricalParameterRangeSpecificationTypeDef,
    },
    total=False,
)

_RequiredHyperParameterSpecificationTypeDef = TypedDict(
    "_RequiredHyperParameterSpecificationTypeDef",
    {"Name": str, "Type": Literal["Integer", "Continuous", "Categorical", "FreeText"]},
)
_OptionalHyperParameterSpecificationTypeDef = TypedDict(
    "_OptionalHyperParameterSpecificationTypeDef",
    {
        "Description": str,
        "Range": ParameterRangeTypeDef,
        "IsTunable": bool,
        "IsRequired": bool,
        "DefaultValue": str,
    },
    total=False,
)


class HyperParameterSpecificationTypeDef(
    _RequiredHyperParameterSpecificationTypeDef, _OptionalHyperParameterSpecificationTypeDef
):
    pass


HyperParameterTuningJobObjectiveTypeDef = TypedDict(
    "HyperParameterTuningJobObjectiveTypeDef",
    {"Type": Literal["Maximize", "Minimize"], "MetricName": str},
)

_RequiredTrainingSpecificationTypeDef = TypedDict(
    "_RequiredTrainingSpecificationTypeDef",
    {
        "TrainingImage": str,
        "SupportedTrainingInstanceTypes": List[
            Literal[
                "ml.m4.xlarge",
                "ml.m4.2xlarge",
                "ml.m4.4xlarge",
                "ml.m4.10xlarge",
                "ml.m4.16xlarge",
                "ml.g4dn.xlarge",
                "ml.g4dn.2xlarge",
                "ml.g4dn.4xlarge",
                "ml.g4dn.8xlarge",
                "ml.g4dn.12xlarge",
                "ml.g4dn.16xlarge",
                "ml.m5.large",
                "ml.m5.xlarge",
                "ml.m5.2xlarge",
                "ml.m5.4xlarge",
                "ml.m5.12xlarge",
                "ml.m5.24xlarge",
                "ml.c4.xlarge",
                "ml.c4.2xlarge",
                "ml.c4.4xlarge",
                "ml.c4.8xlarge",
                "ml.p2.xlarge",
                "ml.p2.8xlarge",
                "ml.p2.16xlarge",
                "ml.p3.2xlarge",
                "ml.p3.8xlarge",
                "ml.p3.16xlarge",
                "ml.p3dn.24xlarge",
                "ml.c5.xlarge",
                "ml.c5.2xlarge",
                "ml.c5.4xlarge",
                "ml.c5.9xlarge",
                "ml.c5.18xlarge",
            ]
        ],
        "TrainingChannels": List[ChannelSpecificationTypeDef],
    },
)
_OptionalTrainingSpecificationTypeDef = TypedDict(
    "_OptionalTrainingSpecificationTypeDef",
    {
        "TrainingImageDigest": str,
        "SupportedHyperParameters": List[HyperParameterSpecificationTypeDef],
        "SupportsDistributedTraining": bool,
        "MetricDefinitions": List[MetricDefinitionTypeDef],
        "SupportedTuningJobObjectiveMetrics": List[HyperParameterTuningJobObjectiveTypeDef],
    },
    total=False,
)


class TrainingSpecificationTypeDef(
    _RequiredTrainingSpecificationTypeDef, _OptionalTrainingSpecificationTypeDef
):
    pass


_RequiredDescribeAlgorithmOutputTypeDef = TypedDict(
    "_RequiredDescribeAlgorithmOutputTypeDef",
    {
        "AlgorithmName": str,
        "AlgorithmArn": str,
        "CreationTime": datetime,
        "TrainingSpecification": TrainingSpecificationTypeDef,
        "AlgorithmStatus": Literal["Pending", "InProgress", "Completed", "Failed", "Deleting"],
        "AlgorithmStatusDetails": AlgorithmStatusDetailsTypeDef,
    },
)
_OptionalDescribeAlgorithmOutputTypeDef = TypedDict(
    "_OptionalDescribeAlgorithmOutputTypeDef",
    {
        "AlgorithmDescription": str,
        "InferenceSpecification": InferenceSpecificationTypeDef,
        "ValidationSpecification": AlgorithmValidationSpecificationTypeDef,
        "ProductId": str,
        "CertifyForMarketplace": bool,
    },
    total=False,
)


class DescribeAlgorithmOutputTypeDef(
    _RequiredDescribeAlgorithmOutputTypeDef, _OptionalDescribeAlgorithmOutputTypeDef
):
    pass


ResourceSpecTypeDef = TypedDict(
    "ResourceSpecTypeDef",
    {
        "EnvironmentArn": str,
        "InstanceType": Literal[
            "system",
            "ml.t3.micro",
            "ml.t3.small",
            "ml.t3.medium",
            "ml.t3.large",
            "ml.t3.xlarge",
            "ml.t3.2xlarge",
            "ml.m5.large",
            "ml.m5.xlarge",
            "ml.m5.2xlarge",
            "ml.m5.4xlarge",
            "ml.m5.8xlarge",
            "ml.m5.12xlarge",
            "ml.m5.16xlarge",
            "ml.m5.24xlarge",
            "ml.c5.large",
            "ml.c5.xlarge",
            "ml.c5.2xlarge",
            "ml.c5.4xlarge",
            "ml.c5.9xlarge",
            "ml.c5.12xlarge",
            "ml.c5.18xlarge",
            "ml.c5.24xlarge",
            "ml.p3.2xlarge",
            "ml.p3.8xlarge",
            "ml.p3.16xlarge",
            "ml.g4dn.xlarge",
            "ml.g4dn.2xlarge",
            "ml.g4dn.4xlarge",
            "ml.g4dn.8xlarge",
            "ml.g4dn.12xlarge",
            "ml.g4dn.16xlarge",
        ],
    },
    total=False,
)

DescribeAppResponseTypeDef = TypedDict(
    "DescribeAppResponseTypeDef",
    {
        "AppArn": str,
        "AppType": Literal["JupyterServer", "KernelGateway", "TensorBoard"],
        "AppName": str,
        "DomainId": str,
        "UserProfileName": str,
        "Status": Literal["Deleted", "Deleting", "Failed", "InService", "Pending"],
        "LastHealthCheckTimestamp": datetime,
        "LastUserActivityTimestamp": datetime,
        "CreationTime": datetime,
        "FailureReason": str,
        "ResourceSpec": ResourceSpecTypeDef,
    },
    total=False,
)

AutoMLCandidateStepTypeDef = TypedDict(
    "AutoMLCandidateStepTypeDef",
    {
        "CandidateStepType": Literal[
            "AWS::SageMaker::TrainingJob",
            "AWS::SageMaker::TransformJob",
            "AWS::SageMaker::ProcessingJob",
        ],
        "CandidateStepArn": str,
        "CandidateStepName": str,
    },
)

_RequiredAutoMLContainerDefinitionTypeDef = TypedDict(
    "_RequiredAutoMLContainerDefinitionTypeDef", {"Image": str, "ModelDataUrl": str}
)
_OptionalAutoMLContainerDefinitionTypeDef = TypedDict(
    "_OptionalAutoMLContainerDefinitionTypeDef", {"Environment": Dict[str, str]}, total=False
)


class AutoMLContainerDefinitionTypeDef(
    _RequiredAutoMLContainerDefinitionTypeDef, _OptionalAutoMLContainerDefinitionTypeDef
):
    pass


_RequiredFinalAutoMLJobObjectiveMetricTypeDef = TypedDict(
    "_RequiredFinalAutoMLJobObjectiveMetricTypeDef",
    {"MetricName": Literal["Accuracy", "MSE", "F1", "F1macro"], "Value": float},
)
_OptionalFinalAutoMLJobObjectiveMetricTypeDef = TypedDict(
    "_OptionalFinalAutoMLJobObjectiveMetricTypeDef",
    {"Type": Literal["Maximize", "Minimize"]},
    total=False,
)


class FinalAutoMLJobObjectiveMetricTypeDef(
    _RequiredFinalAutoMLJobObjectiveMetricTypeDef, _OptionalFinalAutoMLJobObjectiveMetricTypeDef
):
    pass


_RequiredAutoMLCandidateTypeDef = TypedDict(
    "_RequiredAutoMLCandidateTypeDef",
    {
        "CandidateName": str,
        "ObjectiveStatus": Literal["Succeeded", "Pending", "Failed"],
        "CandidateSteps": List[AutoMLCandidateStepTypeDef],
        "CandidateStatus": Literal["Completed", "InProgress", "Failed", "Stopped", "Stopping"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)
_OptionalAutoMLCandidateTypeDef = TypedDict(
    "_OptionalAutoMLCandidateTypeDef",
    {
        "FinalAutoMLJobObjectiveMetric": FinalAutoMLJobObjectiveMetricTypeDef,
        "InferenceContainers": List[AutoMLContainerDefinitionTypeDef],
        "EndTime": datetime,
        "FailureReason": str,
    },
    total=False,
)


class AutoMLCandidateTypeDef(_RequiredAutoMLCandidateTypeDef, _OptionalAutoMLCandidateTypeDef):
    pass


AutoMLJobArtifactsTypeDef = TypedDict(
    "AutoMLJobArtifactsTypeDef",
    {"CandidateDefinitionNotebookLocation": str, "DataExplorationNotebookLocation": str},
    total=False,
)

ResolvedAttributesTypeDef = TypedDict(
    "ResolvedAttributesTypeDef",
    {
        "AutoMLJobObjective": AutoMLJobObjectiveTypeDef,
        "ProblemType": Literal["BinaryClassification", "MulticlassClassification", "Regression"],
        "CompletionCriteria": AutoMLJobCompletionCriteriaTypeDef,
    },
    total=False,
)

_RequiredDescribeAutoMLJobResponseTypeDef = TypedDict(
    "_RequiredDescribeAutoMLJobResponseTypeDef",
    {
        "AutoMLJobName": str,
        "AutoMLJobArn": str,
        "InputDataConfig": List[AutoMLChannelTypeDef],
        "OutputDataConfig": AutoMLOutputDataConfigTypeDef,
        "RoleArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "AutoMLJobStatus": Literal["Completed", "InProgress", "Failed", "Stopped", "Stopping"],
        "AutoMLJobSecondaryStatus": Literal[
            "Starting",
            "AnalyzingData",
            "FeatureEngineering",
            "ModelTuning",
            "MaxCandidatesReached",
            "Failed",
            "Stopped",
            "MaxAutoMLJobRuntimeReached",
            "Stopping",
            "CandidateDefinitionsGenerated",
        ],
    },
)
_OptionalDescribeAutoMLJobResponseTypeDef = TypedDict(
    "_OptionalDescribeAutoMLJobResponseTypeDef",
    {
        "AutoMLJobObjective": AutoMLJobObjectiveTypeDef,
        "ProblemType": Literal["BinaryClassification", "MulticlassClassification", "Regression"],
        "AutoMLJobConfig": AutoMLJobConfigTypeDef,
        "EndTime": datetime,
        "FailureReason": str,
        "BestCandidate": AutoMLCandidateTypeDef,
        "GenerateCandidateDefinitionsOnly": bool,
        "AutoMLJobArtifacts": AutoMLJobArtifactsTypeDef,
        "ResolvedAttributes": ResolvedAttributesTypeDef,
    },
    total=False,
)


class DescribeAutoMLJobResponseTypeDef(
    _RequiredDescribeAutoMLJobResponseTypeDef, _OptionalDescribeAutoMLJobResponseTypeDef
):
    pass


_RequiredGitConfigTypeDef = TypedDict("_RequiredGitConfigTypeDef", {"RepositoryUrl": str})
_OptionalGitConfigTypeDef = TypedDict(
    "_OptionalGitConfigTypeDef", {"Branch": str, "SecretArn": str}, total=False
)


class GitConfigTypeDef(_RequiredGitConfigTypeDef, _OptionalGitConfigTypeDef):
    pass


_RequiredDescribeCodeRepositoryOutputTypeDef = TypedDict(
    "_RequiredDescribeCodeRepositoryOutputTypeDef",
    {
        "CodeRepositoryName": str,
        "CodeRepositoryArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)
_OptionalDescribeCodeRepositoryOutputTypeDef = TypedDict(
    "_OptionalDescribeCodeRepositoryOutputTypeDef", {"GitConfig": GitConfigTypeDef}, total=False
)


class DescribeCodeRepositoryOutputTypeDef(
    _RequiredDescribeCodeRepositoryOutputTypeDef, _OptionalDescribeCodeRepositoryOutputTypeDef
):
    pass


InputConfigTypeDef = TypedDict(
    "InputConfigTypeDef",
    {
        "S3Uri": str,
        "DataInputConfig": str,
        "Framework": Literal["TENSORFLOW", "KERAS", "MXNET", "ONNX", "PYTORCH", "XGBOOST"],
    },
)

ModelArtifactsTypeDef = TypedDict("ModelArtifactsTypeDef", {"S3ModelArtifacts": str})

OutputConfigTypeDef = TypedDict(
    "OutputConfigTypeDef",
    {
        "S3OutputLocation": str,
        "TargetDevice": Literal[
            "lambda",
            "ml_m4",
            "ml_m5",
            "ml_c4",
            "ml_c5",
            "ml_p2",
            "ml_p3",
            "ml_inf1",
            "jetson_tx1",
            "jetson_tx2",
            "jetson_nano",
            "jetson_xavier",
            "rasp3b",
            "imx8qm",
            "deeplens",
            "rk3399",
            "rk3288",
            "aisage",
            "sbe_c",
            "qcs605",
            "qcs603",
            "sitara_am57x",
            "amba_cv22",
        ],
    },
)

_RequiredDescribeCompilationJobResponseTypeDef = TypedDict(
    "_RequiredDescribeCompilationJobResponseTypeDef",
    {
        "CompilationJobName": str,
        "CompilationJobArn": str,
        "CompilationJobStatus": Literal[
            "INPROGRESS", "COMPLETED", "FAILED", "STARTING", "STOPPING", "STOPPED"
        ],
        "StoppingCondition": StoppingConditionTypeDef,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "ModelArtifacts": ModelArtifactsTypeDef,
        "RoleArn": str,
        "InputConfig": InputConfigTypeDef,
        "OutputConfig": OutputConfigTypeDef,
    },
)
_OptionalDescribeCompilationJobResponseTypeDef = TypedDict(
    "_OptionalDescribeCompilationJobResponseTypeDef",
    {"CompilationStartTime": datetime, "CompilationEndTime": datetime},
    total=False,
)


class DescribeCompilationJobResponseTypeDef(
    _RequiredDescribeCompilationJobResponseTypeDef, _OptionalDescribeCompilationJobResponseTypeDef
):
    pass


JupyterServerAppSettingsTypeDef = TypedDict(
    "JupyterServerAppSettingsTypeDef", {"DefaultResourceSpec": ResourceSpecTypeDef}, total=False
)

KernelGatewayAppSettingsTypeDef = TypedDict(
    "KernelGatewayAppSettingsTypeDef", {"DefaultResourceSpec": ResourceSpecTypeDef}, total=False
)

SharingSettingsTypeDef = TypedDict(
    "SharingSettingsTypeDef",
    {
        "NotebookOutputOption": Literal["Allowed", "Disabled"],
        "S3OutputPath": str,
        "S3KmsKeyId": str,
    },
    total=False,
)

TensorBoardAppSettingsTypeDef = TypedDict(
    "TensorBoardAppSettingsTypeDef", {"DefaultResourceSpec": ResourceSpecTypeDef}, total=False
)

UserSettingsTypeDef = TypedDict(
    "UserSettingsTypeDef",
    {
        "ExecutionRole": str,
        "SecurityGroups": List[str],
        "SharingSettings": SharingSettingsTypeDef,
        "JupyterServerAppSettings": JupyterServerAppSettingsTypeDef,
        "KernelGatewayAppSettings": KernelGatewayAppSettingsTypeDef,
        "TensorBoardAppSettings": TensorBoardAppSettingsTypeDef,
    },
    total=False,
)

DescribeDomainResponseTypeDef = TypedDict(
    "DescribeDomainResponseTypeDef",
    {
        "DomainArn": str,
        "DomainId": str,
        "DomainName": str,
        "HomeEfsFileSystemId": str,
        "SingleSignOnManagedApplicationInstanceId": str,
        "Status": Literal["Deleting", "Failed", "InService", "Pending"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "AuthMode": Literal["SSO", "IAM"],
        "DefaultUserSettings": UserSettingsTypeDef,
        "HomeEfsFileSystemKmsKeyId": str,
        "SubnetIds": List[str],
        "Url": str,
        "VpcId": str,
    },
    total=False,
)

_RequiredProductionVariantTypeDef = TypedDict(
    "_RequiredProductionVariantTypeDef",
    {
        "VariantName": str,
        "ModelName": str,
        "InitialInstanceCount": int,
        "InstanceType": Literal[
            "ml.t2.medium",
            "ml.t2.large",
            "ml.t2.xlarge",
            "ml.t2.2xlarge",
            "ml.m4.xlarge",
            "ml.m4.2xlarge",
            "ml.m4.4xlarge",
            "ml.m4.10xlarge",
            "ml.m4.16xlarge",
            "ml.m5.large",
            "ml.m5.xlarge",
            "ml.m5.2xlarge",
            "ml.m5.4xlarge",
            "ml.m5.12xlarge",
            "ml.m5.24xlarge",
            "ml.m5d.large",
            "ml.m5d.xlarge",
            "ml.m5d.2xlarge",
            "ml.m5d.4xlarge",
            "ml.m5d.12xlarge",
            "ml.m5d.24xlarge",
            "ml.c4.large",
            "ml.c4.xlarge",
            "ml.c4.2xlarge",
            "ml.c4.4xlarge",
            "ml.c4.8xlarge",
            "ml.p2.xlarge",
            "ml.p2.8xlarge",
            "ml.p2.16xlarge",
            "ml.p3.2xlarge",
            "ml.p3.8xlarge",
            "ml.p3.16xlarge",
            "ml.c5.large",
            "ml.c5.xlarge",
            "ml.c5.2xlarge",
            "ml.c5.4xlarge",
            "ml.c5.9xlarge",
            "ml.c5.18xlarge",
            "ml.c5d.large",
            "ml.c5d.xlarge",
            "ml.c5d.2xlarge",
            "ml.c5d.4xlarge",
            "ml.c5d.9xlarge",
            "ml.c5d.18xlarge",
            "ml.g4dn.xlarge",
            "ml.g4dn.2xlarge",
            "ml.g4dn.4xlarge",
            "ml.g4dn.8xlarge",
            "ml.g4dn.12xlarge",
            "ml.g4dn.16xlarge",
            "ml.r5.large",
            "ml.r5.xlarge",
            "ml.r5.2xlarge",
            "ml.r5.4xlarge",
            "ml.r5.12xlarge",
            "ml.r5.24xlarge",
            "ml.r5d.large",
            "ml.r5d.xlarge",
            "ml.r5d.2xlarge",
            "ml.r5d.4xlarge",
            "ml.r5d.12xlarge",
            "ml.r5d.24xlarge",
            "ml.inf1.xlarge",
            "ml.inf1.2xlarge",
            "ml.inf1.6xlarge",
            "ml.inf1.24xlarge",
        ],
    },
)
_OptionalProductionVariantTypeDef = TypedDict(
    "_OptionalProductionVariantTypeDef",
    {
        "InitialVariantWeight": float,
        "AcceleratorType": Literal[
            "ml.eia1.medium",
            "ml.eia1.large",
            "ml.eia1.xlarge",
            "ml.eia2.medium",
            "ml.eia2.large",
            "ml.eia2.xlarge",
        ],
    },
    total=False,
)


class ProductionVariantTypeDef(
    _RequiredProductionVariantTypeDef, _OptionalProductionVariantTypeDef
):
    pass


_RequiredDescribeEndpointConfigOutputTypeDef = TypedDict(
    "_RequiredDescribeEndpointConfigOutputTypeDef",
    {
        "EndpointConfigName": str,
        "EndpointConfigArn": str,
        "ProductionVariants": List[ProductionVariantTypeDef],
        "CreationTime": datetime,
    },
)
_OptionalDescribeEndpointConfigOutputTypeDef = TypedDict(
    "_OptionalDescribeEndpointConfigOutputTypeDef",
    {"DataCaptureConfig": DataCaptureConfigTypeDef, "KmsKeyId": str},
    total=False,
)


class DescribeEndpointConfigOutputTypeDef(
    _RequiredDescribeEndpointConfigOutputTypeDef, _OptionalDescribeEndpointConfigOutputTypeDef
):
    pass


DataCaptureConfigSummaryTypeDef = TypedDict(
    "DataCaptureConfigSummaryTypeDef",
    {
        "EnableCapture": bool,
        "CaptureStatus": Literal["Started", "Stopped"],
        "CurrentSamplingPercentage": int,
        "DestinationS3Uri": str,
        "KmsKeyId": str,
    },
)

DeployedImageTypeDef = TypedDict(
    "DeployedImageTypeDef",
    {"SpecifiedImage": str, "ResolvedImage": str, "ResolutionTime": datetime},
    total=False,
)

_RequiredProductionVariantSummaryTypeDef = TypedDict(
    "_RequiredProductionVariantSummaryTypeDef", {"VariantName": str}
)
_OptionalProductionVariantSummaryTypeDef = TypedDict(
    "_OptionalProductionVariantSummaryTypeDef",
    {
        "DeployedImages": List[DeployedImageTypeDef],
        "CurrentWeight": float,
        "DesiredWeight": float,
        "CurrentInstanceCount": int,
        "DesiredInstanceCount": int,
    },
    total=False,
)


class ProductionVariantSummaryTypeDef(
    _RequiredProductionVariantSummaryTypeDef, _OptionalProductionVariantSummaryTypeDef
):
    pass


_RequiredDescribeEndpointOutputTypeDef = TypedDict(
    "_RequiredDescribeEndpointOutputTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "EndpointConfigName": str,
        "EndpointStatus": Literal[
            "OutOfService",
            "Creating",
            "Updating",
            "SystemUpdating",
            "RollingBack",
            "InService",
            "Deleting",
            "Failed",
        ],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)
_OptionalDescribeEndpointOutputTypeDef = TypedDict(
    "_OptionalDescribeEndpointOutputTypeDef",
    {
        "ProductionVariants": List[ProductionVariantSummaryTypeDef],
        "DataCaptureConfig": DataCaptureConfigSummaryTypeDef,
        "FailureReason": str,
    },
    total=False,
)


class DescribeEndpointOutputTypeDef(
    _RequiredDescribeEndpointOutputTypeDef, _OptionalDescribeEndpointOutputTypeDef
):
    pass


_RequiredExperimentSourceTypeDef = TypedDict("_RequiredExperimentSourceTypeDef", {"SourceArn": str})
_OptionalExperimentSourceTypeDef = TypedDict(
    "_OptionalExperimentSourceTypeDef", {"SourceType": str}, total=False
)


class ExperimentSourceTypeDef(_RequiredExperimentSourceTypeDef, _OptionalExperimentSourceTypeDef):
    pass


UserContextTypeDef = TypedDict(
    "UserContextTypeDef",
    {"UserProfileArn": str, "UserProfileName": str, "DomainId": str},
    total=False,
)

DescribeExperimentResponseTypeDef = TypedDict(
    "DescribeExperimentResponseTypeDef",
    {
        "ExperimentName": str,
        "ExperimentArn": str,
        "DisplayName": str,
        "Source": ExperimentSourceTypeDef,
        "Description": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
    },
    total=False,
)

_RequiredFlowDefinitionOutputConfigTypeDef = TypedDict(
    "_RequiredFlowDefinitionOutputConfigTypeDef", {"S3OutputPath": str}
)
_OptionalFlowDefinitionOutputConfigTypeDef = TypedDict(
    "_OptionalFlowDefinitionOutputConfigTypeDef", {"KmsKeyId": str}, total=False
)


class FlowDefinitionOutputConfigTypeDef(
    _RequiredFlowDefinitionOutputConfigTypeDef, _OptionalFlowDefinitionOutputConfigTypeDef
):
    pass


HumanLoopActivationConditionsConfigTypeDef = TypedDict(
    "HumanLoopActivationConditionsConfigTypeDef", {"HumanLoopActivationConditions": str}
)

HumanLoopActivationConfigTypeDef = TypedDict(
    "HumanLoopActivationConfigTypeDef",
    {"HumanLoopActivationConditionsConfig": HumanLoopActivationConditionsConfigTypeDef},
)

USDTypeDef = TypedDict(
    "USDTypeDef", {"Dollars": int, "Cents": int, "TenthFractionsOfACent": int}, total=False
)

PublicWorkforceTaskPriceTypeDef = TypedDict(
    "PublicWorkforceTaskPriceTypeDef", {"AmountInUsd": USDTypeDef}, total=False
)

_RequiredHumanLoopConfigTypeDef = TypedDict(
    "_RequiredHumanLoopConfigTypeDef",
    {
        "WorkteamArn": str,
        "HumanTaskUiArn": str,
        "TaskTitle": str,
        "TaskDescription": str,
        "TaskCount": int,
    },
)
_OptionalHumanLoopConfigTypeDef = TypedDict(
    "_OptionalHumanLoopConfigTypeDef",
    {
        "TaskAvailabilityLifetimeInSeconds": int,
        "TaskTimeLimitInSeconds": int,
        "TaskKeywords": List[str],
        "PublicWorkforceTaskPrice": PublicWorkforceTaskPriceTypeDef,
    },
    total=False,
)


class HumanLoopConfigTypeDef(_RequiredHumanLoopConfigTypeDef, _OptionalHumanLoopConfigTypeDef):
    pass


HumanLoopRequestSourceTypeDef = TypedDict(
    "HumanLoopRequestSourceTypeDef",
    {
        "AwsManagedHumanLoopRequestSource": Literal[
            "AWS/Rekognition/DetectModerationLabels/Image/V3",
            "AWS/Textract/AnalyzeDocument/Forms/V1",
        ]
    },
)

_RequiredDescribeFlowDefinitionResponseTypeDef = TypedDict(
    "_RequiredDescribeFlowDefinitionResponseTypeDef",
    {
        "FlowDefinitionArn": str,
        "FlowDefinitionName": str,
        "FlowDefinitionStatus": Literal["Initializing", "Active", "Failed", "Deleting"],
        "CreationTime": datetime,
        "HumanLoopConfig": HumanLoopConfigTypeDef,
        "OutputConfig": FlowDefinitionOutputConfigTypeDef,
        "RoleArn": str,
    },
)
_OptionalDescribeFlowDefinitionResponseTypeDef = TypedDict(
    "_OptionalDescribeFlowDefinitionResponseTypeDef",
    {
        "HumanLoopRequestSource": HumanLoopRequestSourceTypeDef,
        "HumanLoopActivationConfig": HumanLoopActivationConfigTypeDef,
        "FailureReason": str,
    },
    total=False,
)


class DescribeFlowDefinitionResponseTypeDef(
    _RequiredDescribeFlowDefinitionResponseTypeDef, _OptionalDescribeFlowDefinitionResponseTypeDef
):
    pass


UiTemplateInfoTypeDef = TypedDict(
    "UiTemplateInfoTypeDef", {"Url": str, "ContentSha256": str}, total=False
)

DescribeHumanTaskUiResponseTypeDef = TypedDict(
    "DescribeHumanTaskUiResponseTypeDef",
    {
        "HumanTaskUiArn": str,
        "HumanTaskUiName": str,
        "CreationTime": datetime,
        "UiTemplate": UiTemplateInfoTypeDef,
    },
)

_RequiredHyperParameterAlgorithmSpecificationTypeDef = TypedDict(
    "_RequiredHyperParameterAlgorithmSpecificationTypeDef",
    {"TrainingInputMode": Literal["Pipe", "File"]},
)
_OptionalHyperParameterAlgorithmSpecificationTypeDef = TypedDict(
    "_OptionalHyperParameterAlgorithmSpecificationTypeDef",
    {
        "TrainingImage": str,
        "AlgorithmName": str,
        "MetricDefinitions": List[MetricDefinitionTypeDef],
    },
    total=False,
)


class HyperParameterAlgorithmSpecificationTypeDef(
    _RequiredHyperParameterAlgorithmSpecificationTypeDef,
    _OptionalHyperParameterAlgorithmSpecificationTypeDef,
):
    pass


CategoricalParameterRangeTypeDef = TypedDict(
    "CategoricalParameterRangeTypeDef", {"Name": str, "Values": List[str]}
)

_RequiredContinuousParameterRangeTypeDef = TypedDict(
    "_RequiredContinuousParameterRangeTypeDef", {"Name": str, "MinValue": str, "MaxValue": str}
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
    "_RequiredIntegerParameterRangeTypeDef", {"Name": str, "MinValue": str, "MaxValue": str}
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
        "IntegerParameterRanges": List[IntegerParameterRangeTypeDef],
        "ContinuousParameterRanges": List[ContinuousParameterRangeTypeDef],
        "CategoricalParameterRanges": List[CategoricalParameterRangeTypeDef],
    },
    total=False,
)

_RequiredHyperParameterTrainingJobDefinitionTypeDef = TypedDict(
    "_RequiredHyperParameterTrainingJobDefinitionTypeDef",
    {
        "AlgorithmSpecification": HyperParameterAlgorithmSpecificationTypeDef,
        "RoleArn": str,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "ResourceConfig": ResourceConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
    },
)
_OptionalHyperParameterTrainingJobDefinitionTypeDef = TypedDict(
    "_OptionalHyperParameterTrainingJobDefinitionTypeDef",
    {
        "DefinitionName": str,
        "TuningObjective": HyperParameterTuningJobObjectiveTypeDef,
        "HyperParameterRanges": ParameterRangesTypeDef,
        "StaticHyperParameters": Dict[str, str],
        "InputDataConfig": List[ChannelTypeDef],
        "VpcConfig": VpcConfigTypeDef,
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigTypeDef,
    },
    total=False,
)


class HyperParameterTrainingJobDefinitionTypeDef(
    _RequiredHyperParameterTrainingJobDefinitionTypeDef,
    _OptionalHyperParameterTrainingJobDefinitionTypeDef,
):
    pass


_RequiredFinalHyperParameterTuningJobObjectiveMetricTypeDef = TypedDict(
    "_RequiredFinalHyperParameterTuningJobObjectiveMetricTypeDef",
    {"MetricName": str, "Value": float},
)
_OptionalFinalHyperParameterTuningJobObjectiveMetricTypeDef = TypedDict(
    "_OptionalFinalHyperParameterTuningJobObjectiveMetricTypeDef",
    {"Type": Literal["Maximize", "Minimize"]},
    total=False,
)


class FinalHyperParameterTuningJobObjectiveMetricTypeDef(
    _RequiredFinalHyperParameterTuningJobObjectiveMetricTypeDef,
    _OptionalFinalHyperParameterTuningJobObjectiveMetricTypeDef,
):
    pass


_RequiredHyperParameterTrainingJobSummaryTypeDef = TypedDict(
    "_RequiredHyperParameterTrainingJobSummaryTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "CreationTime": datetime,
        "TrainingJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
        "TunedHyperParameters": Dict[str, str],
    },
)
_OptionalHyperParameterTrainingJobSummaryTypeDef = TypedDict(
    "_OptionalHyperParameterTrainingJobSummaryTypeDef",
    {
        "TrainingJobDefinitionName": str,
        "TuningJobName": str,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "FailureReason": str,
        "FinalHyperParameterTuningJobObjectiveMetric": FinalHyperParameterTuningJobObjectiveMetricTypeDef,
        "ObjectiveStatus": Literal["Succeeded", "Pending", "Failed"],
    },
    total=False,
)


class HyperParameterTrainingJobSummaryTypeDef(
    _RequiredHyperParameterTrainingJobSummaryTypeDef,
    _OptionalHyperParameterTrainingJobSummaryTypeDef,
):
    pass


ResourceLimitsTypeDef = TypedDict(
    "ResourceLimitsTypeDef", {"MaxNumberOfTrainingJobs": int, "MaxParallelTrainingJobs": int}
)

TuningJobCompletionCriteriaTypeDef = TypedDict(
    "TuningJobCompletionCriteriaTypeDef", {"TargetObjectiveMetricValue": float}
)

_RequiredHyperParameterTuningJobConfigTypeDef = TypedDict(
    "_RequiredHyperParameterTuningJobConfigTypeDef",
    {"Strategy": Literal["Bayesian", "Random"], "ResourceLimits": ResourceLimitsTypeDef},
)
_OptionalHyperParameterTuningJobConfigTypeDef = TypedDict(
    "_OptionalHyperParameterTuningJobConfigTypeDef",
    {
        "HyperParameterTuningJobObjective": HyperParameterTuningJobObjectiveTypeDef,
        "ParameterRanges": ParameterRangesTypeDef,
        "TrainingJobEarlyStoppingType": Literal["Off", "Auto"],
        "TuningJobCompletionCriteria": TuningJobCompletionCriteriaTypeDef,
    },
    total=False,
)


class HyperParameterTuningJobConfigTypeDef(
    _RequiredHyperParameterTuningJobConfigTypeDef, _OptionalHyperParameterTuningJobConfigTypeDef
):
    pass


ParentHyperParameterTuningJobTypeDef = TypedDict(
    "ParentHyperParameterTuningJobTypeDef", {"HyperParameterTuningJobName": str}, total=False
)

HyperParameterTuningJobWarmStartConfigTypeDef = TypedDict(
    "HyperParameterTuningJobWarmStartConfigTypeDef",
    {
        "ParentHyperParameterTuningJobs": List[ParentHyperParameterTuningJobTypeDef],
        "WarmStartType": Literal["IdenticalDataAndAlgorithm", "TransferLearning"],
    },
)

ObjectiveStatusCountersTypeDef = TypedDict(
    "ObjectiveStatusCountersTypeDef", {"Succeeded": int, "Pending": int, "Failed": int}, total=False
)

TrainingJobStatusCountersTypeDef = TypedDict(
    "TrainingJobStatusCountersTypeDef",
    {
        "Completed": int,
        "InProgress": int,
        "RetryableError": int,
        "NonRetryableError": int,
        "Stopped": int,
    },
    total=False,
)

_RequiredDescribeHyperParameterTuningJobResponseTypeDef = TypedDict(
    "_RequiredDescribeHyperParameterTuningJobResponseTypeDef",
    {
        "HyperParameterTuningJobName": str,
        "HyperParameterTuningJobArn": str,
        "HyperParameterTuningJobConfig": HyperParameterTuningJobConfigTypeDef,
        "HyperParameterTuningJobStatus": Literal[
            "Completed", "InProgress", "Failed", "Stopped", "Stopping"
        ],
        "CreationTime": datetime,
        "TrainingJobStatusCounters": TrainingJobStatusCountersTypeDef,
        "ObjectiveStatusCounters": ObjectiveStatusCountersTypeDef,
    },
)
_OptionalDescribeHyperParameterTuningJobResponseTypeDef = TypedDict(
    "_OptionalDescribeHyperParameterTuningJobResponseTypeDef",
    {
        "TrainingJobDefinition": HyperParameterTrainingJobDefinitionTypeDef,
        "TrainingJobDefinitions": List[HyperParameterTrainingJobDefinitionTypeDef],
        "HyperParameterTuningEndTime": datetime,
        "LastModifiedTime": datetime,
        "BestTrainingJob": HyperParameterTrainingJobSummaryTypeDef,
        "OverallBestTrainingJob": HyperParameterTrainingJobSummaryTypeDef,
        "WarmStartConfig": HyperParameterTuningJobWarmStartConfigTypeDef,
        "FailureReason": str,
    },
    total=False,
)


class DescribeHyperParameterTuningJobResponseTypeDef(
    _RequiredDescribeHyperParameterTuningJobResponseTypeDef,
    _OptionalDescribeHyperParameterTuningJobResponseTypeDef,
):
    pass


AnnotationConsolidationConfigTypeDef = TypedDict(
    "AnnotationConsolidationConfigTypeDef", {"AnnotationConsolidationLambdaArn": str}
)

UiConfigTypeDef = TypedDict("UiConfigTypeDef", {"UiTemplateS3Uri": str})

_RequiredHumanTaskConfigTypeDef = TypedDict(
    "_RequiredHumanTaskConfigTypeDef",
    {
        "WorkteamArn": str,
        "UiConfig": UiConfigTypeDef,
        "PreHumanTaskLambdaArn": str,
        "TaskTitle": str,
        "TaskDescription": str,
        "NumberOfHumanWorkersPerDataObject": int,
        "TaskTimeLimitInSeconds": int,
        "AnnotationConsolidationConfig": AnnotationConsolidationConfigTypeDef,
    },
)
_OptionalHumanTaskConfigTypeDef = TypedDict(
    "_OptionalHumanTaskConfigTypeDef",
    {
        "TaskKeywords": List[str],
        "TaskAvailabilityLifetimeInSeconds": int,
        "MaxConcurrentTaskCount": int,
        "PublicWorkforceTaskPrice": PublicWorkforceTaskPriceTypeDef,
    },
    total=False,
)


class HumanTaskConfigTypeDef(_RequiredHumanTaskConfigTypeDef, _OptionalHumanTaskConfigTypeDef):
    pass


LabelCountersTypeDef = TypedDict(
    "LabelCountersTypeDef",
    {
        "TotalLabeled": int,
        "HumanLabeled": int,
        "MachineLabeled": int,
        "FailedNonRetryableError": int,
        "Unlabeled": int,
    },
    total=False,
)

LabelingJobResourceConfigTypeDef = TypedDict(
    "LabelingJobResourceConfigTypeDef", {"VolumeKmsKeyId": str}, total=False
)

_RequiredLabelingJobAlgorithmsConfigTypeDef = TypedDict(
    "_RequiredLabelingJobAlgorithmsConfigTypeDef", {"LabelingJobAlgorithmSpecificationArn": str}
)
_OptionalLabelingJobAlgorithmsConfigTypeDef = TypedDict(
    "_OptionalLabelingJobAlgorithmsConfigTypeDef",
    {
        "InitialActiveLearningModelArn": str,
        "LabelingJobResourceConfig": LabelingJobResourceConfigTypeDef,
    },
    total=False,
)


class LabelingJobAlgorithmsConfigTypeDef(
    _RequiredLabelingJobAlgorithmsConfigTypeDef, _OptionalLabelingJobAlgorithmsConfigTypeDef
):
    pass


LabelingJobDataAttributesTypeDef = TypedDict(
    "LabelingJobDataAttributesTypeDef",
    {
        "ContentClassifiers": List[
            Literal["FreeOfPersonallyIdentifiableInformation", "FreeOfAdultContent"]
        ]
    },
    total=False,
)

LabelingJobS3DataSourceTypeDef = TypedDict("LabelingJobS3DataSourceTypeDef", {"ManifestS3Uri": str})

LabelingJobDataSourceTypeDef = TypedDict(
    "LabelingJobDataSourceTypeDef", {"S3DataSource": LabelingJobS3DataSourceTypeDef}
)

_RequiredLabelingJobInputConfigTypeDef = TypedDict(
    "_RequiredLabelingJobInputConfigTypeDef", {"DataSource": LabelingJobDataSourceTypeDef}
)
_OptionalLabelingJobInputConfigTypeDef = TypedDict(
    "_OptionalLabelingJobInputConfigTypeDef",
    {"DataAttributes": LabelingJobDataAttributesTypeDef},
    total=False,
)


class LabelingJobInputConfigTypeDef(
    _RequiredLabelingJobInputConfigTypeDef, _OptionalLabelingJobInputConfigTypeDef
):
    pass


_RequiredLabelingJobOutputConfigTypeDef = TypedDict(
    "_RequiredLabelingJobOutputConfigTypeDef", {"S3OutputPath": str}
)
_OptionalLabelingJobOutputConfigTypeDef = TypedDict(
    "_OptionalLabelingJobOutputConfigTypeDef", {"KmsKeyId": str}, total=False
)


class LabelingJobOutputConfigTypeDef(
    _RequiredLabelingJobOutputConfigTypeDef, _OptionalLabelingJobOutputConfigTypeDef
):
    pass


_RequiredLabelingJobOutputTypeDef = TypedDict(
    "_RequiredLabelingJobOutputTypeDef", {"OutputDatasetS3Uri": str}
)
_OptionalLabelingJobOutputTypeDef = TypedDict(
    "_OptionalLabelingJobOutputTypeDef", {"FinalActiveLearningModelArn": str}, total=False
)


class LabelingJobOutputTypeDef(
    _RequiredLabelingJobOutputTypeDef, _OptionalLabelingJobOutputTypeDef
):
    pass


LabelingJobStoppingConditionsTypeDef = TypedDict(
    "LabelingJobStoppingConditionsTypeDef",
    {"MaxHumanLabeledObjectCount": int, "MaxPercentageOfInputDatasetLabeled": int},
    total=False,
)

_RequiredDescribeLabelingJobResponseTypeDef = TypedDict(
    "_RequiredDescribeLabelingJobResponseTypeDef",
    {
        "LabelingJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
        "LabelCounters": LabelCountersTypeDef,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "JobReferenceCode": str,
        "LabelingJobName": str,
        "LabelingJobArn": str,
        "InputConfig": LabelingJobInputConfigTypeDef,
        "OutputConfig": LabelingJobOutputConfigTypeDef,
        "RoleArn": str,
        "HumanTaskConfig": HumanTaskConfigTypeDef,
    },
)
_OptionalDescribeLabelingJobResponseTypeDef = TypedDict(
    "_OptionalDescribeLabelingJobResponseTypeDef",
    {
        "FailureReason": str,
        "LabelAttributeName": str,
        "LabelCategoryConfigS3Uri": str,
        "StoppingConditions": LabelingJobStoppingConditionsTypeDef,
        "LabelingJobAlgorithmsConfig": LabelingJobAlgorithmsConfigTypeDef,
        "Tags": List[TagTypeDef],
        "LabelingJobOutput": LabelingJobOutputTypeDef,
    },
    total=False,
)


class DescribeLabelingJobResponseTypeDef(
    _RequiredDescribeLabelingJobResponseTypeDef, _OptionalDescribeLabelingJobResponseTypeDef
):
    pass


_RequiredDescribeModelOutputTypeDef = TypedDict(
    "_RequiredDescribeModelOutputTypeDef",
    {"ModelName": str, "ExecutionRoleArn": str, "CreationTime": datetime, "ModelArn": str},
)
_OptionalDescribeModelOutputTypeDef = TypedDict(
    "_OptionalDescribeModelOutputTypeDef",
    {
        "PrimaryContainer": ContainerDefinitionTypeDef,
        "Containers": List[ContainerDefinitionTypeDef],
        "VpcConfig": VpcConfigTypeDef,
        "EnableNetworkIsolation": bool,
    },
    total=False,
)


class DescribeModelOutputTypeDef(
    _RequiredDescribeModelOutputTypeDef, _OptionalDescribeModelOutputTypeDef
):
    pass


_RequiredModelPackageStatusItemTypeDef = TypedDict(
    "_RequiredModelPackageStatusItemTypeDef",
    {"Name": str, "Status": Literal["NotStarted", "InProgress", "Completed", "Failed"]},
)
_OptionalModelPackageStatusItemTypeDef = TypedDict(
    "_OptionalModelPackageStatusItemTypeDef", {"FailureReason": str}, total=False
)


class ModelPackageStatusItemTypeDef(
    _RequiredModelPackageStatusItemTypeDef, _OptionalModelPackageStatusItemTypeDef
):
    pass


_RequiredModelPackageStatusDetailsTypeDef = TypedDict(
    "_RequiredModelPackageStatusDetailsTypeDef",
    {"ValidationStatuses": List[ModelPackageStatusItemTypeDef]},
)
_OptionalModelPackageStatusDetailsTypeDef = TypedDict(
    "_OptionalModelPackageStatusDetailsTypeDef",
    {"ImageScanStatuses": List[ModelPackageStatusItemTypeDef]},
    total=False,
)


class ModelPackageStatusDetailsTypeDef(
    _RequiredModelPackageStatusDetailsTypeDef, _OptionalModelPackageStatusDetailsTypeDef
):
    pass


ModelPackageValidationProfileTypeDef = TypedDict(
    "ModelPackageValidationProfileTypeDef",
    {"ProfileName": str, "TransformJobDefinition": TransformJobDefinitionTypeDef},
)

ModelPackageValidationSpecificationTypeDef = TypedDict(
    "ModelPackageValidationSpecificationTypeDef",
    {"ValidationRole": str, "ValidationProfiles": List[ModelPackageValidationProfileTypeDef]},
)

_RequiredSourceAlgorithmTypeDef = TypedDict(
    "_RequiredSourceAlgorithmTypeDef", {"AlgorithmName": str}
)
_OptionalSourceAlgorithmTypeDef = TypedDict(
    "_OptionalSourceAlgorithmTypeDef", {"ModelDataUrl": str}, total=False
)


class SourceAlgorithmTypeDef(_RequiredSourceAlgorithmTypeDef, _OptionalSourceAlgorithmTypeDef):
    pass


SourceAlgorithmSpecificationTypeDef = TypedDict(
    "SourceAlgorithmSpecificationTypeDef", {"SourceAlgorithms": List[SourceAlgorithmTypeDef]}
)

_RequiredDescribeModelPackageOutputTypeDef = TypedDict(
    "_RequiredDescribeModelPackageOutputTypeDef",
    {
        "ModelPackageName": str,
        "ModelPackageArn": str,
        "CreationTime": datetime,
        "ModelPackageStatus": Literal["Pending", "InProgress", "Completed", "Failed", "Deleting"],
        "ModelPackageStatusDetails": ModelPackageStatusDetailsTypeDef,
    },
)
_OptionalDescribeModelPackageOutputTypeDef = TypedDict(
    "_OptionalDescribeModelPackageOutputTypeDef",
    {
        "ModelPackageDescription": str,
        "InferenceSpecification": InferenceSpecificationTypeDef,
        "SourceAlgorithmSpecification": SourceAlgorithmSpecificationTypeDef,
        "ValidationSpecification": ModelPackageValidationSpecificationTypeDef,
        "CertifyForMarketplace": bool,
    },
    total=False,
)


class DescribeModelPackageOutputTypeDef(
    _RequiredDescribeModelPackageOutputTypeDef, _OptionalDescribeModelPackageOutputTypeDef
):
    pass


_RequiredMonitoringExecutionSummaryTypeDef = TypedDict(
    "_RequiredMonitoringExecutionSummaryTypeDef",
    {
        "MonitoringScheduleName": str,
        "ScheduledTime": datetime,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringExecutionStatus": Literal[
            "Pending",
            "Completed",
            "CompletedWithViolations",
            "InProgress",
            "Failed",
            "Stopping",
            "Stopped",
        ],
    },
)
_OptionalMonitoringExecutionSummaryTypeDef = TypedDict(
    "_OptionalMonitoringExecutionSummaryTypeDef",
    {"ProcessingJobArn": str, "EndpointName": str, "FailureReason": str},
    total=False,
)


class MonitoringExecutionSummaryTypeDef(
    _RequiredMonitoringExecutionSummaryTypeDef, _OptionalMonitoringExecutionSummaryTypeDef
):
    pass


_RequiredMonitoringAppSpecificationTypeDef = TypedDict(
    "_RequiredMonitoringAppSpecificationTypeDef", {"ImageUri": str}
)
_OptionalMonitoringAppSpecificationTypeDef = TypedDict(
    "_OptionalMonitoringAppSpecificationTypeDef",
    {
        "ContainerEntrypoint": List[str],
        "ContainerArguments": List[str],
        "RecordPreprocessorSourceUri": str,
        "PostAnalyticsProcessorSourceUri": str,
    },
    total=False,
)


class MonitoringAppSpecificationTypeDef(
    _RequiredMonitoringAppSpecificationTypeDef, _OptionalMonitoringAppSpecificationTypeDef
):
    pass


MonitoringConstraintsResourceTypeDef = TypedDict(
    "MonitoringConstraintsResourceTypeDef", {"S3Uri": str}, total=False
)

MonitoringStatisticsResourceTypeDef = TypedDict(
    "MonitoringStatisticsResourceTypeDef", {"S3Uri": str}, total=False
)

MonitoringBaselineConfigTypeDef = TypedDict(
    "MonitoringBaselineConfigTypeDef",
    {
        "ConstraintsResource": MonitoringConstraintsResourceTypeDef,
        "StatisticsResource": MonitoringStatisticsResourceTypeDef,
    },
    total=False,
)

_RequiredEndpointInputTypeDef = TypedDict(
    "_RequiredEndpointInputTypeDef", {"EndpointName": str, "LocalPath": str}
)
_OptionalEndpointInputTypeDef = TypedDict(
    "_OptionalEndpointInputTypeDef",
    {
        "S3InputMode": Literal["Pipe", "File"],
        "S3DataDistributionType": Literal["FullyReplicated", "ShardedByS3Key"],
    },
    total=False,
)


class EndpointInputTypeDef(_RequiredEndpointInputTypeDef, _OptionalEndpointInputTypeDef):
    pass


MonitoringInputTypeDef = TypedDict(
    "MonitoringInputTypeDef", {"EndpointInput": EndpointInputTypeDef}
)

_RequiredMonitoringS3OutputTypeDef = TypedDict(
    "_RequiredMonitoringS3OutputTypeDef", {"S3Uri": str, "LocalPath": str}
)
_OptionalMonitoringS3OutputTypeDef = TypedDict(
    "_OptionalMonitoringS3OutputTypeDef",
    {"S3UploadMode": Literal["Continuous", "EndOfJob"]},
    total=False,
)


class MonitoringS3OutputTypeDef(
    _RequiredMonitoringS3OutputTypeDef, _OptionalMonitoringS3OutputTypeDef
):
    pass


MonitoringOutputTypeDef = TypedDict(
    "MonitoringOutputTypeDef", {"S3Output": MonitoringS3OutputTypeDef}
)

_RequiredMonitoringOutputConfigTypeDef = TypedDict(
    "_RequiredMonitoringOutputConfigTypeDef", {"MonitoringOutputs": List[MonitoringOutputTypeDef]}
)
_OptionalMonitoringOutputConfigTypeDef = TypedDict(
    "_OptionalMonitoringOutputConfigTypeDef", {"KmsKeyId": str}, total=False
)


class MonitoringOutputConfigTypeDef(
    _RequiredMonitoringOutputConfigTypeDef, _OptionalMonitoringOutputConfigTypeDef
):
    pass


_RequiredMonitoringClusterConfigTypeDef = TypedDict(
    "_RequiredMonitoringClusterConfigTypeDef",
    {
        "InstanceCount": int,
        "InstanceType": Literal[
            "ml.t3.medium",
            "ml.t3.large",
            "ml.t3.xlarge",
            "ml.t3.2xlarge",
            "ml.m4.xlarge",
            "ml.m4.2xlarge",
            "ml.m4.4xlarge",
            "ml.m4.10xlarge",
            "ml.m4.16xlarge",
            "ml.c4.xlarge",
            "ml.c4.2xlarge",
            "ml.c4.4xlarge",
            "ml.c4.8xlarge",
            "ml.p2.xlarge",
            "ml.p2.8xlarge",
            "ml.p2.16xlarge",
            "ml.p3.2xlarge",
            "ml.p3.8xlarge",
            "ml.p3.16xlarge",
            "ml.c5.xlarge",
            "ml.c5.2xlarge",
            "ml.c5.4xlarge",
            "ml.c5.9xlarge",
            "ml.c5.18xlarge",
            "ml.m5.large",
            "ml.m5.xlarge",
            "ml.m5.2xlarge",
            "ml.m5.4xlarge",
            "ml.m5.12xlarge",
            "ml.m5.24xlarge",
            "ml.r5.large",
            "ml.r5.xlarge",
            "ml.r5.2xlarge",
            "ml.r5.4xlarge",
            "ml.r5.8xlarge",
            "ml.r5.12xlarge",
            "ml.r5.16xlarge",
            "ml.r5.24xlarge",
        ],
        "VolumeSizeInGB": int,
    },
)
_OptionalMonitoringClusterConfigTypeDef = TypedDict(
    "_OptionalMonitoringClusterConfigTypeDef", {"VolumeKmsKeyId": str}, total=False
)


class MonitoringClusterConfigTypeDef(
    _RequiredMonitoringClusterConfigTypeDef, _OptionalMonitoringClusterConfigTypeDef
):
    pass


MonitoringResourcesTypeDef = TypedDict(
    "MonitoringResourcesTypeDef", {"ClusterConfig": MonitoringClusterConfigTypeDef}
)

MonitoringStoppingConditionTypeDef = TypedDict(
    "MonitoringStoppingConditionTypeDef", {"MaxRuntimeInSeconds": int}
)

NetworkConfigTypeDef = TypedDict(
    "NetworkConfigTypeDef",
    {"EnableNetworkIsolation": bool, "VpcConfig": VpcConfigTypeDef},
    total=False,
)

_RequiredMonitoringJobDefinitionTypeDef = TypedDict(
    "_RequiredMonitoringJobDefinitionTypeDef",
    {
        "MonitoringInputs": List[MonitoringInputTypeDef],
        "MonitoringOutputConfig": MonitoringOutputConfigTypeDef,
        "MonitoringResources": MonitoringResourcesTypeDef,
        "MonitoringAppSpecification": MonitoringAppSpecificationTypeDef,
        "RoleArn": str,
    },
)
_OptionalMonitoringJobDefinitionTypeDef = TypedDict(
    "_OptionalMonitoringJobDefinitionTypeDef",
    {
        "BaselineConfig": MonitoringBaselineConfigTypeDef,
        "StoppingCondition": MonitoringStoppingConditionTypeDef,
        "Environment": Dict[str, str],
        "NetworkConfig": NetworkConfigTypeDef,
    },
    total=False,
)


class MonitoringJobDefinitionTypeDef(
    _RequiredMonitoringJobDefinitionTypeDef, _OptionalMonitoringJobDefinitionTypeDef
):
    pass


ScheduleConfigTypeDef = TypedDict("ScheduleConfigTypeDef", {"ScheduleExpression": str})

_RequiredMonitoringScheduleConfigTypeDef = TypedDict(
    "_RequiredMonitoringScheduleConfigTypeDef",
    {"MonitoringJobDefinition": MonitoringJobDefinitionTypeDef},
)
_OptionalMonitoringScheduleConfigTypeDef = TypedDict(
    "_OptionalMonitoringScheduleConfigTypeDef",
    {"ScheduleConfig": ScheduleConfigTypeDef},
    total=False,
)


class MonitoringScheduleConfigTypeDef(
    _RequiredMonitoringScheduleConfigTypeDef, _OptionalMonitoringScheduleConfigTypeDef
):
    pass


_RequiredDescribeMonitoringScheduleResponseTypeDef = TypedDict(
    "_RequiredDescribeMonitoringScheduleResponseTypeDef",
    {
        "MonitoringScheduleArn": str,
        "MonitoringScheduleName": str,
        "MonitoringScheduleStatus": Literal["Pending", "Failed", "Scheduled", "Stopped"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleConfig": MonitoringScheduleConfigTypeDef,
    },
)
_OptionalDescribeMonitoringScheduleResponseTypeDef = TypedDict(
    "_OptionalDescribeMonitoringScheduleResponseTypeDef",
    {
        "FailureReason": str,
        "EndpointName": str,
        "LastMonitoringExecutionSummary": MonitoringExecutionSummaryTypeDef,
    },
    total=False,
)


class DescribeMonitoringScheduleResponseTypeDef(
    _RequiredDescribeMonitoringScheduleResponseTypeDef,
    _OptionalDescribeMonitoringScheduleResponseTypeDef,
):
    pass


NotebookInstanceLifecycleHookTypeDef = TypedDict(
    "NotebookInstanceLifecycleHookTypeDef", {"Content": str}, total=False
)

DescribeNotebookInstanceLifecycleConfigOutputTypeDef = TypedDict(
    "DescribeNotebookInstanceLifecycleConfigOutputTypeDef",
    {
        "NotebookInstanceLifecycleConfigArn": str,
        "NotebookInstanceLifecycleConfigName": str,
        "OnCreate": List[NotebookInstanceLifecycleHookTypeDef],
        "OnStart": List[NotebookInstanceLifecycleHookTypeDef],
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
    },
    total=False,
)

DescribeNotebookInstanceOutputTypeDef = TypedDict(
    "DescribeNotebookInstanceOutputTypeDef",
    {
        "NotebookInstanceArn": str,
        "NotebookInstanceName": str,
        "NotebookInstanceStatus": Literal[
            "Pending", "InService", "Stopping", "Stopped", "Failed", "Deleting", "Updating"
        ],
        "FailureReason": str,
        "Url": str,
        "InstanceType": Literal[
            "ml.t2.medium",
            "ml.t2.large",
            "ml.t2.xlarge",
            "ml.t2.2xlarge",
            "ml.t3.medium",
            "ml.t3.large",
            "ml.t3.xlarge",
            "ml.t3.2xlarge",
            "ml.m4.xlarge",
            "ml.m4.2xlarge",
            "ml.m4.4xlarge",
            "ml.m4.10xlarge",
            "ml.m4.16xlarge",
            "ml.m5.xlarge",
            "ml.m5.2xlarge",
            "ml.m5.4xlarge",
            "ml.m5.12xlarge",
            "ml.m5.24xlarge",
            "ml.c4.xlarge",
            "ml.c4.2xlarge",
            "ml.c4.4xlarge",
            "ml.c4.8xlarge",
            "ml.c5.xlarge",
            "ml.c5.2xlarge",
            "ml.c5.4xlarge",
            "ml.c5.9xlarge",
            "ml.c5.18xlarge",
            "ml.c5d.xlarge",
            "ml.c5d.2xlarge",
            "ml.c5d.4xlarge",
            "ml.c5d.9xlarge",
            "ml.c5d.18xlarge",
            "ml.p2.xlarge",
            "ml.p2.8xlarge",
            "ml.p2.16xlarge",
            "ml.p3.2xlarge",
            "ml.p3.8xlarge",
            "ml.p3.16xlarge",
        ],
        "SubnetId": str,
        "SecurityGroups": List[str],
        "RoleArn": str,
        "KmsKeyId": str,
        "NetworkInterfaceId": str,
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "NotebookInstanceLifecycleConfigName": str,
        "DirectInternetAccess": Literal["Enabled", "Disabled"],
        "VolumeSizeInGB": int,
        "AcceleratorTypes": List[
            Literal[
                "ml.eia1.medium",
                "ml.eia1.large",
                "ml.eia1.xlarge",
                "ml.eia2.medium",
                "ml.eia2.large",
                "ml.eia2.xlarge",
            ]
        ],
        "DefaultCodeRepository": str,
        "AdditionalCodeRepositories": List[str],
        "RootAccess": Literal["Enabled", "Disabled"],
    },
    total=False,
)

ExperimentConfigTypeDef = TypedDict(
    "ExperimentConfigTypeDef",
    {"ExperimentName": str, "TrialName": str, "TrialComponentDisplayName": str},
    total=False,
)

_RequiredProcessingS3InputTypeDef = TypedDict(
    "_RequiredProcessingS3InputTypeDef",
    {
        "S3Uri": str,
        "LocalPath": str,
        "S3DataType": Literal["ManifestFile", "S3Prefix"],
        "S3InputMode": Literal["Pipe", "File"],
    },
)
_OptionalProcessingS3InputTypeDef = TypedDict(
    "_OptionalProcessingS3InputTypeDef",
    {
        "S3DataDistributionType": Literal["FullyReplicated", "ShardedByS3Key"],
        "S3CompressionType": Literal["None", "Gzip"],
    },
    total=False,
)


class ProcessingS3InputTypeDef(
    _RequiredProcessingS3InputTypeDef, _OptionalProcessingS3InputTypeDef
):
    pass


ProcessingInputTypeDef = TypedDict(
    "ProcessingInputTypeDef", {"InputName": str, "S3Input": ProcessingS3InputTypeDef}
)

ProcessingS3OutputTypeDef = TypedDict(
    "ProcessingS3OutputTypeDef",
    {"S3Uri": str, "LocalPath": str, "S3UploadMode": Literal["Continuous", "EndOfJob"]},
)

ProcessingOutputTypeDef = TypedDict(
    "ProcessingOutputTypeDef", {"OutputName": str, "S3Output": ProcessingS3OutputTypeDef}
)

_RequiredProcessingOutputConfigTypeDef = TypedDict(
    "_RequiredProcessingOutputConfigTypeDef", {"Outputs": List[ProcessingOutputTypeDef]}
)
_OptionalProcessingOutputConfigTypeDef = TypedDict(
    "_OptionalProcessingOutputConfigTypeDef", {"KmsKeyId": str}, total=False
)


class ProcessingOutputConfigTypeDef(
    _RequiredProcessingOutputConfigTypeDef, _OptionalProcessingOutputConfigTypeDef
):
    pass


_RequiredProcessingClusterConfigTypeDef = TypedDict(
    "_RequiredProcessingClusterConfigTypeDef",
    {
        "InstanceCount": int,
        "InstanceType": Literal[
            "ml.t3.medium",
            "ml.t3.large",
            "ml.t3.xlarge",
            "ml.t3.2xlarge",
            "ml.m4.xlarge",
            "ml.m4.2xlarge",
            "ml.m4.4xlarge",
            "ml.m4.10xlarge",
            "ml.m4.16xlarge",
            "ml.c4.xlarge",
            "ml.c4.2xlarge",
            "ml.c4.4xlarge",
            "ml.c4.8xlarge",
            "ml.p2.xlarge",
            "ml.p2.8xlarge",
            "ml.p2.16xlarge",
            "ml.p3.2xlarge",
            "ml.p3.8xlarge",
            "ml.p3.16xlarge",
            "ml.c5.xlarge",
            "ml.c5.2xlarge",
            "ml.c5.4xlarge",
            "ml.c5.9xlarge",
            "ml.c5.18xlarge",
            "ml.m5.large",
            "ml.m5.xlarge",
            "ml.m5.2xlarge",
            "ml.m5.4xlarge",
            "ml.m5.12xlarge",
            "ml.m5.24xlarge",
            "ml.r5.large",
            "ml.r5.xlarge",
            "ml.r5.2xlarge",
            "ml.r5.4xlarge",
            "ml.r5.8xlarge",
            "ml.r5.12xlarge",
            "ml.r5.16xlarge",
            "ml.r5.24xlarge",
        ],
        "VolumeSizeInGB": int,
    },
)
_OptionalProcessingClusterConfigTypeDef = TypedDict(
    "_OptionalProcessingClusterConfigTypeDef", {"VolumeKmsKeyId": str}, total=False
)


class ProcessingClusterConfigTypeDef(
    _RequiredProcessingClusterConfigTypeDef, _OptionalProcessingClusterConfigTypeDef
):
    pass


ProcessingResourcesTypeDef = TypedDict(
    "ProcessingResourcesTypeDef", {"ClusterConfig": ProcessingClusterConfigTypeDef}
)

ProcessingStoppingConditionTypeDef = TypedDict(
    "ProcessingStoppingConditionTypeDef", {"MaxRuntimeInSeconds": int}
)

_RequiredDescribeProcessingJobResponseTypeDef = TypedDict(
    "_RequiredDescribeProcessingJobResponseTypeDef",
    {
        "ProcessingJobName": str,
        "ProcessingResources": ProcessingResourcesTypeDef,
        "AppSpecification": AppSpecificationTypeDef,
        "ProcessingJobArn": str,
        "ProcessingJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
        "CreationTime": datetime,
    },
)
_OptionalDescribeProcessingJobResponseTypeDef = TypedDict(
    "_OptionalDescribeProcessingJobResponseTypeDef",
    {
        "ProcessingInputs": List[ProcessingInputTypeDef],
        "ProcessingOutputConfig": ProcessingOutputConfigTypeDef,
        "StoppingCondition": ProcessingStoppingConditionTypeDef,
        "Environment": Dict[str, str],
        "NetworkConfig": NetworkConfigTypeDef,
        "RoleArn": str,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "ExitMessage": str,
        "FailureReason": str,
        "ProcessingEndTime": datetime,
        "ProcessingStartTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleArn": str,
        "AutoMLJobArn": str,
        "TrainingJobArn": str,
    },
    total=False,
)


class DescribeProcessingJobResponseTypeDef(
    _RequiredDescribeProcessingJobResponseTypeDef, _OptionalDescribeProcessingJobResponseTypeDef
):
    pass


_RequiredSubscribedWorkteamTypeDef = TypedDict(
    "_RequiredSubscribedWorkteamTypeDef", {"WorkteamArn": str}
)
_OptionalSubscribedWorkteamTypeDef = TypedDict(
    "_OptionalSubscribedWorkteamTypeDef",
    {"MarketplaceTitle": str, "SellerName": str, "MarketplaceDescription": str, "ListingId": str},
    total=False,
)


class SubscribedWorkteamTypeDef(
    _RequiredSubscribedWorkteamTypeDef, _OptionalSubscribedWorkteamTypeDef
):
    pass


DescribeSubscribedWorkteamResponseTypeDef = TypedDict(
    "DescribeSubscribedWorkteamResponseTypeDef", {"SubscribedWorkteam": SubscribedWorkteamTypeDef}
)

DebugRuleEvaluationStatusTypeDef = TypedDict(
    "DebugRuleEvaluationStatusTypeDef",
    {
        "RuleConfigurationName": str,
        "RuleEvaluationJobArn": str,
        "RuleEvaluationStatus": Literal[
            "InProgress", "NoIssuesFound", "IssuesFound", "Error", "Stopping", "Stopped"
        ],
        "StatusDetails": str,
        "LastModifiedTime": datetime,
    },
    total=False,
)

MetricDataTypeDef = TypedDict(
    "MetricDataTypeDef", {"MetricName": str, "Value": float, "Timestamp": datetime}, total=False
)

_RequiredSecondaryStatusTransitionTypeDef = TypedDict(
    "_RequiredSecondaryStatusTransitionTypeDef",
    {
        "Status": Literal[
            "Starting",
            "LaunchingMLInstances",
            "PreparingTrainingStack",
            "Downloading",
            "DownloadingTrainingImage",
            "Training",
            "Uploading",
            "Stopping",
            "Stopped",
            "MaxRuntimeExceeded",
            "Completed",
            "Failed",
            "Interrupted",
            "MaxWaitTimeExceeded",
        ],
        "StartTime": datetime,
    },
)
_OptionalSecondaryStatusTransitionTypeDef = TypedDict(
    "_OptionalSecondaryStatusTransitionTypeDef",
    {"EndTime": datetime, "StatusMessage": str},
    total=False,
)


class SecondaryStatusTransitionTypeDef(
    _RequiredSecondaryStatusTransitionTypeDef, _OptionalSecondaryStatusTransitionTypeDef
):
    pass


_RequiredTensorBoardOutputConfigTypeDef = TypedDict(
    "_RequiredTensorBoardOutputConfigTypeDef", {"S3OutputPath": str}
)
_OptionalTensorBoardOutputConfigTypeDef = TypedDict(
    "_OptionalTensorBoardOutputConfigTypeDef", {"LocalPath": str}, total=False
)


class TensorBoardOutputConfigTypeDef(
    _RequiredTensorBoardOutputConfigTypeDef, _OptionalTensorBoardOutputConfigTypeDef
):
    pass


_RequiredDescribeTrainingJobResponseTypeDef = TypedDict(
    "_RequiredDescribeTrainingJobResponseTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "ModelArtifacts": ModelArtifactsTypeDef,
        "TrainingJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
        "SecondaryStatus": Literal[
            "Starting",
            "LaunchingMLInstances",
            "PreparingTrainingStack",
            "Downloading",
            "DownloadingTrainingImage",
            "Training",
            "Uploading",
            "Stopping",
            "Stopped",
            "MaxRuntimeExceeded",
            "Completed",
            "Failed",
            "Interrupted",
            "MaxWaitTimeExceeded",
        ],
        "AlgorithmSpecification": AlgorithmSpecificationTypeDef,
        "ResourceConfig": ResourceConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
        "CreationTime": datetime,
    },
)
_OptionalDescribeTrainingJobResponseTypeDef = TypedDict(
    "_OptionalDescribeTrainingJobResponseTypeDef",
    {
        "TuningJobArn": str,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "FailureReason": str,
        "HyperParameters": Dict[str, str],
        "RoleArn": str,
        "InputDataConfig": List[ChannelTypeDef],
        "OutputDataConfig": OutputDataConfigTypeDef,
        "VpcConfig": VpcConfigTypeDef,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "LastModifiedTime": datetime,
        "SecondaryStatusTransitions": List[SecondaryStatusTransitionTypeDef],
        "FinalMetricDataList": List[MetricDataTypeDef],
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigTypeDef,
        "TrainingTimeInSeconds": int,
        "BillableTimeInSeconds": int,
        "DebugHookConfig": DebugHookConfigTypeDef,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "DebugRuleConfigurations": List[DebugRuleConfigurationTypeDef],
        "TensorBoardOutputConfig": TensorBoardOutputConfigTypeDef,
        "DebugRuleEvaluationStatuses": List[DebugRuleEvaluationStatusTypeDef],
    },
    total=False,
)


class DescribeTrainingJobResponseTypeDef(
    _RequiredDescribeTrainingJobResponseTypeDef, _OptionalDescribeTrainingJobResponseTypeDef
):
    pass


_RequiredDescribeTransformJobResponseTypeDef = TypedDict(
    "_RequiredDescribeTransformJobResponseTypeDef",
    {
        "TransformJobName": str,
        "TransformJobArn": str,
        "TransformJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
        "ModelName": str,
        "TransformInput": TransformInputTypeDef,
        "TransformResources": TransformResourcesTypeDef,
        "CreationTime": datetime,
    },
)
_OptionalDescribeTransformJobResponseTypeDef = TypedDict(
    "_OptionalDescribeTransformJobResponseTypeDef",
    {
        "FailureReason": str,
        "MaxConcurrentTransforms": int,
        "MaxPayloadInMB": int,
        "BatchStrategy": Literal["MultiRecord", "SingleRecord"],
        "Environment": Dict[str, str],
        "TransformOutput": TransformOutputTypeDef,
        "TransformStartTime": datetime,
        "TransformEndTime": datetime,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "DataProcessing": DataProcessingTypeDef,
        "ExperimentConfig": ExperimentConfigTypeDef,
    },
    total=False,
)


class DescribeTransformJobResponseTypeDef(
    _RequiredDescribeTransformJobResponseTypeDef, _OptionalDescribeTransformJobResponseTypeDef
):
    pass


_RequiredTrialComponentArtifactTypeDef = TypedDict(
    "_RequiredTrialComponentArtifactTypeDef", {"Value": str}
)
_OptionalTrialComponentArtifactTypeDef = TypedDict(
    "_OptionalTrialComponentArtifactTypeDef", {"MediaType": str}, total=False
)


class TrialComponentArtifactTypeDef(
    _RequiredTrialComponentArtifactTypeDef, _OptionalTrialComponentArtifactTypeDef
):
    pass


TrialComponentMetricSummaryTypeDef = TypedDict(
    "TrialComponentMetricSummaryTypeDef",
    {
        "MetricName": str,
        "SourceArn": str,
        "TimeStamp": datetime,
        "Max": float,
        "Min": float,
        "Last": float,
        "Count": int,
        "Avg": float,
        "StdDev": float,
    },
    total=False,
)

TrialComponentParameterValueTypeDef = TypedDict(
    "TrialComponentParameterValueTypeDef", {"StringValue": str, "NumberValue": float}, total=False
)

_RequiredTrialComponentSourceTypeDef = TypedDict(
    "_RequiredTrialComponentSourceTypeDef", {"SourceArn": str}
)
_OptionalTrialComponentSourceTypeDef = TypedDict(
    "_OptionalTrialComponentSourceTypeDef", {"SourceType": str}, total=False
)


class TrialComponentSourceTypeDef(
    _RequiredTrialComponentSourceTypeDef, _OptionalTrialComponentSourceTypeDef
):
    pass


TrialComponentStatusTypeDef = TypedDict(
    "TrialComponentStatusTypeDef",
    {"PrimaryStatus": Literal["InProgress", "Completed", "Failed"], "Message": str},
    total=False,
)

DescribeTrialComponentResponseTypeDef = TypedDict(
    "DescribeTrialComponentResponseTypeDef",
    {
        "TrialComponentName": str,
        "TrialComponentArn": str,
        "DisplayName": str,
        "Source": TrialComponentSourceTypeDef,
        "Status": TrialComponentStatusTypeDef,
        "StartTime": datetime,
        "EndTime": datetime,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "Parameters": Dict[str, TrialComponentParameterValueTypeDef],
        "InputArtifacts": Dict[str, TrialComponentArtifactTypeDef],
        "OutputArtifacts": Dict[str, TrialComponentArtifactTypeDef],
        "Metrics": List[TrialComponentMetricSummaryTypeDef],
    },
    total=False,
)

_RequiredTrialSourceTypeDef = TypedDict("_RequiredTrialSourceTypeDef", {"SourceArn": str})
_OptionalTrialSourceTypeDef = TypedDict(
    "_OptionalTrialSourceTypeDef", {"SourceType": str}, total=False
)


class TrialSourceTypeDef(_RequiredTrialSourceTypeDef, _OptionalTrialSourceTypeDef):
    pass


DescribeTrialResponseTypeDef = TypedDict(
    "DescribeTrialResponseTypeDef",
    {
        "TrialName": str,
        "TrialArn": str,
        "DisplayName": str,
        "ExperimentName": str,
        "Source": TrialSourceTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
    },
    total=False,
)

DescribeUserProfileResponseTypeDef = TypedDict(
    "DescribeUserProfileResponseTypeDef",
    {
        "DomainId": str,
        "UserProfileArn": str,
        "UserProfileName": str,
        "HomeEfsFileSystemUid": str,
        "Status": Literal["Deleting", "Failed", "InService", "Pending"],
        "LastModifiedTime": datetime,
        "CreationTime": datetime,
        "FailureReason": str,
        "SingleSignOnUserIdentifier": str,
        "SingleSignOnUserValue": str,
        "UserSettings": UserSettingsTypeDef,
    },
    total=False,
)

SourceIpConfigTypeDef = TypedDict("SourceIpConfigTypeDef", {"Cidrs": List[str]})

_RequiredWorkforceTypeDef = TypedDict(
    "_RequiredWorkforceTypeDef", {"WorkforceName": str, "WorkforceArn": str}
)
_OptionalWorkforceTypeDef = TypedDict(
    "_OptionalWorkforceTypeDef",
    {"LastUpdatedDate": datetime, "SourceIpConfig": SourceIpConfigTypeDef},
    total=False,
)


class WorkforceTypeDef(_RequiredWorkforceTypeDef, _OptionalWorkforceTypeDef):
    pass


DescribeWorkforceResponseTypeDef = TypedDict(
    "DescribeWorkforceResponseTypeDef", {"Workforce": WorkforceTypeDef}
)

CognitoMemberDefinitionTypeDef = TypedDict(
    "CognitoMemberDefinitionTypeDef", {"UserPool": str, "UserGroup": str, "ClientId": str}
)

MemberDefinitionTypeDef = TypedDict(
    "MemberDefinitionTypeDef",
    {"CognitoMemberDefinition": CognitoMemberDefinitionTypeDef},
    total=False,
)

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef", {"NotificationTopicArn": str}, total=False
)

_RequiredWorkteamTypeDef = TypedDict(
    "_RequiredWorkteamTypeDef",
    {
        "WorkteamName": str,
        "MemberDefinitions": List[MemberDefinitionTypeDef],
        "WorkteamArn": str,
        "Description": str,
    },
)
_OptionalWorkteamTypeDef = TypedDict(
    "_OptionalWorkteamTypeDef",
    {
        "ProductListingIds": List[str],
        "SubDomain": str,
        "CreateDate": datetime,
        "LastUpdatedDate": datetime,
        "NotificationConfiguration": NotificationConfigurationTypeDef,
    },
    total=False,
)


class WorkteamTypeDef(_RequiredWorkteamTypeDef, _OptionalWorkteamTypeDef):
    pass


DescribeWorkteamResponseTypeDef = TypedDict(
    "DescribeWorkteamResponseTypeDef", {"Workteam": WorkteamTypeDef}
)

_RequiredDesiredWeightAndCapacityTypeDef = TypedDict(
    "_RequiredDesiredWeightAndCapacityTypeDef", {"VariantName": str}
)
_OptionalDesiredWeightAndCapacityTypeDef = TypedDict(
    "_OptionalDesiredWeightAndCapacityTypeDef",
    {"DesiredWeight": float, "DesiredInstanceCount": int},
    total=False,
)


class DesiredWeightAndCapacityTypeDef(
    _RequiredDesiredWeightAndCapacityTypeDef, _OptionalDesiredWeightAndCapacityTypeDef
):
    pass


DisassociateTrialComponentResponseTypeDef = TypedDict(
    "DisassociateTrialComponentResponseTypeDef",
    {"TrialComponentArn": str, "TrialArn": str},
    total=False,
)

PropertyNameSuggestionTypeDef = TypedDict(
    "PropertyNameSuggestionTypeDef", {"PropertyName": str}, total=False
)

GetSearchSuggestionsResponseTypeDef = TypedDict(
    "GetSearchSuggestionsResponseTypeDef",
    {"PropertyNameSuggestions": List[PropertyNameSuggestionTypeDef]},
    total=False,
)

GitConfigForUpdateTypeDef = TypedDict("GitConfigForUpdateTypeDef", {"SecretArn": str}, total=False)

_RequiredAlgorithmSummaryTypeDef = TypedDict(
    "_RequiredAlgorithmSummaryTypeDef",
    {
        "AlgorithmName": str,
        "AlgorithmArn": str,
        "CreationTime": datetime,
        "AlgorithmStatus": Literal["Pending", "InProgress", "Completed", "Failed", "Deleting"],
    },
)
_OptionalAlgorithmSummaryTypeDef = TypedDict(
    "_OptionalAlgorithmSummaryTypeDef", {"AlgorithmDescription": str}, total=False
)


class AlgorithmSummaryTypeDef(_RequiredAlgorithmSummaryTypeDef, _OptionalAlgorithmSummaryTypeDef):
    pass


_RequiredListAlgorithmsOutputTypeDef = TypedDict(
    "_RequiredListAlgorithmsOutputTypeDef", {"AlgorithmSummaryList": List[AlgorithmSummaryTypeDef]}
)
_OptionalListAlgorithmsOutputTypeDef = TypedDict(
    "_OptionalListAlgorithmsOutputTypeDef", {"NextToken": str}, total=False
)


class ListAlgorithmsOutputTypeDef(
    _RequiredListAlgorithmsOutputTypeDef, _OptionalListAlgorithmsOutputTypeDef
):
    pass


AppDetailsTypeDef = TypedDict(
    "AppDetailsTypeDef",
    {
        "DomainId": str,
        "UserProfileName": str,
        "AppType": Literal["JupyterServer", "KernelGateway", "TensorBoard"],
        "AppName": str,
        "Status": Literal["Deleted", "Deleting", "Failed", "InService", "Pending"],
        "CreationTime": datetime,
    },
    total=False,
)

ListAppsResponseTypeDef = TypedDict(
    "ListAppsResponseTypeDef", {"Apps": List[AppDetailsTypeDef], "NextToken": str}, total=False
)

_RequiredAutoMLJobSummaryTypeDef = TypedDict(
    "_RequiredAutoMLJobSummaryTypeDef",
    {
        "AutoMLJobName": str,
        "AutoMLJobArn": str,
        "AutoMLJobStatus": Literal["Completed", "InProgress", "Failed", "Stopped", "Stopping"],
        "AutoMLJobSecondaryStatus": Literal[
            "Starting",
            "AnalyzingData",
            "FeatureEngineering",
            "ModelTuning",
            "MaxCandidatesReached",
            "Failed",
            "Stopped",
            "MaxAutoMLJobRuntimeReached",
            "Stopping",
            "CandidateDefinitionsGenerated",
        ],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)
_OptionalAutoMLJobSummaryTypeDef = TypedDict(
    "_OptionalAutoMLJobSummaryTypeDef", {"EndTime": datetime, "FailureReason": str}, total=False
)


class AutoMLJobSummaryTypeDef(_RequiredAutoMLJobSummaryTypeDef, _OptionalAutoMLJobSummaryTypeDef):
    pass


_RequiredListAutoMLJobsResponseTypeDef = TypedDict(
    "_RequiredListAutoMLJobsResponseTypeDef", {"AutoMLJobSummaries": List[AutoMLJobSummaryTypeDef]}
)
_OptionalListAutoMLJobsResponseTypeDef = TypedDict(
    "_OptionalListAutoMLJobsResponseTypeDef", {"NextToken": str}, total=False
)


class ListAutoMLJobsResponseTypeDef(
    _RequiredListAutoMLJobsResponseTypeDef, _OptionalListAutoMLJobsResponseTypeDef
):
    pass


_RequiredListCandidatesForAutoMLJobResponseTypeDef = TypedDict(
    "_RequiredListCandidatesForAutoMLJobResponseTypeDef",
    {"Candidates": List[AutoMLCandidateTypeDef]},
)
_OptionalListCandidatesForAutoMLJobResponseTypeDef = TypedDict(
    "_OptionalListCandidatesForAutoMLJobResponseTypeDef", {"NextToken": str}, total=False
)


class ListCandidatesForAutoMLJobResponseTypeDef(
    _RequiredListCandidatesForAutoMLJobResponseTypeDef,
    _OptionalListCandidatesForAutoMLJobResponseTypeDef,
):
    pass


_RequiredCodeRepositorySummaryTypeDef = TypedDict(
    "_RequiredCodeRepositorySummaryTypeDef",
    {
        "CodeRepositoryName": str,
        "CodeRepositoryArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
)
_OptionalCodeRepositorySummaryTypeDef = TypedDict(
    "_OptionalCodeRepositorySummaryTypeDef", {"GitConfig": GitConfigTypeDef}, total=False
)


class CodeRepositorySummaryTypeDef(
    _RequiredCodeRepositorySummaryTypeDef, _OptionalCodeRepositorySummaryTypeDef
):
    pass


_RequiredListCodeRepositoriesOutputTypeDef = TypedDict(
    "_RequiredListCodeRepositoriesOutputTypeDef",
    {"CodeRepositorySummaryList": List[CodeRepositorySummaryTypeDef]},
)
_OptionalListCodeRepositoriesOutputTypeDef = TypedDict(
    "_OptionalListCodeRepositoriesOutputTypeDef", {"NextToken": str}, total=False
)


class ListCodeRepositoriesOutputTypeDef(
    _RequiredListCodeRepositoriesOutputTypeDef, _OptionalListCodeRepositoriesOutputTypeDef
):
    pass


_RequiredCompilationJobSummaryTypeDef = TypedDict(
    "_RequiredCompilationJobSummaryTypeDef",
    {
        "CompilationJobName": str,
        "CompilationJobArn": str,
        "CreationTime": datetime,
        "CompilationTargetDevice": Literal[
            "lambda",
            "ml_m4",
            "ml_m5",
            "ml_c4",
            "ml_c5",
            "ml_p2",
            "ml_p3",
            "ml_inf1",
            "jetson_tx1",
            "jetson_tx2",
            "jetson_nano",
            "jetson_xavier",
            "rasp3b",
            "imx8qm",
            "deeplens",
            "rk3399",
            "rk3288",
            "aisage",
            "sbe_c",
            "qcs605",
            "qcs603",
            "sitara_am57x",
            "amba_cv22",
        ],
        "CompilationJobStatus": Literal[
            "INPROGRESS", "COMPLETED", "FAILED", "STARTING", "STOPPING", "STOPPED"
        ],
    },
)
_OptionalCompilationJobSummaryTypeDef = TypedDict(
    "_OptionalCompilationJobSummaryTypeDef",
    {
        "CompilationStartTime": datetime,
        "CompilationEndTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)


class CompilationJobSummaryTypeDef(
    _RequiredCompilationJobSummaryTypeDef, _OptionalCompilationJobSummaryTypeDef
):
    pass


_RequiredListCompilationJobsResponseTypeDef = TypedDict(
    "_RequiredListCompilationJobsResponseTypeDef",
    {"CompilationJobSummaries": List[CompilationJobSummaryTypeDef]},
)
_OptionalListCompilationJobsResponseTypeDef = TypedDict(
    "_OptionalListCompilationJobsResponseTypeDef", {"NextToken": str}, total=False
)


class ListCompilationJobsResponseTypeDef(
    _RequiredListCompilationJobsResponseTypeDef, _OptionalListCompilationJobsResponseTypeDef
):
    pass


DomainDetailsTypeDef = TypedDict(
    "DomainDetailsTypeDef",
    {
        "DomainArn": str,
        "DomainId": str,
        "DomainName": str,
        "Status": Literal["Deleting", "Failed", "InService", "Pending"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Url": str,
    },
    total=False,
)

ListDomainsResponseTypeDef = TypedDict(
    "ListDomainsResponseTypeDef",
    {"Domains": List[DomainDetailsTypeDef], "NextToken": str},
    total=False,
)

EndpointConfigSummaryTypeDef = TypedDict(
    "EndpointConfigSummaryTypeDef",
    {"EndpointConfigName": str, "EndpointConfigArn": str, "CreationTime": datetime},
)

_RequiredListEndpointConfigsOutputTypeDef = TypedDict(
    "_RequiredListEndpointConfigsOutputTypeDef",
    {"EndpointConfigs": List[EndpointConfigSummaryTypeDef]},
)
_OptionalListEndpointConfigsOutputTypeDef = TypedDict(
    "_OptionalListEndpointConfigsOutputTypeDef", {"NextToken": str}, total=False
)


class ListEndpointConfigsOutputTypeDef(
    _RequiredListEndpointConfigsOutputTypeDef, _OptionalListEndpointConfigsOutputTypeDef
):
    pass


EndpointSummaryTypeDef = TypedDict(
    "EndpointSummaryTypeDef",
    {
        "EndpointName": str,
        "EndpointArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "EndpointStatus": Literal[
            "OutOfService",
            "Creating",
            "Updating",
            "SystemUpdating",
            "RollingBack",
            "InService",
            "Deleting",
            "Failed",
        ],
    },
)

_RequiredListEndpointsOutputTypeDef = TypedDict(
    "_RequiredListEndpointsOutputTypeDef", {"Endpoints": List[EndpointSummaryTypeDef]}
)
_OptionalListEndpointsOutputTypeDef = TypedDict(
    "_OptionalListEndpointsOutputTypeDef", {"NextToken": str}, total=False
)


class ListEndpointsOutputTypeDef(
    _RequiredListEndpointsOutputTypeDef, _OptionalListEndpointsOutputTypeDef
):
    pass


ExperimentSummaryTypeDef = TypedDict(
    "ExperimentSummaryTypeDef",
    {
        "ExperimentArn": str,
        "ExperimentName": str,
        "DisplayName": str,
        "ExperimentSource": ExperimentSourceTypeDef,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

ListExperimentsResponseTypeDef = TypedDict(
    "ListExperimentsResponseTypeDef",
    {"ExperimentSummaries": List[ExperimentSummaryTypeDef], "NextToken": str},
    total=False,
)

_RequiredFlowDefinitionSummaryTypeDef = TypedDict(
    "_RequiredFlowDefinitionSummaryTypeDef",
    {
        "FlowDefinitionName": str,
        "FlowDefinitionArn": str,
        "FlowDefinitionStatus": Literal["Initializing", "Active", "Failed", "Deleting"],
        "CreationTime": datetime,
    },
)
_OptionalFlowDefinitionSummaryTypeDef = TypedDict(
    "_OptionalFlowDefinitionSummaryTypeDef", {"FailureReason": str}, total=False
)


class FlowDefinitionSummaryTypeDef(
    _RequiredFlowDefinitionSummaryTypeDef, _OptionalFlowDefinitionSummaryTypeDef
):
    pass


_RequiredListFlowDefinitionsResponseTypeDef = TypedDict(
    "_RequiredListFlowDefinitionsResponseTypeDef",
    {"FlowDefinitionSummaries": List[FlowDefinitionSummaryTypeDef]},
)
_OptionalListFlowDefinitionsResponseTypeDef = TypedDict(
    "_OptionalListFlowDefinitionsResponseTypeDef", {"NextToken": str}, total=False
)


class ListFlowDefinitionsResponseTypeDef(
    _RequiredListFlowDefinitionsResponseTypeDef, _OptionalListFlowDefinitionsResponseTypeDef
):
    pass


HumanTaskUiSummaryTypeDef = TypedDict(
    "HumanTaskUiSummaryTypeDef",
    {"HumanTaskUiName": str, "HumanTaskUiArn": str, "CreationTime": datetime},
)

_RequiredListHumanTaskUisResponseTypeDef = TypedDict(
    "_RequiredListHumanTaskUisResponseTypeDef",
    {"HumanTaskUiSummaries": List[HumanTaskUiSummaryTypeDef]},
)
_OptionalListHumanTaskUisResponseTypeDef = TypedDict(
    "_OptionalListHumanTaskUisResponseTypeDef", {"NextToken": str}, total=False
)


class ListHumanTaskUisResponseTypeDef(
    _RequiredListHumanTaskUisResponseTypeDef, _OptionalListHumanTaskUisResponseTypeDef
):
    pass


_RequiredHyperParameterTuningJobSummaryTypeDef = TypedDict(
    "_RequiredHyperParameterTuningJobSummaryTypeDef",
    {
        "HyperParameterTuningJobName": str,
        "HyperParameterTuningJobArn": str,
        "HyperParameterTuningJobStatus": Literal[
            "Completed", "InProgress", "Failed", "Stopped", "Stopping"
        ],
        "Strategy": Literal["Bayesian", "Random"],
        "CreationTime": datetime,
        "TrainingJobStatusCounters": TrainingJobStatusCountersTypeDef,
        "ObjectiveStatusCounters": ObjectiveStatusCountersTypeDef,
    },
)
_OptionalHyperParameterTuningJobSummaryTypeDef = TypedDict(
    "_OptionalHyperParameterTuningJobSummaryTypeDef",
    {
        "HyperParameterTuningEndTime": datetime,
        "LastModifiedTime": datetime,
        "ResourceLimits": ResourceLimitsTypeDef,
    },
    total=False,
)


class HyperParameterTuningJobSummaryTypeDef(
    _RequiredHyperParameterTuningJobSummaryTypeDef, _OptionalHyperParameterTuningJobSummaryTypeDef
):
    pass


_RequiredListHyperParameterTuningJobsResponseTypeDef = TypedDict(
    "_RequiredListHyperParameterTuningJobsResponseTypeDef",
    {"HyperParameterTuningJobSummaries": List[HyperParameterTuningJobSummaryTypeDef]},
)
_OptionalListHyperParameterTuningJobsResponseTypeDef = TypedDict(
    "_OptionalListHyperParameterTuningJobsResponseTypeDef", {"NextToken": str}, total=False
)


class ListHyperParameterTuningJobsResponseTypeDef(
    _RequiredListHyperParameterTuningJobsResponseTypeDef,
    _OptionalListHyperParameterTuningJobsResponseTypeDef,
):
    pass


LabelCountersForWorkteamTypeDef = TypedDict(
    "LabelCountersForWorkteamTypeDef",
    {"HumanLabeled": int, "PendingHuman": int, "Total": int},
    total=False,
)

_RequiredLabelingJobForWorkteamSummaryTypeDef = TypedDict(
    "_RequiredLabelingJobForWorkteamSummaryTypeDef",
    {"JobReferenceCode": str, "WorkRequesterAccountId": str, "CreationTime": datetime},
)
_OptionalLabelingJobForWorkteamSummaryTypeDef = TypedDict(
    "_OptionalLabelingJobForWorkteamSummaryTypeDef",
    {
        "LabelingJobName": str,
        "LabelCounters": LabelCountersForWorkteamTypeDef,
        "NumberOfHumanWorkersPerDataObject": int,
    },
    total=False,
)


class LabelingJobForWorkteamSummaryTypeDef(
    _RequiredLabelingJobForWorkteamSummaryTypeDef, _OptionalLabelingJobForWorkteamSummaryTypeDef
):
    pass


_RequiredListLabelingJobsForWorkteamResponseTypeDef = TypedDict(
    "_RequiredListLabelingJobsForWorkteamResponseTypeDef",
    {"LabelingJobSummaryList": List[LabelingJobForWorkteamSummaryTypeDef]},
)
_OptionalListLabelingJobsForWorkteamResponseTypeDef = TypedDict(
    "_OptionalListLabelingJobsForWorkteamResponseTypeDef", {"NextToken": str}, total=False
)


class ListLabelingJobsForWorkteamResponseTypeDef(
    _RequiredListLabelingJobsForWorkteamResponseTypeDef,
    _OptionalListLabelingJobsForWorkteamResponseTypeDef,
):
    pass


_RequiredLabelingJobSummaryTypeDef = TypedDict(
    "_RequiredLabelingJobSummaryTypeDef",
    {
        "LabelingJobName": str,
        "LabelingJobArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LabelingJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
        "LabelCounters": LabelCountersTypeDef,
        "WorkteamArn": str,
        "PreHumanTaskLambdaArn": str,
    },
)
_OptionalLabelingJobSummaryTypeDef = TypedDict(
    "_OptionalLabelingJobSummaryTypeDef",
    {
        "AnnotationConsolidationLambdaArn": str,
        "FailureReason": str,
        "LabelingJobOutput": LabelingJobOutputTypeDef,
        "InputConfig": LabelingJobInputConfigTypeDef,
    },
    total=False,
)


class LabelingJobSummaryTypeDef(
    _RequiredLabelingJobSummaryTypeDef, _OptionalLabelingJobSummaryTypeDef
):
    pass


ListLabelingJobsResponseTypeDef = TypedDict(
    "ListLabelingJobsResponseTypeDef",
    {"LabelingJobSummaryList": List[LabelingJobSummaryTypeDef], "NextToken": str},
    total=False,
)

_RequiredModelPackageSummaryTypeDef = TypedDict(
    "_RequiredModelPackageSummaryTypeDef",
    {
        "ModelPackageName": str,
        "ModelPackageArn": str,
        "CreationTime": datetime,
        "ModelPackageStatus": Literal["Pending", "InProgress", "Completed", "Failed", "Deleting"],
    },
)
_OptionalModelPackageSummaryTypeDef = TypedDict(
    "_OptionalModelPackageSummaryTypeDef", {"ModelPackageDescription": str}, total=False
)


class ModelPackageSummaryTypeDef(
    _RequiredModelPackageSummaryTypeDef, _OptionalModelPackageSummaryTypeDef
):
    pass


_RequiredListModelPackagesOutputTypeDef = TypedDict(
    "_RequiredListModelPackagesOutputTypeDef",
    {"ModelPackageSummaryList": List[ModelPackageSummaryTypeDef]},
)
_OptionalListModelPackagesOutputTypeDef = TypedDict(
    "_OptionalListModelPackagesOutputTypeDef", {"NextToken": str}, total=False
)


class ListModelPackagesOutputTypeDef(
    _RequiredListModelPackagesOutputTypeDef, _OptionalListModelPackagesOutputTypeDef
):
    pass


ModelSummaryTypeDef = TypedDict(
    "ModelSummaryTypeDef", {"ModelName": str, "ModelArn": str, "CreationTime": datetime}
)

_RequiredListModelsOutputTypeDef = TypedDict(
    "_RequiredListModelsOutputTypeDef", {"Models": List[ModelSummaryTypeDef]}
)
_OptionalListModelsOutputTypeDef = TypedDict(
    "_OptionalListModelsOutputTypeDef", {"NextToken": str}, total=False
)


class ListModelsOutputTypeDef(_RequiredListModelsOutputTypeDef, _OptionalListModelsOutputTypeDef):
    pass


_RequiredListMonitoringExecutionsResponseTypeDef = TypedDict(
    "_RequiredListMonitoringExecutionsResponseTypeDef",
    {"MonitoringExecutionSummaries": List[MonitoringExecutionSummaryTypeDef]},
)
_OptionalListMonitoringExecutionsResponseTypeDef = TypedDict(
    "_OptionalListMonitoringExecutionsResponseTypeDef", {"NextToken": str}, total=False
)


class ListMonitoringExecutionsResponseTypeDef(
    _RequiredListMonitoringExecutionsResponseTypeDef,
    _OptionalListMonitoringExecutionsResponseTypeDef,
):
    pass


_RequiredMonitoringScheduleSummaryTypeDef = TypedDict(
    "_RequiredMonitoringScheduleSummaryTypeDef",
    {
        "MonitoringScheduleName": str,
        "MonitoringScheduleArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "MonitoringScheduleStatus": Literal["Pending", "Failed", "Scheduled", "Stopped"],
    },
)
_OptionalMonitoringScheduleSummaryTypeDef = TypedDict(
    "_OptionalMonitoringScheduleSummaryTypeDef", {"EndpointName": str}, total=False
)


class MonitoringScheduleSummaryTypeDef(
    _RequiredMonitoringScheduleSummaryTypeDef, _OptionalMonitoringScheduleSummaryTypeDef
):
    pass


_RequiredListMonitoringSchedulesResponseTypeDef = TypedDict(
    "_RequiredListMonitoringSchedulesResponseTypeDef",
    {"MonitoringScheduleSummaries": List[MonitoringScheduleSummaryTypeDef]},
)
_OptionalListMonitoringSchedulesResponseTypeDef = TypedDict(
    "_OptionalListMonitoringSchedulesResponseTypeDef", {"NextToken": str}, total=False
)


class ListMonitoringSchedulesResponseTypeDef(
    _RequiredListMonitoringSchedulesResponseTypeDef, _OptionalListMonitoringSchedulesResponseTypeDef
):
    pass


_RequiredNotebookInstanceLifecycleConfigSummaryTypeDef = TypedDict(
    "_RequiredNotebookInstanceLifecycleConfigSummaryTypeDef",
    {"NotebookInstanceLifecycleConfigName": str, "NotebookInstanceLifecycleConfigArn": str},
)
_OptionalNotebookInstanceLifecycleConfigSummaryTypeDef = TypedDict(
    "_OptionalNotebookInstanceLifecycleConfigSummaryTypeDef",
    {"CreationTime": datetime, "LastModifiedTime": datetime},
    total=False,
)


class NotebookInstanceLifecycleConfigSummaryTypeDef(
    _RequiredNotebookInstanceLifecycleConfigSummaryTypeDef,
    _OptionalNotebookInstanceLifecycleConfigSummaryTypeDef,
):
    pass


ListNotebookInstanceLifecycleConfigsOutputTypeDef = TypedDict(
    "ListNotebookInstanceLifecycleConfigsOutputTypeDef",
    {
        "NextToken": str,
        "NotebookInstanceLifecycleConfigs": List[NotebookInstanceLifecycleConfigSummaryTypeDef],
    },
    total=False,
)

_RequiredNotebookInstanceSummaryTypeDef = TypedDict(
    "_RequiredNotebookInstanceSummaryTypeDef",
    {"NotebookInstanceName": str, "NotebookInstanceArn": str},
)
_OptionalNotebookInstanceSummaryTypeDef = TypedDict(
    "_OptionalNotebookInstanceSummaryTypeDef",
    {
        "NotebookInstanceStatus": Literal[
            "Pending", "InService", "Stopping", "Stopped", "Failed", "Deleting", "Updating"
        ],
        "Url": str,
        "InstanceType": Literal[
            "ml.t2.medium",
            "ml.t2.large",
            "ml.t2.xlarge",
            "ml.t2.2xlarge",
            "ml.t3.medium",
            "ml.t3.large",
            "ml.t3.xlarge",
            "ml.t3.2xlarge",
            "ml.m4.xlarge",
            "ml.m4.2xlarge",
            "ml.m4.4xlarge",
            "ml.m4.10xlarge",
            "ml.m4.16xlarge",
            "ml.m5.xlarge",
            "ml.m5.2xlarge",
            "ml.m5.4xlarge",
            "ml.m5.12xlarge",
            "ml.m5.24xlarge",
            "ml.c4.xlarge",
            "ml.c4.2xlarge",
            "ml.c4.4xlarge",
            "ml.c4.8xlarge",
            "ml.c5.xlarge",
            "ml.c5.2xlarge",
            "ml.c5.4xlarge",
            "ml.c5.9xlarge",
            "ml.c5.18xlarge",
            "ml.c5d.xlarge",
            "ml.c5d.2xlarge",
            "ml.c5d.4xlarge",
            "ml.c5d.9xlarge",
            "ml.c5d.18xlarge",
            "ml.p2.xlarge",
            "ml.p2.8xlarge",
            "ml.p2.16xlarge",
            "ml.p3.2xlarge",
            "ml.p3.8xlarge",
            "ml.p3.16xlarge",
        ],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "NotebookInstanceLifecycleConfigName": str,
        "DefaultCodeRepository": str,
        "AdditionalCodeRepositories": List[str],
    },
    total=False,
)


class NotebookInstanceSummaryTypeDef(
    _RequiredNotebookInstanceSummaryTypeDef, _OptionalNotebookInstanceSummaryTypeDef
):
    pass


ListNotebookInstancesOutputTypeDef = TypedDict(
    "ListNotebookInstancesOutputTypeDef",
    {"NextToken": str, "NotebookInstances": List[NotebookInstanceSummaryTypeDef]},
    total=False,
)

_RequiredProcessingJobSummaryTypeDef = TypedDict(
    "_RequiredProcessingJobSummaryTypeDef",
    {
        "ProcessingJobName": str,
        "ProcessingJobArn": str,
        "CreationTime": datetime,
        "ProcessingJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
    },
)
_OptionalProcessingJobSummaryTypeDef = TypedDict(
    "_OptionalProcessingJobSummaryTypeDef",
    {
        "ProcessingEndTime": datetime,
        "LastModifiedTime": datetime,
        "FailureReason": str,
        "ExitMessage": str,
    },
    total=False,
)


class ProcessingJobSummaryTypeDef(
    _RequiredProcessingJobSummaryTypeDef, _OptionalProcessingJobSummaryTypeDef
):
    pass


_RequiredListProcessingJobsResponseTypeDef = TypedDict(
    "_RequiredListProcessingJobsResponseTypeDef",
    {"ProcessingJobSummaries": List[ProcessingJobSummaryTypeDef]},
)
_OptionalListProcessingJobsResponseTypeDef = TypedDict(
    "_OptionalListProcessingJobsResponseTypeDef", {"NextToken": str}, total=False
)


class ListProcessingJobsResponseTypeDef(
    _RequiredListProcessingJobsResponseTypeDef, _OptionalListProcessingJobsResponseTypeDef
):
    pass


_RequiredListSubscribedWorkteamsResponseTypeDef = TypedDict(
    "_RequiredListSubscribedWorkteamsResponseTypeDef",
    {"SubscribedWorkteams": List[SubscribedWorkteamTypeDef]},
)
_OptionalListSubscribedWorkteamsResponseTypeDef = TypedDict(
    "_OptionalListSubscribedWorkteamsResponseTypeDef", {"NextToken": str}, total=False
)


class ListSubscribedWorkteamsResponseTypeDef(
    _RequiredListSubscribedWorkteamsResponseTypeDef, _OptionalListSubscribedWorkteamsResponseTypeDef
):
    pass


ListTagsOutputTypeDef = TypedDict(
    "ListTagsOutputTypeDef", {"Tags": List[TagTypeDef], "NextToken": str}, total=False
)

_RequiredListTrainingJobsForHyperParameterTuningJobResponseTypeDef = TypedDict(
    "_RequiredListTrainingJobsForHyperParameterTuningJobResponseTypeDef",
    {"TrainingJobSummaries": List[HyperParameterTrainingJobSummaryTypeDef]},
)
_OptionalListTrainingJobsForHyperParameterTuningJobResponseTypeDef = TypedDict(
    "_OptionalListTrainingJobsForHyperParameterTuningJobResponseTypeDef",
    {"NextToken": str},
    total=False,
)


class ListTrainingJobsForHyperParameterTuningJobResponseTypeDef(
    _RequiredListTrainingJobsForHyperParameterTuningJobResponseTypeDef,
    _OptionalListTrainingJobsForHyperParameterTuningJobResponseTypeDef,
):
    pass


_RequiredTrainingJobSummaryTypeDef = TypedDict(
    "_RequiredTrainingJobSummaryTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "CreationTime": datetime,
        "TrainingJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
    },
)
_OptionalTrainingJobSummaryTypeDef = TypedDict(
    "_OptionalTrainingJobSummaryTypeDef",
    {"TrainingEndTime": datetime, "LastModifiedTime": datetime},
    total=False,
)


class TrainingJobSummaryTypeDef(
    _RequiredTrainingJobSummaryTypeDef, _OptionalTrainingJobSummaryTypeDef
):
    pass


_RequiredListTrainingJobsResponseTypeDef = TypedDict(
    "_RequiredListTrainingJobsResponseTypeDef",
    {"TrainingJobSummaries": List[TrainingJobSummaryTypeDef]},
)
_OptionalListTrainingJobsResponseTypeDef = TypedDict(
    "_OptionalListTrainingJobsResponseTypeDef", {"NextToken": str}, total=False
)


class ListTrainingJobsResponseTypeDef(
    _RequiredListTrainingJobsResponseTypeDef, _OptionalListTrainingJobsResponseTypeDef
):
    pass


_RequiredTransformJobSummaryTypeDef = TypedDict(
    "_RequiredTransformJobSummaryTypeDef",
    {
        "TransformJobName": str,
        "TransformJobArn": str,
        "CreationTime": datetime,
        "TransformJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
    },
)
_OptionalTransformJobSummaryTypeDef = TypedDict(
    "_OptionalTransformJobSummaryTypeDef",
    {"TransformEndTime": datetime, "LastModifiedTime": datetime, "FailureReason": str},
    total=False,
)


class TransformJobSummaryTypeDef(
    _RequiredTransformJobSummaryTypeDef, _OptionalTransformJobSummaryTypeDef
):
    pass


_RequiredListTransformJobsResponseTypeDef = TypedDict(
    "_RequiredListTransformJobsResponseTypeDef",
    {"TransformJobSummaries": List[TransformJobSummaryTypeDef]},
)
_OptionalListTransformJobsResponseTypeDef = TypedDict(
    "_OptionalListTransformJobsResponseTypeDef", {"NextToken": str}, total=False
)


class ListTransformJobsResponseTypeDef(
    _RequiredListTransformJobsResponseTypeDef, _OptionalListTransformJobsResponseTypeDef
):
    pass


TrialComponentSummaryTypeDef = TypedDict(
    "TrialComponentSummaryTypeDef",
    {
        "TrialComponentName": str,
        "TrialComponentArn": str,
        "DisplayName": str,
        "TrialComponentSource": TrialComponentSourceTypeDef,
        "Status": TrialComponentStatusTypeDef,
        "StartTime": datetime,
        "EndTime": datetime,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
    },
    total=False,
)

ListTrialComponentsResponseTypeDef = TypedDict(
    "ListTrialComponentsResponseTypeDef",
    {"TrialComponentSummaries": List[TrialComponentSummaryTypeDef], "NextToken": str},
    total=False,
)

TrialSummaryTypeDef = TypedDict(
    "TrialSummaryTypeDef",
    {
        "TrialArn": str,
        "TrialName": str,
        "DisplayName": str,
        "TrialSource": TrialSourceTypeDef,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

ListTrialsResponseTypeDef = TypedDict(
    "ListTrialsResponseTypeDef",
    {"TrialSummaries": List[TrialSummaryTypeDef], "NextToken": str},
    total=False,
)

UserProfileDetailsTypeDef = TypedDict(
    "UserProfileDetailsTypeDef",
    {
        "DomainId": str,
        "UserProfileName": str,
        "Status": Literal["Deleting", "Failed", "InService", "Pending"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

ListUserProfilesResponseTypeDef = TypedDict(
    "ListUserProfilesResponseTypeDef",
    {"UserProfiles": List[UserProfileDetailsTypeDef], "NextToken": str},
    total=False,
)

_RequiredListWorkteamsResponseTypeDef = TypedDict(
    "_RequiredListWorkteamsResponseTypeDef", {"Workteams": List[WorkteamTypeDef]}
)
_OptionalListWorkteamsResponseTypeDef = TypedDict(
    "_OptionalListWorkteamsResponseTypeDef", {"NextToken": str}, total=False
)


class ListWorkteamsResponseTypeDef(
    _RequiredListWorkteamsResponseTypeDef, _OptionalListWorkteamsResponseTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

RenderingErrorTypeDef = TypedDict("RenderingErrorTypeDef", {"Code": str, "Message": str})

RenderUiTemplateResponseTypeDef = TypedDict(
    "RenderUiTemplateResponseTypeDef",
    {"RenderedContent": str, "Errors": List[RenderingErrorTypeDef]},
)

RenderableTaskTypeDef = TypedDict("RenderableTaskTypeDef", {"Input": str})

RetentionPolicyTypeDef = TypedDict(
    "RetentionPolicyTypeDef", {"HomeEfsFileSystem": Literal["Retain", "Delete"]}, total=False
)

_RequiredFilterTypeDef = TypedDict("_RequiredFilterTypeDef", {"Name": str})
_OptionalFilterTypeDef = TypedDict(
    "_OptionalFilterTypeDef",
    {
        "Operator": Literal[
            "Equals",
            "NotEquals",
            "GreaterThan",
            "GreaterThanOrEqualTo",
            "LessThan",
            "LessThanOrEqualTo",
            "Contains",
            "Exists",
            "NotExists",
            "In",
        ],
        "Value": str,
    },
    total=False,
)


class FilterTypeDef(_RequiredFilterTypeDef, _OptionalFilterTypeDef):
    pass


NestedFiltersTypeDef = TypedDict(
    "NestedFiltersTypeDef", {"NestedPropertyName": str, "Filters": List[FilterTypeDef]}
)

SearchExpressionTypeDef = TypedDict(
    "SearchExpressionTypeDef",
    {
        "Filters": List[FilterTypeDef],
        "NestedFilters": List[NestedFiltersTypeDef],
        "SubExpressions": List["SearchExpressionTypeDef"],
        "Operator": Literal["And", "Or"],
    },
    total=False,
)

ExperimentTypeDef = TypedDict(
    "ExperimentTypeDef",
    {
        "ExperimentName": str,
        "ExperimentArn": str,
        "DisplayName": str,
        "Source": ExperimentSourceTypeDef,
        "Description": str,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

TrainingJobTypeDef = TypedDict(
    "TrainingJobTypeDef",
    {
        "TrainingJobName": str,
        "TrainingJobArn": str,
        "TuningJobArn": str,
        "LabelingJobArn": str,
        "AutoMLJobArn": str,
        "ModelArtifacts": ModelArtifactsTypeDef,
        "TrainingJobStatus": Literal["InProgress", "Completed", "Failed", "Stopping", "Stopped"],
        "SecondaryStatus": Literal[
            "Starting",
            "LaunchingMLInstances",
            "PreparingTrainingStack",
            "Downloading",
            "DownloadingTrainingImage",
            "Training",
            "Uploading",
            "Stopping",
            "Stopped",
            "MaxRuntimeExceeded",
            "Completed",
            "Failed",
            "Interrupted",
            "MaxWaitTimeExceeded",
        ],
        "FailureReason": str,
        "HyperParameters": Dict[str, str],
        "AlgorithmSpecification": AlgorithmSpecificationTypeDef,
        "RoleArn": str,
        "InputDataConfig": List[ChannelTypeDef],
        "OutputDataConfig": OutputDataConfigTypeDef,
        "ResourceConfig": ResourceConfigTypeDef,
        "VpcConfig": VpcConfigTypeDef,
        "StoppingCondition": StoppingConditionTypeDef,
        "CreationTime": datetime,
        "TrainingStartTime": datetime,
        "TrainingEndTime": datetime,
        "LastModifiedTime": datetime,
        "SecondaryStatusTransitions": List[SecondaryStatusTransitionTypeDef],
        "FinalMetricDataList": List[MetricDataTypeDef],
        "EnableNetworkIsolation": bool,
        "EnableInterContainerTrafficEncryption": bool,
        "EnableManagedSpotTraining": bool,
        "CheckpointConfig": CheckpointConfigTypeDef,
        "TrainingTimeInSeconds": int,
        "BillableTimeInSeconds": int,
        "DebugHookConfig": DebugHookConfigTypeDef,
        "ExperimentConfig": ExperimentConfigTypeDef,
        "DebugRuleConfigurations": List[DebugRuleConfigurationTypeDef],
        "TensorBoardOutputConfig": TensorBoardOutputConfigTypeDef,
        "DebugRuleEvaluationStatuses": List[DebugRuleEvaluationStatusTypeDef],
        "Tags": List[TagTypeDef],
    },
    total=False,
)

ParentTypeDef = TypedDict("ParentTypeDef", {"TrialName": str, "ExperimentName": str}, total=False)

TrialComponentSourceDetailTypeDef = TypedDict(
    "TrialComponentSourceDetailTypeDef",
    {"SourceArn": str, "TrainingJob": TrainingJobTypeDef},
    total=False,
)

TrialComponentTypeDef = TypedDict(
    "TrialComponentTypeDef",
    {
        "TrialComponentName": str,
        "DisplayName": str,
        "TrialComponentArn": str,
        "Source": TrialComponentSourceTypeDef,
        "Status": TrialComponentStatusTypeDef,
        "StartTime": datetime,
        "EndTime": datetime,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "Parameters": Dict[str, TrialComponentParameterValueTypeDef],
        "InputArtifacts": Dict[str, TrialComponentArtifactTypeDef],
        "OutputArtifacts": Dict[str, TrialComponentArtifactTypeDef],
        "Metrics": List[TrialComponentMetricSummaryTypeDef],
        "SourceDetail": TrialComponentSourceDetailTypeDef,
        "Tags": List[TagTypeDef],
        "Parents": List[ParentTypeDef],
    },
    total=False,
)

TrialComponentSimpleSummaryTypeDef = TypedDict(
    "TrialComponentSimpleSummaryTypeDef",
    {
        "TrialComponentName": str,
        "TrialComponentArn": str,
        "TrialComponentSource": TrialComponentSourceTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
    },
    total=False,
)

TrialTypeDef = TypedDict(
    "TrialTypeDef",
    {
        "TrialName": str,
        "TrialArn": str,
        "DisplayName": str,
        "ExperimentName": str,
        "Source": TrialSourceTypeDef,
        "CreationTime": datetime,
        "CreatedBy": UserContextTypeDef,
        "LastModifiedTime": datetime,
        "LastModifiedBy": UserContextTypeDef,
        "Tags": List[TagTypeDef],
        "TrialComponentSummaries": List[TrialComponentSimpleSummaryTypeDef],
    },
    total=False,
)

SearchRecordTypeDef = TypedDict(
    "SearchRecordTypeDef",
    {
        "TrainingJob": TrainingJobTypeDef,
        "Experiment": ExperimentTypeDef,
        "Trial": TrialTypeDef,
        "TrialComponent": TrialComponentTypeDef,
    },
    total=False,
)

SearchResponseTypeDef = TypedDict(
    "SearchResponseTypeDef", {"Results": List[SearchRecordTypeDef], "NextToken": str}, total=False
)

PropertyNameQueryTypeDef = TypedDict("PropertyNameQueryTypeDef", {"PropertyNameHint": str})

SuggestionQueryTypeDef = TypedDict(
    "SuggestionQueryTypeDef", {"PropertyNameQuery": PropertyNameQueryTypeDef}, total=False
)

UiTemplateTypeDef = TypedDict("UiTemplateTypeDef", {"Content": str})

UpdateCodeRepositoryOutputTypeDef = TypedDict(
    "UpdateCodeRepositoryOutputTypeDef", {"CodeRepositoryArn": str}
)

UpdateDomainResponseTypeDef = TypedDict(
    "UpdateDomainResponseTypeDef", {"DomainArn": str}, total=False
)

UpdateEndpointOutputTypeDef = TypedDict("UpdateEndpointOutputTypeDef", {"EndpointArn": str})

UpdateEndpointWeightsAndCapacitiesOutputTypeDef = TypedDict(
    "UpdateEndpointWeightsAndCapacitiesOutputTypeDef", {"EndpointArn": str}
)

UpdateExperimentResponseTypeDef = TypedDict(
    "UpdateExperimentResponseTypeDef", {"ExperimentArn": str}, total=False
)

UpdateMonitoringScheduleResponseTypeDef = TypedDict(
    "UpdateMonitoringScheduleResponseTypeDef", {"MonitoringScheduleArn": str}
)

UpdateTrialComponentResponseTypeDef = TypedDict(
    "UpdateTrialComponentResponseTypeDef", {"TrialComponentArn": str}, total=False
)

UpdateTrialResponseTypeDef = TypedDict("UpdateTrialResponseTypeDef", {"TrialArn": str}, total=False)

UpdateUserProfileResponseTypeDef = TypedDict(
    "UpdateUserProfileResponseTypeDef", {"UserProfileArn": str}, total=False
)

UpdateWorkforceResponseTypeDef = TypedDict(
    "UpdateWorkforceResponseTypeDef", {"Workforce": WorkforceTypeDef}
)

UpdateWorkteamResponseTypeDef = TypedDict(
    "UpdateWorkteamResponseTypeDef", {"Workteam": WorkteamTypeDef}
)

VariantPropertyTypeDef = TypedDict(
    "VariantPropertyTypeDef",
    {"VariantPropertyType": Literal["DesiredInstanceCount", "DesiredWeight", "DataCaptureConfig"]},
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
