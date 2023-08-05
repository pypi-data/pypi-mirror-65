"""
Main interface for iot-data service type definitions.

Usage::

    from mypy_boto3.iot_data.type_defs import DeleteThingShadowResponseTypeDef

    data: DeleteThingShadowResponseTypeDef = {...}
"""
import sys
from typing import IO, Union

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DeleteThingShadowResponseTypeDef",
    "GetThingShadowResponseTypeDef",
    "UpdateThingShadowResponseTypeDef",
)

DeleteThingShadowResponseTypeDef = TypedDict(
    "DeleteThingShadowResponseTypeDef", {"payload": Union[bytes, IO]}
)

GetThingShadowResponseTypeDef = TypedDict(
    "GetThingShadowResponseTypeDef", {"payload": Union[bytes, IO]}, total=False
)

UpdateThingShadowResponseTypeDef = TypedDict(
    "UpdateThingShadowResponseTypeDef", {"payload": Union[bytes, IO]}, total=False
)
