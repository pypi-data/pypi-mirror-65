"""
Main interface for dataexchange service type definitions.

Usage::

    from mypy_boto3.dataexchange.type_defs import OriginDetailsTypeDef

    data: OriginDetailsTypeDef = {...}
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
    "OriginDetailsTypeDef",
    "CreateDataSetResponseTypeDef",
    "AssetSourceEntryTypeDef",
    "ImportAssetFromSignedUrlJobErrorDetailsTypeDef",
    "DetailsTypeDef",
    "JobErrorTypeDef",
    "ExportAssetToSignedUrlResponseDetailsTypeDef",
    "AssetDestinationEntryTypeDef",
    "ExportAssetsToS3ResponseDetailsTypeDef",
    "ImportAssetFromSignedUrlResponseDetailsTypeDef",
    "ImportAssetsFromS3ResponseDetailsTypeDef",
    "ResponseDetailsTypeDef",
    "CreateJobResponseTypeDef",
    "CreateRevisionResponseTypeDef",
    "S3SnapshotAssetTypeDef",
    "AssetDetailsTypeDef",
    "GetAssetResponseTypeDef",
    "GetDataSetResponseTypeDef",
    "GetJobResponseTypeDef",
    "GetRevisionResponseTypeDef",
    "RevisionEntryTypeDef",
    "ListDataSetRevisionsResponseTypeDef",
    "DataSetEntryTypeDef",
    "ListDataSetsResponseTypeDef",
    "JobEntryTypeDef",
    "ListJobsResponseTypeDef",
    "AssetEntryTypeDef",
    "ListRevisionAssetsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ExportAssetToSignedUrlRequestDetailsTypeDef",
    "ExportAssetsToS3RequestDetailsTypeDef",
    "ImportAssetFromSignedUrlRequestDetailsTypeDef",
    "ImportAssetsFromS3RequestDetailsTypeDef",
    "RequestDetailsTypeDef",
    "UpdateAssetResponseTypeDef",
    "UpdateDataSetResponseTypeDef",
    "UpdateRevisionResponseTypeDef",
)

OriginDetailsTypeDef = TypedDict("OriginDetailsTypeDef", {"ProductId": str})

CreateDataSetResponseTypeDef = TypedDict(
    "CreateDataSetResponseTypeDef",
    {
        "Arn": str,
        "AssetType": Literal["S3_SNAPSHOT"],
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": Literal["OWNED", "ENTITLED"],
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
    },
    total=False,
)

AssetSourceEntryTypeDef = TypedDict("AssetSourceEntryTypeDef", {"Bucket": str, "Key": str})

ImportAssetFromSignedUrlJobErrorDetailsTypeDef = TypedDict(
    "ImportAssetFromSignedUrlJobErrorDetailsTypeDef", {"AssetName": str}
)

DetailsTypeDef = TypedDict(
    "DetailsTypeDef",
    {
        "ImportAssetFromSignedUrlJobErrorDetails": ImportAssetFromSignedUrlJobErrorDetailsTypeDef,
        "ImportAssetsFromS3JobErrorDetails": List[AssetSourceEntryTypeDef],
    },
    total=False,
)

_RequiredJobErrorTypeDef = TypedDict(
    "_RequiredJobErrorTypeDef",
    {
        "Code": Literal[
            "ACCESS_DENIED_EXCEPTION",
            "INTERNAL_SERVER_EXCEPTION",
            "MALWARE_DETECTED",
            "RESOURCE_NOT_FOUND_EXCEPTION",
            "SERVICE_QUOTA_EXCEEDED_EXCEPTION",
            "VALIDATION_EXCEPTION",
            "MALWARE_SCAN_ENCRYPTED_FILE",
        ],
        "Message": str,
    },
)
_OptionalJobErrorTypeDef = TypedDict(
    "_OptionalJobErrorTypeDef",
    {
        "Details": DetailsTypeDef,
        "LimitName": Literal["Assets per revision", "Asset size in GB"],
        "LimitValue": float,
        "ResourceId": str,
        "ResourceType": Literal["REVISION", "ASSET"],
    },
    total=False,
)


class JobErrorTypeDef(_RequiredJobErrorTypeDef, _OptionalJobErrorTypeDef):
    pass


_RequiredExportAssetToSignedUrlResponseDetailsTypeDef = TypedDict(
    "_RequiredExportAssetToSignedUrlResponseDetailsTypeDef",
    {"AssetId": str, "DataSetId": str, "RevisionId": str},
)
_OptionalExportAssetToSignedUrlResponseDetailsTypeDef = TypedDict(
    "_OptionalExportAssetToSignedUrlResponseDetailsTypeDef",
    {"SignedUrl": str, "SignedUrlExpiresAt": datetime},
    total=False,
)


class ExportAssetToSignedUrlResponseDetailsTypeDef(
    _RequiredExportAssetToSignedUrlResponseDetailsTypeDef,
    _OptionalExportAssetToSignedUrlResponseDetailsTypeDef,
):
    pass


_RequiredAssetDestinationEntryTypeDef = TypedDict(
    "_RequiredAssetDestinationEntryTypeDef", {"AssetId": str, "Bucket": str}
)
_OptionalAssetDestinationEntryTypeDef = TypedDict(
    "_OptionalAssetDestinationEntryTypeDef", {"Key": str}, total=False
)


class AssetDestinationEntryTypeDef(
    _RequiredAssetDestinationEntryTypeDef, _OptionalAssetDestinationEntryTypeDef
):
    pass


ExportAssetsToS3ResponseDetailsTypeDef = TypedDict(
    "ExportAssetsToS3ResponseDetailsTypeDef",
    {"AssetDestinations": List[AssetDestinationEntryTypeDef], "DataSetId": str, "RevisionId": str},
)

_RequiredImportAssetFromSignedUrlResponseDetailsTypeDef = TypedDict(
    "_RequiredImportAssetFromSignedUrlResponseDetailsTypeDef",
    {"AssetName": str, "DataSetId": str, "RevisionId": str},
)
_OptionalImportAssetFromSignedUrlResponseDetailsTypeDef = TypedDict(
    "_OptionalImportAssetFromSignedUrlResponseDetailsTypeDef",
    {"Md5Hash": str, "SignedUrl": str, "SignedUrlExpiresAt": datetime},
    total=False,
)


class ImportAssetFromSignedUrlResponseDetailsTypeDef(
    _RequiredImportAssetFromSignedUrlResponseDetailsTypeDef,
    _OptionalImportAssetFromSignedUrlResponseDetailsTypeDef,
):
    pass


ImportAssetsFromS3ResponseDetailsTypeDef = TypedDict(
    "ImportAssetsFromS3ResponseDetailsTypeDef",
    {"AssetSources": List[AssetSourceEntryTypeDef], "DataSetId": str, "RevisionId": str},
)

ResponseDetailsTypeDef = TypedDict(
    "ResponseDetailsTypeDef",
    {
        "ExportAssetToSignedUrl": ExportAssetToSignedUrlResponseDetailsTypeDef,
        "ExportAssetsToS3": ExportAssetsToS3ResponseDetailsTypeDef,
        "ImportAssetFromSignedUrl": ImportAssetFromSignedUrlResponseDetailsTypeDef,
        "ImportAssetsFromS3": ImportAssetsFromS3ResponseDetailsTypeDef,
    },
    total=False,
)

CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsTypeDef,
        "Errors": List[JobErrorTypeDef],
        "Id": str,
        "State": Literal["WAITING", "IN_PROGRESS", "ERROR", "COMPLETED", "CANCELLED", "TIMED_OUT"],
        "Type": Literal[
            "IMPORT_ASSETS_FROM_S3",
            "IMPORT_ASSET_FROM_SIGNED_URL",
            "EXPORT_ASSETS_TO_S3",
            "EXPORT_ASSET_TO_SIGNED_URL",
        ],
        "UpdatedAt": datetime,
    },
    total=False,
)

CreateRevisionResponseTypeDef = TypedDict(
    "CreateRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
    },
    total=False,
)

S3SnapshotAssetTypeDef = TypedDict("S3SnapshotAssetTypeDef", {"Size": float})

AssetDetailsTypeDef = TypedDict(
    "AssetDetailsTypeDef", {"S3SnapshotAsset": S3SnapshotAssetTypeDef}, total=False
)

GetAssetResponseTypeDef = TypedDict(
    "GetAssetResponseTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsTypeDef,
        "AssetType": Literal["S3_SNAPSHOT"],
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "SourceId": str,
        "UpdatedAt": datetime,
    },
    total=False,
)

GetDataSetResponseTypeDef = TypedDict(
    "GetDataSetResponseTypeDef",
    {
        "Arn": str,
        "AssetType": Literal["S3_SNAPSHOT"],
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": Literal["OWNED", "ENTITLED"],
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
    },
    total=False,
)

GetJobResponseTypeDef = TypedDict(
    "GetJobResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsTypeDef,
        "Errors": List[JobErrorTypeDef],
        "Id": str,
        "State": Literal["WAITING", "IN_PROGRESS", "ERROR", "COMPLETED", "CANCELLED", "TIMED_OUT"],
        "Type": Literal[
            "IMPORT_ASSETS_FROM_S3",
            "IMPORT_ASSET_FROM_SIGNED_URL",
            "EXPORT_ASSETS_TO_S3",
            "EXPORT_ASSET_TO_SIGNED_URL",
        ],
        "UpdatedAt": datetime,
    },
    total=False,
)

GetRevisionResponseTypeDef = TypedDict(
    "GetRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
    },
    total=False,
)

_RequiredRevisionEntryTypeDef = TypedDict(
    "_RequiredRevisionEntryTypeDef",
    {"Arn": str, "CreatedAt": datetime, "DataSetId": str, "Id": str, "UpdatedAt": datetime},
)
_OptionalRevisionEntryTypeDef = TypedDict(
    "_OptionalRevisionEntryTypeDef",
    {"Comment": str, "Finalized": bool, "SourceId": str},
    total=False,
)


class RevisionEntryTypeDef(_RequiredRevisionEntryTypeDef, _OptionalRevisionEntryTypeDef):
    pass


ListDataSetRevisionsResponseTypeDef = TypedDict(
    "ListDataSetRevisionsResponseTypeDef",
    {"NextToken": str, "Revisions": List[RevisionEntryTypeDef]},
    total=False,
)

_RequiredDataSetEntryTypeDef = TypedDict(
    "_RequiredDataSetEntryTypeDef",
    {
        "Arn": str,
        "AssetType": Literal["S3_SNAPSHOT"],
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": Literal["OWNED", "ENTITLED"],
        "UpdatedAt": datetime,
    },
)
_OptionalDataSetEntryTypeDef = TypedDict(
    "_OptionalDataSetEntryTypeDef",
    {"OriginDetails": OriginDetailsTypeDef, "SourceId": str},
    total=False,
)


class DataSetEntryTypeDef(_RequiredDataSetEntryTypeDef, _OptionalDataSetEntryTypeDef):
    pass


ListDataSetsResponseTypeDef = TypedDict(
    "ListDataSetsResponseTypeDef",
    {"DataSets": List[DataSetEntryTypeDef], "NextToken": str},
    total=False,
)

_RequiredJobEntryTypeDef = TypedDict(
    "_RequiredJobEntryTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsTypeDef,
        "Id": str,
        "State": Literal["WAITING", "IN_PROGRESS", "ERROR", "COMPLETED", "CANCELLED", "TIMED_OUT"],
        "Type": Literal[
            "IMPORT_ASSETS_FROM_S3",
            "IMPORT_ASSET_FROM_SIGNED_URL",
            "EXPORT_ASSETS_TO_S3",
            "EXPORT_ASSET_TO_SIGNED_URL",
        ],
        "UpdatedAt": datetime,
    },
)
_OptionalJobEntryTypeDef = TypedDict(
    "_OptionalJobEntryTypeDef", {"Errors": List[JobErrorTypeDef]}, total=False
)


class JobEntryTypeDef(_RequiredJobEntryTypeDef, _OptionalJobEntryTypeDef):
    pass


ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef", {"Jobs": List[JobEntryTypeDef], "NextToken": str}, total=False
)

_RequiredAssetEntryTypeDef = TypedDict(
    "_RequiredAssetEntryTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsTypeDef,
        "AssetType": Literal["S3_SNAPSHOT"],
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "UpdatedAt": datetime,
    },
)
_OptionalAssetEntryTypeDef = TypedDict("_OptionalAssetEntryTypeDef", {"SourceId": str}, total=False)


class AssetEntryTypeDef(_RequiredAssetEntryTypeDef, _OptionalAssetEntryTypeDef):
    pass


ListRevisionAssetsResponseTypeDef = TypedDict(
    "ListRevisionAssetsResponseTypeDef",
    {"Assets": List[AssetEntryTypeDef], "NextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

ExportAssetToSignedUrlRequestDetailsTypeDef = TypedDict(
    "ExportAssetToSignedUrlRequestDetailsTypeDef",
    {"AssetId": str, "DataSetId": str, "RevisionId": str},
)

ExportAssetsToS3RequestDetailsTypeDef = TypedDict(
    "ExportAssetsToS3RequestDetailsTypeDef",
    {"AssetDestinations": List[AssetDestinationEntryTypeDef], "DataSetId": str, "RevisionId": str},
)

ImportAssetFromSignedUrlRequestDetailsTypeDef = TypedDict(
    "ImportAssetFromSignedUrlRequestDetailsTypeDef",
    {"AssetName": str, "DataSetId": str, "Md5Hash": str, "RevisionId": str},
)

ImportAssetsFromS3RequestDetailsTypeDef = TypedDict(
    "ImportAssetsFromS3RequestDetailsTypeDef",
    {"AssetSources": List[AssetSourceEntryTypeDef], "DataSetId": str, "RevisionId": str},
)

RequestDetailsTypeDef = TypedDict(
    "RequestDetailsTypeDef",
    {
        "ExportAssetToSignedUrl": ExportAssetToSignedUrlRequestDetailsTypeDef,
        "ExportAssetsToS3": ExportAssetsToS3RequestDetailsTypeDef,
        "ImportAssetFromSignedUrl": ImportAssetFromSignedUrlRequestDetailsTypeDef,
        "ImportAssetsFromS3": ImportAssetsFromS3RequestDetailsTypeDef,
    },
    total=False,
)

UpdateAssetResponseTypeDef = TypedDict(
    "UpdateAssetResponseTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsTypeDef,
        "AssetType": Literal["S3_SNAPSHOT"],
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "SourceId": str,
        "UpdatedAt": datetime,
    },
    total=False,
)

UpdateDataSetResponseTypeDef = TypedDict(
    "UpdateDataSetResponseTypeDef",
    {
        "Arn": str,
        "AssetType": Literal["S3_SNAPSHOT"],
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": Literal["OWNED", "ENTITLED"],
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
        "UpdatedAt": datetime,
    },
    total=False,
)

UpdateRevisionResponseTypeDef = TypedDict(
    "UpdateRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "UpdatedAt": datetime,
    },
    total=False,
)
