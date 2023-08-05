"""
Main interface for signer service type definitions.

Usage::

    from mypy_boto3.signer.type_defs import S3SignedObjectTypeDef

    data: S3SignedObjectTypeDef = {...}
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
    "S3SignedObjectTypeDef",
    "SignedObjectTypeDef",
    "SigningMaterialTypeDef",
    "SigningConfigurationOverridesTypeDef",
    "SigningPlatformOverridesTypeDef",
    "S3SourceTypeDef",
    "SourceTypeDef",
    "DescribeSigningJobResponseTypeDef",
    "S3DestinationTypeDef",
    "DestinationTypeDef",
    "EncryptionAlgorithmOptionsTypeDef",
    "HashAlgorithmOptionsTypeDef",
    "SigningConfigurationTypeDef",
    "SigningImageFormatTypeDef",
    "GetSigningPlatformResponseTypeDef",
    "GetSigningProfileResponseTypeDef",
    "SigningJobTypeDef",
    "ListSigningJobsResponseTypeDef",
    "SigningPlatformTypeDef",
    "ListSigningPlatformsResponseTypeDef",
    "SigningProfileTypeDef",
    "ListSigningProfilesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutSigningProfileResponseTypeDef",
    "StartSigningJobResponseTypeDef",
    "WaiterConfigTypeDef",
)

S3SignedObjectTypeDef = TypedDict(
    "S3SignedObjectTypeDef", {"bucketName": str, "key": str}, total=False
)

SignedObjectTypeDef = TypedDict("SignedObjectTypeDef", {"s3": S3SignedObjectTypeDef}, total=False)

SigningMaterialTypeDef = TypedDict("SigningMaterialTypeDef", {"certificateArn": str})

SigningConfigurationOverridesTypeDef = TypedDict(
    "SigningConfigurationOverridesTypeDef",
    {"encryptionAlgorithm": Literal["RSA", "ECDSA"], "hashAlgorithm": Literal["SHA1", "SHA256"]},
    total=False,
)

SigningPlatformOverridesTypeDef = TypedDict(
    "SigningPlatformOverridesTypeDef",
    {
        "signingConfiguration": SigningConfigurationOverridesTypeDef,
        "signingImageFormat": Literal["JSON", "JSONEmbedded", "JSONDetached"],
    },
    total=False,
)

S3SourceTypeDef = TypedDict("S3SourceTypeDef", {"bucketName": str, "key": str, "version": str})

SourceTypeDef = TypedDict("SourceTypeDef", {"s3": S3SourceTypeDef}, total=False)

DescribeSigningJobResponseTypeDef = TypedDict(
    "DescribeSigningJobResponseTypeDef",
    {
        "jobId": str,
        "source": SourceTypeDef,
        "signingMaterial": SigningMaterialTypeDef,
        "platformId": str,
        "profileName": str,
        "overrides": SigningPlatformOverridesTypeDef,
        "signingParameters": Dict[str, str],
        "createdAt": datetime,
        "completedAt": datetime,
        "requestedBy": str,
        "status": Literal["InProgress", "Failed", "Succeeded"],
        "statusReason": str,
        "signedObject": SignedObjectTypeDef,
    },
    total=False,
)

S3DestinationTypeDef = TypedDict(
    "S3DestinationTypeDef", {"bucketName": str, "prefix": str}, total=False
)

DestinationTypeDef = TypedDict("DestinationTypeDef", {"s3": S3DestinationTypeDef}, total=False)

EncryptionAlgorithmOptionsTypeDef = TypedDict(
    "EncryptionAlgorithmOptionsTypeDef",
    {"allowedValues": List[Literal["RSA", "ECDSA"]], "defaultValue": Literal["RSA", "ECDSA"]},
)

HashAlgorithmOptionsTypeDef = TypedDict(
    "HashAlgorithmOptionsTypeDef",
    {"allowedValues": List[Literal["SHA1", "SHA256"]], "defaultValue": Literal["SHA1", "SHA256"]},
)

SigningConfigurationTypeDef = TypedDict(
    "SigningConfigurationTypeDef",
    {
        "encryptionAlgorithmOptions": EncryptionAlgorithmOptionsTypeDef,
        "hashAlgorithmOptions": HashAlgorithmOptionsTypeDef,
    },
)

SigningImageFormatTypeDef = TypedDict(
    "SigningImageFormatTypeDef",
    {
        "supportedFormats": List[Literal["JSON", "JSONEmbedded", "JSONDetached"]],
        "defaultFormat": Literal["JSON", "JSONEmbedded", "JSONDetached"],
    },
)

GetSigningPlatformResponseTypeDef = TypedDict(
    "GetSigningPlatformResponseTypeDef",
    {
        "platformId": str,
        "displayName": str,
        "partner": str,
        "target": str,
        "category": Literal["AWSIoT"],
        "signingConfiguration": SigningConfigurationTypeDef,
        "signingImageFormat": SigningImageFormatTypeDef,
        "maxSizeInMB": int,
    },
    total=False,
)

GetSigningProfileResponseTypeDef = TypedDict(
    "GetSigningProfileResponseTypeDef",
    {
        "profileName": str,
        "signingMaterial": SigningMaterialTypeDef,
        "platformId": str,
        "overrides": SigningPlatformOverridesTypeDef,
        "signingParameters": Dict[str, str],
        "status": Literal["Active", "Canceled"],
        "arn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

SigningJobTypeDef = TypedDict(
    "SigningJobTypeDef",
    {
        "jobId": str,
        "source": SourceTypeDef,
        "signedObject": SignedObjectTypeDef,
        "signingMaterial": SigningMaterialTypeDef,
        "createdAt": datetime,
        "status": Literal["InProgress", "Failed", "Succeeded"],
    },
    total=False,
)

ListSigningJobsResponseTypeDef = TypedDict(
    "ListSigningJobsResponseTypeDef",
    {"jobs": List[SigningJobTypeDef], "nextToken": str},
    total=False,
)

SigningPlatformTypeDef = TypedDict(
    "SigningPlatformTypeDef",
    {
        "platformId": str,
        "displayName": str,
        "partner": str,
        "target": str,
        "category": Literal["AWSIoT"],
        "signingConfiguration": SigningConfigurationTypeDef,
        "signingImageFormat": SigningImageFormatTypeDef,
        "maxSizeInMB": int,
    },
    total=False,
)

ListSigningPlatformsResponseTypeDef = TypedDict(
    "ListSigningPlatformsResponseTypeDef",
    {"platforms": List[SigningPlatformTypeDef], "nextToken": str},
    total=False,
)

SigningProfileTypeDef = TypedDict(
    "SigningProfileTypeDef",
    {
        "profileName": str,
        "signingMaterial": SigningMaterialTypeDef,
        "platformId": str,
        "signingParameters": Dict[str, str],
        "status": Literal["Active", "Canceled"],
        "arn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

ListSigningProfilesResponseTypeDef = TypedDict(
    "ListSigningProfilesResponseTypeDef",
    {"profiles": List[SigningProfileTypeDef], "nextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": Dict[str, str]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutSigningProfileResponseTypeDef = TypedDict(
    "PutSigningProfileResponseTypeDef", {"arn": str}, total=False
)

StartSigningJobResponseTypeDef = TypedDict(
    "StartSigningJobResponseTypeDef", {"jobId": str}, total=False
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
