"""
Main interface for cognito-idp service type definitions.

Usage::

    from mypy_boto3.cognito_idp.type_defs import RecoveryOptionTypeTypeDef

    data: RecoveryOptionTypeTypeDef = {...}
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
    "RecoveryOptionTypeTypeDef",
    "AccountRecoverySettingTypeTypeDef",
    "AccountTakeoverActionTypeTypeDef",
    "AccountTakeoverActionsTypeTypeDef",
    "NotifyEmailTypeTypeDef",
    "NotifyConfigurationTypeTypeDef",
    "AccountTakeoverRiskConfigurationTypeTypeDef",
    "MessageTemplateTypeTypeDef",
    "AdminCreateUserConfigTypeTypeDef",
    "AttributeTypeTypeDef",
    "MFAOptionTypeTypeDef",
    "UserTypeTypeDef",
    "AdminCreateUserResponseTypeDef",
    "DeviceTypeTypeDef",
    "AdminGetDeviceResponseTypeDef",
    "AdminGetUserResponseTypeDef",
    "NewDeviceMetadataTypeTypeDef",
    "AuthenticationResultTypeTypeDef",
    "AdminInitiateAuthResponseTypeDef",
    "AdminListDevicesResponseTypeDef",
    "GroupTypeTypeDef",
    "AdminListGroupsForUserResponseTypeDef",
    "ChallengeResponseTypeTypeDef",
    "EventContextDataTypeTypeDef",
    "EventFeedbackTypeTypeDef",
    "EventRiskTypeTypeDef",
    "AuthEventTypeTypeDef",
    "AdminListUserAuthEventsResponseTypeDef",
    "AdminRespondToAuthChallengeResponseTypeDef",
    "AnalyticsConfigurationTypeTypeDef",
    "AnalyticsMetadataTypeTypeDef",
    "AssociateSoftwareTokenResponseTypeDef",
    "CompromisedCredentialsActionsTypeTypeDef",
    "CompromisedCredentialsRiskConfigurationTypeTypeDef",
    "ConfirmDeviceResponseTypeDef",
    "HttpHeaderTypeDef",
    "ContextDataTypeTypeDef",
    "CreateGroupResponseTypeDef",
    "IdentityProviderTypeTypeDef",
    "CreateIdentityProviderResponseTypeDef",
    "ResourceServerScopeTypeTypeDef",
    "ResourceServerTypeTypeDef",
    "CreateResourceServerResponseTypeDef",
    "UserImportJobTypeTypeDef",
    "CreateUserImportJobResponseTypeDef",
    "UserPoolClientTypeTypeDef",
    "CreateUserPoolClientResponseTypeDef",
    "CreateUserPoolDomainResponseTypeDef",
    "DeviceConfigurationTypeTypeDef",
    "EmailConfigurationTypeTypeDef",
    "LambdaConfigTypeTypeDef",
    "NumberAttributeConstraintsTypeTypeDef",
    "StringAttributeConstraintsTypeTypeDef",
    "SchemaAttributeTypeTypeDef",
    "SmsConfigurationTypeTypeDef",
    "UserPoolAddOnsTypeTypeDef",
    "PasswordPolicyTypeTypeDef",
    "UserPoolPolicyTypeTypeDef",
    "UsernameConfigurationTypeTypeDef",
    "VerificationMessageTemplateTypeTypeDef",
    "UserPoolTypeTypeDef",
    "CreateUserPoolResponseTypeDef",
    "CustomDomainConfigTypeTypeDef",
    "DescribeIdentityProviderResponseTypeDef",
    "DescribeResourceServerResponseTypeDef",
    "RiskExceptionConfigurationTypeTypeDef",
    "RiskConfigurationTypeTypeDef",
    "DescribeRiskConfigurationResponseTypeDef",
    "DescribeUserImportJobResponseTypeDef",
    "DescribeUserPoolClientResponseTypeDef",
    "DomainDescriptionTypeTypeDef",
    "DescribeUserPoolDomainResponseTypeDef",
    "DescribeUserPoolResponseTypeDef",
    "DeviceSecretVerifierConfigTypeTypeDef",
    "CodeDeliveryDetailsTypeTypeDef",
    "ForgotPasswordResponseTypeDef",
    "GetCSVHeaderResponseTypeDef",
    "GetDeviceResponseTypeDef",
    "GetGroupResponseTypeDef",
    "GetIdentityProviderByIdentifierResponseTypeDef",
    "GetSigningCertificateResponseTypeDef",
    "UICustomizationTypeTypeDef",
    "GetUICustomizationResponseTypeDef",
    "GetUserAttributeVerificationCodeResponseTypeDef",
    "SmsMfaConfigTypeTypeDef",
    "SoftwareTokenMfaConfigTypeTypeDef",
    "GetUserPoolMfaConfigResponseTypeDef",
    "GetUserResponseTypeDef",
    "InitiateAuthResponseTypeDef",
    "ListDevicesResponseTypeDef",
    "ListGroupsResponseTypeDef",
    "ProviderDescriptionTypeDef",
    "ListIdentityProvidersResponseTypeDef",
    "ListResourceServersResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUserImportJobsResponseTypeDef",
    "UserPoolClientDescriptionTypeDef",
    "ListUserPoolClientsResponseTypeDef",
    "UserPoolDescriptionTypeTypeDef",
    "ListUserPoolsResponseTypeDef",
    "ListUsersInGroupResponseTypeDef",
    "ListUsersResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ProviderUserIdentifierTypeTypeDef",
    "ResendConfirmationCodeResponseTypeDef",
    "RespondToAuthChallengeResponseTypeDef",
    "SMSMfaSettingsTypeTypeDef",
    "SetRiskConfigurationResponseTypeDef",
    "SetUICustomizationResponseTypeDef",
    "SetUserPoolMfaConfigResponseTypeDef",
    "SignUpResponseTypeDef",
    "SoftwareTokenMfaSettingsTypeTypeDef",
    "StartUserImportJobResponseTypeDef",
    "StopUserImportJobResponseTypeDef",
    "UpdateGroupResponseTypeDef",
    "UpdateIdentityProviderResponseTypeDef",
    "UpdateResourceServerResponseTypeDef",
    "UpdateUserAttributesResponseTypeDef",
    "UpdateUserPoolClientResponseTypeDef",
    "UpdateUserPoolDomainResponseTypeDef",
    "UserContextDataTypeTypeDef",
    "VerifySoftwareTokenResponseTypeDef",
)

RecoveryOptionTypeTypeDef = TypedDict(
    "RecoveryOptionTypeTypeDef",
    {"Priority": int, "Name": Literal["verified_email", "verified_phone_number", "admin_only"]},
)

AccountRecoverySettingTypeTypeDef = TypedDict(
    "AccountRecoverySettingTypeTypeDef",
    {"RecoveryMechanisms": List[RecoveryOptionTypeTypeDef]},
    total=False,
)

AccountTakeoverActionTypeTypeDef = TypedDict(
    "AccountTakeoverActionTypeTypeDef",
    {
        "Notify": bool,
        "EventAction": Literal["BLOCK", "MFA_IF_CONFIGURED", "MFA_REQUIRED", "NO_ACTION"],
    },
)

AccountTakeoverActionsTypeTypeDef = TypedDict(
    "AccountTakeoverActionsTypeTypeDef",
    {
        "LowAction": AccountTakeoverActionTypeTypeDef,
        "MediumAction": AccountTakeoverActionTypeTypeDef,
        "HighAction": AccountTakeoverActionTypeTypeDef,
    },
    total=False,
)

_RequiredNotifyEmailTypeTypeDef = TypedDict("_RequiredNotifyEmailTypeTypeDef", {"Subject": str})
_OptionalNotifyEmailTypeTypeDef = TypedDict(
    "_OptionalNotifyEmailTypeTypeDef", {"HtmlBody": str, "TextBody": str}, total=False
)


class NotifyEmailTypeTypeDef(_RequiredNotifyEmailTypeTypeDef, _OptionalNotifyEmailTypeTypeDef):
    pass


_RequiredNotifyConfigurationTypeTypeDef = TypedDict(
    "_RequiredNotifyConfigurationTypeTypeDef", {"SourceArn": str}
)
_OptionalNotifyConfigurationTypeTypeDef = TypedDict(
    "_OptionalNotifyConfigurationTypeTypeDef",
    {
        "From": str,
        "ReplyTo": str,
        "BlockEmail": NotifyEmailTypeTypeDef,
        "NoActionEmail": NotifyEmailTypeTypeDef,
        "MfaEmail": NotifyEmailTypeTypeDef,
    },
    total=False,
)


class NotifyConfigurationTypeTypeDef(
    _RequiredNotifyConfigurationTypeTypeDef, _OptionalNotifyConfigurationTypeTypeDef
):
    pass


_RequiredAccountTakeoverRiskConfigurationTypeTypeDef = TypedDict(
    "_RequiredAccountTakeoverRiskConfigurationTypeTypeDef",
    {"Actions": AccountTakeoverActionsTypeTypeDef},
)
_OptionalAccountTakeoverRiskConfigurationTypeTypeDef = TypedDict(
    "_OptionalAccountTakeoverRiskConfigurationTypeTypeDef",
    {"NotifyConfiguration": NotifyConfigurationTypeTypeDef},
    total=False,
)


class AccountTakeoverRiskConfigurationTypeTypeDef(
    _RequiredAccountTakeoverRiskConfigurationTypeTypeDef,
    _OptionalAccountTakeoverRiskConfigurationTypeTypeDef,
):
    pass


MessageTemplateTypeTypeDef = TypedDict(
    "MessageTemplateTypeTypeDef",
    {"SMSMessage": str, "EmailMessage": str, "EmailSubject": str},
    total=False,
)

AdminCreateUserConfigTypeTypeDef = TypedDict(
    "AdminCreateUserConfigTypeTypeDef",
    {
        "AllowAdminCreateUserOnly": bool,
        "UnusedAccountValidityDays": int,
        "InviteMessageTemplate": MessageTemplateTypeTypeDef,
    },
    total=False,
)

_RequiredAttributeTypeTypeDef = TypedDict("_RequiredAttributeTypeTypeDef", {"Name": str})
_OptionalAttributeTypeTypeDef = TypedDict(
    "_OptionalAttributeTypeTypeDef", {"Value": str}, total=False
)


class AttributeTypeTypeDef(_RequiredAttributeTypeTypeDef, _OptionalAttributeTypeTypeDef):
    pass


MFAOptionTypeTypeDef = TypedDict(
    "MFAOptionTypeTypeDef",
    {"DeliveryMedium": Literal["SMS", "EMAIL"], "AttributeName": str},
    total=False,
)

UserTypeTypeDef = TypedDict(
    "UserTypeTypeDef",
    {
        "Username": str,
        "Attributes": List[AttributeTypeTypeDef],
        "UserCreateDate": datetime,
        "UserLastModifiedDate": datetime,
        "Enabled": bool,
        "UserStatus": Literal[
            "UNCONFIRMED",
            "CONFIRMED",
            "ARCHIVED",
            "COMPROMISED",
            "UNKNOWN",
            "RESET_REQUIRED",
            "FORCE_CHANGE_PASSWORD",
        ],
        "MFAOptions": List[MFAOptionTypeTypeDef],
    },
    total=False,
)

AdminCreateUserResponseTypeDef = TypedDict(
    "AdminCreateUserResponseTypeDef", {"User": UserTypeTypeDef}, total=False
)

DeviceTypeTypeDef = TypedDict(
    "DeviceTypeTypeDef",
    {
        "DeviceKey": str,
        "DeviceAttributes": List[AttributeTypeTypeDef],
        "DeviceCreateDate": datetime,
        "DeviceLastModifiedDate": datetime,
        "DeviceLastAuthenticatedDate": datetime,
    },
    total=False,
)

AdminGetDeviceResponseTypeDef = TypedDict(
    "AdminGetDeviceResponseTypeDef", {"Device": DeviceTypeTypeDef}
)

_RequiredAdminGetUserResponseTypeDef = TypedDict(
    "_RequiredAdminGetUserResponseTypeDef", {"Username": str}
)
_OptionalAdminGetUserResponseTypeDef = TypedDict(
    "_OptionalAdminGetUserResponseTypeDef",
    {
        "UserAttributes": List[AttributeTypeTypeDef],
        "UserCreateDate": datetime,
        "UserLastModifiedDate": datetime,
        "Enabled": bool,
        "UserStatus": Literal[
            "UNCONFIRMED",
            "CONFIRMED",
            "ARCHIVED",
            "COMPROMISED",
            "UNKNOWN",
            "RESET_REQUIRED",
            "FORCE_CHANGE_PASSWORD",
        ],
        "MFAOptions": List[MFAOptionTypeTypeDef],
        "PreferredMfaSetting": str,
        "UserMFASettingList": List[str],
    },
    total=False,
)


class AdminGetUserResponseTypeDef(
    _RequiredAdminGetUserResponseTypeDef, _OptionalAdminGetUserResponseTypeDef
):
    pass


NewDeviceMetadataTypeTypeDef = TypedDict(
    "NewDeviceMetadataTypeTypeDef", {"DeviceKey": str, "DeviceGroupKey": str}, total=False
)

AuthenticationResultTypeTypeDef = TypedDict(
    "AuthenticationResultTypeTypeDef",
    {
        "AccessToken": str,
        "ExpiresIn": int,
        "TokenType": str,
        "RefreshToken": str,
        "IdToken": str,
        "NewDeviceMetadata": NewDeviceMetadataTypeTypeDef,
    },
    total=False,
)

AdminInitiateAuthResponseTypeDef = TypedDict(
    "AdminInitiateAuthResponseTypeDef",
    {
        "ChallengeName": Literal[
            "SMS_MFA",
            "SOFTWARE_TOKEN_MFA",
            "SELECT_MFA_TYPE",
            "MFA_SETUP",
            "PASSWORD_VERIFIER",
            "CUSTOM_CHALLENGE",
            "DEVICE_SRP_AUTH",
            "DEVICE_PASSWORD_VERIFIER",
            "ADMIN_NO_SRP_AUTH",
            "NEW_PASSWORD_REQUIRED",
        ],
        "Session": str,
        "ChallengeParameters": Dict[str, str],
        "AuthenticationResult": AuthenticationResultTypeTypeDef,
    },
    total=False,
)

AdminListDevicesResponseTypeDef = TypedDict(
    "AdminListDevicesResponseTypeDef",
    {"Devices": List[DeviceTypeTypeDef], "PaginationToken": str},
    total=False,
)

GroupTypeTypeDef = TypedDict(
    "GroupTypeTypeDef",
    {
        "GroupName": str,
        "UserPoolId": str,
        "Description": str,
        "RoleArn": str,
        "Precedence": int,
        "LastModifiedDate": datetime,
        "CreationDate": datetime,
    },
    total=False,
)

AdminListGroupsForUserResponseTypeDef = TypedDict(
    "AdminListGroupsForUserResponseTypeDef",
    {"Groups": List[GroupTypeTypeDef], "NextToken": str},
    total=False,
)

ChallengeResponseTypeTypeDef = TypedDict(
    "ChallengeResponseTypeTypeDef",
    {
        "ChallengeName": Literal["Password", "Mfa"],
        "ChallengeResponse": Literal["Success", "Failure"],
    },
    total=False,
)

EventContextDataTypeTypeDef = TypedDict(
    "EventContextDataTypeTypeDef",
    {"IpAddress": str, "DeviceName": str, "Timezone": str, "City": str, "Country": str},
    total=False,
)

_RequiredEventFeedbackTypeTypeDef = TypedDict(
    "_RequiredEventFeedbackTypeTypeDef",
    {"FeedbackValue": Literal["Valid", "Invalid"], "Provider": str},
)
_OptionalEventFeedbackTypeTypeDef = TypedDict(
    "_OptionalEventFeedbackTypeTypeDef", {"FeedbackDate": datetime}, total=False
)


class EventFeedbackTypeTypeDef(
    _RequiredEventFeedbackTypeTypeDef, _OptionalEventFeedbackTypeTypeDef
):
    pass


EventRiskTypeTypeDef = TypedDict(
    "EventRiskTypeTypeDef",
    {
        "RiskDecision": Literal["NoRisk", "AccountTakeover", "Block"],
        "RiskLevel": Literal["Low", "Medium", "High"],
        "CompromisedCredentialsDetected": bool,
    },
    total=False,
)

AuthEventTypeTypeDef = TypedDict(
    "AuthEventTypeTypeDef",
    {
        "EventId": str,
        "EventType": Literal["SignIn", "SignUp", "ForgotPassword"],
        "CreationDate": datetime,
        "EventResponse": Literal["Success", "Failure"],
        "EventRisk": EventRiskTypeTypeDef,
        "ChallengeResponses": List[ChallengeResponseTypeTypeDef],
        "EventContextData": EventContextDataTypeTypeDef,
        "EventFeedback": EventFeedbackTypeTypeDef,
    },
    total=False,
)

AdminListUserAuthEventsResponseTypeDef = TypedDict(
    "AdminListUserAuthEventsResponseTypeDef",
    {"AuthEvents": List[AuthEventTypeTypeDef], "NextToken": str},
    total=False,
)

AdminRespondToAuthChallengeResponseTypeDef = TypedDict(
    "AdminRespondToAuthChallengeResponseTypeDef",
    {
        "ChallengeName": Literal[
            "SMS_MFA",
            "SOFTWARE_TOKEN_MFA",
            "SELECT_MFA_TYPE",
            "MFA_SETUP",
            "PASSWORD_VERIFIER",
            "CUSTOM_CHALLENGE",
            "DEVICE_SRP_AUTH",
            "DEVICE_PASSWORD_VERIFIER",
            "ADMIN_NO_SRP_AUTH",
            "NEW_PASSWORD_REQUIRED",
        ],
        "Session": str,
        "ChallengeParameters": Dict[str, str],
        "AuthenticationResult": AuthenticationResultTypeTypeDef,
    },
    total=False,
)

_RequiredAnalyticsConfigurationTypeTypeDef = TypedDict(
    "_RequiredAnalyticsConfigurationTypeTypeDef",
    {"ApplicationId": str, "RoleArn": str, "ExternalId": str},
)
_OptionalAnalyticsConfigurationTypeTypeDef = TypedDict(
    "_OptionalAnalyticsConfigurationTypeTypeDef", {"UserDataShared": bool}, total=False
)


class AnalyticsConfigurationTypeTypeDef(
    _RequiredAnalyticsConfigurationTypeTypeDef, _OptionalAnalyticsConfigurationTypeTypeDef
):
    pass


AnalyticsMetadataTypeTypeDef = TypedDict(
    "AnalyticsMetadataTypeTypeDef", {"AnalyticsEndpointId": str}, total=False
)

AssociateSoftwareTokenResponseTypeDef = TypedDict(
    "AssociateSoftwareTokenResponseTypeDef", {"SecretCode": str, "Session": str}, total=False
)

CompromisedCredentialsActionsTypeTypeDef = TypedDict(
    "CompromisedCredentialsActionsTypeTypeDef", {"EventAction": Literal["BLOCK", "NO_ACTION"]}
)

_RequiredCompromisedCredentialsRiskConfigurationTypeTypeDef = TypedDict(
    "_RequiredCompromisedCredentialsRiskConfigurationTypeTypeDef",
    {"Actions": CompromisedCredentialsActionsTypeTypeDef},
)
_OptionalCompromisedCredentialsRiskConfigurationTypeTypeDef = TypedDict(
    "_OptionalCompromisedCredentialsRiskConfigurationTypeTypeDef",
    {"EventFilter": List[Literal["SIGN_IN", "PASSWORD_CHANGE", "SIGN_UP"]]},
    total=False,
)


class CompromisedCredentialsRiskConfigurationTypeTypeDef(
    _RequiredCompromisedCredentialsRiskConfigurationTypeTypeDef,
    _OptionalCompromisedCredentialsRiskConfigurationTypeTypeDef,
):
    pass


ConfirmDeviceResponseTypeDef = TypedDict(
    "ConfirmDeviceResponseTypeDef", {"UserConfirmationNecessary": bool}, total=False
)

HttpHeaderTypeDef = TypedDict(
    "HttpHeaderTypeDef", {"headerName": str, "headerValue": str}, total=False
)

_RequiredContextDataTypeTypeDef = TypedDict(
    "_RequiredContextDataTypeTypeDef",
    {
        "IpAddress": str,
        "ServerName": str,
        "ServerPath": str,
        "HttpHeaders": List[HttpHeaderTypeDef],
    },
)
_OptionalContextDataTypeTypeDef = TypedDict(
    "_OptionalContextDataTypeTypeDef", {"EncodedData": str}, total=False
)


class ContextDataTypeTypeDef(_RequiredContextDataTypeTypeDef, _OptionalContextDataTypeTypeDef):
    pass


CreateGroupResponseTypeDef = TypedDict(
    "CreateGroupResponseTypeDef", {"Group": GroupTypeTypeDef}, total=False
)

IdentityProviderTypeTypeDef = TypedDict(
    "IdentityProviderTypeTypeDef",
    {
        "UserPoolId": str,
        "ProviderName": str,
        "ProviderType": Literal[
            "SAML", "Facebook", "Google", "LoginWithAmazon", "SignInWithApple", "OIDC"
        ],
        "ProviderDetails": Dict[str, str],
        "AttributeMapping": Dict[str, str],
        "IdpIdentifiers": List[str],
        "LastModifiedDate": datetime,
        "CreationDate": datetime,
    },
    total=False,
)

CreateIdentityProviderResponseTypeDef = TypedDict(
    "CreateIdentityProviderResponseTypeDef", {"IdentityProvider": IdentityProviderTypeTypeDef}
)

ResourceServerScopeTypeTypeDef = TypedDict(
    "ResourceServerScopeTypeTypeDef", {"ScopeName": str, "ScopeDescription": str}
)

ResourceServerTypeTypeDef = TypedDict(
    "ResourceServerTypeTypeDef",
    {
        "UserPoolId": str,
        "Identifier": str,
        "Name": str,
        "Scopes": List[ResourceServerScopeTypeTypeDef],
    },
    total=False,
)

CreateResourceServerResponseTypeDef = TypedDict(
    "CreateResourceServerResponseTypeDef", {"ResourceServer": ResourceServerTypeTypeDef}
)

UserImportJobTypeTypeDef = TypedDict(
    "UserImportJobTypeTypeDef",
    {
        "JobName": str,
        "JobId": str,
        "UserPoolId": str,
        "PreSignedUrl": str,
        "CreationDate": datetime,
        "StartDate": datetime,
        "CompletionDate": datetime,
        "Status": Literal[
            "Created",
            "Pending",
            "InProgress",
            "Stopping",
            "Expired",
            "Stopped",
            "Failed",
            "Succeeded",
        ],
        "CloudWatchLogsRoleArn": str,
        "ImportedUsers": int,
        "SkippedUsers": int,
        "FailedUsers": int,
        "CompletionMessage": str,
    },
    total=False,
)

CreateUserImportJobResponseTypeDef = TypedDict(
    "CreateUserImportJobResponseTypeDef", {"UserImportJob": UserImportJobTypeTypeDef}, total=False
)

UserPoolClientTypeTypeDef = TypedDict(
    "UserPoolClientTypeTypeDef",
    {
        "UserPoolId": str,
        "ClientName": str,
        "ClientId": str,
        "ClientSecret": str,
        "LastModifiedDate": datetime,
        "CreationDate": datetime,
        "RefreshTokenValidity": int,
        "ReadAttributes": List[str],
        "WriteAttributes": List[str],
        "ExplicitAuthFlows": List[
            Literal[
                "ADMIN_NO_SRP_AUTH",
                "CUSTOM_AUTH_FLOW_ONLY",
                "USER_PASSWORD_AUTH",
                "ALLOW_ADMIN_USER_PASSWORD_AUTH",
                "ALLOW_CUSTOM_AUTH",
                "ALLOW_USER_PASSWORD_AUTH",
                "ALLOW_USER_SRP_AUTH",
                "ALLOW_REFRESH_TOKEN_AUTH",
            ]
        ],
        "SupportedIdentityProviders": List[str],
        "CallbackURLs": List[str],
        "LogoutURLs": List[str],
        "DefaultRedirectURI": str,
        "AllowedOAuthFlows": List[Literal["code", "implicit", "client_credentials"]],
        "AllowedOAuthScopes": List[str],
        "AllowedOAuthFlowsUserPoolClient": bool,
        "AnalyticsConfiguration": AnalyticsConfigurationTypeTypeDef,
        "PreventUserExistenceErrors": Literal["LEGACY", "ENABLED"],
    },
    total=False,
)

CreateUserPoolClientResponseTypeDef = TypedDict(
    "CreateUserPoolClientResponseTypeDef",
    {"UserPoolClient": UserPoolClientTypeTypeDef},
    total=False,
)

CreateUserPoolDomainResponseTypeDef = TypedDict(
    "CreateUserPoolDomainResponseTypeDef", {"CloudFrontDomain": str}, total=False
)

DeviceConfigurationTypeTypeDef = TypedDict(
    "DeviceConfigurationTypeTypeDef",
    {"ChallengeRequiredOnNewDevice": bool, "DeviceOnlyRememberedOnUserPrompt": bool},
    total=False,
)

EmailConfigurationTypeTypeDef = TypedDict(
    "EmailConfigurationTypeTypeDef",
    {
        "SourceArn": str,
        "ReplyToEmailAddress": str,
        "EmailSendingAccount": Literal["COGNITO_DEFAULT", "DEVELOPER"],
        "From": str,
        "ConfigurationSet": str,
    },
    total=False,
)

LambdaConfigTypeTypeDef = TypedDict(
    "LambdaConfigTypeTypeDef",
    {
        "PreSignUp": str,
        "CustomMessage": str,
        "PostConfirmation": str,
        "PreAuthentication": str,
        "PostAuthentication": str,
        "DefineAuthChallenge": str,
        "CreateAuthChallenge": str,
        "VerifyAuthChallengeResponse": str,
        "PreTokenGeneration": str,
        "UserMigration": str,
    },
    total=False,
)

NumberAttributeConstraintsTypeTypeDef = TypedDict(
    "NumberAttributeConstraintsTypeTypeDef", {"MinValue": str, "MaxValue": str}, total=False
)

StringAttributeConstraintsTypeTypeDef = TypedDict(
    "StringAttributeConstraintsTypeTypeDef", {"MinLength": str, "MaxLength": str}, total=False
)

SchemaAttributeTypeTypeDef = TypedDict(
    "SchemaAttributeTypeTypeDef",
    {
        "Name": str,
        "AttributeDataType": Literal["String", "Number", "DateTime", "Boolean"],
        "DeveloperOnlyAttribute": bool,
        "Mutable": bool,
        "Required": bool,
        "NumberAttributeConstraints": NumberAttributeConstraintsTypeTypeDef,
        "StringAttributeConstraints": StringAttributeConstraintsTypeTypeDef,
    },
    total=False,
)

_RequiredSmsConfigurationTypeTypeDef = TypedDict(
    "_RequiredSmsConfigurationTypeTypeDef", {"SnsCallerArn": str}
)
_OptionalSmsConfigurationTypeTypeDef = TypedDict(
    "_OptionalSmsConfigurationTypeTypeDef", {"ExternalId": str}, total=False
)


class SmsConfigurationTypeTypeDef(
    _RequiredSmsConfigurationTypeTypeDef, _OptionalSmsConfigurationTypeTypeDef
):
    pass


UserPoolAddOnsTypeTypeDef = TypedDict(
    "UserPoolAddOnsTypeTypeDef", {"AdvancedSecurityMode": Literal["OFF", "AUDIT", "ENFORCED"]}
)

PasswordPolicyTypeTypeDef = TypedDict(
    "PasswordPolicyTypeTypeDef",
    {
        "MinimumLength": int,
        "RequireUppercase": bool,
        "RequireLowercase": bool,
        "RequireNumbers": bool,
        "RequireSymbols": bool,
        "TemporaryPasswordValidityDays": int,
    },
    total=False,
)

UserPoolPolicyTypeTypeDef = TypedDict(
    "UserPoolPolicyTypeTypeDef", {"PasswordPolicy": PasswordPolicyTypeTypeDef}, total=False
)

UsernameConfigurationTypeTypeDef = TypedDict(
    "UsernameConfigurationTypeTypeDef", {"CaseSensitive": bool}
)

VerificationMessageTemplateTypeTypeDef = TypedDict(
    "VerificationMessageTemplateTypeTypeDef",
    {
        "SmsMessage": str,
        "EmailMessage": str,
        "EmailSubject": str,
        "EmailMessageByLink": str,
        "EmailSubjectByLink": str,
        "DefaultEmailOption": Literal["CONFIRM_WITH_LINK", "CONFIRM_WITH_CODE"],
    },
    total=False,
)

UserPoolTypeTypeDef = TypedDict(
    "UserPoolTypeTypeDef",
    {
        "Id": str,
        "Name": str,
        "Policies": UserPoolPolicyTypeTypeDef,
        "LambdaConfig": LambdaConfigTypeTypeDef,
        "Status": Literal["Enabled", "Disabled"],
        "LastModifiedDate": datetime,
        "CreationDate": datetime,
        "SchemaAttributes": List[SchemaAttributeTypeTypeDef],
        "AutoVerifiedAttributes": List[Literal["phone_number", "email"]],
        "AliasAttributes": List[Literal["phone_number", "email", "preferred_username"]],
        "UsernameAttributes": List[Literal["phone_number", "email"]],
        "SmsVerificationMessage": str,
        "EmailVerificationMessage": str,
        "EmailVerificationSubject": str,
        "VerificationMessageTemplate": VerificationMessageTemplateTypeTypeDef,
        "SmsAuthenticationMessage": str,
        "MfaConfiguration": Literal["OFF", "ON", "OPTIONAL"],
        "DeviceConfiguration": DeviceConfigurationTypeTypeDef,
        "EstimatedNumberOfUsers": int,
        "EmailConfiguration": EmailConfigurationTypeTypeDef,
        "SmsConfiguration": SmsConfigurationTypeTypeDef,
        "UserPoolTags": Dict[str, str],
        "SmsConfigurationFailure": str,
        "EmailConfigurationFailure": str,
        "Domain": str,
        "CustomDomain": str,
        "AdminCreateUserConfig": AdminCreateUserConfigTypeTypeDef,
        "UserPoolAddOns": UserPoolAddOnsTypeTypeDef,
        "UsernameConfiguration": UsernameConfigurationTypeTypeDef,
        "Arn": str,
        "AccountRecoverySetting": AccountRecoverySettingTypeTypeDef,
    },
    total=False,
)

CreateUserPoolResponseTypeDef = TypedDict(
    "CreateUserPoolResponseTypeDef", {"UserPool": UserPoolTypeTypeDef}, total=False
)

CustomDomainConfigTypeTypeDef = TypedDict("CustomDomainConfigTypeTypeDef", {"CertificateArn": str})

DescribeIdentityProviderResponseTypeDef = TypedDict(
    "DescribeIdentityProviderResponseTypeDef", {"IdentityProvider": IdentityProviderTypeTypeDef}
)

DescribeResourceServerResponseTypeDef = TypedDict(
    "DescribeResourceServerResponseTypeDef", {"ResourceServer": ResourceServerTypeTypeDef}
)

RiskExceptionConfigurationTypeTypeDef = TypedDict(
    "RiskExceptionConfigurationTypeTypeDef",
    {"BlockedIPRangeList": List[str], "SkippedIPRangeList": List[str]},
    total=False,
)

RiskConfigurationTypeTypeDef = TypedDict(
    "RiskConfigurationTypeTypeDef",
    {
        "UserPoolId": str,
        "ClientId": str,
        "CompromisedCredentialsRiskConfiguration": CompromisedCredentialsRiskConfigurationTypeTypeDef,
        "AccountTakeoverRiskConfiguration": AccountTakeoverRiskConfigurationTypeTypeDef,
        "RiskExceptionConfiguration": RiskExceptionConfigurationTypeTypeDef,
        "LastModifiedDate": datetime,
    },
    total=False,
)

DescribeRiskConfigurationResponseTypeDef = TypedDict(
    "DescribeRiskConfigurationResponseTypeDef", {"RiskConfiguration": RiskConfigurationTypeTypeDef}
)

DescribeUserImportJobResponseTypeDef = TypedDict(
    "DescribeUserImportJobResponseTypeDef", {"UserImportJob": UserImportJobTypeTypeDef}, total=False
)

DescribeUserPoolClientResponseTypeDef = TypedDict(
    "DescribeUserPoolClientResponseTypeDef",
    {"UserPoolClient": UserPoolClientTypeTypeDef},
    total=False,
)

DomainDescriptionTypeTypeDef = TypedDict(
    "DomainDescriptionTypeTypeDef",
    {
        "UserPoolId": str,
        "AWSAccountId": str,
        "Domain": str,
        "S3Bucket": str,
        "CloudFrontDistribution": str,
        "Version": str,
        "Status": Literal["CREATING", "DELETING", "UPDATING", "ACTIVE", "FAILED"],
        "CustomDomainConfig": CustomDomainConfigTypeTypeDef,
    },
    total=False,
)

DescribeUserPoolDomainResponseTypeDef = TypedDict(
    "DescribeUserPoolDomainResponseTypeDef",
    {"DomainDescription": DomainDescriptionTypeTypeDef},
    total=False,
)

DescribeUserPoolResponseTypeDef = TypedDict(
    "DescribeUserPoolResponseTypeDef", {"UserPool": UserPoolTypeTypeDef}, total=False
)

DeviceSecretVerifierConfigTypeTypeDef = TypedDict(
    "DeviceSecretVerifierConfigTypeTypeDef", {"PasswordVerifier": str, "Salt": str}, total=False
)

CodeDeliveryDetailsTypeTypeDef = TypedDict(
    "CodeDeliveryDetailsTypeTypeDef",
    {"Destination": str, "DeliveryMedium": Literal["SMS", "EMAIL"], "AttributeName": str},
    total=False,
)

ForgotPasswordResponseTypeDef = TypedDict(
    "ForgotPasswordResponseTypeDef",
    {"CodeDeliveryDetails": CodeDeliveryDetailsTypeTypeDef},
    total=False,
)

GetCSVHeaderResponseTypeDef = TypedDict(
    "GetCSVHeaderResponseTypeDef", {"UserPoolId": str, "CSVHeader": List[str]}, total=False
)

GetDeviceResponseTypeDef = TypedDict("GetDeviceResponseTypeDef", {"Device": DeviceTypeTypeDef})

GetGroupResponseTypeDef = TypedDict(
    "GetGroupResponseTypeDef", {"Group": GroupTypeTypeDef}, total=False
)

GetIdentityProviderByIdentifierResponseTypeDef = TypedDict(
    "GetIdentityProviderByIdentifierResponseTypeDef",
    {"IdentityProvider": IdentityProviderTypeTypeDef},
)

GetSigningCertificateResponseTypeDef = TypedDict(
    "GetSigningCertificateResponseTypeDef", {"Certificate": str}, total=False
)

UICustomizationTypeTypeDef = TypedDict(
    "UICustomizationTypeTypeDef",
    {
        "UserPoolId": str,
        "ClientId": str,
        "ImageUrl": str,
        "CSS": str,
        "CSSVersion": str,
        "LastModifiedDate": datetime,
        "CreationDate": datetime,
    },
    total=False,
)

GetUICustomizationResponseTypeDef = TypedDict(
    "GetUICustomizationResponseTypeDef", {"UICustomization": UICustomizationTypeTypeDef}
)

GetUserAttributeVerificationCodeResponseTypeDef = TypedDict(
    "GetUserAttributeVerificationCodeResponseTypeDef",
    {"CodeDeliveryDetails": CodeDeliveryDetailsTypeTypeDef},
    total=False,
)

SmsMfaConfigTypeTypeDef = TypedDict(
    "SmsMfaConfigTypeTypeDef",
    {"SmsAuthenticationMessage": str, "SmsConfiguration": SmsConfigurationTypeTypeDef},
    total=False,
)

SoftwareTokenMfaConfigTypeTypeDef = TypedDict(
    "SoftwareTokenMfaConfigTypeTypeDef", {"Enabled": bool}, total=False
)

GetUserPoolMfaConfigResponseTypeDef = TypedDict(
    "GetUserPoolMfaConfigResponseTypeDef",
    {
        "SmsMfaConfiguration": SmsMfaConfigTypeTypeDef,
        "SoftwareTokenMfaConfiguration": SoftwareTokenMfaConfigTypeTypeDef,
        "MfaConfiguration": Literal["OFF", "ON", "OPTIONAL"],
    },
    total=False,
)

_RequiredGetUserResponseTypeDef = TypedDict(
    "_RequiredGetUserResponseTypeDef",
    {"Username": str, "UserAttributes": List[AttributeTypeTypeDef]},
)
_OptionalGetUserResponseTypeDef = TypedDict(
    "_OptionalGetUserResponseTypeDef",
    {
        "MFAOptions": List[MFAOptionTypeTypeDef],
        "PreferredMfaSetting": str,
        "UserMFASettingList": List[str],
    },
    total=False,
)


class GetUserResponseTypeDef(_RequiredGetUserResponseTypeDef, _OptionalGetUserResponseTypeDef):
    pass


InitiateAuthResponseTypeDef = TypedDict(
    "InitiateAuthResponseTypeDef",
    {
        "ChallengeName": Literal[
            "SMS_MFA",
            "SOFTWARE_TOKEN_MFA",
            "SELECT_MFA_TYPE",
            "MFA_SETUP",
            "PASSWORD_VERIFIER",
            "CUSTOM_CHALLENGE",
            "DEVICE_SRP_AUTH",
            "DEVICE_PASSWORD_VERIFIER",
            "ADMIN_NO_SRP_AUTH",
            "NEW_PASSWORD_REQUIRED",
        ],
        "Session": str,
        "ChallengeParameters": Dict[str, str],
        "AuthenticationResult": AuthenticationResultTypeTypeDef,
    },
    total=False,
)

ListDevicesResponseTypeDef = TypedDict(
    "ListDevicesResponseTypeDef",
    {"Devices": List[DeviceTypeTypeDef], "PaginationToken": str},
    total=False,
)

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef", {"Groups": List[GroupTypeTypeDef], "NextToken": str}, total=False
)

ProviderDescriptionTypeDef = TypedDict(
    "ProviderDescriptionTypeDef",
    {
        "ProviderName": str,
        "ProviderType": Literal[
            "SAML", "Facebook", "Google", "LoginWithAmazon", "SignInWithApple", "OIDC"
        ],
        "LastModifiedDate": datetime,
        "CreationDate": datetime,
    },
    total=False,
)

_RequiredListIdentityProvidersResponseTypeDef = TypedDict(
    "_RequiredListIdentityProvidersResponseTypeDef", {"Providers": List[ProviderDescriptionTypeDef]}
)
_OptionalListIdentityProvidersResponseTypeDef = TypedDict(
    "_OptionalListIdentityProvidersResponseTypeDef", {"NextToken": str}, total=False
)


class ListIdentityProvidersResponseTypeDef(
    _RequiredListIdentityProvidersResponseTypeDef, _OptionalListIdentityProvidersResponseTypeDef
):
    pass


_RequiredListResourceServersResponseTypeDef = TypedDict(
    "_RequiredListResourceServersResponseTypeDef",
    {"ResourceServers": List[ResourceServerTypeTypeDef]},
)
_OptionalListResourceServersResponseTypeDef = TypedDict(
    "_OptionalListResourceServersResponseTypeDef", {"NextToken": str}, total=False
)


class ListResourceServersResponseTypeDef(
    _RequiredListResourceServersResponseTypeDef, _OptionalListResourceServersResponseTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

ListUserImportJobsResponseTypeDef = TypedDict(
    "ListUserImportJobsResponseTypeDef",
    {"UserImportJobs": List[UserImportJobTypeTypeDef], "PaginationToken": str},
    total=False,
)

UserPoolClientDescriptionTypeDef = TypedDict(
    "UserPoolClientDescriptionTypeDef",
    {"ClientId": str, "UserPoolId": str, "ClientName": str},
    total=False,
)

ListUserPoolClientsResponseTypeDef = TypedDict(
    "ListUserPoolClientsResponseTypeDef",
    {"UserPoolClients": List[UserPoolClientDescriptionTypeDef], "NextToken": str},
    total=False,
)

UserPoolDescriptionTypeTypeDef = TypedDict(
    "UserPoolDescriptionTypeTypeDef",
    {
        "Id": str,
        "Name": str,
        "LambdaConfig": LambdaConfigTypeTypeDef,
        "Status": Literal["Enabled", "Disabled"],
        "LastModifiedDate": datetime,
        "CreationDate": datetime,
    },
    total=False,
)

ListUserPoolsResponseTypeDef = TypedDict(
    "ListUserPoolsResponseTypeDef",
    {"UserPools": List[UserPoolDescriptionTypeTypeDef], "NextToken": str},
    total=False,
)

ListUsersInGroupResponseTypeDef = TypedDict(
    "ListUsersInGroupResponseTypeDef",
    {"Users": List[UserTypeTypeDef], "NextToken": str},
    total=False,
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {"Users": List[UserTypeTypeDef], "PaginationToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

ProviderUserIdentifierTypeTypeDef = TypedDict(
    "ProviderUserIdentifierTypeTypeDef",
    {"ProviderName": str, "ProviderAttributeName": str, "ProviderAttributeValue": str},
    total=False,
)

ResendConfirmationCodeResponseTypeDef = TypedDict(
    "ResendConfirmationCodeResponseTypeDef",
    {"CodeDeliveryDetails": CodeDeliveryDetailsTypeTypeDef},
    total=False,
)

RespondToAuthChallengeResponseTypeDef = TypedDict(
    "RespondToAuthChallengeResponseTypeDef",
    {
        "ChallengeName": Literal[
            "SMS_MFA",
            "SOFTWARE_TOKEN_MFA",
            "SELECT_MFA_TYPE",
            "MFA_SETUP",
            "PASSWORD_VERIFIER",
            "CUSTOM_CHALLENGE",
            "DEVICE_SRP_AUTH",
            "DEVICE_PASSWORD_VERIFIER",
            "ADMIN_NO_SRP_AUTH",
            "NEW_PASSWORD_REQUIRED",
        ],
        "Session": str,
        "ChallengeParameters": Dict[str, str],
        "AuthenticationResult": AuthenticationResultTypeTypeDef,
    },
    total=False,
)

SMSMfaSettingsTypeTypeDef = TypedDict(
    "SMSMfaSettingsTypeTypeDef", {"Enabled": bool, "PreferredMfa": bool}, total=False
)

SetRiskConfigurationResponseTypeDef = TypedDict(
    "SetRiskConfigurationResponseTypeDef", {"RiskConfiguration": RiskConfigurationTypeTypeDef}
)

SetUICustomizationResponseTypeDef = TypedDict(
    "SetUICustomizationResponseTypeDef", {"UICustomization": UICustomizationTypeTypeDef}
)

SetUserPoolMfaConfigResponseTypeDef = TypedDict(
    "SetUserPoolMfaConfigResponseTypeDef",
    {
        "SmsMfaConfiguration": SmsMfaConfigTypeTypeDef,
        "SoftwareTokenMfaConfiguration": SoftwareTokenMfaConfigTypeTypeDef,
        "MfaConfiguration": Literal["OFF", "ON", "OPTIONAL"],
    },
    total=False,
)

_RequiredSignUpResponseTypeDef = TypedDict(
    "_RequiredSignUpResponseTypeDef", {"UserConfirmed": bool, "UserSub": str}
)
_OptionalSignUpResponseTypeDef = TypedDict(
    "_OptionalSignUpResponseTypeDef",
    {"CodeDeliveryDetails": CodeDeliveryDetailsTypeTypeDef},
    total=False,
)


class SignUpResponseTypeDef(_RequiredSignUpResponseTypeDef, _OptionalSignUpResponseTypeDef):
    pass


SoftwareTokenMfaSettingsTypeTypeDef = TypedDict(
    "SoftwareTokenMfaSettingsTypeTypeDef", {"Enabled": bool, "PreferredMfa": bool}, total=False
)

StartUserImportJobResponseTypeDef = TypedDict(
    "StartUserImportJobResponseTypeDef", {"UserImportJob": UserImportJobTypeTypeDef}, total=False
)

StopUserImportJobResponseTypeDef = TypedDict(
    "StopUserImportJobResponseTypeDef", {"UserImportJob": UserImportJobTypeTypeDef}, total=False
)

UpdateGroupResponseTypeDef = TypedDict(
    "UpdateGroupResponseTypeDef", {"Group": GroupTypeTypeDef}, total=False
)

UpdateIdentityProviderResponseTypeDef = TypedDict(
    "UpdateIdentityProviderResponseTypeDef", {"IdentityProvider": IdentityProviderTypeTypeDef}
)

UpdateResourceServerResponseTypeDef = TypedDict(
    "UpdateResourceServerResponseTypeDef", {"ResourceServer": ResourceServerTypeTypeDef}
)

UpdateUserAttributesResponseTypeDef = TypedDict(
    "UpdateUserAttributesResponseTypeDef",
    {"CodeDeliveryDetailsList": List[CodeDeliveryDetailsTypeTypeDef]},
    total=False,
)

UpdateUserPoolClientResponseTypeDef = TypedDict(
    "UpdateUserPoolClientResponseTypeDef",
    {"UserPoolClient": UserPoolClientTypeTypeDef},
    total=False,
)

UpdateUserPoolDomainResponseTypeDef = TypedDict(
    "UpdateUserPoolDomainResponseTypeDef", {"CloudFrontDomain": str}, total=False
)

UserContextDataTypeTypeDef = TypedDict(
    "UserContextDataTypeTypeDef", {"EncodedData": str}, total=False
)

VerifySoftwareTokenResponseTypeDef = TypedDict(
    "VerifySoftwareTokenResponseTypeDef",
    {"Status": Literal["SUCCESS", "ERROR"], "Session": str},
    total=False,
)
