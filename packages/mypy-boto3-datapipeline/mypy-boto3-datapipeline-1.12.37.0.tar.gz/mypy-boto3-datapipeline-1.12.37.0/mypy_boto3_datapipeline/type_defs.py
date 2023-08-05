"""
Main interface for datapipeline service type definitions.

Usage::

    from mypy_boto3.datapipeline.type_defs import CreatePipelineOutputTypeDef

    data: CreatePipelineOutputTypeDef = {...}
"""
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CreatePipelineOutputTypeDef",
    "FieldTypeDef",
    "PipelineObjectTypeDef",
    "DescribeObjectsOutputTypeDef",
    "TagTypeDef",
    "PipelineDescriptionTypeDef",
    "DescribePipelinesOutputTypeDef",
    "EvaluateExpressionOutputTypeDef",
    "ParameterAttributeTypeDef",
    "ParameterObjectTypeDef",
    "ParameterValueTypeDef",
    "GetPipelineDefinitionOutputTypeDef",
    "InstanceIdentityTypeDef",
    "PipelineIdNameTypeDef",
    "ListPipelinesOutputTypeDef",
    "PaginatorConfigTypeDef",
    "TaskObjectTypeDef",
    "PollForTaskOutputTypeDef",
    "ValidationErrorTypeDef",
    "ValidationWarningTypeDef",
    "PutPipelineDefinitionOutputTypeDef",
    "QueryObjectsOutputTypeDef",
    "OperatorTypeDef",
    "SelectorTypeDef",
    "QueryTypeDef",
    "ReportTaskProgressOutputTypeDef",
    "ReportTaskRunnerHeartbeatOutputTypeDef",
    "ValidatePipelineDefinitionOutputTypeDef",
)

CreatePipelineOutputTypeDef = TypedDict("CreatePipelineOutputTypeDef", {"pipelineId": str})

_RequiredFieldTypeDef = TypedDict("_RequiredFieldTypeDef", {"key": str})
_OptionalFieldTypeDef = TypedDict(
    "_OptionalFieldTypeDef", {"stringValue": str, "refValue": str}, total=False
)


class FieldTypeDef(_RequiredFieldTypeDef, _OptionalFieldTypeDef):
    pass


PipelineObjectTypeDef = TypedDict(
    "PipelineObjectTypeDef", {"id": str, "name": str, "fields": List[FieldTypeDef]}
)

_RequiredDescribeObjectsOutputTypeDef = TypedDict(
    "_RequiredDescribeObjectsOutputTypeDef", {"pipelineObjects": List[PipelineObjectTypeDef]}
)
_OptionalDescribeObjectsOutputTypeDef = TypedDict(
    "_OptionalDescribeObjectsOutputTypeDef", {"marker": str, "hasMoreResults": bool}, total=False
)


class DescribeObjectsOutputTypeDef(
    _RequiredDescribeObjectsOutputTypeDef, _OptionalDescribeObjectsOutputTypeDef
):
    pass


TagTypeDef = TypedDict("TagTypeDef", {"key": str, "value": str})

_RequiredPipelineDescriptionTypeDef = TypedDict(
    "_RequiredPipelineDescriptionTypeDef",
    {"pipelineId": str, "name": str, "fields": List[FieldTypeDef]},
)
_OptionalPipelineDescriptionTypeDef = TypedDict(
    "_OptionalPipelineDescriptionTypeDef",
    {"description": str, "tags": List[TagTypeDef]},
    total=False,
)


class PipelineDescriptionTypeDef(
    _RequiredPipelineDescriptionTypeDef, _OptionalPipelineDescriptionTypeDef
):
    pass


DescribePipelinesOutputTypeDef = TypedDict(
    "DescribePipelinesOutputTypeDef", {"pipelineDescriptionList": List[PipelineDescriptionTypeDef]}
)

EvaluateExpressionOutputTypeDef = TypedDict(
    "EvaluateExpressionOutputTypeDef", {"evaluatedExpression": str}
)

ParameterAttributeTypeDef = TypedDict("ParameterAttributeTypeDef", {"key": str, "stringValue": str})

ParameterObjectTypeDef = TypedDict(
    "ParameterObjectTypeDef", {"id": str, "attributes": List[ParameterAttributeTypeDef]}
)

