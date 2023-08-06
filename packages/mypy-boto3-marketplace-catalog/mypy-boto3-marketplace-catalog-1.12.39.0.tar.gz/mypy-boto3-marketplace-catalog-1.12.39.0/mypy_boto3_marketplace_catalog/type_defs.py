"""
Main interface for marketplace-catalog service type definitions.

Usage::

    from mypy_boto3.marketplace_catalog.type_defs import CancelChangeSetResponseTypeDef

    data: CancelChangeSetResponseTypeDef = {...}
"""
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
    "CancelChangeSetResponseTypeDef",
    "EntityTypeDef",
    "ChangeTypeDef",
    "ErrorDetailTypeDef",
    "ChangeSummaryTypeDef",
    "DescribeChangeSetResponseTypeDef",
    "DescribeEntityResponseTypeDef",
    "FilterTypeDef",
    "ChangeSetSummaryListItemTypeDef",
    "ListChangeSetsResponseTypeDef",
    "EntitySummaryTypeDef",
    "ListEntitiesResponseTypeDef",
    "SortTypeDef",
    "StartChangeSetResponseTypeDef",
)

CancelChangeSetResponseTypeDef = TypedDict(
    "CancelChangeSetResponseTypeDef", {"ChangeSetId": str, "ChangeSetArn": str}, total=False
)

_RequiredEntityTypeDef = TypedDict("_RequiredEntityTypeDef", {"Type": str})
_OptionalEntityTypeDef = TypedDict("_OptionalEntityTypeDef", {"Identifier": str}, total=False)


class EntityTypeDef(_RequiredEntityTypeDef, _OptionalEntityTypeDef):
    pass


ChangeTypeDef = TypedDict(
    "ChangeTypeDef", {"ChangeType": str, "Entity": EntityTypeDef, "Details": str}
)

ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef", {"ErrorCode": str, "ErrorMessage": str}, total=False
)

ChangeSummaryTypeDef = TypedDict(
    "ChangeSummaryTypeDef",
    {"ChangeType": str, "Entity": EntityTypeDef, "ErrorDetailList": List[ErrorDetailTypeDef]},
    total=False,
)

DescribeChangeSetResponseTypeDef = TypedDict(
    "DescribeChangeSetResponseTypeDef",
    {
        "ChangeSetId": str,
        "ChangeSetArn": str,
        "ChangeSetName": str,
        "StartTime": str,
        "EndTime": str,
        "Status": Literal["PREPARING", "APPLYING", "SUCCEEDED", "CANCELLED", "FAILED"],
        "FailureDescription": str,
        "ChangeSet": List[ChangeSummaryTypeDef],
    },
    total=False,
)

DescribeEntityResponseTypeDef = TypedDict(
    "DescribeEntityResponseTypeDef",
    {
        "EntityType": str,
        "EntityIdentifier": str,
        "EntityArn": str,
        "LastModifiedDate": str,
        "Details": str,
    },
    total=False,
)

FilterTypeDef = TypedDict("FilterTypeDef", {"Name": str, "ValueList": List[str]}, total=False)

ChangeSetSummaryListItemTypeDef = TypedDict(
    "ChangeSetSummaryListItemTypeDef",
    {
        "ChangeSetId": str,
        "ChangeSetArn": str,
        "ChangeSetName": str,
        "StartTime": str,
        "EndTime": str,
        "Status": Literal["PREPARING", "APPLYING", "SUCCEEDED", "CANCELLED", "FAILED"],
        "EntityIdList": List[str],
    },
    total=False,
)

ListChangeSetsResponseTypeDef = TypedDict(
    "ListChangeSetsResponseTypeDef",
    {"ChangeSetSummaryList": List[ChangeSetSummaryListItemTypeDef], "NextToken": str},
    total=False,
)

EntitySummaryTypeDef = TypedDict(
    "EntitySummaryTypeDef",
    {
        "Name": str,
        "EntityType": str,
        "EntityId": str,
        "EntityArn": str,
        "LastModifiedDate": str,
        "Visibility": str,
    },
    total=False,
)

ListEntitiesResponseTypeDef = TypedDict(
    "ListEntitiesResponseTypeDef",
    {"EntitySummaryList": List[EntitySummaryTypeDef], "NextToken": str},
    total=False,
)

SortTypeDef = TypedDict(
    "SortTypeDef", {"SortBy": str, "SortOrder": Literal["ASCENDING", "DESCENDING"]}, total=False
)

StartChangeSetResponseTypeDef = TypedDict(
    "StartChangeSetResponseTypeDef", {"ChangeSetId": str, "ChangeSetArn": str}, total=False
)
