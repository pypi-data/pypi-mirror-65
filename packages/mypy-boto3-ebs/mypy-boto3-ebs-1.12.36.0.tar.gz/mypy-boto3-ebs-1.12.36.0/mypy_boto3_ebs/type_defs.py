"""
Main interface for ebs service type definitions.

Usage::

    from mypy_boto3.ebs.type_defs import GetSnapshotBlockResponseTypeDef

    data: GetSnapshotBlockResponseTypeDef = {...}
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
    "GetSnapshotBlockResponseTypeDef",
    "ChangedBlockTypeDef",
    "ListChangedBlocksResponseTypeDef",
    "BlockTypeDef",
    "ListSnapshotBlocksResponseTypeDef",
)

GetSnapshotBlockResponseTypeDef = TypedDict(
    "GetSnapshotBlockResponseTypeDef",
    {
        "DataLength": int,
        "BlockData": Union[bytes, IO],
        "Checksum": str,
        "ChecksumAlgorithm": Literal["SHA256"],
    },
    total=False,
)

ChangedBlockTypeDef = TypedDict(
    "ChangedBlockTypeDef",
    {"BlockIndex": int, "FirstBlockToken": str, "SecondBlockToken": str},
    total=False,
)

ListChangedBlocksResponseTypeDef = TypedDict(
    "ListChangedBlocksResponseTypeDef",
    {
        "ChangedBlocks": List[ChangedBlockTypeDef],
        "ExpiryTime": datetime,
        "VolumeSize": int,
        "BlockSize": int,
        "NextToken": str,
    },
    total=False,
)

BlockTypeDef = TypedDict("BlockTypeDef", {"BlockIndex": int, "BlockToken": str}, total=False)

ListSnapshotBlocksResponseTypeDef = TypedDict(
    "ListSnapshotBlocksResponseTypeDef",
    {
        "Blocks": List[BlockTypeDef],
        "ExpiryTime": datetime,
        "VolumeSize": int,
        "BlockSize": int,
        "NextToken": str,
    },
    total=False,
)