ParameterValueTypeDef = TypedDict("ParameterValueTypeDef", {"id": str, "stringValue": str})

GetPipelineDefinitionOutputTypeDef = TypedDict(
    "GetPipelineDefinitionOutputTypeDef",
    {
        "pipelineObjects": List[PipelineObjectTypeDef],
        "parameterObjects": List[ParameterObjectTypeDef],
        "parameterValues": List[ParameterValueTypeDef],
    },
    total=False,
)

InstanceIdentityTypeDef = TypedDict(
    "InstanceIdentityTypeDef", {"document": str, "signature": str}, total=False
)

PipelineIdNameTypeDef = TypedDict("PipelineIdNameTypeDef", {"id": str, "name": str}, total=False)

_RequiredListPipelinesOutputTypeDef = TypedDict(
    "_RequiredListPipelinesOutputTypeDef", {"pipelineIdList": List[PipelineIdNameTypeDef]}
)
_OptionalListPipelinesOutputTypeDef = TypedDict(
    "_OptionalListPipelinesOutputTypeDef", {"marker": str, "hasMoreResults": bool}, total=False
)


class ListPipelinesOutputTypeDef(
    _RequiredListPipelinesOutputTypeDef, _OptionalListPipelinesOutputTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

TaskObjectTypeDef = TypedDict(
    "TaskObjectTypeDef",
    {
        "taskId": str,
        "pipelineId": str,
        "attemptId": str,
        "objects": Dict[str, PipelineObjectTypeDef],
    },
    total=False,
)

PollForTaskOutputTypeDef = TypedDict(
    "PollForTaskOutputTypeDef", {"taskObject": TaskObjectTypeDef}, total=False
)

ValidationErrorTypeDef = TypedDict(
    "ValidationErrorTypeDef", {"id": str, "errors": List[str]}, total=False
)

ValidationWarningTypeDef = TypedDict(
    "ValidationWarningTypeDef", {"id": str, "warnings": List[str]}, total=False
)

_RequiredPutPipelineDefinitionOutputTypeDef = TypedDict(
    "_RequiredPutPipelineDefinitionOutputTypeDef", {"errored": bool}
)
_OptionalPutPipelineDefinitionOutputTypeDef = TypedDict(
    "_OptionalPutPipelineDefinitionOutputTypeDef",
    {
        "validationErrors": List[ValidationErrorTypeDef],
        "validationWarnings": List[ValidationWarningTypeDef],
    },
    total=False,
)


class PutPipelineDefinitionOutputTypeDef(
    _RequiredPutPipelineDefinitionOutputTypeDef, _OptionalPutPipelineDefinitionOutputTypeDef
):
    pass


QueryObjectsOutputTypeDef = TypedDict(
    "QueryObjectsOutputTypeDef",
    {"ids": List[str], "marker": str, "hasMoreResults": bool},
    total=False,
)

OperatorTypeDef = TypedDict(
    "OperatorTypeDef",
    {"type": Literal["EQ", "REF_EQ", "LE", "GE", "BETWEEN"], "values": List[str]},
    total=False,
)

SelectorTypeDef = TypedDict(
    "SelectorTypeDef", {"fieldName": str, "operator": OperatorTypeDef}, total=False
)

QueryTypeDef = TypedDict("QueryTypeDef", {"selectors": List[SelectorTypeDef]}, total=False)

ReportTaskProgressOutputTypeDef = TypedDict("ReportTaskProgressOutputTypeDef", {"canceled": bool})

ReportTaskRunnerHeartbeatOutputTypeDef = TypedDict(
    "ReportTaskRunnerHeartbeatOutputTypeDef", {"terminate": bool}
)

_RequiredValidatePipelineDefinitionOutputTypeDef = TypedDict(
    "_RequiredValidatePipelineDefinitionOutputTypeDef", {"errored": bool}
)
_OptionalValidatePipelineDefinitionOutputTypeDef = TypedDict(
    "_OptionalValidatePipelineDefinitionOutputTypeDef",
    {
        "validationErrors": List[ValidationErrorTypeDef],
        "validationWarnings": List[ValidationWarningTypeDef],
    },
    total=False,
)


class ValidatePipelineDefinitionOutputTypeDef(
    _RequiredValidatePipelineDefinitionOutputTypeDef,
    _OptionalValidatePipelineDefinitionOutputTypeDef,
):
    pass
