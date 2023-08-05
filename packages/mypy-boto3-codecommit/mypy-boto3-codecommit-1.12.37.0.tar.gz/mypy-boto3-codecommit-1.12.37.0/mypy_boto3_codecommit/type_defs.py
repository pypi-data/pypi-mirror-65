"""
Main interface for codecommit service type definitions.

Usage::

    from mypy_boto3.codecommit.type_defs import BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef

    data: BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef = {...}
"""
from datetime import datetime
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
    "BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef",
    "BatchDescribeMergeConflictsErrorTypeDef",
    "FileModesTypeDef",
    "FileSizesTypeDef",
    "IsBinaryFileTypeDef",
    "MergeOperationsTypeDef",
    "ObjectTypesTypeDef",
    "ConflictMetadataTypeDef",
    "MergeHunkDetailTypeDef",
    "MergeHunkTypeDef",
    "ConflictTypeDef",
    "BatchDescribeMergeConflictsOutputTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef",
    "BatchGetCommitsErrorTypeDef",
    "UserInfoTypeDef",
    "CommitTypeDef",
    "BatchGetCommitsOutputTypeDef",
    "RepositoryMetadataTypeDef",
    "BatchGetRepositoriesOutputTypeDef",
    "DeleteFileEntryTypeDef",
    "ReplaceContentEntryTypeDef",
    "SetFileModeEntryTypeDef",
    "ConflictResolutionTypeDef",
    "ApprovalRuleTemplateTypeDef",
    "CreateApprovalRuleTemplateOutputTypeDef",
    "FileMetadataTypeDef",
    "CreateCommitOutputTypeDef",
    "OriginApprovalRuleTemplateTypeDef",
    "ApprovalRuleTypeDef",
    "CreatePullRequestApprovalRuleOutputTypeDef",
    "MergeMetadataTypeDef",
    "PullRequestTargetTypeDef",
    "PullRequestTypeDef",
    "CreatePullRequestOutputTypeDef",
    "CreateRepositoryOutputTypeDef",
    "CreateUnreferencedMergeCommitOutputTypeDef",
    "DeleteApprovalRuleTemplateOutputTypeDef",
    "BranchInfoTypeDef",
    "DeleteBranchOutputTypeDef",
    "CommentTypeDef",
    "DeleteCommentContentOutputTypeDef",
    "DeleteFileOutputTypeDef",
    "DeletePullRequestApprovalRuleOutputTypeDef",
    "DeleteRepositoryOutputTypeDef",
    "DescribeMergeConflictsOutputTypeDef",
    "ApprovalRuleEventMetadataTypeDef",
    "ApprovalRuleOverriddenEventMetadataTypeDef",
    "ApprovalStateChangedEventMetadataTypeDef",
    "PullRequestCreatedEventMetadataTypeDef",
    "PullRequestMergedStateChangedEventMetadataTypeDef",
    "PullRequestSourceReferenceUpdatedEventMetadataTypeDef",
    "PullRequestStatusChangedEventMetadataTypeDef",
    "PullRequestEventTypeDef",
    "DescribePullRequestEventsOutputTypeDef",
    "EvaluationTypeDef",
    "EvaluatePullRequestApprovalRulesOutputTypeDef",
    "GetApprovalRuleTemplateOutputTypeDef",
    "GetBlobOutputTypeDef",
    "GetBranchOutputTypeDef",
    "GetCommentOutputTypeDef",
    "LocationTypeDef",
    "CommentsForComparedCommitTypeDef",
    "GetCommentsForComparedCommitOutputTypeDef",
    "CommentsForPullRequestTypeDef",
    "GetCommentsForPullRequestOutputTypeDef",
    "GetCommitOutputTypeDef",
    "BlobMetadataTypeDef",
    "DifferenceTypeDef",
    "GetDifferencesOutputTypeDef",
    "GetFileOutputTypeDef",
    "FileTypeDef",
    "FolderTypeDef",
    "SubModuleTypeDef",
    "SymbolicLinkTypeDef",
    "GetFolderOutputTypeDef",
    "GetMergeCommitOutputTypeDef",
    "GetMergeConflictsOutputTypeDef",
    "GetMergeOptionsOutputTypeDef",
    "ApprovalTypeDef",
    "GetPullRequestApprovalStatesOutputTypeDef",
    "GetPullRequestOutputTypeDef",
    "GetPullRequestOverrideStateOutputTypeDef",
    "GetRepositoryOutputTypeDef",
    "RepositoryTriggerTypeDef",
    "GetRepositoryTriggersOutputTypeDef",
    "ListApprovalRuleTemplatesOutputTypeDef",
    "ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef",
    "ListBranchesOutputTypeDef",
    "ListPullRequestsOutputTypeDef",
    "ListRepositoriesForApprovalRuleTemplateOutputTypeDef",
    "RepositoryNameIdPairTypeDef",
    "ListRepositoriesOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MergeBranchesByFastForwardOutputTypeDef",
    "MergeBranchesBySquashOutputTypeDef",
    "MergeBranchesByThreeWayOutputTypeDef",
    "MergePullRequestByFastForwardOutputTypeDef",
    "MergePullRequestBySquashOutputTypeDef",
    "MergePullRequestByThreeWayOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PostCommentForComparedCommitOutputTypeDef",
    "PostCommentForPullRequestOutputTypeDef",
    "PostCommentReplyOutputTypeDef",
    "SourceFileSpecifierTypeDef",
    "PutFileEntryTypeDef",
    "PutFileOutputTypeDef",
    "PutRepositoryTriggersOutputTypeDef",
    "TargetTypeDef",
    "RepositoryTriggerExecutionFailureTypeDef",
    "TestRepositoryTriggersOutputTypeDef",
    "UpdateApprovalRuleTemplateContentOutputTypeDef",
    "UpdateApprovalRuleTemplateDescriptionOutputTypeDef",
    "UpdateApprovalRuleTemplateNameOutputTypeDef",
    "UpdateCommentOutputTypeDef",
    "UpdatePullRequestApprovalRuleContentOutputTypeDef",
    "UpdatePullRequestDescriptionOutputTypeDef",
    "UpdatePullRequestStatusOutputTypeDef",
    "UpdatePullRequestTitleOutputTypeDef",
)

BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef = TypedDict(
    "BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef",
    {"repositoryName": str, "errorCode": str, "errorMessage": str},
    total=False,
)

BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef = TypedDict(
    "BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef",
    {
        "associatedRepositoryNames": List[str],
        "errors": List[BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef],
    },
)

BatchDescribeMergeConflictsErrorTypeDef = TypedDict(
    "BatchDescribeMergeConflictsErrorTypeDef",
    {"filePath": str, "exceptionName": str, "message": str},
)

FileModesTypeDef = TypedDict(
    "FileModesTypeDef",
    {
        "source": Literal["EXECUTABLE", "NORMAL", "SYMLINK"],
        "destination": Literal["EXECUTABLE", "NORMAL", "SYMLINK"],
        "base": Literal["EXECUTABLE", "NORMAL", "SYMLINK"],
    },
    total=False,
)

FileSizesTypeDef = TypedDict(
    "FileSizesTypeDef", {"source": int, "destination": int, "base": int}, total=False
)

IsBinaryFileTypeDef = TypedDict(
    "IsBinaryFileTypeDef", {"source": bool, "destination": bool, "base": bool}, total=False
)

MergeOperationsTypeDef = TypedDict(
    "MergeOperationsTypeDef",
    {"source": Literal["A", "M", "D"], "destination": Literal["A", "M", "D"]},
    total=False,
)

ObjectTypesTypeDef = TypedDict(
    "ObjectTypesTypeDef",
    {
        "source": Literal["FILE", "DIRECTORY", "GIT_LINK", "SYMBOLIC_LINK"],
        "destination": Literal["FILE", "DIRECTORY", "GIT_LINK", "SYMBOLIC_LINK"],
        "base": Literal["FILE", "DIRECTORY", "GIT_LINK", "SYMBOLIC_LINK"],
    },
    total=False,
)

ConflictMetadataTypeDef = TypedDict(
    "ConflictMetadataTypeDef",
    {
        "filePath": str,
        "fileSizes": FileSizesTypeDef,
        "fileModes": FileModesTypeDef,
        "objectTypes": ObjectTypesTypeDef,
        "numberOfConflicts": int,
        "isBinaryFile": IsBinaryFileTypeDef,
        "contentConflict": bool,
        "fileModeConflict": bool,
        "objectTypeConflict": bool,
        "mergeOperations": MergeOperationsTypeDef,
    },
    total=False,
)

MergeHunkDetailTypeDef = TypedDict(
    "MergeHunkDetailTypeDef", {"startLine": int, "endLine": int, "hunkContent": str}, total=False
)

MergeHunkTypeDef = TypedDict(
    "MergeHunkTypeDef",
    {
        "isConflict": bool,
        "source": MergeHunkDetailTypeDef,
        "destination": MergeHunkDetailTypeDef,
        "base": MergeHunkDetailTypeDef,
    },
    total=False,
)

ConflictTypeDef = TypedDict(
    "ConflictTypeDef",
    {"conflictMetadata": ConflictMetadataTypeDef, "mergeHunks": List[MergeHunkTypeDef]},
    total=False,
)

_RequiredBatchDescribeMergeConflictsOutputTypeDef = TypedDict(
    "_RequiredBatchDescribeMergeConflictsOutputTypeDef",
    {"conflicts": List[ConflictTypeDef], "destinationCommitId": str, "sourceCommitId": str},
)
_OptionalBatchDescribeMergeConflictsOutputTypeDef = TypedDict(
    "_OptionalBatchDescribeMergeConflictsOutputTypeDef",
    {
        "nextToken": str,
        "errors": List[BatchDescribeMergeConflictsErrorTypeDef],
        "baseCommitId": str,
    },
    total=False,
)


