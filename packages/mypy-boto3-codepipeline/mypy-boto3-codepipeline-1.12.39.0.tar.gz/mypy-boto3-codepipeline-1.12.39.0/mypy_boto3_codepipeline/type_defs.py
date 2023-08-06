"""
Main interface for codepipeline service type definitions.

Usage::

    from mypy_boto3.codepipeline.type_defs import AcknowledgeJobOutputTypeDef

    data: AcknowledgeJobOutputTypeDef = {...}
"""
from datetime import datetime
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
    "AcknowledgeJobOutputTypeDef",
    "AcknowledgeThirdPartyJobOutputTypeDef",
    "ActionConfigurationPropertyTypeDef",
    "ActionExecutionFilterTypeDef",
    "ActionRevisionTypeDef",
    "ActionTypeIdTypeDef",
    "ActionTypeSettingsTypeDef",
    "ApprovalResultTypeDef",
    "ArtifactDetailsTypeDef",
    "ActionTypeTypeDef",
    "TagTypeDef",
    "CreateCustomActionTypeOutputTypeDef",
    "EncryptionKeyTypeDef",
    "ArtifactStoreTypeDef",
    "InputArtifactTypeDef",
    "OutputArtifactTypeDef",
    "ActionDeclarationTypeDef",
    "BlockerDeclarationTypeDef",
    "StageDeclarationTypeDef",
    "PipelineDeclarationTypeDef",
    "CreatePipelineOutputTypeDef",
    "CurrentRevisionTypeDef",
    "ExecutionDetailsTypeDef",
    "FailureDetailsTypeDef",
    "AWSSessionCredentialsTypeDef",
    "ActionConfigurationTypeDef",
    "S3ArtifactLocationTypeDef",
    "ArtifactLocationTypeDef",
    "ArtifactTypeDef",
    "ActionContextTypeDef",
    "StageContextTypeDef",
    "PipelineContextTypeDef",
    "JobDataTypeDef",
    "JobDetailsTypeDef",
    "GetJobDetailsOutputTypeDef",
    "ArtifactRevisionTypeDef",
    "PipelineExecutionTypeDef",
    "GetPipelineExecutionOutputTypeDef",
    "PipelineMetadataTypeDef",
    "GetPipelineOutputTypeDef",
    "ErrorDetailsTypeDef",
    "ActionExecutionTypeDef",
    "ActionStateTypeDef",
    "StageExecutionTypeDef",
    "TransitionStateTypeDef",
    "StageStateTypeDef",
    "GetPipelineStateOutputTypeDef",
    "ThirdPartyJobDataTypeDef",
    "ThirdPartyJobDetailsTypeDef",
    "GetThirdPartyJobDetailsOutputTypeDef",
    "S3LocationTypeDef",
    "ArtifactDetailTypeDef",
    "ActionExecutionInputTypeDef",
    "ActionExecutionResultTypeDef",
    "ActionExecutionOutputTypeDef",
    "ActionExecutionDetailTypeDef",
    "ListActionExecutionsOutputTypeDef",
    "ListActionTypesOutputTypeDef",
    "ExecutionTriggerTypeDef",
    "SourceRevisionTypeDef",
    "StopExecutionTriggerTypeDef",
    "PipelineExecutionSummaryTypeDef",
    "ListPipelineExecutionsOutputTypeDef",
    "PipelineSummaryTypeDef",
    "ListPipelinesOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "WebhookAuthConfigurationTypeDef",
    "WebhookFilterRuleTypeDef",
    "WebhookDefinitionTypeDef",
    "ListWebhookItemTypeDef",
    "ListWebhooksOutputTypeDef",
    "PaginatorConfigTypeDef",
    "JobTypeDef",
    "PollForJobsOutputTypeDef",
    "ThirdPartyJobTypeDef",
    "PollForThirdPartyJobsOutputTypeDef",
    "PutActionRevisionOutputTypeDef",
    "PutApprovalResultOutputTypeDef",
    "PutWebhookOutputTypeDef",
    "RetryStageExecutionOutputTypeDef",
    "StartPipelineExecutionOutputTypeDef",
    "StopPipelineExecutionOutputTypeDef",
    "UpdatePipelineOutputTypeDef",
)

