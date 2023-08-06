"""
Main interface for s3control service type definitions.

Usage::

    from mypy_boto3.s3control.type_defs import CreateJobResultTypeDef

    data: CreateJobResultTypeDef = {...}
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
    "CreateJobResultTypeDef",
    "JobFailureTypeDef",
    "JobManifestLocationTypeDef",
    "JobManifestSpecTypeDef",
    "JobManifestTypeDef",
    "LambdaInvokeOperationTypeDef",
    "S3GranteeTypeDef",
    "S3GrantTypeDef",
    "S3ObjectMetadataTypeDef",
    "S3TagTypeDef",
    "S3CopyObjectOperationTypeDef",
    "S3InitiateRestoreObjectOperationTypeDef",
    "S3ObjectOwnerTypeDef",
    "S3AccessControlListTypeDef",
    "S3AccessControlPolicyTypeDef",
    "S3SetObjectAclOperationTypeDef",
    "S3SetObjectTaggingOperationTypeDef",
    "JobOperationTypeDef",
    "JobProgressSummaryTypeDef",
    "JobReportTypeDef",
    "JobDescriptorTypeDef",
    "DescribeJobResultTypeDef",
    "GetAccessPointPolicyResultTypeDef",
    "PolicyStatusTypeDef",
    "GetAccessPointPolicyStatusResultTypeDef",
    "PublicAccessBlockConfigurationTypeDef",
    "VpcConfigurationTypeDef",
    "GetAccessPointResultTypeDef",
    "GetJobTaggingResultTypeDef",
    "GetPublicAccessBlockOutputTypeDef",
    "AccessPointTypeDef",
    "ListAccessPointsResultTypeDef",
    "JobListDescriptorTypeDef",
    "ListJobsResultTypeDef",
    "UpdateJobPriorityResultTypeDef",
    "UpdateJobStatusResultTypeDef",
)

CreateJobResultTypeDef = TypedDict("CreateJobResultTypeDef", {"JobId": str}, total=False)

JobFailureTypeDef = TypedDict(
    "JobFailureTypeDef", {"FailureCode": str, "FailureReason": str}, total=False
)

_RequiredJobManifestLocationTypeDef = TypedDict(
    "_RequiredJobManifestLocationTypeDef", {"ObjectArn": str, "ETag": str}
)
_OptionalJobManifestLocationTypeDef = TypedDict(
    "_OptionalJobManifestLocationTypeDef", {"ObjectVersionId": str}, total=False
)


class JobManifestLocationTypeDef(
    _RequiredJobManifestLocationTypeDef, _OptionalJobManifestLocationTypeDef
):
    pass


_RequiredJobManifestSpecTypeDef = TypedDict(
    "_RequiredJobManifestSpecTypeDef",
    {"Format": Literal["S3BatchOperations_CSV_20180820", "S3InventoryReport_CSV_20161130"]},
)
_OptionalJobManifestSpecTypeDef = TypedDict(
    "_OptionalJobManifestSpecTypeDef",
    {"Fields": List[Literal["Ignore", "Bucket", "Key", "VersionId"]]},
    total=False,
)


class JobManifestSpecTypeDef(_RequiredJobManifestSpecTypeDef, _OptionalJobManifestSpecTypeDef):
    pass


JobManifestTypeDef = TypedDict(
    "JobManifestTypeDef", {"Spec": JobManifestSpecTypeDef, "Location": JobManifestLocationTypeDef}
)

LambdaInvokeOperationTypeDef = TypedDict(
    "LambdaInvokeOperationTypeDef", {"FunctionArn": str}, total=False
)

S3GranteeTypeDef = TypedDict(
    "S3GranteeTypeDef",
    {"TypeIdentifier": Literal["id", "emailAddress", "uri"], "Identifier": str, "DisplayName": str},
    total=False,
)

S3GrantTypeDef = TypedDict(
    "S3GrantTypeDef",
    {
        "Grantee": S3GranteeTypeDef,
        "Permission": Literal["FULL_CONTROL", "READ", "WRITE", "READ_ACP", "WRITE_ACP"],
    },
    total=False,
)

S3ObjectMetadataTypeDef = TypedDict(
    "S3ObjectMetadataTypeDef",
    {
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "UserMetadata": Dict[str, str],
        "ContentLength": int,
        "ContentMD5": str,
        "ContentType": str,
        "HttpExpiresDate": datetime,
        "RequesterCharged": bool,
        "SSEAlgorithm": Literal["AES256", "KMS"],
    },
    total=False,
)

S3TagTypeDef = TypedDict("S3TagTypeDef", {"Key": str, "Value": str})

S3CopyObjectOperationTypeDef = TypedDict(
    "S3CopyObjectOperationTypeDef",
    {
        "TargetResource": str,
        "CannedAccessControlList": Literal[
            "private",
            "public-read",
            "public-read-write",
            "aws-exec-read",
            "authenticated-read",
            "bucket-owner-read",
            "bucket-owner-full-control",
        ],
        "AccessControlGrants": List[S3GrantTypeDef],
        "MetadataDirective": Literal["COPY", "REPLACE"],
        "ModifiedSinceConstraint": datetime,
        "NewObjectMetadata": S3ObjectMetadataTypeDef,
        "NewObjectTagging": List[S3TagTypeDef],
        "RedirectLocation": str,
        "RequesterPays": bool,
        "StorageClass": Literal[
            "STANDARD",
            "STANDARD_IA",
            "ONEZONE_IA",
            "GLACIER",
            "INTELLIGENT_TIERING",
            "DEEP_ARCHIVE",
        ],
        "UnModifiedSinceConstraint": datetime,
        "SSEAwsKmsKeyId": str,
        "TargetKeyPrefix": str,
        "ObjectLockLegalHoldStatus": Literal["OFF", "ON"],
        "ObjectLockMode": Literal["COMPLIANCE", "GOVERNANCE"],
        "ObjectLockRetainUntilDate": datetime,
    },
    total=False,
)

S3InitiateRestoreObjectOperationTypeDef = TypedDict(
    "S3InitiateRestoreObjectOperationTypeDef",
    {"ExpirationInDays": int, "GlacierJobTier": Literal["BULK", "STANDARD"]},
    total=False,
)

S3ObjectOwnerTypeDef = TypedDict(
    "S3ObjectOwnerTypeDef", {"ID": str, "DisplayName": str}, total=False
)

_RequiredS3AccessControlListTypeDef = TypedDict(
    "_RequiredS3AccessControlListTypeDef", {"Owner": S3ObjectOwnerTypeDef}
)
_OptionalS3AccessControlListTypeDef = TypedDict(
    "_OptionalS3AccessControlListTypeDef", {"Grants": List[S3GrantTypeDef]}, total=False
)


class S3AccessControlListTypeDef(
    _RequiredS3AccessControlListTypeDef, _OptionalS3AccessControlListTypeDef
):
    pass


S3AccessControlPolicyTypeDef = TypedDict(
    "S3AccessControlPolicyTypeDef",
    {
        "AccessControlList": S3AccessControlListTypeDef,
        "CannedAccessControlList": Literal[
            "private",
            "public-read",
            "public-read-write",
            "aws-exec-read",
            "authenticated-read",
            "bucket-owner-read",
            "bucket-owner-full-control",
        ],
    },
    total=False,
)

S3SetObjectAclOperationTypeDef = TypedDict(
    "S3SetObjectAclOperationTypeDef",
    {"AccessControlPolicy": S3AccessControlPolicyTypeDef},
    total=False,
)

S3SetObjectTaggingOperationTypeDef = TypedDict(
    "S3SetObjectTaggingOperationTypeDef", {"TagSet": List[S3TagTypeDef]}, total=False
)

JobOperationTypeDef = TypedDict(
    "JobOperationTypeDef",
    {
        "LambdaInvoke": LambdaInvokeOperationTypeDef,
        "S3PutObjectCopy": S3CopyObjectOperationTypeDef,
        "S3PutObjectAcl": S3SetObjectAclOperationTypeDef,
        "S3PutObjectTagging": S3SetObjectTaggingOperationTypeDef,
        "S3InitiateRestoreObject": S3InitiateRestoreObjectOperationTypeDef,
    },
    total=False,
)

JobProgressSummaryTypeDef = TypedDict(
    "JobProgressSummaryTypeDef",
    {"TotalNumberOfTasks": int, "NumberOfTasksSucceeded": int, "NumberOfTasksFailed": int},
    total=False,
)

_RequiredJobReportTypeDef = TypedDict("_RequiredJobReportTypeDef", {"Enabled": bool})
_OptionalJobReportTypeDef = TypedDict(
    "_OptionalJobReportTypeDef",
    {
        "Bucket": str,
        "Format": Literal["Report_CSV_20180820"],
        "Prefix": str,
        "ReportScope": Literal["AllTasks", "FailedTasksOnly"],
    },
    total=False,
)


class JobReportTypeDef(_RequiredJobReportTypeDef, _OptionalJobReportTypeDef):
    pass


JobDescriptorTypeDef = TypedDict(
    "JobDescriptorTypeDef",
    {
        "JobId": str,
        "ConfirmationRequired": bool,
        "Description": str,
        "JobArn": str,
        "Status": Literal[
            "Active",
            "Cancelled",
            "Cancelling",
            "Complete",
            "Completing",
            "Failed",
            "Failing",
            "New",
            "Paused",
            "Pausing",
            "Preparing",
            "Ready",
            "Suspended",
        ],
        "Manifest": JobManifestTypeDef,
        "Operation": JobOperationTypeDef,
        "Priority": int,
        "ProgressSummary": JobProgressSummaryTypeDef,
        "StatusUpdateReason": str,
        "FailureReasons": List[JobFailureTypeDef],
        "Report": JobReportTypeDef,
        "CreationTime": datetime,
        "TerminationDate": datetime,
        "RoleArn": str,
        "SuspendedDate": datetime,
        "SuspendedCause": str,
    },
    total=False,
)

DescribeJobResultTypeDef = TypedDict(
    "DescribeJobResultTypeDef", {"Job": JobDescriptorTypeDef}, total=False
)

GetAccessPointPolicyResultTypeDef = TypedDict(
    "GetAccessPointPolicyResultTypeDef", {"Policy": str}, total=False
)

PolicyStatusTypeDef = TypedDict("PolicyStatusTypeDef", {"IsPublic": bool}, total=False)

GetAccessPointPolicyStatusResultTypeDef = TypedDict(
    "GetAccessPointPolicyStatusResultTypeDef", {"PolicyStatus": PolicyStatusTypeDef}, total=False
)

PublicAccessBlockConfigurationTypeDef = TypedDict(
    "PublicAccessBlockConfigurationTypeDef",
    {
        "BlockPublicAcls": bool,
        "IgnorePublicAcls": bool,
        "BlockPublicPolicy": bool,
        "RestrictPublicBuckets": bool,
    },
    total=False,
)

VpcConfigurationTypeDef = TypedDict("VpcConfigurationTypeDef", {"VpcId": str})

GetAccessPointResultTypeDef = TypedDict(
    "GetAccessPointResultTypeDef",
    {
        "Name": str,
        "Bucket": str,
        "NetworkOrigin": Literal["Internet", "VPC"],
        "VpcConfiguration": VpcConfigurationTypeDef,
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "CreationDate": datetime,
    },
    total=False,
)

GetJobTaggingResultTypeDef = TypedDict(
    "GetJobTaggingResultTypeDef", {"Tags": List[S3TagTypeDef]}, total=False
)

GetPublicAccessBlockOutputTypeDef = TypedDict(
    "GetPublicAccessBlockOutputTypeDef",
    {"PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef},
    total=False,
)

_RequiredAccessPointTypeDef = TypedDict(
    "_RequiredAccessPointTypeDef",
    {"Name": str, "NetworkOrigin": Literal["Internet", "VPC"], "Bucket": str},
)
_OptionalAccessPointTypeDef = TypedDict(
    "_OptionalAccessPointTypeDef", {"VpcConfiguration": VpcConfigurationTypeDef}, total=False
)


class AccessPointTypeDef(_RequiredAccessPointTypeDef, _OptionalAccessPointTypeDef):
    pass


ListAccessPointsResultTypeDef = TypedDict(
    "ListAccessPointsResultTypeDef",
    {"AccessPointList": List[AccessPointTypeDef], "NextToken": str},
    total=False,
)

JobListDescriptorTypeDef = TypedDict(
    "JobListDescriptorTypeDef",
    {
        "JobId": str,
        "Description": str,
        "Operation": Literal[
            "LambdaInvoke",
            "S3PutObjectCopy",
            "S3PutObjectAcl",
            "S3PutObjectTagging",
            "S3InitiateRestoreObject",
        ],
        "Priority": int,
        "Status": Literal[
            "Active",
            "Cancelled",
            "Cancelling",
            "Complete",
            "Completing",
            "Failed",
            "Failing",
            "New",
            "Paused",
            "Pausing",
            "Preparing",
            "Ready",
            "Suspended",
        ],
        "CreationTime": datetime,
        "TerminationDate": datetime,
        "ProgressSummary": JobProgressSummaryTypeDef,
    },
    total=False,
)

ListJobsResultTypeDef = TypedDict(
    "ListJobsResultTypeDef", {"NextToken": str, "Jobs": List[JobListDescriptorTypeDef]}, total=False
)

UpdateJobPriorityResultTypeDef = TypedDict(
    "UpdateJobPriorityResultTypeDef", {"JobId": str, "Priority": int}
)

UpdateJobStatusResultTypeDef = TypedDict(
    "UpdateJobStatusResultTypeDef",
    {
        "JobId": str,
        "Status": Literal[
            "Active",
            "Cancelled",
            "Cancelling",
            "Complete",
            "Completing",
            "Failed",
            "Failing",
            "New",
            "Paused",
            "Pausing",
            "Preparing",
            "Ready",
            "Suspended",
        ],
        "StatusUpdateReason": str,
    },
    total=False,
)
