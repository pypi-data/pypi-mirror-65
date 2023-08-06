"""
Main interface for securityhub service type definitions.

Usage::

    from mypy_boto3.securityhub.type_defs import AccountDetailsTypeDef

    data: AccountDetailsTypeDef = {...}
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
    "AccountDetailsTypeDef",
    "DateRangeTypeDef",
    "DateFilterTypeDef",
    "IpFilterTypeDef",
    "KeywordFilterTypeDef",
    "MapFilterTypeDef",
    "NumberFilterTypeDef",
    "StringFilterTypeDef",
    "AwsSecurityFindingFiltersTypeDef",
    "ComplianceTypeDef",
    "MalwareTypeDef",
    "NetworkTypeDef",
    "NoteTypeDef",
    "ProcessDetailsTypeDef",
    "RelatedFindingTypeDef",
    "RecommendationTypeDef",
    "RemediationTypeDef",
    "AwsCloudFrontDistributionLoggingTypeDef",
    "AwsCloudFrontDistributionOriginItemTypeDef",
    "AwsCloudFrontDistributionOriginsTypeDef",
    "AwsCloudFrontDistributionDetailsTypeDef",
    "AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef",
    "AwsCodeBuildProjectEnvironmentTypeDef",
    "AwsCodeBuildProjectSourceTypeDef",
    "AwsCodeBuildProjectVpcConfigTypeDef",
    "AwsCodeBuildProjectDetailsTypeDef",
    "AwsEc2InstanceDetailsTypeDef",
    "AwsEc2NetworkInterfaceAttachmentTypeDef",
    "AwsEc2NetworkInterfaceSecurityGroupTypeDef",
    "AwsEc2NetworkInterfaceDetailsTypeDef",
    "AwsEc2SecurityGroupIpRangeTypeDef",
    "AwsEc2SecurityGroupIpv6RangeTypeDef",
    "AwsEc2SecurityGroupPrefixListIdTypeDef",
    "AwsEc2SecurityGroupUserIdGroupPairTypeDef",
    "AwsEc2SecurityGroupIpPermissionTypeDef",
    "AwsEc2SecurityGroupDetailsTypeDef",
    "AwsElasticsearchDomainDomainEndpointOptionsTypeDef",
    "AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef",
    "AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef",
    "AwsElasticsearchDomainVPCOptionsTypeDef",
    "AwsElasticsearchDomainDetailsTypeDef",
    "AvailabilityZoneTypeDef",
    "LoadBalancerStateTypeDef",
    "AwsElbv2LoadBalancerDetailsTypeDef",
    "AwsIamAccessKeyDetailsTypeDef",
    "AwsIamRoleDetailsTypeDef",
    "AwsKmsKeyDetailsTypeDef",
    "AwsLambdaFunctionCodeTypeDef",
    "AwsLambdaFunctionDeadLetterConfigTypeDef",
    "AwsLambdaFunctionEnvironmentErrorTypeDef",
    "AwsLambdaFunctionEnvironmentTypeDef",
    "AwsLambdaFunctionLayerTypeDef",
    "AwsLambdaFunctionTracingConfigTypeDef",
    "AwsLambdaFunctionVpcConfigTypeDef",
    "AwsLambdaFunctionDetailsTypeDef",
    "AwsLambdaLayerVersionDetailsTypeDef",
    "AwsRdsDbInstanceAssociatedRoleTypeDef",
    "AwsRdsDbInstanceEndpointTypeDef",
    "AwsRdsDbInstanceVpcSecurityGroupTypeDef",
    "AwsRdsDbInstanceDetailsTypeDef",
    "AwsS3BucketServerSideEncryptionByDefaultTypeDef",
    "AwsS3BucketServerSideEncryptionRuleTypeDef",
    "AwsS3BucketServerSideEncryptionConfigurationTypeDef",
    "AwsS3BucketDetailsTypeDef",
    "AwsS3ObjectDetailsTypeDef",
    "AwsSnsTopicSubscriptionTypeDef",
    "AwsSnsTopicDetailsTypeDef",
    "AwsSqsQueueDetailsTypeDef",
    "WafActionTypeDef",
    "WafExcludedRuleTypeDef",
    "WafOverrideActionTypeDef",
    "AwsWafWebAclRuleTypeDef",
    "AwsWafWebAclDetailsTypeDef",
    "ContainerDetailsTypeDef",
    "ResourceDetailsTypeDef",
    "ResourceTypeDef",
    "SeverityTypeDef",
    "ThreatIntelIndicatorTypeDef",
    "WorkflowTypeDef",
    "AwsSecurityFindingTypeDef",
    "StandardsSubscriptionTypeDef",
    "BatchDisableStandardsResponseTypeDef",
    "BatchEnableStandardsResponseTypeDef",
    "ImportFindingsErrorTypeDef",
    "BatchImportFindingsResponseTypeDef",
    "CreateActionTargetResponseTypeDef",
    "CreateInsightResponseTypeDef",
    "ResultTypeDef",
    "CreateMembersResponseTypeDef",
    "DeclineInvitationsResponseTypeDef",
    "DeleteActionTargetResponseTypeDef",
    "DeleteInsightResponseTypeDef",
    "DeleteInvitationsResponseTypeDef",
    "DeleteMembersResponseTypeDef",
    "ActionTargetTypeDef",
    "DescribeActionTargetsResponseTypeDef",
    "DescribeHubResponseTypeDef",
    "ProductTypeDef",
    "DescribeProductsResponseTypeDef",
    "StandardsControlTypeDef",
    "DescribeStandardsControlsResponseTypeDef",
    "StandardTypeDef",
    "DescribeStandardsResponseTypeDef",
    "EnableImportFindingsForProductResponseTypeDef",
    "GetEnabledStandardsResponseTypeDef",
    "GetFindingsResponseTypeDef",
    "InsightResultValueTypeDef",
    "InsightResultsTypeDef",
    "GetInsightResultsResponseTypeDef",
    "InsightTypeDef",
    "GetInsightsResponseTypeDef",
    "GetInvitationsCountResponseTypeDef",
    "InvitationTypeDef",
    "GetMasterAccountResponseTypeDef",
    "MemberTypeDef",
    "GetMembersResponseTypeDef",
    "InviteMembersResponseTypeDef",
    "ListEnabledProductsForImportResponseTypeDef",
    "ListInvitationsResponseTypeDef",
    "ListMembersResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NoteUpdateTypeDef",
    "PaginatorConfigTypeDef",
    "SortCriterionTypeDef",
    "StandardsSubscriptionRequestTypeDef",
)

AccountDetailsTypeDef = TypedDict(
    "AccountDetailsTypeDef", {"AccountId": str, "Email": str}, total=False
)

DateRangeTypeDef = TypedDict(
    "DateRangeTypeDef", {"Value": int, "Unit": Literal["DAYS"]}, total=False
)

DateFilterTypeDef = TypedDict(
    "DateFilterTypeDef", {"Start": str, "End": str, "DateRange": DateRangeTypeDef}, total=False
)

IpFilterTypeDef = TypedDict("IpFilterTypeDef", {"Cidr": str}, total=False)

KeywordFilterTypeDef = TypedDict("KeywordFilterTypeDef", {"Value": str}, total=False)

MapFilterTypeDef = TypedDict(
    "MapFilterTypeDef", {"Key": str, "Value": str, "Comparison": Literal["EQUALS"]}, total=False
)

NumberFilterTypeDef = TypedDict(
    "NumberFilterTypeDef", {"Gte": float, "Lte": float, "Eq": float}, total=False
)

StringFilterTypeDef = TypedDict(
    "StringFilterTypeDef", {"Value": str, "Comparison": Literal["EQUALS", "PREFIX"]}, total=False
)

AwsSecurityFindingFiltersTypeDef = TypedDict(
    "AwsSecurityFindingFiltersTypeDef",
    {
        "ProductArn": List[StringFilterTypeDef],
        "AwsAccountId": List[StringFilterTypeDef],
        "Id": List[StringFilterTypeDef],
        "GeneratorId": List[StringFilterTypeDef],
        "Type": List[StringFilterTypeDef],
        "FirstObservedAt": List[DateFilterTypeDef],
        "LastObservedAt": List[DateFilterTypeDef],
        "CreatedAt": List[DateFilterTypeDef],
        "UpdatedAt": List[DateFilterTypeDef],
        "SeverityProduct": List[NumberFilterTypeDef],
        "SeverityNormalized": List[NumberFilterTypeDef],
        "SeverityLabel": List[StringFilterTypeDef],
        "Confidence": List[NumberFilterTypeDef],
        "Criticality": List[NumberFilterTypeDef],
        "Title": List[StringFilterTypeDef],
        "Description": List[StringFilterTypeDef],
        "RecommendationText": List[StringFilterTypeDef],
        "SourceUrl": List[StringFilterTypeDef],
        "ProductFields": List[MapFilterTypeDef],
        "ProductName": List[StringFilterTypeDef],
        "CompanyName": List[StringFilterTypeDef],
        "UserDefinedFields": List[MapFilterTypeDef],
        "MalwareName": List[StringFilterTypeDef],
        "MalwareType": List[StringFilterTypeDef],
        "MalwarePath": List[StringFilterTypeDef],
        "MalwareState": List[StringFilterTypeDef],
        "NetworkDirection": List[StringFilterTypeDef],
        "NetworkProtocol": List[StringFilterTypeDef],
        "NetworkSourceIpV4": List[IpFilterTypeDef],
        "NetworkSourceIpV6": List[IpFilterTypeDef],
        "NetworkSourcePort": List[NumberFilterTypeDef],
        "NetworkSourceDomain": List[StringFilterTypeDef],
        "NetworkSourceMac": List[StringFilterTypeDef],
        "NetworkDestinationIpV4": List[IpFilterTypeDef],
        "NetworkDestinationIpV6": List[IpFilterTypeDef],
        "NetworkDestinationPort": List[NumberFilterTypeDef],
        "NetworkDestinationDomain": List[StringFilterTypeDef],
        "ProcessName": List[StringFilterTypeDef],
        "ProcessPath": List[StringFilterTypeDef],
        "ProcessPid": List[NumberFilterTypeDef],
        "ProcessParentPid": List[NumberFilterTypeDef],
        "ProcessLaunchedAt": List[DateFilterTypeDef],
        "ProcessTerminatedAt": List[DateFilterTypeDef],
        "ThreatIntelIndicatorType": List[StringFilterTypeDef],
        "ThreatIntelIndicatorValue": List[StringFilterTypeDef],
        "ThreatIntelIndicatorCategory": List[StringFilterTypeDef],
        "ThreatIntelIndicatorLastObservedAt": List[DateFilterTypeDef],
        "ThreatIntelIndicatorSource": List[StringFilterTypeDef],
        "ThreatIntelIndicatorSourceUrl": List[StringFilterTypeDef],
        "ResourceType": List[StringFilterTypeDef],
        "ResourceId": List[StringFilterTypeDef],
        "ResourcePartition": List[StringFilterTypeDef],
        "ResourceRegion": List[StringFilterTypeDef],
        "ResourceTags": List[MapFilterTypeDef],
        "ResourceAwsEc2InstanceType": List[StringFilterTypeDef],
        "ResourceAwsEc2InstanceImageId": List[StringFilterTypeDef],
        "ResourceAwsEc2InstanceIpV4Addresses": List[IpFilterTypeDef],
        "ResourceAwsEc2InstanceIpV6Addresses": List[IpFilterTypeDef],
        "ResourceAwsEc2InstanceKeyName": List[StringFilterTypeDef],
        "ResourceAwsEc2InstanceIamInstanceProfileArn": List[StringFilterTypeDef],
        "ResourceAwsEc2InstanceVpcId": List[StringFilterTypeDef],
        "ResourceAwsEc2InstanceSubnetId": List[StringFilterTypeDef],
        "ResourceAwsEc2InstanceLaunchedAt": List[DateFilterTypeDef],
        "ResourceAwsS3BucketOwnerId": List[StringFilterTypeDef],
        "ResourceAwsS3BucketOwnerName": List[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyUserName": List[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyStatus": List[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyCreatedAt": List[DateFilterTypeDef],
        "ResourceContainerName": List[StringFilterTypeDef],
        "ResourceContainerImageId": List[StringFilterTypeDef],
        "ResourceContainerImageName": List[StringFilterTypeDef],
        "ResourceContainerLaunchedAt": List[DateFilterTypeDef],
        "ResourceDetailsOther": List[MapFilterTypeDef],
        "ComplianceStatus": List[StringFilterTypeDef],
        "VerificationState": List[StringFilterTypeDef],
        "WorkflowState": List[StringFilterTypeDef],
        "WorkflowStatus": List[StringFilterTypeDef],
        "RecordState": List[StringFilterTypeDef],
        "RelatedFindingsProductArn": List[StringFilterTypeDef],
        "RelatedFindingsId": List[StringFilterTypeDef],
        "NoteText": List[StringFilterTypeDef],
        "NoteUpdatedAt": List[DateFilterTypeDef],
        "NoteUpdatedBy": List[StringFilterTypeDef],
        "Keyword": List[KeywordFilterTypeDef],
    },
    total=False,
)

ComplianceTypeDef = TypedDict(
    "ComplianceTypeDef",
    {
        "Status": Literal["PASSED", "WARNING", "FAILED", "NOT_AVAILABLE"],
        "RelatedRequirements": List[str],
    },
    total=False,
)

_RequiredMalwareTypeDef = TypedDict("_RequiredMalwareTypeDef", {"Name": str})
_OptionalMalwareTypeDef = TypedDict(
    "_OptionalMalwareTypeDef",
    {
        "Type": Literal[
            "ADWARE",
            "BLENDED_THREAT",
            "BOTNET_AGENT",
            "COIN_MINER",
            "EXPLOIT_KIT",
            "KEYLOGGER",
            "MACRO",
            "POTENTIALLY_UNWANTED",
            "SPYWARE",
            "RANSOMWARE",
            "REMOTE_ACCESS",
            "ROOTKIT",
            "TROJAN",
            "VIRUS",
            "WORM",
        ],
        "Path": str,
        "State": Literal["OBSERVED", "REMOVAL_FAILED", "REMOVED"],
    },
    total=False,
)


class MalwareTypeDef(_RequiredMalwareTypeDef, _OptionalMalwareTypeDef):
    pass


NetworkTypeDef = TypedDict(
    "NetworkTypeDef",
    {
        "Direction": Literal["IN", "OUT"],
        "Protocol": str,
        "SourceIpV4": str,
        "SourceIpV6": str,
        "SourcePort": int,
        "SourceDomain": str,
        "SourceMac": str,
        "DestinationIpV4": str,
        "DestinationIpV6": str,
        "DestinationPort": int,
        "DestinationDomain": str,
    },
    total=False,
)

NoteTypeDef = TypedDict("NoteTypeDef", {"Text": str, "UpdatedBy": str, "UpdatedAt": str})

ProcessDetailsTypeDef = TypedDict(
    "ProcessDetailsTypeDef",
    {
        "Name": str,
        "Path": str,
        "Pid": int,
        "ParentPid": int,
        "LaunchedAt": str,
        "TerminatedAt": str,
    },
    total=False,
)

RelatedFindingTypeDef = TypedDict("RelatedFindingTypeDef", {"ProductArn": str, "Id": str})

RecommendationTypeDef = TypedDict("RecommendationTypeDef", {"Text": str, "Url": str}, total=False)

RemediationTypeDef = TypedDict(
    "RemediationTypeDef", {"Recommendation": RecommendationTypeDef}, total=False
)

AwsCloudFrontDistributionLoggingTypeDef = TypedDict(
    "AwsCloudFrontDistributionLoggingTypeDef",
    {"Bucket": str, "Enabled": bool, "IncludeCookies": bool, "Prefix": str},
    total=False,
)

AwsCloudFrontDistributionOriginItemTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginItemTypeDef",
    {"DomainName": str, "Id": str, "OriginPath": str},
    total=False,
)

AwsCloudFrontDistributionOriginsTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginsTypeDef",
    {"Items": List[AwsCloudFrontDistributionOriginItemTypeDef]},
    total=False,
)

AwsCloudFrontDistributionDetailsTypeDef = TypedDict(
    "AwsCloudFrontDistributionDetailsTypeDef",
    {
        "DomainName": str,
        "ETag": str,
        "LastModifiedTime": str,
        "Logging": AwsCloudFrontDistributionLoggingTypeDef,
        "Origins": AwsCloudFrontDistributionOriginsTypeDef,
        "Status": str,
        "WebAclId": str,
    },
    total=False,
)

AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef = TypedDict(
    "AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef",
    {"Credential": str, "CredentialProvider": str},
    total=False,
)

AwsCodeBuildProjectEnvironmentTypeDef = TypedDict(
    "AwsCodeBuildProjectEnvironmentTypeDef",
    {
        "Certificate": str,
        "ImagePullCredentialsType": str,
        "RegistryCredential": AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef,
        "Type": str,
    },
    total=False,
)

AwsCodeBuildProjectSourceTypeDef = TypedDict(
    "AwsCodeBuildProjectSourceTypeDef",
    {"Type": str, "Location": str, "GitCloneDepth": int, "InsecureSsl": bool},
    total=False,
)

AwsCodeBuildProjectVpcConfigTypeDef = TypedDict(
    "AwsCodeBuildProjectVpcConfigTypeDef",
    {"VpcId": str, "Subnets": List[str], "SecurityGroupIds": List[str]},
    total=False,
)

AwsCodeBuildProjectDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectDetailsTypeDef",
    {
        "EncryptionKey": str,
        "Environment": AwsCodeBuildProjectEnvironmentTypeDef,
        "Name": str,
        "Source": AwsCodeBuildProjectSourceTypeDef,
        "ServiceRole": str,
        "VpcConfig": AwsCodeBuildProjectVpcConfigTypeDef,
    },
    total=False,
)

AwsEc2InstanceDetailsTypeDef = TypedDict(
    "AwsEc2InstanceDetailsTypeDef",
    {
        "Type": str,
        "ImageId": str,
        "IpV4Addresses": List[str],
        "IpV6Addresses": List[str],
        "KeyName": str,
        "IamInstanceProfileArn": str,
        "VpcId": str,
        "SubnetId": str,
        "LaunchedAt": str,
    },
    total=False,
)

AwsEc2NetworkInterfaceAttachmentTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceAttachmentTypeDef",
    {
        "AttachTime": str,
        "AttachmentId": str,
        "DeleteOnTermination": bool,
        "DeviceIndex": int,
        "InstanceId": str,
        "InstanceOwnerId": str,
        "Status": str,
    },
    total=False,
)

AwsEc2NetworkInterfaceSecurityGroupTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceSecurityGroupTypeDef", {"GroupName": str, "GroupId": str}, total=False
)

AwsEc2NetworkInterfaceDetailsTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceDetailsTypeDef",
    {
        "Attachment": AwsEc2NetworkInterfaceAttachmentTypeDef,
        "NetworkInterfaceId": str,
        "SecurityGroups": List[AwsEc2NetworkInterfaceSecurityGroupTypeDef],
        "SourceDestCheck": bool,
    },
    total=False,
)

AwsEc2SecurityGroupIpRangeTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpRangeTypeDef", {"CidrIp": str}, total=False
)

AwsEc2SecurityGroupIpv6RangeTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpv6RangeTypeDef", {"CidrIpv6": str}, total=False
)

AwsEc2SecurityGroupPrefixListIdTypeDef = TypedDict(
    "AwsEc2SecurityGroupPrefixListIdTypeDef", {"PrefixListId": str}, total=False
)

AwsEc2SecurityGroupUserIdGroupPairTypeDef = TypedDict(
    "AwsEc2SecurityGroupUserIdGroupPairTypeDef",
    {
        "GroupId": str,
        "GroupName": str,
        "PeeringStatus": str,
        "UserId": str,
        "VpcId": str,
        "VpcPeeringConnectionId": str,
    },
    total=False,
)

AwsEc2SecurityGroupIpPermissionTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpPermissionTypeDef",
    {
        "IpProtocol": str,
        "FromPort": int,
        "ToPort": int,
        "UserIdGroupPairs": List[AwsEc2SecurityGroupUserIdGroupPairTypeDef],
        "IpRanges": List[AwsEc2SecurityGroupIpRangeTypeDef],
        "Ipv6Ranges": List[AwsEc2SecurityGroupIpv6RangeTypeDef],
        "PrefixListIds": List[AwsEc2SecurityGroupPrefixListIdTypeDef],
    },
    total=False,
)

AwsEc2SecurityGroupDetailsTypeDef = TypedDict(
    "AwsEc2SecurityGroupDetailsTypeDef",
    {
        "GroupName": str,
        "GroupId": str,
        "OwnerId": str,
        "VpcId": str,
        "IpPermissions": List[AwsEc2SecurityGroupIpPermissionTypeDef],
        "IpPermissionsEgress": List[AwsEc2SecurityGroupIpPermissionTypeDef],
    },
    total=False,
)

AwsElasticsearchDomainDomainEndpointOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainDomainEndpointOptionsTypeDef",
    {"EnforceHTTPS": bool, "TLSSecurityPolicy": str},
    total=False,
)

AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef",
    {"Enabled": bool, "KmsKeyId": str},
    total=False,
)

AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef", {"Enabled": bool}, total=False
)

AwsElasticsearchDomainVPCOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainVPCOptionsTypeDef",
    {
        "AvailabilityZones": List[str],
        "SecurityGroupIds": List[str],
        "SubnetIds": List[str],
        "VPCId": str,
    },
    total=False,
)

AwsElasticsearchDomainDetailsTypeDef = TypedDict(
    "AwsElasticsearchDomainDetailsTypeDef",
    {
        "AccessPolicies": str,
        "DomainEndpointOptions": AwsElasticsearchDomainDomainEndpointOptionsTypeDef,
        "DomainId": str,
        "DomainName": str,
        "Endpoint": str,
        "Endpoints": Dict[str, str],
        "ElasticsearchVersion": str,
        "EncryptionAtRestOptions": AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef,
        "NodeToNodeEncryptionOptions": AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef,
        "VPCOptions": AwsElasticsearchDomainVPCOptionsTypeDef,
    },
    total=False,
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef", {"ZoneName": str, "SubnetId": str}, total=False
)

LoadBalancerStateTypeDef = TypedDict(
    "LoadBalancerStateTypeDef", {"Code": str, "Reason": str}, total=False
)

AwsElbv2LoadBalancerDetailsTypeDef = TypedDict(
    "AwsElbv2LoadBalancerDetailsTypeDef",
    {
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "CanonicalHostedZoneId": str,
        "CreatedTime": str,
        "DNSName": str,
        "IpAddressType": str,
        "Scheme": str,
        "SecurityGroups": List[str],
        "State": LoadBalancerStateTypeDef,
        "Type": str,
        "VpcId": str,
    },
    total=False,
)

AwsIamAccessKeyDetailsTypeDef = TypedDict(
    "AwsIamAccessKeyDetailsTypeDef",
    {
        "UserName": str,
        "Status": Literal["Active", "Inactive"],
        "CreatedAt": str,
        "PrincipalId": str,
        "PrincipalType": str,
        "PrincipalName": str,
    },
    total=False,
)

AwsIamRoleDetailsTypeDef = TypedDict(
    "AwsIamRoleDetailsTypeDef",
    {
        "AssumeRolePolicyDocument": str,
        "CreateDate": str,
        "RoleId": str,
        "RoleName": str,
        "MaxSessionDuration": int,
        "Path": str,
    },
    total=False,
)

AwsKmsKeyDetailsTypeDef = TypedDict(
    "AwsKmsKeyDetailsTypeDef",
    {
        "AWSAccountId": str,
        "CreationDate": float,
        "KeyId": str,
        "KeyManager": str,
        "KeyState": str,
        "Origin": str,
    },
    total=False,
)

AwsLambdaFunctionCodeTypeDef = TypedDict(
    "AwsLambdaFunctionCodeTypeDef",
    {"S3Bucket": str, "S3Key": str, "S3ObjectVersion": str, "ZipFile": str},
    total=False,
)

AwsLambdaFunctionDeadLetterConfigTypeDef = TypedDict(
    "AwsLambdaFunctionDeadLetterConfigTypeDef", {"TargetArn": str}, total=False
)

AwsLambdaFunctionEnvironmentErrorTypeDef = TypedDict(
    "AwsLambdaFunctionEnvironmentErrorTypeDef", {"ErrorCode": str, "Message": str}, total=False
)

AwsLambdaFunctionEnvironmentTypeDef = TypedDict(
    "AwsLambdaFunctionEnvironmentTypeDef",
    {"Variables": Dict[str, str], "Error": AwsLambdaFunctionEnvironmentErrorTypeDef},
    total=False,
)

AwsLambdaFunctionLayerTypeDef = TypedDict(
    "AwsLambdaFunctionLayerTypeDef", {"Arn": str, "CodeSize": int}, total=False
)

AwsLambdaFunctionTracingConfigTypeDef = TypedDict(
    "AwsLambdaFunctionTracingConfigTypeDef", {"Mode": str}, total=False
)

AwsLambdaFunctionVpcConfigTypeDef = TypedDict(
    "AwsLambdaFunctionVpcConfigTypeDef",
    {"SecurityGroupIds": List[str], "SubnetIds": List[str], "VpcId": str},
    total=False,
)

AwsLambdaFunctionDetailsTypeDef = TypedDict(
    "AwsLambdaFunctionDetailsTypeDef",
    {
        "Code": AwsLambdaFunctionCodeTypeDef,
        "CodeSha256": str,
        "DeadLetterConfig": AwsLambdaFunctionDeadLetterConfigTypeDef,
        "Environment": AwsLambdaFunctionEnvironmentTypeDef,
        "FunctionName": str,
        "Handler": str,
        "KmsKeyArn": str,
        "LastModified": str,
        "Layers": List[AwsLambdaFunctionLayerTypeDef],
        "MasterArn": str,
        "MemorySize": int,
        "RevisionId": str,
        "Role": str,
        "Runtime": str,
        "Timeout": int,
        "TracingConfig": AwsLambdaFunctionTracingConfigTypeDef,
        "VpcConfig": AwsLambdaFunctionVpcConfigTypeDef,
        "Version": str,
    },
    total=False,
)

AwsLambdaLayerVersionDetailsTypeDef = TypedDict(
    "AwsLambdaLayerVersionDetailsTypeDef",
    {"Version": int, "CompatibleRuntimes": List[str], "CreatedDate": str},
    total=False,
)

AwsRdsDbInstanceAssociatedRoleTypeDef = TypedDict(
    "AwsRdsDbInstanceAssociatedRoleTypeDef",
    {"RoleArn": str, "FeatureName": str, "Status": str},
    total=False,
)

AwsRdsDbInstanceEndpointTypeDef = TypedDict(
    "AwsRdsDbInstanceEndpointTypeDef",
    {"Address": str, "Port": int, "HostedZoneId": str},
    total=False,
)

AwsRdsDbInstanceVpcSecurityGroupTypeDef = TypedDict(
    "AwsRdsDbInstanceVpcSecurityGroupTypeDef",
    {"VpcSecurityGroupId": str, "Status": str},
    total=False,
)

AwsRdsDbInstanceDetailsTypeDef = TypedDict(
    "AwsRdsDbInstanceDetailsTypeDef",
    {
        "AssociatedRoles": List[AwsRdsDbInstanceAssociatedRoleTypeDef],
        "CACertificateIdentifier": str,
        "DBClusterIdentifier": str,
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "DbInstancePort": int,
        "DbiResourceId": str,
        "DBName": str,
        "DeletionProtection": bool,
        "Endpoint": AwsRdsDbInstanceEndpointTypeDef,
        "Engine": str,
        "EngineVersion": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "InstanceCreateTime": str,
        "KmsKeyId": str,
        "PubliclyAccessible": bool,
        "StorageEncrypted": bool,
        "TdeCredentialArn": str,
        "VpcSecurityGroups": List[AwsRdsDbInstanceVpcSecurityGroupTypeDef],
    },
    total=False,
)

AwsS3BucketServerSideEncryptionByDefaultTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionByDefaultTypeDef",
    {"SSEAlgorithm": str, "KMSMasterKeyID": str},
    total=False,
)

AwsS3BucketServerSideEncryptionRuleTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionRuleTypeDef",
    {"ApplyServerSideEncryptionByDefault": AwsS3BucketServerSideEncryptionByDefaultTypeDef},
    total=False,
)

AwsS3BucketServerSideEncryptionConfigurationTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionConfigurationTypeDef",
    {"Rules": List[AwsS3BucketServerSideEncryptionRuleTypeDef]},
    total=False,
)

AwsS3BucketDetailsTypeDef = TypedDict(
    "AwsS3BucketDetailsTypeDef",
    {
        "OwnerId": str,
        "OwnerName": str,
        "CreatedAt": str,
        "ServerSideEncryptionConfiguration": AwsS3BucketServerSideEncryptionConfigurationTypeDef,
    },
    total=False,
)

AwsS3ObjectDetailsTypeDef = TypedDict(
    "AwsS3ObjectDetailsTypeDef",
    {
        "LastModified": str,
        "ETag": str,
        "VersionId": str,
        "ContentType": str,
        "ServerSideEncryption": str,
        "SSEKMSKeyId": str,
    },
    total=False,
)

AwsSnsTopicSubscriptionTypeDef = TypedDict(
    "AwsSnsTopicSubscriptionTypeDef", {"Endpoint": str, "Protocol": str}, total=False
)

AwsSnsTopicDetailsTypeDef = TypedDict(
    "AwsSnsTopicDetailsTypeDef",
    {
        "KmsMasterKeyId": str,
        "Subscription": List[AwsSnsTopicSubscriptionTypeDef],
        "TopicName": str,
        "Owner": str,
    },
    total=False,
)

AwsSqsQueueDetailsTypeDef = TypedDict(
    "AwsSqsQueueDetailsTypeDef",
    {
        "KmsDataKeyReusePeriodSeconds": int,
        "KmsMasterKeyId": str,
        "QueueName": str,
        "DeadLetterTargetArn": str,
    },
    total=False,
)

WafActionTypeDef = TypedDict("WafActionTypeDef", {"Type": str}, total=False)

WafExcludedRuleTypeDef = TypedDict("WafExcludedRuleTypeDef", {"RuleId": str}, total=False)

WafOverrideActionTypeDef = TypedDict("WafOverrideActionTypeDef", {"Type": str}, total=False)

AwsWafWebAclRuleTypeDef = TypedDict(
    "AwsWafWebAclRuleTypeDef",
    {
        "Action": WafActionTypeDef,
        "ExcludedRules": List[WafExcludedRuleTypeDef],
        "OverrideAction": WafOverrideActionTypeDef,
        "Priority": int,
        "RuleId": str,
        "Type": str,
    },
    total=False,
)

AwsWafWebAclDetailsTypeDef = TypedDict(
    "AwsWafWebAclDetailsTypeDef",
    {"Name": str, "DefaultAction": str, "Rules": List[AwsWafWebAclRuleTypeDef], "WebAclId": str},
    total=False,
)

ContainerDetailsTypeDef = TypedDict(
    "ContainerDetailsTypeDef",
    {"Name": str, "ImageId": str, "ImageName": str, "LaunchedAt": str},
    total=False,
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "AwsCodeBuildProject": AwsCodeBuildProjectDetailsTypeDef,
        "AwsCloudFrontDistribution": AwsCloudFrontDistributionDetailsTypeDef,
        "AwsEc2Instance": AwsEc2InstanceDetailsTypeDef,
        "AwsEc2NetworkInterface": AwsEc2NetworkInterfaceDetailsTypeDef,
        "AwsEc2SecurityGroup": AwsEc2SecurityGroupDetailsTypeDef,
        "AwsElbv2LoadBalancer": AwsElbv2LoadBalancerDetailsTypeDef,
        "AwsElasticsearchDomain": AwsElasticsearchDomainDetailsTypeDef,
        "AwsS3Bucket": AwsS3BucketDetailsTypeDef,
        "AwsS3Object": AwsS3ObjectDetailsTypeDef,
        "AwsIamAccessKey": AwsIamAccessKeyDetailsTypeDef,
        "AwsIamRole": AwsIamRoleDetailsTypeDef,
        "AwsKmsKey": AwsKmsKeyDetailsTypeDef,
        "AwsLambdaFunction": AwsLambdaFunctionDetailsTypeDef,
        "AwsLambdaLayerVersion": AwsLambdaLayerVersionDetailsTypeDef,
        "AwsRdsDbInstance": AwsRdsDbInstanceDetailsTypeDef,
        "AwsSnsTopic": AwsSnsTopicDetailsTypeDef,
        "AwsSqsQueue": AwsSqsQueueDetailsTypeDef,
        "AwsWafWebAcl": AwsWafWebAclDetailsTypeDef,
        "Container": ContainerDetailsTypeDef,
        "Other": Dict[str, str],
    },
    total=False,
)

_RequiredResourceTypeDef = TypedDict("_RequiredResourceTypeDef", {"Type": str, "Id": str})
_OptionalResourceTypeDef = TypedDict(
    "_OptionalResourceTypeDef",
    {
        "Partition": Literal["aws", "aws-cn", "aws-us-gov"],
        "Region": str,
        "Tags": Dict[str, str],
        "Details": ResourceDetailsTypeDef,
    },
    total=False,
)


class ResourceTypeDef(_RequiredResourceTypeDef, _OptionalResourceTypeDef):
    pass


SeverityTypeDef = TypedDict(
    "SeverityTypeDef",
    {
        "Product": float,
        "Label": Literal["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
        "Normalized": int,
    },
    total=False,
)

ThreatIntelIndicatorTypeDef = TypedDict(
    "ThreatIntelIndicatorTypeDef",
    {
        "Type": Literal[
            "DOMAIN",
            "EMAIL_ADDRESS",
            "HASH_MD5",
            "HASH_SHA1",
            "HASH_SHA256",
            "HASH_SHA512",
            "IPV4_ADDRESS",
            "IPV6_ADDRESS",
            "MUTEX",
            "PROCESS",
            "URL",
        ],
        "Value": str,
        "Category": Literal[
            "BACKDOOR",
            "CARD_STEALER",
            "COMMAND_AND_CONTROL",
            "DROP_SITE",
            "EXPLOIT_SITE",
            "KEYLOGGER",
        ],
        "LastObservedAt": str,
        "Source": str,
        "SourceUrl": str,
    },
    total=False,
)

WorkflowTypeDef = TypedDict(
    "WorkflowTypeDef", {"Status": Literal["NEW", "NOTIFIED", "RESOLVED", "SUPPRESSED"]}, total=False
)

_RequiredAwsSecurityFindingTypeDef = TypedDict(
    "_RequiredAwsSecurityFindingTypeDef",
    {
        "SchemaVersion": str,
        "Id": str,
        "ProductArn": str,
        "GeneratorId": str,
        "AwsAccountId": str,
        "Types": List[str],
        "CreatedAt": str,
        "UpdatedAt": str,
        "Severity": SeverityTypeDef,
        "Title": str,
        "Description": str,
        "Resources": List[ResourceTypeDef],
    },
)
_OptionalAwsSecurityFindingTypeDef = TypedDict(
    "_OptionalAwsSecurityFindingTypeDef",
    {
        "FirstObservedAt": str,
        "LastObservedAt": str,
        "Confidence": int,
        "Criticality": int,
        "Remediation": RemediationTypeDef,
        "SourceUrl": str,
        "ProductFields": Dict[str, str],
        "UserDefinedFields": Dict[str, str],
        "Malware": List[MalwareTypeDef],
        "Network": NetworkTypeDef,
        "Process": ProcessDetailsTypeDef,
        "ThreatIntelIndicators": List[ThreatIntelIndicatorTypeDef],
        "Compliance": ComplianceTypeDef,
        "VerificationState": Literal[
            "UNKNOWN", "TRUE_POSITIVE", "FALSE_POSITIVE", "BENIGN_POSITIVE"
        ],
        "WorkflowState": Literal["NEW", "ASSIGNED", "IN_PROGRESS", "DEFERRED", "RESOLVED"],
        "Workflow": WorkflowTypeDef,
        "RecordState": Literal["ACTIVE", "ARCHIVED"],
        "RelatedFindings": List[RelatedFindingTypeDef],
        "Note": NoteTypeDef,
    },
    total=False,
)


class AwsSecurityFindingTypeDef(
    _RequiredAwsSecurityFindingTypeDef, _OptionalAwsSecurityFindingTypeDef
):
    pass


StandardsSubscriptionTypeDef = TypedDict(
    "StandardsSubscriptionTypeDef",
    {
        "StandardsSubscriptionArn": str,
        "StandardsArn": str,
        "StandardsInput": Dict[str, str],
        "StandardsStatus": Literal["PENDING", "READY", "FAILED", "DELETING", "INCOMPLETE"],
    },
)

BatchDisableStandardsResponseTypeDef = TypedDict(
    "BatchDisableStandardsResponseTypeDef",
    {"StandardsSubscriptions": List[StandardsSubscriptionTypeDef]},
    total=False,
)

BatchEnableStandardsResponseTypeDef = TypedDict(
    "BatchEnableStandardsResponseTypeDef",
    {"StandardsSubscriptions": List[StandardsSubscriptionTypeDef]},
    total=False,
)

ImportFindingsErrorTypeDef = TypedDict(
    "ImportFindingsErrorTypeDef", {"Id": str, "ErrorCode": str, "ErrorMessage": str}
)

_RequiredBatchImportFindingsResponseTypeDef = TypedDict(
    "_RequiredBatchImportFindingsResponseTypeDef", {"FailedCount": int, "SuccessCount": int}
)
_OptionalBatchImportFindingsResponseTypeDef = TypedDict(
    "_OptionalBatchImportFindingsResponseTypeDef",
    {"FailedFindings": List[ImportFindingsErrorTypeDef]},
    total=False,
)


class BatchImportFindingsResponseTypeDef(
    _RequiredBatchImportFindingsResponseTypeDef, _OptionalBatchImportFindingsResponseTypeDef
):
    pass


CreateActionTargetResponseTypeDef = TypedDict(
    "CreateActionTargetResponseTypeDef", {"ActionTargetArn": str}
)

CreateInsightResponseTypeDef = TypedDict("CreateInsightResponseTypeDef", {"InsightArn": str})

ResultTypeDef = TypedDict("ResultTypeDef", {"AccountId": str, "ProcessingResult": str}, total=False)

CreateMembersResponseTypeDef = TypedDict(
    "CreateMembersResponseTypeDef", {"UnprocessedAccounts": List[ResultTypeDef]}, total=False
)

DeclineInvitationsResponseTypeDef = TypedDict(
    "DeclineInvitationsResponseTypeDef", {"UnprocessedAccounts": List[ResultTypeDef]}, total=False
)

DeleteActionTargetResponseTypeDef = TypedDict(
    "DeleteActionTargetResponseTypeDef", {"ActionTargetArn": str}
)

DeleteInsightResponseTypeDef = TypedDict("DeleteInsightResponseTypeDef", {"InsightArn": str})

DeleteInvitationsResponseTypeDef = TypedDict(
    "DeleteInvitationsResponseTypeDef", {"UnprocessedAccounts": List[ResultTypeDef]}, total=False
)

DeleteMembersResponseTypeDef = TypedDict(
    "DeleteMembersResponseTypeDef", {"UnprocessedAccounts": List[ResultTypeDef]}, total=False
)

ActionTargetTypeDef = TypedDict(
    "ActionTargetTypeDef", {"ActionTargetArn": str, "Name": str, "Description": str}
)

_RequiredDescribeActionTargetsResponseTypeDef = TypedDict(
    "_RequiredDescribeActionTargetsResponseTypeDef", {"ActionTargets": List[ActionTargetTypeDef]}
)
_OptionalDescribeActionTargetsResponseTypeDef = TypedDict(
    "_OptionalDescribeActionTargetsResponseTypeDef", {"NextToken": str}, total=False
)


class DescribeActionTargetsResponseTypeDef(
    _RequiredDescribeActionTargetsResponseTypeDef, _OptionalDescribeActionTargetsResponseTypeDef
):
    pass


DescribeHubResponseTypeDef = TypedDict(
    "DescribeHubResponseTypeDef", {"HubArn": str, "SubscribedAt": str}, total=False
)

_RequiredProductTypeDef = TypedDict("_RequiredProductTypeDef", {"ProductArn": str})
_OptionalProductTypeDef = TypedDict(
    "_OptionalProductTypeDef",
    {
        "ProductName": str,
        "CompanyName": str,
        "Description": str,
        "Categories": List[str],
        "IntegrationTypes": List[
            Literal["SEND_FINDINGS_TO_SECURITY_HUB", "RECEIVE_FINDINGS_FROM_SECURITY_HUB"]
        ],
        "MarketplaceUrl": str,
        "ActivationUrl": str,
        "ProductSubscriptionResourcePolicy": str,
    },
    total=False,
)


class ProductTypeDef(_RequiredProductTypeDef, _OptionalProductTypeDef):
    pass


_RequiredDescribeProductsResponseTypeDef = TypedDict(
    "_RequiredDescribeProductsResponseTypeDef", {"Products": List[ProductTypeDef]}
)
_OptionalDescribeProductsResponseTypeDef = TypedDict(
    "_OptionalDescribeProductsResponseTypeDef", {"NextToken": str}, total=False
)


class DescribeProductsResponseTypeDef(
    _RequiredDescribeProductsResponseTypeDef, _OptionalDescribeProductsResponseTypeDef
):
    pass


StandardsControlTypeDef = TypedDict(
    "StandardsControlTypeDef",
    {
        "StandardsControlArn": str,
        "ControlStatus": Literal["ENABLED", "DISABLED"],
        "DisabledReason": str,
        "ControlStatusUpdatedAt": datetime,
        "ControlId": str,
        "Title": str,
        "Description": str,
        "RemediationUrl": str,
        "SeverityRating": Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        "RelatedRequirements": List[str],
    },
    total=False,
)

DescribeStandardsControlsResponseTypeDef = TypedDict(
    "DescribeStandardsControlsResponseTypeDef",
    {"Controls": List[StandardsControlTypeDef], "NextToken": str},
    total=False,
)

StandardTypeDef = TypedDict(
    "StandardTypeDef",
    {"StandardsArn": str, "Name": str, "Description": str, "EnabledByDefault": bool},
    total=False,
)

DescribeStandardsResponseTypeDef = TypedDict(
    "DescribeStandardsResponseTypeDef",
    {"Standards": List[StandardTypeDef], "NextToken": str},
    total=False,
)

EnableImportFindingsForProductResponseTypeDef = TypedDict(
    "EnableImportFindingsForProductResponseTypeDef", {"ProductSubscriptionArn": str}, total=False
)

GetEnabledStandardsResponseTypeDef = TypedDict(
    "GetEnabledStandardsResponseTypeDef",
    {"StandardsSubscriptions": List[StandardsSubscriptionTypeDef], "NextToken": str},
    total=False,
)

_RequiredGetFindingsResponseTypeDef = TypedDict(
    "_RequiredGetFindingsResponseTypeDef", {"Findings": List[AwsSecurityFindingTypeDef]}
)
_OptionalGetFindingsResponseTypeDef = TypedDict(
    "_OptionalGetFindingsResponseTypeDef", {"NextToken": str}, total=False
)


class GetFindingsResponseTypeDef(
    _RequiredGetFindingsResponseTypeDef, _OptionalGetFindingsResponseTypeDef
):
    pass


InsightResultValueTypeDef = TypedDict(
    "InsightResultValueTypeDef", {"GroupByAttributeValue": str, "Count": int}
)

InsightResultsTypeDef = TypedDict(
    "InsightResultsTypeDef",
    {"InsightArn": str, "GroupByAttribute": str, "ResultValues": List[InsightResultValueTypeDef]},
)

GetInsightResultsResponseTypeDef = TypedDict(
    "GetInsightResultsResponseTypeDef", {"InsightResults": InsightResultsTypeDef}
)

InsightTypeDef = TypedDict(
    "InsightTypeDef",
    {
        "InsightArn": str,
        "Name": str,
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "GroupByAttribute": str,
    },
)

_RequiredGetInsightsResponseTypeDef = TypedDict(
    "_RequiredGetInsightsResponseTypeDef", {"Insights": List[InsightTypeDef]}
)
_OptionalGetInsightsResponseTypeDef = TypedDict(
    "_OptionalGetInsightsResponseTypeDef", {"NextToken": str}, total=False
)


class GetInsightsResponseTypeDef(
    _RequiredGetInsightsResponseTypeDef, _OptionalGetInsightsResponseTypeDef
):
    pass


GetInvitationsCountResponseTypeDef = TypedDict(
    "GetInvitationsCountResponseTypeDef", {"InvitationsCount": int}, total=False
)

InvitationTypeDef = TypedDict(
    "InvitationTypeDef",
    {"AccountId": str, "InvitationId": str, "InvitedAt": datetime, "MemberStatus": str},
    total=False,
)

GetMasterAccountResponseTypeDef = TypedDict(
    "GetMasterAccountResponseTypeDef", {"Master": InvitationTypeDef}, total=False
)

MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "AccountId": str,
        "Email": str,
        "MasterId": str,
        "MemberStatus": str,
        "InvitedAt": datetime,
        "UpdatedAt": datetime,
    },
    total=False,
)

GetMembersResponseTypeDef = TypedDict(
    "GetMembersResponseTypeDef",
    {"Members": List[MemberTypeDef], "UnprocessedAccounts": List[ResultTypeDef]},
    total=False,
)

InviteMembersResponseTypeDef = TypedDict(
    "InviteMembersResponseTypeDef", {"UnprocessedAccounts": List[ResultTypeDef]}, total=False
)

ListEnabledProductsForImportResponseTypeDef = TypedDict(
    "ListEnabledProductsForImportResponseTypeDef",
    {"ProductSubscriptions": List[str], "NextToken": str},
    total=False,
)

ListInvitationsResponseTypeDef = TypedDict(
    "ListInvitationsResponseTypeDef",
    {"Invitations": List[InvitationTypeDef], "NextToken": str},
    total=False,
)

ListMembersResponseTypeDef = TypedDict(
    "ListMembersResponseTypeDef", {"Members": List[MemberTypeDef], "NextToken": str}, total=False
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

NoteUpdateTypeDef = TypedDict("NoteUpdateTypeDef", {"Text": str, "UpdatedBy": str})

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

SortCriterionTypeDef = TypedDict(
    "SortCriterionTypeDef", {"Field": str, "SortOrder": Literal["asc", "desc"]}, total=False
)

_RequiredStandardsSubscriptionRequestTypeDef = TypedDict(
    "_RequiredStandardsSubscriptionRequestTypeDef", {"StandardsArn": str}
)
_OptionalStandardsSubscriptionRequestTypeDef = TypedDict(
    "_OptionalStandardsSubscriptionRequestTypeDef", {"StandardsInput": Dict[str, str]}, total=False
)


class StandardsSubscriptionRequestTypeDef(
    _RequiredStandardsSubscriptionRequestTypeDef, _OptionalStandardsSubscriptionRequestTypeDef
):
    pass