class BatchDescribeMergeConflictsOutputTypeDef(
    _RequiredBatchDescribeMergeConflictsOutputTypeDef,
    _OptionalBatchDescribeMergeConflictsOutputTypeDef,
):
    pass


BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef = TypedDict(
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef",
    {"repositoryName": str, "errorCode": str, "errorMessage": str},
    total=False,
)

BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef = TypedDict(
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef",
    {
        "disassociatedRepositoryNames": List[str],
        "errors": List[BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef],
    },
)

BatchGetCommitsErrorTypeDef = TypedDict(
    "BatchGetCommitsErrorTypeDef",
    {"commitId": str, "errorCode": str, "errorMessage": str},
    total=False,
)

UserInfoTypeDef = TypedDict(
    "UserInfoTypeDef", {"name": str, "email": str, "date": str}, total=False
)

CommitTypeDef = TypedDict(
    "CommitTypeDef",
    {
        "commitId": str,
        "treeId": str,
        "parents": List[str],
        "message": str,
        "author": UserInfoTypeDef,
        "committer": UserInfoTypeDef,
        "additionalData": str,
    },
    total=False,
)

BatchGetCommitsOutputTypeDef = TypedDict(
    "BatchGetCommitsOutputTypeDef",
    {"commits": List[CommitTypeDef], "errors": List[BatchGetCommitsErrorTypeDef]},
    total=False,
)

RepositoryMetadataTypeDef = TypedDict(
    "RepositoryMetadataTypeDef",
    {
        "accountId": str,
        "repositoryId": str,
        "repositoryName": str,
        "repositoryDescription": str,
        "defaultBranch": str,
        "lastModifiedDate": datetime,
        "creationDate": datetime,
        "cloneUrlHttp": str,
        "cloneUrlSsh": str,
        "Arn": str,
    },
    total=False,
)

BatchGetRepositoriesOutputTypeDef = TypedDict(
    "BatchGetRepositoriesOutputTypeDef",
    {"repositories": List[RepositoryMetadataTypeDef], "repositoriesNotFound": List[str]},
    total=False,
)

DeleteFileEntryTypeDef = TypedDict("DeleteFileEntryTypeDef", {"filePath": str})

_RequiredReplaceContentEntryTypeDef = TypedDict(
    "_RequiredReplaceContentEntryTypeDef",
    {
        "filePath": str,
        "replacementType": Literal[
            "KEEP_BASE", "KEEP_SOURCE", "KEEP_DESTINATION", "USE_NEW_CONTENT"
        ],
    },
)
_OptionalReplaceContentEntryTypeDef = TypedDict(
    "_OptionalReplaceContentEntryTypeDef",
    {"content": Union[bytes, IO], "fileMode": Literal["EXECUTABLE", "NORMAL", "SYMLINK"]},
    total=False,
)


class ReplaceContentEntryTypeDef(
    _RequiredReplaceContentEntryTypeDef, _OptionalReplaceContentEntryTypeDef
):
    pass


SetFileModeEntryTypeDef = TypedDict(
    "SetFileModeEntryTypeDef",
    {"filePath": str, "fileMode": Literal["EXECUTABLE", "NORMAL", "SYMLINK"]},
)

ConflictResolutionTypeDef = TypedDict(
    "ConflictResolutionTypeDef",
    {
        "replaceContents": List[ReplaceContentEntryTypeDef],
        "deleteFiles": List[DeleteFileEntryTypeDef],
        "setFileModes": List[SetFileModeEntryTypeDef],
    },
    total=False,
)

ApprovalRuleTemplateTypeDef = TypedDict(
    "ApprovalRuleTemplateTypeDef",
    {
        "approvalRuleTemplateId": str,
        "approvalRuleTemplateName": str,
        "approvalRuleTemplateDescription": str,
        "approvalRuleTemplateContent": str,
        "ruleContentSha256": str,
        "lastModifiedDate": datetime,
        "creationDate": datetime,
        "lastModifiedUser": str,
    },
    total=False,
)

CreateApprovalRuleTemplateOutputTypeDef = TypedDict(
    "CreateApprovalRuleTemplateOutputTypeDef", {"approvalRuleTemplate": ApprovalRuleTemplateTypeDef}
)

FileMetadataTypeDef = TypedDict(
    "FileMetadataTypeDef",
    {"absolutePath": str, "blobId": str, "fileMode": Literal["EXECUTABLE", "NORMAL", "SYMLINK"]},
    total=False,
)

CreateCommitOutputTypeDef = TypedDict(
    "CreateCommitOutputTypeDef",
    {
        "commitId": str,
        "treeId": str,
        "filesAdded": List[FileMetadataTypeDef],
        "filesUpdated": List[FileMetadataTypeDef],
        "filesDeleted": List[FileMetadataTypeDef],
    },
    total=False,
)