AcknowledgeJobOutputTypeDef = TypedDict(
    "AcknowledgeJobOutputTypeDef",
    {
        "status": Literal[
            "Created", "Queued", "Dispatched", "InProgress", "TimedOut", "Succeeded", "Failed"
        ]
    },
    total=False,
)

AcknowledgeThirdPartyJobOutputTypeDef = TypedDict(
    "AcknowledgeThirdPartyJobOutputTypeDef",
    {
        "status": Literal[
            "Created", "Queued", "Dispatched", "InProgress", "TimedOut", "Succeeded", "Failed"
        ]
    },
    total=False,
)

_RequiredActionConfigurationPropertyTypeDef = TypedDict(
    "_RequiredActionConfigurationPropertyTypeDef",
    {"name": str, "required": bool, "key": bool, "secret": bool},
)
_OptionalActionConfigurationPropertyTypeDef = TypedDict(
    "_OptionalActionConfigurationPropertyTypeDef",
    {"queryable": bool, "description": str, "type": Literal["String", "Number", "Boolean"]},
    total=False,
)


class ActionConfigurationPropertyTypeDef(
    _RequiredActionConfigurationPropertyTypeDef, _OptionalActionConfigurationPropertyTypeDef
):
    pass


ActionExecutionFilterTypeDef = TypedDict(
    "ActionExecutionFilterTypeDef", {"pipelineExecutionId": str}, total=False
)

ActionRevisionTypeDef = TypedDict(
    "ActionRevisionTypeDef", {"revisionId": str, "revisionChangeId": str, "created": datetime}
)

ActionTypeIdTypeDef = TypedDict(
    "ActionTypeIdTypeDef",
    {
        "category": Literal["Source", "Build", "Deploy", "Test", "Invoke", "Approval"],
        "owner": Literal["AWS", "ThirdParty", "Custom"],
        "provider": str,
        "version": str,
    },
)

ActionTypeSettingsTypeDef = TypedDict(
    "ActionTypeSettingsTypeDef",
    {
        "thirdPartyConfigurationUrl": str,
        "entityUrlTemplate": str,
        "executionUrlTemplate": str,
        "revisionUrlTemplate": str,
    },
    total=False,
)

ApprovalResultTypeDef = TypedDict(
    "ApprovalResultTypeDef", {"summary": str, "status": Literal["Approved", "Rejected"]}
)

ArtifactDetailsTypeDef = TypedDict(
    "ArtifactDetailsTypeDef", {"minimumCount": int, "maximumCount": int}
)

_RequiredActionTypeTypeDef = TypedDict(
    "_RequiredActionTypeTypeDef",
    {
        "id": ActionTypeIdTypeDef,
        "inputArtifactDetails": ArtifactDetailsTypeDef,
        "outputArtifactDetails": ArtifactDetailsTypeDef,
    },
)
_OptionalActionTypeTypeDef = TypedDict(
    "_OptionalActionTypeTypeDef",
    {
        "settings": ActionTypeSettingsTypeDef,
        "actionConfigurationProperties": List[ActionConfigurationPropertyTypeDef],
    },
    total=False,
)


class ActionTypeTypeDef(_RequiredActionTypeTypeDef, _OptionalActionTypeTypeDef):
    pass


TagTypeDef = TypedDict("TagTypeDef", {"key": str, "value": str})

_RequiredCreateCustomActionTypeOutputTypeDef = TypedDict(
    "_RequiredCreateCustomActionTypeOutputTypeDef", {"actionType": ActionTypeTypeDef}
)
_OptionalCreateCustomActionTypeOutputTypeDef = TypedDict(
    "_OptionalCreateCustomActionTypeOutputTypeDef", {"tags": List[TagTypeDef]}, total=False
)


