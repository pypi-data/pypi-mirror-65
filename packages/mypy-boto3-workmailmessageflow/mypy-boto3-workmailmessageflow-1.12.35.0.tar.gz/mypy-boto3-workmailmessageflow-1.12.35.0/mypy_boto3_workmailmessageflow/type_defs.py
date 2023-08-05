"""
Main interface for workmailmessageflow service type definitions.

Usage::

    from mypy_boto3.workmailmessageflow.type_defs import GetRawMessageContentResponseTypeDef

    data: GetRawMessageContentResponseTypeDef = {...}
"""
import sys
from typing import IO, Union

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = ("GetRawMessageContentResponseTypeDef",)

GetRawMessageContentResponseTypeDef = TypedDict(
    "GetRawMessageContentResponseTypeDef", {"messageContent": Union[bytes, IO]}
)
