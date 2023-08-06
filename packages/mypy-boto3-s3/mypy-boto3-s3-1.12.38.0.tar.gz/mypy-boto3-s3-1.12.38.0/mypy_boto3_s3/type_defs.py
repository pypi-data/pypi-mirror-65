"""
Main interface for s3 service type definitions.

Usage::

    from mypy_boto3.s3.type_defs import AbortMultipartUploadOutputTypeDef

    data: AbortMultipartUploadOutputTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Any, Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AbortMultipartUploadOutputTypeDef",
    "AccelerateConfigurationTypeDef",
    "GranteeTypeDef",
    "GrantTypeDef",
    "OwnerTypeDef",
    "AccessControlPolicyTypeDef",
    "TagTypeDef",
    "AnalyticsAndOperatorTypeDef",
    "AnalyticsFilterTypeDef",
    "AnalyticsS3BucketDestinationTypeDef",
    "AnalyticsExportDestinationTypeDef",
    "StorageClassAnalysisDataExportTypeDef",
    "StorageClassAnalysisTypeDef",
    "AnalyticsConfigurationTypeDef",
    "AbortIncompleteMultipartUploadTypeDef",
    "LifecycleExpirationTypeDef",
    "LifecycleRuleAndOperatorTypeDef",
    "LifecycleRuleFilterTypeDef",
    "NoncurrentVersionExpirationTypeDef",
    "NoncurrentVersionTransitionTypeDef",
    "TransitionTypeDef",
    "LifecycleRuleTypeDef",
    "BucketLifecycleConfigurationTypeDef",
    "TargetGrantTypeDef",
    "LoggingEnabledTypeDef",
    "BucketLoggingStatusTypeDef",
    "CORSRuleTypeDef",
    "CORSConfigurationTypeDef",
    "CompleteMultipartUploadOutputTypeDef",
    "CompletedPartTypeDef",
    "CompletedMultipartUploadTypeDef",
    "CopyObjectResultTypeDef",
    "CopyObjectOutputTypeDef",
    "CopySourceTypeDef",
    "CreateBucketConfigurationTypeDef",
    "CreateBucketOutputTypeDef",
    "CreateMultipartUploadOutputTypeDef",
    "DeleteObjectOutputTypeDef",
    "DeleteObjectTaggingOutputTypeDef",
    "DeletedObjectTypeDef",
    "ErrorTypeDef",
    "DeleteObjectsOutputTypeDef",
    "ObjectIdentifierTypeDef",
    "DeleteTypeDef",
    "GetBucketAccelerateConfigurationOutputTypeDef",
    "GetBucketAclOutputTypeDef",
    "GetBucketAnalyticsConfigurationOutputTypeDef",
    "GetBucketCorsOutputTypeDef",
    "ServerSideEncryptionByDefaultTypeDef",
    "ServerSideEncryptionRuleTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "GetBucketEncryptionOutputTypeDef",
    "SSEKMSTypeDef",
    "InventoryEncryptionTypeDef",
    "InventoryS3BucketDestinationTypeDef",
    "InventoryDestinationTypeDef",
    "InventoryFilterTypeDef",
    "InventoryScheduleTypeDef",
    "InventoryConfigurationTypeDef",
    "GetBucketInventoryConfigurationOutputTypeDef",
    "GetBucketLifecycleConfigurationOutputTypeDef",
    "RuleTypeDef",
    "GetBucketLifecycleOutputTypeDef",
    "GetBucketLocationOutputTypeDef",
    "GetBucketLoggingOutputTypeDef",
    "MetricsAndOperatorTypeDef",
    "MetricsFilterTypeDef",
    "MetricsConfigurationTypeDef",
    "GetBucketMetricsConfigurationOutputTypeDef",
    "GetBucketPolicyOutputTypeDef",
    "PolicyStatusTypeDef",
    "GetBucketPolicyStatusOutputTypeDef",
    "DeleteMarkerReplicationTypeDef",
    "AccessControlTranslationTypeDef",
    "EncryptionConfigurationTypeDef",
    "ReplicationTimeValueTypeDef",
    "MetricsTypeDef",
    "ReplicationTimeTypeDef",
    "DestinationTypeDef",
    "ExistingObjectReplicationTypeDef",
    "ReplicationRuleAndOperatorTypeDef",
    "ReplicationRuleFilterTypeDef",
    "SseKmsEncryptedObjectsTypeDef",
    "SourceSelectionCriteriaTypeDef",
    "ReplicationRuleTypeDef",
    "ReplicationConfigurationTypeDef",
    "GetBucketReplicationOutputTypeDef",
    "GetBucketRequestPaymentOutputTypeDef",
    "GetBucketTaggingOutputTypeDef",
    "GetBucketVersioningOutputTypeDef",
    "ErrorDocumentTypeDef",
    "IndexDocumentTypeDef",
    "RedirectAllRequestsToTypeDef",
    "ConditionTypeDef",
    "RedirectTypeDef",
    "RoutingRuleTypeDef",
    "GetBucketWebsiteOutputTypeDef",
    "GetObjectAclOutputTypeDef",
    "ObjectLockLegalHoldTypeDef",
    "GetObjectLegalHoldOutputTypeDef",
    "DefaultRetentionTypeDef",
    "ObjectLockRuleTypeDef",
    "ObjectLockConfigurationTypeDef",
    "GetObjectLockConfigurationOutputTypeDef",
    "GetObjectOutputTypeDef",
    "ObjectLockRetentionTypeDef",
    "GetObjectRetentionOutputTypeDef",
    "GetObjectTaggingOutputTypeDef",
    "GetObjectTorrentOutputTypeDef",
    "PublicAccessBlockConfigurationTypeDef",
    "GetPublicAccessBlockOutputTypeDef",
    "HeadObjectOutputTypeDef",
    "CSVInputTypeDef",
    "JSONInputTypeDef",
    "InputSerializationTypeDef",
    "LifecycleConfigurationTypeDef",
    "ListBucketAnalyticsConfigurationsOutputTypeDef",
    "ListBucketInventoryConfigurationsOutputTypeDef",
    "ListBucketMetricsConfigurationsOutputTypeDef",
    "BucketTypeDef",
    "ListBucketsOutputTypeDef",
    "CommonPrefixTypeDef",
    "InitiatorTypeDef",
    "MultipartUploadTypeDef",
    "ListMultipartUploadsOutputTypeDef",
    "DeleteMarkerEntryTypeDef",
    "ObjectVersionTypeDef",
    "ListObjectVersionsOutputTypeDef",
    "ObjectTypeDef",
    "ListObjectsOutputTypeDef",
    "ListObjectsV2OutputTypeDef",
    "PartTypeDef",
    "ListPartsOutputTypeDef",
    "CloudFunctionConfigurationTypeDef",
    "QueueConfigurationDeprecatedTypeDef",
    "TopicConfigurationDeprecatedTypeDef",
    "NotificationConfigurationDeprecatedTypeDef",
    "FilterRuleTypeDef",
    "S3KeyFilterTypeDef",
    "NotificationConfigurationFilterTypeDef",
    "LambdaFunctionConfigurationTypeDef",
    "QueueConfigurationTypeDef",
    "TopicConfigurationTypeDef",
    "NotificationConfigurationTypeDef",
    "CSVOutputTypeDef",
    "JSONOutputTypeDef",
    "OutputSerializationTypeDef",
    "PaginatorConfigTypeDef",
    "PutObjectAclOutputTypeDef",
    "PutObjectLegalHoldOutputTypeDef",
    "PutObjectLockConfigurationOutputTypeDef",
    "PutObjectOutputTypeDef",
    "PutObjectRetentionOutputTypeDef",
    "PutObjectTaggingOutputTypeDef",
    "RequestPaymentConfigurationTypeDef",
    "RequestProgressTypeDef",
    "RestoreObjectOutputTypeDef",
    "GlacierJobParametersTypeDef",
    "EncryptionTypeDef",
    "MetadataEntryTypeDef",
    "TaggingTypeDef",
    "S3LocationTypeDef",
    "OutputLocationTypeDef",
    "SelectParametersTypeDef",
    "RestoreRequestTypeDef",
    "ScanRangeTypeDef",
    "ProgressTypeDef",
    "ProgressEventTypeDef",
    "RecordsEventTypeDef",
    "StatsTypeDef",
    "StatsEventTypeDef",
    "SelectObjectContentEventStreamTypeDef",
    "SelectObjectContentOutputTypeDef",
    "CopyPartResultTypeDef",
    "UploadPartCopyOutputTypeDef",
    "UploadPartOutputTypeDef",
    "VersioningConfigurationTypeDef",
    "WaiterConfigTypeDef",
    "WebsiteConfigurationTypeDef",
)

AbortMultipartUploadOutputTypeDef = TypedDict(
    "AbortMultipartUploadOutputTypeDef", {"RequestCharged": Literal["requester"]}, total=False
)

AccelerateConfigurationTypeDef = TypedDict(
    "AccelerateConfigurationTypeDef", {"Status": Literal["Enabled", "Suspended"]}, total=False
)

_RequiredGranteeTypeDef = TypedDict(
    "_RequiredGranteeTypeDef", {"Type": Literal["CanonicalUser", "AmazonCustomerByEmail", "Group"]}
)
_OptionalGranteeTypeDef = TypedDict(
    "_OptionalGranteeTypeDef",
    {"DisplayName": str, "EmailAddress": str, "ID": str, "URI": str},
    total=False,
)


class GranteeTypeDef(_RequiredGranteeTypeDef, _OptionalGranteeTypeDef):
    pass


GrantTypeDef = TypedDict(
    "GrantTypeDef",
    {
        "Grantee": GranteeTypeDef,
        "Permission": Literal["FULL_CONTROL", "WRITE", "WRITE_ACP", "READ", "READ_ACP"],
    },
    total=False,
)

OwnerTypeDef = TypedDict("OwnerTypeDef", {"DisplayName": str, "ID": str}, total=False)

AccessControlPolicyTypeDef = TypedDict(
    "AccessControlPolicyTypeDef", {"Grants": List[GrantTypeDef], "Owner": OwnerTypeDef}, total=False
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

AnalyticsAndOperatorTypeDef = TypedDict(
    "AnalyticsAndOperatorTypeDef", {"Prefix": str, "Tags": List[TagTypeDef]}, total=False
)

AnalyticsFilterTypeDef = TypedDict(
    "AnalyticsFilterTypeDef",
    {"Prefix": str, "Tag": TagTypeDef, "And": AnalyticsAndOperatorTypeDef},
    total=False,
)

_RequiredAnalyticsS3BucketDestinationTypeDef = TypedDict(
    "_RequiredAnalyticsS3BucketDestinationTypeDef", {"Format": Literal["CSV"], "Bucket": str}
)
_OptionalAnalyticsS3BucketDestinationTypeDef = TypedDict(
    "_OptionalAnalyticsS3BucketDestinationTypeDef",
    {"BucketAccountId": str, "Prefix": str},
    total=False,
)


class AnalyticsS3BucketDestinationTypeDef(
    _RequiredAnalyticsS3BucketDestinationTypeDef, _OptionalAnalyticsS3BucketDestinationTypeDef
):
    pass


AnalyticsExportDestinationTypeDef = TypedDict(
    "AnalyticsExportDestinationTypeDef",
    {"S3BucketDestination": AnalyticsS3BucketDestinationTypeDef},
)

StorageClassAnalysisDataExportTypeDef = TypedDict(
    "StorageClassAnalysisDataExportTypeDef",
    {"OutputSchemaVersion": Literal["V_1"], "Destination": AnalyticsExportDestinationTypeDef},
)

StorageClassAnalysisTypeDef = TypedDict(
    "StorageClassAnalysisTypeDef",
    {"DataExport": StorageClassAnalysisDataExportTypeDef},
    total=False,
)

_RequiredAnalyticsConfigurationTypeDef = TypedDict(
    "_RequiredAnalyticsConfigurationTypeDef",
    {"Id": str, "StorageClassAnalysis": StorageClassAnalysisTypeDef},
)
_OptionalAnalyticsConfigurationTypeDef = TypedDict(
    "_OptionalAnalyticsConfigurationTypeDef", {"Filter": AnalyticsFilterTypeDef}, total=False
)


class AnalyticsConfigurationTypeDef(
    _RequiredAnalyticsConfigurationTypeDef, _OptionalAnalyticsConfigurationTypeDef
):
    pass


AbortIncompleteMultipartUploadTypeDef = TypedDict(
    "AbortIncompleteMultipartUploadTypeDef", {"DaysAfterInitiation": int}, total=False
)

LifecycleExpirationTypeDef = TypedDict(
    "LifecycleExpirationTypeDef",
    {"Date": datetime, "Days": int, "ExpiredObjectDeleteMarker": bool},
    total=False,
)

LifecycleRuleAndOperatorTypeDef = TypedDict(
    "LifecycleRuleAndOperatorTypeDef", {"Prefix": str, "Tags": List[TagTypeDef]}, total=False
)

LifecycleRuleFilterTypeDef = TypedDict(
    "LifecycleRuleFilterTypeDef",
    {"Prefix": str, "Tag": TagTypeDef, "And": LifecycleRuleAndOperatorTypeDef},
    total=False,
)

NoncurrentVersionExpirationTypeDef = TypedDict(
    "NoncurrentVersionExpirationTypeDef", {"NoncurrentDays": int}, total=False
)

NoncurrentVersionTransitionTypeDef = TypedDict(
    "NoncurrentVersionTransitionTypeDef",
    {
        "NoncurrentDays": int,
        "StorageClass": Literal[
            "GLACIER", "STANDARD_IA", "ONEZONE_IA", "INTELLIGENT_TIERING", "DEEP_ARCHIVE"
        ],
    },
    total=False,
)

TransitionTypeDef = TypedDict(
    "TransitionTypeDef",
    {
        "Date": datetime,
        "Days": int,
        "StorageClass": Literal[
            "GLACIER", "STANDARD_IA", "ONEZONE_IA", "INTELLIGENT_TIERING", "DEEP_ARCHIVE"
        ],
    },
    total=False,
)

_RequiredLifecycleRuleTypeDef = TypedDict(
    "_RequiredLifecycleRuleTypeDef", {"Status": Literal["Enabled", "Disabled"]}
)
_OptionalLifecycleRuleTypeDef = TypedDict(
    "_OptionalLifecycleRuleTypeDef",
    {
        "Expiration": LifecycleExpirationTypeDef,
        "ID": str,
        "Prefix": str,
        "Filter": LifecycleRuleFilterTypeDef,
        "Transitions": List[TransitionTypeDef],
        "NoncurrentVersionTransitions": List[NoncurrentVersionTransitionTypeDef],
        "NoncurrentVersionExpiration": NoncurrentVersionExpirationTypeDef,
        "AbortIncompleteMultipartUpload": AbortIncompleteMultipartUploadTypeDef,
    },
    total=False,
)


class LifecycleRuleTypeDef(_RequiredLifecycleRuleTypeDef, _OptionalLifecycleRuleTypeDef):
    pass


BucketLifecycleConfigurationTypeDef = TypedDict(
    "BucketLifecycleConfigurationTypeDef", {"Rules": List[LifecycleRuleTypeDef]}
)

TargetGrantTypeDef = TypedDict(
    "TargetGrantTypeDef",
    {"Grantee": GranteeTypeDef, "Permission": Literal["FULL_CONTROL", "READ", "WRITE"]},
    total=False,
)

_RequiredLoggingEnabledTypeDef = TypedDict(
    "_RequiredLoggingEnabledTypeDef", {"TargetBucket": str, "TargetPrefix": str}
)
_OptionalLoggingEnabledTypeDef = TypedDict(
    "_OptionalLoggingEnabledTypeDef", {"TargetGrants": List[TargetGrantTypeDef]}, total=False
)


class LoggingEnabledTypeDef(_RequiredLoggingEnabledTypeDef, _OptionalLoggingEnabledTypeDef):
    pass


BucketLoggingStatusTypeDef = TypedDict(
    "BucketLoggingStatusTypeDef", {"LoggingEnabled": LoggingEnabledTypeDef}, total=False
)

_RequiredCORSRuleTypeDef = TypedDict(
    "_RequiredCORSRuleTypeDef", {"AllowedMethods": List[str], "AllowedOrigins": List[str]}
)
_OptionalCORSRuleTypeDef = TypedDict(
    "_OptionalCORSRuleTypeDef",
    {"AllowedHeaders": List[str], "ExposeHeaders": List[str], "MaxAgeSeconds": int},
    total=False,
)


class CORSRuleTypeDef(_RequiredCORSRuleTypeDef, _OptionalCORSRuleTypeDef):
    pass


CORSConfigurationTypeDef = TypedDict(
    "CORSConfigurationTypeDef", {"CORSRules": List[CORSRuleTypeDef]}
)

CompleteMultipartUploadOutputTypeDef = TypedDict(
    "CompleteMultipartUploadOutputTypeDef",
    {
        "Location": str,
        "Bucket": str,
        "Key": str,
        "Expiration": str,
        "ETag": str,
        "ServerSideEncryption": Literal["AES256", "aws:kms"],
        "VersionId": str,
        "SSEKMSKeyId": str,
        "RequestCharged": Literal["requester"],
    },
    total=False,
)

CompletedPartTypeDef = TypedDict(
    "CompletedPartTypeDef", {"ETag": str, "PartNumber": int}, total=False
)

CompletedMultipartUploadTypeDef = TypedDict(
    "CompletedMultipartUploadTypeDef", {"Parts": List[CompletedPartTypeDef]}, total=False
)

CopyObjectResultTypeDef = TypedDict(
    "CopyObjectResultTypeDef", {"ETag": str, "LastModified": datetime}, total=False
)

CopyObjectOutputTypeDef = TypedDict(
    "CopyObjectOutputTypeDef",
    {
        "CopyObjectResult": CopyObjectResultTypeDef,
        "Expiration": str,
        "CopySourceVersionId": str,
        "VersionId": str,
        "ServerSideEncryption": Literal["AES256", "aws:kms"],
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "RequestCharged": Literal["requester"],
    },
    total=False,
)

_RequiredCopySourceTypeDef = TypedDict("_RequiredCopySourceTypeDef", {"Bucket": str, "Key": str})
_OptionalCopySourceTypeDef = TypedDict(
    "_OptionalCopySourceTypeDef", {"VersionId": str}, total=False
)


class CopySourceTypeDef(_RequiredCopySourceTypeDef, _OptionalCopySourceTypeDef):
    pass


CreateBucketConfigurationTypeDef = TypedDict(
    "CreateBucketConfigurationTypeDef",
    {
        "LocationConstraint": Literal[
            "EU",
            "eu-west-1",
            "us-west-1",
            "us-west-2",
            "ap-south-1",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-northeast-1",
            "sa-east-1",
            "cn-north-1",
            "eu-central-1",
        ]
    },
    total=False,
)

CreateBucketOutputTypeDef = TypedDict("CreateBucketOutputTypeDef", {"Location": str}, total=False)

CreateMultipartUploadOutputTypeDef = TypedDict(
    "CreateMultipartUploadOutputTypeDef",
    {
        "AbortDate": datetime,
        "AbortRuleId": str,
        "Bucket": str,
        "Key": str,
        "UploadId": str,
        "ServerSideEncryption": Literal["AES256", "aws:kms"],
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "RequestCharged": Literal["requester"],
    },
    total=False,
)

DeleteObjectOutputTypeDef = TypedDict(
    "DeleteObjectOutputTypeDef",
    {"DeleteMarker": bool, "VersionId": str, "RequestCharged": Literal["requester"]},
    total=False,
)

DeleteObjectTaggingOutputTypeDef = TypedDict(
    "DeleteObjectTaggingOutputTypeDef", {"VersionId": str}, total=False
)

DeletedObjectTypeDef = TypedDict(
    "DeletedObjectTypeDef",
    {"Key": str, "VersionId": str, "DeleteMarker": bool, "DeleteMarkerVersionId": str},
    total=False,
)

ErrorTypeDef = TypedDict(
    "ErrorTypeDef", {"Key": str, "VersionId": str, "Code": str, "Message": str}, total=False
)

DeleteObjectsOutputTypeDef = TypedDict(
    "DeleteObjectsOutputTypeDef",
    {
        "Deleted": List[DeletedObjectTypeDef],
        "RequestCharged": Literal["requester"],
        "Errors": List[ErrorTypeDef],
    },
    total=False,
)

_RequiredObjectIdentifierTypeDef = TypedDict("_RequiredObjectIdentifierTypeDef", {"Key": str})
_OptionalObjectIdentifierTypeDef = TypedDict(
    "_OptionalObjectIdentifierTypeDef", {"VersionId": str}, total=False
)


class ObjectIdentifierTypeDef(_RequiredObjectIdentifierTypeDef, _OptionalObjectIdentifierTypeDef):
    pass


_RequiredDeleteTypeDef = TypedDict(
    "_RequiredDeleteTypeDef", {"Objects": List[ObjectIdentifierTypeDef]}
)
_OptionalDeleteTypeDef = TypedDict("_OptionalDeleteTypeDef", {"Quiet": bool}, total=False)


class DeleteTypeDef(_RequiredDeleteTypeDef, _OptionalDeleteTypeDef):
    pass


GetBucketAccelerateConfigurationOutputTypeDef = TypedDict(
    "GetBucketAccelerateConfigurationOutputTypeDef",
    {"Status": Literal["Enabled", "Suspended"]},
    total=False,
)

GetBucketAclOutputTypeDef = TypedDict(
    "GetBucketAclOutputTypeDef", {"Owner": OwnerTypeDef, "Grants": List[GrantTypeDef]}, total=False
)

GetBucketAnalyticsConfigurationOutputTypeDef = TypedDict(
    "GetBucketAnalyticsConfigurationOutputTypeDef",
    {"AnalyticsConfiguration": AnalyticsConfigurationTypeDef},
    total=False,
)

GetBucketCorsOutputTypeDef = TypedDict(
    "GetBucketCorsOutputTypeDef", {"CORSRules": List[CORSRuleTypeDef]}, total=False
)

_RequiredServerSideEncryptionByDefaultTypeDef = TypedDict(
    "_RequiredServerSideEncryptionByDefaultTypeDef", {"SSEAlgorithm": Literal["AES256", "aws:kms"]}
)
_OptionalServerSideEncryptionByDefaultTypeDef = TypedDict(
    "_OptionalServerSideEncryptionByDefaultTypeDef", {"KMSMasterKeyID": str}, total=False
)


class ServerSideEncryptionByDefaultTypeDef(
    _RequiredServerSideEncryptionByDefaultTypeDef, _OptionalServerSideEncryptionByDefaultTypeDef
):
    pass


ServerSideEncryptionRuleTypeDef = TypedDict(
    "ServerSideEncryptionRuleTypeDef",
    {"ApplyServerSideEncryptionByDefault": ServerSideEncryptionByDefaultTypeDef},
    total=False,
)

ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef", {"Rules": List[ServerSideEncryptionRuleTypeDef]}
)

GetBucketEncryptionOutputTypeDef = TypedDict(
    "GetBucketEncryptionOutputTypeDef",
    {"ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef},
    total=False,
)

SSEKMSTypeDef = TypedDict("SSEKMSTypeDef", {"KeyId": str})

InventoryEncryptionTypeDef = TypedDict(
    "InventoryEncryptionTypeDef", {"SSES3": Dict[str, Any], "SSEKMS": SSEKMSTypeDef}, total=False
)

_RequiredInventoryS3BucketDestinationTypeDef = TypedDict(
    "_RequiredInventoryS3BucketDestinationTypeDef",
    {"Bucket": str, "Format": Literal["CSV", "ORC", "Parquet"]},
)
_OptionalInventoryS3BucketDestinationTypeDef = TypedDict(
    "_OptionalInventoryS3BucketDestinationTypeDef",
    {"AccountId": str, "Prefix": str, "Encryption": InventoryEncryptionTypeDef},
    total=False,
)


class InventoryS3BucketDestinationTypeDef(
    _RequiredInventoryS3BucketDestinationTypeDef, _OptionalInventoryS3BucketDestinationTypeDef
):
    pass


InventoryDestinationTypeDef = TypedDict(
    "InventoryDestinationTypeDef", {"S3BucketDestination": InventoryS3BucketDestinationTypeDef}
)

InventoryFilterTypeDef = TypedDict("InventoryFilterTypeDef", {"Prefix": str})

InventoryScheduleTypeDef = TypedDict(
    "InventoryScheduleTypeDef", {"Frequency": Literal["Daily", "Weekly"]}
)

_RequiredInventoryConfigurationTypeDef = TypedDict(
    "_RequiredInventoryConfigurationTypeDef",
    {
        "Destination": InventoryDestinationTypeDef,
        "IsEnabled": bool,
        "Id": str,
        "IncludedObjectVersions": Literal["All", "Current"],
        "Schedule": InventoryScheduleTypeDef,
    },
)
_OptionalInventoryConfigurationTypeDef = TypedDict(
    "_OptionalInventoryConfigurationTypeDef",
    {
        "Filter": InventoryFilterTypeDef,
        "OptionalFields": List[
            Literal[
                "Size",
                "LastModifiedDate",
                "StorageClass",
                "ETag",
                "IsMultipartUploaded",
                "ReplicationStatus",
                "EncryptionStatus",
                "ObjectLockRetainUntilDate",
                "ObjectLockMode",
                "ObjectLockLegalHoldStatus",
                "IntelligentTieringAccessTier",
            ]
        ],
    },
    total=False,
)


class InventoryConfigurationTypeDef(
    _RequiredInventoryConfigurationTypeDef, _OptionalInventoryConfigurationTypeDef
):
    pass


GetBucketInventoryConfigurationOutputTypeDef = TypedDict(
    "GetBucketInventoryConfigurationOutputTypeDef",
    {"InventoryConfiguration": InventoryConfigurationTypeDef},
    total=False,
)

GetBucketLifecycleConfigurationOutputTypeDef = TypedDict(
    "GetBucketLifecycleConfigurationOutputTypeDef",
    {"Rules": List[LifecycleRuleTypeDef]},
    total=False,
)

_RequiredRuleTypeDef = TypedDict(
    "_RequiredRuleTypeDef", {"Prefix": str, "Status": Literal["Enabled", "Disabled"]}
)
_OptionalRuleTypeDef = TypedDict(
    "_OptionalRuleTypeDef",
    {
        "Expiration": LifecycleExpirationTypeDef,
        "ID": str,
        "Transition": TransitionTypeDef,
        "NoncurrentVersionTransition": NoncurrentVersionTransitionTypeDef,
        "NoncurrentVersionExpiration": NoncurrentVersionExpirationTypeDef,
        "AbortIncompleteMultipartUpload": AbortIncompleteMultipartUploadTypeDef,
    },
    total=False,
)


class RuleTypeDef(_RequiredRuleTypeDef, _OptionalRuleTypeDef):
    pass


GetBucketLifecycleOutputTypeDef = TypedDict(
    "GetBucketLifecycleOutputTypeDef", {"Rules": List[RuleTypeDef]}, total=False
)

GetBucketLocationOutputTypeDef = TypedDict(
    "GetBucketLocationOutputTypeDef",
    {
        "LocationConstraint": Literal[
            "EU",
            "eu-west-1",
            "us-west-1",
            "us-west-2",
            "ap-south-1",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-northeast-1",
            "sa-east-1",
            "cn-north-1",
            "eu-central-1",
        ]
    },
    total=False,
)

GetBucketLoggingOutputTypeDef = TypedDict(
    "GetBucketLoggingOutputTypeDef", {"LoggingEnabled": LoggingEnabledTypeDef}, total=False
)

MetricsAndOperatorTypeDef = TypedDict(
    "MetricsAndOperatorTypeDef", {"Prefix": str, "Tags": List[TagTypeDef]}, total=False
)

MetricsFilterTypeDef = TypedDict(
    "MetricsFilterTypeDef",
    {"Prefix": str, "Tag": TagTypeDef, "And": MetricsAndOperatorTypeDef},
    total=False,
)

_RequiredMetricsConfigurationTypeDef = TypedDict(
    "_RequiredMetricsConfigurationTypeDef", {"Id": str}
)
_OptionalMetricsConfigurationTypeDef = TypedDict(
    "_OptionalMetricsConfigurationTypeDef", {"Filter": MetricsFilterTypeDef}, total=False
)


class MetricsConfigurationTypeDef(
    _RequiredMetricsConfigurationTypeDef, _OptionalMetricsConfigurationTypeDef
):
    pass


GetBucketMetricsConfigurationOutputTypeDef = TypedDict(
    "GetBucketMetricsConfigurationOutputTypeDef",
    {"MetricsConfiguration": MetricsConfigurationTypeDef},
    total=False,
)

GetBucketPolicyOutputTypeDef = TypedDict(
    "GetBucketPolicyOutputTypeDef", {"Policy": str}, total=False
)

PolicyStatusTypeDef = TypedDict("PolicyStatusTypeDef", {"IsPublic": bool}, total=False)

GetBucketPolicyStatusOutputTypeDef = TypedDict(
    "GetBucketPolicyStatusOutputTypeDef", {"PolicyStatus": PolicyStatusTypeDef}, total=False
)

DeleteMarkerReplicationTypeDef = TypedDict(
    "DeleteMarkerReplicationTypeDef", {"Status": Literal["Enabled", "Disabled"]}, total=False
)

AccessControlTranslationTypeDef = TypedDict(
    "AccessControlTranslationTypeDef", {"Owner": Literal["Destination"]}
)

EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef", {"ReplicaKmsKeyID": str}, total=False
)

ReplicationTimeValueTypeDef = TypedDict(
    "ReplicationTimeValueTypeDef", {"Minutes": int}, total=False
)

MetricsTypeDef = TypedDict(
    "MetricsTypeDef",
    {"Status": Literal["Enabled", "Disabled"], "EventThreshold": ReplicationTimeValueTypeDef},
)

ReplicationTimeTypeDef = TypedDict(
    "ReplicationTimeTypeDef",
    {"Status": Literal["Enabled", "Disabled"], "Time": ReplicationTimeValueTypeDef},
)

_RequiredDestinationTypeDef = TypedDict("_RequiredDestinationTypeDef", {"Bucket": str})
_OptionalDestinationTypeDef = TypedDict(
    "_OptionalDestinationTypeDef",
    {
        "Account": str,
        "StorageClass": Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ],
        "AccessControlTranslation": AccessControlTranslationTypeDef,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "ReplicationTime": ReplicationTimeTypeDef,
        "Metrics": MetricsTypeDef,
    },
    total=False,
)


class DestinationTypeDef(_RequiredDestinationTypeDef, _OptionalDestinationTypeDef):
    pass


ExistingObjectReplicationTypeDef = TypedDict(
    "ExistingObjectReplicationTypeDef", {"Status": Literal["Enabled", "Disabled"]}
)

ReplicationRuleAndOperatorTypeDef = TypedDict(
    "ReplicationRuleAndOperatorTypeDef", {"Prefix": str, "Tags": List[TagTypeDef]}, total=False
)

ReplicationRuleFilterTypeDef = TypedDict(
    "ReplicationRuleFilterTypeDef",
    {"Prefix": str, "Tag": TagTypeDef, "And": ReplicationRuleAndOperatorTypeDef},
    total=False,
)

SseKmsEncryptedObjectsTypeDef = TypedDict(
    "SseKmsEncryptedObjectsTypeDef", {"Status": Literal["Enabled", "Disabled"]}
)

SourceSelectionCriteriaTypeDef = TypedDict(
    "SourceSelectionCriteriaTypeDef",
    {"SseKmsEncryptedObjects": SseKmsEncryptedObjectsTypeDef},
    total=False,
)

_RequiredReplicationRuleTypeDef = TypedDict(
    "_RequiredReplicationRuleTypeDef",
    {"Status": Literal["Enabled", "Disabled"], "Destination": DestinationTypeDef},
)
_OptionalReplicationRuleTypeDef = TypedDict(
    "_OptionalReplicationRuleTypeDef",
    {
        "ID": str,
        "Priority": int,
        "Prefix": str,
        "Filter": ReplicationRuleFilterTypeDef,
        "SourceSelectionCriteria": SourceSelectionCriteriaTypeDef,
        "ExistingObjectReplication": ExistingObjectReplicationTypeDef,
        "DeleteMarkerReplication": DeleteMarkerReplicationTypeDef,
    },
    total=False,
)


class ReplicationRuleTypeDef(_RequiredReplicationRuleTypeDef, _OptionalReplicationRuleTypeDef):
    pass


ReplicationConfigurationTypeDef = TypedDict(
    "ReplicationConfigurationTypeDef", {"Role": str, "Rules": List[ReplicationRuleTypeDef]}
)

GetBucketReplicationOutputTypeDef = TypedDict(
    "GetBucketReplicationOutputTypeDef",
    {"ReplicationConfiguration": ReplicationConfigurationTypeDef},
    total=False,
)

GetBucketRequestPaymentOutputTypeDef = TypedDict(
    "GetBucketRequestPaymentOutputTypeDef",
    {"Payer": Literal["Requester", "BucketOwner"]},
    total=False,
)

GetBucketTaggingOutputTypeDef = TypedDict(
    "GetBucketTaggingOutputTypeDef", {"TagSet": List[TagTypeDef]}
)

GetBucketVersioningOutputTypeDef = TypedDict(
    "GetBucketVersioningOutputTypeDef",
    {"Status": Literal["Enabled", "Suspended"], "MFADelete": Literal["Enabled", "Disabled"]},
    total=False,
)

ErrorDocumentTypeDef = TypedDict("ErrorDocumentTypeDef", {"Key": str})

IndexDocumentTypeDef = TypedDict("IndexDocumentTypeDef", {"Suffix": str})

_RequiredRedirectAllRequestsToTypeDef = TypedDict(
    "_RequiredRedirectAllRequestsToTypeDef", {"HostName": str}
)
_OptionalRedirectAllRequestsToTypeDef = TypedDict(
    "_OptionalRedirectAllRequestsToTypeDef", {"Protocol": Literal["http", "https"]}, total=False
)


class RedirectAllRequestsToTypeDef(
    _RequiredRedirectAllRequestsToTypeDef, _OptionalRedirectAllRequestsToTypeDef
):
    pass


ConditionTypeDef = TypedDict(
    "ConditionTypeDef", {"HttpErrorCodeReturnedEquals": str, "KeyPrefixEquals": str}, total=False
)

RedirectTypeDef = TypedDict(
    "RedirectTypeDef",
    {
        "HostName": str,
        "HttpRedirectCode": str,
        "Protocol": Literal["http", "https"],
        "ReplaceKeyPrefixWith": str,
        "ReplaceKeyWith": str,
    },
    total=False,
)

_RequiredRoutingRuleTypeDef = TypedDict(
    "_RequiredRoutingRuleTypeDef", {"Redirect": RedirectTypeDef}
)
_OptionalRoutingRuleTypeDef = TypedDict(
    "_OptionalRoutingRuleTypeDef", {"Condition": ConditionTypeDef}, total=False
)


class RoutingRuleTypeDef(_RequiredRoutingRuleTypeDef, _OptionalRoutingRuleTypeDef):
    pass


GetBucketWebsiteOutputTypeDef = TypedDict(
    "GetBucketWebsiteOutputTypeDef",
    {
        "RedirectAllRequestsTo": RedirectAllRequestsToTypeDef,
        "IndexDocument": IndexDocumentTypeDef,
        "ErrorDocument": ErrorDocumentTypeDef,
        "RoutingRules": List[RoutingRuleTypeDef],
    },
    total=False,
)

GetObjectAclOutputTypeDef = TypedDict(
    "GetObjectAclOutputTypeDef",
    {"Owner": OwnerTypeDef, "Grants": List[GrantTypeDef], "RequestCharged": Literal["requester"]},
    total=False,
)

ObjectLockLegalHoldTypeDef = TypedDict(
    "ObjectLockLegalHoldTypeDef", {"Status": Literal["ON", "OFF"]}, total=False
)

GetObjectLegalHoldOutputTypeDef = TypedDict(
    "GetObjectLegalHoldOutputTypeDef", {"LegalHold": ObjectLockLegalHoldTypeDef}, total=False
)

DefaultRetentionTypeDef = TypedDict(
    "DefaultRetentionTypeDef",
    {"Mode": Literal["GOVERNANCE", "COMPLIANCE"], "Days": int, "Years": int},
    total=False,
)

ObjectLockRuleTypeDef = TypedDict(
    "ObjectLockRuleTypeDef", {"DefaultRetention": DefaultRetentionTypeDef}, total=False
)

ObjectLockConfigurationTypeDef = TypedDict(
    "ObjectLockConfigurationTypeDef",
    {"ObjectLockEnabled": Literal["Enabled"], "Rule": ObjectLockRuleTypeDef},
    total=False,
)

GetObjectLockConfigurationOutputTypeDef = TypedDict(
    "GetObjectLockConfigurationOutputTypeDef",
    {"ObjectLockConfiguration": ObjectLockConfigurationTypeDef},
    total=False,
)

GetObjectOutputTypeDef = TypedDict(
    "GetObjectOutputTypeDef",
    {
        "Body": Union[bytes, IO],
        "DeleteMarker": bool,
        "AcceptRanges": str,
        "Expiration": str,
        "Restore": str,
        "LastModified": datetime,
        "ContentLength": int,
        "ETag": str,
        "MissingMeta": int,
        "VersionId": str,
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentRange": str,
        "ContentType": str,
        "Expires": datetime,
        "WebsiteRedirectLocation": str,
        "ServerSideEncryption": Literal["AES256", "aws:kms"],
        "Metadata": Dict[str, str],
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "StorageClass": Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ],
        "RequestCharged": Literal["requester"],
        "ReplicationStatus": Literal["COMPLETE", "PENDING", "FAILED", "REPLICA"],
        "PartsCount": int,
        "TagCount": int,
        "ObjectLockMode": Literal["GOVERNANCE", "COMPLIANCE"],
        "ObjectLockRetainUntilDate": datetime,
        "ObjectLockLegalHoldStatus": Literal["ON", "OFF"],
    },
    total=False,
)

ObjectLockRetentionTypeDef = TypedDict(
    "ObjectLockRetentionTypeDef",
    {"Mode": Literal["GOVERNANCE", "COMPLIANCE"], "RetainUntilDate": datetime},
    total=False,
)

GetObjectRetentionOutputTypeDef = TypedDict(
    "GetObjectRetentionOutputTypeDef", {"Retention": ObjectLockRetentionTypeDef}, total=False
)

_RequiredGetObjectTaggingOutputTypeDef = TypedDict(
    "_RequiredGetObjectTaggingOutputTypeDef", {"TagSet": List[TagTypeDef]}
)
_OptionalGetObjectTaggingOutputTypeDef = TypedDict(
    "_OptionalGetObjectTaggingOutputTypeDef", {"VersionId": str}, total=False
)


class GetObjectTaggingOutputTypeDef(
    _RequiredGetObjectTaggingOutputTypeDef, _OptionalGetObjectTaggingOutputTypeDef
):
    pass


GetObjectTorrentOutputTypeDef = TypedDict(
    "GetObjectTorrentOutputTypeDef",
    {"Body": Union[bytes, IO], "RequestCharged": Literal["requester"]},
    total=False,
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

GetPublicAccessBlockOutputTypeDef = TypedDict(
    "GetPublicAccessBlockOutputTypeDef",
    {"PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef},
    total=False,
)

HeadObjectOutputTypeDef = TypedDict(
    "HeadObjectOutputTypeDef",
    {
        "DeleteMarker": bool,
        "AcceptRanges": str,
        "Expiration": str,
        "Restore": str,
        "LastModified": datetime,
        "ContentLength": int,
        "ETag": str,
        "MissingMeta": int,
        "VersionId": str,
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "ContentType": str,
        "Expires": datetime,
        "WebsiteRedirectLocation": str,
        "ServerSideEncryption": Literal["AES256", "aws:kms"],
        "Metadata": Dict[str, str],
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "StorageClass": Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ],
        "RequestCharged": Literal["requester"],
        "ReplicationStatus": Literal["COMPLETE", "PENDING", "FAILED", "REPLICA"],
        "PartsCount": int,
        "ObjectLockMode": Literal["GOVERNANCE", "COMPLIANCE"],
        "ObjectLockRetainUntilDate": datetime,
        "ObjectLockLegalHoldStatus": Literal["ON", "OFF"],
    },
    total=False,
)

CSVInputTypeDef = TypedDict(
    "CSVInputTypeDef",
    {
        "FileHeaderInfo": Literal["USE", "IGNORE", "NONE"],
        "Comments": str,
        "QuoteEscapeCharacter": str,
        "RecordDelimiter": str,
        "FieldDelimiter": str,
        "QuoteCharacter": str,
        "AllowQuotedRecordDelimiter": bool,
    },
    total=False,
)

JSONInputTypeDef = TypedDict(
    "JSONInputTypeDef", {"Type": Literal["DOCUMENT", "LINES"]}, total=False
)

InputSerializationTypeDef = TypedDict(
    "InputSerializationTypeDef",
    {
        "CSV": CSVInputTypeDef,
        "CompressionType": Literal["NONE", "GZIP", "BZIP2"],
        "JSON": JSONInputTypeDef,
        "Parquet": Dict[str, Any],
    },
    total=False,
)

LifecycleConfigurationTypeDef = TypedDict(
    "LifecycleConfigurationTypeDef", {"Rules": List[RuleTypeDef]}
)

ListBucketAnalyticsConfigurationsOutputTypeDef = TypedDict(
    "ListBucketAnalyticsConfigurationsOutputTypeDef",
    {
        "IsTruncated": bool,
        "ContinuationToken": str,
        "NextContinuationToken": str,
        "AnalyticsConfigurationList": List[AnalyticsConfigurationTypeDef],
    },
    total=False,
)

ListBucketInventoryConfigurationsOutputTypeDef = TypedDict(
    "ListBucketInventoryConfigurationsOutputTypeDef",
    {
        "ContinuationToken": str,
        "InventoryConfigurationList": List[InventoryConfigurationTypeDef],
        "IsTruncated": bool,
        "NextContinuationToken": str,
    },
    total=False,
)

ListBucketMetricsConfigurationsOutputTypeDef = TypedDict(
    "ListBucketMetricsConfigurationsOutputTypeDef",
    {
        "IsTruncated": bool,
        "ContinuationToken": str,
        "NextContinuationToken": str,
        "MetricsConfigurationList": List[MetricsConfigurationTypeDef],
    },
    total=False,
)

BucketTypeDef = TypedDict("BucketTypeDef", {"Name": str, "CreationDate": datetime}, total=False)

ListBucketsOutputTypeDef = TypedDict(
    "ListBucketsOutputTypeDef", {"Buckets": List[BucketTypeDef], "Owner": OwnerTypeDef}, total=False
)

CommonPrefixTypeDef = TypedDict("CommonPrefixTypeDef", {"Prefix": str}, total=False)

InitiatorTypeDef = TypedDict("InitiatorTypeDef", {"ID": str, "DisplayName": str}, total=False)

MultipartUploadTypeDef = TypedDict(
    "MultipartUploadTypeDef",
    {
        "UploadId": str,
        "Key": str,
        "Initiated": datetime,
        "StorageClass": Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ],
        "Owner": OwnerTypeDef,
        "Initiator": InitiatorTypeDef,
    },
    total=False,
)

ListMultipartUploadsOutputTypeDef = TypedDict(
    "ListMultipartUploadsOutputTypeDef",
    {
        "Bucket": str,
        "KeyMarker": str,
        "UploadIdMarker": str,
        "NextKeyMarker": str,
        "Prefix": str,
        "Delimiter": str,
        "NextUploadIdMarker": str,
        "MaxUploads": int,
        "IsTruncated": bool,
        "Uploads": List[MultipartUploadTypeDef],
        "CommonPrefixes": List[CommonPrefixTypeDef],
        "EncodingType": Literal["url"],
    },
    total=False,
)

DeleteMarkerEntryTypeDef = TypedDict(
    "DeleteMarkerEntryTypeDef",
    {
        "Owner": OwnerTypeDef,
        "Key": str,
        "VersionId": str,
        "IsLatest": bool,
        "LastModified": datetime,
    },
    total=False,
)

ObjectVersionTypeDef = TypedDict(
    "ObjectVersionTypeDef",
    {
        "ETag": str,
        "Size": int,
        "StorageClass": Literal["STANDARD"],
        "Key": str,
        "VersionId": str,
        "IsLatest": bool,
        "LastModified": datetime,
        "Owner": OwnerTypeDef,
    },
    total=False,
)

ListObjectVersionsOutputTypeDef = TypedDict(
    "ListObjectVersionsOutputTypeDef",
    {
        "IsTruncated": bool,
        "KeyMarker": str,
        "VersionIdMarker": str,
        "NextKeyMarker": str,
        "NextVersionIdMarker": str,
        "Versions": List[ObjectVersionTypeDef],
        "DeleteMarkers": List[DeleteMarkerEntryTypeDef],
        "Name": str,
        "Prefix": str,
        "Delimiter": str,
        "MaxKeys": int,
        "CommonPrefixes": List[CommonPrefixTypeDef],
        "EncodingType": Literal["url"],
    },
    total=False,
)

ObjectTypeDef = TypedDict(
    "ObjectTypeDef",
    {
        "Key": str,
        "LastModified": datetime,
        "ETag": str,
        "Size": int,
        "StorageClass": Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "GLACIER",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "DEEP_ARCHIVE",
        ],
        "Owner": OwnerTypeDef,
    },
    total=False,
)

ListObjectsOutputTypeDef = TypedDict(
    "ListObjectsOutputTypeDef",
    {
        "IsTruncated": bool,
        "Marker": str,
        "NextMarker": str,
        "Contents": List[ObjectTypeDef],
        "Name": str,
        "Prefix": str,
        "Delimiter": str,
        "MaxKeys": int,
        "CommonPrefixes": List[CommonPrefixTypeDef],
        "EncodingType": Literal["url"],
    },
    total=False,
)

ListObjectsV2OutputTypeDef = TypedDict(
    "ListObjectsV2OutputTypeDef",
    {
        "IsTruncated": bool,
        "Contents": List[ObjectTypeDef],
        "Name": str,
        "Prefix": str,
        "Delimiter": str,
        "MaxKeys": int,
        "CommonPrefixes": List[CommonPrefixTypeDef],
        "EncodingType": Literal["url"],
        "KeyCount": int,
        "ContinuationToken": str,
        "NextContinuationToken": str,
        "StartAfter": str,
    },
    total=False,
)

PartTypeDef = TypedDict(
    "PartTypeDef",
    {"PartNumber": int, "LastModified": datetime, "ETag": str, "Size": int},
    total=False,
)

ListPartsOutputTypeDef = TypedDict(
    "ListPartsOutputTypeDef",
    {
        "AbortDate": datetime,
        "AbortRuleId": str,
        "Bucket": str,
        "Key": str,
        "UploadId": str,
        "PartNumberMarker": int,
        "NextPartNumberMarker": int,
        "MaxParts": int,
        "IsTruncated": bool,
        "Parts": List[PartTypeDef],
        "Initiator": InitiatorTypeDef,
        "Owner": OwnerTypeDef,
        "StorageClass": Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ],
        "RequestCharged": Literal["requester"],
    },
    total=False,
)

CloudFunctionConfigurationTypeDef = TypedDict(
    "CloudFunctionConfigurationTypeDef",
    {
        "Id": str,
        "Event": Literal[
            "s3:ReducedRedundancyLostObject",
            "s3:ObjectCreated:*",
            "s3:ObjectCreated:Put",
            "s3:ObjectCreated:Post",
            "s3:ObjectCreated:Copy",
            "s3:ObjectCreated:CompleteMultipartUpload",
            "s3:ObjectRemoved:*",
            "s3:ObjectRemoved:Delete",
            "s3:ObjectRemoved:DeleteMarkerCreated",
            "s3:ObjectRestore:*",
            "s3:ObjectRestore:Post",
            "s3:ObjectRestore:Completed",
            "s3:Replication:*",
            "s3:Replication:OperationFailedReplication",
            "s3:Replication:OperationNotTracked",
            "s3:Replication:OperationMissedThreshold",
            "s3:Replication:OperationReplicatedAfterThreshold",
        ],
        "Events": List[
            Literal[
                "s3:ReducedRedundancyLostObject",
                "s3:ObjectCreated:*",
                "s3:ObjectCreated:Put",
                "s3:ObjectCreated:Post",
                "s3:ObjectCreated:Copy",
                "s3:ObjectCreated:CompleteMultipartUpload",
                "s3:ObjectRemoved:*",
                "s3:ObjectRemoved:Delete",
                "s3:ObjectRemoved:DeleteMarkerCreated",
                "s3:ObjectRestore:*",
                "s3:ObjectRestore:Post",
                "s3:ObjectRestore:Completed",
                "s3:Replication:*",
                "s3:Replication:OperationFailedReplication",
                "s3:Replication:OperationNotTracked",
                "s3:Replication:OperationMissedThreshold",
                "s3:Replication:OperationReplicatedAfterThreshold",
            ]
        ],
        "CloudFunction": str,
        "InvocationRole": str,
    },
    total=False,
)

QueueConfigurationDeprecatedTypeDef = TypedDict(
    "QueueConfigurationDeprecatedTypeDef",
    {
        "Id": str,
        "Event": Literal[
            "s3:ReducedRedundancyLostObject",
            "s3:ObjectCreated:*",
            "s3:ObjectCreated:Put",
            "s3:ObjectCreated:Post",
            "s3:ObjectCreated:Copy",
            "s3:ObjectCreated:CompleteMultipartUpload",
            "s3:ObjectRemoved:*",
            "s3:ObjectRemoved:Delete",
            "s3:ObjectRemoved:DeleteMarkerCreated",
            "s3:ObjectRestore:*",
            "s3:ObjectRestore:Post",
            "s3:ObjectRestore:Completed",
            "s3:Replication:*",
            "s3:Replication:OperationFailedReplication",
            "s3:Replication:OperationNotTracked",
            "s3:Replication:OperationMissedThreshold",
            "s3:Replication:OperationReplicatedAfterThreshold",
        ],
        "Events": List[
            Literal[
                "s3:ReducedRedundancyLostObject",
                "s3:ObjectCreated:*",
                "s3:ObjectCreated:Put",
                "s3:ObjectCreated:Post",
                "s3:ObjectCreated:Copy",
                "s3:ObjectCreated:CompleteMultipartUpload",
                "s3:ObjectRemoved:*",
                "s3:ObjectRemoved:Delete",
                "s3:ObjectRemoved:DeleteMarkerCreated",
                "s3:ObjectRestore:*",
                "s3:ObjectRestore:Post",
                "s3:ObjectRestore:Completed",
                "s3:Replication:*",
                "s3:Replication:OperationFailedReplication",
                "s3:Replication:OperationNotTracked",
                "s3:Replication:OperationMissedThreshold",
                "s3:Replication:OperationReplicatedAfterThreshold",
            ]
        ],
        "Queue": str,
    },
    total=False,
)

TopicConfigurationDeprecatedTypeDef = TypedDict(
    "TopicConfigurationDeprecatedTypeDef",
    {
        "Id": str,
        "Events": List[
            Literal[
                "s3:ReducedRedundancyLostObject",
                "s3:ObjectCreated:*",
                "s3:ObjectCreated:Put",
                "s3:ObjectCreated:Post",
                "s3:ObjectCreated:Copy",
                "s3:ObjectCreated:CompleteMultipartUpload",
                "s3:ObjectRemoved:*",
                "s3:ObjectRemoved:Delete",
                "s3:ObjectRemoved:DeleteMarkerCreated",
                "s3:ObjectRestore:*",
                "s3:ObjectRestore:Post",
                "s3:ObjectRestore:Completed",
                "s3:Replication:*",
                "s3:Replication:OperationFailedReplication",
                "s3:Replication:OperationNotTracked",
                "s3:Replication:OperationMissedThreshold",
                "s3:Replication:OperationReplicatedAfterThreshold",
            ]
        ],
        "Event": Literal[
            "s3:ReducedRedundancyLostObject",
            "s3:ObjectCreated:*",
            "s3:ObjectCreated:Put",
            "s3:ObjectCreated:Post",
            "s3:ObjectCreated:Copy",
            "s3:ObjectCreated:CompleteMultipartUpload",
            "s3:ObjectRemoved:*",
            "s3:ObjectRemoved:Delete",
            "s3:ObjectRemoved:DeleteMarkerCreated",
            "s3:ObjectRestore:*",
            "s3:ObjectRestore:Post",
            "s3:ObjectRestore:Completed",
            "s3:Replication:*",
            "s3:Replication:OperationFailedReplication",
            "s3:Replication:OperationNotTracked",
            "s3:Replication:OperationMissedThreshold",
            "s3:Replication:OperationReplicatedAfterThreshold",
        ],
        "Topic": str,
    },
    total=False,
)

NotificationConfigurationDeprecatedTypeDef = TypedDict(
    "NotificationConfigurationDeprecatedTypeDef",
    {
        "TopicConfiguration": TopicConfigurationDeprecatedTypeDef,
        "QueueConfiguration": QueueConfigurationDeprecatedTypeDef,
        "CloudFunctionConfiguration": CloudFunctionConfigurationTypeDef,
    },
    total=False,
)

FilterRuleTypeDef = TypedDict(
    "FilterRuleTypeDef", {"Name": Literal["prefix", "suffix"], "Value": str}, total=False
)

S3KeyFilterTypeDef = TypedDict(
    "S3KeyFilterTypeDef", {"FilterRules": List[FilterRuleTypeDef]}, total=False
)

NotificationConfigurationFilterTypeDef = TypedDict(
    "NotificationConfigurationFilterTypeDef", {"Key": S3KeyFilterTypeDef}, total=False
)

_RequiredLambdaFunctionConfigurationTypeDef = TypedDict(
    "_RequiredLambdaFunctionConfigurationTypeDef",
    {
        "LambdaFunctionArn": str,
        "Events": List[
            Literal[
                "s3:ReducedRedundancyLostObject",
                "s3:ObjectCreated:*",
                "s3:ObjectCreated:Put",
                "s3:ObjectCreated:Post",
                "s3:ObjectCreated:Copy",
                "s3:ObjectCreated:CompleteMultipartUpload",
                "s3:ObjectRemoved:*",
                "s3:ObjectRemoved:Delete",
                "s3:ObjectRemoved:DeleteMarkerCreated",
                "s3:ObjectRestore:*",
                "s3:ObjectRestore:Post",
                "s3:ObjectRestore:Completed",
                "s3:Replication:*",
                "s3:Replication:OperationFailedReplication",
                "s3:Replication:OperationNotTracked",
                "s3:Replication:OperationMissedThreshold",
                "s3:Replication:OperationReplicatedAfterThreshold",
            ]
        ],
    },
)
_OptionalLambdaFunctionConfigurationTypeDef = TypedDict(
    "_OptionalLambdaFunctionConfigurationTypeDef",
    {"Id": str, "Filter": NotificationConfigurationFilterTypeDef},
    total=False,
)


class LambdaFunctionConfigurationTypeDef(
    _RequiredLambdaFunctionConfigurationTypeDef, _OptionalLambdaFunctionConfigurationTypeDef
):
    pass


_RequiredQueueConfigurationTypeDef = TypedDict(
    "_RequiredQueueConfigurationTypeDef",
    {
        "QueueArn": str,
        "Events": List[
            Literal[
                "s3:ReducedRedundancyLostObject",
                "s3:ObjectCreated:*",
                "s3:ObjectCreated:Put",
                "s3:ObjectCreated:Post",
                "s3:ObjectCreated:Copy",
                "s3:ObjectCreated:CompleteMultipartUpload",
                "s3:ObjectRemoved:*",
                "s3:ObjectRemoved:Delete",
                "s3:ObjectRemoved:DeleteMarkerCreated",
                "s3:ObjectRestore:*",
                "s3:ObjectRestore:Post",
                "s3:ObjectRestore:Completed",
                "s3:Replication:*",
                "s3:Replication:OperationFailedReplication",
                "s3:Replication:OperationNotTracked",
                "s3:Replication:OperationMissedThreshold",
                "s3:Replication:OperationReplicatedAfterThreshold",
            ]
        ],
    },
)
_OptionalQueueConfigurationTypeDef = TypedDict(
    "_OptionalQueueConfigurationTypeDef",
    {"Id": str, "Filter": NotificationConfigurationFilterTypeDef},
    total=False,
)


class QueueConfigurationTypeDef(
    _RequiredQueueConfigurationTypeDef, _OptionalQueueConfigurationTypeDef
):
    pass


_RequiredTopicConfigurationTypeDef = TypedDict(
    "_RequiredTopicConfigurationTypeDef",
    {
        "TopicArn": str,
        "Events": List[
            Literal[
                "s3:ReducedRedundancyLostObject",
                "s3:ObjectCreated:*",
                "s3:ObjectCreated:Put",
                "s3:ObjectCreated:Post",
                "s3:ObjectCreated:Copy",
                "s3:ObjectCreated:CompleteMultipartUpload",
                "s3:ObjectRemoved:*",
                "s3:ObjectRemoved:Delete",
                "s3:ObjectRemoved:DeleteMarkerCreated",
                "s3:ObjectRestore:*",
                "s3:ObjectRestore:Post",
                "s3:ObjectRestore:Completed",
                "s3:Replication:*",
                "s3:Replication:OperationFailedReplication",
                "s3:Replication:OperationNotTracked",
                "s3:Replication:OperationMissedThreshold",
                "s3:Replication:OperationReplicatedAfterThreshold",
            ]
        ],
    },
)
_OptionalTopicConfigurationTypeDef = TypedDict(
    "_OptionalTopicConfigurationTypeDef",
    {"Id": str, "Filter": NotificationConfigurationFilterTypeDef},
    total=False,
)


class TopicConfigurationTypeDef(
    _RequiredTopicConfigurationTypeDef, _OptionalTopicConfigurationTypeDef
):
    pass


NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef",
    {
        "TopicConfigurations": List[TopicConfigurationTypeDef],
        "QueueConfigurations": List[QueueConfigurationTypeDef],
        "LambdaFunctionConfigurations": List[LambdaFunctionConfigurationTypeDef],
    },
    total=False,
)

CSVOutputTypeDef = TypedDict(
    "CSVOutputTypeDef",
    {
        "QuoteFields": Literal["ALWAYS", "ASNEEDED"],
        "QuoteEscapeCharacter": str,
        "RecordDelimiter": str,
        "FieldDelimiter": str,
        "QuoteCharacter": str,
    },
    total=False,
)

JSONOutputTypeDef = TypedDict("JSONOutputTypeDef", {"RecordDelimiter": str}, total=False)

OutputSerializationTypeDef = TypedDict(
    "OutputSerializationTypeDef", {"CSV": CSVOutputTypeDef, "JSON": JSONOutputTypeDef}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutObjectAclOutputTypeDef = TypedDict(
    "PutObjectAclOutputTypeDef", {"RequestCharged": Literal["requester"]}, total=False
)

PutObjectLegalHoldOutputTypeDef = TypedDict(
    "PutObjectLegalHoldOutputTypeDef", {"RequestCharged": Literal["requester"]}, total=False
)

PutObjectLockConfigurationOutputTypeDef = TypedDict(
    "PutObjectLockConfigurationOutputTypeDef", {"RequestCharged": Literal["requester"]}, total=False
)

PutObjectOutputTypeDef = TypedDict(
    "PutObjectOutputTypeDef",
    {
        "Expiration": str,
        "ETag": str,
        "ServerSideEncryption": Literal["AES256", "aws:kms"],
        "VersionId": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "SSEKMSEncryptionContext": str,
        "RequestCharged": Literal["requester"],
    },
    total=False,
)

PutObjectRetentionOutputTypeDef = TypedDict(
    "PutObjectRetentionOutputTypeDef", {"RequestCharged": Literal["requester"]}, total=False
)

PutObjectTaggingOutputTypeDef = TypedDict(
    "PutObjectTaggingOutputTypeDef", {"VersionId": str}, total=False
)

RequestPaymentConfigurationTypeDef = TypedDict(
    "RequestPaymentConfigurationTypeDef", {"Payer": Literal["Requester", "BucketOwner"]}
)

RequestProgressTypeDef = TypedDict("RequestProgressTypeDef", {"Enabled": bool}, total=False)

RestoreObjectOutputTypeDef = TypedDict(
    "RestoreObjectOutputTypeDef",
    {"RequestCharged": Literal["requester"], "RestoreOutputPath": str},
    total=False,
)

GlacierJobParametersTypeDef = TypedDict(
    "GlacierJobParametersTypeDef", {"Tier": Literal["Standard", "Bulk", "Expedited"]}
)

_RequiredEncryptionTypeDef = TypedDict(
    "_RequiredEncryptionTypeDef", {"EncryptionType": Literal["AES256", "aws:kms"]}
)
_OptionalEncryptionTypeDef = TypedDict(
    "_OptionalEncryptionTypeDef", {"KMSKeyId": str, "KMSContext": str}, total=False
)


class EncryptionTypeDef(_RequiredEncryptionTypeDef, _OptionalEncryptionTypeDef):
    pass


MetadataEntryTypeDef = TypedDict("MetadataEntryTypeDef", {"Name": str, "Value": str}, total=False)

TaggingTypeDef = TypedDict("TaggingTypeDef", {"TagSet": List[TagTypeDef]})

_RequiredS3LocationTypeDef = TypedDict(
    "_RequiredS3LocationTypeDef", {"BucketName": str, "Prefix": str}
)
_OptionalS3LocationTypeDef = TypedDict(
    "_OptionalS3LocationTypeDef",
    {
        "Encryption": EncryptionTypeDef,
        "CannedACL": Literal[
            "private",
            "public-read",
            "public-read-write",
            "authenticated-read",
            "aws-exec-read",
            "bucket-owner-read",
            "bucket-owner-full-control",
        ],
        "AccessControlList": List[GrantTypeDef],
        "Tagging": TaggingTypeDef,
        "UserMetadata": List[MetadataEntryTypeDef],
        "StorageClass": Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ],
    },
    total=False,
)


class S3LocationTypeDef(_RequiredS3LocationTypeDef, _OptionalS3LocationTypeDef):
    pass


OutputLocationTypeDef = TypedDict("OutputLocationTypeDef", {"S3": S3LocationTypeDef}, total=False)

SelectParametersTypeDef = TypedDict(
    "SelectParametersTypeDef",
    {
        "InputSerialization": InputSerializationTypeDef,
        "ExpressionType": Literal["SQL"],
        "Expression": str,
        "OutputSerialization": OutputSerializationTypeDef,
    },
)

RestoreRequestTypeDef = TypedDict(
    "RestoreRequestTypeDef",
    {
        "Days": int,
        "GlacierJobParameters": GlacierJobParametersTypeDef,
        "Type": Literal["SELECT"],
        "Tier": Literal["Standard", "Bulk", "Expedited"],
        "Description": str,
        "SelectParameters": SelectParametersTypeDef,
        "OutputLocation": OutputLocationTypeDef,
    },
    total=False,
)

ScanRangeTypeDef = TypedDict("ScanRangeTypeDef", {"Start": int, "End": int}, total=False)

ProgressTypeDef = TypedDict(
    "ProgressTypeDef",
    {"BytesScanned": int, "BytesProcessed": int, "BytesReturned": int},
    total=False,
)

ProgressEventTypeDef = TypedDict("ProgressEventTypeDef", {"Details": ProgressTypeDef}, total=False)

RecordsEventTypeDef = TypedDict("RecordsEventTypeDef", {"Payload": Union[bytes, IO]}, total=False)

StatsTypeDef = TypedDict(
    "StatsTypeDef", {"BytesScanned": int, "BytesProcessed": int, "BytesReturned": int}, total=False
)

StatsEventTypeDef = TypedDict("StatsEventTypeDef", {"Details": StatsTypeDef}, total=False)

SelectObjectContentEventStreamTypeDef = TypedDict(
    "SelectObjectContentEventStreamTypeDef",
    {
        "Records": RecordsEventTypeDef,
        "Stats": StatsEventTypeDef,
        "Progress": ProgressEventTypeDef,
        "Cont": Dict[str, Any],
        "End": Dict[str, Any],
    },
    total=False,
)

SelectObjectContentOutputTypeDef = TypedDict(
    "SelectObjectContentOutputTypeDef",
    {"Payload": SelectObjectContentEventStreamTypeDef},
    total=False,
)

CopyPartResultTypeDef = TypedDict(
    "CopyPartResultTypeDef", {"ETag": str, "LastModified": datetime}, total=False
)

UploadPartCopyOutputTypeDef = TypedDict(
    "UploadPartCopyOutputTypeDef",
    {
        "CopySourceVersionId": str,
        "CopyPartResult": CopyPartResultTypeDef,
        "ServerSideEncryption": Literal["AES256", "aws:kms"],
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "RequestCharged": Literal["requester"],
    },
    total=False,
)

UploadPartOutputTypeDef = TypedDict(
    "UploadPartOutputTypeDef",
    {
        "ServerSideEncryption": Literal["AES256", "aws:kms"],
        "ETag": str,
        "SSECustomerAlgorithm": str,
        "SSECustomerKeyMD5": str,
        "SSEKMSKeyId": str,
        "RequestCharged": Literal["requester"],
    },
    total=False,
)

VersioningConfigurationTypeDef = TypedDict(
    "VersioningConfigurationTypeDef",
    {"MFADelete": Literal["Enabled", "Disabled"], "Status": Literal["Enabled", "Suspended"]},
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)

WebsiteConfigurationTypeDef = TypedDict(
    "WebsiteConfigurationTypeDef",
    {
        "ErrorDocument": ErrorDocumentTypeDef,
        "IndexDocument": IndexDocumentTypeDef,
        "RedirectAllRequestsTo": RedirectAllRequestsToTypeDef,
        "RoutingRules": List[RoutingRuleTypeDef],
    },
    total=False,
)
