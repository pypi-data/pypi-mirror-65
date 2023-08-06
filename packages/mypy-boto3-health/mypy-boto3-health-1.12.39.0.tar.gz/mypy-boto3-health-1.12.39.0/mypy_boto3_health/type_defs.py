"""
Main interface for health service type definitions.

Usage::

    from mypy_boto3.health.type_defs import DescribeAffectedAccountsForOrganizationResponseTypeDef

    data: DescribeAffectedAccountsForOrganizationResponseTypeDef = {...}
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
    "DescribeAffectedAccountsForOrganizationResponseTypeDef",
    "AffectedEntityTypeDef",
    "OrganizationAffectedEntitiesErrorItemTypeDef",
    "DescribeAffectedEntitiesForOrganizationResponseTypeDef",
    "DescribeAffectedEntitiesResponseTypeDef",
    "EntityAggregateTypeDef",
    "DescribeEntityAggregatesResponseTypeDef",
    "EventAggregateTypeDef",
    "DescribeEventAggregatesResponseTypeDef",
    "OrganizationEventDetailsErrorItemTypeDef",
    "EventDescriptionTypeDef",
    "EventTypeDef",
    "OrganizationEventDetailsTypeDef",
    "DescribeEventDetailsForOrganizationResponseTypeDef",
    "EventDetailsErrorItemTypeDef",
    "EventDetailsTypeDef",
    "DescribeEventDetailsResponseTypeDef",
    "EventTypeTypeDef",
    "DescribeEventTypesResponseTypeDef",
    "OrganizationEventTypeDef",
    "DescribeEventsForOrganizationResponseTypeDef",
    "DescribeEventsResponseTypeDef",
    "DescribeHealthServiceStatusForOrganizationResponseTypeDef",
    "DateTimeRangeTypeDef",
    "EntityFilterTypeDef",
    "EventAccountFilterTypeDef",
    "EventFilterTypeDef",
    "EventTypeFilterTypeDef",
    "OrganizationEventFilterTypeDef",
    "PaginatorConfigTypeDef",
)

DescribeAffectedAccountsForOrganizationResponseTypeDef = TypedDict(
    "DescribeAffectedAccountsForOrganizationResponseTypeDef",
    {"affectedAccounts": List[str], "nextToken": str},
    total=False,
)

AffectedEntityTypeDef = TypedDict(
    "AffectedEntityTypeDef",
    {
        "entityArn": str,
        "eventArn": str,
        "entityValue": str,
        "entityUrl": str,
        "awsAccountId": str,
        "lastUpdatedTime": datetime,
        "statusCode": Literal["IMPAIRED", "UNIMPAIRED", "UNKNOWN"],
        "tags": Dict[str, str],
    },
    total=False,
)

OrganizationAffectedEntitiesErrorItemTypeDef = TypedDict(
    "OrganizationAffectedEntitiesErrorItemTypeDef",
    {"awsAccountId": str, "eventArn": str, "errorName": str, "errorMessage": str},
    total=False,
)

DescribeAffectedEntitiesForOrganizationResponseTypeDef = TypedDict(
    "DescribeAffectedEntitiesForOrganizationResponseTypeDef",
    {
        "entities": List[AffectedEntityTypeDef],
        "failedSet": List[OrganizationAffectedEntitiesErrorItemTypeDef],
        "nextToken": str,
    },
    total=False,
)

DescribeAffectedEntitiesResponseTypeDef = TypedDict(
    "DescribeAffectedEntitiesResponseTypeDef",
    {"entities": List[AffectedEntityTypeDef], "nextToken": str},
    total=False,
)

EntityAggregateTypeDef = TypedDict(
    "EntityAggregateTypeDef", {"eventArn": str, "count": int}, total=False
)

DescribeEntityAggregatesResponseTypeDef = TypedDict(
    "DescribeEntityAggregatesResponseTypeDef",
    {"entityAggregates": List[EntityAggregateTypeDef]},
    total=False,
)

EventAggregateTypeDef = TypedDict(
    "EventAggregateTypeDef", {"aggregateValue": str, "count": int}, total=False
)

DescribeEventAggregatesResponseTypeDef = TypedDict(
    "DescribeEventAggregatesResponseTypeDef",
    {"eventAggregates": List[EventAggregateTypeDef], "nextToken": str},
    total=False,
)

OrganizationEventDetailsErrorItemTypeDef = TypedDict(
    "OrganizationEventDetailsErrorItemTypeDef",
    {"awsAccountId": str, "eventArn": str, "errorName": str, "errorMessage": str},
    total=False,
)

EventDescriptionTypeDef = TypedDict(
    "EventDescriptionTypeDef", {"latestDescription": str}, total=False
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "arn": str,
        "service": str,
        "eventTypeCode": str,
        "eventTypeCategory": Literal[
            "issue", "accountNotification", "scheduledChange", "investigation"
        ],
        "region": str,
        "availabilityZone": str,
        "startTime": datetime,
        "endTime": datetime,
        "lastUpdatedTime": datetime,
        "statusCode": Literal["open", "closed", "upcoming"],
    },
    total=False,
)

OrganizationEventDetailsTypeDef = TypedDict(
    "OrganizationEventDetailsTypeDef",
    {
        "awsAccountId": str,
        "event": EventTypeDef,
        "eventDescription": EventDescriptionTypeDef,
        "eventMetadata": Dict[str, str],
    },
    total=False,
)

DescribeEventDetailsForOrganizationResponseTypeDef = TypedDict(
    "DescribeEventDetailsForOrganizationResponseTypeDef",
    {
        "successfulSet": List[OrganizationEventDetailsTypeDef],
        "failedSet": List[OrganizationEventDetailsErrorItemTypeDef],
    },
    total=False,
)

EventDetailsErrorItemTypeDef = TypedDict(
    "EventDetailsErrorItemTypeDef",
    {"eventArn": str, "errorName": str, "errorMessage": str},
    total=False,
)

EventDetailsTypeDef = TypedDict(
    "EventDetailsTypeDef",
    {
        "event": EventTypeDef,
        "eventDescription": EventDescriptionTypeDef,
        "eventMetadata": Dict[str, str],
    },
    total=False,
)

DescribeEventDetailsResponseTypeDef = TypedDict(
    "DescribeEventDetailsResponseTypeDef",
    {"successfulSet": List[EventDetailsTypeDef], "failedSet": List[EventDetailsErrorItemTypeDef]},
    total=False,
)

EventTypeTypeDef = TypedDict(
    "EventTypeTypeDef",
    {
        "service": str,
        "code": str,
        "category": Literal["issue", "accountNotification", "scheduledChange", "investigation"],
    },
    total=False,
)

DescribeEventTypesResponseTypeDef = TypedDict(
    "DescribeEventTypesResponseTypeDef",
    {"eventTypes": List[EventTypeTypeDef], "nextToken": str},
    total=False,
)

OrganizationEventTypeDef = TypedDict(
    "OrganizationEventTypeDef",
    {
        "arn": str,
        "service": str,
        "eventTypeCode": str,
        "eventTypeCategory": Literal[
            "issue", "accountNotification", "scheduledChange", "investigation"
        ],
        "region": str,
        "startTime": datetime,
        "endTime": datetime,
        "lastUpdatedTime": datetime,
        "statusCode": Literal["open", "closed", "upcoming"],
    },
    total=False,
)

DescribeEventsForOrganizationResponseTypeDef = TypedDict(
    "DescribeEventsForOrganizationResponseTypeDef",
    {"events": List[OrganizationEventTypeDef], "nextToken": str},
    total=False,
)

DescribeEventsResponseTypeDef = TypedDict(
    "DescribeEventsResponseTypeDef", {"events": List[EventTypeDef], "nextToken": str}, total=False
)

DescribeHealthServiceStatusForOrganizationResponseTypeDef = TypedDict(
    "DescribeHealthServiceStatusForOrganizationResponseTypeDef",
    {"healthServiceAccessStatusForOrganization": str},
    total=False,
)

DateTimeRangeTypeDef = TypedDict(
    "DateTimeRangeTypeDef", {"from": datetime, "to": datetime}, total=False
)

_RequiredEntityFilterTypeDef = TypedDict("_RequiredEntityFilterTypeDef", {"eventArns": List[str]})
_OptionalEntityFilterTypeDef = TypedDict(
    "_OptionalEntityFilterTypeDef",
    {
        "entityArns": List[str],
        "entityValues": List[str],
        "lastUpdatedTimes": List[DateTimeRangeTypeDef],
        "tags": List[Dict[str, str]],
        "statusCodes": List[Literal["IMPAIRED", "UNIMPAIRED", "UNKNOWN"]],
    },
    total=False,
)


class EntityFilterTypeDef(_RequiredEntityFilterTypeDef, _OptionalEntityFilterTypeDef):
    pass


EventAccountFilterTypeDef = TypedDict(
    "EventAccountFilterTypeDef", {"eventArn": str, "awsAccountId": str}
)

EventFilterTypeDef = TypedDict(
    "EventFilterTypeDef",
    {
        "eventArns": List[str],
        "eventTypeCodes": List[str],
        "services": List[str],
        "regions": List[str],
        "availabilityZones": List[str],
        "startTimes": List[DateTimeRangeTypeDef],
        "endTimes": List[DateTimeRangeTypeDef],
        "lastUpdatedTimes": List[DateTimeRangeTypeDef],
        "entityArns": List[str],
        "entityValues": List[str],
        "eventTypeCategories": List[
            Literal["issue", "accountNotification", "scheduledChange", "investigation"]
        ],
        "tags": List[Dict[str, str]],
        "eventStatusCodes": List[Literal["open", "closed", "upcoming"]],
    },
    total=False,
)

EventTypeFilterTypeDef = TypedDict(
    "EventTypeFilterTypeDef",
    {
        "eventTypeCodes": List[str],
        "services": List[str],
        "eventTypeCategories": List[
            Literal["issue", "accountNotification", "scheduledChange", "investigation"]
        ],
    },
    total=False,
)

OrganizationEventFilterTypeDef = TypedDict(
    "OrganizationEventFilterTypeDef",
    {
        "eventTypeCodes": List[str],
        "awsAccountIds": List[str],
        "services": List[str],
        "regions": List[str],
        "startTime": DateTimeRangeTypeDef,
        "endTime": DateTimeRangeTypeDef,
        "lastUpdatedTime": DateTimeRangeTypeDef,
        "entityArns": List[str],
        "entityValues": List[str],
        "eventTypeCategories": List[
            Literal["issue", "accountNotification", "scheduledChange", "investigation"]
        ],
        "eventStatusCodes": List[Literal["open", "closed", "upcoming"]],
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
