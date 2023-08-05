"""
Main interface for pinpoint service type definitions.

Usage::

    from mypy_boto3.pinpoint.type_defs import ADMChannelRequestTypeDef

    data: ADMChannelRequestTypeDef = {...}
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
    "ADMChannelRequestTypeDef",
    "APNSChannelRequestTypeDef",
    "APNSSandboxChannelRequestTypeDef",
    "APNSVoipChannelRequestTypeDef",
    "APNSVoipSandboxChannelRequestTypeDef",
    "BaiduChannelRequestTypeDef",
    "ApplicationResponseTypeDef",
    "CreateAppResponseTypeDef",
    "CreateApplicationRequestTypeDef",
    "CampaignHookTypeDef",
    "CampaignLimitsTypeDef",
    "CampaignStateTypeDef",
    "CampaignEmailMessageTypeDef",
    "CampaignSmsMessageTypeDef",
    "MessageTypeDef",
    "MessageConfigurationTypeDef",
    "AttributeDimensionTypeDef",
    "MetricDimensionTypeDef",
    "SetDimensionTypeDef",
    "EventDimensionsTypeDef",
    "CampaignEventFilterTypeDef",
    "QuietTimeTypeDef",
    "ScheduleTypeDef",
    "TemplateTypeDef",
    "TemplateConfigurationTypeDef",
    "TreatmentResourceTypeDef",
    "CampaignResponseTypeDef",
    "CreateCampaignResponseTypeDef",
    "CreateTemplateMessageBodyTypeDef",
    "CreateEmailTemplateResponseTypeDef",
    "ExportJobResourceTypeDef",
    "ExportJobResponseTypeDef",
    "CreateExportJobResponseTypeDef",
    "ImportJobResourceTypeDef",
    "ImportJobResponseTypeDef",
    "CreateImportJobResponseTypeDef",
    "EventConditionTypeDef",
    "SegmentConditionTypeDef",
    "RecencyDimensionTypeDef",
    "SegmentBehaviorsTypeDef",
    "SegmentDemographicsTypeDef",
    "GPSCoordinatesTypeDef",
    "GPSPointDimensionTypeDef",
    "SegmentLocationTypeDef",
    "SegmentDimensionsTypeDef",
    "SimpleConditionTypeDef",
    "ConditionTypeDef",
    "WaitTimeTypeDef",
    "ConditionalSplitActivityTypeDef",
    "JourneyEmailMessageTypeDef",
    "EmailMessageActivityTypeDef",
    "HoldoutActivityTypeDef",
    "MultiConditionalBranchTypeDef",
    "MultiConditionalSplitActivityTypeDef",
    "RandomSplitEntryTypeDef",
    "RandomSplitActivityTypeDef",
    "WaitActivityTypeDef",
    "ActivityTypeDef",
    "JourneyLimitsTypeDef",
    "JourneyScheduleTypeDef",
    "StartConditionTypeDef",
    "JourneyResponseTypeDef",
    "CreateJourneyResponseTypeDef",
    "CreatePushTemplateResponseTypeDef",
    "RecommenderConfigurationResponseTypeDef",
    "CreateRecommenderConfigurationResponseTypeDef",
    "CreateRecommenderConfigurationTypeDef",
    "SegmentReferenceTypeDef",
    "SegmentGroupTypeDef",
    "SegmentGroupListTypeDef",
    "SegmentImportResourceTypeDef",
    "SegmentResponseTypeDef",
    "CreateSegmentResponseTypeDef",
    "CreateSmsTemplateResponseTypeDef",
    "CreateVoiceTemplateResponseTypeDef",
    "ADMChannelResponseTypeDef",
    "DeleteAdmChannelResponseTypeDef",
    "APNSChannelResponseTypeDef",
    "DeleteApnsChannelResponseTypeDef",
    "APNSSandboxChannelResponseTypeDef",
    "DeleteApnsSandboxChannelResponseTypeDef",
    "APNSVoipChannelResponseTypeDef",
    "DeleteApnsVoipChannelResponseTypeDef",
    "APNSVoipSandboxChannelResponseTypeDef",
    "DeleteApnsVoipSandboxChannelResponseTypeDef",
    "DeleteAppResponseTypeDef",
    "BaiduChannelResponseTypeDef",
    "DeleteBaiduChannelResponseTypeDef",
    "DeleteCampaignResponseTypeDef",
    "EmailChannelResponseTypeDef",
    "DeleteEmailChannelResponseTypeDef",
    "MessageBodyTypeDef",
    "DeleteEmailTemplateResponseTypeDef",
    "EndpointDemographicTypeDef",
    "EndpointLocationTypeDef",
    "EndpointUserTypeDef",
    "EndpointResponseTypeDef",
    "DeleteEndpointResponseTypeDef",
    "EventStreamTypeDef",
    "DeleteEventStreamResponseTypeDef",
    "GCMChannelResponseTypeDef",
    "DeleteGcmChannelResponseTypeDef",
    "DeleteJourneyResponseTypeDef",
    "DeletePushTemplateResponseTypeDef",
    "DeleteRecommenderConfigurationResponseTypeDef",
    "DeleteSegmentResponseTypeDef",
    "SMSChannelResponseTypeDef",
    "DeleteSmsChannelResponseTypeDef",
    "DeleteSmsTemplateResponseTypeDef",
    "EndpointsResponseTypeDef",
    "DeleteUserEndpointsResponseTypeDef",
    "VoiceChannelResponseTypeDef",
    "DeleteVoiceChannelResponseTypeDef",
    "DeleteVoiceTemplateResponseTypeDef",
    "EmailChannelRequestTypeDef",
    "EmailTemplateRequestTypeDef",
    "EndpointBatchItemTypeDef",
    "EndpointBatchRequestTypeDef",
    "EndpointRequestTypeDef",
    "SessionTypeDef",
    "EventTypeDef",
    "PublicEndpointTypeDef",
    "EventsBatchTypeDef",
    "EventsRequestTypeDef",
    "ExportJobRequestTypeDef",
    "GCMChannelRequestTypeDef",
    "GetAdmChannelResponseTypeDef",
    "GetApnsChannelResponseTypeDef",
    "GetApnsSandboxChannelResponseTypeDef",
    "GetApnsVoipChannelResponseTypeDef",
    "GetApnsVoipSandboxChannelResponseTypeDef",
    "GetAppResponseTypeDef",
    "ResultRowValueTypeDef",
    "ResultRowTypeDef",
    "BaseKpiResultTypeDef",
    "ApplicationDateRangeKpiResponseTypeDef",
    "GetApplicationDateRangeKpiResponseTypeDef",
    "ApplicationSettingsResourceTypeDef",
    "GetApplicationSettingsResponseTypeDef",
    "ApplicationsResponseTypeDef",
    "GetAppsResponseTypeDef",
    "GetBaiduChannelResponseTypeDef",
    "ActivityResponseTypeDef",
    "ActivitiesResponseTypeDef",
    "GetCampaignActivitiesResponseTypeDef",
    "CampaignDateRangeKpiResponseTypeDef",
    "GetCampaignDateRangeKpiResponseTypeDef",
    "GetCampaignResponseTypeDef",
    "GetCampaignVersionResponseTypeDef",
    "CampaignsResponseTypeDef",
    "GetCampaignVersionsResponseTypeDef",
    "GetCampaignsResponseTypeDef",
    "ChannelResponseTypeDef",
    "ChannelsResponseTypeDef",
    "GetChannelsResponseTypeDef",
    "GetEmailChannelResponseTypeDef",
    "EmailTemplateResponseTypeDef",
    "GetEmailTemplateResponseTypeDef",
    "GetEndpointResponseTypeDef",
    "GetEventStreamResponseTypeDef",
    "GetExportJobResponseTypeDef",
    "ExportJobsResponseTypeDef",
    "GetExportJobsResponseTypeDef",
    "GetGcmChannelResponseTypeDef",
    "GetImportJobResponseTypeDef",
    "ImportJobsResponseTypeDef",
    "GetImportJobsResponseTypeDef",
    "JourneyDateRangeKpiResponseTypeDef",
    "GetJourneyDateRangeKpiResponseTypeDef",
    "JourneyExecutionActivityMetricsResponseTypeDef",
    "GetJourneyExecutionActivityMetricsResponseTypeDef",
    "JourneyExecutionMetricsResponseTypeDef",
    "GetJourneyExecutionMetricsResponseTypeDef",
    "GetJourneyResponseTypeDef",
    "APNSPushNotificationTemplateTypeDef",
    "AndroidPushNotificationTemplateTypeDef",
    "DefaultPushNotificationTemplateTypeDef",
    "PushNotificationTemplateResponseTypeDef",
    "GetPushTemplateResponseTypeDef",
    "GetRecommenderConfigurationResponseTypeDef",
    "ListRecommenderConfigurationsResponseTypeDef",
    "GetRecommenderConfigurationsResponseTypeDef",
    "GetSegmentExportJobsResponseTypeDef",
    "GetSegmentImportJobsResponseTypeDef",
    "GetSegmentResponseTypeDef",
    "GetSegmentVersionResponseTypeDef",
    "SegmentsResponseTypeDef",
    "GetSegmentVersionsResponseTypeDef",
    "GetSegmentsResponseTypeDef",
    "GetSmsChannelResponseTypeDef",
    "SMSTemplateResponseTypeDef",
    "GetSmsTemplateResponseTypeDef",
    "GetUserEndpointsResponseTypeDef",
    "GetVoiceChannelResponseTypeDef",
    "VoiceTemplateResponseTypeDef",
    "GetVoiceTemplateResponseTypeDef",
    "ImportJobRequestTypeDef",
    "JourneyStateRequestTypeDef",
    "JourneysResponseTypeDef",
    "ListJourneysResponseTypeDef",
    "TagsModelTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TemplateVersionResponseTypeDef",
    "TemplateVersionsResponseTypeDef",
    "ListTemplateVersionsResponseTypeDef",
    "TemplateResponseTypeDef",
    "TemplatesResponseTypeDef",
    "ListTemplatesResponseTypeDef",
    "AddressConfigurationTypeDef",
    "ADMMessageTypeDef",
    "APNSMessageTypeDef",
    "BaiduMessageTypeDef",
    "DefaultMessageTypeDef",
    "DefaultPushNotificationMessageTypeDef",
    "RawEmailTypeDef",
    "SimpleEmailPartTypeDef",
    "SimpleEmailTypeDef",
    "EmailMessageTypeDef",
    "GCMMessageTypeDef",
    "SMSMessageTypeDef",
    "VoiceMessageTypeDef",
    "DirectMessageConfigurationTypeDef",
    "EndpointSendConfigurationTypeDef",
    "MessageRequestTypeDef",
    "NumberValidateRequestTypeDef",
    "NumberValidateResponseTypeDef",
    "PhoneNumberValidateResponseTypeDef",
    "PushNotificationTemplateRequestTypeDef",
    "PutEventStreamResponseTypeDef",
    "EndpointItemResponseTypeDef",
    "EventItemResponseTypeDef",
    "ItemResponseTypeDef",
    "EventsResponseTypeDef",
    "PutEventsResponseTypeDef",
    "AttributesResourceTypeDef",
    "RemoveAttributesResponseTypeDef",
    "SMSChannelRequestTypeDef",
    "SMSTemplateRequestTypeDef",
    "EndpointMessageResultTypeDef",
    "MessageResultTypeDef",
    "MessageResponseTypeDef",
    "SendMessagesResponseTypeDef",
    "SendUsersMessageRequestTypeDef",
    "SendUsersMessageResponseTypeDef",
    "SendUsersMessagesResponseTypeDef",
    "TemplateActiveVersionRequestTypeDef",
    "UpdateAdmChannelResponseTypeDef",
    "UpdateApnsChannelResponseTypeDef",
    "UpdateApnsSandboxChannelResponseTypeDef",
    "UpdateApnsVoipChannelResponseTypeDef",
    "UpdateApnsVoipSandboxChannelResponseTypeDef",
    "UpdateApplicationSettingsResponseTypeDef",
    "UpdateAttributesRequestTypeDef",
    "UpdateBaiduChannelResponseTypeDef",
    "UpdateCampaignResponseTypeDef",
    "UpdateEmailChannelResponseTypeDef",
    "UpdateEmailTemplateResponseTypeDef",
    "UpdateEndpointResponseTypeDef",
    "UpdateEndpointsBatchResponseTypeDef",
    "UpdateGcmChannelResponseTypeDef",
    "UpdateJourneyResponseTypeDef",
    "UpdateJourneyStateResponseTypeDef",
    "UpdatePushTemplateResponseTypeDef",
    "UpdateRecommenderConfigurationResponseTypeDef",
    "UpdateRecommenderConfigurationTypeDef",
    "UpdateSegmentResponseTypeDef",
    "UpdateSmsChannelResponseTypeDef",
    "UpdateSmsTemplateResponseTypeDef",
    "UpdateTemplateActiveVersionResponseTypeDef",
    "UpdateVoiceChannelResponseTypeDef",
    "UpdateVoiceTemplateResponseTypeDef",
    "VoiceChannelRequestTypeDef",
    "VoiceTemplateRequestTypeDef",
    "WriteApplicationSettingsRequestTypeDef",
    "WriteTreatmentResourceTypeDef",
    "WriteCampaignRequestTypeDef",
    "WriteEventStreamTypeDef",
    "WriteJourneyRequestTypeDef",
    "WriteSegmentRequestTypeDef",
)

_RequiredADMChannelRequestTypeDef = TypedDict(
    "_RequiredADMChannelRequestTypeDef", {"ClientId": str, "ClientSecret": str}
)
_OptionalADMChannelRequestTypeDef = TypedDict(
    "_OptionalADMChannelRequestTypeDef", {"Enabled": bool}, total=False
)


class ADMChannelRequestTypeDef(
    _RequiredADMChannelRequestTypeDef, _OptionalADMChannelRequestTypeDef
):
    pass


APNSChannelRequestTypeDef = TypedDict(
    "APNSChannelRequestTypeDef",
    {
        "BundleId": str,
        "Certificate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "PrivateKey": str,
        "TeamId": str,
        "TokenKey": str,
        "TokenKeyId": str,
    },
    total=False,
)

APNSSandboxChannelRequestTypeDef = TypedDict(
    "APNSSandboxChannelRequestTypeDef",
    {
        "BundleId": str,
        "Certificate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "PrivateKey": str,
        "TeamId": str,
        "TokenKey": str,
        "TokenKeyId": str,
    },
    total=False,
)

APNSVoipChannelRequestTypeDef = TypedDict(
    "APNSVoipChannelRequestTypeDef",
    {
        "BundleId": str,
        "Certificate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "PrivateKey": str,
        "TeamId": str,
        "TokenKey": str,
        "TokenKeyId": str,
    },
    total=False,
)

APNSVoipSandboxChannelRequestTypeDef = TypedDict(
    "APNSVoipSandboxChannelRequestTypeDef",
    {
        "BundleId": str,
        "Certificate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "PrivateKey": str,
        "TeamId": str,
        "TokenKey": str,
        "TokenKeyId": str,
    },
    total=False,
)

_RequiredBaiduChannelRequestTypeDef = TypedDict(
    "_RequiredBaiduChannelRequestTypeDef", {"ApiKey": str, "SecretKey": str}
)
_OptionalBaiduChannelRequestTypeDef = TypedDict(
    "_OptionalBaiduChannelRequestTypeDef", {"Enabled": bool}, total=False
)


class BaiduChannelRequestTypeDef(
    _RequiredBaiduChannelRequestTypeDef, _OptionalBaiduChannelRequestTypeDef
):
    pass


_RequiredApplicationResponseTypeDef = TypedDict(
    "_RequiredApplicationResponseTypeDef", {"Arn": str, "Id": str, "Name": str}
)
_OptionalApplicationResponseTypeDef = TypedDict(
    "_OptionalApplicationResponseTypeDef", {"tags": Dict[str, str]}, total=False
)


class ApplicationResponseTypeDef(
    _RequiredApplicationResponseTypeDef, _OptionalApplicationResponseTypeDef
):
    pass


CreateAppResponseTypeDef = TypedDict(
    "CreateAppResponseTypeDef", {"ApplicationResponse": ApplicationResponseTypeDef}
)

_RequiredCreateApplicationRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestTypeDef", {"Name": str}
)
_OptionalCreateApplicationRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestTypeDef", {"tags": Dict[str, str]}, total=False
)


class CreateApplicationRequestTypeDef(
    _RequiredCreateApplicationRequestTypeDef, _OptionalCreateApplicationRequestTypeDef
):
    pass


CampaignHookTypeDef = TypedDict(
    "CampaignHookTypeDef",
    {"LambdaFunctionName": str, "Mode": Literal["DELIVERY", "FILTER"], "WebUrl": str},
    total=False,
)

CampaignLimitsTypeDef = TypedDict(
    "CampaignLimitsTypeDef",
    {"Daily": int, "MaximumDuration": int, "MessagesPerSecond": int, "Total": int},
    total=False,
)

CampaignStateTypeDef = TypedDict(
    "CampaignStateTypeDef",
    {
        "CampaignStatus": Literal[
            "SCHEDULED", "EXECUTING", "PENDING_NEXT_RUN", "COMPLETED", "PAUSED", "DELETED"
        ]
    },
    total=False,
)

CampaignEmailMessageTypeDef = TypedDict(
    "CampaignEmailMessageTypeDef",
    {"Body": str, "FromAddress": str, "HtmlBody": str, "Title": str},
    total=False,
)

CampaignSmsMessageTypeDef = TypedDict(
    "CampaignSmsMessageTypeDef",
    {"Body": str, "MessageType": Literal["TRANSACTIONAL", "PROMOTIONAL"], "SenderId": str},
    total=False,
)

MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "Action": Literal["OPEN_APP", "DEEP_LINK", "URL"],
        "Body": str,
        "ImageIconUrl": str,
        "ImageSmallIconUrl": str,
        "ImageUrl": str,
        "JsonBody": str,
        "MediaUrl": str,
        "RawContent": str,
        "SilentPush": bool,
        "TimeToLive": int,
        "Title": str,
        "Url": str,
    },
    total=False,
)

MessageConfigurationTypeDef = TypedDict(
    "MessageConfigurationTypeDef",
    {
        "ADMMessage": MessageTypeDef,
        "APNSMessage": MessageTypeDef,
        "BaiduMessage": MessageTypeDef,
        "DefaultMessage": MessageTypeDef,
        "EmailMessage": CampaignEmailMessageTypeDef,
        "GCMMessage": MessageTypeDef,
        "SMSMessage": CampaignSmsMessageTypeDef,
    },
    total=False,
)

_RequiredAttributeDimensionTypeDef = TypedDict(
    "_RequiredAttributeDimensionTypeDef", {"Values": List[str]}
)
_OptionalAttributeDimensionTypeDef = TypedDict(
    "_OptionalAttributeDimensionTypeDef",
    {"AttributeType": Literal["INCLUSIVE", "EXCLUSIVE"]},
    total=False,
)


class AttributeDimensionTypeDef(
    _RequiredAttributeDimensionTypeDef, _OptionalAttributeDimensionTypeDef
):
    pass


MetricDimensionTypeDef = TypedDict(
    "MetricDimensionTypeDef", {"ComparisonOperator": str, "Value": float}
)

_RequiredSetDimensionTypeDef = TypedDict("_RequiredSetDimensionTypeDef", {"Values": List[str]})
_OptionalSetDimensionTypeDef = TypedDict(
    "_OptionalSetDimensionTypeDef",
    {"DimensionType": Literal["INCLUSIVE", "EXCLUSIVE"]},
    total=False,
)


class SetDimensionTypeDef(_RequiredSetDimensionTypeDef, _OptionalSetDimensionTypeDef):
    pass


EventDimensionsTypeDef = TypedDict(
    "EventDimensionsTypeDef",
    {
        "Attributes": Dict[str, AttributeDimensionTypeDef],
        "EventType": SetDimensionTypeDef,
        "Metrics": Dict[str, MetricDimensionTypeDef],
    },
    total=False,
)

CampaignEventFilterTypeDef = TypedDict(
    "CampaignEventFilterTypeDef",
    {"Dimensions": EventDimensionsTypeDef, "FilterType": Literal["SYSTEM", "ENDPOINT"]},
)

QuietTimeTypeDef = TypedDict("QuietTimeTypeDef", {"End": str, "Start": str}, total=False)

_RequiredScheduleTypeDef = TypedDict("_RequiredScheduleTypeDef", {"StartTime": str})
_OptionalScheduleTypeDef = TypedDict(
    "_OptionalScheduleTypeDef",
    {
        "EndTime": str,
        "EventFilter": CampaignEventFilterTypeDef,
        "Frequency": Literal["ONCE", "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "EVENT"],
        "IsLocalTime": bool,
        "QuietTime": QuietTimeTypeDef,
        "Timezone": str,
    },
    total=False,
)


class ScheduleTypeDef(_RequiredScheduleTypeDef, _OptionalScheduleTypeDef):
    pass


TemplateTypeDef = TypedDict("TemplateTypeDef", {"Name": str, "Version": str}, total=False)

TemplateConfigurationTypeDef = TypedDict(
    "TemplateConfigurationTypeDef",
    {
        "EmailTemplate": TemplateTypeDef,
        "PushTemplate": TemplateTypeDef,
        "SMSTemplate": TemplateTypeDef,
        "VoiceTemplate": TemplateTypeDef,
    },
    total=False,
)

_RequiredTreatmentResourceTypeDef = TypedDict(
    "_RequiredTreatmentResourceTypeDef", {"Id": str, "SizePercent": int}
)
_OptionalTreatmentResourceTypeDef = TypedDict(
    "_OptionalTreatmentResourceTypeDef",
    {
        "MessageConfiguration": MessageConfigurationTypeDef,
        "Schedule": ScheduleTypeDef,
        "State": CampaignStateTypeDef,
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TreatmentDescription": str,
        "TreatmentName": str,
    },
    total=False,
)


class TreatmentResourceTypeDef(
    _RequiredTreatmentResourceTypeDef, _OptionalTreatmentResourceTypeDef
):
    pass


_RequiredCampaignResponseTypeDef = TypedDict(
    "_RequiredCampaignResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreationDate": str,
        "Id": str,
        "LastModifiedDate": str,
        "SegmentId": str,
        "SegmentVersion": int,
    },
)
_OptionalCampaignResponseTypeDef = TypedDict(
    "_OptionalCampaignResponseTypeDef",
    {
        "AdditionalTreatments": List[TreatmentResourceTypeDef],
        "DefaultState": CampaignStateTypeDef,
        "Description": str,
        "HoldoutPercent": int,
        "Hook": CampaignHookTypeDef,
        "IsPaused": bool,
        "Limits": CampaignLimitsTypeDef,
        "MessageConfiguration": MessageConfigurationTypeDef,
        "Name": str,
        "Schedule": ScheduleTypeDef,
        "State": CampaignStateTypeDef,
        "tags": Dict[str, str],
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TreatmentDescription": str,
        "TreatmentName": str,
        "Version": int,
    },
    total=False,
)


class CampaignResponseTypeDef(_RequiredCampaignResponseTypeDef, _OptionalCampaignResponseTypeDef):
    pass


CreateCampaignResponseTypeDef = TypedDict(
    "CreateCampaignResponseTypeDef", {"CampaignResponse": CampaignResponseTypeDef}
)

CreateTemplateMessageBodyTypeDef = TypedDict(
    "CreateTemplateMessageBodyTypeDef", {"Arn": str, "Message": str, "RequestID": str}, total=False
)

CreateEmailTemplateResponseTypeDef = TypedDict(
    "CreateEmailTemplateResponseTypeDef",
    {"CreateTemplateMessageBody": CreateTemplateMessageBodyTypeDef},
)

_RequiredExportJobResourceTypeDef = TypedDict(
    "_RequiredExportJobResourceTypeDef", {"RoleArn": str, "S3UrlPrefix": str}
)
_OptionalExportJobResourceTypeDef = TypedDict(
    "_OptionalExportJobResourceTypeDef", {"SegmentId": str, "SegmentVersion": int}, total=False
)


class ExportJobResourceTypeDef(
    _RequiredExportJobResourceTypeDef, _OptionalExportJobResourceTypeDef
):
    pass


_RequiredExportJobResponseTypeDef = TypedDict(
    "_RequiredExportJobResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Definition": ExportJobResourceTypeDef,
        "Id": str,
        "JobStatus": Literal[
            "CREATED",
            "PREPARING_FOR_INITIALIZATION",
            "INITIALIZING",
            "PROCESSING",
            "PENDING_JOB",
            "COMPLETING",
            "COMPLETED",
            "FAILING",
            "FAILED",
        ],
        "Type": str,
    },
)
_OptionalExportJobResponseTypeDef = TypedDict(
    "_OptionalExportJobResponseTypeDef",
    {
        "CompletedPieces": int,
        "CompletionDate": str,
        "FailedPieces": int,
        "Failures": List[str],
        "TotalFailures": int,
        "TotalPieces": int,
        "TotalProcessed": int,
    },
    total=False,
)


class ExportJobResponseTypeDef(
    _RequiredExportJobResponseTypeDef, _OptionalExportJobResponseTypeDef
):
    pass


CreateExportJobResponseTypeDef = TypedDict(
    "CreateExportJobResponseTypeDef", {"ExportJobResponse": ExportJobResponseTypeDef}
)

_RequiredImportJobResourceTypeDef = TypedDict(
    "_RequiredImportJobResourceTypeDef",
    {"Format": Literal["CSV", "JSON"], "RoleArn": str, "S3Url": str},
)
_OptionalImportJobResourceTypeDef = TypedDict(
    "_OptionalImportJobResourceTypeDef",
    {
        "DefineSegment": bool,
        "ExternalId": str,
        "RegisterEndpoints": bool,
        "SegmentId": str,
        "SegmentName": str,
    },
    total=False,
)


class ImportJobResourceTypeDef(
    _RequiredImportJobResourceTypeDef, _OptionalImportJobResourceTypeDef
):
    pass


_RequiredImportJobResponseTypeDef = TypedDict(
    "_RequiredImportJobResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Definition": ImportJobResourceTypeDef,
        "Id": str,
        "JobStatus": Literal[
            "CREATED",
            "PREPARING_FOR_INITIALIZATION",
            "INITIALIZING",
            "PROCESSING",
            "PENDING_JOB",
            "COMPLETING",
            "COMPLETED",
            "FAILING",
            "FAILED",
        ],
        "Type": str,
    },
)
_OptionalImportJobResponseTypeDef = TypedDict(
    "_OptionalImportJobResponseTypeDef",
    {
        "CompletedPieces": int,
        "CompletionDate": str,
        "FailedPieces": int,
        "Failures": List[str],
        "TotalFailures": int,
        "TotalPieces": int,
        "TotalProcessed": int,
    },
    total=False,
)


class ImportJobResponseTypeDef(
    _RequiredImportJobResponseTypeDef, _OptionalImportJobResponseTypeDef
):
    pass


CreateImportJobResponseTypeDef = TypedDict(
    "CreateImportJobResponseTypeDef", {"ImportJobResponse": ImportJobResponseTypeDef}
)

_RequiredEventConditionTypeDef = TypedDict(
    "_RequiredEventConditionTypeDef", {"Dimensions": EventDimensionsTypeDef}
)
_OptionalEventConditionTypeDef = TypedDict(
    "_OptionalEventConditionTypeDef", {"MessageActivity": str}, total=False
)


class EventConditionTypeDef(_RequiredEventConditionTypeDef, _OptionalEventConditionTypeDef):
    pass


SegmentConditionTypeDef = TypedDict("SegmentConditionTypeDef", {"SegmentId": str})

RecencyDimensionTypeDef = TypedDict(
    "RecencyDimensionTypeDef",
    {
        "Duration": Literal["HR_24", "DAY_7", "DAY_14", "DAY_30"],
        "RecencyType": Literal["ACTIVE", "INACTIVE"],
    },
)

SegmentBehaviorsTypeDef = TypedDict(
    "SegmentBehaviorsTypeDef", {"Recency": RecencyDimensionTypeDef}, total=False
)

SegmentDemographicsTypeDef = TypedDict(
    "SegmentDemographicsTypeDef",
    {
        "AppVersion": SetDimensionTypeDef,
        "Channel": SetDimensionTypeDef,
        "DeviceType": SetDimensionTypeDef,
        "Make": SetDimensionTypeDef,
        "Model": SetDimensionTypeDef,
        "Platform": SetDimensionTypeDef,
    },
    total=False,
)

GPSCoordinatesTypeDef = TypedDict("GPSCoordinatesTypeDef", {"Latitude": float, "Longitude": float})

_RequiredGPSPointDimensionTypeDef = TypedDict(
    "_RequiredGPSPointDimensionTypeDef", {"Coordinates": GPSCoordinatesTypeDef}
)
_OptionalGPSPointDimensionTypeDef = TypedDict(
    "_OptionalGPSPointDimensionTypeDef", {"RangeInKilometers": float}, total=False
)


class GPSPointDimensionTypeDef(
    _RequiredGPSPointDimensionTypeDef, _OptionalGPSPointDimensionTypeDef
):
    pass


SegmentLocationTypeDef = TypedDict(
    "SegmentLocationTypeDef",
    {"Country": SetDimensionTypeDef, "GPSPoint": GPSPointDimensionTypeDef},
    total=False,
)

SegmentDimensionsTypeDef = TypedDict(
    "SegmentDimensionsTypeDef",
    {
        "Attributes": Dict[str, AttributeDimensionTypeDef],
        "Behavior": SegmentBehaviorsTypeDef,
        "Demographic": SegmentDemographicsTypeDef,
        "Location": SegmentLocationTypeDef,
        "Metrics": Dict[str, MetricDimensionTypeDef],
        "UserAttributes": Dict[str, AttributeDimensionTypeDef],
    },
    total=False,
)

SimpleConditionTypeDef = TypedDict(
    "SimpleConditionTypeDef",
    {
        "EventCondition": EventConditionTypeDef,
        "SegmentCondition": SegmentConditionTypeDef,
        "SegmentDimensions": SegmentDimensionsTypeDef,
    },
    total=False,
)

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {"Conditions": List[SimpleConditionTypeDef], "Operator": Literal["ALL", "ANY"]},
    total=False,
)

WaitTimeTypeDef = TypedDict("WaitTimeTypeDef", {"WaitFor": str, "WaitUntil": str}, total=False)

ConditionalSplitActivityTypeDef = TypedDict(
    "ConditionalSplitActivityTypeDef",
    {
        "Condition": ConditionTypeDef,
        "EvaluationWaitTime": WaitTimeTypeDef,
        "FalseActivity": str,
        "TrueActivity": str,
    },
    total=False,
)

JourneyEmailMessageTypeDef = TypedDict(
    "JourneyEmailMessageTypeDef", {"FromAddress": str}, total=False
)

EmailMessageActivityTypeDef = TypedDict(
    "EmailMessageActivityTypeDef",
    {
        "MessageConfig": JourneyEmailMessageTypeDef,
        "NextActivity": str,
        "TemplateName": str,
        "TemplateVersion": str,
    },
    total=False,
)

_RequiredHoldoutActivityTypeDef = TypedDict("_RequiredHoldoutActivityTypeDef", {"Percentage": int})
_OptionalHoldoutActivityTypeDef = TypedDict(
    "_OptionalHoldoutActivityTypeDef", {"NextActivity": str}, total=False
)


class HoldoutActivityTypeDef(_RequiredHoldoutActivityTypeDef, _OptionalHoldoutActivityTypeDef):
    pass


MultiConditionalBranchTypeDef = TypedDict(
    "MultiConditionalBranchTypeDef",
    {"Condition": SimpleConditionTypeDef, "NextActivity": str},
    total=False,
)

MultiConditionalSplitActivityTypeDef = TypedDict(
    "MultiConditionalSplitActivityTypeDef",
    {
        "Branches": List[MultiConditionalBranchTypeDef],
        "DefaultActivity": str,
        "EvaluationWaitTime": WaitTimeTypeDef,
    },
    total=False,
)

RandomSplitEntryTypeDef = TypedDict(
    "RandomSplitEntryTypeDef", {"NextActivity": str, "Percentage": int}, total=False
)

RandomSplitActivityTypeDef = TypedDict(
    "RandomSplitActivityTypeDef", {"Branches": List[RandomSplitEntryTypeDef]}, total=False
)

WaitActivityTypeDef = TypedDict(
    "WaitActivityTypeDef", {"NextActivity": str, "WaitTime": WaitTimeTypeDef}, total=False
)

ActivityTypeDef = TypedDict(
    "ActivityTypeDef",
    {
        "ConditionalSplit": ConditionalSplitActivityTypeDef,
        "Description": str,
        "EMAIL": EmailMessageActivityTypeDef,
        "Holdout": HoldoutActivityTypeDef,
        "MultiCondition": MultiConditionalSplitActivityTypeDef,
        "RandomSplit": RandomSplitActivityTypeDef,
        "Wait": WaitActivityTypeDef,
    },
    total=False,
)

JourneyLimitsTypeDef = TypedDict(
    "JourneyLimitsTypeDef",
    {"DailyCap": int, "EndpointReentryCap": int, "MessagesPerSecond": int},
    total=False,
)

JourneyScheduleTypeDef = TypedDict(
    "JourneyScheduleTypeDef",
    {"EndTime": datetime, "StartTime": datetime, "Timezone": str},
    total=False,
)

StartConditionTypeDef = TypedDict(
    "StartConditionTypeDef",
    {"Description": str, "SegmentStartCondition": SegmentConditionTypeDef},
    total=False,
)

_RequiredJourneyResponseTypeDef = TypedDict(
    "_RequiredJourneyResponseTypeDef", {"ApplicationId": str, "Id": str, "Name": str}
)
_OptionalJourneyResponseTypeDef = TypedDict(
    "_OptionalJourneyResponseTypeDef",
    {
        "Activities": Dict[str, ActivityTypeDef],
        "CreationDate": str,
        "LastModifiedDate": str,
        "Limits": JourneyLimitsTypeDef,
        "LocalTime": bool,
        "QuietTime": QuietTimeTypeDef,
        "RefreshFrequency": str,
        "Schedule": JourneyScheduleTypeDef,
        "StartActivity": str,
        "StartCondition": StartConditionTypeDef,
        "State": Literal["DRAFT", "ACTIVE", "COMPLETED", "CANCELLED", "CLOSED"],
        "tags": Dict[str, str],
    },
    total=False,
)


class JourneyResponseTypeDef(_RequiredJourneyResponseTypeDef, _OptionalJourneyResponseTypeDef):
    pass


CreateJourneyResponseTypeDef = TypedDict(
    "CreateJourneyResponseTypeDef", {"JourneyResponse": JourneyResponseTypeDef}
)

CreatePushTemplateResponseTypeDef = TypedDict(
    "CreatePushTemplateResponseTypeDef",
    {"CreateTemplateMessageBody": CreateTemplateMessageBodyTypeDef},
)

_RequiredRecommenderConfigurationResponseTypeDef = TypedDict(
    "_RequiredRecommenderConfigurationResponseTypeDef",
    {
        "CreationDate": str,
        "Id": str,
        "LastModifiedDate": str,
        "RecommendationProviderRoleArn": str,
        "RecommendationProviderUri": str,
    },
)
_OptionalRecommenderConfigurationResponseTypeDef = TypedDict(
    "_OptionalRecommenderConfigurationResponseTypeDef",
    {
        "Attributes": Dict[str, str],
        "Description": str,
        "Name": str,
        "RecommendationProviderIdType": str,
        "RecommendationTransformerUri": str,
        "RecommendationsDisplayName": str,
        "RecommendationsPerMessage": int,
    },
    total=False,
)


class RecommenderConfigurationResponseTypeDef(
    _RequiredRecommenderConfigurationResponseTypeDef,
    _OptionalRecommenderConfigurationResponseTypeDef,
):
    pass


CreateRecommenderConfigurationResponseTypeDef = TypedDict(
    "CreateRecommenderConfigurationResponseTypeDef",
    {"RecommenderConfigurationResponse": RecommenderConfigurationResponseTypeDef},
)

_RequiredCreateRecommenderConfigurationTypeDef = TypedDict(
    "_RequiredCreateRecommenderConfigurationTypeDef",
    {"RecommendationProviderRoleArn": str, "RecommendationProviderUri": str},
)
_OptionalCreateRecommenderConfigurationTypeDef = TypedDict(
    "_OptionalCreateRecommenderConfigurationTypeDef",
    {
        "Attributes": Dict[str, str],
        "Description": str,
        "Name": str,
        "RecommendationProviderIdType": str,
        "RecommendationTransformerUri": str,
        "RecommendationsDisplayName": str,
        "RecommendationsPerMessage": int,
    },
    total=False,
)


class CreateRecommenderConfigurationTypeDef(
    _RequiredCreateRecommenderConfigurationTypeDef, _OptionalCreateRecommenderConfigurationTypeDef
):
    pass


_RequiredSegmentReferenceTypeDef = TypedDict("_RequiredSegmentReferenceTypeDef", {"Id": str})
_OptionalSegmentReferenceTypeDef = TypedDict(
    "_OptionalSegmentReferenceTypeDef", {"Version": int}, total=False
)


class SegmentReferenceTypeDef(_RequiredSegmentReferenceTypeDef, _OptionalSegmentReferenceTypeDef):
    pass


SegmentGroupTypeDef = TypedDict(
    "SegmentGroupTypeDef",
    {
        "Dimensions": List[SegmentDimensionsTypeDef],
        "SourceSegments": List[SegmentReferenceTypeDef],
        "SourceType": Literal["ALL", "ANY", "NONE"],
        "Type": Literal["ALL", "ANY", "NONE"],
    },
    total=False,
)

SegmentGroupListTypeDef = TypedDict(
    "SegmentGroupListTypeDef",
    {"Groups": List[SegmentGroupTypeDef], "Include": Literal["ALL", "ANY", "NONE"]},
    total=False,
)

_RequiredSegmentImportResourceTypeDef = TypedDict(
    "_RequiredSegmentImportResourceTypeDef",
    {
        "ExternalId": str,
        "Format": Literal["CSV", "JSON"],
        "RoleArn": str,
        "S3Url": str,
        "Size": int,
    },
)
_OptionalSegmentImportResourceTypeDef = TypedDict(
    "_OptionalSegmentImportResourceTypeDef", {"ChannelCounts": Dict[str, int]}, total=False
)


class SegmentImportResourceTypeDef(
    _RequiredSegmentImportResourceTypeDef, _OptionalSegmentImportResourceTypeDef
):
    pass


_RequiredSegmentResponseTypeDef = TypedDict(
    "_RequiredSegmentResponseTypeDef",
    {
        "ApplicationId": str,
        "Arn": str,
        "CreationDate": str,
        "Id": str,
        "SegmentType": Literal["DIMENSIONAL", "IMPORT"],
    },
)
_OptionalSegmentResponseTypeDef = TypedDict(
    "_OptionalSegmentResponseTypeDef",
    {
        "Dimensions": SegmentDimensionsTypeDef,
        "ImportDefinition": SegmentImportResourceTypeDef,
        "LastModifiedDate": str,
        "Name": str,
        "SegmentGroups": SegmentGroupListTypeDef,
        "tags": Dict[str, str],
        "Version": int,
    },
    total=False,
)


class SegmentResponseTypeDef(_RequiredSegmentResponseTypeDef, _OptionalSegmentResponseTypeDef):
    pass


CreateSegmentResponseTypeDef = TypedDict(
    "CreateSegmentResponseTypeDef", {"SegmentResponse": SegmentResponseTypeDef}
)

CreateSmsTemplateResponseTypeDef = TypedDict(
    "CreateSmsTemplateResponseTypeDef",
    {"CreateTemplateMessageBody": CreateTemplateMessageBodyTypeDef},
)

CreateVoiceTemplateResponseTypeDef = TypedDict(
    "CreateVoiceTemplateResponseTypeDef",
    {"CreateTemplateMessageBody": CreateTemplateMessageBodyTypeDef},
)

_RequiredADMChannelResponseTypeDef = TypedDict(
    "_RequiredADMChannelResponseTypeDef", {"Platform": str}
)
_OptionalADMChannelResponseTypeDef = TypedDict(
    "_OptionalADMChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class ADMChannelResponseTypeDef(
    _RequiredADMChannelResponseTypeDef, _OptionalADMChannelResponseTypeDef
):
    pass


DeleteAdmChannelResponseTypeDef = TypedDict(
    "DeleteAdmChannelResponseTypeDef", {"ADMChannelResponse": ADMChannelResponseTypeDef}
)

_RequiredAPNSChannelResponseTypeDef = TypedDict(
    "_RequiredAPNSChannelResponseTypeDef", {"Platform": str}
)
_OptionalAPNSChannelResponseTypeDef = TypedDict(
    "_OptionalAPNSChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "HasCredential": bool,
        "HasTokenKey": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class APNSChannelResponseTypeDef(
    _RequiredAPNSChannelResponseTypeDef, _OptionalAPNSChannelResponseTypeDef
):
    pass


DeleteApnsChannelResponseTypeDef = TypedDict(
    "DeleteApnsChannelResponseTypeDef", {"APNSChannelResponse": APNSChannelResponseTypeDef}
)

_RequiredAPNSSandboxChannelResponseTypeDef = TypedDict(
    "_RequiredAPNSSandboxChannelResponseTypeDef", {"Platform": str}
)
_OptionalAPNSSandboxChannelResponseTypeDef = TypedDict(
    "_OptionalAPNSSandboxChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "HasCredential": bool,
        "HasTokenKey": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class APNSSandboxChannelResponseTypeDef(
    _RequiredAPNSSandboxChannelResponseTypeDef, _OptionalAPNSSandboxChannelResponseTypeDef
):
    pass


DeleteApnsSandboxChannelResponseTypeDef = TypedDict(
    "DeleteApnsSandboxChannelResponseTypeDef",
    {"APNSSandboxChannelResponse": APNSSandboxChannelResponseTypeDef},
)

_RequiredAPNSVoipChannelResponseTypeDef = TypedDict(
    "_RequiredAPNSVoipChannelResponseTypeDef", {"Platform": str}
)
_OptionalAPNSVoipChannelResponseTypeDef = TypedDict(
    "_OptionalAPNSVoipChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "HasCredential": bool,
        "HasTokenKey": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class APNSVoipChannelResponseTypeDef(
    _RequiredAPNSVoipChannelResponseTypeDef, _OptionalAPNSVoipChannelResponseTypeDef
):
    pass


DeleteApnsVoipChannelResponseTypeDef = TypedDict(
    "DeleteApnsVoipChannelResponseTypeDef",
    {"APNSVoipChannelResponse": APNSVoipChannelResponseTypeDef},
)

_RequiredAPNSVoipSandboxChannelResponseTypeDef = TypedDict(
    "_RequiredAPNSVoipSandboxChannelResponseTypeDef", {"Platform": str}
)
_OptionalAPNSVoipSandboxChannelResponseTypeDef = TypedDict(
    "_OptionalAPNSVoipSandboxChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "DefaultAuthenticationMethod": str,
        "Enabled": bool,
        "HasCredential": bool,
        "HasTokenKey": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class APNSVoipSandboxChannelResponseTypeDef(
    _RequiredAPNSVoipSandboxChannelResponseTypeDef, _OptionalAPNSVoipSandboxChannelResponseTypeDef
):
    pass


DeleteApnsVoipSandboxChannelResponseTypeDef = TypedDict(
    "DeleteApnsVoipSandboxChannelResponseTypeDef",
    {"APNSVoipSandboxChannelResponse": APNSVoipSandboxChannelResponseTypeDef},
)

DeleteAppResponseTypeDef = TypedDict(
    "DeleteAppResponseTypeDef", {"ApplicationResponse": ApplicationResponseTypeDef}
)

_RequiredBaiduChannelResponseTypeDef = TypedDict(
    "_RequiredBaiduChannelResponseTypeDef", {"Credential": str, "Platform": str}
)
_OptionalBaiduChannelResponseTypeDef = TypedDict(
    "_OptionalBaiduChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class BaiduChannelResponseTypeDef(
    _RequiredBaiduChannelResponseTypeDef, _OptionalBaiduChannelResponseTypeDef
):
    pass


DeleteBaiduChannelResponseTypeDef = TypedDict(
    "DeleteBaiduChannelResponseTypeDef", {"BaiduChannelResponse": BaiduChannelResponseTypeDef}
)

DeleteCampaignResponseTypeDef = TypedDict(
    "DeleteCampaignResponseTypeDef", {"CampaignResponse": CampaignResponseTypeDef}
)

_RequiredEmailChannelResponseTypeDef = TypedDict(
    "_RequiredEmailChannelResponseTypeDef", {"Platform": str}
)
_OptionalEmailChannelResponseTypeDef = TypedDict(
    "_OptionalEmailChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "ConfigurationSet": str,
        "CreationDate": str,
        "Enabled": bool,
        "FromAddress": str,
        "HasCredential": bool,
        "Id": str,
        "Identity": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "MessagesPerSecond": int,
        "RoleArn": str,
        "Version": int,
    },
    total=False,
)


class EmailChannelResponseTypeDef(
    _RequiredEmailChannelResponseTypeDef, _OptionalEmailChannelResponseTypeDef
):
    pass


DeleteEmailChannelResponseTypeDef = TypedDict(
    "DeleteEmailChannelResponseTypeDef", {"EmailChannelResponse": EmailChannelResponseTypeDef}
)

MessageBodyTypeDef = TypedDict(
    "MessageBodyTypeDef", {"Message": str, "RequestID": str}, total=False
)

DeleteEmailTemplateResponseTypeDef = TypedDict(
    "DeleteEmailTemplateResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

EndpointDemographicTypeDef = TypedDict(
    "EndpointDemographicTypeDef",
    {
        "AppVersion": str,
        "Locale": str,
        "Make": str,
        "Model": str,
        "ModelVersion": str,
        "Platform": str,
        "PlatformVersion": str,
        "Timezone": str,
    },
    total=False,
)

EndpointLocationTypeDef = TypedDict(
    "EndpointLocationTypeDef",
    {
        "City": str,
        "Country": str,
        "Latitude": float,
        "Longitude": float,
        "PostalCode": str,
        "Region": str,
    },
    total=False,
)

EndpointUserTypeDef = TypedDict(
    "EndpointUserTypeDef", {"UserAttributes": Dict[str, List[str]], "UserId": str}, total=False
)

EndpointResponseTypeDef = TypedDict(
    "EndpointResponseTypeDef",
    {
        "Address": str,
        "ApplicationId": str,
        "Attributes": Dict[str, List[str]],
        "ChannelType": Literal[
            "GCM",
            "APNS",
            "APNS_SANDBOX",
            "APNS_VOIP",
            "APNS_VOIP_SANDBOX",
            "ADM",
            "SMS",
            "VOICE",
            "EMAIL",
            "BAIDU",
            "CUSTOM",
        ],
        "CohortId": str,
        "CreationDate": str,
        "Demographic": EndpointDemographicTypeDef,
        "EffectiveDate": str,
        "EndpointStatus": str,
        "Id": str,
        "Location": EndpointLocationTypeDef,
        "Metrics": Dict[str, float],
        "OptOut": str,
        "RequestId": str,
        "User": EndpointUserTypeDef,
    },
    total=False,
)

DeleteEndpointResponseTypeDef = TypedDict(
    "DeleteEndpointResponseTypeDef", {"EndpointResponse": EndpointResponseTypeDef}
)

_RequiredEventStreamTypeDef = TypedDict(
    "_RequiredEventStreamTypeDef",
    {"ApplicationId": str, "DestinationStreamArn": str, "RoleArn": str},
)
_OptionalEventStreamTypeDef = TypedDict(
    "_OptionalEventStreamTypeDef",
    {"ExternalId": str, "LastModifiedDate": str, "LastUpdatedBy": str},
    total=False,
)


class EventStreamTypeDef(_RequiredEventStreamTypeDef, _OptionalEventStreamTypeDef):
    pass


DeleteEventStreamResponseTypeDef = TypedDict(
    "DeleteEventStreamResponseTypeDef", {"EventStream": EventStreamTypeDef}
)

_RequiredGCMChannelResponseTypeDef = TypedDict(
    "_RequiredGCMChannelResponseTypeDef", {"Credential": str, "Platform": str}
)
_OptionalGCMChannelResponseTypeDef = TypedDict(
    "_OptionalGCMChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class GCMChannelResponseTypeDef(
    _RequiredGCMChannelResponseTypeDef, _OptionalGCMChannelResponseTypeDef
):
    pass


DeleteGcmChannelResponseTypeDef = TypedDict(
    "DeleteGcmChannelResponseTypeDef", {"GCMChannelResponse": GCMChannelResponseTypeDef}
)

DeleteJourneyResponseTypeDef = TypedDict(
    "DeleteJourneyResponseTypeDef", {"JourneyResponse": JourneyResponseTypeDef}
)

DeletePushTemplateResponseTypeDef = TypedDict(
    "DeletePushTemplateResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

DeleteRecommenderConfigurationResponseTypeDef = TypedDict(
    "DeleteRecommenderConfigurationResponseTypeDef",
    {"RecommenderConfigurationResponse": RecommenderConfigurationResponseTypeDef},
)

DeleteSegmentResponseTypeDef = TypedDict(
    "DeleteSegmentResponseTypeDef", {"SegmentResponse": SegmentResponseTypeDef}
)

_RequiredSMSChannelResponseTypeDef = TypedDict(
    "_RequiredSMSChannelResponseTypeDef", {"Platform": str}
)
_OptionalSMSChannelResponseTypeDef = TypedDict(
    "_OptionalSMSChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "PromotionalMessagesPerSecond": int,
        "SenderId": str,
        "ShortCode": str,
        "TransactionalMessagesPerSecond": int,
        "Version": int,
    },
    total=False,
)


class SMSChannelResponseTypeDef(
    _RequiredSMSChannelResponseTypeDef, _OptionalSMSChannelResponseTypeDef
):
    pass


DeleteSmsChannelResponseTypeDef = TypedDict(
    "DeleteSmsChannelResponseTypeDef", {"SMSChannelResponse": SMSChannelResponseTypeDef}
)

DeleteSmsTemplateResponseTypeDef = TypedDict(
    "DeleteSmsTemplateResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

EndpointsResponseTypeDef = TypedDict(
    "EndpointsResponseTypeDef", {"Item": List[EndpointResponseTypeDef]}
)

DeleteUserEndpointsResponseTypeDef = TypedDict(
    "DeleteUserEndpointsResponseTypeDef", {"EndpointsResponse": EndpointsResponseTypeDef}
)

_RequiredVoiceChannelResponseTypeDef = TypedDict(
    "_RequiredVoiceChannelResponseTypeDef", {"Platform": str}
)
_OptionalVoiceChannelResponseTypeDef = TypedDict(
    "_OptionalVoiceChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)


class VoiceChannelResponseTypeDef(
    _RequiredVoiceChannelResponseTypeDef, _OptionalVoiceChannelResponseTypeDef
):
    pass


DeleteVoiceChannelResponseTypeDef = TypedDict(
    "DeleteVoiceChannelResponseTypeDef", {"VoiceChannelResponse": VoiceChannelResponseTypeDef}
)

DeleteVoiceTemplateResponseTypeDef = TypedDict(
    "DeleteVoiceTemplateResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

_RequiredEmailChannelRequestTypeDef = TypedDict(
    "_RequiredEmailChannelRequestTypeDef", {"FromAddress": str, "Identity": str}
)
_OptionalEmailChannelRequestTypeDef = TypedDict(
    "_OptionalEmailChannelRequestTypeDef",
    {"ConfigurationSet": str, "Enabled": bool, "RoleArn": str},
    total=False,
)


class EmailChannelRequestTypeDef(
    _RequiredEmailChannelRequestTypeDef, _OptionalEmailChannelRequestTypeDef
):
    pass


EmailTemplateRequestTypeDef = TypedDict(
    "EmailTemplateRequestTypeDef",
    {
        "DefaultSubstitutions": str,
        "HtmlPart": str,
        "RecommenderId": str,
        "Subject": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "TextPart": str,
    },
    total=False,
)

EndpointBatchItemTypeDef = TypedDict(
    "EndpointBatchItemTypeDef",
    {
        "Address": str,
        "Attributes": Dict[str, List[str]],
        "ChannelType": Literal[
            "GCM",
            "APNS",
            "APNS_SANDBOX",
            "APNS_VOIP",
            "APNS_VOIP_SANDBOX",
            "ADM",
            "SMS",
            "VOICE",
            "EMAIL",
            "BAIDU",
            "CUSTOM",
        ],
        "Demographic": EndpointDemographicTypeDef,
        "EffectiveDate": str,
        "EndpointStatus": str,
        "Id": str,
        "Location": EndpointLocationTypeDef,
        "Metrics": Dict[str, float],
        "OptOut": str,
        "RequestId": str,
        "User": EndpointUserTypeDef,
    },
    total=False,
)

EndpointBatchRequestTypeDef = TypedDict(
    "EndpointBatchRequestTypeDef", {"Item": List[EndpointBatchItemTypeDef]}
)

EndpointRequestTypeDef = TypedDict(
    "EndpointRequestTypeDef",
    {
        "Address": str,
        "Attributes": Dict[str, List[str]],
        "ChannelType": Literal[
            "GCM",
            "APNS",
            "APNS_SANDBOX",
            "APNS_VOIP",
            "APNS_VOIP_SANDBOX",
            "ADM",
            "SMS",
            "VOICE",
            "EMAIL",
            "BAIDU",
            "CUSTOM",
        ],
        "Demographic": EndpointDemographicTypeDef,
        "EffectiveDate": str,
        "EndpointStatus": str,
        "Location": EndpointLocationTypeDef,
        "Metrics": Dict[str, float],
        "OptOut": str,
        "RequestId": str,
        "User": EndpointUserTypeDef,
    },
    total=False,
)

_RequiredSessionTypeDef = TypedDict("_RequiredSessionTypeDef", {"Id": str, "StartTimestamp": str})
_OptionalSessionTypeDef = TypedDict(
    "_OptionalSessionTypeDef", {"Duration": int, "StopTimestamp": str}, total=False
)


class SessionTypeDef(_RequiredSessionTypeDef, _OptionalSessionTypeDef):
    pass


_RequiredEventTypeDef = TypedDict("_RequiredEventTypeDef", {"EventType": str, "Timestamp": str})
_OptionalEventTypeDef = TypedDict(
    "_OptionalEventTypeDef",
    {
        "AppPackageName": str,
        "AppTitle": str,
        "AppVersionCode": str,
        "Attributes": Dict[str, str],
        "ClientSdkVersion": str,
        "Metrics": Dict[str, float],
        "SdkName": str,
        "Session": SessionTypeDef,
    },
    total=False,
)


class EventTypeDef(_RequiredEventTypeDef, _OptionalEventTypeDef):
    pass


PublicEndpointTypeDef = TypedDict(
    "PublicEndpointTypeDef",
    {
        "Address": str,
        "Attributes": Dict[str, List[str]],
        "ChannelType": Literal[
            "GCM",
            "APNS",
            "APNS_SANDBOX",
            "APNS_VOIP",
            "APNS_VOIP_SANDBOX",
            "ADM",
            "SMS",
            "VOICE",
            "EMAIL",
            "BAIDU",
            "CUSTOM",
        ],
        "Demographic": EndpointDemographicTypeDef,
        "EffectiveDate": str,
        "EndpointStatus": str,
        "Location": EndpointLocationTypeDef,
        "Metrics": Dict[str, float],
        "OptOut": str,
        "RequestId": str,
        "User": EndpointUserTypeDef,
    },
    total=False,
)

EventsBatchTypeDef = TypedDict(
    "EventsBatchTypeDef", {"Endpoint": PublicEndpointTypeDef, "Events": Dict[str, EventTypeDef]}
)

EventsRequestTypeDef = TypedDict(
    "EventsRequestTypeDef", {"BatchItem": Dict[str, EventsBatchTypeDef]}
)

_RequiredExportJobRequestTypeDef = TypedDict(
    "_RequiredExportJobRequestTypeDef", {"RoleArn": str, "S3UrlPrefix": str}
)
_OptionalExportJobRequestTypeDef = TypedDict(
    "_OptionalExportJobRequestTypeDef", {"SegmentId": str, "SegmentVersion": int}, total=False
)


class ExportJobRequestTypeDef(_RequiredExportJobRequestTypeDef, _OptionalExportJobRequestTypeDef):
    pass


_RequiredGCMChannelRequestTypeDef = TypedDict("_RequiredGCMChannelRequestTypeDef", {"ApiKey": str})
_OptionalGCMChannelRequestTypeDef = TypedDict(
    "_OptionalGCMChannelRequestTypeDef", {"Enabled": bool}, total=False
)


class GCMChannelRequestTypeDef(
    _RequiredGCMChannelRequestTypeDef, _OptionalGCMChannelRequestTypeDef
):
    pass


GetAdmChannelResponseTypeDef = TypedDict(
    "GetAdmChannelResponseTypeDef", {"ADMChannelResponse": ADMChannelResponseTypeDef}
)

GetApnsChannelResponseTypeDef = TypedDict(
    "GetApnsChannelResponseTypeDef", {"APNSChannelResponse": APNSChannelResponseTypeDef}
)

GetApnsSandboxChannelResponseTypeDef = TypedDict(
    "GetApnsSandboxChannelResponseTypeDef",
    {"APNSSandboxChannelResponse": APNSSandboxChannelResponseTypeDef},
)

GetApnsVoipChannelResponseTypeDef = TypedDict(
    "GetApnsVoipChannelResponseTypeDef", {"APNSVoipChannelResponse": APNSVoipChannelResponseTypeDef}
)

GetApnsVoipSandboxChannelResponseTypeDef = TypedDict(
    "GetApnsVoipSandboxChannelResponseTypeDef",
    {"APNSVoipSandboxChannelResponse": APNSVoipSandboxChannelResponseTypeDef},
)

GetAppResponseTypeDef = TypedDict(
    "GetAppResponseTypeDef", {"ApplicationResponse": ApplicationResponseTypeDef}
)

ResultRowValueTypeDef = TypedDict("ResultRowValueTypeDef", {"Key": str, "Type": str, "Value": str})

ResultRowTypeDef = TypedDict(
    "ResultRowTypeDef",
    {"GroupedBys": List[ResultRowValueTypeDef], "Values": List[ResultRowValueTypeDef]},
)

BaseKpiResultTypeDef = TypedDict("BaseKpiResultTypeDef", {"Rows": List[ResultRowTypeDef]})

_RequiredApplicationDateRangeKpiResponseTypeDef = TypedDict(
    "_RequiredApplicationDateRangeKpiResponseTypeDef",
    {
        "ApplicationId": str,
        "EndTime": datetime,
        "KpiName": str,
        "KpiResult": BaseKpiResultTypeDef,
        "StartTime": datetime,
    },
)
_OptionalApplicationDateRangeKpiResponseTypeDef = TypedDict(
    "_OptionalApplicationDateRangeKpiResponseTypeDef", {"NextToken": str}, total=False
)


class ApplicationDateRangeKpiResponseTypeDef(
    _RequiredApplicationDateRangeKpiResponseTypeDef, _OptionalApplicationDateRangeKpiResponseTypeDef
):
    pass


GetApplicationDateRangeKpiResponseTypeDef = TypedDict(
    "GetApplicationDateRangeKpiResponseTypeDef",
    {"ApplicationDateRangeKpiResponse": ApplicationDateRangeKpiResponseTypeDef},
)

_RequiredApplicationSettingsResourceTypeDef = TypedDict(
    "_RequiredApplicationSettingsResourceTypeDef", {"ApplicationId": str}
)
_OptionalApplicationSettingsResourceTypeDef = TypedDict(
    "_OptionalApplicationSettingsResourceTypeDef",
    {
        "CampaignHook": CampaignHookTypeDef,
        "LastModifiedDate": str,
        "Limits": CampaignLimitsTypeDef,
        "QuietTime": QuietTimeTypeDef,
    },
    total=False,
)


class ApplicationSettingsResourceTypeDef(
    _RequiredApplicationSettingsResourceTypeDef, _OptionalApplicationSettingsResourceTypeDef
):
    pass


GetApplicationSettingsResponseTypeDef = TypedDict(
    "GetApplicationSettingsResponseTypeDef",
    {"ApplicationSettingsResource": ApplicationSettingsResourceTypeDef},
)

ApplicationsResponseTypeDef = TypedDict(
    "ApplicationsResponseTypeDef",
    {"Item": List[ApplicationResponseTypeDef], "NextToken": str},
    total=False,
)

GetAppsResponseTypeDef = TypedDict(
    "GetAppsResponseTypeDef", {"ApplicationsResponse": ApplicationsResponseTypeDef}
)

GetBaiduChannelResponseTypeDef = TypedDict(
    "GetBaiduChannelResponseTypeDef", {"BaiduChannelResponse": BaiduChannelResponseTypeDef}
)

_RequiredActivityResponseTypeDef = TypedDict(
    "_RequiredActivityResponseTypeDef", {"ApplicationId": str, "CampaignId": str, "Id": str}
)
_OptionalActivityResponseTypeDef = TypedDict(
    "_OptionalActivityResponseTypeDef",
    {
        "End": str,
        "Result": str,
        "ScheduledStart": str,
        "Start": str,
        "State": str,
        "SuccessfulEndpointCount": int,
        "TimezonesCompletedCount": int,
        "TimezonesTotalCount": int,
        "TotalEndpointCount": int,
        "TreatmentId": str,
    },
    total=False,
)


class ActivityResponseTypeDef(_RequiredActivityResponseTypeDef, _OptionalActivityResponseTypeDef):
    pass


_RequiredActivitiesResponseTypeDef = TypedDict(
    "_RequiredActivitiesResponseTypeDef", {"Item": List[ActivityResponseTypeDef]}
)
_OptionalActivitiesResponseTypeDef = TypedDict(
    "_OptionalActivitiesResponseTypeDef", {"NextToken": str}, total=False
)


class ActivitiesResponseTypeDef(
    _RequiredActivitiesResponseTypeDef, _OptionalActivitiesResponseTypeDef
):
    pass


GetCampaignActivitiesResponseTypeDef = TypedDict(
    "GetCampaignActivitiesResponseTypeDef", {"ActivitiesResponse": ActivitiesResponseTypeDef}
)

_RequiredCampaignDateRangeKpiResponseTypeDef = TypedDict(
    "_RequiredCampaignDateRangeKpiResponseTypeDef",
    {
        "ApplicationId": str,
        "CampaignId": str,
        "EndTime": datetime,
        "KpiName": str,
        "KpiResult": BaseKpiResultTypeDef,
        "StartTime": datetime,
    },
)
_OptionalCampaignDateRangeKpiResponseTypeDef = TypedDict(
    "_OptionalCampaignDateRangeKpiResponseTypeDef", {"NextToken": str}, total=False
)


class CampaignDateRangeKpiResponseTypeDef(
    _RequiredCampaignDateRangeKpiResponseTypeDef, _OptionalCampaignDateRangeKpiResponseTypeDef
):
    pass


GetCampaignDateRangeKpiResponseTypeDef = TypedDict(
    "GetCampaignDateRangeKpiResponseTypeDef",
    {"CampaignDateRangeKpiResponse": CampaignDateRangeKpiResponseTypeDef},
)

GetCampaignResponseTypeDef = TypedDict(
    "GetCampaignResponseTypeDef", {"CampaignResponse": CampaignResponseTypeDef}
)

GetCampaignVersionResponseTypeDef = TypedDict(
    "GetCampaignVersionResponseTypeDef", {"CampaignResponse": CampaignResponseTypeDef}
)

_RequiredCampaignsResponseTypeDef = TypedDict(
    "_RequiredCampaignsResponseTypeDef", {"Item": List[CampaignResponseTypeDef]}
)
_OptionalCampaignsResponseTypeDef = TypedDict(
    "_OptionalCampaignsResponseTypeDef", {"NextToken": str}, total=False
)


class CampaignsResponseTypeDef(
    _RequiredCampaignsResponseTypeDef, _OptionalCampaignsResponseTypeDef
):
    pass


GetCampaignVersionsResponseTypeDef = TypedDict(
    "GetCampaignVersionsResponseTypeDef", {"CampaignsResponse": CampaignsResponseTypeDef}
)

GetCampaignsResponseTypeDef = TypedDict(
    "GetCampaignsResponseTypeDef", {"CampaignsResponse": CampaignsResponseTypeDef}
)

ChannelResponseTypeDef = TypedDict(
    "ChannelResponseTypeDef",
    {
        "ApplicationId": str,
        "CreationDate": str,
        "Enabled": bool,
        "HasCredential": bool,
        "Id": str,
        "IsArchived": bool,
        "LastModifiedBy": str,
        "LastModifiedDate": str,
        "Version": int,
    },
    total=False,
)

ChannelsResponseTypeDef = TypedDict(
    "ChannelsResponseTypeDef", {"Channels": Dict[str, ChannelResponseTypeDef]}
)

GetChannelsResponseTypeDef = TypedDict(
    "GetChannelsResponseTypeDef", {"ChannelsResponse": ChannelsResponseTypeDef}
)

GetEmailChannelResponseTypeDef = TypedDict(
    "GetEmailChannelResponseTypeDef", {"EmailChannelResponse": EmailChannelResponseTypeDef}
)

_RequiredEmailTemplateResponseTypeDef = TypedDict(
    "_RequiredEmailTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": Literal["EMAIL", "SMS", "VOICE", "PUSH"],
    },
)
_OptionalEmailTemplateResponseTypeDef = TypedDict(
    "_OptionalEmailTemplateResponseTypeDef",
    {
        "Arn": str,
        "DefaultSubstitutions": str,
        "HtmlPart": str,
        "RecommenderId": str,
        "Subject": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "TextPart": str,
        "Version": str,
    },
    total=False,
)


class EmailTemplateResponseTypeDef(
    _RequiredEmailTemplateResponseTypeDef, _OptionalEmailTemplateResponseTypeDef
):
    pass


GetEmailTemplateResponseTypeDef = TypedDict(
    "GetEmailTemplateResponseTypeDef", {"EmailTemplateResponse": EmailTemplateResponseTypeDef}
)

GetEndpointResponseTypeDef = TypedDict(
    "GetEndpointResponseTypeDef", {"EndpointResponse": EndpointResponseTypeDef}
)

GetEventStreamResponseTypeDef = TypedDict(
    "GetEventStreamResponseTypeDef", {"EventStream": EventStreamTypeDef}
)

GetExportJobResponseTypeDef = TypedDict(
    "GetExportJobResponseTypeDef", {"ExportJobResponse": ExportJobResponseTypeDef}
)

_RequiredExportJobsResponseTypeDef = TypedDict(
    "_RequiredExportJobsResponseTypeDef", {"Item": List[ExportJobResponseTypeDef]}
)
_OptionalExportJobsResponseTypeDef = TypedDict(
    "_OptionalExportJobsResponseTypeDef", {"NextToken": str}, total=False
)


class ExportJobsResponseTypeDef(
    _RequiredExportJobsResponseTypeDef, _OptionalExportJobsResponseTypeDef
):
    pass


GetExportJobsResponseTypeDef = TypedDict(
    "GetExportJobsResponseTypeDef", {"ExportJobsResponse": ExportJobsResponseTypeDef}
)

GetGcmChannelResponseTypeDef = TypedDict(
    "GetGcmChannelResponseTypeDef", {"GCMChannelResponse": GCMChannelResponseTypeDef}
)

GetImportJobResponseTypeDef = TypedDict(
    "GetImportJobResponseTypeDef", {"ImportJobResponse": ImportJobResponseTypeDef}
)

_RequiredImportJobsResponseTypeDef = TypedDict(
    "_RequiredImportJobsResponseTypeDef", {"Item": List[ImportJobResponseTypeDef]}
)
_OptionalImportJobsResponseTypeDef = TypedDict(
    "_OptionalImportJobsResponseTypeDef", {"NextToken": str}, total=False
)


class ImportJobsResponseTypeDef(
    _RequiredImportJobsResponseTypeDef, _OptionalImportJobsResponseTypeDef
):
    pass


GetImportJobsResponseTypeDef = TypedDict(
    "GetImportJobsResponseTypeDef", {"ImportJobsResponse": ImportJobsResponseTypeDef}
)

_RequiredJourneyDateRangeKpiResponseTypeDef = TypedDict(
    "_RequiredJourneyDateRangeKpiResponseTypeDef",
    {
        "ApplicationId": str,
        "EndTime": datetime,
        "JourneyId": str,
        "KpiName": str,
        "KpiResult": BaseKpiResultTypeDef,
        "StartTime": datetime,
    },
)
_OptionalJourneyDateRangeKpiResponseTypeDef = TypedDict(
    "_OptionalJourneyDateRangeKpiResponseTypeDef", {"NextToken": str}, total=False
)


class JourneyDateRangeKpiResponseTypeDef(
    _RequiredJourneyDateRangeKpiResponseTypeDef, _OptionalJourneyDateRangeKpiResponseTypeDef
):
    pass


GetJourneyDateRangeKpiResponseTypeDef = TypedDict(
    "GetJourneyDateRangeKpiResponseTypeDef",
    {"JourneyDateRangeKpiResponse": JourneyDateRangeKpiResponseTypeDef},
)

JourneyExecutionActivityMetricsResponseTypeDef = TypedDict(
    "JourneyExecutionActivityMetricsResponseTypeDef",
    {
        "ActivityType": str,
        "ApplicationId": str,
        "JourneyActivityId": str,
        "JourneyId": str,
        "LastEvaluatedTime": str,
        "Metrics": Dict[str, str],
    },
)

GetJourneyExecutionActivityMetricsResponseTypeDef = TypedDict(
    "GetJourneyExecutionActivityMetricsResponseTypeDef",
    {"JourneyExecutionActivityMetricsResponse": JourneyExecutionActivityMetricsResponseTypeDef},
)

JourneyExecutionMetricsResponseTypeDef = TypedDict(
    "JourneyExecutionMetricsResponseTypeDef",
    {"ApplicationId": str, "JourneyId": str, "LastEvaluatedTime": str, "Metrics": Dict[str, str]},
)

GetJourneyExecutionMetricsResponseTypeDef = TypedDict(
    "GetJourneyExecutionMetricsResponseTypeDef",
    {"JourneyExecutionMetricsResponse": JourneyExecutionMetricsResponseTypeDef},
)

GetJourneyResponseTypeDef = TypedDict(
    "GetJourneyResponseTypeDef", {"JourneyResponse": JourneyResponseTypeDef}
)

APNSPushNotificationTemplateTypeDef = TypedDict(
    "APNSPushNotificationTemplateTypeDef",
    {
        "Action": Literal["OPEN_APP", "DEEP_LINK", "URL"],
        "Body": str,
        "MediaUrl": str,
        "RawContent": str,
        "Sound": str,
        "Title": str,
        "Url": str,
    },
    total=False,
)

AndroidPushNotificationTemplateTypeDef = TypedDict(
    "AndroidPushNotificationTemplateTypeDef",
    {
        "Action": Literal["OPEN_APP", "DEEP_LINK", "URL"],
        "Body": str,
        "ImageIconUrl": str,
        "ImageUrl": str,
        "RawContent": str,
        "SmallImageIconUrl": str,
        "Sound": str,
        "Title": str,
        "Url": str,
    },
    total=False,
)

DefaultPushNotificationTemplateTypeDef = TypedDict(
    "DefaultPushNotificationTemplateTypeDef",
    {
        "Action": Literal["OPEN_APP", "DEEP_LINK", "URL"],
        "Body": str,
        "Sound": str,
        "Title": str,
        "Url": str,
    },
    total=False,
)

_RequiredPushNotificationTemplateResponseTypeDef = TypedDict(
    "_RequiredPushNotificationTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": Literal["EMAIL", "SMS", "VOICE", "PUSH"],
    },
)
_OptionalPushNotificationTemplateResponseTypeDef = TypedDict(
    "_OptionalPushNotificationTemplateResponseTypeDef",
    {
        "ADM": AndroidPushNotificationTemplateTypeDef,
        "APNS": APNSPushNotificationTemplateTypeDef,
        "Arn": str,
        "Baidu": AndroidPushNotificationTemplateTypeDef,
        "Default": DefaultPushNotificationTemplateTypeDef,
        "DefaultSubstitutions": str,
        "GCM": AndroidPushNotificationTemplateTypeDef,
        "RecommenderId": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "Version": str,
    },
    total=False,
)


class PushNotificationTemplateResponseTypeDef(
    _RequiredPushNotificationTemplateResponseTypeDef,
    _OptionalPushNotificationTemplateResponseTypeDef,
):
    pass


GetPushTemplateResponseTypeDef = TypedDict(
    "GetPushTemplateResponseTypeDef",
    {"PushNotificationTemplateResponse": PushNotificationTemplateResponseTypeDef},
)

GetRecommenderConfigurationResponseTypeDef = TypedDict(
    "GetRecommenderConfigurationResponseTypeDef",
    {"RecommenderConfigurationResponse": RecommenderConfigurationResponseTypeDef},
)

_RequiredListRecommenderConfigurationsResponseTypeDef = TypedDict(
    "_RequiredListRecommenderConfigurationsResponseTypeDef",
    {"Item": List[RecommenderConfigurationResponseTypeDef]},
)
_OptionalListRecommenderConfigurationsResponseTypeDef = TypedDict(
    "_OptionalListRecommenderConfigurationsResponseTypeDef", {"NextToken": str}, total=False
)


class ListRecommenderConfigurationsResponseTypeDef(
    _RequiredListRecommenderConfigurationsResponseTypeDef,
    _OptionalListRecommenderConfigurationsResponseTypeDef,
):
    pass


GetRecommenderConfigurationsResponseTypeDef = TypedDict(
    "GetRecommenderConfigurationsResponseTypeDef",
    {"ListRecommenderConfigurationsResponse": ListRecommenderConfigurationsResponseTypeDef},
)

GetSegmentExportJobsResponseTypeDef = TypedDict(
    "GetSegmentExportJobsResponseTypeDef", {"ExportJobsResponse": ExportJobsResponseTypeDef}
)

GetSegmentImportJobsResponseTypeDef = TypedDict(
    "GetSegmentImportJobsResponseTypeDef", {"ImportJobsResponse": ImportJobsResponseTypeDef}
)

GetSegmentResponseTypeDef = TypedDict(
    "GetSegmentResponseTypeDef", {"SegmentResponse": SegmentResponseTypeDef}
)

GetSegmentVersionResponseTypeDef = TypedDict(
    "GetSegmentVersionResponseTypeDef", {"SegmentResponse": SegmentResponseTypeDef}
)

_RequiredSegmentsResponseTypeDef = TypedDict(
    "_RequiredSegmentsResponseTypeDef", {"Item": List[SegmentResponseTypeDef]}
)
_OptionalSegmentsResponseTypeDef = TypedDict(
    "_OptionalSegmentsResponseTypeDef", {"NextToken": str}, total=False
)


class SegmentsResponseTypeDef(_RequiredSegmentsResponseTypeDef, _OptionalSegmentsResponseTypeDef):
    pass


GetSegmentVersionsResponseTypeDef = TypedDict(
    "GetSegmentVersionsResponseTypeDef", {"SegmentsResponse": SegmentsResponseTypeDef}
)

GetSegmentsResponseTypeDef = TypedDict(
    "GetSegmentsResponseTypeDef", {"SegmentsResponse": SegmentsResponseTypeDef}
)

GetSmsChannelResponseTypeDef = TypedDict(
    "GetSmsChannelResponseTypeDef", {"SMSChannelResponse": SMSChannelResponseTypeDef}
)

_RequiredSMSTemplateResponseTypeDef = TypedDict(
    "_RequiredSMSTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": Literal["EMAIL", "SMS", "VOICE", "PUSH"],
    },
)
_OptionalSMSTemplateResponseTypeDef = TypedDict(
    "_OptionalSMSTemplateResponseTypeDef",
    {
        "Arn": str,
        "Body": str,
        "DefaultSubstitutions": str,
        "RecommenderId": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "Version": str,
    },
    total=False,
)


class SMSTemplateResponseTypeDef(
    _RequiredSMSTemplateResponseTypeDef, _OptionalSMSTemplateResponseTypeDef
):
    pass


GetSmsTemplateResponseTypeDef = TypedDict(
    "GetSmsTemplateResponseTypeDef", {"SMSTemplateResponse": SMSTemplateResponseTypeDef}
)

GetUserEndpointsResponseTypeDef = TypedDict(
    "GetUserEndpointsResponseTypeDef", {"EndpointsResponse": EndpointsResponseTypeDef}
)

GetVoiceChannelResponseTypeDef = TypedDict(
    "GetVoiceChannelResponseTypeDef", {"VoiceChannelResponse": VoiceChannelResponseTypeDef}
)

_RequiredVoiceTemplateResponseTypeDef = TypedDict(
    "_RequiredVoiceTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": Literal["EMAIL", "SMS", "VOICE", "PUSH"],
    },
)
_OptionalVoiceTemplateResponseTypeDef = TypedDict(
    "_OptionalVoiceTemplateResponseTypeDef",
    {
        "Arn": str,
        "Body": str,
        "DefaultSubstitutions": str,
        "LanguageCode": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "Version": str,
        "VoiceId": str,
    },
    total=False,
)


class VoiceTemplateResponseTypeDef(
    _RequiredVoiceTemplateResponseTypeDef, _OptionalVoiceTemplateResponseTypeDef
):
    pass


GetVoiceTemplateResponseTypeDef = TypedDict(
    "GetVoiceTemplateResponseTypeDef", {"VoiceTemplateResponse": VoiceTemplateResponseTypeDef}
)

_RequiredImportJobRequestTypeDef = TypedDict(
    "_RequiredImportJobRequestTypeDef",
    {"Format": Literal["CSV", "JSON"], "RoleArn": str, "S3Url": str},
)
_OptionalImportJobRequestTypeDef = TypedDict(
    "_OptionalImportJobRequestTypeDef",
    {
        "DefineSegment": bool,
        "ExternalId": str,
        "RegisterEndpoints": bool,
        "SegmentId": str,
        "SegmentName": str,
    },
    total=False,
)


class ImportJobRequestTypeDef(_RequiredImportJobRequestTypeDef, _OptionalImportJobRequestTypeDef):
    pass


JourneyStateRequestTypeDef = TypedDict(
    "JourneyStateRequestTypeDef",
    {"State": Literal["DRAFT", "ACTIVE", "COMPLETED", "CANCELLED", "CLOSED"]},
    total=False,
)

_RequiredJourneysResponseTypeDef = TypedDict(
    "_RequiredJourneysResponseTypeDef", {"Item": List[JourneyResponseTypeDef]}
)
_OptionalJourneysResponseTypeDef = TypedDict(
    "_OptionalJourneysResponseTypeDef", {"NextToken": str}, total=False
)


class JourneysResponseTypeDef(_RequiredJourneysResponseTypeDef, _OptionalJourneysResponseTypeDef):
    pass


ListJourneysResponseTypeDef = TypedDict(
    "ListJourneysResponseTypeDef", {"JourneysResponse": JourneysResponseTypeDef}
)

TagsModelTypeDef = TypedDict("TagsModelTypeDef", {"tags": Dict[str, str]})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"TagsModel": TagsModelTypeDef}
)

_RequiredTemplateVersionResponseTypeDef = TypedDict(
    "_RequiredTemplateVersionResponseTypeDef",
    {"CreationDate": str, "LastModifiedDate": str, "TemplateName": str, "TemplateType": str},
)
_OptionalTemplateVersionResponseTypeDef = TypedDict(
    "_OptionalTemplateVersionResponseTypeDef",
    {"DefaultSubstitutions": str, "TemplateDescription": str, "Version": str},
    total=False,
)


class TemplateVersionResponseTypeDef(
    _RequiredTemplateVersionResponseTypeDef, _OptionalTemplateVersionResponseTypeDef
):
    pass


_RequiredTemplateVersionsResponseTypeDef = TypedDict(
    "_RequiredTemplateVersionsResponseTypeDef", {"Item": List[TemplateVersionResponseTypeDef]}
)
_OptionalTemplateVersionsResponseTypeDef = TypedDict(
    "_OptionalTemplateVersionsResponseTypeDef",
    {"Message": str, "NextToken": str, "RequestID": str},
    total=False,
)


class TemplateVersionsResponseTypeDef(
    _RequiredTemplateVersionsResponseTypeDef, _OptionalTemplateVersionsResponseTypeDef
):
    pass


ListTemplateVersionsResponseTypeDef = TypedDict(
    "ListTemplateVersionsResponseTypeDef",
    {"TemplateVersionsResponse": TemplateVersionsResponseTypeDef},
)

_RequiredTemplateResponseTypeDef = TypedDict(
    "_RequiredTemplateResponseTypeDef",
    {
        "CreationDate": str,
        "LastModifiedDate": str,
        "TemplateName": str,
        "TemplateType": Literal["EMAIL", "SMS", "VOICE", "PUSH"],
    },
)
_OptionalTemplateResponseTypeDef = TypedDict(
    "_OptionalTemplateResponseTypeDef",
    {
        "Arn": str,
        "DefaultSubstitutions": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "Version": str,
    },
    total=False,
)


class TemplateResponseTypeDef(_RequiredTemplateResponseTypeDef, _OptionalTemplateResponseTypeDef):
    pass


_RequiredTemplatesResponseTypeDef = TypedDict(
    "_RequiredTemplatesResponseTypeDef", {"Item": List[TemplateResponseTypeDef]}
)
_OptionalTemplatesResponseTypeDef = TypedDict(
    "_OptionalTemplatesResponseTypeDef", {"NextToken": str}, total=False
)


class TemplatesResponseTypeDef(
    _RequiredTemplatesResponseTypeDef, _OptionalTemplatesResponseTypeDef
):
    pass


ListTemplatesResponseTypeDef = TypedDict(
    "ListTemplatesResponseTypeDef", {"TemplatesResponse": TemplatesResponseTypeDef}
)

AddressConfigurationTypeDef = TypedDict(
    "AddressConfigurationTypeDef",
    {
        "BodyOverride": str,
        "ChannelType": Literal[
            "GCM",
            "APNS",
            "APNS_SANDBOX",
            "APNS_VOIP",
            "APNS_VOIP_SANDBOX",
            "ADM",
            "SMS",
            "VOICE",
            "EMAIL",
            "BAIDU",
            "CUSTOM",
        ],
        "Context": Dict[str, str],
        "RawContent": str,
        "Substitutions": Dict[str, List[str]],
        "TitleOverride": str,
    },
    total=False,
)

ADMMessageTypeDef = TypedDict(
    "ADMMessageTypeDef",
    {
        "Action": Literal["OPEN_APP", "DEEP_LINK", "URL"],
        "Body": str,
        "ConsolidationKey": str,
        "Data": Dict[str, str],
        "ExpiresAfter": str,
        "IconReference": str,
        "ImageIconUrl": str,
        "ImageUrl": str,
        "MD5": str,
        "RawContent": str,
        "SilentPush": bool,
        "SmallImageIconUrl": str,
        "Sound": str,
        "Substitutions": Dict[str, List[str]],
        "Title": str,
        "Url": str,
    },
    total=False,
)

APNSMessageTypeDef = TypedDict(
    "APNSMessageTypeDef",
    {
        "APNSPushType": str,
        "Action": Literal["OPEN_APP", "DEEP_LINK", "URL"],
        "Badge": int,
        "Body": str,
        "Category": str,
        "CollapseId": str,
        "Data": Dict[str, str],
        "MediaUrl": str,
        "PreferredAuthenticationMethod": str,
        "Priority": str,
        "RawContent": str,
        "SilentPush": bool,
        "Sound": str,
        "Substitutions": Dict[str, List[str]],
        "ThreadId": str,
        "TimeToLive": int,
        "Title": str,
        "Url": str,
    },
    total=False,
)

BaiduMessageTypeDef = TypedDict(
    "BaiduMessageTypeDef",
    {
        "Action": Literal["OPEN_APP", "DEEP_LINK", "URL"],
        "Body": str,
        "Data": Dict[str, str],
        "IconReference": str,
        "ImageIconUrl": str,
        "ImageUrl": str,
        "RawContent": str,
        "SilentPush": bool,
        "SmallImageIconUrl": str,
        "Sound": str,
        "Substitutions": Dict[str, List[str]],
        "TimeToLive": int,
        "Title": str,
        "Url": str,
    },
    total=False,
)

DefaultMessageTypeDef = TypedDict(
    "DefaultMessageTypeDef", {"Body": str, "Substitutions": Dict[str, List[str]]}, total=False
)

DefaultPushNotificationMessageTypeDef = TypedDict(
    "DefaultPushNotificationMessageTypeDef",
    {
        "Action": Literal["OPEN_APP", "DEEP_LINK", "URL"],
        "Body": str,
        "Data": Dict[str, str],
        "SilentPush": bool,
        "Substitutions": Dict[str, List[str]],
        "Title": str,
        "Url": str,
    },
    total=False,
)

RawEmailTypeDef = TypedDict("RawEmailTypeDef", {"Data": Union[bytes, IO]}, total=False)

SimpleEmailPartTypeDef = TypedDict(
    "SimpleEmailPartTypeDef", {"Charset": str, "Data": str}, total=False
)

SimpleEmailTypeDef = TypedDict(
    "SimpleEmailTypeDef",
    {
        "HtmlPart": SimpleEmailPartTypeDef,
        "Subject": SimpleEmailPartTypeDef,
        "TextPart": SimpleEmailPartTypeDef,
    },
    total=False,
)

EmailMessageTypeDef = TypedDict(
    "EmailMessageTypeDef",
    {
        "Body": str,
        "FeedbackForwardingAddress": str,
        "FromAddress": str,
        "RawEmail": RawEmailTypeDef,
        "ReplyToAddresses": List[str],
        "SimpleEmail": SimpleEmailTypeDef,
        "Substitutions": Dict[str, List[str]],
    },
    total=False,
)

GCMMessageTypeDef = TypedDict(
    "GCMMessageTypeDef",
    {
        "Action": Literal["OPEN_APP", "DEEP_LINK", "URL"],
        "Body": str,
        "CollapseKey": str,
        "Data": Dict[str, str],
        "IconReference": str,
        "ImageIconUrl": str,
        "ImageUrl": str,
        "Priority": str,
        "RawContent": str,
        "RestrictedPackageName": str,
        "SilentPush": bool,
        "SmallImageIconUrl": str,
        "Sound": str,
        "Substitutions": Dict[str, List[str]],
        "TimeToLive": int,
        "Title": str,
        "Url": str,
    },
    total=False,
)

SMSMessageTypeDef = TypedDict(
    "SMSMessageTypeDef",
    {
        "Body": str,
        "Keyword": str,
        "MediaUrl": str,
        "MessageType": Literal["TRANSACTIONAL", "PROMOTIONAL"],
        "OriginationNumber": str,
        "SenderId": str,
        "Substitutions": Dict[str, List[str]],
    },
    total=False,
)

VoiceMessageTypeDef = TypedDict(
    "VoiceMessageTypeDef",
    {
        "Body": str,
        "LanguageCode": str,
        "OriginationNumber": str,
        "Substitutions": Dict[str, List[str]],
        "VoiceId": str,
    },
    total=False,
)

DirectMessageConfigurationTypeDef = TypedDict(
    "DirectMessageConfigurationTypeDef",
    {
        "ADMMessage": ADMMessageTypeDef,
        "APNSMessage": APNSMessageTypeDef,
        "BaiduMessage": BaiduMessageTypeDef,
        "DefaultMessage": DefaultMessageTypeDef,
        "DefaultPushNotificationMessage": DefaultPushNotificationMessageTypeDef,
        "EmailMessage": EmailMessageTypeDef,
        "GCMMessage": GCMMessageTypeDef,
        "SMSMessage": SMSMessageTypeDef,
        "VoiceMessage": VoiceMessageTypeDef,
    },
    total=False,
)

EndpointSendConfigurationTypeDef = TypedDict(
    "EndpointSendConfigurationTypeDef",
    {
        "BodyOverride": str,
        "Context": Dict[str, str],
        "RawContent": str,
        "Substitutions": Dict[str, List[str]],
        "TitleOverride": str,
    },
    total=False,
)

_RequiredMessageRequestTypeDef = TypedDict(
    "_RequiredMessageRequestTypeDef", {"MessageConfiguration": DirectMessageConfigurationTypeDef}
)
_OptionalMessageRequestTypeDef = TypedDict(
    "_OptionalMessageRequestTypeDef",
    {
        "Addresses": Dict[str, AddressConfigurationTypeDef],
        "Context": Dict[str, str],
        "Endpoints": Dict[str, EndpointSendConfigurationTypeDef],
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TraceId": str,
    },
    total=False,
)


class MessageRequestTypeDef(_RequiredMessageRequestTypeDef, _OptionalMessageRequestTypeDef):
    pass


NumberValidateRequestTypeDef = TypedDict(
    "NumberValidateRequestTypeDef", {"IsoCountryCode": str, "PhoneNumber": str}, total=False
)

NumberValidateResponseTypeDef = TypedDict(
    "NumberValidateResponseTypeDef",
    {
        "Carrier": str,
        "City": str,
        "CleansedPhoneNumberE164": str,
        "CleansedPhoneNumberNational": str,
        "Country": str,
        "CountryCodeIso2": str,
        "CountryCodeNumeric": str,
        "County": str,
        "OriginalCountryCodeIso2": str,
        "OriginalPhoneNumber": str,
        "PhoneType": str,
        "PhoneTypeCode": int,
        "Timezone": str,
        "ZipCode": str,
    },
    total=False,
)

PhoneNumberValidateResponseTypeDef = TypedDict(
    "PhoneNumberValidateResponseTypeDef", {"NumberValidateResponse": NumberValidateResponseTypeDef}
)

PushNotificationTemplateRequestTypeDef = TypedDict(
    "PushNotificationTemplateRequestTypeDef",
    {
        "ADM": AndroidPushNotificationTemplateTypeDef,
        "APNS": APNSPushNotificationTemplateTypeDef,
        "Baidu": AndroidPushNotificationTemplateTypeDef,
        "Default": DefaultPushNotificationTemplateTypeDef,
        "DefaultSubstitutions": str,
        "GCM": AndroidPushNotificationTemplateTypeDef,
        "RecommenderId": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
    },
    total=False,
)

PutEventStreamResponseTypeDef = TypedDict(
    "PutEventStreamResponseTypeDef", {"EventStream": EventStreamTypeDef}
)

EndpointItemResponseTypeDef = TypedDict(
    "EndpointItemResponseTypeDef", {"Message": str, "StatusCode": int}, total=False
)

EventItemResponseTypeDef = TypedDict(
    "EventItemResponseTypeDef", {"Message": str, "StatusCode": int}, total=False
)

ItemResponseTypeDef = TypedDict(
    "ItemResponseTypeDef",
    {
        "EndpointItemResponse": EndpointItemResponseTypeDef,
        "EventsItemResponse": Dict[str, EventItemResponseTypeDef],
    },
    total=False,
)

EventsResponseTypeDef = TypedDict(
    "EventsResponseTypeDef", {"Results": Dict[str, ItemResponseTypeDef]}, total=False
)

PutEventsResponseTypeDef = TypedDict(
    "PutEventsResponseTypeDef", {"EventsResponse": EventsResponseTypeDef}
)

_RequiredAttributesResourceTypeDef = TypedDict(
    "_RequiredAttributesResourceTypeDef", {"ApplicationId": str, "AttributeType": str}
)
_OptionalAttributesResourceTypeDef = TypedDict(
    "_OptionalAttributesResourceTypeDef", {"Attributes": List[str]}, total=False
)


class AttributesResourceTypeDef(
    _RequiredAttributesResourceTypeDef, _OptionalAttributesResourceTypeDef
):
    pass


RemoveAttributesResponseTypeDef = TypedDict(
    "RemoveAttributesResponseTypeDef", {"AttributesResource": AttributesResourceTypeDef}
)

SMSChannelRequestTypeDef = TypedDict(
    "SMSChannelRequestTypeDef", {"Enabled": bool, "SenderId": str, "ShortCode": str}, total=False
)

SMSTemplateRequestTypeDef = TypedDict(
    "SMSTemplateRequestTypeDef",
    {
        "Body": str,
        "DefaultSubstitutions": str,
        "RecommenderId": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
    },
    total=False,
)

_RequiredEndpointMessageResultTypeDef = TypedDict(
    "_RequiredEndpointMessageResultTypeDef",
    {
        "DeliveryStatus": Literal[
            "SUCCESSFUL",
            "THROTTLED",
            "TEMPORARY_FAILURE",
            "PERMANENT_FAILURE",
            "UNKNOWN_FAILURE",
            "OPT_OUT",
            "DUPLICATE",
        ],
        "StatusCode": int,
    },
)
_OptionalEndpointMessageResultTypeDef = TypedDict(
    "_OptionalEndpointMessageResultTypeDef",
    {"Address": str, "MessageId": str, "StatusMessage": str, "UpdatedToken": str},
    total=False,
)


class EndpointMessageResultTypeDef(
    _RequiredEndpointMessageResultTypeDef, _OptionalEndpointMessageResultTypeDef
):
    pass


_RequiredMessageResultTypeDef = TypedDict(
    "_RequiredMessageResultTypeDef",
    {
        "DeliveryStatus": Literal[
            "SUCCESSFUL",
            "THROTTLED",
            "TEMPORARY_FAILURE",
            "PERMANENT_FAILURE",
            "UNKNOWN_FAILURE",
            "OPT_OUT",
            "DUPLICATE",
        ],
        "StatusCode": int,
    },
)
_OptionalMessageResultTypeDef = TypedDict(
    "_OptionalMessageResultTypeDef",
    {"MessageId": str, "StatusMessage": str, "UpdatedToken": str},
    total=False,
)


class MessageResultTypeDef(_RequiredMessageResultTypeDef, _OptionalMessageResultTypeDef):
    pass


_RequiredMessageResponseTypeDef = TypedDict(
    "_RequiredMessageResponseTypeDef", {"ApplicationId": str}
)
_OptionalMessageResponseTypeDef = TypedDict(
    "_OptionalMessageResponseTypeDef",
    {
        "EndpointResult": Dict[str, EndpointMessageResultTypeDef],
        "RequestId": str,
        "Result": Dict[str, MessageResultTypeDef],
    },
    total=False,
)


class MessageResponseTypeDef(_RequiredMessageResponseTypeDef, _OptionalMessageResponseTypeDef):
    pass


SendMessagesResponseTypeDef = TypedDict(
    "SendMessagesResponseTypeDef", {"MessageResponse": MessageResponseTypeDef}
)

_RequiredSendUsersMessageRequestTypeDef = TypedDict(
    "_RequiredSendUsersMessageRequestTypeDef",
    {
        "MessageConfiguration": DirectMessageConfigurationTypeDef,
        "Users": Dict[str, EndpointSendConfigurationTypeDef],
    },
)
_OptionalSendUsersMessageRequestTypeDef = TypedDict(
    "_OptionalSendUsersMessageRequestTypeDef",
    {
        "Context": Dict[str, str],
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TraceId": str,
    },
    total=False,
)


class SendUsersMessageRequestTypeDef(
    _RequiredSendUsersMessageRequestTypeDef, _OptionalSendUsersMessageRequestTypeDef
):
    pass


_RequiredSendUsersMessageResponseTypeDef = TypedDict(
    "_RequiredSendUsersMessageResponseTypeDef", {"ApplicationId": str}
)
_OptionalSendUsersMessageResponseTypeDef = TypedDict(
    "_OptionalSendUsersMessageResponseTypeDef",
    {"RequestId": str, "Result": Dict[str, Dict[str, EndpointMessageResultTypeDef]]},
    total=False,
)


class SendUsersMessageResponseTypeDef(
    _RequiredSendUsersMessageResponseTypeDef, _OptionalSendUsersMessageResponseTypeDef
):
    pass


SendUsersMessagesResponseTypeDef = TypedDict(
    "SendUsersMessagesResponseTypeDef",
    {"SendUsersMessageResponse": SendUsersMessageResponseTypeDef},
)

TemplateActiveVersionRequestTypeDef = TypedDict(
    "TemplateActiveVersionRequestTypeDef", {"Version": str}, total=False
)

UpdateAdmChannelResponseTypeDef = TypedDict(
    "UpdateAdmChannelResponseTypeDef", {"ADMChannelResponse": ADMChannelResponseTypeDef}
)

UpdateApnsChannelResponseTypeDef = TypedDict(
    "UpdateApnsChannelResponseTypeDef", {"APNSChannelResponse": APNSChannelResponseTypeDef}
)

UpdateApnsSandboxChannelResponseTypeDef = TypedDict(
    "UpdateApnsSandboxChannelResponseTypeDef",
    {"APNSSandboxChannelResponse": APNSSandboxChannelResponseTypeDef},
)

UpdateApnsVoipChannelResponseTypeDef = TypedDict(
    "UpdateApnsVoipChannelResponseTypeDef",
    {"APNSVoipChannelResponse": APNSVoipChannelResponseTypeDef},
)

UpdateApnsVoipSandboxChannelResponseTypeDef = TypedDict(
    "UpdateApnsVoipSandboxChannelResponseTypeDef",
    {"APNSVoipSandboxChannelResponse": APNSVoipSandboxChannelResponseTypeDef},
)

UpdateApplicationSettingsResponseTypeDef = TypedDict(
    "UpdateApplicationSettingsResponseTypeDef",
    {"ApplicationSettingsResource": ApplicationSettingsResourceTypeDef},
)

UpdateAttributesRequestTypeDef = TypedDict(
    "UpdateAttributesRequestTypeDef", {"Blacklist": List[str]}, total=False
)

UpdateBaiduChannelResponseTypeDef = TypedDict(
    "UpdateBaiduChannelResponseTypeDef", {"BaiduChannelResponse": BaiduChannelResponseTypeDef}
)

UpdateCampaignResponseTypeDef = TypedDict(
    "UpdateCampaignResponseTypeDef", {"CampaignResponse": CampaignResponseTypeDef}
)

UpdateEmailChannelResponseTypeDef = TypedDict(
    "UpdateEmailChannelResponseTypeDef", {"EmailChannelResponse": EmailChannelResponseTypeDef}
)

UpdateEmailTemplateResponseTypeDef = TypedDict(
    "UpdateEmailTemplateResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

UpdateEndpointResponseTypeDef = TypedDict(
    "UpdateEndpointResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

UpdateEndpointsBatchResponseTypeDef = TypedDict(
    "UpdateEndpointsBatchResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

UpdateGcmChannelResponseTypeDef = TypedDict(
    "UpdateGcmChannelResponseTypeDef", {"GCMChannelResponse": GCMChannelResponseTypeDef}
)

UpdateJourneyResponseTypeDef = TypedDict(
    "UpdateJourneyResponseTypeDef", {"JourneyResponse": JourneyResponseTypeDef}
)

UpdateJourneyStateResponseTypeDef = TypedDict(
    "UpdateJourneyStateResponseTypeDef", {"JourneyResponse": JourneyResponseTypeDef}
)

UpdatePushTemplateResponseTypeDef = TypedDict(
    "UpdatePushTemplateResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

UpdateRecommenderConfigurationResponseTypeDef = TypedDict(
    "UpdateRecommenderConfigurationResponseTypeDef",
    {"RecommenderConfigurationResponse": RecommenderConfigurationResponseTypeDef},
)

_RequiredUpdateRecommenderConfigurationTypeDef = TypedDict(
    "_RequiredUpdateRecommenderConfigurationTypeDef",
    {"RecommendationProviderRoleArn": str, "RecommendationProviderUri": str},
)
_OptionalUpdateRecommenderConfigurationTypeDef = TypedDict(
    "_OptionalUpdateRecommenderConfigurationTypeDef",
    {
        "Attributes": Dict[str, str],
        "Description": str,
        "Name": str,
        "RecommendationProviderIdType": str,
        "RecommendationTransformerUri": str,
        "RecommendationsDisplayName": str,
        "RecommendationsPerMessage": int,
    },
    total=False,
)


class UpdateRecommenderConfigurationTypeDef(
    _RequiredUpdateRecommenderConfigurationTypeDef, _OptionalUpdateRecommenderConfigurationTypeDef
):
    pass


UpdateSegmentResponseTypeDef = TypedDict(
    "UpdateSegmentResponseTypeDef", {"SegmentResponse": SegmentResponseTypeDef}
)

UpdateSmsChannelResponseTypeDef = TypedDict(
    "UpdateSmsChannelResponseTypeDef", {"SMSChannelResponse": SMSChannelResponseTypeDef}
)

UpdateSmsTemplateResponseTypeDef = TypedDict(
    "UpdateSmsTemplateResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

UpdateTemplateActiveVersionResponseTypeDef = TypedDict(
    "UpdateTemplateActiveVersionResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

UpdateVoiceChannelResponseTypeDef = TypedDict(
    "UpdateVoiceChannelResponseTypeDef", {"VoiceChannelResponse": VoiceChannelResponseTypeDef}
)

UpdateVoiceTemplateResponseTypeDef = TypedDict(
    "UpdateVoiceTemplateResponseTypeDef", {"MessageBody": MessageBodyTypeDef}
)

VoiceChannelRequestTypeDef = TypedDict("VoiceChannelRequestTypeDef", {"Enabled": bool}, total=False)

VoiceTemplateRequestTypeDef = TypedDict(
    "VoiceTemplateRequestTypeDef",
    {
        "Body": str,
        "DefaultSubstitutions": str,
        "LanguageCode": str,
        "tags": Dict[str, str],
        "TemplateDescription": str,
        "VoiceId": str,
    },
    total=False,
)

WriteApplicationSettingsRequestTypeDef = TypedDict(
    "WriteApplicationSettingsRequestTypeDef",
    {
        "CampaignHook": CampaignHookTypeDef,
        "CloudWatchMetricsEnabled": bool,
        "Limits": CampaignLimitsTypeDef,
        "QuietTime": QuietTimeTypeDef,
    },
    total=False,
)

_RequiredWriteTreatmentResourceTypeDef = TypedDict(
    "_RequiredWriteTreatmentResourceTypeDef", {"SizePercent": int}
)
_OptionalWriteTreatmentResourceTypeDef = TypedDict(
    "_OptionalWriteTreatmentResourceTypeDef",
    {
        "MessageConfiguration": MessageConfigurationTypeDef,
        "Schedule": ScheduleTypeDef,
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TreatmentDescription": str,
        "TreatmentName": str,
    },
    total=False,
)


class WriteTreatmentResourceTypeDef(
    _RequiredWriteTreatmentResourceTypeDef, _OptionalWriteTreatmentResourceTypeDef
):
    pass


WriteCampaignRequestTypeDef = TypedDict(
    "WriteCampaignRequestTypeDef",
    {
        "AdditionalTreatments": List[WriteTreatmentResourceTypeDef],
        "Description": str,
        "HoldoutPercent": int,
        "Hook": CampaignHookTypeDef,
        "IsPaused": bool,
        "Limits": CampaignLimitsTypeDef,
        "MessageConfiguration": MessageConfigurationTypeDef,
        "Name": str,
        "Schedule": ScheduleTypeDef,
        "SegmentId": str,
        "SegmentVersion": int,
        "tags": Dict[str, str],
        "TemplateConfiguration": TemplateConfigurationTypeDef,
        "TreatmentDescription": str,
        "TreatmentName": str,
    },
    total=False,
)

WriteEventStreamTypeDef = TypedDict(
    "WriteEventStreamTypeDef", {"DestinationStreamArn": str, "RoleArn": str}
)

_RequiredWriteJourneyRequestTypeDef = TypedDict(
    "_RequiredWriteJourneyRequestTypeDef", {"Name": str}
)
_OptionalWriteJourneyRequestTypeDef = TypedDict(
    "_OptionalWriteJourneyRequestTypeDef",
    {
        "Activities": Dict[str, ActivityTypeDef],
        "CreationDate": str,
        "LastModifiedDate": str,
        "Limits": JourneyLimitsTypeDef,
        "LocalTime": bool,
        "QuietTime": QuietTimeTypeDef,
        "RefreshFrequency": str,
        "Schedule": JourneyScheduleTypeDef,
        "StartActivity": str,
        "StartCondition": StartConditionTypeDef,
        "State": Literal["DRAFT", "ACTIVE", "COMPLETED", "CANCELLED", "CLOSED"],
    },
    total=False,
)


class WriteJourneyRequestTypeDef(
    _RequiredWriteJourneyRequestTypeDef, _OptionalWriteJourneyRequestTypeDef
):
    pass


WriteSegmentRequestTypeDef = TypedDict(
    "WriteSegmentRequestTypeDef",
    {
        "Dimensions": SegmentDimensionsTypeDef,
        "Name": str,
        "SegmentGroups": SegmentGroupListTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)
