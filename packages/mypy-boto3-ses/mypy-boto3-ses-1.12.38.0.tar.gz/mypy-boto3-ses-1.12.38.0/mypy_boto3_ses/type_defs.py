"""
Main interface for ses service type definitions.

Usage::

    from mypy_boto3.ses.type_defs import ExtensionFieldTypeDef

    data: ExtensionFieldTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ExtensionFieldTypeDef",
    "RecipientDsnFieldsTypeDef",
    "BouncedRecipientInfoTypeDef",
    "DestinationTypeDef",
    "MessageTagTypeDef",
    "BulkEmailDestinationTypeDef",
    "ConfigurationSetTypeDef",
    "DeliveryOptionsTypeDef",
    "ReceiptRuleSetMetadataTypeDef",
    "AddHeaderActionTypeDef",
    "BounceActionTypeDef",
    "LambdaActionTypeDef",
    "S3ActionTypeDef",
    "SNSActionTypeDef",
    "StopActionTypeDef",
    "WorkmailActionTypeDef",
    "ReceiptActionTypeDef",
    "ReceiptRuleTypeDef",
    "DescribeActiveReceiptRuleSetResponseTypeDef",
    "CloudWatchDimensionConfigurationTypeDef",
    "CloudWatchDestinationTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "SNSDestinationTypeDef",
    "EventDestinationTypeDef",
    "ReputationOptionsTypeDef",
    "TrackingOptionsTypeDef",
    "DescribeConfigurationSetResponseTypeDef",
    "DescribeReceiptRuleResponseTypeDef",
    "DescribeReceiptRuleSetResponseTypeDef",
    "GetAccountSendingEnabledResponseTypeDef",
    "GetCustomVerificationEmailTemplateResponseTypeDef",
    "IdentityDkimAttributesTypeDef",
    "GetIdentityDkimAttributesResponseTypeDef",
    "IdentityMailFromDomainAttributesTypeDef",
    "GetIdentityMailFromDomainAttributesResponseTypeDef",
    "IdentityNotificationAttributesTypeDef",
    "GetIdentityNotificationAttributesResponseTypeDef",
    "GetIdentityPoliciesResponseTypeDef",
    "IdentityVerificationAttributesTypeDef",
    "GetIdentityVerificationAttributesResponseTypeDef",
    "GetSendQuotaResponseTypeDef",
    "SendDataPointTypeDef",
    "GetSendStatisticsResponseTypeDef",
    "TemplateTypeDef",
    "GetTemplateResponseTypeDef",
    "ListConfigurationSetsResponseTypeDef",
    "CustomVerificationEmailTemplateTypeDef",
    "ListCustomVerificationEmailTemplatesResponseTypeDef",
    "ListIdentitiesResponseTypeDef",
    "ListIdentityPoliciesResponseTypeDef",
    "ReceiptIpFilterTypeDef",
    "ReceiptFilterTypeDef",
    "ListReceiptFiltersResponseTypeDef",
    "ListReceiptRuleSetsResponseTypeDef",
    "TemplateMetadataTypeDef",
    "ListTemplatesResponseTypeDef",
    "ListVerifiedEmailAddressesResponseTypeDef",
    "MessageDsnTypeDef",
    "ContentTypeDef",
    "BodyTypeDef",
    "MessageTypeDef",
    "PaginatorConfigTypeDef",
    "RawMessageTypeDef",
    "SendBounceResponseTypeDef",
    "BulkEmailDestinationStatusTypeDef",
    "SendBulkTemplatedEmailResponseTypeDef",
    "SendCustomVerificationEmailResponseTypeDef",
    "SendEmailResponseTypeDef",
    "SendRawEmailResponseTypeDef",
    "SendTemplatedEmailResponseTypeDef",
    "TestRenderTemplateResponseTypeDef",
    "VerifyDomainDkimResponseTypeDef",
    "VerifyDomainIdentityResponseTypeDef",
    "WaiterConfigTypeDef",
)

ExtensionFieldTypeDef = TypedDict("ExtensionFieldTypeDef", {"Name": str, "Value": str})

_RequiredRecipientDsnFieldsTypeDef = TypedDict(
    "_RequiredRecipientDsnFieldsTypeDef",
    {"Action": Literal["failed", "delayed", "delivered", "relayed", "expanded"], "Status": str},
)
_OptionalRecipientDsnFieldsTypeDef = TypedDict(
    "_OptionalRecipientDsnFieldsTypeDef",
    {
        "FinalRecipient": str,
        "RemoteMta": str,
        "DiagnosticCode": str,
        "LastAttemptDate": datetime,
        "ExtensionFields": List[ExtensionFieldTypeDef],
    },
    total=False,
)


class RecipientDsnFieldsTypeDef(
    _RequiredRecipientDsnFieldsTypeDef, _OptionalRecipientDsnFieldsTypeDef
):
    pass


_RequiredBouncedRecipientInfoTypeDef = TypedDict(
    "_RequiredBouncedRecipientInfoTypeDef", {"Recipient": str}
)
_OptionalBouncedRecipientInfoTypeDef = TypedDict(
    "_OptionalBouncedRecipientInfoTypeDef",
    {
        "RecipientArn": str,
        "BounceType": Literal[
            "DoesNotExist",
            "MessageTooLarge",
            "ExceededQuota",
            "ContentRejected",
            "Undefined",
            "TemporaryFailure",
        ],
        "RecipientDsnFields": RecipientDsnFieldsTypeDef,
    },
    total=False,
)


class BouncedRecipientInfoTypeDef(
    _RequiredBouncedRecipientInfoTypeDef, _OptionalBouncedRecipientInfoTypeDef
):
    pass


DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {"ToAddresses": List[str], "CcAddresses": List[str], "BccAddresses": List[str]},
    total=False,
)

MessageTagTypeDef = TypedDict("MessageTagTypeDef", {"Name": str, "Value": str})

_RequiredBulkEmailDestinationTypeDef = TypedDict(
    "_RequiredBulkEmailDestinationTypeDef", {"Destination": DestinationTypeDef}
)
_OptionalBulkEmailDestinationTypeDef = TypedDict(
    "_OptionalBulkEmailDestinationTypeDef",
    {"ReplacementTags": List[MessageTagTypeDef], "ReplacementTemplateData": str},
    total=False,
)


class BulkEmailDestinationTypeDef(
    _RequiredBulkEmailDestinationTypeDef, _OptionalBulkEmailDestinationTypeDef
):
    pass


ConfigurationSetTypeDef = TypedDict("ConfigurationSetTypeDef", {"Name": str})

DeliveryOptionsTypeDef = TypedDict(
    "DeliveryOptionsTypeDef", {"TlsPolicy": Literal["Require", "Optional"]}, total=False
)

ReceiptRuleSetMetadataTypeDef = TypedDict(
    "ReceiptRuleSetMetadataTypeDef", {"Name": str, "CreatedTimestamp": datetime}, total=False
)

AddHeaderActionTypeDef = TypedDict(
    "AddHeaderActionTypeDef", {"HeaderName": str, "HeaderValue": str}
)

_RequiredBounceActionTypeDef = TypedDict(
    "_RequiredBounceActionTypeDef", {"SmtpReplyCode": str, "Message": str, "Sender": str}
)
_OptionalBounceActionTypeDef = TypedDict(
    "_OptionalBounceActionTypeDef", {"TopicArn": str, "StatusCode": str}, total=False
)


class BounceActionTypeDef(_RequiredBounceActionTypeDef, _OptionalBounceActionTypeDef):
    pass


_RequiredLambdaActionTypeDef = TypedDict("_RequiredLambdaActionTypeDef", {"FunctionArn": str})
_OptionalLambdaActionTypeDef = TypedDict(
    "_OptionalLambdaActionTypeDef",
    {"TopicArn": str, "InvocationType": Literal["Event", "RequestResponse"]},
    total=False,
)


class LambdaActionTypeDef(_RequiredLambdaActionTypeDef, _OptionalLambdaActionTypeDef):
    pass


_RequiredS3ActionTypeDef = TypedDict("_RequiredS3ActionTypeDef", {"BucketName": str})
_OptionalS3ActionTypeDef = TypedDict(
    "_OptionalS3ActionTypeDef",
    {"TopicArn": str, "ObjectKeyPrefix": str, "KmsKeyArn": str},
    total=False,
)


class S3ActionTypeDef(_RequiredS3ActionTypeDef, _OptionalS3ActionTypeDef):
    pass


_RequiredSNSActionTypeDef = TypedDict("_RequiredSNSActionTypeDef", {"TopicArn": str})
_OptionalSNSActionTypeDef = TypedDict(
    "_OptionalSNSActionTypeDef", {"Encoding": Literal["UTF-8", "Base64"]}, total=False
)


class SNSActionTypeDef(_RequiredSNSActionTypeDef, _OptionalSNSActionTypeDef):
    pass


_RequiredStopActionTypeDef = TypedDict("_RequiredStopActionTypeDef", {"Scope": Literal["RuleSet"]})
_OptionalStopActionTypeDef = TypedDict("_OptionalStopActionTypeDef", {"TopicArn": str}, total=False)


class StopActionTypeDef(_RequiredStopActionTypeDef, _OptionalStopActionTypeDef):
    pass


_RequiredWorkmailActionTypeDef = TypedDict(
    "_RequiredWorkmailActionTypeDef", {"OrganizationArn": str}
)
_OptionalWorkmailActionTypeDef = TypedDict(
    "_OptionalWorkmailActionTypeDef", {"TopicArn": str}, total=False
)


class WorkmailActionTypeDef(_RequiredWorkmailActionTypeDef, _OptionalWorkmailActionTypeDef):
    pass


ReceiptActionTypeDef = TypedDict(
    "ReceiptActionTypeDef",
    {
        "S3Action": S3ActionTypeDef,
        "BounceAction": BounceActionTypeDef,
        "WorkmailAction": WorkmailActionTypeDef,
        "LambdaAction": LambdaActionTypeDef,
        "StopAction": StopActionTypeDef,
        "AddHeaderAction": AddHeaderActionTypeDef,
        "SNSAction": SNSActionTypeDef,
    },
    total=False,
)

_RequiredReceiptRuleTypeDef = TypedDict("_RequiredReceiptRuleTypeDef", {"Name": str})
_OptionalReceiptRuleTypeDef = TypedDict(
    "_OptionalReceiptRuleTypeDef",
    {
        "Enabled": bool,
        "TlsPolicy": Literal["Require", "Optional"],
        "Recipients": List[str],
        "Actions": List[ReceiptActionTypeDef],
        "ScanEnabled": bool,
    },
    total=False,
)


class ReceiptRuleTypeDef(_RequiredReceiptRuleTypeDef, _OptionalReceiptRuleTypeDef):
    pass


DescribeActiveReceiptRuleSetResponseTypeDef = TypedDict(
    "DescribeActiveReceiptRuleSetResponseTypeDef",
    {"Metadata": ReceiptRuleSetMetadataTypeDef, "Rules": List[ReceiptRuleTypeDef]},
    total=False,
)

CloudWatchDimensionConfigurationTypeDef = TypedDict(
    "CloudWatchDimensionConfigurationTypeDef",
    {
        "DimensionName": str,
        "DimensionValueSource": Literal["messageTag", "emailHeader", "linkTag"],
        "DefaultDimensionValue": str,
    },
)

CloudWatchDestinationTypeDef = TypedDict(
    "CloudWatchDestinationTypeDef",
    {"DimensionConfigurations": List[CloudWatchDimensionConfigurationTypeDef]},
)

KinesisFirehoseDestinationTypeDef = TypedDict(
    "KinesisFirehoseDestinationTypeDef", {"IAMRoleARN": str, "DeliveryStreamARN": str}
)

SNSDestinationTypeDef = TypedDict("SNSDestinationTypeDef", {"TopicARN": str})

_RequiredEventDestinationTypeDef = TypedDict(
    "_RequiredEventDestinationTypeDef",
    {
        "Name": str,
        "MatchingEventTypes": List[
            Literal[
                "send",
                "reject",
                "bounce",
                "complaint",
                "delivery",
                "open",
                "click",
                "renderingFailure",
            ]
        ],
    },
)
_OptionalEventDestinationTypeDef = TypedDict(
    "_OptionalEventDestinationTypeDef",
    {
        "Enabled": bool,
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "CloudWatchDestination": CloudWatchDestinationTypeDef,
        "SNSDestination": SNSDestinationTypeDef,
    },
    total=False,
)


class EventDestinationTypeDef(_RequiredEventDestinationTypeDef, _OptionalEventDestinationTypeDef):
    pass


ReputationOptionsTypeDef = TypedDict(
    "ReputationOptionsTypeDef",
    {"SendingEnabled": bool, "ReputationMetricsEnabled": bool, "LastFreshStart": datetime},
    total=False,
)

TrackingOptionsTypeDef = TypedDict(
    "TrackingOptionsTypeDef", {"CustomRedirectDomain": str}, total=False
)

DescribeConfigurationSetResponseTypeDef = TypedDict(
    "DescribeConfigurationSetResponseTypeDef",
    {
        "ConfigurationSet": ConfigurationSetTypeDef,
        "EventDestinations": List[EventDestinationTypeDef],
        "TrackingOptions": TrackingOptionsTypeDef,
        "DeliveryOptions": DeliveryOptionsTypeDef,
        "ReputationOptions": ReputationOptionsTypeDef,
    },
    total=False,
)

DescribeReceiptRuleResponseTypeDef = TypedDict(
    "DescribeReceiptRuleResponseTypeDef", {"Rule": ReceiptRuleTypeDef}, total=False
)

DescribeReceiptRuleSetResponseTypeDef = TypedDict(
    "DescribeReceiptRuleSetResponseTypeDef",
    {"Metadata": ReceiptRuleSetMetadataTypeDef, "Rules": List[ReceiptRuleTypeDef]},
    total=False,
)

GetAccountSendingEnabledResponseTypeDef = TypedDict(
    "GetAccountSendingEnabledResponseTypeDef", {"Enabled": bool}, total=False
)

GetCustomVerificationEmailTemplateResponseTypeDef = TypedDict(
    "GetCustomVerificationEmailTemplateResponseTypeDef",
    {
        "TemplateName": str,
        "FromEmailAddress": str,
        "TemplateSubject": str,
        "TemplateContent": str,
        "SuccessRedirectionURL": str,
        "FailureRedirectionURL": str,
    },
    total=False,
)

_RequiredIdentityDkimAttributesTypeDef = TypedDict(
    "_RequiredIdentityDkimAttributesTypeDef",
    {
        "DkimEnabled": bool,
        "DkimVerificationStatus": Literal[
            "Pending", "Success", "Failed", "TemporaryFailure", "NotStarted"
        ],
    },
)
_OptionalIdentityDkimAttributesTypeDef = TypedDict(
    "_OptionalIdentityDkimAttributesTypeDef", {"DkimTokens": List[str]}, total=False
)


class IdentityDkimAttributesTypeDef(
    _RequiredIdentityDkimAttributesTypeDef, _OptionalIdentityDkimAttributesTypeDef
):
    pass


GetIdentityDkimAttributesResponseTypeDef = TypedDict(
    "GetIdentityDkimAttributesResponseTypeDef",
    {"DkimAttributes": Dict[str, IdentityDkimAttributesTypeDef]},
)

IdentityMailFromDomainAttributesTypeDef = TypedDict(
    "IdentityMailFromDomainAttributesTypeDef",
    {
        "MailFromDomain": str,
        "MailFromDomainStatus": Literal["Pending", "Success", "Failed", "TemporaryFailure"],
        "BehaviorOnMXFailure": Literal["UseDefaultValue", "RejectMessage"],
    },
)

GetIdentityMailFromDomainAttributesResponseTypeDef = TypedDict(
    "GetIdentityMailFromDomainAttributesResponseTypeDef",
    {"MailFromDomainAttributes": Dict[str, IdentityMailFromDomainAttributesTypeDef]},
)

_RequiredIdentityNotificationAttributesTypeDef = TypedDict(
    "_RequiredIdentityNotificationAttributesTypeDef",
    {"BounceTopic": str, "ComplaintTopic": str, "DeliveryTopic": str, "ForwardingEnabled": bool},
)
_OptionalIdentityNotificationAttributesTypeDef = TypedDict(
    "_OptionalIdentityNotificationAttributesTypeDef",
    {
        "HeadersInBounceNotificationsEnabled": bool,
        "HeadersInComplaintNotificationsEnabled": bool,
        "HeadersInDeliveryNotificationsEnabled": bool,
    },
    total=False,
)


class IdentityNotificationAttributesTypeDef(
    _RequiredIdentityNotificationAttributesTypeDef, _OptionalIdentityNotificationAttributesTypeDef
):
    pass


GetIdentityNotificationAttributesResponseTypeDef = TypedDict(
    "GetIdentityNotificationAttributesResponseTypeDef",
    {"NotificationAttributes": Dict[str, IdentityNotificationAttributesTypeDef]},
)

GetIdentityPoliciesResponseTypeDef = TypedDict(
    "GetIdentityPoliciesResponseTypeDef", {"Policies": Dict[str, str]}
)

_RequiredIdentityVerificationAttributesTypeDef = TypedDict(
    "_RequiredIdentityVerificationAttributesTypeDef",
    {
        "VerificationStatus": Literal[
            "Pending", "Success", "Failed", "TemporaryFailure", "NotStarted"
        ]
    },
)
_OptionalIdentityVerificationAttributesTypeDef = TypedDict(
    "_OptionalIdentityVerificationAttributesTypeDef", {"VerificationToken": str}, total=False
)


class IdentityVerificationAttributesTypeDef(
    _RequiredIdentityVerificationAttributesTypeDef, _OptionalIdentityVerificationAttributesTypeDef
):
    pass


GetIdentityVerificationAttributesResponseTypeDef = TypedDict(
    "GetIdentityVerificationAttributesResponseTypeDef",
    {"VerificationAttributes": Dict[str, IdentityVerificationAttributesTypeDef]},
)

GetSendQuotaResponseTypeDef = TypedDict(
    "GetSendQuotaResponseTypeDef",
    {"Max24HourSend": float, "MaxSendRate": float, "SentLast24Hours": float},
    total=False,
)

SendDataPointTypeDef = TypedDict(
    "SendDataPointTypeDef",
    {
        "Timestamp": datetime,
        "DeliveryAttempts": int,
        "Bounces": int,
        "Complaints": int,
        "Rejects": int,
    },
    total=False,
)

GetSendStatisticsResponseTypeDef = TypedDict(
    "GetSendStatisticsResponseTypeDef", {"SendDataPoints": List[SendDataPointTypeDef]}, total=False
)

_RequiredTemplateTypeDef = TypedDict("_RequiredTemplateTypeDef", {"TemplateName": str})
_OptionalTemplateTypeDef = TypedDict(
    "_OptionalTemplateTypeDef", {"SubjectPart": str, "TextPart": str, "HtmlPart": str}, total=False
)


class TemplateTypeDef(_RequiredTemplateTypeDef, _OptionalTemplateTypeDef):
    pass


GetTemplateResponseTypeDef = TypedDict(
    "GetTemplateResponseTypeDef", {"Template": TemplateTypeDef}, total=False
)

ListConfigurationSetsResponseTypeDef = TypedDict(
    "ListConfigurationSetsResponseTypeDef",
    {"ConfigurationSets": List[ConfigurationSetTypeDef], "NextToken": str},
    total=False,
)

CustomVerificationEmailTemplateTypeDef = TypedDict(
    "CustomVerificationEmailTemplateTypeDef",
    {
        "TemplateName": str,
        "FromEmailAddress": str,
        "TemplateSubject": str,
        "SuccessRedirectionURL": str,
        "FailureRedirectionURL": str,
    },
    total=False,
)

ListCustomVerificationEmailTemplatesResponseTypeDef = TypedDict(
    "ListCustomVerificationEmailTemplatesResponseTypeDef",
    {
        "CustomVerificationEmailTemplates": List[CustomVerificationEmailTemplateTypeDef],
        "NextToken": str,
    },
    total=False,
)

_RequiredListIdentitiesResponseTypeDef = TypedDict(
    "_RequiredListIdentitiesResponseTypeDef", {"Identities": List[str]}
)
_OptionalListIdentitiesResponseTypeDef = TypedDict(
    "_OptionalListIdentitiesResponseTypeDef", {"NextToken": str}, total=False
)


class ListIdentitiesResponseTypeDef(
    _RequiredListIdentitiesResponseTypeDef, _OptionalListIdentitiesResponseTypeDef
):
    pass


ListIdentityPoliciesResponseTypeDef = TypedDict(
    "ListIdentityPoliciesResponseTypeDef", {"PolicyNames": List[str]}
)

ReceiptIpFilterTypeDef = TypedDict(
    "ReceiptIpFilterTypeDef", {"Policy": Literal["Block", "Allow"], "Cidr": str}
)

ReceiptFilterTypeDef = TypedDict(
    "ReceiptFilterTypeDef", {"Name": str, "IpFilter": ReceiptIpFilterTypeDef}
)

ListReceiptFiltersResponseTypeDef = TypedDict(
    "ListReceiptFiltersResponseTypeDef", {"Filters": List[ReceiptFilterTypeDef]}, total=False
)

ListReceiptRuleSetsResponseTypeDef = TypedDict(
    "ListReceiptRuleSetsResponseTypeDef",
    {"RuleSets": List[ReceiptRuleSetMetadataTypeDef], "NextToken": str},
    total=False,
)

TemplateMetadataTypeDef = TypedDict(
    "TemplateMetadataTypeDef", {"Name": str, "CreatedTimestamp": datetime}, total=False
)

ListTemplatesResponseTypeDef = TypedDict(
    "ListTemplatesResponseTypeDef",
    {"TemplatesMetadata": List[TemplateMetadataTypeDef], "NextToken": str},
    total=False,
)

ListVerifiedEmailAddressesResponseTypeDef = TypedDict(
    "ListVerifiedEmailAddressesResponseTypeDef", {"VerifiedEmailAddresses": List[str]}, total=False
)

_RequiredMessageDsnTypeDef = TypedDict("_RequiredMessageDsnTypeDef", {"ReportingMta": str})
_OptionalMessageDsnTypeDef = TypedDict(
    "_OptionalMessageDsnTypeDef",
    {"ArrivalDate": datetime, "ExtensionFields": List[ExtensionFieldTypeDef]},
    total=False,
)


class MessageDsnTypeDef(_RequiredMessageDsnTypeDef, _OptionalMessageDsnTypeDef):
    pass


_RequiredContentTypeDef = TypedDict("_RequiredContentTypeDef", {"Data": str})
_OptionalContentTypeDef = TypedDict("_OptionalContentTypeDef", {"Charset": str}, total=False)


class ContentTypeDef(_RequiredContentTypeDef, _OptionalContentTypeDef):
    pass


BodyTypeDef = TypedDict(
    "BodyTypeDef", {"Text": ContentTypeDef, "Html": ContentTypeDef}, total=False
)

MessageTypeDef = TypedDict("MessageTypeDef", {"Subject": ContentTypeDef, "Body": BodyTypeDef})

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

RawMessageTypeDef = TypedDict("RawMessageTypeDef", {"Data": Union[bytes, IO]})

SendBounceResponseTypeDef = TypedDict("SendBounceResponseTypeDef", {"MessageId": str}, total=False)

BulkEmailDestinationStatusTypeDef = TypedDict(
    "BulkEmailDestinationStatusTypeDef",
    {
        "Status": Literal[
            "Success",
            "MessageRejected",
            "MailFromDomainNotVerified",
            "ConfigurationSetDoesNotExist",
            "TemplateDoesNotExist",
            "AccountSuspended",
            "AccountThrottled",
            "AccountDailyQuotaExceeded",
            "InvalidSendingPoolName",
            "AccountSendingPaused",
            "ConfigurationSetSendingPaused",
            "InvalidParameterValue",
            "TransientFailure",
            "Failed",
        ],
        "Error": str,
        "MessageId": str,
    },
    total=False,
)

SendBulkTemplatedEmailResponseTypeDef = TypedDict(
    "SendBulkTemplatedEmailResponseTypeDef", {"Status": List[BulkEmailDestinationStatusTypeDef]}
)

SendCustomVerificationEmailResponseTypeDef = TypedDict(
    "SendCustomVerificationEmailResponseTypeDef", {"MessageId": str}, total=False
)

SendEmailResponseTypeDef = TypedDict("SendEmailResponseTypeDef", {"MessageId": str})

SendRawEmailResponseTypeDef = TypedDict("SendRawEmailResponseTypeDef", {"MessageId": str})

SendTemplatedEmailResponseTypeDef = TypedDict(
    "SendTemplatedEmailResponseTypeDef", {"MessageId": str}
)

TestRenderTemplateResponseTypeDef = TypedDict(
    "TestRenderTemplateResponseTypeDef", {"RenderedTemplate": str}, total=False
)

VerifyDomainDkimResponseTypeDef = TypedDict(
    "VerifyDomainDkimResponseTypeDef", {"DkimTokens": List[str]}
)

VerifyDomainIdentityResponseTypeDef = TypedDict(
    "VerifyDomainIdentityResponseTypeDef", {"VerificationToken": str}
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