OriginApprovalRuleTemplateTypeDef = TypedDict(
    "OriginApprovalRuleTemplateTypeDef",
    {"approvalRuleTemplateId": str, "approvalRuleTemplateName": str},
    total=False,
)

ApprovalRuleTypeDef = TypedDict(
    "ApprovalRuleTypeDef",
    {
        "approvalRuleId": str,
        "approvalRuleName": str,
        "approvalRuleContent": str,
        "ruleContentSha256": str,
        "lastModifiedDate": datetime,
        "creationDate": datetime,
        "lastModifiedUser": str,
        "originApprovalRuleTemplate": OriginApprovalRuleTemplateTypeDef,
    },
    total=False,
)

CreatePullRequestApprovalRuleOutputTypeDef = TypedDict(
    "CreatePullRequestApprovalRuleOutputTypeDef", {"approvalRule": ApprovalRuleTypeDef}
)

MergeMetadataTypeDef = TypedDict(
    "MergeMetadataTypeDef",
    {
        "isMerged": bool,
        "mergedBy": str,
        "mergeCommitId": str,
        "mergeOption": Literal["FAST_FORWARD_MERGE", "SQUASH_MERGE", "THREE_WAY_MERGE"],
    },
    total=False,
)

PullRequestTargetTypeDef = TypedDict(
    "PullRequestTargetTypeDef",
    {
        "repositoryName": str,
        "sourceReference": str,
        "destinationReference": str,
        "destinationCommit": str,
        "sourceCommit": str,
        "mergeBase": str,
        "mergeMetadata": MergeMetadataTypeDef,
    },
    total=False,
)

PullRequestTypeDef = TypedDict(
    "PullRequestTypeDef",
    {
        "pullRequestId": str,
        "title": str,
        "description": str,
        "lastActivityDate": datetime,
        "creationDate": datetime,
        "pullRequestStatus": Literal["OPEN", "CLOSED"],
        "authorArn": str,
        "pullRequestTargets": List[PullRequestTargetTypeDef],
        "clientRequestToken": str,
        "revisionId": str,
        "approvalRules": List[ApprovalRuleTypeDef],
    },
    total=False,
)

CreatePullRequestOutputTypeDef = TypedDict(
    "CreatePullRequestOutputTypeDef", {"pullRequest": PullRequestTypeDef}
)

CreateRepositoryOutputTypeDef = TypedDict(
    "CreateRepositoryOutputTypeDef", {"repositoryMetadata": RepositoryMetadataTypeDef}, total=False
)

CreateUnreferencedMergeCommitOutputTypeDef = TypedDict(
    "CreateUnreferencedMergeCommitOutputTypeDef", {"commitId": str, "treeId": str}, total=False
)

DeleteApprovalRuleTemplateOutputTypeDef = TypedDict(
    "DeleteApprovalRuleTemplateOutputTypeDef", {"approvalRuleTemplateId": str}
)

BranchInfoTypeDef = TypedDict(
    "BranchInfoTypeDef", {"branchName": str, "commitId": str}, total=False
)

DeleteBranchOutputTypeDef = TypedDict(
    "DeleteBranchOutputTypeDef", {"deletedBranch": BranchInfoTypeDef}, total=False
)

CommentTypeDef = TypedDict(
    "CommentTypeDef",
    {
        "commentId": str,
        "content": str,
        "inReplyTo": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "authorArn": str,
        "deleted": bool,
        "clientRequestToken": str,
    },
    total=False,
)

DeleteCommentContentOutputTypeDef = TypedDict(
    "DeleteCommentContentOutputTypeDef", {"comment": CommentTypeDef}, total=False
)

DeleteFileOutputTypeDef = TypedDict(
    "DeleteFileOutputTypeDef", {"commitId": str, "blobId": str, "treeId": str, "filePath": str}
)

DeletePullRequestApprovalRuleOutputTypeDef = TypedDict(
    "DeletePullRequestApprovalRuleOutputTypeDef", {"approvalRuleId": str}
)

DeleteRepositoryOutputTypeDef = TypedDict(
    "DeleteRepositoryOutputTypeDef", {"repositoryId": str}, total=False
)

_RequiredDescribeMergeConflictsOutputTypeDef = TypedDict(
    "_RequiredDescribeMergeConflictsOutputTypeDef",
    {
        "conflictMetadata": ConflictMetadataTypeDef,
        "mergeHunks": List[MergeHunkTypeDef],
        "destinationCommitId": str,
        "sourceCommitId": str,
    },
)
_OptionalDescribeMergeConflictsOutputTypeDef = TypedDict(
    "_OptionalDescribeMergeConflictsOutputTypeDef",
    {"nextToken": str, "baseCommitId": str},
    total=False,
)


class DescribeMergeConflictsOutputTypeDef(
    _RequiredDescribeMergeConflictsOutputTypeDef, _OptionalDescribeMergeConflictsOutputTypeDef
):
    pass


ApprovalRuleEventMetadataTypeDef = TypedDict(
    "ApprovalRuleEventMetadataTypeDef",
    {"approvalRuleName": str, "approvalRuleId": str, "approvalRuleContent": str},
    total=False,
)

