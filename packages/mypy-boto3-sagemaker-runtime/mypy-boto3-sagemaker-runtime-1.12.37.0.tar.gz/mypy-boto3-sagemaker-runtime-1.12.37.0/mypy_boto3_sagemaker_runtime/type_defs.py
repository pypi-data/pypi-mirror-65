"""
Main interface for sagemaker-runtime service type definitions.

Usage::

    from mypy_boto3.sagemaker_runtime.type_defs import InvokeEndpointOutputTypeDef

    data: InvokeEndpointOutputTypeDef = {...}
"""
import sys
from typing import IO, Union

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = ("InvokeEndpointOutputTypeDef",)

_RequiredInvokeEndpointOutputTypeDef = TypedDict(
    "_RequiredInvokeEndpointOutputTypeDef", {"Body": Union[bytes, IO]}
)
_OptionalInvokeEndpointOutputTypeDef = TypedDict(
    "_OptionalInvokeEndpointOutputTypeDef",
    {"ContentType": str, "InvokedProductionVariant": str, "CustomAttributes": str},
    total=False,
)


class InvokeEndpointOutputTypeDef(
    _RequiredInvokeEndpointOutputTypeDef, _OptionalInvokeEndpointOutputTypeDef
):
    pass
