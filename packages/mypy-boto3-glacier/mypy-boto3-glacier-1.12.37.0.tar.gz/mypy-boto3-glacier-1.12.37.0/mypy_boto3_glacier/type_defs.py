"""
Main interface for glacier service type definitions.

Usage::

    from mypy_boto3.glacier.type_defs import ArchiveCreationOutputTypeDef

    data: ArchiveCreationOutputTypeDef = {...}
"""
import sys
from typing import Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ArchiveCreationOutputTypeDef",
    "CreateVaultOutputTypeDef",
    "DataRetrievalRuleTypeDef",
    "DataRetrievalPolicyTypeDef",
    "DescribeVaultOutputTypeDef",
    "GetDataRetrievalPolicyOutputTypeDef",
    "GetJobOutputOutputTypeDef",
    "VaultAccessPolicyTypeDef",
    "GetVaultAccessPolicyOutputTypeDef",
    "GetVaultLockOutputTypeDef",
    "VaultNotificationConfigTypeDef",
    "GetVaultNotificationsOutputTypeDef",
    "InventoryRetrievalJobDescriptionTypeDef",
    "EncryptionTypeDef",
    "GranteeTypeDef",
    "GrantTypeDef",
    "S3LocationTypeDef",
    "OutputLocationTypeDef",
    "CSVInputTypeDef",
    "InputSerializationTypeDef",
    "CSVOutputTypeDef",
    "OutputSerializationTypeDef",
    "SelectParametersTypeDef",
    "GlacierJobDescriptionTypeDef",
    "InitiateJobOutputTypeDef",
    "InitiateMultipartUploadOutputTypeDef",
    "InitiateVaultLockOutputTypeDef",
    "InventoryRetrievalJobInputTypeDef",
    "JobParametersTypeDef",
    "ListJobsOutputTypeDef",
    "UploadListElementTypeDef",
    "ListMultipartUploadsOutputTypeDef",
    "PartListElementTypeDef",
    "ListPartsOutputTypeDef",
    "ProvisionedCapacityDescriptionTypeDef",
    "ListProvisionedCapacityOutputTypeDef",
    "ListTagsForVaultOutputTypeDef",
    "ListVaultsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PurchaseProvisionedCapacityOutputTypeDef",
    "UploadMultipartPartOutputTypeDef",
    "VaultLockPolicyTypeDef",
    "WaiterConfigTypeDef",
)

ArchiveCreationOutputTypeDef = TypedDict(
    "ArchiveCreationOutputTypeDef",
    {"location": str, "checksum": str, "archiveId": str},
    total=False,
)

CreateVaultOutputTypeDef = TypedDict("CreateVaultOutputTypeDef", {"location": str}, total=False)

DataRetrievalRuleTypeDef = TypedDict(
    "DataRetrievalRuleTypeDef", {"Strategy": str, "BytesPerHour": int}, total=False
)

DataRetrievalPolicyTypeDef = TypedDict(
    "DataRetrievalPolicyTypeDef", {"Rules": List[DataRetrievalRuleTypeDef]}, total=False
)

DescribeVaultOutputTypeDef = TypedDict(
    "DescribeVaultOutputTypeDef",
    {
        "VaultARN": str,
        "VaultName": str,
        "CreationDate": str,
        "LastInventoryDate": str,
        "NumberOfArchives": int,
        "SizeInBytes": int,
    },
    total=False,
)

GetDataRetrievalPolicyOutputTypeDef = TypedDict(
    "GetDataRetrievalPolicyOutputTypeDef", {"Policy": DataRetrievalPolicyTypeDef}, total=False
)

GetJobOutputOutputTypeDef = TypedDict(
    "GetJobOutputOutputTypeDef",
    {
        "body": Union[bytes, IO],
        "checksum": str,
        "status": int,
        "contentRange": str,
        "acceptRanges": str,
        "contentType": str,
        "archiveDescription": str,
    },
    total=False,
)

VaultAccessPolicyTypeDef = TypedDict("VaultAccessPolicyTypeDef", {"Policy": str}, total=False)