ApprovalRuleOverriddenEventMetadataTypeDef = TypedDict(
    "ApprovalRuleOverriddenEventMetadataTypeDef",
    {"revisionId": str, "overrideStatus": Literal["OVERRIDE", "REVOKE"]},
    total=False,
)

ApprovalStateChangedEventMetadataTypeDef = TypedDict(
    "ApprovalStateChangedEventMetadataTypeDef",
    {"revisionId": str, "approvalStatus": Literal["APPROVE", "REVOKE"]},
    total=False,
)

PullRequestCreatedEventMetadataTypeDef = TypedDict(
    "PullRequestCreatedEventMetadataTypeDef",
    {"repositoryName": str, "sourceCommitId": str, "destinationCommitId": str, "mergeBase": str},
    total=False,
)

PullRequestMergedStateChangedEventMetadataTypeDef = TypedDict(
    "PullRequestMergedStateChangedEventMetadataTypeDef",
    {"repositoryName": str, "destinationReference": str, "mergeMetadata": MergeMetadataTypeDef},
    total=False,
)

PullRequestSourceReferenceUpdatedEventMetadataTypeDef = TypedDict(
    "PullRequestSourceReferenceUpdatedEventMetadataTypeDef",
    {"repositoryName": str, "beforeCommitId": str, "afterCommitId": str, "mergeBase": str},
    total=False,
)

PullRequestStatusChangedEventMetadataTypeDef = TypedDict(
    "PullRequestStatusChangedEventMetadataTypeDef",
    {"pullRequestStatus": Literal["OPEN", "CLOSED"]},
    total=False,
)

PullRequestEventTypeDef = TypedDict(
    "PullRequestEventTypeDef",
    {
        "pullRequestId": str,
        "eventDate": datetime,
        "pullRequestEventType": Literal[
            "PULL_REQUEST_CREATED",
            "PULL_REQUEST_STATUS_CHANGED",
            "PULL_REQUEST_SOURCE_REFERENCE_UPDATED",
            "PULL_REQUEST_MERGE_STATE_CHANGED",
            "PULL_REQUEST_APPROVAL_RULE_CREATED",
            "PULL_REQUEST_APPROVAL_RULE_UPDATED",
            "PULL_REQUEST_APPROVAL_RULE_DELETED",
            "PULL_REQUEST_APPROVAL_RULE_OVERRIDDEN",
            "PULL_REQUEST_APPROVAL_STATE_CHANGED",
        ],
        "actorArn": str,
        "pullRequestCreatedEventMetadata": PullRequestCreatedEventMetadataTypeDef,
        "pullRequestStatusChangedEventMetadata": PullRequestStatusChangedEventMetadataTypeDef,
        "pullRequestSourceReferenceUpdatedEventMetadata": PullRequestSourceReferenceUpdatedEventMetadataTypeDef,
        "pullRequestMergedStateChangedEventMetadata": PullRequestMergedStateChangedEventMetadataTypeDef,
        "approvalRuleEventMetadata": ApprovalRuleEventMetadataTypeDef,
        "approvalStateChangedEventMetadata": ApprovalStateChangedEventMetadataTypeDef,
        "approvalRuleOverriddenEventMetadata": ApprovalRuleOverriddenEventMetadataTypeDef,
    },
    total=False,
)

_RequiredDescribePullRequestEventsOutputTypeDef = TypedDict(
    "_RequiredDescribePullRequestEventsOutputTypeDef",
    {"pullRequestEvents": List[PullRequestEventTypeDef]},
)
_OptionalDescribePullRequestEventsOutputTypeDef = TypedDict(
    "_OptionalDescribePullRequestEventsOutputTypeDef", {"nextToken": str}, total=False
)


class DescribePullRequestEventsOutputTypeDef(
    _RequiredDescribePullRequestEventsOutputTypeDef, _OptionalDescribePullRequestEventsOutputTypeDef
):
    pass


EvaluationTypeDef = TypedDict(
    "EvaluationTypeDef",
    {
        "approved": bool,
        "overridden": bool,
        "approvalRulesSatisfied": List[str],
        "approvalRulesNotSatisfied": List[str],
    },
    total=False,
)

EvaluatePullRequestApprovalRulesOutputTypeDef = TypedDict(
    "EvaluatePullRequestApprovalRulesOutputTypeDef", {"evaluation": EvaluationTypeDef}
)

GetApprovalRuleTemplateOutputTypeDef = TypedDict(
    "GetApprovalRuleTemplateOutputTypeDef", {"approvalRuleTemplate": ApprovalRuleTemplateTypeDef}
)

GetBlobOutputTypeDef = TypedDict("GetBlobOutputTypeDef", {"content": Union[bytes, IO]})

GetBranchOutputTypeDef = TypedDict(
    "GetBranchOutputTypeDef", {"branch": BranchInfoTypeDef}, total=False
)

