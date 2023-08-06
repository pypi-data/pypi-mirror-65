"""
Main interface for clouddirectory service type definitions.

Usage::

    from mypy_boto3.clouddirectory.type_defs import ApplySchemaResponseTypeDef

    data: ApplySchemaResponseTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Any, Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ApplySchemaResponseTypeDef",
    "AttachObjectResponseTypeDef",
    "AttachToIndexResponseTypeDef",
    "TypedAttributeValueTypeDef",
    "AttributeNameAndValueTypeDef",
    "ObjectReferenceTypeDef",
    "TypedLinkSchemaAndFacetNameTypeDef",
    "TypedLinkSpecifierTypeDef",
    "AttachTypedLinkResponseTypeDef",
    "AttributeKeyTypeDef",
    "AttributeKeyAndValueTypeDef",
    "BatchGetLinkAttributesTypeDef",
    "SchemaFacetTypeDef",
    "BatchGetObjectAttributesTypeDef",
    "BatchGetObjectInformationTypeDef",
    "BatchListAttachedIndicesTypeDef",
    "TypedAttributeValueRangeTypeDef",
    "TypedLinkAttributeRangeTypeDef",
    "BatchListIncomingTypedLinksTypeDef",
    "ObjectAttributeRangeTypeDef",
    "BatchListIndexTypeDef",
    "BatchListObjectAttributesTypeDef",
    "BatchListObjectChildrenTypeDef",
    "BatchListObjectParentPathsTypeDef",
    "BatchListObjectParentsTypeDef",
    "BatchListObjectPoliciesTypeDef",
    "BatchListOutgoingTypedLinksTypeDef",
    "BatchListPolicyAttachmentsTypeDef",
    "BatchLookupPolicyTypeDef",
    "BatchReadOperationTypeDef",
    "BatchReadExceptionTypeDef",
    "BatchGetLinkAttributesResponseTypeDef",
    "BatchGetObjectAttributesResponseTypeDef",
    "BatchGetObjectInformationResponseTypeDef",
    "IndexAttachmentTypeDef",
    "BatchListAttachedIndicesResponseTypeDef",
    "BatchListIncomingTypedLinksResponseTypeDef",
    "BatchListIndexResponseTypeDef",
    "BatchListObjectAttributesResponseTypeDef",
    "BatchListObjectChildrenResponseTypeDef",
    "PathToObjectIdentifiersTypeDef",
    "BatchListObjectParentPathsResponseTypeDef",
    "ObjectIdentifierAndLinkNameTupleTypeDef",
    "BatchListObjectParentsResponseTypeDef",
    "BatchListObjectPoliciesResponseTypeDef",
    "BatchListOutgoingTypedLinksResponseTypeDef",
    "BatchListPolicyAttachmentsResponseTypeDef",
    "PolicyAttachmentTypeDef",
    "PolicyToPathTypeDef",
    "BatchLookupPolicyResponseTypeDef",
    "BatchReadSuccessfulResponseTypeDef",
    "BatchReadOperationResponseTypeDef",
    "BatchReadResponseTypeDef",
    "BatchAddFacetToObjectTypeDef",
    "BatchAttachObjectTypeDef",
    "BatchAttachPolicyTypeDef",
    "BatchAttachToIndexTypeDef",
    "BatchAttachTypedLinkTypeDef",
    "BatchCreateIndexTypeDef",
    "BatchCreateObjectTypeDef",
    "BatchDeleteObjectTypeDef",
    "BatchDetachFromIndexTypeDef",
    "BatchDetachObjectTypeDef",
    "BatchDetachPolicyTypeDef",
    "BatchDetachTypedLinkTypeDef",
    "BatchRemoveFacetFromObjectTypeDef",
    "LinkAttributeActionTypeDef",
    "LinkAttributeUpdateTypeDef",
    "BatchUpdateLinkAttributesTypeDef",
    "ObjectAttributeActionTypeDef",
    "ObjectAttributeUpdateTypeDef",
    "BatchUpdateObjectAttributesTypeDef",
    "BatchWriteOperationTypeDef",
    "BatchAttachObjectResponseTypeDef",
    "BatchAttachToIndexResponseTypeDef",
    "BatchAttachTypedLinkResponseTypeDef",
    "BatchCreateIndexResponseTypeDef",
    "BatchCreateObjectResponseTypeDef",
    "BatchDetachFromIndexResponseTypeDef",
    "BatchDetachObjectResponseTypeDef",
    "BatchUpdateObjectAttributesResponseTypeDef",
    "BatchWriteOperationResponseTypeDef",
    "BatchWriteResponseTypeDef",
    "CreateDirectoryResponseTypeDef",
    "CreateIndexResponseTypeDef",
    "CreateObjectResponseTypeDef",
    "CreateSchemaResponseTypeDef",
    "DeleteDirectoryResponseTypeDef",
    "DeleteSchemaResponseTypeDef",
    "DetachFromIndexResponseTypeDef",
    "DetachObjectResponseTypeDef",
    "DisableDirectoryResponseTypeDef",
    "EnableDirectoryResponseTypeDef",
    "RuleTypeDef",
    "FacetAttributeDefinitionTypeDef",
    "FacetAttributeReferenceTypeDef",
    "FacetAttributeTypeDef",
    "FacetAttributeUpdateTypeDef",
    "GetAppliedSchemaVersionResponseTypeDef",
    "DirectoryTypeDef",
    "GetDirectoryResponseTypeDef",
    "FacetTypeDef",
    "GetFacetResponseTypeDef",
    "GetLinkAttributesResponseTypeDef",
    "GetObjectAttributesResponseTypeDef",
    "GetObjectInformationResponseTypeDef",
    "GetSchemaAsJsonResponseTypeDef",
    "GetTypedLinkFacetInformationResponseTypeDef",
    "ListAppliedSchemaArnsResponseTypeDef",
    "ListAttachedIndicesResponseTypeDef",
    "ListDevelopmentSchemaArnsResponseTypeDef",
    "ListDirectoriesResponseTypeDef",
    "ListFacetAttributesResponseTypeDef",
    "ListFacetNamesResponseTypeDef",
    "ListIncomingTypedLinksResponseTypeDef",
    "ListIndexResponseTypeDef",
    "ListManagedSchemaArnsResponseTypeDef",
    "ListObjectAttributesResponseTypeDef",
    "ListObjectChildrenResponseTypeDef",
    "ListObjectParentPathsResponseTypeDef",
    "ListObjectParentsResponseTypeDef",
    "ListObjectPoliciesResponseTypeDef",
    "ListOutgoingTypedLinksResponseTypeDef",
    "ListPolicyAttachmentsResponseTypeDef",
    "ListPublishedSchemaArnsResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TypedLinkAttributeDefinitionTypeDef",
    "ListTypedLinkFacetAttributesResponseTypeDef",
    "ListTypedLinkFacetNamesResponseTypeDef",
    "LookupPolicyResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PublishSchemaResponseTypeDef",
    "PutSchemaFromJsonResponseTypeDef",
    "TypedLinkFacetAttributeUpdateTypeDef",
    "TypedLinkFacetTypeDef",
    "UpdateObjectAttributesResponseTypeDef",
    "UpdateSchemaResponseTypeDef",
    "UpgradeAppliedSchemaResponseTypeDef",
    "UpgradePublishedSchemaResponseTypeDef",
)

ApplySchemaResponseTypeDef = TypedDict(
    "ApplySchemaResponseTypeDef", {"AppliedSchemaArn": str, "DirectoryArn": str}, total=False
)

AttachObjectResponseTypeDef = TypedDict(
    "AttachObjectResponseTypeDef", {"AttachedObjectIdentifier": str}, total=False
)

AttachToIndexResponseTypeDef = TypedDict(
    "AttachToIndexResponseTypeDef", {"AttachedObjectIdentifier": str}, total=False
)

TypedAttributeValueTypeDef = TypedDict(
    "TypedAttributeValueTypeDef",
    {
        "StringValue": str,
        "BinaryValue": Union[bytes, IO],
        "BooleanValue": bool,
        "NumberValue": str,
        "DatetimeValue": datetime,
    },
    total=False,
)

AttributeNameAndValueTypeDef = TypedDict(
    "AttributeNameAndValueTypeDef", {"AttributeName": str, "Value": TypedAttributeValueTypeDef}
)

ObjectReferenceTypeDef = TypedDict("ObjectReferenceTypeDef", {"Selector": str}, total=False)

TypedLinkSchemaAndFacetNameTypeDef = TypedDict(
    "TypedLinkSchemaAndFacetNameTypeDef", {"SchemaArn": str, "TypedLinkName": str}
)

TypedLinkSpecifierTypeDef = TypedDict(
    "TypedLinkSpecifierTypeDef",
    {
        "TypedLinkFacet": TypedLinkSchemaAndFacetNameTypeDef,
        "SourceObjectReference": ObjectReferenceTypeDef,
        "TargetObjectReference": ObjectReferenceTypeDef,
        "IdentityAttributeValues": List[AttributeNameAndValueTypeDef],
    },
)

AttachTypedLinkResponseTypeDef = TypedDict(
    "AttachTypedLinkResponseTypeDef", {"TypedLinkSpecifier": TypedLinkSpecifierTypeDef}, total=False
)

AttributeKeyTypeDef = TypedDict(
    "AttributeKeyTypeDef", {"SchemaArn": str, "FacetName": str, "Name": str}
)

AttributeKeyAndValueTypeDef = TypedDict(
    "AttributeKeyAndValueTypeDef", {"Key": AttributeKeyTypeDef, "Value": TypedAttributeValueTypeDef}
)

BatchGetLinkAttributesTypeDef = TypedDict(
    "BatchGetLinkAttributesTypeDef",
    {"TypedLinkSpecifier": TypedLinkSpecifierTypeDef, "AttributeNames": List[str]},
)

SchemaFacetTypeDef = TypedDict(
    "SchemaFacetTypeDef", {"SchemaArn": str, "FacetName": str}, total=False
)

BatchGetObjectAttributesTypeDef = TypedDict(
    "BatchGetObjectAttributesTypeDef",
    {
        "ObjectReference": ObjectReferenceTypeDef,
        "SchemaFacet": SchemaFacetTypeDef,
        "AttributeNames": List[str],
    },
)

BatchGetObjectInformationTypeDef = TypedDict(
    "BatchGetObjectInformationTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)

_RequiredBatchListAttachedIndicesTypeDef = TypedDict(
    "_RequiredBatchListAttachedIndicesTypeDef", {"TargetReference": ObjectReferenceTypeDef}
)
_OptionalBatchListAttachedIndicesTypeDef = TypedDict(
    "_OptionalBatchListAttachedIndicesTypeDef", {"NextToken": str, "MaxResults": int}, total=False
)


class BatchListAttachedIndicesTypeDef(
    _RequiredBatchListAttachedIndicesTypeDef, _OptionalBatchListAttachedIndicesTypeDef
):
    pass


_RequiredTypedAttributeValueRangeTypeDef = TypedDict(
    "_RequiredTypedAttributeValueRangeTypeDef",
    {
        "StartMode": Literal[
            "FIRST", "LAST", "LAST_BEFORE_MISSING_VALUES", "INCLUSIVE", "EXCLUSIVE"
        ],
        "EndMode": Literal["FIRST", "LAST", "LAST_BEFORE_MISSING_VALUES", "INCLUSIVE", "EXCLUSIVE"],
    },
)
_OptionalTypedAttributeValueRangeTypeDef = TypedDict(
    "_OptionalTypedAttributeValueRangeTypeDef",
    {"StartValue": TypedAttributeValueTypeDef, "EndValue": TypedAttributeValueTypeDef},
    total=False,
)


class TypedAttributeValueRangeTypeDef(
    _RequiredTypedAttributeValueRangeTypeDef, _OptionalTypedAttributeValueRangeTypeDef
):
    pass


_RequiredTypedLinkAttributeRangeTypeDef = TypedDict(
    "_RequiredTypedLinkAttributeRangeTypeDef", {"Range": TypedAttributeValueRangeTypeDef}
)
_OptionalTypedLinkAttributeRangeTypeDef = TypedDict(
    "_OptionalTypedLinkAttributeRangeTypeDef", {"AttributeName": str}, total=False
)


class TypedLinkAttributeRangeTypeDef(
    _RequiredTypedLinkAttributeRangeTypeDef, _OptionalTypedLinkAttributeRangeTypeDef
):
    pass


_RequiredBatchListIncomingTypedLinksTypeDef = TypedDict(
    "_RequiredBatchListIncomingTypedLinksTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)
_OptionalBatchListIncomingTypedLinksTypeDef = TypedDict(
    "_OptionalBatchListIncomingTypedLinksTypeDef",
    {
        "FilterAttributeRanges": List[TypedLinkAttributeRangeTypeDef],
        "FilterTypedLink": TypedLinkSchemaAndFacetNameTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class BatchListIncomingTypedLinksTypeDef(
    _RequiredBatchListIncomingTypedLinksTypeDef, _OptionalBatchListIncomingTypedLinksTypeDef
):
    pass


ObjectAttributeRangeTypeDef = TypedDict(
    "ObjectAttributeRangeTypeDef",
    {"AttributeKey": AttributeKeyTypeDef, "Range": TypedAttributeValueRangeTypeDef},
    total=False,
)

_RequiredBatchListIndexTypeDef = TypedDict(
    "_RequiredBatchListIndexTypeDef", {"IndexReference": ObjectReferenceTypeDef}
)
_OptionalBatchListIndexTypeDef = TypedDict(
    "_OptionalBatchListIndexTypeDef",
    {
        "RangesOnIndexedValues": List[ObjectAttributeRangeTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class BatchListIndexTypeDef(_RequiredBatchListIndexTypeDef, _OptionalBatchListIndexTypeDef):
    pass


_RequiredBatchListObjectAttributesTypeDef = TypedDict(
    "_RequiredBatchListObjectAttributesTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)
_OptionalBatchListObjectAttributesTypeDef = TypedDict(
    "_OptionalBatchListObjectAttributesTypeDef",
    {"NextToken": str, "MaxResults": int, "FacetFilter": SchemaFacetTypeDef},
    total=False,
)


class BatchListObjectAttributesTypeDef(
    _RequiredBatchListObjectAttributesTypeDef, _OptionalBatchListObjectAttributesTypeDef
):
    pass


_RequiredBatchListObjectChildrenTypeDef = TypedDict(
    "_RequiredBatchListObjectChildrenTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)
_OptionalBatchListObjectChildrenTypeDef = TypedDict(
    "_OptionalBatchListObjectChildrenTypeDef", {"NextToken": str, "MaxResults": int}, total=False
)


class BatchListObjectChildrenTypeDef(
    _RequiredBatchListObjectChildrenTypeDef, _OptionalBatchListObjectChildrenTypeDef
):
    pass


_RequiredBatchListObjectParentPathsTypeDef = TypedDict(
    "_RequiredBatchListObjectParentPathsTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)
_OptionalBatchListObjectParentPathsTypeDef = TypedDict(
    "_OptionalBatchListObjectParentPathsTypeDef", {"NextToken": str, "MaxResults": int}, total=False
)


class BatchListObjectParentPathsTypeDef(
    _RequiredBatchListObjectParentPathsTypeDef, _OptionalBatchListObjectParentPathsTypeDef
):
    pass


_RequiredBatchListObjectParentsTypeDef = TypedDict(
    "_RequiredBatchListObjectParentsTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)
_OptionalBatchListObjectParentsTypeDef = TypedDict(
    "_OptionalBatchListObjectParentsTypeDef", {"NextToken": str, "MaxResults": int}, total=False
)


class BatchListObjectParentsTypeDef(
    _RequiredBatchListObjectParentsTypeDef, _OptionalBatchListObjectParentsTypeDef
):
    pass


_RequiredBatchListObjectPoliciesTypeDef = TypedDict(
    "_RequiredBatchListObjectPoliciesTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)
_OptionalBatchListObjectPoliciesTypeDef = TypedDict(
    "_OptionalBatchListObjectPoliciesTypeDef", {"NextToken": str, "MaxResults": int}, total=False
)


class BatchListObjectPoliciesTypeDef(
    _RequiredBatchListObjectPoliciesTypeDef, _OptionalBatchListObjectPoliciesTypeDef
):
    pass


_RequiredBatchListOutgoingTypedLinksTypeDef = TypedDict(
    "_RequiredBatchListOutgoingTypedLinksTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)
_OptionalBatchListOutgoingTypedLinksTypeDef = TypedDict(
    "_OptionalBatchListOutgoingTypedLinksTypeDef",
    {
        "FilterAttributeRanges": List[TypedLinkAttributeRangeTypeDef],
        "FilterTypedLink": TypedLinkSchemaAndFacetNameTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class BatchListOutgoingTypedLinksTypeDef(
    _RequiredBatchListOutgoingTypedLinksTypeDef, _OptionalBatchListOutgoingTypedLinksTypeDef
):
    pass


_RequiredBatchListPolicyAttachmentsTypeDef = TypedDict(
    "_RequiredBatchListPolicyAttachmentsTypeDef", {"PolicyReference": ObjectReferenceTypeDef}
)
_OptionalBatchListPolicyAttachmentsTypeDef = TypedDict(
    "_OptionalBatchListPolicyAttachmentsTypeDef", {"NextToken": str, "MaxResults": int}, total=False
)


class BatchListPolicyAttachmentsTypeDef(
    _RequiredBatchListPolicyAttachmentsTypeDef, _OptionalBatchListPolicyAttachmentsTypeDef
):
    pass


_RequiredBatchLookupPolicyTypeDef = TypedDict(
    "_RequiredBatchLookupPolicyTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)
_OptionalBatchLookupPolicyTypeDef = TypedDict(
    "_OptionalBatchLookupPolicyTypeDef", {"NextToken": str, "MaxResults": int}, total=False
)


class BatchLookupPolicyTypeDef(
    _RequiredBatchLookupPolicyTypeDef, _OptionalBatchLookupPolicyTypeDef
):
    pass


BatchReadOperationTypeDef = TypedDict(
    "BatchReadOperationTypeDef",
    {
        "ListObjectAttributes": BatchListObjectAttributesTypeDef,
        "ListObjectChildren": BatchListObjectChildrenTypeDef,
        "ListAttachedIndices": BatchListAttachedIndicesTypeDef,
        "ListObjectParentPaths": BatchListObjectParentPathsTypeDef,
        "GetObjectInformation": BatchGetObjectInformationTypeDef,
        "GetObjectAttributes": BatchGetObjectAttributesTypeDef,
        "ListObjectParents": BatchListObjectParentsTypeDef,
        "ListObjectPolicies": BatchListObjectPoliciesTypeDef,
        "ListPolicyAttachments": BatchListPolicyAttachmentsTypeDef,
        "LookupPolicy": BatchLookupPolicyTypeDef,
        "ListIndex": BatchListIndexTypeDef,
        "ListOutgoingTypedLinks": BatchListOutgoingTypedLinksTypeDef,
        "ListIncomingTypedLinks": BatchListIncomingTypedLinksTypeDef,
        "GetLinkAttributes": BatchGetLinkAttributesTypeDef,
    },
    total=False,
)

BatchReadExceptionTypeDef = TypedDict(
    "BatchReadExceptionTypeDef",
    {
        "Type": Literal[
            "ValidationException",
            "InvalidArnException",
            "ResourceNotFoundException",
            "InvalidNextTokenException",
            "AccessDeniedException",
            "NotNodeException",
            "FacetValidationException",
            "CannotListParentOfRootException",
            "NotIndexException",
            "NotPolicyException",
            "DirectoryNotEnabledException",
            "LimitExceededException",
            "InternalServiceException",
        ],
        "Message": str,
    },
    total=False,
)

BatchGetLinkAttributesResponseTypeDef = TypedDict(
    "BatchGetLinkAttributesResponseTypeDef",
    {"Attributes": List[AttributeKeyAndValueTypeDef]},
    total=False,
)

BatchGetObjectAttributesResponseTypeDef = TypedDict(
    "BatchGetObjectAttributesResponseTypeDef",
    {"Attributes": List[AttributeKeyAndValueTypeDef]},
    total=False,
)

BatchGetObjectInformationResponseTypeDef = TypedDict(
    "BatchGetObjectInformationResponseTypeDef",
    {"SchemaFacets": List[SchemaFacetTypeDef], "ObjectIdentifier": str},
    total=False,
)

IndexAttachmentTypeDef = TypedDict(
    "IndexAttachmentTypeDef",
    {"IndexedAttributes": List[AttributeKeyAndValueTypeDef], "ObjectIdentifier": str},
    total=False,
)

BatchListAttachedIndicesResponseTypeDef = TypedDict(
    "BatchListAttachedIndicesResponseTypeDef",
    {"IndexAttachments": List[IndexAttachmentTypeDef], "NextToken": str},
    total=False,
)

BatchListIncomingTypedLinksResponseTypeDef = TypedDict(
    "BatchListIncomingTypedLinksResponseTypeDef",
    {"LinkSpecifiers": List[TypedLinkSpecifierTypeDef], "NextToken": str},
    total=False,
)

BatchListIndexResponseTypeDef = TypedDict(
    "BatchListIndexResponseTypeDef",
    {"IndexAttachments": List[IndexAttachmentTypeDef], "NextToken": str},
    total=False,
)

BatchListObjectAttributesResponseTypeDef = TypedDict(
    "BatchListObjectAttributesResponseTypeDef",
    {"Attributes": List[AttributeKeyAndValueTypeDef], "NextToken": str},
    total=False,
)

BatchListObjectChildrenResponseTypeDef = TypedDict(
    "BatchListObjectChildrenResponseTypeDef",
    {"Children": Dict[str, str], "NextToken": str},
    total=False,
)

PathToObjectIdentifiersTypeDef = TypedDict(
    "PathToObjectIdentifiersTypeDef", {"Path": str, "ObjectIdentifiers": List[str]}, total=False
)

BatchListObjectParentPathsResponseTypeDef = TypedDict(
    "BatchListObjectParentPathsResponseTypeDef",
    {"PathToObjectIdentifiersList": List[PathToObjectIdentifiersTypeDef], "NextToken": str},
    total=False,
)

ObjectIdentifierAndLinkNameTupleTypeDef = TypedDict(
    "ObjectIdentifierAndLinkNameTupleTypeDef",
    {"ObjectIdentifier": str, "LinkName": str},
    total=False,
)

BatchListObjectParentsResponseTypeDef = TypedDict(
    "BatchListObjectParentsResponseTypeDef",
    {"ParentLinks": List[ObjectIdentifierAndLinkNameTupleTypeDef], "NextToken": str},
    total=False,
)

BatchListObjectPoliciesResponseTypeDef = TypedDict(
    "BatchListObjectPoliciesResponseTypeDef",
    {"AttachedPolicyIds": List[str], "NextToken": str},
    total=False,
)

BatchListOutgoingTypedLinksResponseTypeDef = TypedDict(
    "BatchListOutgoingTypedLinksResponseTypeDef",
    {"TypedLinkSpecifiers": List[TypedLinkSpecifierTypeDef], "NextToken": str},
    total=False,
)

BatchListPolicyAttachmentsResponseTypeDef = TypedDict(
    "BatchListPolicyAttachmentsResponseTypeDef",
    {"ObjectIdentifiers": List[str], "NextToken": str},
    total=False,
)

PolicyAttachmentTypeDef = TypedDict(
    "PolicyAttachmentTypeDef",
    {"PolicyId": str, "ObjectIdentifier": str, "PolicyType": str},
    total=False,
)

PolicyToPathTypeDef = TypedDict(
    "PolicyToPathTypeDef", {"Path": str, "Policies": List[PolicyAttachmentTypeDef]}, total=False
)

BatchLookupPolicyResponseTypeDef = TypedDict(
    "BatchLookupPolicyResponseTypeDef",
    {"PolicyToPathList": List[PolicyToPathTypeDef], "NextToken": str},
    total=False,
)

BatchReadSuccessfulResponseTypeDef = TypedDict(
    "BatchReadSuccessfulResponseTypeDef",
    {
        "ListObjectAttributes": BatchListObjectAttributesResponseTypeDef,
        "ListObjectChildren": BatchListObjectChildrenResponseTypeDef,
        "GetObjectInformation": BatchGetObjectInformationResponseTypeDef,
        "GetObjectAttributes": BatchGetObjectAttributesResponseTypeDef,
        "ListAttachedIndices": BatchListAttachedIndicesResponseTypeDef,
        "ListObjectParentPaths": BatchListObjectParentPathsResponseTypeDef,
        "ListObjectPolicies": BatchListObjectPoliciesResponseTypeDef,
        "ListPolicyAttachments": BatchListPolicyAttachmentsResponseTypeDef,
        "LookupPolicy": BatchLookupPolicyResponseTypeDef,
        "ListIndex": BatchListIndexResponseTypeDef,
        "ListOutgoingTypedLinks": BatchListOutgoingTypedLinksResponseTypeDef,
        "ListIncomingTypedLinks": BatchListIncomingTypedLinksResponseTypeDef,
        "GetLinkAttributes": BatchGetLinkAttributesResponseTypeDef,
        "ListObjectParents": BatchListObjectParentsResponseTypeDef,
    },
    total=False,
)

BatchReadOperationResponseTypeDef = TypedDict(
    "BatchReadOperationResponseTypeDef",
    {
        "SuccessfulResponse": BatchReadSuccessfulResponseTypeDef,
        "ExceptionResponse": BatchReadExceptionTypeDef,
    },
    total=False,
)

BatchReadResponseTypeDef = TypedDict(
    "BatchReadResponseTypeDef", {"Responses": List[BatchReadOperationResponseTypeDef]}, total=False
)

BatchAddFacetToObjectTypeDef = TypedDict(
    "BatchAddFacetToObjectTypeDef",
    {
        "SchemaFacet": SchemaFacetTypeDef,
        "ObjectAttributeList": List[AttributeKeyAndValueTypeDef],
        "ObjectReference": ObjectReferenceTypeDef,
    },
)

BatchAttachObjectTypeDef = TypedDict(
    "BatchAttachObjectTypeDef",
    {
        "ParentReference": ObjectReferenceTypeDef,
        "ChildReference": ObjectReferenceTypeDef,
        "LinkName": str,
    },
)

BatchAttachPolicyTypeDef = TypedDict(
    "BatchAttachPolicyTypeDef",
    {"PolicyReference": ObjectReferenceTypeDef, "ObjectReference": ObjectReferenceTypeDef},
)

BatchAttachToIndexTypeDef = TypedDict(
    "BatchAttachToIndexTypeDef",
    {"IndexReference": ObjectReferenceTypeDef, "TargetReference": ObjectReferenceTypeDef},
)

BatchAttachTypedLinkTypeDef = TypedDict(
    "BatchAttachTypedLinkTypeDef",
    {
        "SourceObjectReference": ObjectReferenceTypeDef,
        "TargetObjectReference": ObjectReferenceTypeDef,
        "TypedLinkFacet": TypedLinkSchemaAndFacetNameTypeDef,
        "Attributes": List[AttributeNameAndValueTypeDef],
    },
)

_RequiredBatchCreateIndexTypeDef = TypedDict(
    "_RequiredBatchCreateIndexTypeDef",
    {"OrderedIndexedAttributeList": List[AttributeKeyTypeDef], "IsUnique": bool},
)
_OptionalBatchCreateIndexTypeDef = TypedDict(
    "_OptionalBatchCreateIndexTypeDef",
    {"ParentReference": ObjectReferenceTypeDef, "LinkName": str, "BatchReferenceName": str},
    total=False,
)


class BatchCreateIndexTypeDef(_RequiredBatchCreateIndexTypeDef, _OptionalBatchCreateIndexTypeDef):
    pass


_RequiredBatchCreateObjectTypeDef = TypedDict(
    "_RequiredBatchCreateObjectTypeDef",
    {
        "SchemaFacet": List[SchemaFacetTypeDef],
        "ObjectAttributeList": List[AttributeKeyAndValueTypeDef],
    },
)
_OptionalBatchCreateObjectTypeDef = TypedDict(
    "_OptionalBatchCreateObjectTypeDef",
    {"ParentReference": ObjectReferenceTypeDef, "LinkName": str, "BatchReferenceName": str},
    total=False,
)


class BatchCreateObjectTypeDef(
    _RequiredBatchCreateObjectTypeDef, _OptionalBatchCreateObjectTypeDef
):
    pass


BatchDeleteObjectTypeDef = TypedDict(
    "BatchDeleteObjectTypeDef", {"ObjectReference": ObjectReferenceTypeDef}
)

BatchDetachFromIndexTypeDef = TypedDict(
    "BatchDetachFromIndexTypeDef",
    {"IndexReference": ObjectReferenceTypeDef, "TargetReference": ObjectReferenceTypeDef},
)

_RequiredBatchDetachObjectTypeDef = TypedDict(
    "_RequiredBatchDetachObjectTypeDef",
    {"ParentReference": ObjectReferenceTypeDef, "LinkName": str},
)
_OptionalBatchDetachObjectTypeDef = TypedDict(
    "_OptionalBatchDetachObjectTypeDef", {"BatchReferenceName": str}, total=False
)


class BatchDetachObjectTypeDef(
    _RequiredBatchDetachObjectTypeDef, _OptionalBatchDetachObjectTypeDef
):
    pass


BatchDetachPolicyTypeDef = TypedDict(
    "BatchDetachPolicyTypeDef",
    {"PolicyReference": ObjectReferenceTypeDef, "ObjectReference": ObjectReferenceTypeDef},
)

BatchDetachTypedLinkTypeDef = TypedDict(
    "BatchDetachTypedLinkTypeDef", {"TypedLinkSpecifier": TypedLinkSpecifierTypeDef}
)

BatchRemoveFacetFromObjectTypeDef = TypedDict(
    "BatchRemoveFacetFromObjectTypeDef",
    {"SchemaFacet": SchemaFacetTypeDef, "ObjectReference": ObjectReferenceTypeDef},
)

LinkAttributeActionTypeDef = TypedDict(
    "LinkAttributeActionTypeDef",
    {
        "AttributeActionType": Literal["CREATE_OR_UPDATE", "DELETE"],
        "AttributeUpdateValue": TypedAttributeValueTypeDef,
    },
    total=False,
)

LinkAttributeUpdateTypeDef = TypedDict(
    "LinkAttributeUpdateTypeDef",
    {"AttributeKey": AttributeKeyTypeDef, "AttributeAction": LinkAttributeActionTypeDef},
    total=False,
)

BatchUpdateLinkAttributesTypeDef = TypedDict(
    "BatchUpdateLinkAttributesTypeDef",
    {
        "TypedLinkSpecifier": TypedLinkSpecifierTypeDef,
        "AttributeUpdates": List[LinkAttributeUpdateTypeDef],
    },
)

ObjectAttributeActionTypeDef = TypedDict(
    "ObjectAttributeActionTypeDef",
    {
        "ObjectAttributeActionType": Literal["CREATE_OR_UPDATE", "DELETE"],
        "ObjectAttributeUpdateValue": TypedAttributeValueTypeDef,
    },
    total=False,
)

ObjectAttributeUpdateTypeDef = TypedDict(
    "ObjectAttributeUpdateTypeDef",
    {
        "ObjectAttributeKey": AttributeKeyTypeDef,
        "ObjectAttributeAction": ObjectAttributeActionTypeDef,
    },
    total=False,
)

BatchUpdateObjectAttributesTypeDef = TypedDict(
    "BatchUpdateObjectAttributesTypeDef",
    {
        "ObjectReference": ObjectReferenceTypeDef,
        "AttributeUpdates": List[ObjectAttributeUpdateTypeDef],
    },
)

BatchWriteOperationTypeDef = TypedDict(
    "BatchWriteOperationTypeDef",
    {
        "CreateObject": BatchCreateObjectTypeDef,
        "AttachObject": BatchAttachObjectTypeDef,
        "DetachObject": BatchDetachObjectTypeDef,
        "UpdateObjectAttributes": BatchUpdateObjectAttributesTypeDef,
        "DeleteObject": BatchDeleteObjectTypeDef,
        "AddFacetToObject": BatchAddFacetToObjectTypeDef,
        "RemoveFacetFromObject": BatchRemoveFacetFromObjectTypeDef,
        "AttachPolicy": BatchAttachPolicyTypeDef,
        "DetachPolicy": BatchDetachPolicyTypeDef,
        "CreateIndex": BatchCreateIndexTypeDef,
        "AttachToIndex": BatchAttachToIndexTypeDef,
        "DetachFromIndex": BatchDetachFromIndexTypeDef,
        "AttachTypedLink": BatchAttachTypedLinkTypeDef,
        "DetachTypedLink": BatchDetachTypedLinkTypeDef,
        "UpdateLinkAttributes": BatchUpdateLinkAttributesTypeDef,
    },
    total=False,
)

BatchAttachObjectResponseTypeDef = TypedDict(
    "BatchAttachObjectResponseTypeDef", {"attachedObjectIdentifier": str}, total=False
)

BatchAttachToIndexResponseTypeDef = TypedDict(
    "BatchAttachToIndexResponseTypeDef", {"AttachedObjectIdentifier": str}, total=False
)

BatchAttachTypedLinkResponseTypeDef = TypedDict(
    "BatchAttachTypedLinkResponseTypeDef",
    {"TypedLinkSpecifier": TypedLinkSpecifierTypeDef},
    total=False,
)

BatchCreateIndexResponseTypeDef = TypedDict(
    "BatchCreateIndexResponseTypeDef", {"ObjectIdentifier": str}, total=False
)

BatchCreateObjectResponseTypeDef = TypedDict(
    "BatchCreateObjectResponseTypeDef", {"ObjectIdentifier": str}, total=False
)

BatchDetachFromIndexResponseTypeDef = TypedDict(
    "BatchDetachFromIndexResponseTypeDef", {"DetachedObjectIdentifier": str}, total=False
)

BatchDetachObjectResponseTypeDef = TypedDict(
    "BatchDetachObjectResponseTypeDef", {"detachedObjectIdentifier": str}, total=False
)

BatchUpdateObjectAttributesResponseTypeDef = TypedDict(
    "BatchUpdateObjectAttributesResponseTypeDef", {"ObjectIdentifier": str}, total=False
)

BatchWriteOperationResponseTypeDef = TypedDict(
    "BatchWriteOperationResponseTypeDef",
    {
        "CreateObject": BatchCreateObjectResponseTypeDef,
        "AttachObject": BatchAttachObjectResponseTypeDef,
        "DetachObject": BatchDetachObjectResponseTypeDef,
        "UpdateObjectAttributes": BatchUpdateObjectAttributesResponseTypeDef,
        "DeleteObject": Dict[str, Any],
        "AddFacetToObject": Dict[str, Any],
        "RemoveFacetFromObject": Dict[str, Any],
        "AttachPolicy": Dict[str, Any],
        "DetachPolicy": Dict[str, Any],
        "CreateIndex": BatchCreateIndexResponseTypeDef,
        "AttachToIndex": BatchAttachToIndexResponseTypeDef,
        "DetachFromIndex": BatchDetachFromIndexResponseTypeDef,
        "AttachTypedLink": BatchAttachTypedLinkResponseTypeDef,
        "DetachTypedLink": Dict[str, Any],
        "UpdateLinkAttributes": Dict[str, Any],
    },
    total=False,
)

BatchWriteResponseTypeDef = TypedDict(
    "BatchWriteResponseTypeDef",
    {"Responses": List[BatchWriteOperationResponseTypeDef]},
    total=False,
)

CreateDirectoryResponseTypeDef = TypedDict(
    "CreateDirectoryResponseTypeDef",
    {"DirectoryArn": str, "Name": str, "ObjectIdentifier": str, "AppliedSchemaArn": str},
)

CreateIndexResponseTypeDef = TypedDict(
    "CreateIndexResponseTypeDef", {"ObjectIdentifier": str}, total=False
)

CreateObjectResponseTypeDef = TypedDict(
    "CreateObjectResponseTypeDef", {"ObjectIdentifier": str}, total=False
)

CreateSchemaResponseTypeDef = TypedDict(
    "CreateSchemaResponseTypeDef", {"SchemaArn": str}, total=False
)

DeleteDirectoryResponseTypeDef = TypedDict("DeleteDirectoryResponseTypeDef", {"DirectoryArn": str})

DeleteSchemaResponseTypeDef = TypedDict(
    "DeleteSchemaResponseTypeDef", {"SchemaArn": str}, total=False
)

DetachFromIndexResponseTypeDef = TypedDict(
    "DetachFromIndexResponseTypeDef", {"DetachedObjectIdentifier": str}, total=False
)

DetachObjectResponseTypeDef = TypedDict(
    "DetachObjectResponseTypeDef", {"DetachedObjectIdentifier": str}, total=False
)

DisableDirectoryResponseTypeDef = TypedDict(
    "DisableDirectoryResponseTypeDef", {"DirectoryArn": str}
)

EnableDirectoryResponseTypeDef = TypedDict("EnableDirectoryResponseTypeDef", {"DirectoryArn": str})

RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "Type": Literal["BINARY_LENGTH", "NUMBER_COMPARISON", "STRING_FROM_SET", "STRING_LENGTH"],
        "Parameters": Dict[str, str],
    },
    total=False,
)

_RequiredFacetAttributeDefinitionTypeDef = TypedDict(
    "_RequiredFacetAttributeDefinitionTypeDef",
    {"Type": Literal["STRING", "BINARY", "BOOLEAN", "NUMBER", "DATETIME", "VARIANT"]},
)
_OptionalFacetAttributeDefinitionTypeDef = TypedDict(
    "_OptionalFacetAttributeDefinitionTypeDef",
    {
        "DefaultValue": TypedAttributeValueTypeDef,
        "IsImmutable": bool,
        "Rules": Dict[str, RuleTypeDef],
    },
    total=False,
)


class FacetAttributeDefinitionTypeDef(
    _RequiredFacetAttributeDefinitionTypeDef, _OptionalFacetAttributeDefinitionTypeDef
):
    pass


FacetAttributeReferenceTypeDef = TypedDict(
    "FacetAttributeReferenceTypeDef", {"TargetFacetName": str, "TargetAttributeName": str}
)

_RequiredFacetAttributeTypeDef = TypedDict("_RequiredFacetAttributeTypeDef", {"Name": str})
_OptionalFacetAttributeTypeDef = TypedDict(
    "_OptionalFacetAttributeTypeDef",
    {
        "AttributeDefinition": FacetAttributeDefinitionTypeDef,
        "AttributeReference": FacetAttributeReferenceTypeDef,
        "RequiredBehavior": Literal["REQUIRED_ALWAYS", "NOT_REQUIRED"],
    },
    total=False,
)


class FacetAttributeTypeDef(_RequiredFacetAttributeTypeDef, _OptionalFacetAttributeTypeDef):
    pass


FacetAttributeUpdateTypeDef = TypedDict(
    "FacetAttributeUpdateTypeDef",
    {"Attribute": FacetAttributeTypeDef, "Action": Literal["CREATE_OR_UPDATE", "DELETE"]},
    total=False,
)

GetAppliedSchemaVersionResponseTypeDef = TypedDict(
    "GetAppliedSchemaVersionResponseTypeDef", {"AppliedSchemaArn": str}, total=False
)

DirectoryTypeDef = TypedDict(
    "DirectoryTypeDef",
    {
        "Name": str,
        "DirectoryArn": str,
        "State": Literal["ENABLED", "DISABLED", "DELETED"],
        "CreationDateTime": datetime,
    },
    total=False,
)

GetDirectoryResponseTypeDef = TypedDict(
    "GetDirectoryResponseTypeDef", {"Directory": DirectoryTypeDef}
)

FacetTypeDef = TypedDict(
    "FacetTypeDef",
    {
        "Name": str,
        "ObjectType": Literal["NODE", "LEAF_NODE", "POLICY", "INDEX"],
        "FacetStyle": Literal["STATIC", "DYNAMIC"],
    },
    total=False,
)

GetFacetResponseTypeDef = TypedDict("GetFacetResponseTypeDef", {"Facet": FacetTypeDef}, total=False)

GetLinkAttributesResponseTypeDef = TypedDict(
    "GetLinkAttributesResponseTypeDef",
    {"Attributes": List[AttributeKeyAndValueTypeDef]},
    total=False,
)

GetObjectAttributesResponseTypeDef = TypedDict(
    "GetObjectAttributesResponseTypeDef",
    {"Attributes": List[AttributeKeyAndValueTypeDef]},
    total=False,
)

GetObjectInformationResponseTypeDef = TypedDict(
    "GetObjectInformationResponseTypeDef",
    {"SchemaFacets": List[SchemaFacetTypeDef], "ObjectIdentifier": str},
    total=False,
)

GetSchemaAsJsonResponseTypeDef = TypedDict(
    "GetSchemaAsJsonResponseTypeDef", {"Name": str, "Document": str}, total=False
)

GetTypedLinkFacetInformationResponseTypeDef = TypedDict(
    "GetTypedLinkFacetInformationResponseTypeDef",
    {"IdentityAttributeOrder": List[str]},
    total=False,
)

ListAppliedSchemaArnsResponseTypeDef = TypedDict(
    "ListAppliedSchemaArnsResponseTypeDef", {"SchemaArns": List[str], "NextToken": str}, total=False
)

ListAttachedIndicesResponseTypeDef = TypedDict(
    "ListAttachedIndicesResponseTypeDef",
    {"IndexAttachments": List[IndexAttachmentTypeDef], "NextToken": str},
    total=False,
)

ListDevelopmentSchemaArnsResponseTypeDef = TypedDict(
    "ListDevelopmentSchemaArnsResponseTypeDef",
    {"SchemaArns": List[str], "NextToken": str},
    total=False,
)

_RequiredListDirectoriesResponseTypeDef = TypedDict(
    "_RequiredListDirectoriesResponseTypeDef", {"Directories": List[DirectoryTypeDef]}
)
_OptionalListDirectoriesResponseTypeDef = TypedDict(
    "_OptionalListDirectoriesResponseTypeDef", {"NextToken": str}, total=False
)


class ListDirectoriesResponseTypeDef(
    _RequiredListDirectoriesResponseTypeDef, _OptionalListDirectoriesResponseTypeDef
):
    pass


ListFacetAttributesResponseTypeDef = TypedDict(
    "ListFacetAttributesResponseTypeDef",
    {"Attributes": List[FacetAttributeTypeDef], "NextToken": str},
    total=False,
)

ListFacetNamesResponseTypeDef = TypedDict(
    "ListFacetNamesResponseTypeDef", {"FacetNames": List[str], "NextToken": str}, total=False
)

ListIncomingTypedLinksResponseTypeDef = TypedDict(
    "ListIncomingTypedLinksResponseTypeDef",
    {"LinkSpecifiers": List[TypedLinkSpecifierTypeDef], "NextToken": str},
    total=False,
)

ListIndexResponseTypeDef = TypedDict(
    "ListIndexResponseTypeDef",
    {"IndexAttachments": List[IndexAttachmentTypeDef], "NextToken": str},
    total=False,
)

ListManagedSchemaArnsResponseTypeDef = TypedDict(
    "ListManagedSchemaArnsResponseTypeDef", {"SchemaArns": List[str], "NextToken": str}, total=False
)

ListObjectAttributesResponseTypeDef = TypedDict(
    "ListObjectAttributesResponseTypeDef",
    {"Attributes": List[AttributeKeyAndValueTypeDef], "NextToken": str},
    total=False,
)

ListObjectChildrenResponseTypeDef = TypedDict(
    "ListObjectChildrenResponseTypeDef", {"Children": Dict[str, str], "NextToken": str}, total=False
)

ListObjectParentPathsResponseTypeDef = TypedDict(
    "ListObjectParentPathsResponseTypeDef",
    {"PathToObjectIdentifiersList": List[PathToObjectIdentifiersTypeDef], "NextToken": str},
    total=False,
)

ListObjectParentsResponseTypeDef = TypedDict(
    "ListObjectParentsResponseTypeDef",
    {
        "Parents": Dict[str, str],
        "NextToken": str,
        "ParentLinks": List[ObjectIdentifierAndLinkNameTupleTypeDef],
    },
    total=False,
)

ListObjectPoliciesResponseTypeDef = TypedDict(
    "ListObjectPoliciesResponseTypeDef",
    {"AttachedPolicyIds": List[str], "NextToken": str},
    total=False,
)

ListOutgoingTypedLinksResponseTypeDef = TypedDict(
    "ListOutgoingTypedLinksResponseTypeDef",
    {"TypedLinkSpecifiers": List[TypedLinkSpecifierTypeDef], "NextToken": str},
    total=False,
)

ListPolicyAttachmentsResponseTypeDef = TypedDict(
    "ListPolicyAttachmentsResponseTypeDef",
    {"ObjectIdentifiers": List[str], "NextToken": str},
    total=False,
)

ListPublishedSchemaArnsResponseTypeDef = TypedDict(
    "ListPublishedSchemaArnsResponseTypeDef",
    {"SchemaArns": List[str], "NextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str}, total=False)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef], "NextToken": str}, total=False
)

_RequiredTypedLinkAttributeDefinitionTypeDef = TypedDict(
    "_RequiredTypedLinkAttributeDefinitionTypeDef",
    {
        "Name": str,
        "Type": Literal["STRING", "BINARY", "BOOLEAN", "NUMBER", "DATETIME", "VARIANT"],
        "RequiredBehavior": Literal["REQUIRED_ALWAYS", "NOT_REQUIRED"],
    },
)
_OptionalTypedLinkAttributeDefinitionTypeDef = TypedDict(
    "_OptionalTypedLinkAttributeDefinitionTypeDef",
    {
        "DefaultValue": TypedAttributeValueTypeDef,
        "IsImmutable": bool,
        "Rules": Dict[str, RuleTypeDef],
    },
    total=False,
)


class TypedLinkAttributeDefinitionTypeDef(
    _RequiredTypedLinkAttributeDefinitionTypeDef, _OptionalTypedLinkAttributeDefinitionTypeDef
):
    pass


ListTypedLinkFacetAttributesResponseTypeDef = TypedDict(
    "ListTypedLinkFacetAttributesResponseTypeDef",
    {"Attributes": List[TypedLinkAttributeDefinitionTypeDef], "NextToken": str},
    total=False,
)

ListTypedLinkFacetNamesResponseTypeDef = TypedDict(
    "ListTypedLinkFacetNamesResponseTypeDef",
    {"FacetNames": List[str], "NextToken": str},
    total=False,
)

LookupPolicyResponseTypeDef = TypedDict(
    "LookupPolicyResponseTypeDef",
    {"PolicyToPathList": List[PolicyToPathTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PublishSchemaResponseTypeDef = TypedDict(
    "PublishSchemaResponseTypeDef", {"PublishedSchemaArn": str}, total=False
)

PutSchemaFromJsonResponseTypeDef = TypedDict(
    "PutSchemaFromJsonResponseTypeDef", {"Arn": str}, total=False
)

TypedLinkFacetAttributeUpdateTypeDef = TypedDict(
    "TypedLinkFacetAttributeUpdateTypeDef",
    {
        "Attribute": TypedLinkAttributeDefinitionTypeDef,
        "Action": Literal["CREATE_OR_UPDATE", "DELETE"],
    },
)

TypedLinkFacetTypeDef = TypedDict(
    "TypedLinkFacetTypeDef",
    {
        "Name": str,
        "Attributes": List[TypedLinkAttributeDefinitionTypeDef],
        "IdentityAttributeOrder": List[str],
    },
)

UpdateObjectAttributesResponseTypeDef = TypedDict(
    "UpdateObjectAttributesResponseTypeDef", {"ObjectIdentifier": str}, total=False
)

UpdateSchemaResponseTypeDef = TypedDict(
    "UpdateSchemaResponseTypeDef", {"SchemaArn": str}, total=False
)

UpgradeAppliedSchemaResponseTypeDef = TypedDict(
    "UpgradeAppliedSchemaResponseTypeDef",
    {"UpgradedSchemaArn": str, "DirectoryArn": str},
    total=False,
)

UpgradePublishedSchemaResponseTypeDef = TypedDict(
    "UpgradePublishedSchemaResponseTypeDef", {"UpgradedSchemaArn": str}, total=False
)
