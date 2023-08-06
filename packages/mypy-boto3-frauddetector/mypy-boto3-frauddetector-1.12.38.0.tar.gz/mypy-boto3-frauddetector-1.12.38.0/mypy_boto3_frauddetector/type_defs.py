"""
Main interface for frauddetector service type definitions.

Usage::

    from mypy_boto3.frauddetector.type_defs import BatchCreateVariableErrorTypeDef

    data: BatchCreateVariableErrorTypeDef = {...}
"""
import sys
from typing import Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BatchCreateVariableErrorTypeDef",
    "BatchCreateVariableResultTypeDef",
    "BatchGetVariableErrorTypeDef",
    "VariableTypeDef",
    "BatchGetVariableResultTypeDef",
    "CreateDetectorVersionResultTypeDef",
    "CreateModelVersionResultTypeDef",
    "RuleTypeDef",
    "CreateRuleResultTypeDef",
    "DetectorVersionSummaryTypeDef",
    "DescribeDetectorResultTypeDef",
    "LabelSchemaTypeDef",
    "ModelVariableTypeDef",
    "TrainingDataSourceTypeDef",
    "ModelVersionDetailTypeDef",
    "DescribeModelVersionsResultTypeDef",
    "ModelVersionTypeDef",
    "GetDetectorVersionResultTypeDef",
    "DetectorTypeDef",
    "GetDetectorsResultTypeDef",
    "ModelInputConfigurationTypeDef",
    "ModelOutputConfigurationTypeDef",
    "RoleTypeDef",
    "ExternalModelTypeDef",
    "GetExternalModelsResultTypeDef",
    "GetModelVersionResultTypeDef",
    "ModelTypeDef",
    "GetModelsResultTypeDef",
    "OutcomeTypeDef",
    "GetOutcomesResultTypeDef",
    "ModelScoresTypeDef",
    "GetPredictionResultTypeDef",
    "RuleDetailTypeDef",
    "GetRulesResultTypeDef",
    "GetVariablesResultTypeDef",
    "ModelEndpointDataBlobTypeDef",
    "UpdateRuleVersionResultTypeDef",
    "VariableEntryTypeDef",
)

BatchCreateVariableErrorTypeDef = TypedDict(
    "BatchCreateVariableErrorTypeDef", {"name": str, "code": int, "message": str}, total=False
)

BatchCreateVariableResultTypeDef = TypedDict(
    "BatchCreateVariableResultTypeDef",
    {"errors": List[BatchCreateVariableErrorTypeDef]},
    total=False,
)

BatchGetVariableErrorTypeDef = TypedDict(
    "BatchGetVariableErrorTypeDef", {"name": str, "code": int, "message": str}, total=False
)

VariableTypeDef = TypedDict(
    "VariableTypeDef",
    {
        "name": str,
        "dataType": Literal["STRING", "INTEGER", "FLOAT", "BOOLEAN"],
        "dataSource": Literal["EVENT", "MODEL_SCORE", "EXTERNAL_MODEL_SCORE"],
        "defaultValue": str,
        "description": str,
        "variableType": str,
        "lastUpdatedTime": str,
        "createdTime": str,
    },
    total=False,
)

BatchGetVariableResultTypeDef = TypedDict(
    "BatchGetVariableResultTypeDef",
    {"variables": List[VariableTypeDef], "errors": List[BatchGetVariableErrorTypeDef]},
    total=False,
)

CreateDetectorVersionResultTypeDef = TypedDict(
    "CreateDetectorVersionResultTypeDef",
    {"detectorId": str, "detectorVersionId": str, "status": Literal["DRAFT", "ACTIVE", "INACTIVE"]},
    total=False,
)

CreateModelVersionResultTypeDef = TypedDict(
    "CreateModelVersionResultTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "modelVersionNumber": str,
        "status": str,
    },
    total=False,
)

RuleTypeDef = TypedDict("RuleTypeDef", {"detectorId": str, "ruleId": str, "ruleVersion": str})

CreateRuleResultTypeDef = TypedDict("CreateRuleResultTypeDef", {"rule": RuleTypeDef}, total=False)

