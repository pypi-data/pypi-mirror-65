"""
Main interface for worklink service type definitions.

Usage::

    from mypy_boto3.worklink.type_defs import AssociateWebsiteAuthorizationProviderResponseTypeDef

    data: AssociateWebsiteAuthorizationProviderResponseTypeDef = {...}
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
    "AssociateWebsiteAuthorizationProviderResponseTypeDef",
    "AssociateWebsiteCertificateAuthorityResponseTypeDef",
    "CreateFleetResponseTypeDef",
    "DescribeAuditStreamConfigurationResponseTypeDef",
    "DescribeCompanyNetworkConfigurationResponseTypeDef",
    "DescribeDevicePolicyConfigurationResponseTypeDef",
    "DescribeDeviceResponseTypeDef",
    "DescribeDomainResponseTypeDef",
    "DescribeFleetMetadataResponseTypeDef",
    "DescribeIdentityProviderConfigurationResponseTypeDef",
    "DescribeWebsiteCertificateAuthorityResponseTypeDef",
    "DeviceSummaryTypeDef",
    "ListDevicesResponseTypeDef",
    "DomainSummaryTypeDef",
    "ListDomainsResponseTypeDef",
    "FleetSummaryTypeDef",
    "ListFleetsResponseTypeDef",
    "WebsiteAuthorizationProviderSummaryTypeDef",
    "ListWebsiteAuthorizationProvidersResponseTypeDef",
    "WebsiteCaSummaryTypeDef",
    "ListWebsiteCertificateAuthoritiesResponseTypeDef",
)

AssociateWebsiteAuthorizationProviderResponseTypeDef = TypedDict(
    "AssociateWebsiteAuthorizationProviderResponseTypeDef",
    {"AuthorizationProviderId": str},
    total=False,
)

AssociateWebsiteCertificateAuthorityResponseTypeDef = TypedDict(
    "AssociateWebsiteCertificateAuthorityResponseTypeDef", {"WebsiteCaId": str}, total=False
)

CreateFleetResponseTypeDef = TypedDict("CreateFleetResponseTypeDef", {"FleetArn": str}, total=False)

DescribeAuditStreamConfigurationResponseTypeDef = TypedDict(
    "DescribeAuditStreamConfigurationResponseTypeDef", {"AuditStreamArn": str}, total=False
)

DescribeCompanyNetworkConfigurationResponseTypeDef = TypedDict(
    "DescribeCompanyNetworkConfigurationResponseTypeDef",
    {"VpcId": str, "SubnetIds": List[str], "SecurityGroupIds": List[str]},
    total=False,
)

DescribeDevicePolicyConfigurationResponseTypeDef = TypedDict(
    "DescribeDevicePolicyConfigurationResponseTypeDef", {"DeviceCaCertificate": str}, total=False
)

DescribeDeviceResponseTypeDef = TypedDict(
    "DescribeDeviceResponseTypeDef",
    {
        "Status": Literal["ACTIVE", "SIGNED_OUT"],
        "Model": str,
        "Manufacturer": str,
        "OperatingSystem": str,
        "OperatingSystemVersion": str,
        "PatchLevel": str,
        "FirstAccessedTime": datetime,
        "LastAccessedTime": datetime,
        "Username": str,
    },
    total=False,
)

DescribeDomainResponseTypeDef = TypedDict(
    "DescribeDomainResponseTypeDef",
    {
        "DomainName": str,
        "DisplayName": str,
        "CreatedTime": datetime,
        "DomainStatus": Literal[
            "PENDING_VALIDATION",
            "ASSOCIATING",
            "ACTIVE",
            "INACTIVE",
            "DISASSOCIATING",
            "DISASSOCIATED",
            "FAILED_TO_ASSOCIATE",
            "FAILED_TO_DISASSOCIATE",
        ],
        "AcmCertificateArn": str,
    },
    total=False,
)

DescribeFleetMetadataResponseTypeDef = TypedDict(
    "DescribeFleetMetadataResponseTypeDef",
    {
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "FleetName": str,
        "DisplayName": str,
        "OptimizeForEndUserLocation": bool,
        "CompanyCode": str,
        "FleetStatus": Literal[
            "CREATING", "ACTIVE", "DELETING", "DELETED", "FAILED_TO_CREATE", "FAILED_TO_DELETE"
        ],
    },
    total=False,
)

DescribeIdentityProviderConfigurationResponseTypeDef = TypedDict(
    "DescribeIdentityProviderConfigurationResponseTypeDef",
    {
        "IdentityProviderType": Literal["SAML"],
        "ServiceProviderSamlMetadata": str,
        "IdentityProviderSamlMetadata": str,
    },
    total=False,
)

DescribeWebsiteCertificateAuthorityResponseTypeDef = TypedDict(
    "DescribeWebsiteCertificateAuthorityResponseTypeDef",
    {"Certificate": str, "CreatedTime": datetime, "DisplayName": str},
    total=False,
)

DeviceSummaryTypeDef = TypedDict(
    "DeviceSummaryTypeDef",
    {"DeviceId": str, "DeviceStatus": Literal["ACTIVE", "SIGNED_OUT"]},
    total=False,
)

ListDevicesResponseTypeDef = TypedDict(
    "ListDevicesResponseTypeDef",
    {"Devices": List[DeviceSummaryTypeDef], "NextToken": str},
    total=False,
)

_RequiredDomainSummaryTypeDef = TypedDict(
    "_RequiredDomainSummaryTypeDef",
    {
        "DomainName": str,
        "CreatedTime": datetime,
        "DomainStatus": Literal[
            "PENDING_VALIDATION",
            "ASSOCIATING",
            "ACTIVE",
            "INACTIVE",
            "DISASSOCIATING",
            "DISASSOCIATED",
            "FAILED_TO_ASSOCIATE",
            "FAILED_TO_DISASSOCIATE",
        ],
    },
)
_OptionalDomainSummaryTypeDef = TypedDict(
    "_OptionalDomainSummaryTypeDef", {"DisplayName": str}, total=False
)


class DomainSummaryTypeDef(_RequiredDomainSummaryTypeDef, _OptionalDomainSummaryTypeDef):
    pass


ListDomainsResponseTypeDef = TypedDict(
    "ListDomainsResponseTypeDef",
    {"Domains": List[DomainSummaryTypeDef], "NextToken": str},
    total=False,
)

FleetSummaryTypeDef = TypedDict(
    "FleetSummaryTypeDef",
    {
        "FleetArn": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "FleetName": str,
        "DisplayName": str,
        "CompanyCode": str,
        "FleetStatus": Literal[
            "CREATING", "ACTIVE", "DELETING", "DELETED", "FAILED_TO_CREATE", "FAILED_TO_DELETE"
        ],
    },
    total=False,
)

ListFleetsResponseTypeDef = TypedDict(
    "ListFleetsResponseTypeDef",
    {"FleetSummaryList": List[FleetSummaryTypeDef], "NextToken": str},
    total=False,
)

_RequiredWebsiteAuthorizationProviderSummaryTypeDef = TypedDict(
    "_RequiredWebsiteAuthorizationProviderSummaryTypeDef",
    {"AuthorizationProviderType": Literal["SAML"]},
)
_OptionalWebsiteAuthorizationProviderSummaryTypeDef = TypedDict(
    "_OptionalWebsiteAuthorizationProviderSummaryTypeDef",
    {"AuthorizationProviderId": str, "DomainName": str, "CreatedTime": datetime},
    total=False,
)


class WebsiteAuthorizationProviderSummaryTypeDef(
    _RequiredWebsiteAuthorizationProviderSummaryTypeDef,
    _OptionalWebsiteAuthorizationProviderSummaryTypeDef,
):
    pass


ListWebsiteAuthorizationProvidersResponseTypeDef = TypedDict(
    "ListWebsiteAuthorizationProvidersResponseTypeDef",
    {
        "WebsiteAuthorizationProviders": List[WebsiteAuthorizationProviderSummaryTypeDef],
        "NextToken": str,
    },
    total=False,
)

WebsiteCaSummaryTypeDef = TypedDict(
    "WebsiteCaSummaryTypeDef",
    {"WebsiteCaId": str, "CreatedTime": datetime, "DisplayName": str},
    total=False,
)

ListWebsiteCertificateAuthoritiesResponseTypeDef = TypedDict(
    "ListWebsiteCertificateAuthoritiesResponseTypeDef",
    {"WebsiteCertificateAuthorities": List[WebsiteCaSummaryTypeDef], "NextToken": str},
    total=False,
)