class CreateCustomActionTypeOutputTypeDef(
    _RequiredCreateCustomActionTypeOutputTypeDef, _OptionalCreateCustomActionTypeOutputTypeDef
):
    pass


EncryptionKeyTypeDef = TypedDict("EncryptionKeyTypeDef", {"id": str, "type": Literal["KMS"]})

_RequiredArtifactStoreTypeDef = TypedDict(
    "_RequiredArtifactStoreTypeDef", {"type": Literal["S3"], "location": str}
)
_OptionalArtifactStoreTypeDef = TypedDict(
    "_OptionalArtifactStoreTypeDef", {"encryptionKey": EncryptionKeyTypeDef}, total=False
)


class ArtifactStoreTypeDef(_RequiredArtifactStoreTypeDef, _OptionalArtifactStoreTypeDef):
    pass


InputArtifactTypeDef = TypedDict("InputArtifactTypeDef", {"name": str})

OutputArtifactTypeDef = TypedDict("OutputArtifactTypeDef", {"name": str})

_RequiredActionDeclarationTypeDef = TypedDict(
    "_RequiredActionDeclarationTypeDef", {"name": str, "actionTypeId": ActionTypeIdTypeDef}
)
_OptionalActionDeclarationTypeDef = TypedDict(
    "_OptionalActionDeclarationTypeDef",
    {
        "runOrder": int,
        "configuration": Dict[str, str],
        "outputArtifacts": List[OutputArtifactTypeDef],
        "inputArtifacts": List[InputArtifactTypeDef],
        "roleArn": str,
        "region": str,
        "namespace": str,
    },
    total=False,
)


class ActionDeclarationTypeDef(
    _RequiredActionDeclarationTypeDef, _OptionalActionDeclarationTypeDef
):
    pass


BlockerDeclarationTypeDef = TypedDict(
    "BlockerDeclarationTypeDef", {"name": str, "type": Literal["Schedule"]}
)

_RequiredStageDeclarationTypeDef = TypedDict(
    "_RequiredStageDeclarationTypeDef", {"name": str, "actions": List[ActionDeclarationTypeDef]}
)
_OptionalStageDeclarationTypeDef = TypedDict(
    "_OptionalStageDeclarationTypeDef", {"blockers": List[BlockerDeclarationTypeDef]}, total=False
)


class StageDeclarationTypeDef(_RequiredStageDeclarationTypeDef, _OptionalStageDeclarationTypeDef):
    pass


_RequiredPipelineDeclarationTypeDef = TypedDict(
    "_RequiredPipelineDeclarationTypeDef",
    {"name": str, "roleArn": str, "stages": List[StageDeclarationTypeDef]},
)
_OptionalPipelineDeclarationTypeDef = TypedDict(
    "_OptionalPipelineDeclarationTypeDef",
    {
        "artifactStore": ArtifactStoreTypeDef,
        "artifactStores": Dict[str, ArtifactStoreTypeDef],
        "version": int,
    },
    total=False,
)


class PipelineDeclarationTypeDef(
    _RequiredPipelineDeclarationTypeDef, _OptionalPipelineDeclarationTypeDef
):
    pass


CreatePipelineOutputTypeDef = TypedDict(
    "CreatePipelineOutputTypeDef",
    {"pipeline": PipelineDeclarationTypeDef, "tags": List[TagTypeDef]},
    total=False,
)

_RequiredCurrentRevisionTypeDef = TypedDict(
    "_RequiredCurrentRevisionTypeDef", {"revision": str, "changeIdentifier": str}
)
_OptionalCurrentRevisionTypeDef = TypedDict(
    "_OptionalCurrentRevisionTypeDef", {"created": datetime, "revisionSummary": str}, total=False
)


class CurrentRevisionTypeDef(_RequiredCurrentRevisionTypeDef, _OptionalCurrentRevisionTypeDef):
    pass


ExecutionDetailsTypeDef = TypedDict(
    "ExecutionDetailsTypeDef",
    {"summary": str, "externalExecutionId": str, "percentComplete": int},
    total=False,
)

