"""
Main interface for cloudsearch service type definitions.

Usage::

    from mypy_boto3.cloudsearch.type_defs import AnalysisOptionsTypeDef

    data: AnalysisOptionsTypeDef = {...}
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
    "AnalysisOptionsTypeDef",
    "AnalysisSchemeTypeDef",
    "BuildSuggestersResponseTypeDef",
    "LimitsTypeDef",
    "ServiceEndpointTypeDef",
    "DomainStatusTypeDef",
    "CreateDomainResponseTypeDef",
    "OptionStatusTypeDef",
    "AnalysisSchemeStatusTypeDef",
    "DefineAnalysisSchemeResponseTypeDef",
    "ExpressionTypeDef",
    "ExpressionStatusTypeDef",
    "DefineExpressionResponseTypeDef",
    "DateArrayOptionsTypeDef",
    "DateOptionsTypeDef",
    "DoubleArrayOptionsTypeDef",
    "DoubleOptionsTypeDef",
    "IntArrayOptionsTypeDef",
    "IntOptionsTypeDef",
    "LatLonOptionsTypeDef",
    "LiteralArrayOptionsTypeDef",
    "LiteralOptionsTypeDef",
    "TextArrayOptionsTypeDef",
    "TextOptionsTypeDef",
    "IndexFieldTypeDef",
    "IndexFieldStatusTypeDef",
    "DefineIndexFieldResponseTypeDef",
    "DocumentSuggesterOptionsTypeDef",
    "SuggesterTypeDef",
    "SuggesterStatusTypeDef",
    "DefineSuggesterResponseTypeDef",
    "DeleteAnalysisSchemeResponseTypeDef",
    "DeleteDomainResponseTypeDef",
    "DeleteExpressionResponseTypeDef",
    "DeleteIndexFieldResponseTypeDef",
    "DeleteSuggesterResponseTypeDef",
    "DescribeAnalysisSchemesResponseTypeDef",
    "AvailabilityOptionsStatusTypeDef",
    "DescribeAvailabilityOptionsResponseTypeDef",
    "DomainEndpointOptionsTypeDef",
    "DomainEndpointOptionsStatusTypeDef",
    "DescribeDomainEndpointOptionsResponseTypeDef",
    "DescribeDomainsResponseTypeDef",
    "DescribeExpressionsResponseTypeDef",
    "DescribeIndexFieldsResponseTypeDef",
    "ScalingParametersTypeDef",
    "ScalingParametersStatusTypeDef",
    "DescribeScalingParametersResponseTypeDef",
    "AccessPoliciesStatusTypeDef",
    "DescribeServiceAccessPoliciesResponseTypeDef",
    "DescribeSuggestersResponseTypeDef",
    "IndexDocumentsResponseTypeDef",
    "ListDomainNamesResponseTypeDef",
    "UpdateAvailabilityOptionsResponseTypeDef",
    "UpdateDomainEndpointOptionsResponseTypeDef",
    "UpdateScalingParametersResponseTypeDef",
    "UpdateServiceAccessPoliciesResponseTypeDef",
)

AnalysisOptionsTypeDef = TypedDict(
    "AnalysisOptionsTypeDef",
    {
        "Synonyms": str,
        "Stopwords": str,
        "StemmingDictionary": str,
        "JapaneseTokenizationDictionary": str,
        "AlgorithmicStemming": Literal["none", "minimal", "light", "full"],
    },
    total=False,
)

_RequiredAnalysisSchemeTypeDef = TypedDict(
    "_RequiredAnalysisSchemeTypeDef",
    {
        "AnalysisSchemeName": str,
        "AnalysisSchemeLanguage": Literal[
            "ar",
            "bg",
            "ca",
            "cs",
            "da",
            "de",
            "el",
            "en",
            "es",
            "eu",
            "fa",
            "fi",
            "fr",
            "ga",
            "gl",
            "he",
            "hi",
            "hu",
            "hy",
            "id",
            "it",
            "ja",
            "ko",
            "lv",
            "mul",
            "nl",
            "no",
            "pt",
            "ro",
            "ru",
            "sv",
            "th",
            "tr",
            "zh-Hans",
            "zh-Hant",
        ],
    },
)
_OptionalAnalysisSchemeTypeDef = TypedDict(
    "_OptionalAnalysisSchemeTypeDef", {"AnalysisOptions": AnalysisOptionsTypeDef}, total=False
)


class AnalysisSchemeTypeDef(_RequiredAnalysisSchemeTypeDef, _OptionalAnalysisSchemeTypeDef):
    pass


BuildSuggestersResponseTypeDef = TypedDict(
    "BuildSuggestersResponseTypeDef", {"FieldNames": List[str]}, total=False
)

LimitsTypeDef = TypedDict(
    "LimitsTypeDef", {"MaximumReplicationCount": int, "MaximumPartitionCount": int}
)

ServiceEndpointTypeDef = TypedDict("ServiceEndpointTypeDef", {"Endpoint": str}, total=False)

_RequiredDomainStatusTypeDef = TypedDict(
    "_RequiredDomainStatusTypeDef",
    {"DomainId": str, "DomainName": str, "RequiresIndexDocuments": bool},
)
_OptionalDomainStatusTypeDef = TypedDict(
    "_OptionalDomainStatusTypeDef",
    {
        "ARN": str,
        "Created": bool,
        "Deleted": bool,
        "DocService": ServiceEndpointTypeDef,
        "SearchService": ServiceEndpointTypeDef,
        "Processing": bool,
        "SearchInstanceType": str,
        "SearchPartitionCount": int,
        "SearchInstanceCount": int,
        "Limits": LimitsTypeDef,
    },
    total=False,
)


class DomainStatusTypeDef(_RequiredDomainStatusTypeDef, _OptionalDomainStatusTypeDef):
    pass


CreateDomainResponseTypeDef = TypedDict(
    "CreateDomainResponseTypeDef", {"DomainStatus": DomainStatusTypeDef}, total=False
)

_RequiredOptionStatusTypeDef = TypedDict(
    "_RequiredOptionStatusTypeDef",
    {
        "CreationDate": datetime,
        "UpdateDate": datetime,
        "State": Literal["RequiresIndexDocuments", "Processing", "Active", "FailedToValidate"],
    },
)
_OptionalOptionStatusTypeDef = TypedDict(
    "_OptionalOptionStatusTypeDef", {"UpdateVersion": int, "PendingDeletion": bool}, total=False
)


class OptionStatusTypeDef(_RequiredOptionStatusTypeDef, _OptionalOptionStatusTypeDef):
    pass


AnalysisSchemeStatusTypeDef = TypedDict(
    "AnalysisSchemeStatusTypeDef", {"Options": AnalysisSchemeTypeDef, "Status": OptionStatusTypeDef}
)

DefineAnalysisSchemeResponseTypeDef = TypedDict(
    "DefineAnalysisSchemeResponseTypeDef", {"AnalysisScheme": AnalysisSchemeStatusTypeDef}
)

ExpressionTypeDef = TypedDict("ExpressionTypeDef", {"ExpressionName": str, "ExpressionValue": str})

ExpressionStatusTypeDef = TypedDict(
    "ExpressionStatusTypeDef", {"Options": ExpressionTypeDef, "Status": OptionStatusTypeDef}
)

DefineExpressionResponseTypeDef = TypedDict(
    "DefineExpressionResponseTypeDef", {"Expression": ExpressionStatusTypeDef}
)

DateArrayOptionsTypeDef = TypedDict(
    "DateArrayOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceFields": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
    },
    total=False,
)

DateOptionsTypeDef = TypedDict(
    "DateOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

DoubleArrayOptionsTypeDef = TypedDict(
    "DoubleArrayOptionsTypeDef",
    {
        "DefaultValue": float,
        "SourceFields": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
    },
    total=False,
)

DoubleOptionsTypeDef = TypedDict(
    "DoubleOptionsTypeDef",
    {
        "DefaultValue": float,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

IntArrayOptionsTypeDef = TypedDict(
    "IntArrayOptionsTypeDef",
    {
        "DefaultValue": int,
        "SourceFields": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
    },
    total=False,
)

IntOptionsTypeDef = TypedDict(
    "IntOptionsTypeDef",
    {
        "DefaultValue": int,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

LatLonOptionsTypeDef = TypedDict(
    "LatLonOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

LiteralArrayOptionsTypeDef = TypedDict(
    "LiteralArrayOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceFields": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
    },
    total=False,
)

LiteralOptionsTypeDef = TypedDict(
    "LiteralOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

TextArrayOptionsTypeDef = TypedDict(
    "TextArrayOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceFields": str,
        "ReturnEnabled": bool,
        "HighlightEnabled": bool,
        "AnalysisScheme": str,
    },
    total=False,
)

TextOptionsTypeDef = TypedDict(
    "TextOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceField": str,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
        "HighlightEnabled": bool,
        "AnalysisScheme": str,
    },
    total=False,
)

_RequiredIndexFieldTypeDef = TypedDict(
    "_RequiredIndexFieldTypeDef",
    {
        "IndexFieldName": str,
        "IndexFieldType": Literal[
            "int",
            "double",
            "literal",
            "text",
            "date",
            "latlon",
            "int-array",
            "double-array",
            "literal-array",
            "text-array",
            "date-array",
        ],
    },
)
_OptionalIndexFieldTypeDef = TypedDict(
    "_OptionalIndexFieldTypeDef",
    {
        "IntOptions": IntOptionsTypeDef,
        "DoubleOptions": DoubleOptionsTypeDef,
        "LiteralOptions": LiteralOptionsTypeDef,
        "TextOptions": TextOptionsTypeDef,
        "DateOptions": DateOptionsTypeDef,
        "LatLonOptions": LatLonOptionsTypeDef,
        "IntArrayOptions": IntArrayOptionsTypeDef,
        "DoubleArrayOptions": DoubleArrayOptionsTypeDef,
        "LiteralArrayOptions": LiteralArrayOptionsTypeDef,
        "TextArrayOptions": TextArrayOptionsTypeDef,
        "DateArrayOptions": DateArrayOptionsTypeDef,
    },
    total=False,
)


class IndexFieldTypeDef(_RequiredIndexFieldTypeDef, _OptionalIndexFieldTypeDef):
    pass


IndexFieldStatusTypeDef = TypedDict(
    "IndexFieldStatusTypeDef", {"Options": IndexFieldTypeDef, "Status": OptionStatusTypeDef}
)

DefineIndexFieldResponseTypeDef = TypedDict(
    "DefineIndexFieldResponseTypeDef", {"IndexField": IndexFieldStatusTypeDef}
)

_RequiredDocumentSuggesterOptionsTypeDef = TypedDict(
    "_RequiredDocumentSuggesterOptionsTypeDef", {"SourceField": str}
)
_OptionalDocumentSuggesterOptionsTypeDef = TypedDict(
    "_OptionalDocumentSuggesterOptionsTypeDef",
    {"FuzzyMatching": Literal["none", "low", "high"], "SortExpression": str},
    total=False,
)


class DocumentSuggesterOptionsTypeDef(
    _RequiredDocumentSuggesterOptionsTypeDef, _OptionalDocumentSuggesterOptionsTypeDef
):
    pass


SuggesterTypeDef = TypedDict(
    "SuggesterTypeDef",
    {"SuggesterName": str, "DocumentSuggesterOptions": DocumentSuggesterOptionsTypeDef},
)

SuggesterStatusTypeDef = TypedDict(
    "SuggesterStatusTypeDef", {"Options": SuggesterTypeDef, "Status": OptionStatusTypeDef}
)

DefineSuggesterResponseTypeDef = TypedDict(
    "DefineSuggesterResponseTypeDef", {"Suggester": SuggesterStatusTypeDef}
)

DeleteAnalysisSchemeResponseTypeDef = TypedDict(
    "DeleteAnalysisSchemeResponseTypeDef", {"AnalysisScheme": AnalysisSchemeStatusTypeDef}
)

DeleteDomainResponseTypeDef = TypedDict(
    "DeleteDomainResponseTypeDef", {"DomainStatus": DomainStatusTypeDef}, total=False
)

DeleteExpressionResponseTypeDef = TypedDict(
    "DeleteExpressionResponseTypeDef", {"Expression": ExpressionStatusTypeDef}
)

DeleteIndexFieldResponseTypeDef = TypedDict(
    "DeleteIndexFieldResponseTypeDef", {"IndexField": IndexFieldStatusTypeDef}
)

DeleteSuggesterResponseTypeDef = TypedDict(
    "DeleteSuggesterResponseTypeDef", {"Suggester": SuggesterStatusTypeDef}
)

DescribeAnalysisSchemesResponseTypeDef = TypedDict(
    "DescribeAnalysisSchemesResponseTypeDef", {"AnalysisSchemes": List[AnalysisSchemeStatusTypeDef]}
)

AvailabilityOptionsStatusTypeDef = TypedDict(
    "AvailabilityOptionsStatusTypeDef", {"Options": bool, "Status": OptionStatusTypeDef}
)

DescribeAvailabilityOptionsResponseTypeDef = TypedDict(
    "DescribeAvailabilityOptionsResponseTypeDef",
    {"AvailabilityOptions": AvailabilityOptionsStatusTypeDef},
    total=False,
)

DomainEndpointOptionsTypeDef = TypedDict(
    "DomainEndpointOptionsTypeDef",
    {
        "EnforceHTTPS": bool,
        "TLSSecurityPolicy": Literal["Policy-Min-TLS-1-0-2019-07", "Policy-Min-TLS-1-2-2019-07"],
    },
    total=False,
)

DomainEndpointOptionsStatusTypeDef = TypedDict(
    "DomainEndpointOptionsStatusTypeDef",
    {"Options": DomainEndpointOptionsTypeDef, "Status": OptionStatusTypeDef},
)

DescribeDomainEndpointOptionsResponseTypeDef = TypedDict(
    "DescribeDomainEndpointOptionsResponseTypeDef",
    {"DomainEndpointOptions": DomainEndpointOptionsStatusTypeDef},
    total=False,
)

DescribeDomainsResponseTypeDef = TypedDict(
    "DescribeDomainsResponseTypeDef", {"DomainStatusList": List[DomainStatusTypeDef]}
)

DescribeExpressionsResponseTypeDef = TypedDict(
    "DescribeExpressionsResponseTypeDef", {"Expressions": List[ExpressionStatusTypeDef]}
)

DescribeIndexFieldsResponseTypeDef = TypedDict(
    "DescribeIndexFieldsResponseTypeDef", {"IndexFields": List[IndexFieldStatusTypeDef]}
)

ScalingParametersTypeDef = TypedDict(
    "ScalingParametersTypeDef",
    {
        "DesiredInstanceType": Literal[
            "search.m1.small",
            "search.m1.large",
            "search.m2.xlarge",
            "search.m2.2xlarge",
            "search.m3.medium",
            "search.m3.large",
            "search.m3.xlarge",
            "search.m3.2xlarge",
        ],
        "DesiredReplicationCount": int,
        "DesiredPartitionCount": int,
    },
    total=False,
)

ScalingParametersStatusTypeDef = TypedDict(
    "ScalingParametersStatusTypeDef",
    {"Options": ScalingParametersTypeDef, "Status": OptionStatusTypeDef},
)

DescribeScalingParametersResponseTypeDef = TypedDict(
    "DescribeScalingParametersResponseTypeDef",
    {"ScalingParameters": ScalingParametersStatusTypeDef},
)

AccessPoliciesStatusTypeDef = TypedDict(
    "AccessPoliciesStatusTypeDef", {"Options": str, "Status": OptionStatusTypeDef}
)

DescribeServiceAccessPoliciesResponseTypeDef = TypedDict(
    "DescribeServiceAccessPoliciesResponseTypeDef", {"AccessPolicies": AccessPoliciesStatusTypeDef}
)

DescribeSuggestersResponseTypeDef = TypedDict(
    "DescribeSuggestersResponseTypeDef", {"Suggesters": List[SuggesterStatusTypeDef]}
)

IndexDocumentsResponseTypeDef = TypedDict(
    "IndexDocumentsResponseTypeDef", {"FieldNames": List[str]}, total=False
)

ListDomainNamesResponseTypeDef = TypedDict(
    "ListDomainNamesResponseTypeDef", {"DomainNames": Dict[str, str]}, total=False
)

UpdateAvailabilityOptionsResponseTypeDef = TypedDict(
    "UpdateAvailabilityOptionsResponseTypeDef",
    {"AvailabilityOptions": AvailabilityOptionsStatusTypeDef},
    total=False,
)

UpdateDomainEndpointOptionsResponseTypeDef = TypedDict(
    "UpdateDomainEndpointOptionsResponseTypeDef",
    {"DomainEndpointOptions": DomainEndpointOptionsStatusTypeDef},
    total=False,
)

UpdateScalingParametersResponseTypeDef = TypedDict(
    "UpdateScalingParametersResponseTypeDef", {"ScalingParameters": ScalingParametersStatusTypeDef}
)

UpdateServiceAccessPoliciesResponseTypeDef = TypedDict(
    "UpdateServiceAccessPoliciesResponseTypeDef", {"AccessPolicies": AccessPoliciesStatusTypeDef}
)
