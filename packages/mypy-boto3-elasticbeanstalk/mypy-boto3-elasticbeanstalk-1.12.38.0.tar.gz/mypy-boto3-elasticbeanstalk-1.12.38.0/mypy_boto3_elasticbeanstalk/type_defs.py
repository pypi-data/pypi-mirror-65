"""
Main interface for elasticbeanstalk service type definitions.

Usage::

    from mypy_boto3.elasticbeanstalk.type_defs import MaxAgeRuleTypeDef

    data: MaxAgeRuleTypeDef = {...}
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
    "MaxAgeRuleTypeDef",
    "MaxCountRuleTypeDef",
    "ApplicationVersionLifecycleConfigTypeDef",
    "ApplicationResourceLifecycleConfigTypeDef",
    "ApplicationDescriptionTypeDef",
    "ApplicationDescriptionMessageTypeDef",
    "ApplicationDescriptionsMessageTypeDef",
    "ApplicationResourceLifecycleDescriptionMessageTypeDef",
    "S3LocationTypeDef",
    "SourceBuildInformationTypeDef",
    "ApplicationVersionDescriptionTypeDef",
    "ApplicationVersionDescriptionMessageTypeDef",
    "ApplicationVersionDescriptionsMessageTypeDef",
    "ApplyEnvironmentManagedActionResultTypeDef",
    "BuildConfigurationTypeDef",
    "CheckDNSAvailabilityResultMessageTypeDef",
    "ConfigurationOptionSettingTypeDef",
    "OptionRestrictionRegexTypeDef",
    "ConfigurationOptionDescriptionTypeDef",
    "ConfigurationOptionsDescriptionTypeDef",
    "ConfigurationSettingsDescriptionTypeDef",
    "ConfigurationSettingsDescriptionsTypeDef",
    "ValidationMessageTypeDef",
    "ConfigurationSettingsValidationMessagesTypeDef",
    "BuilderTypeDef",
    "PlatformSummaryTypeDef",
    "CreatePlatformVersionResultTypeDef",
    "CreateStorageLocationResultMessageTypeDef",
    "DeletePlatformVersionResultTypeDef",
    "ResourceQuotaTypeDef",
    "ResourceQuotasTypeDef",
    "DescribeAccountAttributesResultTypeDef",
    "LatencyTypeDef",
    "StatusCodesTypeDef",
    "ApplicationMetricsTypeDef",
    "InstanceHealthSummaryTypeDef",
    "DescribeEnvironmentHealthResultTypeDef",
    "ManagedActionHistoryItemTypeDef",
    "DescribeEnvironmentManagedActionHistoryResultTypeDef",
    "ManagedActionTypeDef",
    "DescribeEnvironmentManagedActionsResultTypeDef",
    "DeploymentTypeDef",
    "CPUUtilizationTypeDef",
    "SystemStatusTypeDef",
    "SingleInstanceHealthTypeDef",
    "DescribeInstancesHealthResultTypeDef",
    "CustomAmiTypeDef",
    "PlatformFrameworkTypeDef",
    "PlatformProgrammingLanguageTypeDef",
    "PlatformDescriptionTypeDef",
    "DescribePlatformVersionResultTypeDef",
    "EnvironmentLinkTypeDef",
    "ListenerTypeDef",
    "LoadBalancerDescriptionTypeDef",
    "EnvironmentResourcesDescriptionTypeDef",
    "EnvironmentTierTypeDef",
    "EnvironmentDescriptionTypeDef",
    "EnvironmentDescriptionsMessageTypeDef",
    "AutoScalingGroupTypeDef",
    "InstanceTypeDef",
    "LaunchConfigurationTypeDef",
    "LaunchTemplateTypeDef",
    "LoadBalancerTypeDef",
    "QueueTypeDef",
    "TriggerTypeDef",
    "EnvironmentResourceDescriptionTypeDef",
    "EnvironmentResourceDescriptionsMessageTypeDef",
    "EventDescriptionTypeDef",
    "EventDescriptionsMessageTypeDef",
    "SolutionStackDescriptionTypeDef",
    "ListAvailableSolutionStacksResultMessageTypeDef",
    "PlatformBranchSummaryTypeDef",
    "ListPlatformBranchesResultTypeDef",
    "ListPlatformVersionsResultTypeDef",
    "OptionSpecificationTypeDef",
    "PaginatorConfigTypeDef",
    "PlatformFilterTypeDef",
    "TagTypeDef",
    "ResourceTagsDescriptionMessageTypeDef",
    "EnvironmentInfoDescriptionTypeDef",
    "RetrieveEnvironmentInfoResultMessageTypeDef",
    "SearchFilterTypeDef",
    "SourceConfigurationTypeDef",
)

_RequiredMaxAgeRuleTypeDef = TypedDict("_RequiredMaxAgeRuleTypeDef", {"Enabled": bool})
_OptionalMaxAgeRuleTypeDef = TypedDict(
    "_OptionalMaxAgeRuleTypeDef", {"MaxAgeInDays": int, "DeleteSourceFromS3": bool}, total=False
)


class MaxAgeRuleTypeDef(_RequiredMaxAgeRuleTypeDef, _OptionalMaxAgeRuleTypeDef):
    pass


_RequiredMaxCountRuleTypeDef = TypedDict("_RequiredMaxCountRuleTypeDef", {"Enabled": bool})
_OptionalMaxCountRuleTypeDef = TypedDict(
    "_OptionalMaxCountRuleTypeDef", {"MaxCount": int, "DeleteSourceFromS3": bool}, total=False
)


class MaxCountRuleTypeDef(_RequiredMaxCountRuleTypeDef, _OptionalMaxCountRuleTypeDef):
    pass


ApplicationVersionLifecycleConfigTypeDef = TypedDict(
    "ApplicationVersionLifecycleConfigTypeDef",
    {"MaxCountRule": MaxCountRuleTypeDef, "MaxAgeRule": MaxAgeRuleTypeDef},
    total=False,
)

ApplicationResourceLifecycleConfigTypeDef = TypedDict(
    "ApplicationResourceLifecycleConfigTypeDef",
    {"ServiceRole": str, "VersionLifecycleConfig": ApplicationVersionLifecycleConfigTypeDef},
    total=False,
)

ApplicationDescriptionTypeDef = TypedDict(
    "ApplicationDescriptionTypeDef",
    {
        "ApplicationArn": str,
        "ApplicationName": str,
        "Description": str,
        "DateCreated": datetime,
        "DateUpdated": datetime,
        "Versions": List[str],
        "ConfigurationTemplates": List[str],
        "ResourceLifecycleConfig": ApplicationResourceLifecycleConfigTypeDef,
    },
    total=False,
)

ApplicationDescriptionMessageTypeDef = TypedDict(
    "ApplicationDescriptionMessageTypeDef",
    {"Application": ApplicationDescriptionTypeDef},
    total=False,
)

ApplicationDescriptionsMessageTypeDef = TypedDict(
    "ApplicationDescriptionsMessageTypeDef",
    {"Applications": List[ApplicationDescriptionTypeDef]},
    total=False,
)

ApplicationResourceLifecycleDescriptionMessageTypeDef = TypedDict(
    "ApplicationResourceLifecycleDescriptionMessageTypeDef",
    {"ApplicationName": str, "ResourceLifecycleConfig": ApplicationResourceLifecycleConfigTypeDef},
    total=False,
)

S3LocationTypeDef = TypedDict("S3LocationTypeDef", {"S3Bucket": str, "S3Key": str}, total=False)

SourceBuildInformationTypeDef = TypedDict(
    "SourceBuildInformationTypeDef",
    {
        "SourceType": Literal["Git", "Zip"],
        "SourceRepository": Literal["CodeCommit", "S3"],
        "SourceLocation": str,
    },
)

ApplicationVersionDescriptionTypeDef = TypedDict(
    "ApplicationVersionDescriptionTypeDef",
    {
        "ApplicationVersionArn": str,
        "ApplicationName": str,
        "Description": str,
        "VersionLabel": str,
        "SourceBuildInformation": SourceBuildInformationTypeDef,
        "BuildArn": str,
        "SourceBundle": S3LocationTypeDef,
        "DateCreated": datetime,
        "DateUpdated": datetime,
        "Status": Literal["Processed", "Unprocessed", "Failed", "Processing", "Building"],
    },
    total=False,
)

ApplicationVersionDescriptionMessageTypeDef = TypedDict(
    "ApplicationVersionDescriptionMessageTypeDef",
    {"ApplicationVersion": ApplicationVersionDescriptionTypeDef},
    total=False,
)

ApplicationVersionDescriptionsMessageTypeDef = TypedDict(
    "ApplicationVersionDescriptionsMessageTypeDef",
    {"ApplicationVersions": List[ApplicationVersionDescriptionTypeDef], "NextToken": str},
    total=False,
)

ApplyEnvironmentManagedActionResultTypeDef = TypedDict(
    "ApplyEnvironmentManagedActionResultTypeDef",
    {
        "ActionId": str,
        "ActionDescription": str,
        "ActionType": Literal["InstanceRefresh", "PlatformUpdate", "Unknown"],
        "Status": str,
    },
    total=False,
)

_RequiredBuildConfigurationTypeDef = TypedDict(
    "_RequiredBuildConfigurationTypeDef", {"CodeBuildServiceRole": str, "Image": str}
)
_OptionalBuildConfigurationTypeDef = TypedDict(
    "_OptionalBuildConfigurationTypeDef",
    {
        "ArtifactName": str,
        "ComputeType": Literal[
            "BUILD_GENERAL1_SMALL", "BUILD_GENERAL1_MEDIUM", "BUILD_GENERAL1_LARGE"
        ],
        "TimeoutInMinutes": int,
    },
    total=False,
)


class BuildConfigurationTypeDef(
    _RequiredBuildConfigurationTypeDef, _OptionalBuildConfigurationTypeDef
):
    pass


CheckDNSAvailabilityResultMessageTypeDef = TypedDict(
    "CheckDNSAvailabilityResultMessageTypeDef",
    {"Available": bool, "FullyQualifiedCNAME": str},
    total=False,
)

ConfigurationOptionSettingTypeDef = TypedDict(
    "ConfigurationOptionSettingTypeDef",
    {"ResourceName": str, "Namespace": str, "OptionName": str, "Value": str},
    total=False,
)

OptionRestrictionRegexTypeDef = TypedDict(
    "OptionRestrictionRegexTypeDef", {"Pattern": str, "Label": str}, total=False
)

ConfigurationOptionDescriptionTypeDef = TypedDict(
    "ConfigurationOptionDescriptionTypeDef",
    {
        "Namespace": str,
        "Name": str,
        "DefaultValue": str,
        "ChangeSeverity": str,
        "UserDefined": bool,
        "ValueType": Literal["Scalar", "List"],
        "ValueOptions": List[str],
        "MinValue": int,
        "MaxValue": int,
        "MaxLength": int,
        "Regex": OptionRestrictionRegexTypeDef,
    },
    total=False,
)

ConfigurationOptionsDescriptionTypeDef = TypedDict(
    "ConfigurationOptionsDescriptionTypeDef",
    {
        "SolutionStackName": str,
        "PlatformArn": str,
        "Options": List[ConfigurationOptionDescriptionTypeDef],
    },
    total=False,
)

ConfigurationSettingsDescriptionTypeDef = TypedDict(
    "ConfigurationSettingsDescriptionTypeDef",
    {
        "SolutionStackName": str,
        "PlatformArn": str,
        "ApplicationName": str,
        "TemplateName": str,
        "Description": str,
        "EnvironmentName": str,
        "DeploymentStatus": Literal["deployed", "pending", "failed"],
        "DateCreated": datetime,
        "DateUpdated": datetime,
        "OptionSettings": List[ConfigurationOptionSettingTypeDef],
    },
    total=False,
)

ConfigurationSettingsDescriptionsTypeDef = TypedDict(
    "ConfigurationSettingsDescriptionsTypeDef",
    {"ConfigurationSettings": List[ConfigurationSettingsDescriptionTypeDef]},
    total=False,
)

ValidationMessageTypeDef = TypedDict(
    "ValidationMessageTypeDef",
    {"Message": str, "Severity": Literal["error", "warning"], "Namespace": str, "OptionName": str},
    total=False,
)

ConfigurationSettingsValidationMessagesTypeDef = TypedDict(
    "ConfigurationSettingsValidationMessagesTypeDef",
    {"Messages": List[ValidationMessageTypeDef]},
    total=False,
)

BuilderTypeDef = TypedDict("BuilderTypeDef", {"ARN": str}, total=False)

PlatformSummaryTypeDef = TypedDict(
    "PlatformSummaryTypeDef",
    {
        "PlatformArn": str,
        "PlatformOwner": str,
        "PlatformStatus": Literal["Creating", "Failed", "Ready", "Deleting", "Deleted"],
        "PlatformCategory": str,
        "OperatingSystemName": str,
        "OperatingSystemVersion": str,
        "SupportedTierList": List[str],
        "SupportedAddonList": List[str],
        "PlatformLifecycleState": str,
        "PlatformVersion": str,
        "PlatformBranchName": str,
        "PlatformBranchLifecycleState": str,
    },
    total=False,
)

CreatePlatformVersionResultTypeDef = TypedDict(
    "CreatePlatformVersionResultTypeDef",
    {"PlatformSummary": PlatformSummaryTypeDef, "Builder": BuilderTypeDef},
    total=False,
)

CreateStorageLocationResultMessageTypeDef = TypedDict(
    "CreateStorageLocationResultMessageTypeDef", {"S3Bucket": str}, total=False
)

DeletePlatformVersionResultTypeDef = TypedDict(
    "DeletePlatformVersionResultTypeDef", {"PlatformSummary": PlatformSummaryTypeDef}, total=False
)

ResourceQuotaTypeDef = TypedDict("ResourceQuotaTypeDef", {"Maximum": int}, total=False)

ResourceQuotasTypeDef = TypedDict(
    "ResourceQuotasTypeDef",
    {
        "ApplicationQuota": ResourceQuotaTypeDef,
        "ApplicationVersionQuota": ResourceQuotaTypeDef,
        "EnvironmentQuota": ResourceQuotaTypeDef,
        "ConfigurationTemplateQuota": ResourceQuotaTypeDef,
        "CustomPlatformQuota": ResourceQuotaTypeDef,
    },
    total=False,
)

DescribeAccountAttributesResultTypeDef = TypedDict(
    "DescribeAccountAttributesResultTypeDef", {"ResourceQuotas": ResourceQuotasTypeDef}, total=False
)

LatencyTypeDef = TypedDict(
    "LatencyTypeDef",
    {
        "P999": float,
        "P99": float,
        "P95": float,
        "P90": float,
        "P85": float,
        "P75": float,
        "P50": float,
        "P10": float,
    },
    total=False,
)

StatusCodesTypeDef = TypedDict(
    "StatusCodesTypeDef",
    {"Status2xx": int, "Status3xx": int, "Status4xx": int, "Status5xx": int},
    total=False,
)

ApplicationMetricsTypeDef = TypedDict(
    "ApplicationMetricsTypeDef",
    {
        "Duration": int,
        "RequestCount": int,
        "StatusCodes": StatusCodesTypeDef,
        "Latency": LatencyTypeDef,
    },
    total=False,
)

InstanceHealthSummaryTypeDef = TypedDict(
    "InstanceHealthSummaryTypeDef",
    {
        "NoData": int,
        "Unknown": int,
        "Pending": int,
        "Ok": int,
        "Info": int,
        "Warning": int,
        "Degraded": int,
        "Severe": int,
    },
    total=False,
)

DescribeEnvironmentHealthResultTypeDef = TypedDict(
    "DescribeEnvironmentHealthResultTypeDef",
    {
        "EnvironmentName": str,
        "HealthStatus": str,
        "Status": Literal["Green", "Yellow", "Red", "Grey"],
        "Color": str,
        "Causes": List[str],
        "ApplicationMetrics": ApplicationMetricsTypeDef,
        "InstancesHealth": InstanceHealthSummaryTypeDef,
        "RefreshedAt": datetime,
    },
    total=False,
)

ManagedActionHistoryItemTypeDef = TypedDict(
    "ManagedActionHistoryItemTypeDef",
    {
        "ActionId": str,
        "ActionType": Literal["InstanceRefresh", "PlatformUpdate", "Unknown"],
        "ActionDescription": str,
        "FailureType": Literal[
            "UpdateCancelled",
            "CancellationFailed",
            "RollbackFailed",
            "RollbackSuccessful",
            "InternalFailure",
            "InvalidEnvironmentState",
            "PermissionsError",
        ],
        "Status": Literal["Completed", "Failed", "Unknown"],
        "FailureDescription": str,
        "ExecutedTime": datetime,
        "FinishedTime": datetime,
    },
    total=False,
)

DescribeEnvironmentManagedActionHistoryResultTypeDef = TypedDict(
    "DescribeEnvironmentManagedActionHistoryResultTypeDef",
    {"ManagedActionHistoryItems": List[ManagedActionHistoryItemTypeDef], "NextToken": str},
    total=False,
)

ManagedActionTypeDef = TypedDict(
    "ManagedActionTypeDef",
    {
        "ActionId": str,
        "ActionDescription": str,
        "ActionType": Literal["InstanceRefresh", "PlatformUpdate", "Unknown"],
        "Status": Literal["Scheduled", "Pending", "Running", "Unknown"],
        "WindowStartTime": datetime,
    },
    total=False,
)

DescribeEnvironmentManagedActionsResultTypeDef = TypedDict(
    "DescribeEnvironmentManagedActionsResultTypeDef",
    {"ManagedActions": List[ManagedActionTypeDef]},
    total=False,
)

DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {"VersionLabel": str, "DeploymentId": int, "Status": str, "DeploymentTime": datetime},
    total=False,
)

CPUUtilizationTypeDef = TypedDict(
    "CPUUtilizationTypeDef",
    {
        "User": float,
        "Nice": float,
        "System": float,
        "Idle": float,
        "IOWait": float,
        "IRQ": float,
        "SoftIRQ": float,
        "Privileged": float,
    },
    total=False,
)

SystemStatusTypeDef = TypedDict(
    "SystemStatusTypeDef",
    {"CPUUtilization": CPUUtilizationTypeDef, "LoadAverage": List[float]},
    total=False,
)

SingleInstanceHealthTypeDef = TypedDict(
    "SingleInstanceHealthTypeDef",
    {
        "InstanceId": str,
        "HealthStatus": str,
        "Color": str,
        "Causes": List[str],
        "LaunchedAt": datetime,
        "ApplicationMetrics": ApplicationMetricsTypeDef,
        "System": SystemStatusTypeDef,
        "Deployment": DeploymentTypeDef,
        "AvailabilityZone": str,
        "InstanceType": str,
    },
    total=False,
)

DescribeInstancesHealthResultTypeDef = TypedDict(
    "DescribeInstancesHealthResultTypeDef",
    {
        "InstanceHealthList": List[SingleInstanceHealthTypeDef],
        "RefreshedAt": datetime,
        "NextToken": str,
    },
    total=False,
)

CustomAmiTypeDef = TypedDict(
    "CustomAmiTypeDef", {"VirtualizationType": str, "ImageId": str}, total=False
)

PlatformFrameworkTypeDef = TypedDict(
    "PlatformFrameworkTypeDef", {"Name": str, "Version": str}, total=False
)

PlatformProgrammingLanguageTypeDef = TypedDict(
    "PlatformProgrammingLanguageTypeDef", {"Name": str, "Version": str}, total=False
)

PlatformDescriptionTypeDef = TypedDict(
    "PlatformDescriptionTypeDef",
    {
        "PlatformArn": str,
        "PlatformOwner": str,
        "PlatformName": str,
        "PlatformVersion": str,
        "SolutionStackName": str,
        "PlatformStatus": Literal["Creating", "Failed", "Ready", "Deleting", "Deleted"],
        "DateCreated": datetime,
        "DateUpdated": datetime,
        "PlatformCategory": str,
        "Description": str,
        "Maintainer": str,
        "OperatingSystemName": str,
        "OperatingSystemVersion": str,
        "ProgrammingLanguages": List[PlatformProgrammingLanguageTypeDef],
        "Frameworks": List[PlatformFrameworkTypeDef],
        "CustomAmiList": List[CustomAmiTypeDef],
        "SupportedTierList": List[str],
        "SupportedAddonList": List[str],
        "PlatformLifecycleState": str,
        "PlatformBranchName": str,
        "PlatformBranchLifecycleState": str,
    },
    total=False,
)

DescribePlatformVersionResultTypeDef = TypedDict(
    "DescribePlatformVersionResultTypeDef",
    {"PlatformDescription": PlatformDescriptionTypeDef},
    total=False,
)

EnvironmentLinkTypeDef = TypedDict(
    "EnvironmentLinkTypeDef", {"LinkName": str, "EnvironmentName": str}, total=False
)

ListenerTypeDef = TypedDict("ListenerTypeDef", {"Protocol": str, "Port": int}, total=False)

LoadBalancerDescriptionTypeDef = TypedDict(
    "LoadBalancerDescriptionTypeDef",
    {"LoadBalancerName": str, "Domain": str, "Listeners": List[ListenerTypeDef]},
    total=False,
)

EnvironmentResourcesDescriptionTypeDef = TypedDict(
    "EnvironmentResourcesDescriptionTypeDef",
    {"LoadBalancer": LoadBalancerDescriptionTypeDef},
    total=False,
)

EnvironmentTierTypeDef = TypedDict(
    "EnvironmentTierTypeDef", {"Name": str, "Type": str, "Version": str}, total=False
)

EnvironmentDescriptionTypeDef = TypedDict(
    "EnvironmentDescriptionTypeDef",
    {
        "EnvironmentName": str,
        "EnvironmentId": str,
        "ApplicationName": str,
        "VersionLabel": str,
        "SolutionStackName": str,
        "PlatformArn": str,
        "TemplateName": str,
        "Description": str,
        "EndpointURL": str,
        "CNAME": str,
        "DateCreated": datetime,
        "DateUpdated": datetime,
        "Status": Literal["Launching", "Updating", "Ready", "Terminating", "Terminated"],
        "AbortableOperationInProgress": bool,
        "Health": Literal["Green", "Yellow", "Red", "Grey"],
        "HealthStatus": Literal[
            "NoData",
            "Unknown",
            "Pending",
            "Ok",
            "Info",
            "Warning",
            "Degraded",
            "Severe",
            "Suspended",
        ],
        "Resources": EnvironmentResourcesDescriptionTypeDef,
        "Tier": EnvironmentTierTypeDef,
        "EnvironmentLinks": List[EnvironmentLinkTypeDef],
        "EnvironmentArn": str,
    },
    total=False,
)

EnvironmentDescriptionsMessageTypeDef = TypedDict(
    "EnvironmentDescriptionsMessageTypeDef",
    {"Environments": List[EnvironmentDescriptionTypeDef], "NextToken": str},
    total=False,
)

AutoScalingGroupTypeDef = TypedDict("AutoScalingGroupTypeDef", {"Name": str}, total=False)

InstanceTypeDef = TypedDict("InstanceTypeDef", {"Id": str}, total=False)

LaunchConfigurationTypeDef = TypedDict("LaunchConfigurationTypeDef", {"Name": str}, total=False)

LaunchTemplateTypeDef = TypedDict("LaunchTemplateTypeDef", {"Id": str}, total=False)

LoadBalancerTypeDef = TypedDict("LoadBalancerTypeDef", {"Name": str}, total=False)

QueueTypeDef = TypedDict("QueueTypeDef", {"Name": str, "URL": str}, total=False)

TriggerTypeDef = TypedDict("TriggerTypeDef", {"Name": str}, total=False)

EnvironmentResourceDescriptionTypeDef = TypedDict(
    "EnvironmentResourceDescriptionTypeDef",
    {
        "EnvironmentName": str,
        "AutoScalingGroups": List[AutoScalingGroupTypeDef],
        "Instances": List[InstanceTypeDef],
        "LaunchConfigurations": List[LaunchConfigurationTypeDef],
        "LaunchTemplates": List[LaunchTemplateTypeDef],
        "LoadBalancers": List[LoadBalancerTypeDef],
        "Triggers": List[TriggerTypeDef],
        "Queues": List[QueueTypeDef],
    },
    total=False,
)

EnvironmentResourceDescriptionsMessageTypeDef = TypedDict(
    "EnvironmentResourceDescriptionsMessageTypeDef",
    {"EnvironmentResources": EnvironmentResourceDescriptionTypeDef},
    total=False,
)

EventDescriptionTypeDef = TypedDict(
    "EventDescriptionTypeDef",
    {
        "EventDate": datetime,
        "Message": str,
        "ApplicationName": str,
        "VersionLabel": str,
        "TemplateName": str,
        "EnvironmentName": str,
        "PlatformArn": str,
        "RequestId": str,
        "Severity": Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"],
    },
    total=False,
)

EventDescriptionsMessageTypeDef = TypedDict(
    "EventDescriptionsMessageTypeDef",
    {"Events": List[EventDescriptionTypeDef], "NextToken": str},
    total=False,
)

SolutionStackDescriptionTypeDef = TypedDict(
    "SolutionStackDescriptionTypeDef",
    {"SolutionStackName": str, "PermittedFileTypes": List[str]},
    total=False,
)

ListAvailableSolutionStacksResultMessageTypeDef = TypedDict(
    "ListAvailableSolutionStacksResultMessageTypeDef",
    {"SolutionStacks": List[str], "SolutionStackDetails": List[SolutionStackDescriptionTypeDef]},
    total=False,
)

PlatformBranchSummaryTypeDef = TypedDict(
    "PlatformBranchSummaryTypeDef",
    {
        "PlatformName": str,
        "BranchName": str,
        "LifecycleState": str,
        "BranchOrder": int,
        "SupportedTierList": List[str],
    },
    total=False,
)

ListPlatformBranchesResultTypeDef = TypedDict(
    "ListPlatformBranchesResultTypeDef",
    {"PlatformBranchSummaryList": List[PlatformBranchSummaryTypeDef], "NextToken": str},
    total=False,
)

ListPlatformVersionsResultTypeDef = TypedDict(
    "ListPlatformVersionsResultTypeDef",
    {"PlatformSummaryList": List[PlatformSummaryTypeDef], "NextToken": str},
    total=False,
)

OptionSpecificationTypeDef = TypedDict(
    "OptionSpecificationTypeDef",
    {"ResourceName": str, "Namespace": str, "OptionName": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PlatformFilterTypeDef = TypedDict(
    "PlatformFilterTypeDef", {"Type": str, "Operator": str, "Values": List[str]}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str}, total=False)

ResourceTagsDescriptionMessageTypeDef = TypedDict(
    "ResourceTagsDescriptionMessageTypeDef",
    {"ResourceArn": str, "ResourceTags": List[TagTypeDef]},
    total=False,
)

EnvironmentInfoDescriptionTypeDef = TypedDict(
    "EnvironmentInfoDescriptionTypeDef",
    {
        "InfoType": Literal["tail", "bundle"],
        "Ec2InstanceId": str,
        "SampleTimestamp": datetime,
        "Message": str,
    },
    total=False,
)

RetrieveEnvironmentInfoResultMessageTypeDef = TypedDict(
    "RetrieveEnvironmentInfoResultMessageTypeDef",
    {"EnvironmentInfo": List[EnvironmentInfoDescriptionTypeDef]},
    total=False,
)

SearchFilterTypeDef = TypedDict(
    "SearchFilterTypeDef", {"Attribute": str, "Operator": str, "Values": List[str]}, total=False
)

SourceConfigurationTypeDef = TypedDict(
    "SourceConfigurationTypeDef", {"ApplicationName": str, "TemplateName": str}, total=False
)
