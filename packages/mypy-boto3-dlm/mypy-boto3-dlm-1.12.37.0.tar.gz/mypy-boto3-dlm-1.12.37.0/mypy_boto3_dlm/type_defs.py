"""
Main interface for dlm service type definitions.

Usage::

    from mypy_boto3.dlm.type_defs import CreateLifecyclePolicyResponseTypeDef

    data: CreateLifecyclePolicyResponseTypeDef = {...}
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
    "CreateLifecyclePolicyResponseTypeDef",
    "LifecyclePolicySummaryTypeDef",
    "GetLifecyclePoliciesResponseTypeDef",
    "ParametersTypeDef",
    "CreateRuleTypeDef",
    "CrossRegionCopyRetainRuleTypeDef",
    "CrossRegionCopyRuleTypeDef",
    "FastRestoreRuleTypeDef",
    "RetainRuleTypeDef",
    "TagTypeDef",
    "ScheduleTypeDef",
    "PolicyDetailsTypeDef",
    "LifecyclePolicyTypeDef",
    "GetLifecyclePolicyResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
)

CreateLifecyclePolicyResponseTypeDef = TypedDict(
    "CreateLifecyclePolicyResponseTypeDef", {"PolicyId": str}, total=False
)

LifecyclePolicySummaryTypeDef = TypedDict(
    "LifecyclePolicySummaryTypeDef",
    {
        "PolicyId": str,
        "Description": str,
        "State": Literal["ENABLED", "DISABLED", "ERROR"],
        "Tags": Dict[str, str],
    },
    total=False,
)

GetLifecyclePoliciesResponseTypeDef = TypedDict(
    "GetLifecyclePoliciesResponseTypeDef",
    {"Policies": List[LifecyclePolicySummaryTypeDef]},
    total=False,
)

ParametersTypeDef = TypedDict("ParametersTypeDef", {"ExcludeBootVolume": bool}, total=False)

_RequiredCreateRuleTypeDef = TypedDict(
    "_RequiredCreateRuleTypeDef", {"Interval": int, "IntervalUnit": Literal["HOURS"]}
)
_OptionalCreateRuleTypeDef = TypedDict(
    "_OptionalCreateRuleTypeDef", {"Times": List[str]}, total=False
)


class CreateRuleTypeDef(_RequiredCreateRuleTypeDef, _OptionalCreateRuleTypeDef):
    pass


CrossRegionCopyRetainRuleTypeDef = TypedDict(
    "CrossRegionCopyRetainRuleTypeDef",
    {"Interval": int, "IntervalUnit": Literal["DAYS", "WEEKS", "MONTHS", "YEARS"]},
    total=False,
)

_RequiredCrossRegionCopyRuleTypeDef = TypedDict(
    "_RequiredCrossRegionCopyRuleTypeDef", {"TargetRegion": str, "Encrypted": bool}
)
_OptionalCrossRegionCopyRuleTypeDef = TypedDict(
    "_OptionalCrossRegionCopyRuleTypeDef",
    {"CmkArn": str, "CopyTags": bool, "RetainRule": CrossRegionCopyRetainRuleTypeDef},
    total=False,
)


class CrossRegionCopyRuleTypeDef(
    _RequiredCrossRegionCopyRuleTypeDef, _OptionalCrossRegionCopyRuleTypeDef
):
    pass


_RequiredFastRestoreRuleTypeDef = TypedDict(
    "_RequiredFastRestoreRuleTypeDef", {"AvailabilityZones": List[str]}
)
_OptionalFastRestoreRuleTypeDef = TypedDict(
    "_OptionalFastRestoreRuleTypeDef",
    {"Count": int, "Interval": int, "IntervalUnit": Literal["DAYS", "WEEKS", "MONTHS", "YEARS"]},
    total=False,
)


class FastRestoreRuleTypeDef(_RequiredFastRestoreRuleTypeDef, _OptionalFastRestoreRuleTypeDef):
    pass


RetainRuleTypeDef = TypedDict(
    "RetainRuleTypeDef",
    {"Count": int, "Interval": int, "IntervalUnit": Literal["DAYS", "WEEKS", "MONTHS", "YEARS"]},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ScheduleTypeDef = TypedDict(
    "ScheduleTypeDef",
    {
        "Name": str,
        "CopyTags": bool,
        "TagsToAdd": List[TagTypeDef],
        "VariableTags": List[TagTypeDef],
        "CreateRule": CreateRuleTypeDef,
        "RetainRule": RetainRuleTypeDef,
        "FastRestoreRule": FastRestoreRuleTypeDef,
        "CrossRegionCopyRules": List[CrossRegionCopyRuleTypeDef],
    },
    total=False,
)

PolicyDetailsTypeDef = TypedDict(
    "PolicyDetailsTypeDef",
    {
        "PolicyType": Literal["EBS_SNAPSHOT_MANAGEMENT"],
        "ResourceTypes": List[Literal["VOLUME", "INSTANCE"]],
        "TargetTags": List[TagTypeDef],
        "Schedules": List[ScheduleTypeDef],
        "Parameters": ParametersTypeDef,
    },
    total=False,
)

LifecyclePolicyTypeDef = TypedDict(
    "LifecyclePolicyTypeDef",
    {
        "PolicyId": str,
        "Description": str,
        "State": Literal["ENABLED", "DISABLED", "ERROR"],
        "StatusMessage": str,
        "ExecutionRoleArn": str,
        "DateCreated": datetime,
        "DateModified": datetime,
        "PolicyDetails": PolicyDetailsTypeDef,
        "Tags": Dict[str, str],
        "PolicyArn": str,
    },
    total=False,
)

GetLifecyclePolicyResponseTypeDef = TypedDict(
    "GetLifecyclePolicyResponseTypeDef", {"Policy": LifecyclePolicyTypeDef}, total=False
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)
