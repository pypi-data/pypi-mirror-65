"""
Main interface for iot1click-projects service type definitions.

Usage::

    from mypy_boto3.iot1click_projects.type_defs import PlacementDescriptionTypeDef

    data: PlacementDescriptionTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "PlacementDescriptionTypeDef",
    "DescribePlacementResponseTypeDef",
    "DeviceTemplateTypeDef",
    "PlacementTemplateTypeDef",
    "ProjectDescriptionTypeDef",
    "DescribeProjectResponseTypeDef",
    "GetDevicesInPlacementResponseTypeDef",
    "PlacementSummaryTypeDef",
    "ListPlacementsResponseTypeDef",
    "ProjectSummaryTypeDef",
    "ListProjectsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
)

PlacementDescriptionTypeDef = TypedDict(
    "PlacementDescriptionTypeDef",
    {
        "projectName": str,
        "placementName": str,
        "attributes": Dict[str, str],
        "createdDate": datetime,
        "updatedDate": datetime,
    },
)

DescribePlacementResponseTypeDef = TypedDict(
    "DescribePlacementResponseTypeDef", {"placement": PlacementDescriptionTypeDef}
)

DeviceTemplateTypeDef = TypedDict(
    "DeviceTemplateTypeDef", {"deviceType": str, "callbackOverrides": Dict[str, str]}, total=False
)

PlacementTemplateTypeDef = TypedDict(
    "PlacementTemplateTypeDef",
    {"defaultAttributes": Dict[str, str], "deviceTemplates": Dict[str, DeviceTemplateTypeDef]},
    total=False,
)

_RequiredProjectDescriptionTypeDef = TypedDict(
    "_RequiredProjectDescriptionTypeDef",
    {"projectName": str, "createdDate": datetime, "updatedDate": datetime},
)
_OptionalProjectDescriptionTypeDef = TypedDict(
    "_OptionalProjectDescriptionTypeDef",
    {
        "arn": str,
        "description": str,
        "placementTemplate": PlacementTemplateTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)


class ProjectDescriptionTypeDef(
    _RequiredProjectDescriptionTypeDef, _OptionalProjectDescriptionTypeDef
):
    pass


DescribeProjectResponseTypeDef = TypedDict(
    "DescribeProjectResponseTypeDef", {"project": ProjectDescriptionTypeDef}
)

GetDevicesInPlacementResponseTypeDef = TypedDict(
    "GetDevicesInPlacementResponseTypeDef", {"devices": Dict[str, str]}
)

PlacementSummaryTypeDef = TypedDict(
    "PlacementSummaryTypeDef",
    {"projectName": str, "placementName": str, "createdDate": datetime, "updatedDate": datetime},
)

_RequiredListPlacementsResponseTypeDef = TypedDict(
    "_RequiredListPlacementsResponseTypeDef", {"placements": List[PlacementSummaryTypeDef]}
)
_OptionalListPlacementsResponseTypeDef = TypedDict(
    "_OptionalListPlacementsResponseTypeDef", {"nextToken": str}, total=False
)


class ListPlacementsResponseTypeDef(
    _RequiredListPlacementsResponseTypeDef, _OptionalListPlacementsResponseTypeDef
):
    pass


_RequiredProjectSummaryTypeDef = TypedDict(
    "_RequiredProjectSummaryTypeDef",
    {"projectName": str, "createdDate": datetime, "updatedDate": datetime},
)
_OptionalProjectSummaryTypeDef = TypedDict(
    "_OptionalProjectSummaryTypeDef", {"arn": str, "tags": Dict[str, str]}, total=False
)


class ProjectSummaryTypeDef(_RequiredProjectSummaryTypeDef, _OptionalProjectSummaryTypeDef):
    pass


_RequiredListProjectsResponseTypeDef = TypedDict(
    "_RequiredListProjectsResponseTypeDef", {"projects": List[ProjectSummaryTypeDef]}
)
_OptionalListProjectsResponseTypeDef = TypedDict(
    "_OptionalListProjectsResponseTypeDef", {"nextToken": str}, total=False
)


class ListProjectsResponseTypeDef(
    _RequiredListProjectsResponseTypeDef, _OptionalListProjectsResponseTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": Dict[str, str]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
