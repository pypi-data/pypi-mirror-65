"""
Main interface for macie service type definitions.

Usage::

    from mypy_boto3.macie.type_defs import S3ResourceTypeDef

    data: S3ResourceTypeDef = {...}
"""
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "S3ResourceTypeDef",
    "FailedS3ResourceTypeDef",
    "AssociateS3ResourcesResultTypeDef",
    "DisassociateS3ResourcesResultTypeDef",
    "MemberAccountTypeDef",
    "ListMemberAccountsResultTypeDef",
    "ClassificationTypeTypeDef",
    "S3ResourceClassificationTypeDef",
    "ListS3ResourcesResultTypeDef",
    "PaginatorConfigTypeDef",
    "ClassificationTypeUpdateTypeDef",
    "S3ResourceClassificationUpdateTypeDef",
    "UpdateS3ResourcesResultTypeDef",
)

_RequiredS3ResourceTypeDef = TypedDict("_RequiredS3ResourceTypeDef", {"bucketName": str})
_OptionalS3ResourceTypeDef = TypedDict("_OptionalS3ResourceTypeDef", {"prefix": str}, total=False)


class S3ResourceTypeDef(_RequiredS3ResourceTypeDef, _OptionalS3ResourceTypeDef):
    pass


FailedS3ResourceTypeDef = TypedDict(
    "FailedS3ResourceTypeDef",
    {"failedItem": S3ResourceTypeDef, "errorCode": str, "errorMessage": str},
    total=False,
)

AssociateS3ResourcesResultTypeDef = TypedDict(
    "AssociateS3ResourcesResultTypeDef",
    {"failedS3Resources": List[FailedS3ResourceTypeDef]},
    total=False,
)

DisassociateS3ResourcesResultTypeDef = TypedDict(
    "DisassociateS3ResourcesResultTypeDef",
    {"failedS3Resources": List[FailedS3ResourceTypeDef]},
    total=False,
)

MemberAccountTypeDef = TypedDict("MemberAccountTypeDef", {"accountId": str}, total=False)

ListMemberAccountsResultTypeDef = TypedDict(
    "ListMemberAccountsResultTypeDef",
    {"memberAccounts": List[MemberAccountTypeDef], "nextToken": str},
    total=False,
)

ClassificationTypeTypeDef = TypedDict(
    "ClassificationTypeTypeDef", {"oneTime": Literal["FULL", "NONE"], "continuous": Literal["FULL"]}
)

_RequiredS3ResourceClassificationTypeDef = TypedDict(
    "_RequiredS3ResourceClassificationTypeDef",
    {"bucketName": str, "classificationType": ClassificationTypeTypeDef},
)
_OptionalS3ResourceClassificationTypeDef = TypedDict(
    "_OptionalS3ResourceClassificationTypeDef", {"prefix": str}, total=False
)


class S3ResourceClassificationTypeDef(
    _RequiredS3ResourceClassificationTypeDef, _OptionalS3ResourceClassificationTypeDef
):
    pass


ListS3ResourcesResultTypeDef = TypedDict(
    "ListS3ResourcesResultTypeDef",
    {"s3Resources": List[S3ResourceClassificationTypeDef], "nextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

ClassificationTypeUpdateTypeDef = TypedDict(
    "ClassificationTypeUpdateTypeDef",
    {"oneTime": Literal["FULL", "NONE"], "continuous": Literal["FULL"]},
    total=False,
)

_RequiredS3ResourceClassificationUpdateTypeDef = TypedDict(
    "_RequiredS3ResourceClassificationUpdateTypeDef",
    {"bucketName": str, "classificationTypeUpdate": ClassificationTypeUpdateTypeDef},
)
_OptionalS3ResourceClassificationUpdateTypeDef = TypedDict(
    "_OptionalS3ResourceClassificationUpdateTypeDef", {"prefix": str}, total=False
)


class S3ResourceClassificationUpdateTypeDef(
    _RequiredS3ResourceClassificationUpdateTypeDef, _OptionalS3ResourceClassificationUpdateTypeDef
):
    pass


UpdateS3ResourcesResultTypeDef = TypedDict(
    "UpdateS3ResourcesResultTypeDef",
    {"failedS3Resources": List[FailedS3ResourceTypeDef]},
    total=False,
)