DetectorVersionSummaryTypeDef = TypedDict(
    "DetectorVersionSummaryTypeDef",
    {
        "detectorVersionId": str,
        "status": Literal["DRAFT", "ACTIVE", "INACTIVE"],
        "description": str,
        "lastUpdatedTime": str,
    },
    total=False,
)

DescribeDetectorResultTypeDef = TypedDict(
    "DescribeDetectorResultTypeDef",
    {
        "detectorId": str,
        "detectorVersionSummaries": List[DetectorVersionSummaryTypeDef],
        "nextToken": str,
    },
    total=False,
)

LabelSchemaTypeDef = TypedDict(
    "LabelSchemaTypeDef", {"labelKey": str, "labelMapper": Dict[str, List[str]]}
)

_RequiredModelVariableTypeDef = TypedDict("_RequiredModelVariableTypeDef", {"name": str})
_OptionalModelVariableTypeDef = TypedDict(
    "_OptionalModelVariableTypeDef", {"index": int}, total=False
)


class ModelVariableTypeDef(_RequiredModelVariableTypeDef, _OptionalModelVariableTypeDef):
    pass


TrainingDataSourceTypeDef = TypedDict(
    "TrainingDataSourceTypeDef", {"dataLocation": str, "dataAccessRoleArn": str}
)

ModelVersionDetailTypeDef = TypedDict(
    "ModelVersionDetailTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "modelVersionNumber": str,
        "description": str,
        "status": str,
        "trainingDataSource": TrainingDataSourceTypeDef,
        "modelVariables": List[ModelVariableTypeDef],
        "labelSchema": LabelSchemaTypeDef,
        "validationMetrics": Dict[str, str],
        "trainingMetrics": Dict[str, str],
        "lastUpdatedTime": str,
        "createdTime": str,
    },
    total=False,
)

DescribeModelVersionsResultTypeDef = TypedDict(
    "DescribeModelVersionsResultTypeDef",
    {"modelVersionDetails": List[ModelVersionDetailTypeDef], "nextToken": str},
    total=False,
)

ModelVersionTypeDef = TypedDict(
    "ModelVersionTypeDef",
    {"modelId": str, "modelType": Literal["ONLINE_FRAUD_INSIGHTS"], "modelVersionNumber": str},
)

GetDetectorVersionResultTypeDef = TypedDict(
    "GetDetectorVersionResultTypeDef",
    {
        "detectorId": str,
        "detectorVersionId": str,
        "description": str,
        "externalModelEndpoints": List[str],
        "modelVersions": List[ModelVersionTypeDef],
        "rules": List[RuleTypeDef],
        "status": Literal["DRAFT", "ACTIVE", "INACTIVE"],
        "lastUpdatedTime": str,
        "createdTime": str,
    },
    total=False,
)

DetectorTypeDef = TypedDict(
    "DetectorTypeDef",
    {"detectorId": str, "description": str, "lastUpdatedTime": str, "createdTime": str},
    total=False,
)

GetDetectorsResultTypeDef = TypedDict(
    "GetDetectorsResultTypeDef", {"detectors": List[DetectorTypeDef], "nextToken": str}, total=False
)

_RequiredModelInputConfigurationTypeDef = TypedDict(
    "_RequiredModelInputConfigurationTypeDef", {"isOpaque": bool}
)
_OptionalModelInputConfigurationTypeDef = TypedDict(
    "_OptionalModelInputConfigurationTypeDef",
    {
        "format": Literal["TEXT_CSV", "APPLICATION_JSON"],
        "jsonInputTemplate": str,
        "csvInputTemplate": str,
    },
    total=False,
)


class ModelInputConfigurationTypeDef(
    _RequiredModelInputConfigurationTypeDef, _OptionalModelInputConfigurationTypeDef
):
    pass


_RequiredModelOutputConfigurationTypeDef = TypedDict(
    "_RequiredModelOutputConfigurationTypeDef",
    {"format": Literal["TEXT_CSV", "APPLICATION_JSONLINES"]},
)
_OptionalModelOutputConfigurationTypeDef = TypedDict(
    "_OptionalModelOutputConfigurationTypeDef",
    {"jsonKeyToVariableMap": Dict[str, str], "csvIndexToVariableMap": Dict[str, str]},
    total=False,
)


