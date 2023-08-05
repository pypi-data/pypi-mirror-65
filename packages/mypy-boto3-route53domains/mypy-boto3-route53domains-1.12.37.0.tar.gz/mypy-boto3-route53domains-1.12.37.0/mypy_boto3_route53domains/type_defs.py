"""
Main interface for route53domains service type definitions.

Usage::

    from mypy_boto3.route53domains.type_defs import CheckDomainAvailabilityResponseTypeDef

    data: CheckDomainAvailabilityResponseTypeDef = {...}
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
    "CheckDomainAvailabilityResponseTypeDef",
    "DomainTransferabilityTypeDef",
    "CheckDomainTransferabilityResponseTypeDef",
    "ExtraParamTypeDef",
    "ContactDetailTypeDef",
    "DisableDomainTransferLockResponseTypeDef",
    "EnableDomainTransferLockResponseTypeDef",
    "GetContactReachabilityStatusResponseTypeDef",
    "NameserverTypeDef",
    "GetDomainDetailResponseTypeDef",
    "DomainSuggestionTypeDef",
    "GetDomainSuggestionsResponseTypeDef",
    "GetOperationDetailResponseTypeDef",
    "DomainSummaryTypeDef",
    "ListDomainsResponseTypeDef",
    "OperationSummaryTypeDef",
    "ListOperationsResponseTypeDef",
    "TagTypeDef",
    "ListTagsForDomainResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RegisterDomainResponseTypeDef",
    "RenewDomainResponseTypeDef",
    "ResendContactReachabilityEmailResponseTypeDef",
    "RetrieveDomainAuthCodeResponseTypeDef",
    "TransferDomainResponseTypeDef",
    "UpdateDomainContactPrivacyResponseTypeDef",
    "UpdateDomainContactResponseTypeDef",
    "UpdateDomainNameserversResponseTypeDef",
    "BillingRecordTypeDef",
    "ViewBillingResponseTypeDef",
)

CheckDomainAvailabilityResponseTypeDef = TypedDict(
    "CheckDomainAvailabilityResponseTypeDef",
    {
        "Availability": Literal[
            "AVAILABLE",
            "AVAILABLE_RESERVED",
            "AVAILABLE_PREORDER",
            "UNAVAILABLE",
            "UNAVAILABLE_PREMIUM",
            "UNAVAILABLE_RESTRICTED",
            "RESERVED",
            "DONT_KNOW",
        ]
    },
)

DomainTransferabilityTypeDef = TypedDict(
    "DomainTransferabilityTypeDef",
    {"Transferable": Literal["TRANSFERABLE", "UNTRANSFERABLE", "DONT_KNOW"]},
    total=False,
)

CheckDomainTransferabilityResponseTypeDef = TypedDict(
    "CheckDomainTransferabilityResponseTypeDef", {"Transferability": DomainTransferabilityTypeDef}
)

ExtraParamTypeDef = TypedDict(
    "ExtraParamTypeDef",
    {
        "Name": Literal[
            "DUNS_NUMBER",
            "BRAND_NUMBER",
            "BIRTH_DEPARTMENT",
            "BIRTH_DATE_IN_YYYY_MM_DD",
            "BIRTH_COUNTRY",
            "BIRTH_CITY",
            "DOCUMENT_NUMBER",
            "AU_ID_NUMBER",
            "AU_ID_TYPE",
            "CA_LEGAL_TYPE",
            "CA_BUSINESS_ENTITY_TYPE",
            "ES_IDENTIFICATION",
            "ES_IDENTIFICATION_TYPE",
            "ES_LEGAL_FORM",
            "FI_BUSINESS_NUMBER",
            "FI_ID_NUMBER",
            "FI_NATIONALITY",
            "FI_ORGANIZATION_TYPE",
            "IT_PIN",
            "IT_REGISTRANT_ENTITY_TYPE",
            "RU_PASSPORT_DATA",
            "SE_ID_NUMBER",
            "SG_ID_NUMBER",
            "VAT_NUMBER",
            "UK_CONTACT_TYPE",
            "UK_COMPANY_NUMBER",
        ],
        "Value": str,
    },
)

ContactDetailTypeDef = TypedDict(
    "ContactDetailTypeDef",
    {
        "FirstName": str,
        "LastName": str,
        "ContactType": Literal["PERSON", "COMPANY", "ASSOCIATION", "PUBLIC_BODY", "RESELLER"],
        "OrganizationName": str,
        "AddressLine1": str,
        "AddressLine2": str,
        "City": str,
        "State": str,
        "CountryCode": Literal[
            "AD",
            "AE",
            "AF",
            "AG",
            "AI",
            "AL",
            "AM",
            "AN",
            "AO",
            "AQ",
            "AR",
            "AS",
            "AT",
            "AU",
            "AW",
            "AZ",
            "BA",
            "BB",
            "BD",
            "BE",
            "BF",
            "BG",
            "BH",
            "BI",
            "BJ",
            "BL",
            "BM",
            "BN",
            "BO",
            "BR",
            "BS",
            "BT",
            "BW",
            "BY",
            "BZ",
            "CA",
            "CC",
            "CD",
            "CF",
            "CG",
            "CH",
            "CI",
            "CK",
            "CL",
            "CM",
            "CN",
            "CO",
            "CR",
            "CU",
            "CV",
            "CX",
            "CY",
            "CZ",
            "DE",
            "DJ",
            "DK",
            "DM",
            "DO",
            "DZ",
            "EC",
            "EE",
            "EG",
            "ER",
            "ES",
            "ET",
            "FI",
            "FJ",
            "FK",
            "FM",
            "FO",
            "FR",
            "GA",
            "GB",
            "GD",
            "GE",
            "GH",
            "GI",
            "GL",
            "GM",
            "GN",
            "GQ",
            "GR",
            "GT",
            "GU",
            "GW",
            "GY",
            "HK",
            "HN",
            "HR",
            "HT",
            "HU",
            "ID",
            "IE",
            "IL",
            "IM",
            "IN",
            "IQ",
            "IR",
            "IS",
            "IT",
            "JM",
            "JO",
            "JP",
            "KE",
            "KG",
            "KH",
            "KI",
            "KM",
            "KN",
            "KP",
            "KR",
            "KW",
            "KY",
            "KZ",
            "LA",
            "LB",
            "LC",
            "LI",
            "LK",
            "LR",
            "LS",
            "LT",
            "LU",
            "LV",
            "LY",
            "MA",
            "MC",
            "MD",
            "ME",
            "MF",
            "MG",
            "MH",
            "MK",
            "ML",
            "MM",
            "MN",
            "MO",
            "MP",
            "MR",
            "MS",
            "MT",
            "MU",
            "MV",
            "MW",
            "MX",
            "MY",
            "MZ",
            "NA",
            "NC",
            "NE",
            "NG",
            "NI",
            "NL",
            "NO",
            "NP",
            "NR",
            "NU",
            "NZ",
            "OM",
            "PA",
            "PE",
            "PF",
            "PG",
            "PH",
            "PK",
            "PL",
            "PM",
            "PN",
            "PR",
            "PT",
            "PW",
            "PY",
            "QA",
            "RO",
            "RS",
            "RU",
            "RW",
            "SA",
            "SB",
            "SC",
            "SD",
            "SE",
            "SG",
            "SH",
            "SI",
            "SK",
            "SL",
            "SM",
            "SN",
            "SO",
            "SR",
            "ST",
            "SV",
            "SY",
            "SZ",
            "TC",
            "TD",
            "TG",
            "TH",
            "TJ",
            "TK",
            "TL",
            "TM",
            "TN",
            "TO",
            "TR",
            "TT",
            "TV",
            "TW",
            "TZ",
            "UA",
            "UG",
            "US",
            "UY",
            "UZ",
            "VA",
            "VC",
            "VE",
            "VG",
            "VI",
            "VN",
            "VU",
            "WF",
            "WS",
            "YE",
            "YT",
            "ZA",
            "ZM",
            "ZW",
        ],
        "ZipCode": str,
        "PhoneNumber": str,
        "Email": str,
        "Fax": str,
        "ExtraParams": List[ExtraParamTypeDef],
    },
    total=False,
)

DisableDomainTransferLockResponseTypeDef = TypedDict(
    "DisableDomainTransferLockResponseTypeDef", {"OperationId": str}
)

EnableDomainTransferLockResponseTypeDef = TypedDict(
    "EnableDomainTransferLockResponseTypeDef", {"OperationId": str}
)

GetContactReachabilityStatusResponseTypeDef = TypedDict(
    "GetContactReachabilityStatusResponseTypeDef",
    {"domainName": str, "status": Literal["PENDING", "DONE", "EXPIRED"]},
    total=False,
)

_RequiredNameserverTypeDef = TypedDict("_RequiredNameserverTypeDef", {"Name": str})
_OptionalNameserverTypeDef = TypedDict(
    "_OptionalNameserverTypeDef", {"GlueIps": List[str]}, total=False
)


class NameserverTypeDef(_RequiredNameserverTypeDef, _OptionalNameserverTypeDef):
    pass


_RequiredGetDomainDetailResponseTypeDef = TypedDict(
    "_RequiredGetDomainDetailResponseTypeDef",
    {
        "DomainName": str,
        "Nameservers": List[NameserverTypeDef],
        "AdminContact": ContactDetailTypeDef,
        "RegistrantContact": ContactDetailTypeDef,
        "TechContact": ContactDetailTypeDef,
    },
)
_OptionalGetDomainDetailResponseTypeDef = TypedDict(
    "_OptionalGetDomainDetailResponseTypeDef",
    {
        "AutoRenew": bool,
        "AdminPrivacy": bool,
        "RegistrantPrivacy": bool,
        "TechPrivacy": bool,
        "RegistrarName": str,
        "WhoIsServer": str,
        "RegistrarUrl": str,
        "AbuseContactEmail": str,
        "AbuseContactPhone": str,
        "RegistryDomainId": str,
        "CreationDate": datetime,
        "UpdatedDate": datetime,
        "ExpirationDate": datetime,
        "Reseller": str,
        "DnsSec": str,
        "StatusList": List[str],
    },
    total=False,
)


class GetDomainDetailResponseTypeDef(
    _RequiredGetDomainDetailResponseTypeDef, _OptionalGetDomainDetailResponseTypeDef
):
    pass


DomainSuggestionTypeDef = TypedDict(
    "DomainSuggestionTypeDef", {"DomainName": str, "Availability": str}, total=False
)

GetDomainSuggestionsResponseTypeDef = TypedDict(
    "GetDomainSuggestionsResponseTypeDef",
    {"SuggestionsList": List[DomainSuggestionTypeDef]},
    total=False,
)

GetOperationDetailResponseTypeDef = TypedDict(
    "GetOperationDetailResponseTypeDef",
    {
        "OperationId": str,
        "Status": Literal["SUBMITTED", "IN_PROGRESS", "ERROR", "SUCCESSFUL", "FAILED"],
        "Message": str,
        "DomainName": str,
        "Type": Literal[
            "REGISTER_DOMAIN",
            "DELETE_DOMAIN",
            "TRANSFER_IN_DOMAIN",
            "UPDATE_DOMAIN_CONTACT",
            "UPDATE_NAMESERVER",
            "CHANGE_PRIVACY_PROTECTION",
            "DOMAIN_LOCK",
            "ENABLE_AUTORENEW",
            "DISABLE_AUTORENEW",
            "ADD_DNSSEC",
            "REMOVE_DNSSEC",
            "EXPIRE_DOMAIN",
            "TRANSFER_OUT_DOMAIN",
            "CHANGE_DOMAIN_OWNER",
            "RENEW_DOMAIN",
            "PUSH_DOMAIN",
        ],
        "SubmittedDate": datetime,
    },
    total=False,
)

_RequiredDomainSummaryTypeDef = TypedDict("_RequiredDomainSummaryTypeDef", {"DomainName": str})
_OptionalDomainSummaryTypeDef = TypedDict(
    "_OptionalDomainSummaryTypeDef",
    {"AutoRenew": bool, "TransferLock": bool, "Expiry": datetime},
    total=False,
)


class DomainSummaryTypeDef(_RequiredDomainSummaryTypeDef, _OptionalDomainSummaryTypeDef):
    pass


_RequiredListDomainsResponseTypeDef = TypedDict(
    "_RequiredListDomainsResponseTypeDef", {"Domains": List[DomainSummaryTypeDef]}
)
_OptionalListDomainsResponseTypeDef = TypedDict(
    "_OptionalListDomainsResponseTypeDef", {"NextPageMarker": str}, total=False
)


class ListDomainsResponseTypeDef(
    _RequiredListDomainsResponseTypeDef, _OptionalListDomainsResponseTypeDef
):
    pass


OperationSummaryTypeDef = TypedDict(
    "OperationSummaryTypeDef",
    {
        "OperationId": str,
        "Status": Literal["SUBMITTED", "IN_PROGRESS", "ERROR", "SUCCESSFUL", "FAILED"],
        "Type": Literal[
            "REGISTER_DOMAIN",
            "DELETE_DOMAIN",
            "TRANSFER_IN_DOMAIN",
            "UPDATE_DOMAIN_CONTACT",
            "UPDATE_NAMESERVER",
            "CHANGE_PRIVACY_PROTECTION",
            "DOMAIN_LOCK",
            "ENABLE_AUTORENEW",
            "DISABLE_AUTORENEW",
            "ADD_DNSSEC",
            "REMOVE_DNSSEC",
            "EXPIRE_DOMAIN",
            "TRANSFER_OUT_DOMAIN",
            "CHANGE_DOMAIN_OWNER",
            "RENEW_DOMAIN",
            "PUSH_DOMAIN",
        ],
        "SubmittedDate": datetime,
    },
)

_RequiredListOperationsResponseTypeDef = TypedDict(
    "_RequiredListOperationsResponseTypeDef", {"Operations": List[OperationSummaryTypeDef]}
)
_OptionalListOperationsResponseTypeDef = TypedDict(
    "_OptionalListOperationsResponseTypeDef", {"NextPageMarker": str}, total=False
)


class ListOperationsResponseTypeDef(
    _RequiredListOperationsResponseTypeDef, _OptionalListOperationsResponseTypeDef
):
    pass


TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str}, total=False)

ListTagsForDomainResponseTypeDef = TypedDict(
    "ListTagsForDomainResponseTypeDef", {"TagList": List[TagTypeDef]}
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

RegisterDomainResponseTypeDef = TypedDict("RegisterDomainResponseTypeDef", {"OperationId": str})

RenewDomainResponseTypeDef = TypedDict("RenewDomainResponseTypeDef", {"OperationId": str})

ResendContactReachabilityEmailResponseTypeDef = TypedDict(
    "ResendContactReachabilityEmailResponseTypeDef",
    {"domainName": str, "emailAddress": str, "isAlreadyVerified": bool},
    total=False,
)

RetrieveDomainAuthCodeResponseTypeDef = TypedDict(
    "RetrieveDomainAuthCodeResponseTypeDef", {"AuthCode": str}
)

TransferDomainResponseTypeDef = TypedDict("TransferDomainResponseTypeDef", {"OperationId": str})

UpdateDomainContactPrivacyResponseTypeDef = TypedDict(
    "UpdateDomainContactPrivacyResponseTypeDef", {"OperationId": str}
)

UpdateDomainContactResponseTypeDef = TypedDict(
    "UpdateDomainContactResponseTypeDef", {"OperationId": str}
)

UpdateDomainNameserversResponseTypeDef = TypedDict(
    "UpdateDomainNameserversResponseTypeDef", {"OperationId": str}
)

BillingRecordTypeDef = TypedDict(
    "BillingRecordTypeDef",
    {
        "DomainName": str,
        "Operation": Literal[
            "REGISTER_DOMAIN",
            "DELETE_DOMAIN",
            "TRANSFER_IN_DOMAIN",
            "UPDATE_DOMAIN_CONTACT",
            "UPDATE_NAMESERVER",
            "CHANGE_PRIVACY_PROTECTION",
            "DOMAIN_LOCK",
            "ENABLE_AUTORENEW",
            "DISABLE_AUTORENEW",
            "ADD_DNSSEC",
            "REMOVE_DNSSEC",
            "EXPIRE_DOMAIN",
            "TRANSFER_OUT_DOMAIN",
            "CHANGE_DOMAIN_OWNER",
            "RENEW_DOMAIN",
            "PUSH_DOMAIN",
        ],
        "InvoiceId": str,
        "BillDate": datetime,
        "Price": float,
    },
    total=False,
)

ViewBillingResponseTypeDef = TypedDict(
    "ViewBillingResponseTypeDef",
    {"NextPageMarker": str, "BillingRecords": List[BillingRecordTypeDef]},
    total=False,
)