_RequiredFailureDetailsTypeDef = TypedDict(
    "_RequiredFailureDetailsTypeDef",
    {
        "type": Literal[
            "JobFailed",
            "ConfigurationError",
            "PermissionError",
            "RevisionOutOfSync",
            "RevisionUnavailable",
            "SystemUnavailable",
        ],
        "message": str,
    },
)
_OptionalFailureDetailsTypeDef = TypedDict(
    "_OptionalFailureDetailsTypeDef", {"externalExecutionId": str}, total=False
)


class FailureDetailsTypeDef(_RequiredFailureDetailsTypeDef, _OptionalFailureDetailsTypeDef):
    pass


AWSSessionCredentialsTypeDef = TypedDict(
    "AWSSessionCredentialsTypeDef",
    {"accessKeyId": str, "secretAccessKey": str, "sessionToken": str},
)

ActionConfigurationTypeDef = TypedDict(
    "ActionConfigurationTypeDef", {"configuration": Dict[str, str]}, total=False
)

S3ArtifactLocationTypeDef = TypedDict(
    "S3ArtifactLocationTypeDef", {"bucketName": str, "objectKey": str}
)

ArtifactLocationTypeDef = TypedDict(
    "ArtifactLocationTypeDef",
    {"type": Literal["S3"], "s3Location": S3ArtifactLocationTypeDef},
    total=False,
)

ArtifactTypeDef = TypedDict(
    "ArtifactTypeDef",
    {"name": str, "revision": str, "location": ArtifactLocationTypeDef},
    total=False,
)

ActionContextTypeDef = TypedDict(
    "ActionContextTypeDef", {"name": str, "actionExecutionId": str}, total=False
)

StageContextTypeDef = TypedDict("StageContextTypeDef", {"name": str}, total=False)

PipelineContextTypeDef = TypedDict(
    "PipelineContextTypeDef",
    {
        "pipelineName": str,
        "stage": StageContextTypeDef,
        "action": ActionContextTypeDef,
        "pipelineArn": str,
        "pipelineExecutionId": str,
    },
    total=False,
)

JobDataTypeDef = TypedDict(
    "JobDataTypeDef",
    {
        "actionTypeId": ActionTypeIdTypeDef,
        "actionConfiguration": ActionConfigurationTypeDef,
        "pipelineContext": PipelineContextTypeDef,
        "inputArtifacts": List[ArtifactTypeDef],
        "outputArtifacts": List[ArtifactTypeDef],
        "artifactCredentials": AWSSessionCredentialsTypeDef,
        "continuationToken": str,
        "encryptionKey": EncryptionKeyTypeDef,
    },
    total=False,
)

JobDetailsTypeDef = TypedDict(
    "JobDetailsTypeDef", {"id": str, "data": JobDataTypeDef, "accountId": str}, total=False
)

GetJobDetailsOutputTypeDef = TypedDict(
    "GetJobDetailsOutputTypeDef", {"jobDetails": JobDetailsTypeDef}, total=False
)

ArtifactRevisionTypeDef = TypedDict(
    "ArtifactRevisionTypeDef",
    {
        "name": str,
        "revisionId": str,
        "revisionChangeIdentifier": str,
        "revisionSummary": str,
        "created": datetime,
        "revisionUrl": str,
    },
    total=False,
)

PipelineExecutionTypeDef = TypedDict(
    "PipelineExecutionTypeDef",
    {
        "pipelineName": str,
        "pipelineVersion": int,
        "pipelineExecutionId": str,
        "status": Literal["InProgress", "Stopped", "Stopping", "Succeeded", "Superseded", "Failed"],
        "artifactRevisions": List[ArtifactRevisionTypeDef],
    },
    total=False,
)

GetPipelineExecutionOutputTypeDef = TypedDict(
    "GetPipelineExecutionOutputTypeDef",
    {"pipelineExecution": PipelineExecutionTypeDef},
    total=False,
)