GetCommentOutputTypeDef = TypedDict(
    "GetCommentOutputTypeDef", {"comment": CommentTypeDef}, total=False
)

LocationTypeDef = TypedDict(
    "LocationTypeDef",
    {"filePath": str, "filePosition": int, "relativeFileVersion": Literal["BEFORE", "AFTER"]},
    total=False,
)

CommentsForComparedCommitTypeDef = TypedDict(
    "CommentsForComparedCommitTypeDef",
    {
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "beforeBlobId": str,
        "afterBlobId": str,
        "location": LocationTypeDef,
        "comments": List[CommentTypeDef],
    },
    total=False,
)

GetCommentsForComparedCommitOutputTypeDef = TypedDict(
    "GetCommentsForComparedCommitOutputTypeDef",
    {"commentsForComparedCommitData": List[CommentsForComparedCommitTypeDef], "nextToken": str},
    total=False,
)

CommentsForPullRequestTypeDef = TypedDict(
    "CommentsForPullRequestTypeDef",
    {
        "pullRequestId": str,
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "beforeBlobId": str,
        "afterBlobId": str,
        "location": LocationTypeDef,
        "comments": List[CommentTypeDef],
    },
    total=False,
)

GetCommentsForPullRequestOutputTypeDef = TypedDict(
    "GetCommentsForPullRequestOutputTypeDef",
    {"commentsForPullRequestData": List[CommentsForPullRequestTypeDef], "nextToken": str},
    total=False,
)

GetCommitOutputTypeDef = TypedDict("GetCommitOutputTypeDef", {"commit": CommitTypeDef})

BlobMetadataTypeDef = TypedDict(
    "BlobMetadataTypeDef", {"blobId": str, "path": str, "mode": str}, total=False
)

DifferenceTypeDef = TypedDict(
    "DifferenceTypeDef",
    {
        "beforeBlob": BlobMetadataTypeDef,
        "afterBlob": BlobMetadataTypeDef,
        "changeType": Literal["A", "M", "D"],
    },
    total=False,
)

GetDifferencesOutputTypeDef = TypedDict(
    "GetDifferencesOutputTypeDef",
    {"differences": List[DifferenceTypeDef], "NextToken": str},
    total=False,
)

GetFileOutputTypeDef = TypedDict(
    "GetFileOutputTypeDef",
    {
        "commitId": str,
        "blobId": str,
        "filePath": str,
        "fileMode": Literal["EXECUTABLE", "NORMAL", "SYMLINK"],
        "fileSize": int,
        "fileContent": Union[bytes, IO],
    },
)

FileTypeDef = TypedDict(
    "FileTypeDef",
    {
        "blobId": str,
        "absolutePath": str,
        "relativePath": str,
        "fileMode": Literal["EXECUTABLE", "NORMAL", "SYMLINK"],
    },
    total=False,
)

FolderTypeDef = TypedDict(
    "FolderTypeDef", {"treeId": str, "absolutePath": str, "relativePath": str}, total=False
)

SubModuleTypeDef = TypedDict(
    "SubModuleTypeDef", {"commitId": str, "absolutePath": str, "relativePath": str}, total=False
)

SymbolicLinkTypeDef = TypedDict(
    "SymbolicLinkTypeDef",
    {
        "blobId": str,
        "absolutePath": str,
        "relativePath": str,
        "fileMode": Literal["EXECUTABLE", "NORMAL", "SYMLINK"],
    },
    total=False,
)

_RequiredGetFolderOutputTypeDef = TypedDict(
    "_RequiredGetFolderOutputTypeDef", {"commitId": str, "folderPath": str}
)
_OptionalGetFolderOutputTypeDef = TypedDict(
    "_OptionalGetFolderOutputTypeDef",
    {
        "treeId": str,
        "subFolders": List[FolderTypeDef],
        "files": List[FileTypeDef],
        "symbolicLinks": List[SymbolicLinkTypeDef],
        "subModules": List[SubModuleTypeDef],
    },
    total=False,
)


class GetFolderOutputTypeDef(_RequiredGetFolderOutputTypeDef, _OptionalGetFolderOutputTypeDef):
    pass


GetMergeCommitOutputTypeDef = TypedDict(
    "GetMergeCommitOutputTypeDef",
    {"sourceCommitId": str, "destinationCommitId": str, "baseCommitId": str, "mergedCommitId": str},
    total=False,
)

_RequiredGetMergeConflictsOutputTypeDef = TypedDict(
    "_RequiredGetMergeConflictsOutputTypeDef",
    {
        "mergeable": bool,
        "destinationCommitId": str,
        "sourceCommitId": str,
        "conflictMetadataList": List[ConflictMetadataTypeDef],
    },
)
_OptionalGetMergeConflictsOutputTypeDef = TypedDict(
    "_OptionalGetMergeConflictsOutputTypeDef", {"baseCommitId": str, "nextToken": str}, total=False
)


class GetMergeConflictsOutputTypeDef(
    _RequiredGetMergeConflictsOutputTypeDef, _OptionalGetMergeConflictsOutputTypeDef
):
    pass


