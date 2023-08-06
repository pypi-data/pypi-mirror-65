"""
Main interface for elbv2 service type definitions.

Usage::

    from mypy_boto3.elbv2.type_defs import AuthenticateCognitoActionConfigTypeDef

    data: AuthenticateCognitoActionConfigTypeDef = {...}
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
    "AuthenticateCognitoActionConfigTypeDef",
    "AuthenticateOidcActionConfigTypeDef",
    "FixedResponseActionConfigTypeDef",
    "TargetGroupStickinessConfigTypeDef",
    "TargetGroupTupleTypeDef",
    "ForwardActionConfigTypeDef",
    "RedirectActionConfigTypeDef",
    "ActionTypeDef",
    "CertificateTypeDef",
    "AddListenerCertificatesOutputTypeDef",
    "ListenerTypeDef",
    "CreateListenerOutputTypeDef",
    "LoadBalancerAddressTypeDef",
    "AvailabilityZoneTypeDef",
    "LoadBalancerStateTypeDef",
    "LoadBalancerTypeDef",
    "CreateLoadBalancerOutputTypeDef",
    "HostHeaderConditionConfigTypeDef",
    "HttpHeaderConditionConfigTypeDef",
    "HttpRequestMethodConditionConfigTypeDef",
    "PathPatternConditionConfigTypeDef",
    "QueryStringKeyValuePairTypeDef",
    "QueryStringConditionConfigTypeDef",
    "SourceIpConditionConfigTypeDef",
    "RuleConditionTypeDef",
    "RuleTypeDef",
    "CreateRuleOutputTypeDef",
    "MatcherTypeDef",
    "TargetGroupTypeDef",
    "CreateTargetGroupOutputTypeDef",
    "LimitTypeDef",
    "DescribeAccountLimitsOutputTypeDef",
    "DescribeListenerCertificatesOutputTypeDef",
    "DescribeListenersOutputTypeDef",
    "LoadBalancerAttributeTypeDef",
    "DescribeLoadBalancerAttributesOutputTypeDef",
    "DescribeLoadBalancersOutputTypeDef",
    "DescribeRulesOutputTypeDef",
    "CipherTypeDef",
    "SslPolicyTypeDef",
    "DescribeSSLPoliciesOutputTypeDef",
    "TagTypeDef",
    "TagDescriptionTypeDef",
    "DescribeTagsOutputTypeDef",
    "TargetGroupAttributeTypeDef",
    "DescribeTargetGroupAttributesOutputTypeDef",
    "DescribeTargetGroupsOutputTypeDef",
    "TargetDescriptionTypeDef",
    "TargetHealthTypeDef",
    "TargetHealthDescriptionTypeDef",
    "DescribeTargetHealthOutputTypeDef",
    "ModifyListenerOutputTypeDef",
    "ModifyLoadBalancerAttributesOutputTypeDef",
    "ModifyRuleOutputTypeDef",
    "ModifyTargetGroupAttributesOutputTypeDef",
    "ModifyTargetGroupOutputTypeDef",
    "PaginatorConfigTypeDef",
    "RulePriorityPairTypeDef",
    "SetIpAddressTypeOutputTypeDef",
    "SetRulePrioritiesOutputTypeDef",
    "SetSecurityGroupsOutputTypeDef",
    "SetSubnetsOutputTypeDef",
    "SubnetMappingTypeDef",
    "WaiterConfigTypeDef",
)

_RequiredAuthenticateCognitoActionConfigTypeDef = TypedDict(
    "_RequiredAuthenticateCognitoActionConfigTypeDef",
    {"UserPoolArn": str, "UserPoolClientId": str, "UserPoolDomain": str},
)
_OptionalAuthenticateCognitoActionConfigTypeDef = TypedDict(
    "_OptionalAuthenticateCognitoActionConfigTypeDef",
    {
        "SessionCookieName": str,
        "Scope": str,
        "SessionTimeout": int,
        "AuthenticationRequestExtraParams": Dict[str, str],
        "OnUnauthenticatedRequest": Literal["deny", "allow", "authenticate"],
    },
    total=False,
)


class AuthenticateCognitoActionConfigTypeDef(
    _RequiredAuthenticateCognitoActionConfigTypeDef, _OptionalAuthenticateCognitoActionConfigTypeDef
):
    pass


_RequiredAuthenticateOidcActionConfigTypeDef = TypedDict(
    "_RequiredAuthenticateOidcActionConfigTypeDef",
    {
        "Issuer": str,
        "AuthorizationEndpoint": str,
        "TokenEndpoint": str,
        "UserInfoEndpoint": str,
        "ClientId": str,
    },
)
_OptionalAuthenticateOidcActionConfigTypeDef = TypedDict(
    "_OptionalAuthenticateOidcActionConfigTypeDef",
    {
        "ClientSecret": str,
        "SessionCookieName": str,
        "Scope": str,
        "SessionTimeout": int,
        "AuthenticationRequestExtraParams": Dict[str, str],
        "OnUnauthenticatedRequest": Literal["deny", "allow", "authenticate"],
        "UseExistingClientSecret": bool,
    },
    total=False,
)


class AuthenticateOidcActionConfigTypeDef(
    _RequiredAuthenticateOidcActionConfigTypeDef, _OptionalAuthenticateOidcActionConfigTypeDef
):
    pass


_RequiredFixedResponseActionConfigTypeDef = TypedDict(
    "_RequiredFixedResponseActionConfigTypeDef", {"StatusCode": str}
)
_OptionalFixedResponseActionConfigTypeDef = TypedDict(
    "_OptionalFixedResponseActionConfigTypeDef",
    {"MessageBody": str, "ContentType": str},
    total=False,
)


class FixedResponseActionConfigTypeDef(
    _RequiredFixedResponseActionConfigTypeDef, _OptionalFixedResponseActionConfigTypeDef
):
    pass


TargetGroupStickinessConfigTypeDef = TypedDict(
    "TargetGroupStickinessConfigTypeDef", {"Enabled": bool, "DurationSeconds": int}, total=False
)

TargetGroupTupleTypeDef = TypedDict(
    "TargetGroupTupleTypeDef", {"TargetGroupArn": str, "Weight": int}, total=False
)

ForwardActionConfigTypeDef = TypedDict(
    "ForwardActionConfigTypeDef",
    {
        "TargetGroups": List[TargetGroupTupleTypeDef],
        "TargetGroupStickinessConfig": TargetGroupStickinessConfigTypeDef,
    },
    total=False,
)

_RequiredRedirectActionConfigTypeDef = TypedDict(
    "_RequiredRedirectActionConfigTypeDef", {"StatusCode": Literal["HTTP_301", "HTTP_302"]}
)
_OptionalRedirectActionConfigTypeDef = TypedDict(
    "_OptionalRedirectActionConfigTypeDef",
    {"Protocol": str, "Port": str, "Host": str, "Path": str, "Query": str},
    total=False,
)


class RedirectActionConfigTypeDef(
    _RequiredRedirectActionConfigTypeDef, _OptionalRedirectActionConfigTypeDef
):
    pass


_RequiredActionTypeDef = TypedDict(
    "_RequiredActionTypeDef",
    {
        "Type": Literal[
            "forward", "authenticate-oidc", "authenticate-cognito", "redirect", "fixed-response"
        ]
    },
)
_OptionalActionTypeDef = TypedDict(
    "_OptionalActionTypeDef",
    {
        "TargetGroupArn": str,
        "AuthenticateOidcConfig": AuthenticateOidcActionConfigTypeDef,
        "AuthenticateCognitoConfig": AuthenticateCognitoActionConfigTypeDef,
        "Order": int,
        "RedirectConfig": RedirectActionConfigTypeDef,
        "FixedResponseConfig": FixedResponseActionConfigTypeDef,
        "ForwardConfig": ForwardActionConfigTypeDef,
    },
    total=False,
)


class ActionTypeDef(_RequiredActionTypeDef, _OptionalActionTypeDef):
    pass


CertificateTypeDef = TypedDict(
    "CertificateTypeDef", {"CertificateArn": str, "IsDefault": bool}, total=False
)

AddListenerCertificatesOutputTypeDef = TypedDict(
    "AddListenerCertificatesOutputTypeDef", {"Certificates": List[CertificateTypeDef]}, total=False
)

ListenerTypeDef = TypedDict(
    "ListenerTypeDef",
    {
        "ListenerArn": str,
        "LoadBalancerArn": str,
        "Port": int,
        "Protocol": Literal["HTTP", "HTTPS", "TCP", "TLS", "UDP", "TCP_UDP"],
        "Certificates": List[CertificateTypeDef],
        "SslPolicy": str,
        "DefaultActions": List[ActionTypeDef],
    },
    total=False,
)

CreateListenerOutputTypeDef = TypedDict(
    "CreateListenerOutputTypeDef", {"Listeners": List[ListenerTypeDef]}, total=False
)

LoadBalancerAddressTypeDef = TypedDict(
    "LoadBalancerAddressTypeDef",
    {"IpAddress": str, "AllocationId": str, "PrivateIPv4Address": str},
    total=False,
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {"ZoneName": str, "SubnetId": str, "LoadBalancerAddresses": List[LoadBalancerAddressTypeDef]},
    total=False,
)

LoadBalancerStateTypeDef = TypedDict(
    "LoadBalancerStateTypeDef",
    {"Code": Literal["active", "provisioning", "active_impaired", "failed"], "Reason": str},
    total=False,
)

LoadBalancerTypeDef = TypedDict(
    "LoadBalancerTypeDef",
    {
        "LoadBalancerArn": str,
        "DNSName": str,
        "CanonicalHostedZoneId": str,
        "CreatedTime": datetime,
        "LoadBalancerName": str,
        "Scheme": Literal["internet-facing", "internal"],
        "VpcId": str,
        "State": LoadBalancerStateTypeDef,
        "Type": Literal["application", "network"],
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "SecurityGroups": List[str],
        "IpAddressType": Literal["ipv4", "dualstack"],
    },
    total=False,
)

CreateLoadBalancerOutputTypeDef = TypedDict(
    "CreateLoadBalancerOutputTypeDef", {"LoadBalancers": List[LoadBalancerTypeDef]}, total=False
)

HostHeaderConditionConfigTypeDef = TypedDict(
    "HostHeaderConditionConfigTypeDef", {"Values": List[str]}, total=False
)

HttpHeaderConditionConfigTypeDef = TypedDict(
    "HttpHeaderConditionConfigTypeDef", {"HttpHeaderName": str, "Values": List[str]}, total=False
)

HttpRequestMethodConditionConfigTypeDef = TypedDict(
    "HttpRequestMethodConditionConfigTypeDef", {"Values": List[str]}, total=False
)

PathPatternConditionConfigTypeDef = TypedDict(
    "PathPatternConditionConfigTypeDef", {"Values": List[str]}, total=False
)

QueryStringKeyValuePairTypeDef = TypedDict(
    "QueryStringKeyValuePairTypeDef", {"Key": str, "Value": str}, total=False
)

QueryStringConditionConfigTypeDef = TypedDict(
    "QueryStringConditionConfigTypeDef",
    {"Values": List[QueryStringKeyValuePairTypeDef]},
    total=False,
)

SourceIpConditionConfigTypeDef = TypedDict(
    "SourceIpConditionConfigTypeDef", {"Values": List[str]}, total=False
)

RuleConditionTypeDef = TypedDict(
    "RuleConditionTypeDef",
    {
        "Field": str,
        "Values": List[str],
        "HostHeaderConfig": HostHeaderConditionConfigTypeDef,
        "PathPatternConfig": PathPatternConditionConfigTypeDef,
        "HttpHeaderConfig": HttpHeaderConditionConfigTypeDef,
        "QueryStringConfig": QueryStringConditionConfigTypeDef,
        "HttpRequestMethodConfig": HttpRequestMethodConditionConfigTypeDef,
        "SourceIpConfig": SourceIpConditionConfigTypeDef,
    },
    total=False,
)

RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "RuleArn": str,
        "Priority": str,
        "Conditions": List[RuleConditionTypeDef],
        "Actions": List[ActionTypeDef],
        "IsDefault": bool,
    },
    total=False,
)

CreateRuleOutputTypeDef = TypedDict(
    "CreateRuleOutputTypeDef", {"Rules": List[RuleTypeDef]}, total=False
)

MatcherTypeDef = TypedDict("MatcherTypeDef", {"HttpCode": str})

TargetGroupTypeDef = TypedDict(
    "TargetGroupTypeDef",
    {
        "TargetGroupArn": str,
        "TargetGroupName": str,
        "Protocol": Literal["HTTP", "HTTPS", "TCP", "TLS", "UDP", "TCP_UDP"],
        "Port": int,
        "VpcId": str,
        "HealthCheckProtocol": Literal["HTTP", "HTTPS", "TCP", "TLS", "UDP", "TCP_UDP"],
        "HealthCheckPort": str,
        "HealthCheckEnabled": bool,
        "HealthCheckIntervalSeconds": int,
        "HealthCheckTimeoutSeconds": int,
        "HealthyThresholdCount": int,
        "UnhealthyThresholdCount": int,
        "HealthCheckPath": str,
        "Matcher": MatcherTypeDef,
        "LoadBalancerArns": List[str],
        "TargetType": Literal["instance", "ip", "lambda"],
    },
    total=False,
)

CreateTargetGroupOutputTypeDef = TypedDict(
    "CreateTargetGroupOutputTypeDef", {"TargetGroups": List[TargetGroupTypeDef]}, total=False
)

LimitTypeDef = TypedDict("LimitTypeDef", {"Name": str, "Max": str}, total=False)

DescribeAccountLimitsOutputTypeDef = TypedDict(
    "DescribeAccountLimitsOutputTypeDef",
    {"Limits": List[LimitTypeDef], "NextMarker": str},
    total=False,
)

DescribeListenerCertificatesOutputTypeDef = TypedDict(
    "DescribeListenerCertificatesOutputTypeDef",
    {"Certificates": List[CertificateTypeDef], "NextMarker": str},
    total=False,
)

DescribeListenersOutputTypeDef = TypedDict(
    "DescribeListenersOutputTypeDef",
    {"Listeners": List[ListenerTypeDef], "NextMarker": str},
    total=False,
)

LoadBalancerAttributeTypeDef = TypedDict(
    "LoadBalancerAttributeTypeDef", {"Key": str, "Value": str}, total=False
)

DescribeLoadBalancerAttributesOutputTypeDef = TypedDict(
    "DescribeLoadBalancerAttributesOutputTypeDef",
    {"Attributes": List[LoadBalancerAttributeTypeDef]},
    total=False,
)

DescribeLoadBalancersOutputTypeDef = TypedDict(
    "DescribeLoadBalancersOutputTypeDef",
    {"LoadBalancers": List[LoadBalancerTypeDef], "NextMarker": str},
    total=False,
)

DescribeRulesOutputTypeDef = TypedDict(
    "DescribeRulesOutputTypeDef", {"Rules": List[RuleTypeDef], "NextMarker": str}, total=False
)

CipherTypeDef = TypedDict("CipherTypeDef", {"Name": str, "Priority": int}, total=False)

SslPolicyTypeDef = TypedDict(
    "SslPolicyTypeDef",
    {"SslProtocols": List[str], "Ciphers": List[CipherTypeDef], "Name": str},
    total=False,
)

DescribeSSLPoliciesOutputTypeDef = TypedDict(
    "DescribeSSLPoliciesOutputTypeDef",
    {"SslPolicies": List[SslPolicyTypeDef], "NextMarker": str},
    total=False,
)

_RequiredTagTypeDef = TypedDict("_RequiredTagTypeDef", {"Key": str})
_OptionalTagTypeDef = TypedDict("_OptionalTagTypeDef", {"Value": str}, total=False)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


TagDescriptionTypeDef = TypedDict(
    "TagDescriptionTypeDef", {"ResourceArn": str, "Tags": List[TagTypeDef]}, total=False
)

DescribeTagsOutputTypeDef = TypedDict(
    "DescribeTagsOutputTypeDef", {"TagDescriptions": List[TagDescriptionTypeDef]}, total=False
)

TargetGroupAttributeTypeDef = TypedDict(
    "TargetGroupAttributeTypeDef", {"Key": str, "Value": str}, total=False
)

DescribeTargetGroupAttributesOutputTypeDef = TypedDict(
    "DescribeTargetGroupAttributesOutputTypeDef",
    {"Attributes": List[TargetGroupAttributeTypeDef]},
    total=False,
)

DescribeTargetGroupsOutputTypeDef = TypedDict(
    "DescribeTargetGroupsOutputTypeDef",
    {"TargetGroups": List[TargetGroupTypeDef], "NextMarker": str},
    total=False,
)

_RequiredTargetDescriptionTypeDef = TypedDict("_RequiredTargetDescriptionTypeDef", {"Id": str})
_OptionalTargetDescriptionTypeDef = TypedDict(
    "_OptionalTargetDescriptionTypeDef", {"Port": int, "AvailabilityZone": str}, total=False
)


class TargetDescriptionTypeDef(
    _RequiredTargetDescriptionTypeDef, _OptionalTargetDescriptionTypeDef
):
    pass


TargetHealthTypeDef = TypedDict(
    "TargetHealthTypeDef",
    {
        "State": Literal["initial", "healthy", "unhealthy", "unused", "draining", "unavailable"],
        "Reason": Literal[
            "Elb.RegistrationInProgress",
            "Elb.InitialHealthChecking",
            "Target.ResponseCodeMismatch",
            "Target.Timeout",
            "Target.FailedHealthChecks",
            "Target.NotRegistered",
            "Target.NotInUse",
            "Target.DeregistrationInProgress",
            "Target.InvalidState",
            "Target.IpUnusable",
            "Target.HealthCheckDisabled",
            "Elb.InternalError",
        ],
        "Description": str,
    },
    total=False,
)

TargetHealthDescriptionTypeDef = TypedDict(
    "TargetHealthDescriptionTypeDef",
    {
        "Target": TargetDescriptionTypeDef,
        "HealthCheckPort": str,
        "TargetHealth": TargetHealthTypeDef,
    },
    total=False,
)

DescribeTargetHealthOutputTypeDef = TypedDict(
    "DescribeTargetHealthOutputTypeDef",
    {"TargetHealthDescriptions": List[TargetHealthDescriptionTypeDef]},
    total=False,
)

ModifyListenerOutputTypeDef = TypedDict(
    "ModifyListenerOutputTypeDef", {"Listeners": List[ListenerTypeDef]}, total=False
)

ModifyLoadBalancerAttributesOutputTypeDef = TypedDict(
    "ModifyLoadBalancerAttributesOutputTypeDef",
    {"Attributes": List[LoadBalancerAttributeTypeDef]},
    total=False,
)

ModifyRuleOutputTypeDef = TypedDict(
    "ModifyRuleOutputTypeDef", {"Rules": List[RuleTypeDef]}, total=False
)

ModifyTargetGroupAttributesOutputTypeDef = TypedDict(
    "ModifyTargetGroupAttributesOutputTypeDef",
    {"Attributes": List[TargetGroupAttributeTypeDef]},
    total=False,
)

ModifyTargetGroupOutputTypeDef = TypedDict(
    "ModifyTargetGroupOutputTypeDef", {"TargetGroups": List[TargetGroupTypeDef]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

RulePriorityPairTypeDef = TypedDict(
    "RulePriorityPairTypeDef", {"RuleArn": str, "Priority": int}, total=False
)

SetIpAddressTypeOutputTypeDef = TypedDict(
    "SetIpAddressTypeOutputTypeDef", {"IpAddressType": Literal["ipv4", "dualstack"]}, total=False
)

SetRulePrioritiesOutputTypeDef = TypedDict(
    "SetRulePrioritiesOutputTypeDef", {"Rules": List[RuleTypeDef]}, total=False
)

SetSecurityGroupsOutputTypeDef = TypedDict(
    "SetSecurityGroupsOutputTypeDef", {"SecurityGroupIds": List[str]}, total=False
)

SetSubnetsOutputTypeDef = TypedDict(
    "SetSubnetsOutputTypeDef", {"AvailabilityZones": List[AvailabilityZoneTypeDef]}, total=False
)

SubnetMappingTypeDef = TypedDict(
    "SubnetMappingTypeDef",
    {"SubnetId": str, "AllocationId": str, "PrivateIPv4Address": str},
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
