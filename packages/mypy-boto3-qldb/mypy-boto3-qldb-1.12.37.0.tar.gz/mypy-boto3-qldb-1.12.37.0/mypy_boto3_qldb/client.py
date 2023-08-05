"""
Main interface for qldb service client

Usage::

    import boto3
    from mypy_boto3.qldb import QLDBClient

    session = boto3.Session()

    client: QLDBClient = boto3.client("qldb")
    session_client: QLDBClient = session.client("qldb")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from datetime import datetime
import sys
from typing import Any, Dict, List, TYPE_CHECKING, Type
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_qldb.type_defs import (
    CreateLedgerResponseTypeDef,
    DescribeJournalS3ExportResponseTypeDef,
    DescribeLedgerResponseTypeDef,
    ExportJournalToS3ResponseTypeDef,
    GetBlockResponseTypeDef,
    GetDigestResponseTypeDef,
    GetRevisionResponseTypeDef,
    ListJournalS3ExportsForLedgerResponseTypeDef,
    ListJournalS3ExportsResponseTypeDef,
    ListLedgersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    S3ExportConfigurationTypeDef,
    UpdateLedgerResponseTypeDef,
    ValueHolderTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("QLDBClient",)


class Exceptions:
    ClientError: Type[Boto3ClientError]
    InvalidParameterException: Type[Boto3ClientError]
    LimitExceededException: Type[Boto3ClientError]
    ResourceAlreadyExistsException: Type[Boto3ClientError]
    ResourceInUseException: Type[Boto3ClientError]
    ResourceNotFoundException: Type[Boto3ClientError]
    ResourcePreconditionNotMetException: Type[Boto3ClientError]


class QLDBClient:
    """
    [QLDB.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.can_paginate)
        """

    def create_ledger(
        self,
        Name: str,
        PermissionsMode: Literal["ALLOW_ALL"],
        Tags: Dict[str, str] = None,
        DeletionProtection: bool = None,
    ) -> CreateLedgerResponseTypeDef:
        """
        [Client.create_ledger documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.create_ledger)
        """

    def delete_ledger(self, Name: str) -> None:
        """
        [Client.delete_ledger documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.delete_ledger)
        """

    def describe_journal_s3_export(
        self, Name: str, ExportId: str
    ) -> DescribeJournalS3ExportResponseTypeDef:
        """
        [Client.describe_journal_s3_export documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.describe_journal_s3_export)
        """

    def describe_ledger(self, Name: str) -> DescribeLedgerResponseTypeDef:
        """
        [Client.describe_ledger documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.describe_ledger)
        """

    def export_journal_to_s3(
        self,
        Name: str,
        InclusiveStartTime: datetime,
        ExclusiveEndTime: datetime,
        S3ExportConfiguration: S3ExportConfigurationTypeDef,
        RoleArn: str,
    ) -> ExportJournalToS3ResponseTypeDef:
        """
        [Client.export_journal_to_s3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.export_journal_to_s3)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.generate_presigned_url)
        """

    def get_block(
        self,
        Name: str,
        BlockAddress: ValueHolderTypeDef,
        DigestTipAddress: ValueHolderTypeDef = None,
    ) -> GetBlockResponseTypeDef:
        """
        [Client.get_block documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.get_block)
        """

    def get_digest(self, Name: str) -> GetDigestResponseTypeDef:
        """
        [Client.get_digest documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.get_digest)
        """

    def get_revision(
        self,
        Name: str,
        BlockAddress: ValueHolderTypeDef,
        DocumentId: str,
        DigestTipAddress: ValueHolderTypeDef = None,
    ) -> GetRevisionResponseTypeDef:
        """
        [Client.get_revision documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.get_revision)
        """

    def list_journal_s3_exports(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListJournalS3ExportsResponseTypeDef:
        """
        [Client.list_journal_s3_exports documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.list_journal_s3_exports)
        """

    def list_journal_s3_exports_for_ledger(
        self, Name: str, MaxResults: int = None, NextToken: str = None
    ) -> ListJournalS3ExportsForLedgerResponseTypeDef:
        """
        [Client.list_journal_s3_exports_for_ledger documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.list_journal_s3_exports_for_ledger)
        """

    def list_ledgers(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListLedgersResponseTypeDef:
        """
        [Client.list_ledgers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.list_ledgers)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.list_tags_for_resource)
        """

    def tag_resource(self, ResourceArn: str, Tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.untag_resource)
        """

    def update_ledger(
        self, Name: str, DeletionProtection: bool = None
    ) -> UpdateLedgerResponseTypeDef:
        """
        [Client.update_ledger documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/qldb.html#QLDB.Client.update_ledger)
        """
