"""
Main interface for pi service type definitions.

Usage::

    from mypy_boto3.pi.type_defs import DimensionKeyDescriptionTypeDef

    data: DimensionKeyDescriptionTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DimensionKeyDescriptionTypeDef",
    "ResponsePartitionKeyTypeDef",
    "DescribeDimensionKeysResponseTypeDef",
    "DimensionGroupTypeDef",
    "DataPointTypeDef",
    "ResponseResourceMetricKeyTypeDef",
    "MetricKeyDataPointsTypeDef",
    "GetResourceMetricsResponseTypeDef",
    "MetricQueryTypeDef",
)

DimensionKeyDescriptionTypeDef = TypedDict(
    "DimensionKeyDescriptionTypeDef",
    {"Dimensions": Dict[str, str], "Total": float, "Partitions": List[float]},
    total=False,
)

ResponsePartitionKeyTypeDef = TypedDict(
    "ResponsePartitionKeyTypeDef", {"Dimensions": Dict[str, str]}
)

DescribeDimensionKeysResponseTypeDef = TypedDict(
    "DescribeDimensionKeysResponseTypeDef",
    {
        "AlignedStartTime": datetime,
        "AlignedEndTime": datetime,
        "PartitionKeys": List[ResponsePartitionKeyTypeDef],
        "Keys": List[DimensionKeyDescriptionTypeDef],
        "NextToken": str,
    },
    total=False,
)

_RequiredDimensionGroupTypeDef = TypedDict("_RequiredDimensionGroupTypeDef", {"Group": str})
_OptionalDimensionGroupTypeDef = TypedDict(
    "_OptionalDimensionGroupTypeDef", {"Dimensions": List[str], "Limit": int}, total=False
)


class DimensionGroupTypeDef(_RequiredDimensionGroupTypeDef, _OptionalDimensionGroupTypeDef):
    pass


DataPointTypeDef = TypedDict("DataPointTypeDef", {"Timestamp": datetime, "Value": float})

_RequiredResponseResourceMetricKeyTypeDef = TypedDict(
    "_RequiredResponseResourceMetricKeyTypeDef", {"Metric": str}
)
_OptionalResponseResourceMetricKeyTypeDef = TypedDict(
    "_OptionalResponseResourceMetricKeyTypeDef", {"Dimensions": Dict[str, str]}, total=False
)


class ResponseResourceMetricKeyTypeDef(
    _RequiredResponseResourceMetricKeyTypeDef, _OptionalResponseResourceMetricKeyTypeDef
):
    pass


MetricKeyDataPointsTypeDef = TypedDict(
    "MetricKeyDataPointsTypeDef",
    {"Key": ResponseResourceMetricKeyTypeDef, "DataPoints": List[DataPointTypeDef]},
    total=False,
)

GetResourceMetricsResponseTypeDef = TypedDict(
    "GetResourceMetricsResponseTypeDef",
    {
        "AlignedStartTime": datetime,
        "AlignedEndTime": datetime,
        "Identifier": str,
        "MetricList": List[MetricKeyDataPointsTypeDef],
        "NextToken": str,
    },
    total=False,
)

_RequiredMetricQueryTypeDef = TypedDict("_RequiredMetricQueryTypeDef", {"Metric": str})
_OptionalMetricQueryTypeDef = TypedDict(
    "_OptionalMetricQueryTypeDef",
    {"GroupBy": DimensionGroupTypeDef, "Filter": Dict[str, str]},
    total=False,
)


class MetricQueryTypeDef(_RequiredMetricQueryTypeDef, _OptionalMetricQueryTypeDef):
    pass