class ModelOutputConfigurationTypeDef(
    _RequiredModelOutputConfigurationTypeDef, _OptionalModelOutputConfigurationTypeDef
):
    pass


RoleTypeDef = TypedDict("RoleTypeDef", {"arn": str, "name": str})

ExternalModelTypeDef = TypedDict(
    "ExternalModelTypeDef",
    {
        "modelEndpoint": str,
        "modelSource": Literal["SAGEMAKER"],
        "role": RoleTypeDef,
        "inputConfiguration": ModelInputConfigurationTypeDef,
        "outputConfiguration": ModelOutputConfigurationTypeDef,
        "modelEndpointStatus": Literal["ASSOCIATED", "DISSOCIATED"],
        "lastUpdatedTime": str,
        "createdTime": str,
    },
    total=False,
)

GetExternalModelsResultTypeDef = TypedDict(
    "GetExternalModelsResultTypeDef",
    {"externalModels": List[ExternalModelTypeDef], "nextToken": str},
    total=False,
)

GetModelVersionResultTypeDef = TypedDict(
    "GetModelVersionResultTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "modelVersionNumber": str,
        "description": str,
        "status": str,
    },
    total=False,
)

ModelTypeDef = TypedDict(
    "ModelTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "description": str,
        "trainingDataSource": TrainingDataSourceTypeDef,
        "modelVariables": List[ModelVariableTypeDef],
        "labelSchema": LabelSchemaTypeDef,
        "lastUpdatedTime": str,
        "createdTime": str,
    },
    total=False,
)

GetModelsResultTypeDef = TypedDict(
    "GetModelsResultTypeDef", {"nextToken": str, "models": List[ModelTypeDef]}, total=False
)

OutcomeTypeDef = TypedDict(
    "OutcomeTypeDef",
    {"name": str, "description": str, "lastUpdatedTime": str, "createdTime": str},
    total=False,
)

GetOutcomesResultTypeDef = TypedDict(
    "GetOutcomesResultTypeDef", {"outcomes": List[OutcomeTypeDef], "nextToken": str}, total=False
)

ModelScoresTypeDef = TypedDict(
    "ModelScoresTypeDef",
    {"modelVersion": ModelVersionTypeDef, "scores": Dict[str, float]},
    total=False,
)

GetPredictionResultTypeDef = TypedDict(
    "GetPredictionResultTypeDef",
    {"outcomes": List[str], "modelScores": List[ModelScoresTypeDef]},
    total=False,
)

RuleDetailTypeDef = TypedDict(
    "RuleDetailTypeDef",
    {
        "ruleId": str,
        "description": str,
        "detectorId": str,
        "ruleVersion": str,
        "expression": str,
        "language": Literal["DETECTORPL"],
        "outcomes": List[str],
        "lastUpdatedTime": str,
        "createdTime": str,
    },
    total=False,
)

GetRulesResultTypeDef = TypedDict(
    "GetRulesResultTypeDef", {"ruleDetails": List[RuleDetailTypeDef], "nextToken": str}, total=False
)

GetVariablesResultTypeDef = TypedDict(
    "GetVariablesResultTypeDef", {"variables": List[VariableTypeDef], "nextToken": str}, total=False
)

ModelEndpointDataBlobTypeDef = TypedDict(
    "ModelEndpointDataBlobTypeDef",
    {"byteBuffer": Union[bytes, IO], "contentType": str},
    total=False,
)

UpdateRuleVersionResultTypeDef = TypedDict(
    "UpdateRuleVersionResultTypeDef", {"rule": RuleTypeDef}, total=False
)

VariableEntryTypeDef = TypedDict(
    "VariableEntryTypeDef",
    {
        "name": str,
        "dataType": str,
        "dataSource": str,
        "defaultValue": str,
        "description": str,
        "variableType": str,
    },
    total=False,
)