GetMergeOptionsOutputTypeDef = TypedDict(
    "GetMergeOptionsOutputTypeDef",
    {
        "mergeOptions": List[Literal["FAST_FORWARD_MERGE", "SQUASH_MERGE", "THREE_WAY_MERGE"]],
        "sourceCommitId": str,
        "destinationCommitId": str,
        "baseCommitId": str,
    },
)

ApprovalTypeDef = TypedDict(
    "ApprovalTypeDef", {"userArn": str, "approvalState": Literal["APPROVE", "REVOKE"]}, total=False
)

GetPullRequestApprovalStatesOutputTypeDef = TypedDict(
    "GetPullRequestApprovalStatesOutputTypeDef", {"approvals": List[ApprovalTypeDef]}, total=False
)

GetPullRequestOutputTypeDef = TypedDict(
    "GetPullRequestOutputTypeDef", {"pullRequest": PullRequestTypeDef}
)

GetPullRequestOverrideStateOutputTypeDef = TypedDict(
    "GetPullRequestOverrideStateOutputTypeDef", {"overridden": bool, "overrider": str}, total=False
)

GetRepositoryOutputTypeDef = TypedDict(
    "GetRepositoryOutputTypeDef", {"repositoryMetadata": RepositoryMetadataTypeDef}, total=False
)

_RequiredRepositoryTriggerTypeDef = TypedDict(
    "_RequiredRepositoryTriggerTypeDef",
    {
        "name": str,
        "destinationArn": str,
        "events": List[Literal["all", "updateReference", "createReference", "deleteReference"]],
    },
)
_OptionalRepositoryTriggerTypeDef = TypedDict(
    "_OptionalRepositoryTriggerTypeDef", {"customData": str, "branches": List[str]}, total=False
)


class RepositoryTriggerTypeDef(
    _RequiredRepositoryTriggerTypeDef, _OptionalRepositoryTriggerTypeDef
):
    pass


GetRepositoryTriggersOutputTypeDef = TypedDict(
    "GetRepositoryTriggersOutputTypeDef",
    {"configurationId": str, "triggers": List[RepositoryTriggerTypeDef]},
    total=False,
)

ListApprovalRuleTemplatesOutputTypeDef = TypedDict(
    "ListApprovalRuleTemplatesOutputTypeDef",
    {"approvalRuleTemplateNames": List[str], "nextToken": str},
    total=False,
)

ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef = TypedDict(
    "ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef",
    {"approvalRuleTemplateNames": List[str], "nextToken": str},
    total=False,
)

ListBranchesOutputTypeDef = TypedDict(
    "ListBranchesOutputTypeDef", {"branches": List[str], "nextToken": str}, total=False
)

_RequiredListPullRequestsOutputTypeDef = TypedDict(
    "_RequiredListPullRequestsOutputTypeDef", {"pullRequestIds": List[str]}
)
_OptionalListPullRequestsOutputTypeDef = TypedDict(
    "_OptionalListPullRequestsOutputTypeDef", {"nextToken": str}, total=False
)


class ListPullRequestsOutputTypeDef(
    _RequiredListPullRequestsOutputTypeDef, _OptionalListPullRequestsOutputTypeDef
):
    pass


ListRepositoriesForApprovalRuleTemplateOutputTypeDef = TypedDict(
    "ListRepositoriesForApprovalRuleTemplateOutputTypeDef",
    {"repositoryNames": List[str], "nextToken": str},
    total=False,
)

RepositoryNameIdPairTypeDef = TypedDict(
    "RepositoryNameIdPairTypeDef", {"repositoryName": str, "repositoryId": str}, total=False
)

ListRepositoriesOutputTypeDef = TypedDict(
    "ListRepositoriesOutputTypeDef",
    {"repositories": List[RepositoryNameIdPairTypeDef], "nextToken": str},
    total=False,
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef", {"tags": Dict[str, str], "nextToken": str}, total=False
)

MergeBranchesByFastForwardOutputTypeDef = TypedDict(
    "MergeBranchesByFastForwardOutputTypeDef", {"commitId": str, "treeId": str}, total=False
)

MergeBranchesBySquashOutputTypeDef = TypedDict(
    "MergeBranchesBySquashOutputTypeDef", {"commitId": str, "treeId": str}, total=False
)

MergeBranchesByThreeWayOutputTypeDef = TypedDict(
    "MergeBranchesByThreeWayOutputTypeDef", {"commitId": str, "treeId": str}, total=False
)

MergePullRequestByFastForwardOutputTypeDef = TypedDict(
    "MergePullRequestByFastForwardOutputTypeDef", {"pullRequest": PullRequestTypeDef}, total=False
)

MergePullRequestBySquashOutputTypeDef = TypedDict(
    "MergePullRequestBySquashOutputTypeDef", {"pullRequest": PullRequestTypeDef}, total=False
)

