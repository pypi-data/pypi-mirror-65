"""
Main interface for mediastore-data service type definitions.

Usage::

    from mypy_boto3.mediastore_data.type_defs import DescribeObjectResponseTypeDef

    data: DescribeObjectResponseTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DescribeObjectResponseTypeDef",
    "GetObjectResponseTypeDef",
    "ItemTypeDef",
    "ListItemsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutObjectResponseTypeDef",
)

DescribeObjectResponseTypeDef = TypedDict(
    "DescribeObjectResponseTypeDef",
    {
        "ETag": str,
        "ContentType": str,
        "ContentLength": int,
        "CacheControl": str,
        "LastModified": datetime,
    },
    total=False,
)

_RequiredGetObjectResponseTypeDef = TypedDict(
    "_RequiredGetObjectResponseTypeDef", {"StatusCode": int}
)
_OptionalGetObjectResponseTypeDef = TypedDict(
    "_OptionalGetObjectResponseTypeDef",
    {
        "Body": Union[bytes, IO],
        "CacheControl": str,
        "ContentRange": str,
        "ContentLength": int,
        "ContentType": str,
        "ETag": str,
        "LastModified": datetime,
    },
    total=False,
)


class GetObjectResponseTypeDef(
    _RequiredGetObjectResponseTypeDef, _OptionalGetObjectResponseTypeDef
):
    pass


ItemTypeDef = TypedDict(
    "ItemTypeDef",
    {
        "Name": str,
        "Type": Literal["OBJECT", "FOLDER"],
        "ETag": str,
        "LastModified": datetime,
        "ContentType": str,
        "ContentLength": int,
    },
    total=False,
)

ListItemsResponseTypeDef = TypedDict(
    "ListItemsResponseTypeDef", {"Items": List[ItemTypeDef], "NextToken": str}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutObjectResponseTypeDef = TypedDict(
    "PutObjectResponseTypeDef",
    {"ContentSHA256": str, "ETag": str, "StorageClass": Literal["TEMPORAL"]},
    total=False,
)