PipelineMetadataTypeDef = TypedDict(
    "PipelineMetadataTypeDef",
    {"pipelineArn": str, "created": datetime, "updated": datetime},
    total=False,
)

GetPipelineOutputTypeDef = TypedDict(
    "GetPipelineOutputTypeDef",
    {"pipeline": PipelineDeclarationTypeDef, "metadata": PipelineMetadataTypeDef},
    total=False,
)

ErrorDetailsTypeDef = TypedDict("ErrorDetailsTypeDef", {"code": str, "message": str}, total=False)

ActionExecutionTypeDef = TypedDict(
    "ActionExecutionTypeDef",
    {
        "status": Literal["InProgress", "Abandoned", "Succeeded", "Failed"],
        "summary": str,
        "lastStatusChange": datetime,
        "token": str,
        "lastUpdatedBy": str,
        "externalExecutionId": str,
        "externalExecutionUrl": str,
        "percentComplete": int,
        "errorDetails": ErrorDetailsTypeDef,
    },
    total=False,
)

ActionStateTypeDef = TypedDict(
    "ActionStateTypeDef",
    {
        "actionName": str,
        "currentRevision": ActionRevisionTypeDef,
        "latestExecution": ActionExecutionTypeDef,
        "entityUrl": str,
        "revisionUrl": str,
    },
    total=False,
)

StageExecutionTypeDef = TypedDict(
    "StageExecutionTypeDef",
    {
        "pipelineExecutionId": str,
        "status": Literal["InProgress", "Failed", "Stopped", "Stopping", "Succeeded"],
    },
)

TransitionStateTypeDef = TypedDict(
    "TransitionStateTypeDef",
    {"enabled": bool, "lastChangedBy": str, "lastChangedAt": datetime, "disabledReason": str},
    total=False,
)

StageStateTypeDef = TypedDict(
    "StageStateTypeDef",
    {
        "stageName": str,
        "inboundTransitionState": TransitionStateTypeDef,
        "actionStates": List[ActionStateTypeDef],
        "latestExecution": StageExecutionTypeDef,
    },
    total=False,
)

GetPipelineStateOutputTypeDef = TypedDict(
    "GetPipelineStateOutputTypeDef",
    {
        "pipelineName": str,
        "pipelineVersion": int,
        "stageStates": List[StageStateTypeDef],
        "created": datetime,
        "updated": datetime,
    },
    total=False,
)

ThirdPartyJobDataTypeDef = TypedDict(
    "ThirdPartyJobDataTypeDef",
    {
        "actionTypeId": ActionTypeIdTypeDef,
        "actionConfiguration": ActionConfigurationTypeDef,
        "pipelineContext": PipelineContextTypeDef,
        "inputArtifacts": List[ArtifactTypeDef],
        "outputArtifacts": List[ArtifactTypeDef],
        "artifactCredentials": AWSSessionCredentialsTypeDef,
        "continuationToken": str,
        "encryptionKey": EncryptionKeyTypeDef,
    },
    total=False,
)

ThirdPartyJobDetailsTypeDef = TypedDict(
    "ThirdPartyJobDetailsTypeDef",
    {"id": str, "data": ThirdPartyJobDataTypeDef, "nonce": str},
    total=False,
)

GetThirdPartyJobDetailsOutputTypeDef = TypedDict(
    "GetThirdPartyJobDetailsOutputTypeDef", {"jobDetails": ThirdPartyJobDetailsTypeDef}, total=False
)

S3LocationTypeDef = TypedDict("S3LocationTypeDef", {"bucket": str, "key": str}, total=False)

ArtifactDetailTypeDef = TypedDict(
    "ArtifactDetailTypeDef", {"name": str, "s3location": S3LocationTypeDef}, total=False
)

ActionExecutionInputTypeDef = TypedDict(
    "ActionExecutionInputTypeDef",
    {
        "actionTypeId": ActionTypeIdTypeDef,
        "configuration": Dict[str, str],
        "resolvedConfiguration": Dict[str, str],
        "roleArn": str,
        "region": str,
        "inputArtifacts": List[ArtifactDetailTypeDef],
        "namespace": str,
    },
    total=False,
)