MergePullRequestByThreeWayOutputTypeDef = TypedDict(
    "MergePullRequestByThreeWayOutputTypeDef", {"pullRequest": PullRequestTypeDef}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PostCommentForComparedCommitOutputTypeDef = TypedDict(
    "PostCommentForComparedCommitOutputTypeDef",
    {
        "repositoryName": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "beforeBlobId": str,
        "afterBlobId": str,
        "location": LocationTypeDef,
        "comment": CommentTypeDef,
    },
    total=False,
)

PostCommentForPullRequestOutputTypeDef = TypedDict(
    "PostCommentForPullRequestOutputTypeDef",
    {
        "repositoryName": str,
        "pullRequestId": str,
        "beforeCommitId": str,
        "afterCommitId": str,
        "beforeBlobId": str,
        "afterBlobId": str,
        "location": LocationTypeDef,
        "comment": CommentTypeDef,
    },
    total=False,
)

PostCommentReplyOutputTypeDef = TypedDict(
    "PostCommentReplyOutputTypeDef", {"comment": CommentTypeDef}, total=False
)

_RequiredSourceFileSpecifierTypeDef = TypedDict(
    "_RequiredSourceFileSpecifierTypeDef", {"filePath": str}
)
_OptionalSourceFileSpecifierTypeDef = TypedDict(
    "_OptionalSourceFileSpecifierTypeDef", {"isMove": bool}, total=False
)


class SourceFileSpecifierTypeDef(
    _RequiredSourceFileSpecifierTypeDef, _OptionalSourceFileSpecifierTypeDef
):
    pass


_RequiredPutFileEntryTypeDef = TypedDict("_RequiredPutFileEntryTypeDef", {"filePath": str})
_OptionalPutFileEntryTypeDef = TypedDict(
    "_OptionalPutFileEntryTypeDef",
    {
        "fileMode": Literal["EXECUTABLE", "NORMAL", "SYMLINK"],
        "fileContent": Union[bytes, IO],
        "sourceFile": SourceFileSpecifierTypeDef,
    },
    total=False,
)


class PutFileEntryTypeDef(_RequiredPutFileEntryTypeDef, _OptionalPutFileEntryTypeDef):
    pass


PutFileOutputTypeDef = TypedDict(
    "PutFileOutputTypeDef", {"commitId": str, "blobId": str, "treeId": str}
)

PutRepositoryTriggersOutputTypeDef = TypedDict(
    "PutRepositoryTriggersOutputTypeDef", {"configurationId": str}, total=False
)

_RequiredTargetTypeDef = TypedDict(
    "_RequiredTargetTypeDef", {"repositoryName": str, "sourceReference": str}
)
_OptionalTargetTypeDef = TypedDict(
    "_OptionalTargetTypeDef", {"destinationReference": str}, total=False
)


class TargetTypeDef(_RequiredTargetTypeDef, _OptionalTargetTypeDef):
    pass


RepositoryTriggerExecutionFailureTypeDef = TypedDict(
    "RepositoryTriggerExecutionFailureTypeDef", {"trigger": str, "failureMessage": str}, total=False
)

TestRepositoryTriggersOutputTypeDef = TypedDict(
    "TestRepositoryTriggersOutputTypeDef",
    {
        "successfulExecutions": List[str],
        "failedExecutions": List[RepositoryTriggerExecutionFailureTypeDef],
    },
    total=False,
)

UpdateApprovalRuleTemplateContentOutputTypeDef = TypedDict(
    "UpdateApprovalRuleTemplateContentOutputTypeDef",
    {"approvalRuleTemplate": ApprovalRuleTemplateTypeDef},
)

UpdateApprovalRuleTemplateDescriptionOutputTypeDef = TypedDict(
    "UpdateApprovalRuleTemplateDescriptionOutputTypeDef",
    {"approvalRuleTemplate": ApprovalRuleTemplateTypeDef},
)

UpdateApprovalRuleTemplateNameOutputTypeDef = TypedDict(
    "UpdateApprovalRuleTemplateNameOutputTypeDef",
    {"approvalRuleTemplate": ApprovalRuleTemplateTypeDef},
)

UpdateCommentOutputTypeDef = TypedDict(
    "UpdateCommentOutputTypeDef", {"comment": CommentTypeDef}, total=False
)

UpdatePullRequestApprovalRuleContentOutputTypeDef = TypedDict(
    "UpdatePullRequestApprovalRuleContentOutputTypeDef", {"approvalRule": ApprovalRuleTypeDef}
)

UpdatePullRequestDescriptionOutputTypeDef = TypedDict(
    "UpdatePullRequestDescriptionOutputTypeDef", {"pullRequest": PullRequestTypeDef}
)

UpdatePullRequestStatusOutputTypeDef = TypedDict(
    "UpdatePullRequestStatusOutputTypeDef", {"pullRequest": PullRequestTypeDef}
)

UpdatePullRequestTitleOutputTypeDef = TypedDict(
    "UpdatePullRequestTitleOutputTypeDef", {"pullRequest": PullRequestTypeDef}
)
