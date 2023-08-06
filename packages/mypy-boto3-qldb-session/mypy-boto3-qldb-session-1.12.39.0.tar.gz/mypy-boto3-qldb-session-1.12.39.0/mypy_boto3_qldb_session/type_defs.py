"""
Main interface for qldb-session service type definitions.

Usage::

    from mypy_boto3.qldb_session.type_defs import CommitTransactionRequestTypeDef

    data: CommitTransactionRequestTypeDef = {...}
"""
import sys
from typing import Any, Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CommitTransactionRequestTypeDef",
    "ValueHolderTypeDef",
    "ExecuteStatementRequestTypeDef",
    "FetchPageRequestTypeDef",
    "CommitTransactionResultTypeDef",
    "PageTypeDef",
    "ExecuteStatementResultTypeDef",
    "FetchPageResultTypeDef",
    "StartSessionResultTypeDef",
    "StartTransactionResultTypeDef",
    "SendCommandResultTypeDef",
    "StartSessionRequestTypeDef",
)

CommitTransactionRequestTypeDef = TypedDict(
    "CommitTransactionRequestTypeDef", {"TransactionId": str, "CommitDigest": Union[bytes, IO]}
)

ValueHolderTypeDef = TypedDict(
    "ValueHolderTypeDef", {"IonBinary": Union[bytes, IO], "IonText": str}, total=False
)

_RequiredExecuteStatementRequestTypeDef = TypedDict(
    "_RequiredExecuteStatementRequestTypeDef", {"TransactionId": str, "Statement": str}
)
_OptionalExecuteStatementRequestTypeDef = TypedDict(
    "_OptionalExecuteStatementRequestTypeDef", {"Parameters": List[ValueHolderTypeDef]}, total=False
)


class ExecuteStatementRequestTypeDef(
    _RequiredExecuteStatementRequestTypeDef, _OptionalExecuteStatementRequestTypeDef
):
    pass


FetchPageRequestTypeDef = TypedDict(
    "FetchPageRequestTypeDef", {"TransactionId": str, "NextPageToken": str}
)

CommitTransactionResultTypeDef = TypedDict(
    "CommitTransactionResultTypeDef",
    {"TransactionId": str, "CommitDigest": Union[bytes, IO]},
    total=False,
)

PageTypeDef = TypedDict(
    "PageTypeDef", {"Values": List[ValueHolderTypeDef], "NextPageToken": str}, total=False
)

ExecuteStatementResultTypeDef = TypedDict(
    "ExecuteStatementResultTypeDef", {"FirstPage": PageTypeDef}, total=False
)

FetchPageResultTypeDef = TypedDict("FetchPageResultTypeDef", {"Page": PageTypeDef}, total=False)

StartSessionResultTypeDef = TypedDict(
    "StartSessionResultTypeDef", {"SessionToken": str}, total=False
)

StartTransactionResultTypeDef = TypedDict(
    "StartTransactionResultTypeDef", {"TransactionId": str}, total=False
)

SendCommandResultTypeDef = TypedDict(
    "SendCommandResultTypeDef",
    {
        "StartSession": StartSessionResultTypeDef,
        "StartTransaction": StartTransactionResultTypeDef,
        "EndSession": Dict[str, Any],
        "CommitTransaction": CommitTransactionResultTypeDef,
        "AbortTransaction": Dict[str, Any],
        "ExecuteStatement": ExecuteStatementResultTypeDef,
        "FetchPage": FetchPageResultTypeDef,
    },
    total=False,
)

StartSessionRequestTypeDef = TypedDict("StartSessionRequestTypeDef", {"LedgerName": str})
