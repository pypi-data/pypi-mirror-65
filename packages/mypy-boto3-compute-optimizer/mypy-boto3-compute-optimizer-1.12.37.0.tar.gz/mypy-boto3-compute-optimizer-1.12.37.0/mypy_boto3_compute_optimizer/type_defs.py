"""
Main interface for compute-optimizer service type definitions.

Usage::

    from mypy_boto3.compute_optimizer.type_defs import FilterTypeDef

    data: FilterTypeDef = {...}
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
    "FilterTypeDef",
    "AutoScalingGroupConfigurationTypeDef",
    "UtilizationMetricTypeDef",
    "AutoScalingGroupRecommendationOptionTypeDef",
    "AutoScalingGroupRecommendationTypeDef",
    "GetRecommendationErrorTypeDef",
    "GetAutoScalingGroupRecommendationsResponseTypeDef",
    "InstanceRecommendationOptionTypeDef",
    "RecommendationSourceTypeDef",
    "InstanceRecommendationTypeDef",
    "GetEC2InstanceRecommendationsResponseTypeDef",
    "ProjectedMetricTypeDef",
    "RecommendedOptionProjectedMetricTypeDef",
    "GetEC2RecommendationProjectedMetricsResponseTypeDef",
    "GetEnrollmentStatusResponseTypeDef",
    "SummaryTypeDef",
    "RecommendationSummaryTypeDef",
    "GetRecommendationSummariesResponseTypeDef",
    "UpdateEnrollmentStatusResponseTypeDef",
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {"name": Literal["Finding", "RecommendationSourceType"], "values": List[str]},
    total=False,
)

AutoScalingGroupConfigurationTypeDef = TypedDict(
    "AutoScalingGroupConfigurationTypeDef",
    {"desiredCapacity": int, "minSize": int, "maxSize": int, "instanceType": str},
    total=False,
)

UtilizationMetricTypeDef = TypedDict(
    "UtilizationMetricTypeDef",
    {"name": Literal["Cpu", "Memory"], "statistic": Literal["Maximum", "Average"], "value": float},
    total=False,
)

AutoScalingGroupRecommendationOptionTypeDef = TypedDict(
    "AutoScalingGroupRecommendationOptionTypeDef",
    {
        "configuration": AutoScalingGroupConfigurationTypeDef,
        "projectedUtilizationMetrics": List[UtilizationMetricTypeDef],
        "performanceRisk": float,
        "rank": int,
    },
    total=False,
)

AutoScalingGroupRecommendationTypeDef = TypedDict(
    "AutoScalingGroupRecommendationTypeDef",
    {
        "accountId": str,
        "autoScalingGroupArn": str,
        "autoScalingGroupName": str,
        "finding": Literal["Underprovisioned", "Overprovisioned", "Optimized", "NotOptimized"],
        "utilizationMetrics": List[UtilizationMetricTypeDef],
        "lookBackPeriodInDays": float,
        "currentConfiguration": AutoScalingGroupConfigurationTypeDef,
        "recommendationOptions": List[AutoScalingGroupRecommendationOptionTypeDef],
        "lastRefreshTimestamp": datetime,
    },
    total=False,
)

GetRecommendationErrorTypeDef = TypedDict(
    "GetRecommendationErrorTypeDef", {"identifier": str, "code": str, "message": str}, total=False
)

GetAutoScalingGroupRecommendationsResponseTypeDef = TypedDict(
    "GetAutoScalingGroupRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "autoScalingGroupRecommendations": List[AutoScalingGroupRecommendationTypeDef],
        "errors": List[GetRecommendationErrorTypeDef],
    },
    total=False,
)

InstanceRecommendationOptionTypeDef = TypedDict(
    "InstanceRecommendationOptionTypeDef",
    {
        "instanceType": str,
        "projectedUtilizationMetrics": List[UtilizationMetricTypeDef],
        "performanceRisk": float,
        "rank": int,
    },
    total=False,
)

RecommendationSourceTypeDef = TypedDict(
    "RecommendationSourceTypeDef",
    {
        "recommendationSourceArn": str,
        "recommendationSourceType": Literal["Ec2Instance", "AutoScalingGroup"],
    },
    total=False,
)

InstanceRecommendationTypeDef = TypedDict(
    "InstanceRecommendationTypeDef",
    {
        "instanceArn": str,
        "accountId": str,
        "instanceName": str,
        "currentInstanceType": str,
        "finding": Literal["Underprovisioned", "Overprovisioned", "Optimized", "NotOptimized"],
        "utilizationMetrics": List[UtilizationMetricTypeDef],
        "lookBackPeriodInDays": float,
        "recommendationOptions": List[InstanceRecommendationOptionTypeDef],
        "recommendationSources": List[RecommendationSourceTypeDef],
        "lastRefreshTimestamp": datetime,
    },
    total=False,
)

GetEC2InstanceRecommendationsResponseTypeDef = TypedDict(
    "GetEC2InstanceRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "instanceRecommendations": List[InstanceRecommendationTypeDef],
        "errors": List[GetRecommendationErrorTypeDef],
    },
    total=False,
)

ProjectedMetricTypeDef = TypedDict(
    "ProjectedMetricTypeDef",
    {"name": Literal["Cpu", "Memory"], "timestamps": List[datetime], "values": List[float]},
    total=False,
)

RecommendedOptionProjectedMetricTypeDef = TypedDict(
    "RecommendedOptionProjectedMetricTypeDef",
    {"recommendedInstanceType": str, "rank": int, "projectedMetrics": List[ProjectedMetricTypeDef]},
    total=False,
)

GetEC2RecommendationProjectedMetricsResponseTypeDef = TypedDict(
    "GetEC2RecommendationProjectedMetricsResponseTypeDef",
    {"recommendedOptionProjectedMetrics": List[RecommendedOptionProjectedMetricTypeDef]},
    total=False,
)

GetEnrollmentStatusResponseTypeDef = TypedDict(
    "GetEnrollmentStatusResponseTypeDef",
    {
        "status": Literal["Active", "Inactive", "Pending", "Failed"],
        "statusReason": str,
        "memberAccountsEnrolled": bool,
    },
    total=False,
)

SummaryTypeDef = TypedDict(
    "SummaryTypeDef",
    {
        "name": Literal["Underprovisioned", "Overprovisioned", "Optimized", "NotOptimized"],
        "value": float,
    },
    total=False,
)

RecommendationSummaryTypeDef = TypedDict(
    "RecommendationSummaryTypeDef",
    {
        "summaries": List[SummaryTypeDef],
        "recommendationResourceType": Literal["Ec2Instance", "AutoScalingGroup"],
        "accountId": str,
    },
    total=False,
)

GetRecommendationSummariesResponseTypeDef = TypedDict(
    "GetRecommendationSummariesResponseTypeDef",
    {"nextToken": str, "recommendationSummaries": List[RecommendationSummaryTypeDef]},
    total=False,
)

UpdateEnrollmentStatusResponseTypeDef = TypedDict(
    "UpdateEnrollmentStatusResponseTypeDef",
    {"status": Literal["Active", "Inactive", "Pending", "Failed"], "statusReason": str},
    total=False,
)
