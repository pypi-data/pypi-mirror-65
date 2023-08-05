"""
Main interface for sns service type definitions.

Usage::

    from mypy_boto3.sns.type_defs import CheckIfPhoneNumberIsOptedOutResponseTypeDef

    data: CheckIfPhoneNumberIsOptedOutResponseTypeDef = {...}
"""
import sys
from typing import Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CheckIfPhoneNumberIsOptedOutResponseTypeDef",
    "ConfirmSubscriptionResponseTypeDef",
    "CreateEndpointResponseTypeDef",
    "CreatePlatformApplicationResponseTypeDef",
    "CreateTopicResponseTypeDef",
    "GetEndpointAttributesResponseTypeDef",
    "GetPlatformApplicationAttributesResponseTypeDef",
    "GetSMSAttributesResponseTypeDef",
    "GetSubscriptionAttributesResponseTypeDef",
    "GetTopicAttributesResponseTypeDef",
    "EndpointTypeDef",
    "ListEndpointsByPlatformApplicationResponseTypeDef",
    "ListPhoneNumbersOptedOutResponseTypeDef",
    "PlatformApplicationTypeDef",
    "ListPlatformApplicationsResponseTypeDef",
    "SubscriptionTypeDef",
    "ListSubscriptionsByTopicResponseTypeDef",
    "ListSubscriptionsResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TopicTypeDef",
    "ListTopicsResponseTypeDef",
    "MessageAttributeValueTypeDef",
    "PaginatorConfigTypeDef",
    "PublishResponseTypeDef",
    "SubscribeResponseTypeDef",
)

CheckIfPhoneNumberIsOptedOutResponseTypeDef = TypedDict(
    "CheckIfPhoneNumberIsOptedOutResponseTypeDef", {"isOptedOut": bool}, total=False
)

ConfirmSubscriptionResponseTypeDef = TypedDict(
    "ConfirmSubscriptionResponseTypeDef", {"SubscriptionArn": str}, total=False
)

CreateEndpointResponseTypeDef = TypedDict(
    "CreateEndpointResponseTypeDef", {"EndpointArn": str}, total=False
)

CreatePlatformApplicationResponseTypeDef = TypedDict(
    "CreatePlatformApplicationResponseTypeDef", {"PlatformApplicationArn": str}, total=False
)

CreateTopicResponseTypeDef = TypedDict("CreateTopicResponseTypeDef", {"TopicArn": str}, total=False)

GetEndpointAttributesResponseTypeDef = TypedDict(
    "GetEndpointAttributesResponseTypeDef", {"Attributes": Dict[str, str]}, total=False
)

GetPlatformApplicationAttributesResponseTypeDef = TypedDict(
    "GetPlatformApplicationAttributesResponseTypeDef", {"Attributes": Dict[str, str]}, total=False
)

GetSMSAttributesResponseTypeDef = TypedDict(
    "GetSMSAttributesResponseTypeDef", {"attributes": Dict[str, str]}, total=False
)

GetSubscriptionAttributesResponseTypeDef = TypedDict(
    "GetSubscriptionAttributesResponseTypeDef", {"Attributes": Dict[str, str]}, total=False
)

GetTopicAttributesResponseTypeDef = TypedDict(
    "GetTopicAttributesResponseTypeDef", {"Attributes": Dict[str, str]}, total=False
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef", {"EndpointArn": str, "Attributes": Dict[str, str]}, total=False
)

ListEndpointsByPlatformApplicationResponseTypeDef = TypedDict(
    "ListEndpointsByPlatformApplicationResponseTypeDef",
    {"Endpoints": List[EndpointTypeDef], "NextToken": str},
    total=False,
)

ListPhoneNumbersOptedOutResponseTypeDef = TypedDict(
    "ListPhoneNumbersOptedOutResponseTypeDef",
    {"phoneNumbers": List[str], "nextToken": str},
    total=False,
)

PlatformApplicationTypeDef = TypedDict(
    "PlatformApplicationTypeDef",
    {"PlatformApplicationArn": str, "Attributes": Dict[str, str]},
    total=False,
)

ListPlatformApplicationsResponseTypeDef = TypedDict(
    "ListPlatformApplicationsResponseTypeDef",
    {"PlatformApplications": List[PlatformApplicationTypeDef], "NextToken": str},
    total=False,
)

SubscriptionTypeDef = TypedDict(
    "SubscriptionTypeDef",
    {"SubscriptionArn": str, "Owner": str, "Protocol": str, "Endpoint": str, "TopicArn": str},
    total=False,
)

ListSubscriptionsByTopicResponseTypeDef = TypedDict(
    "ListSubscriptionsByTopicResponseTypeDef",
    {"Subscriptions": List[SubscriptionTypeDef], "NextToken": str},
    total=False,
)

ListSubscriptionsResponseTypeDef = TypedDict(
    "ListSubscriptionsResponseTypeDef",
    {"Subscriptions": List[SubscriptionTypeDef], "NextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef]}, total=False
)

TopicTypeDef = TypedDict("TopicTypeDef", {"TopicArn": str}, total=False)

ListTopicsResponseTypeDef = TypedDict(
    "ListTopicsResponseTypeDef", {"Topics": List[TopicTypeDef], "NextToken": str}, total=False
)

_RequiredMessageAttributeValueTypeDef = TypedDict(
    "_RequiredMessageAttributeValueTypeDef", {"DataType": str}
)
_OptionalMessageAttributeValueTypeDef = TypedDict(
    "_OptionalMessageAttributeValueTypeDef",
    {"StringValue": str, "BinaryValue": Union[bytes, IO]},
    total=False,
)


class MessageAttributeValueTypeDef(
    _RequiredMessageAttributeValueTypeDef, _OptionalMessageAttributeValueTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PublishResponseTypeDef = TypedDict("PublishResponseTypeDef", {"MessageId": str}, total=False)

SubscribeResponseTypeDef = TypedDict(
    "SubscribeResponseTypeDef", {"SubscriptionArn": str}, total=False
)
