"""
Main interface for chime service type definitions.

Usage::

    from mypy_boto3.chime.type_defs import AccountSettingsTypeDef

    data: AccountSettingsTypeDef = {...}
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
    "AccountSettingsTypeDef",
    "AlexaForBusinessMetadataTypeDef",
    "PhoneNumberErrorTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef",
    "AttendeeTypeDef",
    "CreateAttendeeErrorTypeDef",
    "BatchCreateAttendeeResponseTypeDef",
    "MemberErrorTypeDef",
    "BatchCreateRoomMembershipResponseTypeDef",
    "BatchDeletePhoneNumberResponseTypeDef",
    "UserErrorTypeDef",
    "BatchSuspendUserResponseTypeDef",
    "BatchUnsuspendUserResponseTypeDef",
    "BatchUpdatePhoneNumberResponseTypeDef",
    "BatchUpdateUserResponseTypeDef",
    "BusinessCallingSettingsTypeDef",
    "SigninDelegateGroupTypeDef",
    "AccountTypeDef",
    "CreateAccountResponseTypeDef",
    "CreateAttendeeRequestItemTypeDef",
    "CreateAttendeeResponseTypeDef",
    "BotTypeDef",
    "CreateBotResponseTypeDef",
    "MediaPlacementTypeDef",
    "MeetingTypeDef",
    "CreateMeetingResponseTypeDef",
    "OrderedPhoneNumberTypeDef",
    "PhoneNumberOrderTypeDef",
    "CreatePhoneNumberOrderResponseTypeDef",
    "MemberTypeDef",
    "RoomMembershipTypeDef",
    "CreateRoomMembershipResponseTypeDef",
    "RoomTypeDef",
    "CreateRoomResponseTypeDef",
    "UserTypeDef",
    "CreateUserResponseTypeDef",
    "VoiceConnectorItemTypeDef",
    "VoiceConnectorGroupTypeDef",
    "CreateVoiceConnectorGroupResponseTypeDef",
    "VoiceConnectorTypeDef",
    "CreateVoiceConnectorResponseTypeDef",
    "CredentialTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef",
    "GetAccountResponseTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "GetAttendeeResponseTypeDef",
    "GetBotResponseTypeDef",
    "EventsConfigurationTypeDef",
    "GetEventsConfigurationResponseTypeDef",
    "VoiceConnectorSettingsTypeDef",
    "GetGlobalSettingsResponseTypeDef",
    "GetMeetingResponseTypeDef",
    "GetPhoneNumberOrderResponseTypeDef",
    "PhoneNumberAssociationTypeDef",
    "PhoneNumberCapabilitiesTypeDef",
    "PhoneNumberTypeDef",
    "GetPhoneNumberResponseTypeDef",
    "GetPhoneNumberSettingsResponseTypeDef",
    "GetRoomResponseTypeDef",
    "GetUserResponseTypeDef",
    "TelephonySettingsTypeDef",
    "UserSettingsTypeDef",
    "GetUserSettingsResponseTypeDef",
    "GetVoiceConnectorGroupResponseTypeDef",
    "LoggingConfigurationTypeDef",
    "GetVoiceConnectorLoggingConfigurationResponseTypeDef",
    "OriginationRouteTypeDef",
    "OriginationTypeDef",
    "GetVoiceConnectorOriginationResponseTypeDef",
    "GetVoiceConnectorResponseTypeDef",
    "StreamingConfigurationTypeDef",
    "GetVoiceConnectorStreamingConfigurationResponseTypeDef",
    "TerminationHealthTypeDef",
    "GetVoiceConnectorTerminationHealthResponseTypeDef",
    "TerminationTypeDef",
    "GetVoiceConnectorTerminationResponseTypeDef",
    "InviteTypeDef",
    "InviteUsersResponseTypeDef",
    "ListAccountsResponseTypeDef",
    "ListAttendeesResponseTypeDef",
    "ListBotsResponseTypeDef",
    "ListMeetingsResponseTypeDef",
    "ListPhoneNumberOrdersResponseTypeDef",
    "ListPhoneNumbersResponseTypeDef",
    "ListRoomMembershipsResponseTypeDef",
    "ListRoomsResponseTypeDef",
    "ListUsersResponseTypeDef",
    "ListVoiceConnectorGroupsResponseTypeDef",
    "ListVoiceConnectorTerminationCredentialsResponseTypeDef",
    "ListVoiceConnectorsResponseTypeDef",
    "MeetingNotificationConfigurationTypeDef",
    "MembershipItemTypeDef",
    "PaginatorConfigTypeDef",
    "PutEventsConfigurationResponseTypeDef",
    "PutVoiceConnectorLoggingConfigurationResponseTypeDef",
    "PutVoiceConnectorOriginationResponseTypeDef",
    "PutVoiceConnectorStreamingConfigurationResponseTypeDef",
    "PutVoiceConnectorTerminationResponseTypeDef",
    "RegenerateSecurityTokenResponseTypeDef",
    "ResetPersonalPINResponseTypeDef",
    "RestorePhoneNumberResponseTypeDef",
    "SearchAvailablePhoneNumbersResponseTypeDef",
    "UpdateAccountResponseTypeDef",
    "UpdateBotResponseTypeDef",
    "UpdatePhoneNumberRequestItemTypeDef",
    "UpdatePhoneNumberResponseTypeDef",
    "UpdateRoomMembershipResponseTypeDef",
    "UpdateRoomResponseTypeDef",
    "UpdateUserRequestItemTypeDef",
    "UpdateUserResponseTypeDef",
    "UpdateVoiceConnectorGroupResponseTypeDef",
    "UpdateVoiceConnectorResponseTypeDef",
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef", {"DisableRemoteControl": bool, "EnableDialOut": bool}, total=False
)

AlexaForBusinessMetadataTypeDef = TypedDict(
    "AlexaForBusinessMetadataTypeDef",
    {"IsAlexaForBusinessEnabled": bool, "AlexaForBusinessRoomArn": str},
    total=False,
)

PhoneNumberErrorTypeDef = TypedDict(
    "PhoneNumberErrorTypeDef",
    {
        "PhoneNumberId": str,
        "ErrorCode": Literal[
            "BadRequest",
            "Conflict",
            "Forbidden",
            "NotFound",
            "PreconditionFailed",
            "ResourceLimitExceeded",
            "ServiceFailure",
            "AccessDenied",
            "ServiceUnavailable",
            "Throttled",
            "Unauthorized",
            "Unprocessable",
            "VoiceConnectorGroupAssociationsExist",
            "PhoneNumberAssociationsExist",
        ],
        "ErrorMessage": str,
    },
    total=False,
)

AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef = TypedDict(
    "AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef",
    {"PhoneNumberErrors": List[PhoneNumberErrorTypeDef]},
    total=False,
)

AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef = TypedDict(
    "AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef",
    {"PhoneNumberErrors": List[PhoneNumberErrorTypeDef]},
    total=False,
)

AttendeeTypeDef = TypedDict(
    "AttendeeTypeDef", {"ExternalUserId": str, "AttendeeId": str, "JoinToken": str}, total=False
)

CreateAttendeeErrorTypeDef = TypedDict(
    "CreateAttendeeErrorTypeDef",
    {"ExternalUserId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

BatchCreateAttendeeResponseTypeDef = TypedDict(
    "BatchCreateAttendeeResponseTypeDef",
    {"Attendees": List[AttendeeTypeDef], "Errors": List[CreateAttendeeErrorTypeDef]},
    total=False,
)

MemberErrorTypeDef = TypedDict(
    "MemberErrorTypeDef",
    {
        "MemberId": str,
        "ErrorCode": Literal[
            "BadRequest",
            "Conflict",
            "Forbidden",
            "NotFound",
            "PreconditionFailed",
            "ResourceLimitExceeded",
            "ServiceFailure",
            "AccessDenied",
            "ServiceUnavailable",
            "Throttled",
            "Unauthorized",
            "Unprocessable",
            "VoiceConnectorGroupAssociationsExist",
            "PhoneNumberAssociationsExist",
        ],
        "ErrorMessage": str,
    },
    total=False,
)

BatchCreateRoomMembershipResponseTypeDef = TypedDict(
    "BatchCreateRoomMembershipResponseTypeDef", {"Errors": List[MemberErrorTypeDef]}, total=False
)

BatchDeletePhoneNumberResponseTypeDef = TypedDict(
    "BatchDeletePhoneNumberResponseTypeDef",
    {"PhoneNumberErrors": List[PhoneNumberErrorTypeDef]},
    total=False,
)

UserErrorTypeDef = TypedDict(
    "UserErrorTypeDef",
    {
        "UserId": str,
        "ErrorCode": Literal[
            "BadRequest",
            "Conflict",
            "Forbidden",
            "NotFound",
            "PreconditionFailed",
            "ResourceLimitExceeded",
            "ServiceFailure",
            "AccessDenied",
            "ServiceUnavailable",
            "Throttled",
            "Unauthorized",
            "Unprocessable",
            "VoiceConnectorGroupAssociationsExist",
            "PhoneNumberAssociationsExist",
        ],
        "ErrorMessage": str,
    },
    total=False,
)

BatchSuspendUserResponseTypeDef = TypedDict(
    "BatchSuspendUserResponseTypeDef", {"UserErrors": List[UserErrorTypeDef]}, total=False
)

BatchUnsuspendUserResponseTypeDef = TypedDict(
    "BatchUnsuspendUserResponseTypeDef", {"UserErrors": List[UserErrorTypeDef]}, total=False
)

BatchUpdatePhoneNumberResponseTypeDef = TypedDict(
    "BatchUpdatePhoneNumberResponseTypeDef",
    {"PhoneNumberErrors": List[PhoneNumberErrorTypeDef]},
    total=False,
)

BatchUpdateUserResponseTypeDef = TypedDict(
    "BatchUpdateUserResponseTypeDef", {"UserErrors": List[UserErrorTypeDef]}, total=False
)

BusinessCallingSettingsTypeDef = TypedDict(
    "BusinessCallingSettingsTypeDef", {"CdrBucket": str}, total=False
)

SigninDelegateGroupTypeDef = TypedDict(
    "SigninDelegateGroupTypeDef", {"GroupName": str}, total=False
)

_RequiredAccountTypeDef = TypedDict(
    "_RequiredAccountTypeDef", {"AwsAccountId": str, "AccountId": str, "Name": str}
)
_OptionalAccountTypeDef = TypedDict(
    "_OptionalAccountTypeDef",
    {
        "AccountType": Literal["Team", "EnterpriseDirectory", "EnterpriseLWA", "EnterpriseOIDC"],
        "CreatedTimestamp": datetime,
        "DefaultLicense": Literal["Basic", "Plus", "Pro", "ProTrial"],
        "SupportedLicenses": List[Literal["Basic", "Plus", "Pro", "ProTrial"]],
        "SigninDelegateGroups": List[SigninDelegateGroupTypeDef],
    },
    total=False,
)


class AccountTypeDef(_RequiredAccountTypeDef, _OptionalAccountTypeDef):
    pass


CreateAccountResponseTypeDef = TypedDict(
    "CreateAccountResponseTypeDef", {"Account": AccountTypeDef}, total=False
)

CreateAttendeeRequestItemTypeDef = TypedDict(
    "CreateAttendeeRequestItemTypeDef", {"ExternalUserId": str}
)

CreateAttendeeResponseTypeDef = TypedDict(
    "CreateAttendeeResponseTypeDef", {"Attendee": AttendeeTypeDef}, total=False
)

BotTypeDef = TypedDict(
    "BotTypeDef",
    {
        "BotId": str,
        "UserId": str,
        "DisplayName": str,
        "BotType": Literal["ChatBot"],
        "Disabled": bool,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "BotEmail": str,
        "SecurityToken": str,
    },
    total=False,
)

CreateBotResponseTypeDef = TypedDict("CreateBotResponseTypeDef", {"Bot": BotTypeDef}, total=False)

MediaPlacementTypeDef = TypedDict(
    "MediaPlacementTypeDef",
    {
        "AudioHostUrl": str,
        "AudioFallbackUrl": str,
        "ScreenDataUrl": str,
        "ScreenSharingUrl": str,
        "ScreenViewingUrl": str,
        "SignalingUrl": str,
        "TurnControlUrl": str,
    },
    total=False,
)

MeetingTypeDef = TypedDict(
    "MeetingTypeDef",
    {"MeetingId": str, "MediaPlacement": MediaPlacementTypeDef, "MediaRegion": str},
    total=False,
)

CreateMeetingResponseTypeDef = TypedDict(
    "CreateMeetingResponseTypeDef", {"Meeting": MeetingTypeDef}, total=False
)

OrderedPhoneNumberTypeDef = TypedDict(
    "OrderedPhoneNumberTypeDef",
    {"E164PhoneNumber": str, "Status": Literal["Processing", "Acquired", "Failed"]},
    total=False,
)

PhoneNumberOrderTypeDef = TypedDict(
    "PhoneNumberOrderTypeDef",
    {
        "PhoneNumberOrderId": str,
        "ProductType": Literal["BusinessCalling", "VoiceConnector"],
        "Status": Literal["Processing", "Successful", "Failed", "Partial"],
        "OrderedPhoneNumbers": List[OrderedPhoneNumberTypeDef],
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

CreatePhoneNumberOrderResponseTypeDef = TypedDict(
    "CreatePhoneNumberOrderResponseTypeDef",
    {"PhoneNumberOrder": PhoneNumberOrderTypeDef},
    total=False,
)

MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "MemberId": str,
        "MemberType": Literal["User", "Bot", "Webhook"],
        "Email": str,
        "FullName": str,
        "AccountId": str,
    },
    total=False,
)

RoomMembershipTypeDef = TypedDict(
    "RoomMembershipTypeDef",
    {
        "RoomId": str,
        "Member": MemberTypeDef,
        "Role": Literal["Administrator", "Member"],
        "InvitedBy": str,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

CreateRoomMembershipResponseTypeDef = TypedDict(
    "CreateRoomMembershipResponseTypeDef", {"RoomMembership": RoomMembershipTypeDef}, total=False
)

RoomTypeDef = TypedDict(
    "RoomTypeDef",
    {
        "RoomId": str,
        "Name": str,
        "AccountId": str,
        "CreatedBy": str,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

CreateRoomResponseTypeDef = TypedDict(
    "CreateRoomResponseTypeDef", {"Room": RoomTypeDef}, total=False
)

_RequiredUserTypeDef = TypedDict("_RequiredUserTypeDef", {"UserId": str})
_OptionalUserTypeDef = TypedDict(
    "_OptionalUserTypeDef",
    {
        "AccountId": str,
        "PrimaryEmail": str,
        "PrimaryProvisionedNumber": str,
        "DisplayName": str,
        "LicenseType": Literal["Basic", "Plus", "Pro", "ProTrial"],
        "UserType": Literal["PrivateUser", "SharedDevice"],
        "UserRegistrationStatus": Literal["Unregistered", "Registered", "Suspended"],
        "UserInvitationStatus": Literal["Pending", "Accepted", "Failed"],
        "RegisteredOn": datetime,
        "InvitedOn": datetime,
        "AlexaForBusinessMetadata": AlexaForBusinessMetadataTypeDef,
        "PersonalPIN": str,
    },
    total=False,
)


class UserTypeDef(_RequiredUserTypeDef, _OptionalUserTypeDef):
    pass


CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef", {"User": UserTypeDef}, total=False
)

VoiceConnectorItemTypeDef = TypedDict(
    "VoiceConnectorItemTypeDef", {"VoiceConnectorId": str, "Priority": int}
)

VoiceConnectorGroupTypeDef = TypedDict(
    "VoiceConnectorGroupTypeDef",
    {
        "VoiceConnectorGroupId": str,
        "Name": str,
        "VoiceConnectorItems": List[VoiceConnectorItemTypeDef],
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

CreateVoiceConnectorGroupResponseTypeDef = TypedDict(
    "CreateVoiceConnectorGroupResponseTypeDef",
    {"VoiceConnectorGroup": VoiceConnectorGroupTypeDef},
    total=False,
)

VoiceConnectorTypeDef = TypedDict(
    "VoiceConnectorTypeDef",
    {
        "VoiceConnectorId": str,
        "AwsRegion": Literal["us-east-1", "us-west-2"],
        "Name": str,
        "OutboundHostName": str,
        "RequireEncryption": bool,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

CreateVoiceConnectorResponseTypeDef = TypedDict(
    "CreateVoiceConnectorResponseTypeDef", {"VoiceConnector": VoiceConnectorTypeDef}, total=False
)

CredentialTypeDef = TypedDict("CredentialTypeDef", {"Username": str, "Password": str}, total=False)

DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef = TypedDict(
    "DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef",
    {"PhoneNumberErrors": List[PhoneNumberErrorTypeDef]},
    total=False,
)

DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef = TypedDict(
    "DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef",
    {"PhoneNumberErrors": List[PhoneNumberErrorTypeDef]},
    total=False,
)

GetAccountResponseTypeDef = TypedDict(
    "GetAccountResponseTypeDef", {"Account": AccountTypeDef}, total=False
)

GetAccountSettingsResponseTypeDef = TypedDict(
    "GetAccountSettingsResponseTypeDef", {"AccountSettings": AccountSettingsTypeDef}, total=False
)

GetAttendeeResponseTypeDef = TypedDict(
    "GetAttendeeResponseTypeDef", {"Attendee": AttendeeTypeDef}, total=False
)

GetBotResponseTypeDef = TypedDict("GetBotResponseTypeDef", {"Bot": BotTypeDef}, total=False)

EventsConfigurationTypeDef = TypedDict(
    "EventsConfigurationTypeDef",
    {"BotId": str, "OutboundEventsHTTPSEndpoint": str, "LambdaFunctionArn": str},
    total=False,
)

GetEventsConfigurationResponseTypeDef = TypedDict(
    "GetEventsConfigurationResponseTypeDef",
    {"EventsConfiguration": EventsConfigurationTypeDef},
    total=False,
)

VoiceConnectorSettingsTypeDef = TypedDict(
    "VoiceConnectorSettingsTypeDef", {"CdrBucket": str}, total=False
)

GetGlobalSettingsResponseTypeDef = TypedDict(
    "GetGlobalSettingsResponseTypeDef",
    {
        "BusinessCalling": BusinessCallingSettingsTypeDef,
        "VoiceConnector": VoiceConnectorSettingsTypeDef,
    },
    total=False,
)

GetMeetingResponseTypeDef = TypedDict(
    "GetMeetingResponseTypeDef", {"Meeting": MeetingTypeDef}, total=False
)

GetPhoneNumberOrderResponseTypeDef = TypedDict(
    "GetPhoneNumberOrderResponseTypeDef", {"PhoneNumberOrder": PhoneNumberOrderTypeDef}, total=False
)

PhoneNumberAssociationTypeDef = TypedDict(
    "PhoneNumberAssociationTypeDef",
    {
        "Value": str,
        "Name": Literal["AccountId", "UserId", "VoiceConnectorId", "VoiceConnectorGroupId"],
        "AssociatedTimestamp": datetime,
    },
    total=False,
)

PhoneNumberCapabilitiesTypeDef = TypedDict(
    "PhoneNumberCapabilitiesTypeDef",
    {
        "InboundCall": bool,
        "OutboundCall": bool,
        "InboundSMS": bool,
        "OutboundSMS": bool,
        "InboundMMS": bool,
        "OutboundMMS": bool,
    },
    total=False,
)

PhoneNumberTypeDef = TypedDict(
    "PhoneNumberTypeDef",
    {
        "PhoneNumberId": str,
        "E164PhoneNumber": str,
        "Type": Literal["Local", "TollFree"],
        "ProductType": Literal["BusinessCalling", "VoiceConnector"],
        "Status": Literal[
            "AcquireInProgress",
            "AcquireFailed",
            "Unassigned",
            "Assigned",
            "ReleaseInProgress",
            "DeleteInProgress",
            "ReleaseFailed",
            "DeleteFailed",
        ],
        "Capabilities": PhoneNumberCapabilitiesTypeDef,
        "Associations": List[PhoneNumberAssociationTypeDef],
        "CallingName": str,
        "CallingNameStatus": Literal[
            "Unassigned", "UpdateInProgress", "UpdateSucceeded", "UpdateFailed"
        ],
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "DeletionTimestamp": datetime,
    },
    total=False,
)

GetPhoneNumberResponseTypeDef = TypedDict(
    "GetPhoneNumberResponseTypeDef", {"PhoneNumber": PhoneNumberTypeDef}, total=False
)

GetPhoneNumberSettingsResponseTypeDef = TypedDict(
    "GetPhoneNumberSettingsResponseTypeDef",
    {"CallingName": str, "CallingNameUpdatedTimestamp": datetime},
    total=False,
)

GetRoomResponseTypeDef = TypedDict("GetRoomResponseTypeDef", {"Room": RoomTypeDef}, total=False)

GetUserResponseTypeDef = TypedDict("GetUserResponseTypeDef", {"User": UserTypeDef}, total=False)

TelephonySettingsTypeDef = TypedDict(
    "TelephonySettingsTypeDef", {"InboundCalling": bool, "OutboundCalling": bool, "SMS": bool}
)

UserSettingsTypeDef = TypedDict("UserSettingsTypeDef", {"Telephony": TelephonySettingsTypeDef})

GetUserSettingsResponseTypeDef = TypedDict(
    "GetUserSettingsResponseTypeDef", {"UserSettings": UserSettingsTypeDef}, total=False
)

GetVoiceConnectorGroupResponseTypeDef = TypedDict(
    "GetVoiceConnectorGroupResponseTypeDef",
    {"VoiceConnectorGroup": VoiceConnectorGroupTypeDef},
    total=False,
)

LoggingConfigurationTypeDef = TypedDict(
    "LoggingConfigurationTypeDef", {"EnableSIPLogs": bool}, total=False
)

GetVoiceConnectorLoggingConfigurationResponseTypeDef = TypedDict(
    "GetVoiceConnectorLoggingConfigurationResponseTypeDef",
    {"LoggingConfiguration": LoggingConfigurationTypeDef},
    total=False,
)

OriginationRouteTypeDef = TypedDict(
    "OriginationRouteTypeDef",
    {"Host": str, "Port": int, "Protocol": Literal["TCP", "UDP"], "Priority": int, "Weight": int},
    total=False,
)

OriginationTypeDef = TypedDict(
    "OriginationTypeDef", {"Routes": List[OriginationRouteTypeDef], "Disabled": bool}, total=False
)

GetVoiceConnectorOriginationResponseTypeDef = TypedDict(
    "GetVoiceConnectorOriginationResponseTypeDef", {"Origination": OriginationTypeDef}, total=False
)

GetVoiceConnectorResponseTypeDef = TypedDict(
    "GetVoiceConnectorResponseTypeDef", {"VoiceConnector": VoiceConnectorTypeDef}, total=False
)

_RequiredStreamingConfigurationTypeDef = TypedDict(
    "_RequiredStreamingConfigurationTypeDef", {"DataRetentionInHours": int}
)
_OptionalStreamingConfigurationTypeDef = TypedDict(
    "_OptionalStreamingConfigurationTypeDef", {"Disabled": bool}, total=False
)


class StreamingConfigurationTypeDef(
    _RequiredStreamingConfigurationTypeDef, _OptionalStreamingConfigurationTypeDef
):
    pass


GetVoiceConnectorStreamingConfigurationResponseTypeDef = TypedDict(
    "GetVoiceConnectorStreamingConfigurationResponseTypeDef",
    {"StreamingConfiguration": StreamingConfigurationTypeDef},
    total=False,
)

TerminationHealthTypeDef = TypedDict(
    "TerminationHealthTypeDef", {"Timestamp": datetime, "Source": str}, total=False
)

GetVoiceConnectorTerminationHealthResponseTypeDef = TypedDict(
    "GetVoiceConnectorTerminationHealthResponseTypeDef",
    {"TerminationHealth": TerminationHealthTypeDef},
    total=False,
)

TerminationTypeDef = TypedDict(
    "TerminationTypeDef",
    {
        "CpsLimit": int,
        "DefaultPhoneNumber": str,
        "CallingRegions": List[str],
        "CidrAllowedList": List[str],
        "Disabled": bool,
    },
    total=False,
)

GetVoiceConnectorTerminationResponseTypeDef = TypedDict(
    "GetVoiceConnectorTerminationResponseTypeDef", {"Termination": TerminationTypeDef}, total=False
)

InviteTypeDef = TypedDict(
    "InviteTypeDef",
    {
        "InviteId": str,
        "Status": Literal["Pending", "Accepted", "Failed"],
        "EmailAddress": str,
        "EmailStatus": Literal["NotSent", "Sent", "Failed"],
    },
    total=False,
)

InviteUsersResponseTypeDef = TypedDict(
    "InviteUsersResponseTypeDef", {"Invites": List[InviteTypeDef]}, total=False
)

ListAccountsResponseTypeDef = TypedDict(
    "ListAccountsResponseTypeDef", {"Accounts": List[AccountTypeDef], "NextToken": str}, total=False
)

ListAttendeesResponseTypeDef = TypedDict(
    "ListAttendeesResponseTypeDef",
    {"Attendees": List[AttendeeTypeDef], "NextToken": str},
    total=False,
)

ListBotsResponseTypeDef = TypedDict(
    "ListBotsResponseTypeDef", {"Bots": List[BotTypeDef], "NextToken": str}, total=False
)

ListMeetingsResponseTypeDef = TypedDict(
    "ListMeetingsResponseTypeDef", {"Meetings": List[MeetingTypeDef], "NextToken": str}, total=False
)

ListPhoneNumberOrdersResponseTypeDef = TypedDict(
    "ListPhoneNumberOrdersResponseTypeDef",
    {"PhoneNumberOrders": List[PhoneNumberOrderTypeDef], "NextToken": str},
    total=False,
)

ListPhoneNumbersResponseTypeDef = TypedDict(
    "ListPhoneNumbersResponseTypeDef",
    {"PhoneNumbers": List[PhoneNumberTypeDef], "NextToken": str},
    total=False,
)

ListRoomMembershipsResponseTypeDef = TypedDict(
    "ListRoomMembershipsResponseTypeDef",
    {"RoomMemberships": List[RoomMembershipTypeDef], "NextToken": str},
    total=False,
)

ListRoomsResponseTypeDef = TypedDict(
    "ListRoomsResponseTypeDef", {"Rooms": List[RoomTypeDef], "NextToken": str}, total=False
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef", {"Users": List[UserTypeDef], "NextToken": str}, total=False
)

ListVoiceConnectorGroupsResponseTypeDef = TypedDict(
    "ListVoiceConnectorGroupsResponseTypeDef",
    {"VoiceConnectorGroups": List[VoiceConnectorGroupTypeDef], "NextToken": str},
    total=False,
)

ListVoiceConnectorTerminationCredentialsResponseTypeDef = TypedDict(
    "ListVoiceConnectorTerminationCredentialsResponseTypeDef", {"Usernames": List[str]}, total=False
)

ListVoiceConnectorsResponseTypeDef = TypedDict(
    "ListVoiceConnectorsResponseTypeDef",
    {"VoiceConnectors": List[VoiceConnectorTypeDef], "NextToken": str},
    total=False,
)

MeetingNotificationConfigurationTypeDef = TypedDict(
    "MeetingNotificationConfigurationTypeDef", {"SnsTopicArn": str, "SqsQueueArn": str}, total=False
)

MembershipItemTypeDef = TypedDict(
    "MembershipItemTypeDef",
    {"MemberId": str, "Role": Literal["Administrator", "Member"]},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutEventsConfigurationResponseTypeDef = TypedDict(
    "PutEventsConfigurationResponseTypeDef",
    {"EventsConfiguration": EventsConfigurationTypeDef},
    total=False,
)

PutVoiceConnectorLoggingConfigurationResponseTypeDef = TypedDict(
    "PutVoiceConnectorLoggingConfigurationResponseTypeDef",
    {"LoggingConfiguration": LoggingConfigurationTypeDef},
    total=False,
)

PutVoiceConnectorOriginationResponseTypeDef = TypedDict(
    "PutVoiceConnectorOriginationResponseTypeDef", {"Origination": OriginationTypeDef}, total=False
)

PutVoiceConnectorStreamingConfigurationResponseTypeDef = TypedDict(
    "PutVoiceConnectorStreamingConfigurationResponseTypeDef",
    {"StreamingConfiguration": StreamingConfigurationTypeDef},
    total=False,
)

PutVoiceConnectorTerminationResponseTypeDef = TypedDict(
    "PutVoiceConnectorTerminationResponseTypeDef", {"Termination": TerminationTypeDef}, total=False
)

RegenerateSecurityTokenResponseTypeDef = TypedDict(
    "RegenerateSecurityTokenResponseTypeDef", {"Bot": BotTypeDef}, total=False
)

ResetPersonalPINResponseTypeDef = TypedDict(
    "ResetPersonalPINResponseTypeDef", {"User": UserTypeDef}, total=False
)

RestorePhoneNumberResponseTypeDef = TypedDict(
    "RestorePhoneNumberResponseTypeDef", {"PhoneNumber": PhoneNumberTypeDef}, total=False
)

SearchAvailablePhoneNumbersResponseTypeDef = TypedDict(
    "SearchAvailablePhoneNumbersResponseTypeDef", {"E164PhoneNumbers": List[str]}, total=False
)

UpdateAccountResponseTypeDef = TypedDict(
    "UpdateAccountResponseTypeDef", {"Account": AccountTypeDef}, total=False
)

UpdateBotResponseTypeDef = TypedDict("UpdateBotResponseTypeDef", {"Bot": BotTypeDef}, total=False)

_RequiredUpdatePhoneNumberRequestItemTypeDef = TypedDict(
    "_RequiredUpdatePhoneNumberRequestItemTypeDef", {"PhoneNumberId": str}
)
_OptionalUpdatePhoneNumberRequestItemTypeDef = TypedDict(
    "_OptionalUpdatePhoneNumberRequestItemTypeDef",
    {"ProductType": Literal["BusinessCalling", "VoiceConnector"], "CallingName": str},
    total=False,
)


class UpdatePhoneNumberRequestItemTypeDef(
    _RequiredUpdatePhoneNumberRequestItemTypeDef, _OptionalUpdatePhoneNumberRequestItemTypeDef
):
    pass


UpdatePhoneNumberResponseTypeDef = TypedDict(
    "UpdatePhoneNumberResponseTypeDef", {"PhoneNumber": PhoneNumberTypeDef}, total=False
)

UpdateRoomMembershipResponseTypeDef = TypedDict(
    "UpdateRoomMembershipResponseTypeDef", {"RoomMembership": RoomMembershipTypeDef}, total=False
)

UpdateRoomResponseTypeDef = TypedDict(
    "UpdateRoomResponseTypeDef", {"Room": RoomTypeDef}, total=False
)

_RequiredUpdateUserRequestItemTypeDef = TypedDict(
    "_RequiredUpdateUserRequestItemTypeDef", {"UserId": str}
)
_OptionalUpdateUserRequestItemTypeDef = TypedDict(
    "_OptionalUpdateUserRequestItemTypeDef",
    {
        "LicenseType": Literal["Basic", "Plus", "Pro", "ProTrial"],
        "UserType": Literal["PrivateUser", "SharedDevice"],
        "AlexaForBusinessMetadata": AlexaForBusinessMetadataTypeDef,
    },
    total=False,
)


class UpdateUserRequestItemTypeDef(
    _RequiredUpdateUserRequestItemTypeDef, _OptionalUpdateUserRequestItemTypeDef
):
    pass


UpdateUserResponseTypeDef = TypedDict(
    "UpdateUserResponseTypeDef", {"User": UserTypeDef}, total=False
)

UpdateVoiceConnectorGroupResponseTypeDef = TypedDict(
    "UpdateVoiceConnectorGroupResponseTypeDef",
    {"VoiceConnectorGroup": VoiceConnectorGroupTypeDef},
    total=False,
)

UpdateVoiceConnectorResponseTypeDef = TypedDict(
    "UpdateVoiceConnectorResponseTypeDef", {"VoiceConnector": VoiceConnectorTypeDef}, total=False
)