GetVaultAccessPolicyOutputTypeDef = TypedDict(
    "GetVaultAccessPolicyOutputTypeDef", {"policy": VaultAccessPolicyTypeDef}, total=False
)

GetVaultLockOutputTypeDef = TypedDict(
    "GetVaultLockOutputTypeDef",
    {"Policy": str, "State": str, "ExpirationDate": str, "CreationDate": str},
    total=False,
)

VaultNotificationConfigTypeDef = TypedDict(
    "VaultNotificationConfigTypeDef", {"SNSTopic": str, "Events": List[str]}, total=False
)

GetVaultNotificationsOutputTypeDef = TypedDict(
    "GetVaultNotificationsOutputTypeDef",
    {"vaultNotificationConfig": VaultNotificationConfigTypeDef},
    total=False,
)

InventoryRetrievalJobDescriptionTypeDef = TypedDict(
    "InventoryRetrievalJobDescriptionTypeDef",
    {"Format": str, "StartDate": str, "EndDate": str, "Limit": str, "Marker": str},
    total=False,
)

EncryptionTypeDef = TypedDict(
    "EncryptionTypeDef",
    {"EncryptionType": Literal["aws:kms", "AES256"], "KMSKeyId": str, "KMSContext": str},
    total=False,
)

_RequiredGranteeTypeDef = TypedDict(
    "_RequiredGranteeTypeDef", {"Type": Literal["AmazonCustomerByEmail", "CanonicalUser", "Group"]}
)
_OptionalGranteeTypeDef = TypedDict(
    "_OptionalGranteeTypeDef",
    {"DisplayName": str, "URI": str, "ID": str, "EmailAddress": str},
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

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "BucketName": str,
        "Prefix": str,
        "Encryption": EncryptionTypeDef,
        "CannedACL": Literal[
            "private",
            "public-read",
            "public-read-write",
            "aws-exec-read",
            "authenticated-read",
            "bucket-owner-read",
            "bucket-owner-full-control",
        ],
        "AccessControlList": List[GrantTypeDef],
        "Tagging": Dict[str, str],
        "UserMetadata": Dict[str, str],
        "StorageClass": Literal["STANDARD", "REDUCED_REDUNDANCY", "STANDARD_IA"],
    },
    total=False,
)

OutputLocationTypeDef = TypedDict("OutputLocationTypeDef", {"S3": S3LocationTypeDef}, total=False)

CSVInputTypeDef = TypedDict(
    "CSVInputTypeDef",
    {
        "FileHeaderInfo": Literal["USE", "IGNORE", "NONE"],
        "Comments": str,
        "QuoteEscapeCharacter": str,
        "RecordDelimiter": str,
        "FieldDelimiter": str,
        "QuoteCharacter": str,
    },
    total=False,
)

