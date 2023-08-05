"""
Main interface for qldb service type definitions.

Usage::

    from mypy_boto3.qldb.type_defs import CreateLedgerResponseTypeDef

    data: CreateLedgerResponseTypeDef = {...}
"""
from datetime import datetime
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
    "CreateLedgerResponseTypeDef",
    "S3EncryptionConfigurationTypeDef",
    "S3ExportConfigurationTypeDef",
    "JournalS3ExportDescriptionTypeDef",
    "DescribeJournalS3ExportResponseTypeDef",
    "DescribeLedgerResponseTypeDef",
    "ExportJournalToS3ResponseTypeDef",
    "ValueHolderTypeDef",
    "GetBlockResponseTypeDef",
    "GetDigestResponseTypeDef",
    "GetRevisionResponseTypeDef",
    "ListJournalS3ExportsForLedgerResponseTypeDef",
    "ListJournalS3ExportsResponseTypeDef",
    "LedgerSummaryTypeDef",
    "ListLedgersResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateLedgerResponseTypeDef",
)

CreateLedgerResponseTypeDef = TypedDict(
    "CreateLedgerResponseTypeDef",
    {
        "Name": str,
        "Arn": str,
        "State": Literal["CREATING", "ACTIVE", "DELETING", "DELETED"],
        "CreationDateTime": datetime,
        "DeletionProtection": bool,
    },
    total=False,
)

_RequiredS3EncryptionConfigurationTypeDef = TypedDict(
    "_RequiredS3EncryptionConfigurationTypeDef",
    {"ObjectEncryptionType": Literal["SSE_KMS", "SSE_S3", "NO_ENCRYPTION"]},
)
_OptionalS3EncryptionConfigurationTypeDef = TypedDict(
    "_OptionalS3EncryptionConfigurationTypeDef", {"KmsKeyArn": str}, total=False
)


class S3EncryptionConfigurationTypeDef(
    _RequiredS3EncryptionConfigurationTypeDef, _OptionalS3EncryptionConfigurationTypeDef
):
    pass


S3ExportConfigurationTypeDef = TypedDict(
    "S3ExportConfigurationTypeDef",
    {"Bucket": str, "Prefix": str, "EncryptionConfiguration": S3EncryptionConfigurationTypeDef},
)

JournalS3ExportDescriptionTypeDef = TypedDict(
    "JournalS3ExportDescriptionTypeDef",
    {
        "LedgerName": str,
        "ExportId": str,
        "ExportCreationTime": datetime,
        "Status": Literal["IN_PROGRESS", "COMPLETED", "CANCELLED"],
        "InclusiveStartTime": datetime,
        "ExclusiveEndTime": datetime,
        "S3ExportConfiguration": S3ExportConfigurationTypeDef,
        "RoleArn": str,
    },
)

DescribeJournalS3ExportResponseTypeDef = TypedDict(
    "DescribeJournalS3ExportResponseTypeDef",
    {"ExportDescription": JournalS3ExportDescriptionTypeDef},
)

DescribeLedgerResponseTypeDef = TypedDict(
    "DescribeLedgerResponseTypeDef",
    {
        "Name": str,
        "Arn": str,
        "State": Literal["CREATING", "ACTIVE", "DELETING", "DELETED"],
        "CreationDateTime": datetime,
        "DeletionProtection": bool,
    },
    total=False,
)

ExportJournalToS3ResponseTypeDef = TypedDict("ExportJournalToS3ResponseTypeDef", {"ExportId": str})

ValueHolderTypeDef = TypedDict("ValueHolderTypeDef", {"IonText": str}, total=False)

_RequiredGetBlockResponseTypeDef = TypedDict(
    "_RequiredGetBlockResponseTypeDef", {"Block": ValueHolderTypeDef}
)
_OptionalGetBlockResponseTypeDef = TypedDict(
    "_OptionalGetBlockResponseTypeDef", {"Proof": ValueHolderTypeDef}, total=False
)


class GetBlockResponseTypeDef(_RequiredGetBlockResponseTypeDef, _OptionalGetBlockResponseTypeDef):
    pass


GetDigestResponseTypeDef = TypedDict(
    "GetDigestResponseTypeDef", {"Digest": Union[bytes, IO], "DigestTipAddress": ValueHolderTypeDef}
)

_RequiredGetRevisionResponseTypeDef = TypedDict(
    "_RequiredGetRevisionResponseTypeDef", {"Revision": ValueHolderTypeDef}
)
_OptionalGetRevisionResponseTypeDef = TypedDict(
    "_OptionalGetRevisionResponseTypeDef", {"Proof": ValueHolderTypeDef}, total=False
)


class GetRevisionResponseTypeDef(
    _RequiredGetRevisionResponseTypeDef, _OptionalGetRevisionResponseTypeDef
):
    pass


ListJournalS3ExportsForLedgerResponseTypeDef = TypedDict(
    "ListJournalS3ExportsForLedgerResponseTypeDef",
    {"JournalS3Exports": List[JournalS3ExportDescriptionTypeDef], "NextToken": str},
    total=False,
)

ListJournalS3ExportsResponseTypeDef = TypedDict(
    "ListJournalS3ExportsResponseTypeDef",
    {"JournalS3Exports": List[JournalS3ExportDescriptionTypeDef], "NextToken": str},
    total=False,
)

LedgerSummaryTypeDef = TypedDict(
    "LedgerSummaryTypeDef",
    {
        "Name": str,
        "State": Literal["CREATING", "ACTIVE", "DELETING", "DELETED"],
        "CreationDateTime": datetime,
    },
    total=False,
)

ListLedgersResponseTypeDef = TypedDict(
    "ListLedgersResponseTypeDef",
    {"Ledgers": List[LedgerSummaryTypeDef], "NextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

UpdateLedgerResponseTypeDef = TypedDict(
    "UpdateLedgerResponseTypeDef",
    {
        "Name": str,
        "Arn": str,
        "State": Literal["CREATING", "ACTIVE", "DELETING", "DELETED"],
        "CreationDateTime": datetime,
        "DeletionProtection": bool,
    },
    total=False,
)
