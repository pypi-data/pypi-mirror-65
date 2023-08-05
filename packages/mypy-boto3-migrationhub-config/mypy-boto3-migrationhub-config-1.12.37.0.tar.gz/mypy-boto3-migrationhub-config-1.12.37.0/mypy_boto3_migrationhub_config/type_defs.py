"""
Main interface for migrationhub-config service type definitions.

Usage::

    from mypy_boto3.migrationhub_config.type_defs import TargetTypeDef

    data: TargetTypeDef = {...}
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
    "TargetTypeDef",
    "HomeRegionControlTypeDef",
    "CreateHomeRegionControlResultTypeDef",
    "DescribeHomeRegionControlsResultTypeDef",
    "GetHomeRegionResultTypeDef",
)

_RequiredTargetTypeDef = TypedDict("_RequiredTargetTypeDef", {"Type": Literal["ACCOUNT"]})
_OptionalTargetTypeDef = TypedDict("_OptionalTargetTypeDef", {"Id": str}, total=False)


class TargetTypeDef(_RequiredTargetTypeDef, _OptionalTargetTypeDef):
    pass


HomeRegionControlTypeDef = TypedDict(
    "HomeRegionControlTypeDef",
    {"ControlId": str, "HomeRegion": str, "Target": TargetTypeDef, "RequestedTime": datetime},
    total=False,
)

CreateHomeRegionControlResultTypeDef = TypedDict(
    "CreateHomeRegionControlResultTypeDef",
    {"HomeRegionControl": HomeRegionControlTypeDef},
    total=False,
)

DescribeHomeRegionControlsResultTypeDef = TypedDict(
    "DescribeHomeRegionControlsResultTypeDef",
    {"HomeRegionControls": List[HomeRegionControlTypeDef], "NextToken": str},
    total=False,
)

GetHomeRegionResultTypeDef = TypedDict(
    "GetHomeRegionResultTypeDef", {"HomeRegion": str}, total=False
)
