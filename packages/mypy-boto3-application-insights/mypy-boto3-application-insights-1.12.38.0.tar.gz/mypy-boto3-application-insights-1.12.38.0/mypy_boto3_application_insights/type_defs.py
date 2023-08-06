"""
Main interface for application-insights service type definitions.

Usage::

    from mypy_boto3.application_insights.type_defs import ApplicationInfoTypeDef

    data: ApplicationInfoTypeDef = {...}
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
    "ApplicationInfoTypeDef",
    "CreateApplicationResponseTypeDef",
    "LogPatternTypeDef",
    "CreateLogPatternResponseTypeDef",
    "DescribeApplicationResponseTypeDef",
    "DescribeComponentConfigurationRecommendationResponseTypeDef",
    "DescribeComponentConfigurationResponseTypeDef",
    "ApplicationComponentTypeDef",
    "DescribeComponentResponseTypeDef",
    "DescribeLogPatternResponseTypeDef",
    "ObservationTypeDef",
    "DescribeObservationResponseTypeDef",
    "RelatedObservationsTypeDef",
    "DescribeProblemObservationsResponseTypeDef",
    "ProblemTypeDef",
    "DescribeProblemResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListComponentsResponseTypeDef",
    "ConfigurationEventTypeDef",
    "ListConfigurationHistoryResponseTypeDef",
    "ListLogPatternSetsResponseTypeDef",
    "ListLogPatternsResponseTypeDef",
    "ListProblemsResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateApplicationResponseTypeDef",
    "UpdateLogPatternResponseTypeDef",
)

ApplicationInfoTypeDef = TypedDict(
    "ApplicationInfoTypeDef",
    {
        "ResourceGroupName": str,
        "LifeCycle": str,
        "OpsItemSNSTopicArn": str,
        "OpsCenterEnabled": bool,
        "CWEMonitorEnabled": bool,
        "Remarks": str,
    },
    total=False,
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef", {"ApplicationInfo": ApplicationInfoTypeDef}, total=False
)

LogPatternTypeDef = TypedDict(
    "LogPatternTypeDef",
    {"PatternSetName": str, "PatternName": str, "Pattern": str, "Rank": int},
    total=False,
)

CreateLogPatternResponseTypeDef = TypedDict(
    "CreateLogPatternResponseTypeDef",
    {"LogPattern": LogPatternTypeDef, "ResourceGroupName": str},
    total=False,
)

DescribeApplicationResponseTypeDef = TypedDict(
    "DescribeApplicationResponseTypeDef", {"ApplicationInfo": ApplicationInfoTypeDef}, total=False
)

DescribeComponentConfigurationRecommendationResponseTypeDef = TypedDict(
    "DescribeComponentConfigurationRecommendationResponseTypeDef",
    {"ComponentConfiguration": str},
    total=False,
)

DescribeComponentConfigurationResponseTypeDef = TypedDict(
    "DescribeComponentConfigurationResponseTypeDef",
    {
        "Monitor": bool,
        "Tier": Literal["DEFAULT", "DOT_NET_CORE", "DOT_NET_WORKER", "DOT_NET_WEB", "SQL_SERVER"],
        "ComponentConfiguration": str,
    },
    total=False,
)

ApplicationComponentTypeDef = TypedDict(
    "ApplicationComponentTypeDef",
    {
        "ComponentName": str,
        "ResourceType": str,
        "Tier": Literal["DEFAULT", "DOT_NET_CORE", "DOT_NET_WORKER", "DOT_NET_WEB", "SQL_SERVER"],
        "Monitor": bool,
    },
    total=False,
)

DescribeComponentResponseTypeDef = TypedDict(
    "DescribeComponentResponseTypeDef",
    {"ApplicationComponent": ApplicationComponentTypeDef, "ResourceList": List[str]},
    total=False,
)

DescribeLogPatternResponseTypeDef = TypedDict(
    "DescribeLogPatternResponseTypeDef",
    {"ResourceGroupName": str, "LogPattern": LogPatternTypeDef},
    total=False,
)

ObservationTypeDef = TypedDict(
    "ObservationTypeDef",
    {
        "Id": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "SourceType": str,
        "SourceARN": str,
        "LogGroup": str,
        "LineTime": datetime,
        "LogText": str,
        "LogFilter": Literal["ERROR", "WARN", "INFO"],
        "MetricNamespace": str,
        "MetricName": str,
        "Unit": str,
        "Value": float,
        "CloudWatchEventId": str,
        "CloudWatchEventSource": Literal["EC2", "CODE_DEPLOY", "HEALTH"],
        "CloudWatchEventDetailType": str,
        "HealthEventArn": str,
        "HealthService": str,
        "HealthEventTypeCode": str,
        "HealthEventTypeCategory": str,
        "HealthEventDescription": str,
        "CodeDeployDeploymentId": str,
        "CodeDeployDeploymentGroup": str,
        "CodeDeployState": str,
        "CodeDeployApplication": str,
        "CodeDeployInstanceGroupId": str,
        "Ec2State": str,
        "XRayFaultPercent": int,
        "XRayThrottlePercent": int,
        "XRayErrorPercent": int,
        "XRayRequestCount": int,
        "XRayRequestAverageLatency": int,
        "XRayNodeName": str,
        "XRayNodeType": str,
    },
    total=False,
)

DescribeObservationResponseTypeDef = TypedDict(
    "DescribeObservationResponseTypeDef", {"Observation": ObservationTypeDef}, total=False
)

RelatedObservationsTypeDef = TypedDict(
    "RelatedObservationsTypeDef", {"ObservationList": List[ObservationTypeDef]}, total=False
)

DescribeProblemObservationsResponseTypeDef = TypedDict(
    "DescribeProblemObservationsResponseTypeDef",
    {"RelatedObservations": RelatedObservationsTypeDef},
    total=False,
)

ProblemTypeDef = TypedDict(
    "ProblemTypeDef",
    {
        "Id": str,
        "Title": str,
        "Insights": str,
        "Status": Literal["IGNORE", "RESOLVED", "PENDING"],
        "AffectedResource": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "SeverityLevel": Literal["Low", "Medium", "High"],
        "ResourceGroupName": str,
        "Feedback": Dict[
            Literal["INSIGHTS_FEEDBACK"], Literal["NOT_SPECIFIED", "USEFUL", "NOT_USEFUL"]
        ],
    },
    total=False,
)

DescribeProblemResponseTypeDef = TypedDict(
    "DescribeProblemResponseTypeDef", {"Problem": ProblemTypeDef}, total=False
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {"ApplicationInfoList": List[ApplicationInfoTypeDef], "NextToken": str},
    total=False,
)

ListComponentsResponseTypeDef = TypedDict(
    "ListComponentsResponseTypeDef",
    {"ApplicationComponentList": List[ApplicationComponentTypeDef], "NextToken": str},
    total=False,
)

ConfigurationEventTypeDef = TypedDict(
    "ConfigurationEventTypeDef",
    {
        "MonitoredResourceARN": str,
        "EventStatus": Literal["INFO", "WARN", "ERROR"],
        "EventResourceType": Literal["CLOUDWATCH_ALARM", "CLOUDFORMATION", "SSM_ASSOCIATION"],
        "EventTime": datetime,
        "EventDetail": str,
        "EventResourceName": str,
    },
    total=False,
)

ListConfigurationHistoryResponseTypeDef = TypedDict(
    "ListConfigurationHistoryResponseTypeDef",
    {"EventList": List[ConfigurationEventTypeDef], "NextToken": str},
    total=False,
)

ListLogPatternSetsResponseTypeDef = TypedDict(
    "ListLogPatternSetsResponseTypeDef",
    {"ResourceGroupName": str, "LogPatternSets": List[str], "NextToken": str},
    total=False,
)

ListLogPatternsResponseTypeDef = TypedDict(
    "ListLogPatternsResponseTypeDef",
    {"ResourceGroupName": str, "LogPatterns": List[LogPatternTypeDef], "NextToken": str},
    total=False,
)

ListProblemsResponseTypeDef = TypedDict(
    "ListProblemsResponseTypeDef",
    {"ProblemList": List[ProblemTypeDef], "NextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef]}, total=False
)

UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef", {"ApplicationInfo": ApplicationInfoTypeDef}, total=False
)

UpdateLogPatternResponseTypeDef = TypedDict(
    "UpdateLogPatternResponseTypeDef",
    {"ResourceGroupName": str, "LogPattern": LogPatternTypeDef},
    total=False,
)
