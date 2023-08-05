"""
Main interface for alexaforbusiness service type definitions.

Usage::

    from mypy_boto3.alexaforbusiness.type_defs import BusinessReportContentRangeTypeDef

    data: BusinessReportContentRangeTypeDef = {...}
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
    "BusinessReportContentRangeTypeDef",
    "BusinessReportRecurrenceTypeDef",
    "ConferencePreferenceTypeDef",
    "AudioTypeDef",
    "SsmlTypeDef",
    "TextTypeDef",
    "ContentTypeDef",
    "CreateAddressBookResponseTypeDef",
    "CreateBusinessReportScheduleResponseTypeDef",
    "CreateConferenceProviderResponseTypeDef",
    "CreateContactResponseTypeDef",
    "CreateGatewayGroupResponseTypeDef",
    "CreateEndOfMeetingReminderTypeDef",
    "CreateInstantBookingTypeDef",
    "CreateRequireCheckInTypeDef",
    "CreateMeetingRoomConfigurationTypeDef",
    "CreateNetworkProfileResponseTypeDef",
    "CreateProfileResponseTypeDef",
    "CreateRoomResponseTypeDef",
    "CreateSkillGroupResponseTypeDef",
    "CreateUserResponseTypeDef",
    "FilterTypeDef",
    "AddressBookTypeDef",
    "GetAddressBookResponseTypeDef",
    "GetConferencePreferenceResponseTypeDef",
    "IPDialInTypeDef",
    "MeetingSettingTypeDef",
    "PSTNDialInTypeDef",
    "ConferenceProviderTypeDef",
    "GetConferenceProviderResponseTypeDef",
    "PhoneNumberTypeDef",
    "SipAddressTypeDef",
    "ContactTypeDef",
    "GetContactResponseTypeDef",
    "DeviceNetworkProfileInfoTypeDef",
    "DeviceStatusDetailTypeDef",
    "DeviceStatusInfoTypeDef",
    "DeviceTypeDef",
    "GetDeviceResponseTypeDef",
    "GatewayGroupTypeDef",
    "GetGatewayGroupResponseTypeDef",
    "GatewayTypeDef",
    "GetGatewayResponseTypeDef",
    "GetInvitationConfigurationResponseTypeDef",
    "NetworkProfileTypeDef",
    "GetNetworkProfileResponseTypeDef",
    "EndOfMeetingReminderTypeDef",
    "InstantBookingTypeDef",
    "RequireCheckInTypeDef",
    "MeetingRoomConfigurationTypeDef",
    "ProfileTypeDef",
    "GetProfileResponseTypeDef",
    "RoomTypeDef",
    "GetRoomResponseTypeDef",
    "RoomSkillParameterTypeDef",
    "GetRoomSkillParameterResponseTypeDef",
    "SkillGroupTypeDef",
    "GetSkillGroupResponseTypeDef",
    "BusinessReportS3LocationTypeDef",
    "BusinessReportTypeDef",
    "BusinessReportScheduleTypeDef",
    "ListBusinessReportSchedulesResponseTypeDef",
    "ListConferenceProvidersResponseTypeDef",
    "DeviceEventTypeDef",
    "ListDeviceEventsResponseTypeDef",
    "GatewayGroupSummaryTypeDef",
    "ListGatewayGroupsResponseTypeDef",
    "GatewaySummaryTypeDef",
    "ListGatewaysResponseTypeDef",
    "SkillSummaryTypeDef",
    "ListSkillsResponseTypeDef",
    "CategoryTypeDef",
    "ListSkillsStoreCategoriesResponseTypeDef",
    "DeveloperInfoTypeDef",
    "SkillDetailsTypeDef",
    "SkillsStoreSkillTypeDef",
    "ListSkillsStoreSkillsByCategoryResponseTypeDef",
    "SmartHomeApplianceTypeDef",
    "ListSmartHomeAppliancesResponseTypeDef",
    "TagTypeDef",
    "ListTagsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RegisterAVSDeviceResponseTypeDef",
    "ResolveRoomResponseTypeDef",
    "AddressBookDataTypeDef",
    "SearchAddressBooksResponseTypeDef",
    "ContactDataTypeDef",
    "SearchContactsResponseTypeDef",
    "DeviceDataTypeDef",
    "SearchDevicesResponseTypeDef",
    "NetworkProfileDataTypeDef",
    "SearchNetworkProfilesResponseTypeDef",
    "ProfileDataTypeDef",
    "SearchProfilesResponseTypeDef",
    "RoomDataTypeDef",
    "SearchRoomsResponseTypeDef",
    "SkillGroupDataTypeDef",
    "SearchSkillGroupsResponseTypeDef",
    "UserDataTypeDef",
    "SearchUsersResponseTypeDef",
    "SendAnnouncementResponseTypeDef",
    "SortTypeDef",
    "UpdateEndOfMeetingReminderTypeDef",
    "UpdateInstantBookingTypeDef",
    "UpdateRequireCheckInTypeDef",
    "UpdateMeetingRoomConfigurationTypeDef",
)

BusinessReportContentRangeTypeDef = TypedDict(
    "BusinessReportContentRangeTypeDef",
    {"Interval": Literal["ONE_DAY", "ONE_WEEK", "THIRTY_DAYS"]},
    total=False,
)

BusinessReportRecurrenceTypeDef = TypedDict(
    "BusinessReportRecurrenceTypeDef", {"StartDate": str}, total=False
)

ConferencePreferenceTypeDef = TypedDict(
    "ConferencePreferenceTypeDef", {"DefaultConferenceProviderArn": str}, total=False
)

AudioTypeDef = TypedDict("AudioTypeDef", {"Locale": Literal["en-US"], "Location": str})

SsmlTypeDef = TypedDict("SsmlTypeDef", {"Locale": Literal["en-US"], "Value": str})

TextTypeDef = TypedDict("TextTypeDef", {"Locale": Literal["en-US"], "Value": str})

ContentTypeDef = TypedDict(
    "ContentTypeDef",
    {"TextList": List[TextTypeDef], "SsmlList": List[SsmlTypeDef], "AudioList": List[AudioTypeDef]},
    total=False,
)

CreateAddressBookResponseTypeDef = TypedDict(
    "CreateAddressBookResponseTypeDef", {"AddressBookArn": str}, total=False
)

CreateBusinessReportScheduleResponseTypeDef = TypedDict(
    "CreateBusinessReportScheduleResponseTypeDef", {"ScheduleArn": str}, total=False
)

CreateConferenceProviderResponseTypeDef = TypedDict(
    "CreateConferenceProviderResponseTypeDef", {"ConferenceProviderArn": str}, total=False
)

CreateContactResponseTypeDef = TypedDict(
    "CreateContactResponseTypeDef", {"ContactArn": str}, total=False
)

CreateGatewayGroupResponseTypeDef = TypedDict(
    "CreateGatewayGroupResponseTypeDef", {"GatewayGroupArn": str}, total=False
)

CreateEndOfMeetingReminderTypeDef = TypedDict(
    "CreateEndOfMeetingReminderTypeDef",
    {
        "ReminderAtMinutes": List[int],
        "ReminderType": Literal[
            "ANNOUNCEMENT_TIME_CHECK", "ANNOUNCEMENT_VARIABLE_TIME_LEFT", "CHIME", "KNOCK"
        ],
        "Enabled": bool,
    },
)

CreateInstantBookingTypeDef = TypedDict(
    "CreateInstantBookingTypeDef", {"DurationInMinutes": int, "Enabled": bool}
)

CreateRequireCheckInTypeDef = TypedDict(
    "CreateRequireCheckInTypeDef", {"ReleaseAfterMinutes": int, "Enabled": bool}
)

CreateMeetingRoomConfigurationTypeDef = TypedDict(
    "CreateMeetingRoomConfigurationTypeDef",
    {
        "RoomUtilizationMetricsEnabled": bool,
        "EndOfMeetingReminder": CreateEndOfMeetingReminderTypeDef,
        "InstantBooking": CreateInstantBookingTypeDef,
        "RequireCheckIn": CreateRequireCheckInTypeDef,
    },
    total=False,
)

CreateNetworkProfileResponseTypeDef = TypedDict(
    "CreateNetworkProfileResponseTypeDef", {"NetworkProfileArn": str}, total=False
)

CreateProfileResponseTypeDef = TypedDict(
    "CreateProfileResponseTypeDef", {"ProfileArn": str}, total=False
)

CreateRoomResponseTypeDef = TypedDict("CreateRoomResponseTypeDef", {"RoomArn": str}, total=False)

CreateSkillGroupResponseTypeDef = TypedDict(
    "CreateSkillGroupResponseTypeDef", {"SkillGroupArn": str}, total=False
)

CreateUserResponseTypeDef = TypedDict("CreateUserResponseTypeDef", {"UserArn": str}, total=False)

FilterTypeDef = TypedDict("FilterTypeDef", {"Key": str, "Values": List[str]})

AddressBookTypeDef = TypedDict(
    "AddressBookTypeDef", {"AddressBookArn": str, "Name": str, "Description": str}, total=False
)

GetAddressBookResponseTypeDef = TypedDict(
    "GetAddressBookResponseTypeDef", {"AddressBook": AddressBookTypeDef}, total=False
)

GetConferencePreferenceResponseTypeDef = TypedDict(
    "GetConferencePreferenceResponseTypeDef",
    {"Preference": ConferencePreferenceTypeDef},
    total=False,
)

IPDialInTypeDef = TypedDict(
    "IPDialInTypeDef", {"Endpoint": str, "CommsProtocol": Literal["SIP", "SIPS", "H323"]}
)

MeetingSettingTypeDef = TypedDict(
    "MeetingSettingTypeDef", {"RequirePin": Literal["YES", "NO", "OPTIONAL"]}
)

PSTNDialInTypeDef = TypedDict(
    "PSTNDialInTypeDef",
    {"CountryCode": str, "PhoneNumber": str, "OneClickIdDelay": str, "OneClickPinDelay": str},
)

ConferenceProviderTypeDef = TypedDict(
    "ConferenceProviderTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Type": Literal[
            "CHIME",
            "BLUEJEANS",
            "FUZE",
            "GOOGLE_HANGOUTS",
            "POLYCOM",
            "RINGCENTRAL",
            "SKYPE_FOR_BUSINESS",
            "WEBEX",
            "ZOOM",
            "CUSTOM",
        ],
        "IPDialIn": IPDialInTypeDef,
        "PSTNDialIn": PSTNDialInTypeDef,
        "MeetingSetting": MeetingSettingTypeDef,
    },
    total=False,
)

GetConferenceProviderResponseTypeDef = TypedDict(
    "GetConferenceProviderResponseTypeDef",
    {"ConferenceProvider": ConferenceProviderTypeDef},
    total=False,
)

PhoneNumberTypeDef = TypedDict(
    "PhoneNumberTypeDef", {"Number": str, "Type": Literal["MOBILE", "WORK", "HOME"]}
)

SipAddressTypeDef = TypedDict("SipAddressTypeDef", {"Uri": str, "Type": Literal["WORK"]})

ContactTypeDef = TypedDict(
    "ContactTypeDef",
    {
        "ContactArn": str,
        "DisplayName": str,
        "FirstName": str,
        "LastName": str,
        "PhoneNumber": str,
        "PhoneNumbers": List[PhoneNumberTypeDef],
        "SipAddresses": List[SipAddressTypeDef],
    },
    total=False,
)

GetContactResponseTypeDef = TypedDict(
    "GetContactResponseTypeDef", {"Contact": ContactTypeDef}, total=False
)

DeviceNetworkProfileInfoTypeDef = TypedDict(
    "DeviceNetworkProfileInfoTypeDef",
    {"NetworkProfileArn": str, "CertificateArn": str, "CertificateExpirationTime": datetime},
    total=False,
)

DeviceStatusDetailTypeDef = TypedDict(
    "DeviceStatusDetailTypeDef",
    {
        "Feature": Literal[
            "BLUETOOTH",
            "VOLUME",
            "NOTIFICATIONS",
            "LISTS",
            "SKILLS",
            "NETWORK_PROFILE",
            "SETTINGS",
            "ALL",
        ],
        "Code": Literal[
            "DEVICE_SOFTWARE_UPDATE_NEEDED",
            "DEVICE_WAS_OFFLINE",
            "CREDENTIALS_ACCESS_FAILURE",
            "TLS_VERSION_MISMATCH",
            "ASSOCIATION_REJECTION",
            "AUTHENTICATION_FAILURE",
            "DHCP_FAILURE",
            "INTERNET_UNAVAILABLE",
            "DNS_FAILURE",
            "UNKNOWN_FAILURE",
            "CERTIFICATE_ISSUING_LIMIT_EXCEEDED",
            "INVALID_CERTIFICATE_AUTHORITY",
            "NETWORK_PROFILE_NOT_FOUND",
            "INVALID_PASSWORD_STATE",
            "PASSWORD_NOT_FOUND",
        ],
    },
    total=False,
)

DeviceStatusInfoTypeDef = TypedDict(
    "DeviceStatusInfoTypeDef",
    {
        "DeviceStatusDetails": List[DeviceStatusDetailTypeDef],
        "ConnectionStatus": Literal["ONLINE", "OFFLINE"],
        "ConnectionStatusUpdatedTime": datetime,
    },
    total=False,
)

DeviceTypeDef = TypedDict(
    "DeviceTypeDef",
    {
        "DeviceArn": str,
        "DeviceSerialNumber": str,
        "DeviceType": str,
        "DeviceName": str,
        "SoftwareVersion": str,
        "MacAddress": str,
        "RoomArn": str,
        "DeviceStatus": Literal["READY", "PENDING", "WAS_OFFLINE", "DEREGISTERED", "FAILED"],
        "DeviceStatusInfo": DeviceStatusInfoTypeDef,
        "NetworkProfileInfo": DeviceNetworkProfileInfoTypeDef,
    },
    total=False,
)

GetDeviceResponseTypeDef = TypedDict(
    "GetDeviceResponseTypeDef", {"Device": DeviceTypeDef}, total=False
)

GatewayGroupTypeDef = TypedDict(
    "GatewayGroupTypeDef", {"Arn": str, "Name": str, "Description": str}, total=False
)

GetGatewayGroupResponseTypeDef = TypedDict(
    "GetGatewayGroupResponseTypeDef", {"GatewayGroup": GatewayGroupTypeDef}, total=False
)

GatewayTypeDef = TypedDict(
    "GatewayTypeDef",
    {"Arn": str, "Name": str, "Description": str, "GatewayGroupArn": str, "SoftwareVersion": str},
    total=False,
)

GetGatewayResponseTypeDef = TypedDict(
    "GetGatewayResponseTypeDef", {"Gateway": GatewayTypeDef}, total=False
)

GetInvitationConfigurationResponseTypeDef = TypedDict(
    "GetInvitationConfigurationResponseTypeDef",
    {"OrganizationName": str, "ContactEmail": str, "PrivateSkillIds": List[str]},
    total=False,
)

NetworkProfileTypeDef = TypedDict(
    "NetworkProfileTypeDef",
    {
        "NetworkProfileArn": str,
        "NetworkProfileName": str,
        "Description": str,
        "Ssid": str,
        "SecurityType": Literal["OPEN", "WEP", "WPA_PSK", "WPA2_PSK", "WPA2_ENTERPRISE"],
        "EapMethod": Literal["EAP_TLS"],
        "CurrentPassword": str,
        "NextPassword": str,
        "CertificateAuthorityArn": str,
        "TrustAnchors": List[str],
    },
    total=False,
)

GetNetworkProfileResponseTypeDef = TypedDict(
    "GetNetworkProfileResponseTypeDef", {"NetworkProfile": NetworkProfileTypeDef}, total=False
)

EndOfMeetingReminderTypeDef = TypedDict(
    "EndOfMeetingReminderTypeDef",
    {
        "ReminderAtMinutes": List[int],
        "ReminderType": Literal[
            "ANNOUNCEMENT_TIME_CHECK", "ANNOUNCEMENT_VARIABLE_TIME_LEFT", "CHIME", "KNOCK"
        ],
        "Enabled": bool,
    },
    total=False,
)

InstantBookingTypeDef = TypedDict(
    "InstantBookingTypeDef", {"DurationInMinutes": int, "Enabled": bool}, total=False
)

RequireCheckInTypeDef = TypedDict(
    "RequireCheckInTypeDef", {"ReleaseAfterMinutes": int, "Enabled": bool}, total=False
)

MeetingRoomConfigurationTypeDef = TypedDict(
    "MeetingRoomConfigurationTypeDef",
    {
        "RoomUtilizationMetricsEnabled": bool,
        "EndOfMeetingReminder": EndOfMeetingReminderTypeDef,
        "InstantBooking": InstantBookingTypeDef,
        "RequireCheckIn": RequireCheckInTypeDef,
    },
    total=False,
)

ProfileTypeDef = TypedDict(
    "ProfileTypeDef",
    {
        "ProfileArn": str,
        "ProfileName": str,
        "IsDefault": bool,
        "Address": str,
        "Timezone": str,
        "DistanceUnit": Literal["METRIC", "IMPERIAL"],
        "TemperatureUnit": Literal["FAHRENHEIT", "CELSIUS"],
        "WakeWord": Literal["ALEXA", "AMAZON", "ECHO", "COMPUTER"],
        "Locale": str,
        "SetupModeDisabled": bool,
        "MaxVolumeLimit": int,
        "PSTNEnabled": bool,
        "AddressBookArn": str,
        "MeetingRoomConfiguration": MeetingRoomConfigurationTypeDef,
    },
    total=False,
)

GetProfileResponseTypeDef = TypedDict(
    "GetProfileResponseTypeDef", {"Profile": ProfileTypeDef}, total=False
)

RoomTypeDef = TypedDict(
    "RoomTypeDef",
    {
        "RoomArn": str,
        "RoomName": str,
        "Description": str,
        "ProviderCalendarId": str,
        "ProfileArn": str,
    },
    total=False,
)

GetRoomResponseTypeDef = TypedDict("GetRoomResponseTypeDef", {"Room": RoomTypeDef}, total=False)

RoomSkillParameterTypeDef = TypedDict(
    "RoomSkillParameterTypeDef", {"ParameterKey": str, "ParameterValue": str}
)

GetRoomSkillParameterResponseTypeDef = TypedDict(
    "GetRoomSkillParameterResponseTypeDef",
    {"RoomSkillParameter": RoomSkillParameterTypeDef},
    total=False,
)

SkillGroupTypeDef = TypedDict(
    "SkillGroupTypeDef",
    {"SkillGroupArn": str, "SkillGroupName": str, "Description": str},
    total=False,
)

GetSkillGroupResponseTypeDef = TypedDict(
    "GetSkillGroupResponseTypeDef", {"SkillGroup": SkillGroupTypeDef}, total=False
)

BusinessReportS3LocationTypeDef = TypedDict(
    "BusinessReportS3LocationTypeDef", {"Path": str, "BucketName": str}, total=False
)

BusinessReportTypeDef = TypedDict(
    "BusinessReportTypeDef",
    {
        "Status": Literal["RUNNING", "SUCCEEDED", "FAILED"],
        "FailureCode": Literal["ACCESS_DENIED", "NO_SUCH_BUCKET", "INTERNAL_FAILURE"],
        "S3Location": BusinessReportS3LocationTypeDef,
        "DeliveryTime": datetime,
        "DownloadUrl": str,
    },
    total=False,
)

BusinessReportScheduleTypeDef = TypedDict(
    "BusinessReportScheduleTypeDef",
    {
        "ScheduleArn": str,
        "ScheduleName": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "Format": Literal["CSV", "CSV_ZIP"],
        "ContentRange": BusinessReportContentRangeTypeDef,
        "Recurrence": BusinessReportRecurrenceTypeDef,
        "LastBusinessReport": BusinessReportTypeDef,
    },
    total=False,
)

ListBusinessReportSchedulesResponseTypeDef = TypedDict(
    "ListBusinessReportSchedulesResponseTypeDef",
    {"BusinessReportSchedules": List[BusinessReportScheduleTypeDef], "NextToken": str},
    total=False,
)

ListConferenceProvidersResponseTypeDef = TypedDict(
    "ListConferenceProvidersResponseTypeDef",
    {"ConferenceProviders": List[ConferenceProviderTypeDef], "NextToken": str},
    total=False,
)

DeviceEventTypeDef = TypedDict(
    "DeviceEventTypeDef",
    {"Type": Literal["CONNECTION_STATUS", "DEVICE_STATUS"], "Value": str, "Timestamp": datetime},
    total=False,
)

ListDeviceEventsResponseTypeDef = TypedDict(
    "ListDeviceEventsResponseTypeDef",
    {"DeviceEvents": List[DeviceEventTypeDef], "NextToken": str},
    total=False,
)

GatewayGroupSummaryTypeDef = TypedDict(
    "GatewayGroupSummaryTypeDef", {"Arn": str, "Name": str, "Description": str}, total=False
)

ListGatewayGroupsResponseTypeDef = TypedDict(
    "ListGatewayGroupsResponseTypeDef",
    {"GatewayGroups": List[GatewayGroupSummaryTypeDef], "NextToken": str},
    total=False,
)

GatewaySummaryTypeDef = TypedDict(
    "GatewaySummaryTypeDef",
    {"Arn": str, "Name": str, "Description": str, "GatewayGroupArn": str, "SoftwareVersion": str},
    total=False,
)

ListGatewaysResponseTypeDef = TypedDict(
    "ListGatewaysResponseTypeDef",
    {"Gateways": List[GatewaySummaryTypeDef], "NextToken": str},
    total=False,
)

SkillSummaryTypeDef = TypedDict(
    "SkillSummaryTypeDef",
    {
        "SkillId": str,
        "SkillName": str,
        "SupportsLinking": bool,
        "EnablementType": Literal["ENABLED", "PENDING"],
        "SkillType": Literal["PUBLIC", "PRIVATE"],
    },
    total=False,
)

ListSkillsResponseTypeDef = TypedDict(
    "ListSkillsResponseTypeDef",
    {"SkillSummaries": List[SkillSummaryTypeDef], "NextToken": str},
    total=False,
)

CategoryTypeDef = TypedDict(
    "CategoryTypeDef", {"CategoryId": int, "CategoryName": str}, total=False
)

ListSkillsStoreCategoriesResponseTypeDef = TypedDict(
    "ListSkillsStoreCategoriesResponseTypeDef",
    {"CategoryList": List[CategoryTypeDef], "NextToken": str},
    total=False,
)

DeveloperInfoTypeDef = TypedDict(
    "DeveloperInfoTypeDef",
    {"DeveloperName": str, "PrivacyPolicy": str, "Email": str, "Url": str},
    total=False,
)

SkillDetailsTypeDef = TypedDict(
    "SkillDetailsTypeDef",
    {
        "ProductDescription": str,
        "InvocationPhrase": str,
        "ReleaseDate": str,
        "EndUserLicenseAgreement": str,
        "GenericKeywords": List[str],
        "BulletPoints": List[str],
        "NewInThisVersionBulletPoints": List[str],
        "SkillTypes": List[str],
        "Reviews": Dict[str, str],
        "DeveloperInfo": DeveloperInfoTypeDef,
    },
    total=False,
)

SkillsStoreSkillTypeDef = TypedDict(
    "SkillsStoreSkillTypeDef",
    {
        "SkillId": str,
        "SkillName": str,
        "ShortDescription": str,
        "IconUrl": str,
        "SampleUtterances": List[str],
        "SkillDetails": SkillDetailsTypeDef,
        "SupportsLinking": bool,
    },
    total=False,
)

ListSkillsStoreSkillsByCategoryResponseTypeDef = TypedDict(
    "ListSkillsStoreSkillsByCategoryResponseTypeDef",
    {"SkillsStoreSkills": List[SkillsStoreSkillTypeDef], "NextToken": str},
    total=False,
)

SmartHomeApplianceTypeDef = TypedDict(
    "SmartHomeApplianceTypeDef",
    {"FriendlyName": str, "Description": str, "ManufacturerName": str},
    total=False,
)

ListSmartHomeAppliancesResponseTypeDef = TypedDict(
    "ListSmartHomeAppliancesResponseTypeDef",
    {"SmartHomeAppliances": List[SmartHomeApplianceTypeDef], "NextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef", {"Tags": List[TagTypeDef], "NextToken": str}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

RegisterAVSDeviceResponseTypeDef = TypedDict(
    "RegisterAVSDeviceResponseTypeDef", {"DeviceArn": str}, total=False
)

ResolveRoomResponseTypeDef = TypedDict(
    "ResolveRoomResponseTypeDef",
    {"RoomArn": str, "RoomName": str, "RoomSkillParameters": List[RoomSkillParameterTypeDef]},
    total=False,
)

AddressBookDataTypeDef = TypedDict(
    "AddressBookDataTypeDef", {"AddressBookArn": str, "Name": str, "Description": str}, total=False
)

SearchAddressBooksResponseTypeDef = TypedDict(
    "SearchAddressBooksResponseTypeDef",
    {"AddressBooks": List[AddressBookDataTypeDef], "NextToken": str, "TotalCount": int},
    total=False,
)

ContactDataTypeDef = TypedDict(
    "ContactDataTypeDef",
    {
        "ContactArn": str,
        "DisplayName": str,
        "FirstName": str,
        "LastName": str,
        "PhoneNumber": str,
        "PhoneNumbers": List[PhoneNumberTypeDef],
        "SipAddresses": List[SipAddressTypeDef],
    },
    total=False,
)

SearchContactsResponseTypeDef = TypedDict(
    "SearchContactsResponseTypeDef",
    {"Contacts": List[ContactDataTypeDef], "NextToken": str, "TotalCount": int},
    total=False,
)

DeviceDataTypeDef = TypedDict(
    "DeviceDataTypeDef",
    {
        "DeviceArn": str,
        "DeviceSerialNumber": str,
        "DeviceType": str,
        "DeviceName": str,
        "SoftwareVersion": str,
        "MacAddress": str,
        "DeviceStatus": Literal["READY", "PENDING", "WAS_OFFLINE", "DEREGISTERED", "FAILED"],
        "NetworkProfileArn": str,
        "NetworkProfileName": str,
        "RoomArn": str,
        "RoomName": str,
        "DeviceStatusInfo": DeviceStatusInfoTypeDef,
        "CreatedTime": datetime,
    },
    total=False,
)

SearchDevicesResponseTypeDef = TypedDict(
    "SearchDevicesResponseTypeDef",
    {"Devices": List[DeviceDataTypeDef], "NextToken": str, "TotalCount": int},
    total=False,
)

NetworkProfileDataTypeDef = TypedDict(
    "NetworkProfileDataTypeDef",
    {
        "NetworkProfileArn": str,
        "NetworkProfileName": str,
        "Description": str,
        "Ssid": str,
        "SecurityType": Literal["OPEN", "WEP", "WPA_PSK", "WPA2_PSK", "WPA2_ENTERPRISE"],
        "EapMethod": Literal["EAP_TLS"],
        "CertificateAuthorityArn": str,
    },
    total=False,
)

SearchNetworkProfilesResponseTypeDef = TypedDict(
    "SearchNetworkProfilesResponseTypeDef",
    {"NetworkProfiles": List[NetworkProfileDataTypeDef], "NextToken": str, "TotalCount": int},
    total=False,
)

ProfileDataTypeDef = TypedDict(
    "ProfileDataTypeDef",
    {
        "ProfileArn": str,
        "ProfileName": str,
        "IsDefault": bool,
        "Address": str,
        "Timezone": str,
        "DistanceUnit": Literal["METRIC", "IMPERIAL"],
        "TemperatureUnit": Literal["FAHRENHEIT", "CELSIUS"],
        "WakeWord": Literal["ALEXA", "AMAZON", "ECHO", "COMPUTER"],
        "Locale": str,
    },
    total=False,
)

SearchProfilesResponseTypeDef = TypedDict(
    "SearchProfilesResponseTypeDef",
    {"Profiles": List[ProfileDataTypeDef], "NextToken": str, "TotalCount": int},
    total=False,
)

RoomDataTypeDef = TypedDict(
    "RoomDataTypeDef",
    {
        "RoomArn": str,
        "RoomName": str,
        "Description": str,
        "ProviderCalendarId": str,
        "ProfileArn": str,
        "ProfileName": str,
    },
    total=False,
)

SearchRoomsResponseTypeDef = TypedDict(
    "SearchRoomsResponseTypeDef",
    {"Rooms": List[RoomDataTypeDef], "NextToken": str, "TotalCount": int},
    total=False,
)

SkillGroupDataTypeDef = TypedDict(
    "SkillGroupDataTypeDef",
    {"SkillGroupArn": str, "SkillGroupName": str, "Description": str},
    total=False,
)

SearchSkillGroupsResponseTypeDef = TypedDict(
    "SearchSkillGroupsResponseTypeDef",
    {"SkillGroups": List[SkillGroupDataTypeDef], "NextToken": str, "TotalCount": int},
    total=False,
)

UserDataTypeDef = TypedDict(
    "UserDataTypeDef",
    {
        "UserArn": str,
        "FirstName": str,
        "LastName": str,
        "Email": str,
        "EnrollmentStatus": Literal[
            "INITIALIZED", "PENDING", "REGISTERED", "DISASSOCIATING", "DEREGISTERING"
        ],
        "EnrollmentId": str,
    },
    total=False,
)

SearchUsersResponseTypeDef = TypedDict(
    "SearchUsersResponseTypeDef",
    {"Users": List[UserDataTypeDef], "NextToken": str, "TotalCount": int},
    total=False,
)

SendAnnouncementResponseTypeDef = TypedDict(
    "SendAnnouncementResponseTypeDef", {"AnnouncementArn": str}, total=False
)

SortTypeDef = TypedDict("SortTypeDef", {"Key": str, "Value": Literal["ASC", "DESC"]})

UpdateEndOfMeetingReminderTypeDef = TypedDict(
    "UpdateEndOfMeetingReminderTypeDef",
    {
        "ReminderAtMinutes": List[int],
        "ReminderType": Literal[
            "ANNOUNCEMENT_TIME_CHECK", "ANNOUNCEMENT_VARIABLE_TIME_LEFT", "CHIME", "KNOCK"
        ],
        "Enabled": bool,
    },
    total=False,
)

UpdateInstantBookingTypeDef = TypedDict(
    "UpdateInstantBookingTypeDef", {"DurationInMinutes": int, "Enabled": bool}, total=False
)

UpdateRequireCheckInTypeDef = TypedDict(
    "UpdateRequireCheckInTypeDef", {"ReleaseAfterMinutes": int, "Enabled": bool}, total=False
)

UpdateMeetingRoomConfigurationTypeDef = TypedDict(
    "UpdateMeetingRoomConfigurationTypeDef",
    {
        "RoomUtilizationMetricsEnabled": bool,
        "EndOfMeetingReminder": UpdateEndOfMeetingReminderTypeDef,
        "InstantBooking": UpdateInstantBookingTypeDef,
        "RequireCheckIn": UpdateRequireCheckInTypeDef,
    },
    total=False,
)