ActionExecutionResultTypeDef = TypedDict(
    "ActionExecutionResultTypeDef",
    {"externalExecutionId": str, "externalExecutionSummary": str, "externalExecutionUrl": str},
    total=False,
)

ActionExecutionOutputTypeDef = TypedDict(
    "ActionExecutionOutputTypeDef",
    {
        "outputArtifacts": List[ArtifactDetailTypeDef],
        "executionResult": ActionExecutionResultTypeDef,
        "outputVariables": Dict[str, str],
    },
    total=False,
)

ActionExecutionDetailTypeDef = TypedDict(
    "ActionExecutionDetailTypeDef",
    {
        "pipelineExecutionId": str,
        "actionExecutionId": str,
        "pipelineVersion": int,
        "stageName": str,
        "actionName": str,
        "startTime": datetime,
        "lastUpdateTime": datetime,
        "status": Literal["InProgress", "Abandoned", "Succeeded", "Failed"],
        "input": ActionExecutionInputTypeDef,
        "output": ActionExecutionOutputTypeDef,
    },
    total=False,
)

ListActionExecutionsOutputTypeDef = TypedDict(
    "ListActionExecutionsOutputTypeDef",
    {"actionExecutionDetails": List[ActionExecutionDetailTypeDef], "nextToken": str},
    total=False,
)

_RequiredListActionTypesOutputTypeDef = TypedDict(
    "_RequiredListActionTypesOutputTypeDef", {"actionTypes": List[ActionTypeTypeDef]}
)
_OptionalListActionTypesOutputTypeDef = TypedDict(
    "_OptionalListActionTypesOutputTypeDef", {"nextToken": str}, total=False
)


class ListActionTypesOutputTypeDef(
    _RequiredListActionTypesOutputTypeDef, _OptionalListActionTypesOutputTypeDef
):
    pass


ExecutionTriggerTypeDef = TypedDict(
    "ExecutionTriggerTypeDef",
    {
        "triggerType": Literal[
            "CreatePipeline",
            "StartPipelineExecution",
            "PollForSourceChanges",
            "Webhook",
            "CloudWatchEvent",
            "PutActionRevision",
        ],
        "triggerDetail": str,
    },
    total=False,
)

_RequiredSourceRevisionTypeDef = TypedDict("_RequiredSourceRevisionTypeDef", {"actionName": str})
_OptionalSourceRevisionTypeDef = TypedDict(
    "_OptionalSourceRevisionTypeDef",
    {"revisionId": str, "revisionSummary": str, "revisionUrl": str},
    total=False,
)


class SourceRevisionTypeDef(_RequiredSourceRevisionTypeDef, _OptionalSourceRevisionTypeDef):
    pass


StopExecutionTriggerTypeDef = TypedDict("StopExecutionTriggerTypeDef", {"reason": str}, total=False)

PipelineExecutionSummaryTypeDef = TypedDict(
    "PipelineExecutionSummaryTypeDef",
    {
        "pipelineExecutionId": str,
        "status": Literal["InProgress", "Stopped", "Stopping", "Succeeded", "Superseded", "Failed"],
        "startTime": datetime,
        "lastUpdateTime": datetime,
        "sourceRevisions": List[SourceRevisionTypeDef],
        "trigger": ExecutionTriggerTypeDef,
        "stopTrigger": StopExecutionTriggerTypeDef,
    },
    total=False,
)

ListPipelineExecutionsOutputTypeDef = TypedDict(
    "ListPipelineExecutionsOutputTypeDef",
    {"pipelineExecutionSummaries": List[PipelineExecutionSummaryTypeDef], "nextToken": str},
    total=False,
)

PipelineSummaryTypeDef = TypedDict(
    "PipelineSummaryTypeDef",
    {"name": str, "version": int, "created": datetime, "updated": datetime},
    total=False,
)