InputSerializationTypeDef = TypedDict(
    "InputSerializationTypeDef", {"csv": CSVInputTypeDef}, total=False
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

OutputSerializationTypeDef = TypedDict(
    "OutputSerializationTypeDef", {"csv": CSVOutputTypeDef}, total=False
)

SelectParametersTypeDef = TypedDict(
    "SelectParametersTypeDef",
    {
        "InputSerialization": InputSerializationTypeDef,
        "ExpressionType": Literal["SQL"],
        "Expression": str,
        "OutputSerialization": OutputSerializationTypeDef,
    },
    total=False,
)

GlacierJobDescriptionTypeDef = TypedDict(
    "GlacierJobDescriptionTypeDef",
    {
        "JobId": str,
        "JobDescription": str,
        "Action": Literal["ArchiveRetrieval", "InventoryRetrieval", "Select"],
        "ArchiveId": str,
        "VaultARN": str,
        "CreationDate": str,
        "Completed": bool,
        "StatusCode": Literal["InProgress", "Succeeded", "Failed"],
        "StatusMessage": str,
        "ArchiveSizeInBytes": int,
        "InventorySizeInBytes": int,
        "SNSTopic": str,
        "CompletionDate": str,
        "SHA256TreeHash": str,
        "ArchiveSHA256TreeHash": str,
        "RetrievalByteRange": str,
        "Tier": str,
        "InventoryRetrievalParameters": InventoryRetrievalJobDescriptionTypeDef,
        "JobOutputPath": str,
        "SelectParameters": SelectParametersTypeDef,
        "OutputLocation": OutputLocationTypeDef,
    },
    total=False,
)

InitiateJobOutputTypeDef = TypedDict(
    "InitiateJobOutputTypeDef", {"location": str, "jobId": str, "jobOutputPath": str}, total=False
)

InitiateMultipartUploadOutputTypeDef = TypedDict(
    "InitiateMultipartUploadOutputTypeDef", {"location": str, "uploadId": str}, total=False
)

InitiateVaultLockOutputTypeDef = TypedDict(
    "InitiateVaultLockOutputTypeDef", {"lockId": str}, total=False
)

InventoryRetrievalJobInputTypeDef = TypedDict(
    "InventoryRetrievalJobInputTypeDef",
    {"StartDate": str, "EndDate": str, "Limit": str, "Marker": str},
    total=False,
)

JobParametersTypeDef = TypedDict(
    "JobParametersTypeDef",
    {
        "Format": str,
        "Type": str,
        "ArchiveId": str,
        "Description": str,
        "SNSTopic": str,
        "RetrievalByteRange": str,
        "Tier": str,
        "InventoryRetrievalParameters": InventoryRetrievalJobInputTypeDef,
        "SelectParameters": SelectParametersTypeDef,
        "OutputLocation": OutputLocationTypeDef,
    },
    total=False,
)

ListJobsOutputTypeDef = TypedDict(
    "ListJobsOutputTypeDef",
    {"JobList": List[GlacierJobDescriptionTypeDef], "Marker": str},
    total=False,
)

UploadListElementTypeDef = TypedDict(
    "UploadListElementTypeDef",
    {
        "MultipartUploadId": str,
        "VaultARN": str,
        "ArchiveDescription": str,
        "PartSizeInBytes": int,
        "CreationDate": str,
    },
    total=False,
)

ListMultipartUploadsOutputTypeDef = TypedDict(
    "ListMultipartUploadsOutputTypeDef",
    {"UploadsList": List[UploadListElementTypeDef], "Marker": str},
    total=False,
)

PartListElementTypeDef = TypedDict(
    "PartListElementTypeDef", {"RangeInBytes": str, "SHA256TreeHash": str}, total=False
)

ListPartsOutputTypeDef = TypedDict(
    "ListPartsOutputTypeDef",
    {
        "MultipartUploadId": str,
        "VaultARN": str,
        "ArchiveDescription": str,
        "PartSizeInBytes": int,
        "CreationDate": str,
        "Parts": List[PartListElementTypeDef],
        "Marker": str,
    },
    total=False,
)

ProvisionedCapacityDescriptionTypeDef = TypedDict(
    "ProvisionedCapacityDescriptionTypeDef",
    {"CapacityId": str, "StartDate": str, "ExpirationDate": str},
    total=False,
)

ListProvisionedCapacityOutputTypeDef = TypedDict(
    "ListProvisionedCapacityOutputTypeDef",
    {"ProvisionedCapacityList": List[ProvisionedCapacityDescriptionTypeDef]},
    total=False,
)

ListTagsForVaultOutputTypeDef = TypedDict(
    "ListTagsForVaultOutputTypeDef", {"Tags": Dict[str, str]}, total=False
)

ListVaultsOutputTypeDef = TypedDict(
    "ListVaultsOutputTypeDef",
    {"VaultList": List[DescribeVaultOutputTypeDef], "Marker": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PurchaseProvisionedCapacityOutputTypeDef = TypedDict(
    "PurchaseProvisionedCapacityOutputTypeDef", {"capacityId": str}, total=False
)

UploadMultipartPartOutputTypeDef = TypedDict(
    "UploadMultipartPartOutputTypeDef", {"checksum": str}, total=False
)

VaultLockPolicyTypeDef = TypedDict("VaultLockPolicyTypeDef", {"Policy": str}, total=False)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
