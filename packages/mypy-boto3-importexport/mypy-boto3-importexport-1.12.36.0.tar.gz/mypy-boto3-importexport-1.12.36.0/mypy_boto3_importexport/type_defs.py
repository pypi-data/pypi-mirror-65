"""
Main interface for importexport service type definitions.

Usage::

    from mypy_boto3.importexport.type_defs import CancelJobOutputTypeDef

    data: CancelJobOutputTypeDef = {...}
"""
from datetime import datetime
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
    "CancelJobOutputTypeDef",
    "ArtifactTypeDef",
    "CreateJobOutputTypeDef",
    "GetShippingLabelOutputTypeDef",
    "GetStatusOutputTypeDef",
    "JobTypeDef",
    "ListJobsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "UpdateJobOutputTypeDef",
)

CancelJobOutputTypeDef = TypedDict("CancelJobOutputTypeDef", {"Success": bool}, total=False)

ArtifactTypeDef = TypedDict("ArtifactTypeDef", {"Description": str, "URL": str}, total=False)

CreateJobOutputTypeDef = TypedDict(
    "CreateJobOutputTypeDef",
    {
        "JobId": str,
        "JobType": Literal["Import", "Export"],
        "Signature": str,
        "SignatureFileContents": str,
        "WarningMessage": str,
        "ArtifactList": List[ArtifactTypeDef],
    },
    total=False,
)

GetShippingLabelOutputTypeDef = TypedDict(
    "GetShippingLabelOutputTypeDef", {"ShippingLabelURL": str, "Warning": str}, total=False
)

GetStatusOutputTypeDef = TypedDict(
    "GetStatusOutputTypeDef",
    {
        "JobId": str,
        "JobType": Literal["Import", "Export"],
        "LocationCode": str,
        "LocationMessage": str,
        "ProgressCode": str,
        "ProgressMessage": str,
        "Carrier": str,
        "TrackingNumber": str,
        "LogBucket": str,
        "LogKey": str,
        "ErrorCount": int,
        "Signature": str,
        "SignatureFileContents": str,
        "CurrentManifest": str,
        "CreationDate": datetime,
        "ArtifactList": List[ArtifactTypeDef],
    },
    total=False,
)

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "JobId": str,
        "CreationDate": datetime,
        "IsCanceled": bool,
        "JobType": Literal["Import", "Export"],
    },
    total=False,
)

ListJobsOutputTypeDef = TypedDict(
    "ListJobsOutputTypeDef", {"Jobs": List[JobTypeDef], "IsTruncated": bool}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

UpdateJobOutputTypeDef = TypedDict(
    "UpdateJobOutputTypeDef",
    {"Success": bool, "WarningMessage": str, "ArtifactList": List[ArtifactTypeDef]},
    total=False,
)