ListPipelinesOutputTypeDef = TypedDict(
    "ListPipelinesOutputTypeDef",
    {"pipelines": List[PipelineSummaryTypeDef], "nextToken": str},
    total=False,
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef", {"tags": List[TagTypeDef], "nextToken": str}, total=False
)

WebhookAuthConfigurationTypeDef = TypedDict(
    "WebhookAuthConfigurationTypeDef", {"AllowedIPRange": str, "SecretToken": str}, total=False
)

_RequiredWebhookFilterRuleTypeDef = TypedDict(
    "_RequiredWebhookFilterRuleTypeDef", {"jsonPath": str}
)
_OptionalWebhookFilterRuleTypeDef = TypedDict(
    "_OptionalWebhookFilterRuleTypeDef", {"matchEquals": str}, total=False
)


class WebhookFilterRuleTypeDef(
    _RequiredWebhookFilterRuleTypeDef, _OptionalWebhookFilterRuleTypeDef
):
    pass


WebhookDefinitionTypeDef = TypedDict(
    "WebhookDefinitionTypeDef",
    {
        "name": str,
        "targetPipeline": str,
        "targetAction": str,
        "filters": List[WebhookFilterRuleTypeDef],
        "authentication": Literal["GITHUB_HMAC", "IP", "UNAUTHENTICATED"],
        "authenticationConfiguration": WebhookAuthConfigurationTypeDef,
    },
)

_RequiredListWebhookItemTypeDef = TypedDict(
    "_RequiredListWebhookItemTypeDef", {"definition": WebhookDefinitionTypeDef, "url": str}
)
_OptionalListWebhookItemTypeDef = TypedDict(
    "_OptionalListWebhookItemTypeDef",
    {
        "errorMessage": str,
        "errorCode": str,
        "lastTriggered": datetime,
        "arn": str,
        "tags": List[TagTypeDef],
    },
    total=False,
)


class ListWebhookItemTypeDef(_RequiredListWebhookItemTypeDef, _OptionalListWebhookItemTypeDef):
    pass


ListWebhooksOutputTypeDef = TypedDict(
    "ListWebhooksOutputTypeDef",
    {"webhooks": List[ListWebhookItemTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

JobTypeDef = TypedDict(
    "JobTypeDef", {"id": str, "data": JobDataTypeDef, "nonce": str, "accountId": str}, total=False
)

PollForJobsOutputTypeDef = TypedDict(
    "PollForJobsOutputTypeDef", {"jobs": List[JobTypeDef]}, total=False
)

ThirdPartyJobTypeDef = TypedDict(
    "ThirdPartyJobTypeDef", {"clientId": str, "jobId": str}, total=False
)

PollForThirdPartyJobsOutputTypeDef = TypedDict(
    "PollForThirdPartyJobsOutputTypeDef", {"jobs": List[ThirdPartyJobTypeDef]}, total=False
)

PutActionRevisionOutputTypeDef = TypedDict(
    "PutActionRevisionOutputTypeDef", {"newRevision": bool, "pipelineExecutionId": str}, total=False
)

PutApprovalResultOutputTypeDef = TypedDict(
    "PutApprovalResultOutputTypeDef", {"approvedAt": datetime}, total=False
)

PutWebhookOutputTypeDef = TypedDict(
    "PutWebhookOutputTypeDef", {"webhook": ListWebhookItemTypeDef}, total=False
)

RetryStageExecutionOutputTypeDef = TypedDict(
    "RetryStageExecutionOutputTypeDef", {"pipelineExecutionId": str}, total=False
)

StartPipelineExecutionOutputTypeDef = TypedDict(
    "StartPipelineExecutionOutputTypeDef", {"pipelineExecutionId": str}, total=False
)

StopPipelineExecutionOutputTypeDef = TypedDict(
    "StopPipelineExecutionOutputTypeDef", {"pipelineExecutionId": str}, total=False
)

UpdatePipelineOutputTypeDef = TypedDict(
    "UpdatePipelineOutputTypeDef", {"pipeline": PipelineDeclarationTypeDef}, total=False
)
