"""
Main interface for apigatewayv2 service type definitions.

Usage::

    from mypy_boto3.apigatewayv2.type_defs import AccessLogSettingsTypeDef

    data: AccessLogSettingsTypeDef = {...}
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
    "AccessLogSettingsTypeDef",
    "CorsTypeDef",
    "CreateApiMappingResponseTypeDef",
    "CreateApiResponseTypeDef",
    "JWTConfigurationTypeDef",
    "CreateAuthorizerResponseTypeDef",
    "CreateDeploymentResponseTypeDef",
    "DomainNameConfigurationTypeDef",
    "CreateDomainNameResponseTypeDef",
    "CreateIntegrationResponseResponseTypeDef",
    "TlsConfigTypeDef",
    "CreateIntegrationResultTypeDef",
    "CreateModelResponseTypeDef",
    "ParameterConstraintsTypeDef",
    "CreateRouteResponseResponseTypeDef",
    "CreateRouteResultTypeDef",
    "RouteSettingsTypeDef",
    "CreateStageResponseTypeDef",
    "CreateVpcLinkResponseTypeDef",
    "GetApiMappingResponseTypeDef",
    "ApiMappingTypeDef",
    "GetApiMappingsResponseTypeDef",
    "GetApiResponseTypeDef",
    "ApiTypeDef",
    "GetApisResponseTypeDef",
    "GetAuthorizerResponseTypeDef",
    "AuthorizerTypeDef",
    "GetAuthorizersResponseTypeDef",
    "GetDeploymentResponseTypeDef",
    "DeploymentTypeDef",
    "GetDeploymentsResponseTypeDef",
    "GetDomainNameResponseTypeDef",
    "DomainNameTypeDef",
    "GetDomainNamesResponseTypeDef",
    "GetIntegrationResponseResponseTypeDef",
    "IntegrationResponseTypeDef",
    "GetIntegrationResponsesResponseTypeDef",
    "GetIntegrationResultTypeDef",
    "IntegrationTypeDef",
    "GetIntegrationsResponseTypeDef",
    "GetModelResponseTypeDef",
    "GetModelTemplateResponseTypeDef",
    "ModelTypeDef",
    "GetModelsResponseTypeDef",
    "GetRouteResponseResponseTypeDef",
    "RouteResponseTypeDef",
    "GetRouteResponsesResponseTypeDef",
    "GetRouteResultTypeDef",
    "RouteTypeDef",
    "GetRoutesResponseTypeDef",
    "GetStageResponseTypeDef",
    "StageTypeDef",
    "GetStagesResponseTypeDef",
    "GetTagsResponseTypeDef",
    "GetVpcLinkResponseTypeDef",
    "VpcLinkTypeDef",
    "GetVpcLinksResponseTypeDef",
    "ImportApiResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ReimportApiResponseTypeDef",
    "TlsConfigInputTypeDef",
    "UpdateApiMappingResponseTypeDef",
    "UpdateApiResponseTypeDef",
    "UpdateAuthorizerResponseTypeDef",
    "UpdateDeploymentResponseTypeDef",
    "UpdateDomainNameResponseTypeDef",
    "UpdateIntegrationResponseResponseTypeDef",
    "UpdateIntegrationResultTypeDef",
    "UpdateModelResponseTypeDef",
    "UpdateRouteResponseResponseTypeDef",
    "UpdateRouteResultTypeDef",
    "UpdateStageResponseTypeDef",
    "UpdateVpcLinkResponseTypeDef",
)

AccessLogSettingsTypeDef = TypedDict(
    "AccessLogSettingsTypeDef", {"DestinationArn": str, "Format": str}, total=False
)

CorsTypeDef = TypedDict(
    "CorsTypeDef",
    {
        "AllowCredentials": bool,
        "AllowHeaders": List[str],
        "AllowMethods": List[str],
        "AllowOrigins": List[str],
        "ExposeHeaders": List[str],
        "MaxAge": int,
    },
    total=False,
)

CreateApiMappingResponseTypeDef = TypedDict(
    "CreateApiMappingResponseTypeDef",
    {"ApiId": str, "ApiMappingId": str, "ApiMappingKey": str, "Stage": str},
    total=False,
)

CreateApiResponseTypeDef = TypedDict(
    "CreateApiResponseTypeDef",
    {
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKeySelectionExpression": str,
        "CorsConfiguration": CorsTypeDef,
        "CreatedDate": datetime,
        "Description": str,
        "DisableSchemaValidation": bool,
        "ImportInfo": List[str],
        "Name": str,
        "ProtocolType": Literal["WEBSOCKET", "HTTP"],
        "RouteSelectionExpression": str,
        "Tags": Dict[str, str],
        "Version": str,
        "Warnings": List[str],
    },
    total=False,
)

JWTConfigurationTypeDef = TypedDict(
    "JWTConfigurationTypeDef", {"Audience": List[str], "Issuer": str}, total=False
)

CreateAuthorizerResponseTypeDef = TypedDict(
    "CreateAuthorizerResponseTypeDef",
    {
        "AuthorizerCredentialsArn": str,
        "AuthorizerId": str,
        "AuthorizerResultTtlInSeconds": int,
        "AuthorizerType": Literal["REQUEST", "JWT"],
        "AuthorizerUri": str,
        "IdentitySource": List[str],
        "IdentityValidationExpression": str,
        "JwtConfiguration": JWTConfigurationTypeDef,
        "Name": str,
    },
    total=False,
)

CreateDeploymentResponseTypeDef = TypedDict(
    "CreateDeploymentResponseTypeDef",
    {
        "AutoDeployed": bool,
        "CreatedDate": datetime,
        "DeploymentId": str,
        "DeploymentStatus": Literal["PENDING", "FAILED", "DEPLOYED"],
        "DeploymentStatusMessage": str,
        "Description": str,
    },
    total=False,
)

DomainNameConfigurationTypeDef = TypedDict(
    "DomainNameConfigurationTypeDef",
    {
        "ApiGatewayDomainName": str,
        "CertificateArn": str,
        "CertificateName": str,
        "CertificateUploadDate": datetime,
        "DomainNameStatus": Literal["AVAILABLE", "UPDATING"],
        "DomainNameStatusMessage": str,
        "EndpointType": Literal["REGIONAL", "EDGE"],
        "HostedZoneId": str,
        "SecurityPolicy": Literal["TLS_1_0", "TLS_1_2"],
    },
    total=False,
)

CreateDomainNameResponseTypeDef = TypedDict(
    "CreateDomainNameResponseTypeDef",
    {
        "ApiMappingSelectionExpression": str,
        "DomainName": str,
        "DomainNameConfigurations": List[DomainNameConfigurationTypeDef],
        "Tags": Dict[str, str],
    },
    total=False,
)

CreateIntegrationResponseResponseTypeDef = TypedDict(
    "CreateIntegrationResponseResponseTypeDef",
    {
        "ContentHandlingStrategy": Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"],
        "IntegrationResponseId": str,
        "IntegrationResponseKey": str,
        "ResponseParameters": Dict[str, str],
        "ResponseTemplates": Dict[str, str],
        "TemplateSelectionExpression": str,
    },
    total=False,
)

TlsConfigTypeDef = TypedDict("TlsConfigTypeDef", {"ServerNameToVerify": str}, total=False)

CreateIntegrationResultTypeDef = TypedDict(
    "CreateIntegrationResultTypeDef",
    {
        "ApiGatewayManaged": bool,
        "ConnectionId": str,
        "ConnectionType": Literal["INTERNET", "VPC_LINK"],
        "ContentHandlingStrategy": Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"],
        "CredentialsArn": str,
        "Description": str,
        "IntegrationId": str,
        "IntegrationMethod": str,
        "IntegrationResponseSelectionExpression": str,
        "IntegrationType": Literal["AWS", "HTTP", "MOCK", "HTTP_PROXY", "AWS_PROXY"],
        "IntegrationUri": str,
        "PassthroughBehavior": Literal["WHEN_NO_MATCH", "NEVER", "WHEN_NO_TEMPLATES"],
        "PayloadFormatVersion": str,
        "RequestParameters": Dict[str, str],
        "RequestTemplates": Dict[str, str],
        "TemplateSelectionExpression": str,
        "TimeoutInMillis": int,
        "TlsConfig": TlsConfigTypeDef,
    },
    total=False,
)

CreateModelResponseTypeDef = TypedDict(
    "CreateModelResponseTypeDef",
    {"ContentType": str, "Description": str, "ModelId": str, "Name": str, "Schema": str},
    total=False,
)

ParameterConstraintsTypeDef = TypedDict(
    "ParameterConstraintsTypeDef", {"Required": bool}, total=False
)

CreateRouteResponseResponseTypeDef = TypedDict(
    "CreateRouteResponseResponseTypeDef",
    {
        "ModelSelectionExpression": str,
        "ResponseModels": Dict[str, str],
        "ResponseParameters": Dict[str, ParameterConstraintsTypeDef],
        "RouteResponseId": str,
        "RouteResponseKey": str,
    },
    total=False,
)

CreateRouteResultTypeDef = TypedDict(
    "CreateRouteResultTypeDef",
    {
        "ApiGatewayManaged": bool,
        "ApiKeyRequired": bool,
        "AuthorizationScopes": List[str],
        "AuthorizationType": Literal["NONE", "AWS_IAM", "CUSTOM", "JWT"],
        "AuthorizerId": str,
        "ModelSelectionExpression": str,
        "OperationName": str,
        "RequestModels": Dict[str, str],
        "RequestParameters": Dict[str, ParameterConstraintsTypeDef],
        "RouteId": str,
        "RouteKey": str,
        "RouteResponseSelectionExpression": str,
        "Target": str,
    },
    total=False,
)

RouteSettingsTypeDef = TypedDict(
    "RouteSettingsTypeDef",
    {
        "DataTraceEnabled": bool,
        "DetailedMetricsEnabled": bool,
        "LoggingLevel": Literal["ERROR", "INFO", "OFF"],
        "ThrottlingBurstLimit": int,
        "ThrottlingRateLimit": float,
    },
    total=False,
)

CreateStageResponseTypeDef = TypedDict(
    "CreateStageResponseTypeDef",
    {
        "AccessLogSettings": AccessLogSettingsTypeDef,
        "ApiGatewayManaged": bool,
        "AutoDeploy": bool,
        "ClientCertificateId": str,
        "CreatedDate": datetime,
        "DefaultRouteSettings": RouteSettingsTypeDef,
        "DeploymentId": str,
        "Description": str,
        "LastDeploymentStatusMessage": str,
        "LastUpdatedDate": datetime,
        "RouteSettings": Dict[str, RouteSettingsTypeDef],
        "StageName": str,
        "StageVariables": Dict[str, str],
        "Tags": Dict[str, str],
    },
    total=False,
)

CreateVpcLinkResponseTypeDef = TypedDict(
    "CreateVpcLinkResponseTypeDef",
    {
        "CreatedDate": datetime,
        "Name": str,
        "SecurityGroupIds": List[str],
        "SubnetIds": List[str],
        "Tags": Dict[str, str],
        "VpcLinkId": str,
        "VpcLinkStatus": Literal["PENDING", "AVAILABLE", "DELETING", "FAILED", "INACTIVE"],
        "VpcLinkStatusMessage": str,
        "VpcLinkVersion": Literal["V2"],
    },
    total=False,
)

GetApiMappingResponseTypeDef = TypedDict(
    "GetApiMappingResponseTypeDef",
    {"ApiId": str, "ApiMappingId": str, "ApiMappingKey": str, "Stage": str},
    total=False,
)

_RequiredApiMappingTypeDef = TypedDict("_RequiredApiMappingTypeDef", {"ApiId": str, "Stage": str})
_OptionalApiMappingTypeDef = TypedDict(
    "_OptionalApiMappingTypeDef", {"ApiMappingId": str, "ApiMappingKey": str}, total=False
)


class ApiMappingTypeDef(_RequiredApiMappingTypeDef, _OptionalApiMappingTypeDef):
    pass


GetApiMappingsResponseTypeDef = TypedDict(
    "GetApiMappingsResponseTypeDef",
    {"Items": List[ApiMappingTypeDef], "NextToken": str},
    total=False,
)

GetApiResponseTypeDef = TypedDict(
    "GetApiResponseTypeDef",
    {
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKeySelectionExpression": str,
        "CorsConfiguration": CorsTypeDef,
        "CreatedDate": datetime,
        "Description": str,
        "DisableSchemaValidation": bool,
        "ImportInfo": List[str],
        "Name": str,
        "ProtocolType": Literal["WEBSOCKET", "HTTP"],
        "RouteSelectionExpression": str,
        "Tags": Dict[str, str],
        "Version": str,
        "Warnings": List[str],
    },
    total=False,
)

_RequiredApiTypeDef = TypedDict(
    "_RequiredApiTypeDef",
    {"Name": str, "ProtocolType": Literal["WEBSOCKET", "HTTP"], "RouteSelectionExpression": str},
)
_OptionalApiTypeDef = TypedDict(
    "_OptionalApiTypeDef",
    {
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKeySelectionExpression": str,
        "CorsConfiguration": CorsTypeDef,
        "CreatedDate": datetime,
        "Description": str,
        "DisableSchemaValidation": bool,
        "ImportInfo": List[str],
        "Tags": Dict[str, str],
        "Version": str,
        "Warnings": List[str],
    },
    total=False,
)


class ApiTypeDef(_RequiredApiTypeDef, _OptionalApiTypeDef):
    pass


GetApisResponseTypeDef = TypedDict(
    "GetApisResponseTypeDef", {"Items": List[ApiTypeDef], "NextToken": str}, total=False
)

GetAuthorizerResponseTypeDef = TypedDict(
    "GetAuthorizerResponseTypeDef",
    {
        "AuthorizerCredentialsArn": str,
        "AuthorizerId": str,
        "AuthorizerResultTtlInSeconds": int,
        "AuthorizerType": Literal["REQUEST", "JWT"],
        "AuthorizerUri": str,
        "IdentitySource": List[str],
        "IdentityValidationExpression": str,
        "JwtConfiguration": JWTConfigurationTypeDef,
        "Name": str,
    },
    total=False,
)

_RequiredAuthorizerTypeDef = TypedDict("_RequiredAuthorizerTypeDef", {"Name": str})
_OptionalAuthorizerTypeDef = TypedDict(
    "_OptionalAuthorizerTypeDef",
    {
        "AuthorizerCredentialsArn": str,
        "AuthorizerId": str,
        "AuthorizerResultTtlInSeconds": int,
        "AuthorizerType": Literal["REQUEST", "JWT"],
        "AuthorizerUri": str,
        "IdentitySource": List[str],
        "IdentityValidationExpression": str,
        "JwtConfiguration": JWTConfigurationTypeDef,
    },
    total=False,
)


class AuthorizerTypeDef(_RequiredAuthorizerTypeDef, _OptionalAuthorizerTypeDef):
    pass


GetAuthorizersResponseTypeDef = TypedDict(
    "GetAuthorizersResponseTypeDef",
    {"Items": List[AuthorizerTypeDef], "NextToken": str},
    total=False,
)

GetDeploymentResponseTypeDef = TypedDict(
    "GetDeploymentResponseTypeDef",
    {
        "AutoDeployed": bool,
        "CreatedDate": datetime,
        "DeploymentId": str,
        "DeploymentStatus": Literal["PENDING", "FAILED", "DEPLOYED"],
        "DeploymentStatusMessage": str,
        "Description": str,
    },
    total=False,
)

DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "AutoDeployed": bool,
        "CreatedDate": datetime,
        "DeploymentId": str,
        "DeploymentStatus": Literal["PENDING", "FAILED", "DEPLOYED"],
        "DeploymentStatusMessage": str,
        "Description": str,
    },
    total=False,
)

GetDeploymentsResponseTypeDef = TypedDict(
    "GetDeploymentsResponseTypeDef",
    {"Items": List[DeploymentTypeDef], "NextToken": str},
    total=False,
)

GetDomainNameResponseTypeDef = TypedDict(
    "GetDomainNameResponseTypeDef",
    {
        "ApiMappingSelectionExpression": str,
        "DomainName": str,
        "DomainNameConfigurations": List[DomainNameConfigurationTypeDef],
        "Tags": Dict[str, str],
    },
    total=False,
)

_RequiredDomainNameTypeDef = TypedDict("_RequiredDomainNameTypeDef", {"DomainName": str})
_OptionalDomainNameTypeDef = TypedDict(
    "_OptionalDomainNameTypeDef",
    {
        "ApiMappingSelectionExpression": str,
        "DomainNameConfigurations": List[DomainNameConfigurationTypeDef],
        "Tags": Dict[str, str],
    },
    total=False,
)


class DomainNameTypeDef(_RequiredDomainNameTypeDef, _OptionalDomainNameTypeDef):
    pass


GetDomainNamesResponseTypeDef = TypedDict(
    "GetDomainNamesResponseTypeDef",
    {"Items": List[DomainNameTypeDef], "NextToken": str},
    total=False,
)

GetIntegrationResponseResponseTypeDef = TypedDict(
    "GetIntegrationResponseResponseTypeDef",
    {
        "ContentHandlingStrategy": Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"],
        "IntegrationResponseId": str,
        "IntegrationResponseKey": str,
        "ResponseParameters": Dict[str, str],
        "ResponseTemplates": Dict[str, str],
        "TemplateSelectionExpression": str,
    },
    total=False,
)

_RequiredIntegrationResponseTypeDef = TypedDict(
    "_RequiredIntegrationResponseTypeDef", {"IntegrationResponseKey": str}
)
_OptionalIntegrationResponseTypeDef = TypedDict(
    "_OptionalIntegrationResponseTypeDef",
    {
        "ContentHandlingStrategy": Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"],
        "IntegrationResponseId": str,
        "ResponseParameters": Dict[str, str],
        "ResponseTemplates": Dict[str, str],
        "TemplateSelectionExpression": str,
    },
    total=False,
)


class IntegrationResponseTypeDef(
    _RequiredIntegrationResponseTypeDef, _OptionalIntegrationResponseTypeDef
):
    pass


GetIntegrationResponsesResponseTypeDef = TypedDict(
    "GetIntegrationResponsesResponseTypeDef",
    {"Items": List[IntegrationResponseTypeDef], "NextToken": str},
    total=False,
)

GetIntegrationResultTypeDef = TypedDict(
    "GetIntegrationResultTypeDef",
    {
        "ApiGatewayManaged": bool,
        "ConnectionId": str,
        "ConnectionType": Literal["INTERNET", "VPC_LINK"],
        "ContentHandlingStrategy": Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"],
        "CredentialsArn": str,
        "Description": str,
        "IntegrationId": str,
        "IntegrationMethod": str,
        "IntegrationResponseSelectionExpression": str,
        "IntegrationType": Literal["AWS", "HTTP", "MOCK", "HTTP_PROXY", "AWS_PROXY"],
        "IntegrationUri": str,
        "PassthroughBehavior": Literal["WHEN_NO_MATCH", "NEVER", "WHEN_NO_TEMPLATES"],
        "PayloadFormatVersion": str,
        "RequestParameters": Dict[str, str],
        "RequestTemplates": Dict[str, str],
        "TemplateSelectionExpression": str,
        "TimeoutInMillis": int,
        "TlsConfig": TlsConfigTypeDef,
    },
    total=False,
)

IntegrationTypeDef = TypedDict(
    "IntegrationTypeDef",
    {
        "ApiGatewayManaged": bool,
        "ConnectionId": str,
        "ConnectionType": Literal["INTERNET", "VPC_LINK"],
        "ContentHandlingStrategy": Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"],
        "CredentialsArn": str,
        "Description": str,
        "IntegrationId": str,
        "IntegrationMethod": str,
        "IntegrationResponseSelectionExpression": str,
        "IntegrationType": Literal["AWS", "HTTP", "MOCK", "HTTP_PROXY", "AWS_PROXY"],
        "IntegrationUri": str,
        "PassthroughBehavior": Literal["WHEN_NO_MATCH", "NEVER", "WHEN_NO_TEMPLATES"],
        "PayloadFormatVersion": str,
        "RequestParameters": Dict[str, str],
        "RequestTemplates": Dict[str, str],
        "TemplateSelectionExpression": str,
        "TimeoutInMillis": int,
        "TlsConfig": TlsConfigTypeDef,
    },
    total=False,
)

GetIntegrationsResponseTypeDef = TypedDict(
    "GetIntegrationsResponseTypeDef",
    {"Items": List[IntegrationTypeDef], "NextToken": str},
    total=False,
)

GetModelResponseTypeDef = TypedDict(
    "GetModelResponseTypeDef",
    {"ContentType": str, "Description": str, "ModelId": str, "Name": str, "Schema": str},
    total=False,
)

GetModelTemplateResponseTypeDef = TypedDict(
    "GetModelTemplateResponseTypeDef", {"Value": str}, total=False
)

_RequiredModelTypeDef = TypedDict("_RequiredModelTypeDef", {"Name": str})
_OptionalModelTypeDef = TypedDict(
    "_OptionalModelTypeDef",
    {"ContentType": str, "Description": str, "ModelId": str, "Schema": str},
    total=False,
)


class ModelTypeDef(_RequiredModelTypeDef, _OptionalModelTypeDef):
    pass


GetModelsResponseTypeDef = TypedDict(
    "GetModelsResponseTypeDef", {"Items": List[ModelTypeDef], "NextToken": str}, total=False
)

GetRouteResponseResponseTypeDef = TypedDict(
    "GetRouteResponseResponseTypeDef",
    {
        "ModelSelectionExpression": str,
        "ResponseModels": Dict[str, str],
        "ResponseParameters": Dict[str, ParameterConstraintsTypeDef],
        "RouteResponseId": str,
        "RouteResponseKey": str,
    },
    total=False,
)

_RequiredRouteResponseTypeDef = TypedDict(
    "_RequiredRouteResponseTypeDef", {"RouteResponseKey": str}
)
_OptionalRouteResponseTypeDef = TypedDict(
    "_OptionalRouteResponseTypeDef",
    {
        "ModelSelectionExpression": str,
        "ResponseModels": Dict[str, str],
        "ResponseParameters": Dict[str, ParameterConstraintsTypeDef],
        "RouteResponseId": str,
    },
    total=False,
)


class RouteResponseTypeDef(_RequiredRouteResponseTypeDef, _OptionalRouteResponseTypeDef):
    pass


GetRouteResponsesResponseTypeDef = TypedDict(
    "GetRouteResponsesResponseTypeDef",
    {"Items": List[RouteResponseTypeDef], "NextToken": str},
    total=False,
)

GetRouteResultTypeDef = TypedDict(
    "GetRouteResultTypeDef",
    {
        "ApiGatewayManaged": bool,
        "ApiKeyRequired": bool,
        "AuthorizationScopes": List[str],
        "AuthorizationType": Literal["NONE", "AWS_IAM", "CUSTOM", "JWT"],
        "AuthorizerId": str,
        "ModelSelectionExpression": str,
        "OperationName": str,
        "RequestModels": Dict[str, str],
        "RequestParameters": Dict[str, ParameterConstraintsTypeDef],
        "RouteId": str,
        "RouteKey": str,
        "RouteResponseSelectionExpression": str,
        "Target": str,
    },
    total=False,
)

_RequiredRouteTypeDef = TypedDict("_RequiredRouteTypeDef", {"RouteKey": str})
_OptionalRouteTypeDef = TypedDict(
    "_OptionalRouteTypeDef",
    {
        "ApiGatewayManaged": bool,
        "ApiKeyRequired": bool,
        "AuthorizationScopes": List[str],
        "AuthorizationType": Literal["NONE", "AWS_IAM", "CUSTOM", "JWT"],
        "AuthorizerId": str,
        "ModelSelectionExpression": str,
        "OperationName": str,
        "RequestModels": Dict[str, str],
        "RequestParameters": Dict[str, ParameterConstraintsTypeDef],
        "RouteId": str,
        "RouteResponseSelectionExpression": str,
        "Target": str,
    },
    total=False,
)


class RouteTypeDef(_RequiredRouteTypeDef, _OptionalRouteTypeDef):
    pass


GetRoutesResponseTypeDef = TypedDict(
    "GetRoutesResponseTypeDef", {"Items": List[RouteTypeDef], "NextToken": str}, total=False
)

GetStageResponseTypeDef = TypedDict(
    "GetStageResponseTypeDef",
    {
        "AccessLogSettings": AccessLogSettingsTypeDef,
        "ApiGatewayManaged": bool,
        "AutoDeploy": bool,
        "ClientCertificateId": str,
        "CreatedDate": datetime,
        "DefaultRouteSettings": RouteSettingsTypeDef,
        "DeploymentId": str,
        "Description": str,
        "LastDeploymentStatusMessage": str,
        "LastUpdatedDate": datetime,
        "RouteSettings": Dict[str, RouteSettingsTypeDef],
        "StageName": str,
        "StageVariables": Dict[str, str],
        "Tags": Dict[str, str],
    },
    total=False,
)

_RequiredStageTypeDef = TypedDict("_RequiredStageTypeDef", {"StageName": str})
_OptionalStageTypeDef = TypedDict(
    "_OptionalStageTypeDef",
    {
        "AccessLogSettings": AccessLogSettingsTypeDef,
        "ApiGatewayManaged": bool,
        "AutoDeploy": bool,
        "ClientCertificateId": str,
        "CreatedDate": datetime,
        "DefaultRouteSettings": RouteSettingsTypeDef,
        "DeploymentId": str,
        "Description": str,
        "LastDeploymentStatusMessage": str,
        "LastUpdatedDate": datetime,
        "RouteSettings": Dict[str, RouteSettingsTypeDef],
        "StageVariables": Dict[str, str],
        "Tags": Dict[str, str],
    },
    total=False,
)


class StageTypeDef(_RequiredStageTypeDef, _OptionalStageTypeDef):
    pass


GetStagesResponseTypeDef = TypedDict(
    "GetStagesResponseTypeDef", {"Items": List[StageTypeDef], "NextToken": str}, total=False
)

GetTagsResponseTypeDef = TypedDict("GetTagsResponseTypeDef", {"Tags": Dict[str, str]}, total=False)

GetVpcLinkResponseTypeDef = TypedDict(
    "GetVpcLinkResponseTypeDef",
    {
        "CreatedDate": datetime,
        "Name": str,
        "SecurityGroupIds": List[str],
        "SubnetIds": List[str],
        "Tags": Dict[str, str],
        "VpcLinkId": str,
        "VpcLinkStatus": Literal["PENDING", "AVAILABLE", "DELETING", "FAILED", "INACTIVE"],
        "VpcLinkStatusMessage": str,
        "VpcLinkVersion": Literal["V2"],
    },
    total=False,
)

_RequiredVpcLinkTypeDef = TypedDict(
    "_RequiredVpcLinkTypeDef",
    {"Name": str, "SecurityGroupIds": List[str], "SubnetIds": List[str], "VpcLinkId": str},
)
_OptionalVpcLinkTypeDef = TypedDict(
    "_OptionalVpcLinkTypeDef",
    {
        "CreatedDate": datetime,
        "Tags": Dict[str, str],
        "VpcLinkStatus": Literal["PENDING", "AVAILABLE", "DELETING", "FAILED", "INACTIVE"],
        "VpcLinkStatusMessage": str,
        "VpcLinkVersion": Literal["V2"],
    },
    total=False,
)


class VpcLinkTypeDef(_RequiredVpcLinkTypeDef, _OptionalVpcLinkTypeDef):
    pass


GetVpcLinksResponseTypeDef = TypedDict(
    "GetVpcLinksResponseTypeDef", {"Items": List[VpcLinkTypeDef], "NextToken": str}, total=False
)

ImportApiResponseTypeDef = TypedDict(
    "ImportApiResponseTypeDef",
    {
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKeySelectionExpression": str,
        "CorsConfiguration": CorsTypeDef,
        "CreatedDate": datetime,
        "Description": str,
        "DisableSchemaValidation": bool,
        "ImportInfo": List[str],
        "Name": str,
        "ProtocolType": Literal["WEBSOCKET", "HTTP"],
        "RouteSelectionExpression": str,
        "Tags": Dict[str, str],
        "Version": str,
        "Warnings": List[str],
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

ReimportApiResponseTypeDef = TypedDict(
    "ReimportApiResponseTypeDef",
    {
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKeySelectionExpression": str,
        "CorsConfiguration": CorsTypeDef,
        "CreatedDate": datetime,
        "Description": str,
        "DisableSchemaValidation": bool,
        "ImportInfo": List[str],
        "Name": str,
        "ProtocolType": Literal["WEBSOCKET", "HTTP"],
        "RouteSelectionExpression": str,
        "Tags": Dict[str, str],
        "Version": str,
        "Warnings": List[str],
    },
    total=False,
)

TlsConfigInputTypeDef = TypedDict("TlsConfigInputTypeDef", {"ServerNameToVerify": str}, total=False)

UpdateApiMappingResponseTypeDef = TypedDict(
    "UpdateApiMappingResponseTypeDef",
    {"ApiId": str, "ApiMappingId": str, "ApiMappingKey": str, "Stage": str},
    total=False,
)

UpdateApiResponseTypeDef = TypedDict(
    "UpdateApiResponseTypeDef",
    {
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKeySelectionExpression": str,
        "CorsConfiguration": CorsTypeDef,
        "CreatedDate": datetime,
        "Description": str,
        "DisableSchemaValidation": bool,
        "ImportInfo": List[str],
        "Name": str,
        "ProtocolType": Literal["WEBSOCKET", "HTTP"],
        "RouteSelectionExpression": str,
        "Tags": Dict[str, str],
        "Version": str,
        "Warnings": List[str],
    },
    total=False,
)

UpdateAuthorizerResponseTypeDef = TypedDict(
    "UpdateAuthorizerResponseTypeDef",
    {
        "AuthorizerCredentialsArn": str,
        "AuthorizerId": str,
        "AuthorizerResultTtlInSeconds": int,
        "AuthorizerType": Literal["REQUEST", "JWT"],
        "AuthorizerUri": str,
        "IdentitySource": List[str],
        "IdentityValidationExpression": str,
        "JwtConfiguration": JWTConfigurationTypeDef,
        "Name": str,
    },
    total=False,
)

UpdateDeploymentResponseTypeDef = TypedDict(
    "UpdateDeploymentResponseTypeDef",
    {
        "AutoDeployed": bool,
        "CreatedDate": datetime,
        "DeploymentId": str,
        "DeploymentStatus": Literal["PENDING", "FAILED", "DEPLOYED"],
        "DeploymentStatusMessage": str,
        "Description": str,
    },
    total=False,
)

UpdateDomainNameResponseTypeDef = TypedDict(
    "UpdateDomainNameResponseTypeDef",
    {
        "ApiMappingSelectionExpression": str,
        "DomainName": str,
        "DomainNameConfigurations": List[DomainNameConfigurationTypeDef],
        "Tags": Dict[str, str],
    },
    total=False,
)

UpdateIntegrationResponseResponseTypeDef = TypedDict(
    "UpdateIntegrationResponseResponseTypeDef",
    {
        "ContentHandlingStrategy": Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"],
        "IntegrationResponseId": str,
        "IntegrationResponseKey": str,
        "ResponseParameters": Dict[str, str],
        "ResponseTemplates": Dict[str, str],
        "TemplateSelectionExpression": str,
    },
    total=False,
)

UpdateIntegrationResultTypeDef = TypedDict(
    "UpdateIntegrationResultTypeDef",
    {
        "ApiGatewayManaged": bool,
        "ConnectionId": str,
        "ConnectionType": Literal["INTERNET", "VPC_LINK"],
        "ContentHandlingStrategy": Literal["CONVERT_TO_BINARY", "CONVERT_TO_TEXT"],
        "CredentialsArn": str,
        "Description": str,
        "IntegrationId": str,
        "IntegrationMethod": str,
        "IntegrationResponseSelectionExpression": str,
        "IntegrationType": Literal["AWS", "HTTP", "MOCK", "HTTP_PROXY", "AWS_PROXY"],
        "IntegrationUri": str,
        "PassthroughBehavior": Literal["WHEN_NO_MATCH", "NEVER", "WHEN_NO_TEMPLATES"],
        "PayloadFormatVersion": str,
        "RequestParameters": Dict[str, str],
        "RequestTemplates": Dict[str, str],
        "TemplateSelectionExpression": str,
        "TimeoutInMillis": int,
        "TlsConfig": TlsConfigTypeDef,
    },
    total=False,
)

UpdateModelResponseTypeDef = TypedDict(
    "UpdateModelResponseTypeDef",
    {"ContentType": str, "Description": str, "ModelId": str, "Name": str, "Schema": str},
    total=False,
)

UpdateRouteResponseResponseTypeDef = TypedDict(
    "UpdateRouteResponseResponseTypeDef",
    {
        "ModelSelectionExpression": str,
        "ResponseModels": Dict[str, str],
        "ResponseParameters": Dict[str, ParameterConstraintsTypeDef],
        "RouteResponseId": str,
        "RouteResponseKey": str,
    },
    total=False,
)

UpdateRouteResultTypeDef = TypedDict(
    "UpdateRouteResultTypeDef",
    {
        "ApiGatewayManaged": bool,
        "ApiKeyRequired": bool,
        "AuthorizationScopes": List[str],
        "AuthorizationType": Literal["NONE", "AWS_IAM", "CUSTOM", "JWT"],
        "AuthorizerId": str,
        "ModelSelectionExpression": str,
        "OperationName": str,
        "RequestModels": Dict[str, str],
        "RequestParameters": Dict[str, ParameterConstraintsTypeDef],
        "RouteId": str,
        "RouteKey": str,
        "RouteResponseSelectionExpression": str,
        "Target": str,
    },
    total=False,
)

UpdateStageResponseTypeDef = TypedDict(
    "UpdateStageResponseTypeDef",
    {
        "AccessLogSettings": AccessLogSettingsTypeDef,
        "ApiGatewayManaged": bool,
        "AutoDeploy": bool,
        "ClientCertificateId": str,
        "CreatedDate": datetime,
        "DefaultRouteSettings": RouteSettingsTypeDef,
        "DeploymentId": str,
        "Description": str,
        "LastDeploymentStatusMessage": str,
        "LastUpdatedDate": datetime,
        "RouteSettings": Dict[str, RouteSettingsTypeDef],
        "StageName": str,
        "StageVariables": Dict[str, str],
        "Tags": Dict[str, str],
    },
    total=False,
)

UpdateVpcLinkResponseTypeDef = TypedDict(
    "UpdateVpcLinkResponseTypeDef",
    {
        "CreatedDate": datetime,
        "Name": str,
        "SecurityGroupIds": List[str],
        "SubnetIds": List[str],
        "Tags": Dict[str, str],
        "VpcLinkId": str,
        "VpcLinkStatus": Literal["PENDING", "AVAILABLE", "DELETING", "FAILED", "INACTIVE"],
        "VpcLinkStatusMessage": str,
        "VpcLinkVersion": Literal["V2"],
    },
    total=False,
)
