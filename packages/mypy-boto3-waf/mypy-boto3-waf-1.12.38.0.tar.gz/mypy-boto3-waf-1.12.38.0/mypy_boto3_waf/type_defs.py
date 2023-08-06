"""
Main interface for waf service type definitions.

Usage::

    from mypy_boto3.waf.type_defs import FieldToMatchTypeDef

    data: FieldToMatchTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "FieldToMatchTypeDef",
    "ByteMatchTupleTypeDef",
    "ByteMatchSetUpdateTypeDef",
    "ByteMatchSetTypeDef",
    "CreateByteMatchSetResponseTypeDef",
    "GeoMatchConstraintTypeDef",
    "GeoMatchSetTypeDef",
    "CreateGeoMatchSetResponseTypeDef",
    "IPSetDescriptorTypeDef",
    "IPSetTypeDef",
    "CreateIPSetResponseTypeDef",
    "PredicateTypeDef",
    "RateBasedRuleTypeDef",
    "CreateRateBasedRuleResponseTypeDef",
    "RegexMatchTupleTypeDef",
    "RegexMatchSetTypeDef",
    "CreateRegexMatchSetResponseTypeDef",
    "RegexPatternSetTypeDef",
    "CreateRegexPatternSetResponseTypeDef",
    "RuleGroupTypeDef",
    "CreateRuleGroupResponseTypeDef",
    "RuleTypeDef",
    "CreateRuleResponseTypeDef",
    "SizeConstraintTypeDef",
    "SizeConstraintSetTypeDef",
    "CreateSizeConstraintSetResponseTypeDef",
    "SqlInjectionMatchTupleTypeDef",
    "SqlInjectionMatchSetTypeDef",
    "CreateSqlInjectionMatchSetResponseTypeDef",
    "ExcludedRuleTypeDef",
    "WafActionTypeDef",
    "WafOverrideActionTypeDef",
    "ActivatedRuleTypeDef",
    "WebACLTypeDef",
    "CreateWebACLResponseTypeDef",
    "XssMatchTupleTypeDef",
    "XssMatchSetTypeDef",
    "CreateXssMatchSetResponseTypeDef",
    "DeleteByteMatchSetResponseTypeDef",
    "DeleteGeoMatchSetResponseTypeDef",
    "DeleteIPSetResponseTypeDef",
    "DeleteRateBasedRuleResponseTypeDef",
    "DeleteRegexMatchSetResponseTypeDef",
    "DeleteRegexPatternSetResponseTypeDef",
    "DeleteRuleGroupResponseTypeDef",
    "DeleteRuleResponseTypeDef",
    "DeleteSizeConstraintSetResponseTypeDef",
    "DeleteSqlInjectionMatchSetResponseTypeDef",
    "DeleteWebACLResponseTypeDef",
    "DeleteXssMatchSetResponseTypeDef",
    "GeoMatchSetUpdateTypeDef",
    "GetByteMatchSetResponseTypeDef",
    "GetChangeTokenResponseTypeDef",
    "GetChangeTokenStatusResponseTypeDef",
    "GetGeoMatchSetResponseTypeDef",
    "GetIPSetResponseTypeDef",
    "LoggingConfigurationTypeDef",
    "GetLoggingConfigurationResponseTypeDef",
    "GetPermissionPolicyResponseTypeDef",
    "GetRateBasedRuleManagedKeysResponseTypeDef",
    "GetRateBasedRuleResponseTypeDef",
    "GetRegexMatchSetResponseTypeDef",
    "GetRegexPatternSetResponseTypeDef",
    "GetRuleGroupResponseTypeDef",
    "GetRuleResponseTypeDef",
    "HTTPHeaderTypeDef",
    "HTTPRequestTypeDef",
    "SampledHTTPRequestTypeDef",
    "TimeWindowTypeDef",
    "GetSampledRequestsResponseTypeDef",
    "GetSizeConstraintSetResponseTypeDef",
    "GetSqlInjectionMatchSetResponseTypeDef",
    "GetWebACLResponseTypeDef",
    "GetXssMatchSetResponseTypeDef",
    "IPSetUpdateTypeDef",
    "ListActivatedRulesInRuleGroupResponseTypeDef",
    "ByteMatchSetSummaryTypeDef",
    "ListByteMatchSetsResponseTypeDef",
    "GeoMatchSetSummaryTypeDef",
    "ListGeoMatchSetsResponseTypeDef",
    "IPSetSummaryTypeDef",
    "ListIPSetsResponseTypeDef",
    "ListLoggingConfigurationsResponseTypeDef",
    "RuleSummaryTypeDef",
    "ListRateBasedRulesResponseTypeDef",
    "RegexMatchSetSummaryTypeDef",
    "ListRegexMatchSetsResponseTypeDef",
    "RegexPatternSetSummaryTypeDef",
    "ListRegexPatternSetsResponseTypeDef",
    "RuleGroupSummaryTypeDef",
    "ListRuleGroupsResponseTypeDef",
    "ListRulesResponseTypeDef",
    "SizeConstraintSetSummaryTypeDef",
    "ListSizeConstraintSetsResponseTypeDef",
    "SqlInjectionMatchSetSummaryTypeDef",
    "ListSqlInjectionMatchSetsResponseTypeDef",
    "SubscribedRuleGroupSummaryTypeDef",
    "ListSubscribedRuleGroupsResponseTypeDef",
    "TagTypeDef",
    "TagInfoForResourceTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "WebACLSummaryTypeDef",
    "ListWebACLsResponseTypeDef",
    "XssMatchSetSummaryTypeDef",
    "ListXssMatchSetsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutLoggingConfigurationResponseTypeDef",
    "RegexMatchSetUpdateTypeDef",
    "RegexPatternSetUpdateTypeDef",
    "RuleGroupUpdateTypeDef",
    "RuleUpdateTypeDef",
    "SizeConstraintSetUpdateTypeDef",
    "SqlInjectionMatchSetUpdateTypeDef",
    "UpdateByteMatchSetResponseTypeDef",
    "UpdateGeoMatchSetResponseTypeDef",
    "UpdateIPSetResponseTypeDef",
    "UpdateRateBasedRuleResponseTypeDef",
    "UpdateRegexMatchSetResponseTypeDef",
    "UpdateRegexPatternSetResponseTypeDef",
    "UpdateRuleGroupResponseTypeDef",
    "UpdateRuleResponseTypeDef",
    "UpdateSizeConstraintSetResponseTypeDef",
    "UpdateSqlInjectionMatchSetResponseTypeDef",
    "UpdateWebACLResponseTypeDef",
    "UpdateXssMatchSetResponseTypeDef",
    "WebACLUpdateTypeDef",
    "XssMatchSetUpdateTypeDef",
)

_RequiredFieldToMatchTypeDef = TypedDict(
    "_RequiredFieldToMatchTypeDef",
    {
        "Type": Literal[
            "URI", "QUERY_STRING", "HEADER", "METHOD", "BODY", "SINGLE_QUERY_ARG", "ALL_QUERY_ARGS"
        ]
    },
)
_OptionalFieldToMatchTypeDef = TypedDict("_OptionalFieldToMatchTypeDef", {"Data": str}, total=False)


class FieldToMatchTypeDef(_RequiredFieldToMatchTypeDef, _OptionalFieldToMatchTypeDef):
    pass


ByteMatchTupleTypeDef = TypedDict(
    "ByteMatchTupleTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TargetString": Union[bytes, IO],
        "TextTransformation": Literal[
            "NONE",
            "COMPRESS_WHITE_SPACE",
            "HTML_ENTITY_DECODE",
            "LOWERCASE",
            "CMD_LINE",
            "URL_DECODE",
        ],
        "PositionalConstraint": Literal[
            "EXACTLY", "STARTS_WITH", "ENDS_WITH", "CONTAINS", "CONTAINS_WORD"
        ],
    },
)

ByteMatchSetUpdateTypeDef = TypedDict(
    "ByteMatchSetUpdateTypeDef",
    {"Action": Literal["INSERT", "DELETE"], "ByteMatchTuple": ByteMatchTupleTypeDef},
)

_RequiredByteMatchSetTypeDef = TypedDict(
    "_RequiredByteMatchSetTypeDef",
    {"ByteMatchSetId": str, "ByteMatchTuples": List[ByteMatchTupleTypeDef]},
)
_OptionalByteMatchSetTypeDef = TypedDict("_OptionalByteMatchSetTypeDef", {"Name": str}, total=False)


class ByteMatchSetTypeDef(_RequiredByteMatchSetTypeDef, _OptionalByteMatchSetTypeDef):
    pass


CreateByteMatchSetResponseTypeDef = TypedDict(
    "CreateByteMatchSetResponseTypeDef",
    {"ByteMatchSet": ByteMatchSetTypeDef, "ChangeToken": str},
    total=False,
)

GeoMatchConstraintTypeDef = TypedDict(
    "GeoMatchConstraintTypeDef",
    {
        "Type": Literal["Country"],
        "Value": Literal[
            "AF",
            "AX",
            "AL",
            "DZ",
            "AS",
            "AD",
            "AO",
            "AI",
            "AQ",
            "AG",
            "AR",
            "AM",
            "AW",
            "AU",
            "AT",
            "AZ",
            "BS",
            "BH",
            "BD",
            "BB",
            "BY",
            "BE",
            "BZ",
            "BJ",
            "BM",
            "BT",
            "BO",
            "BQ",
            "BA",
            "BW",
            "BV",
            "BR",
            "IO",
            "BN",
            "BG",
            "BF",
            "BI",
            "KH",
            "CM",
            "CA",
            "CV",
            "KY",
            "CF",
            "TD",
            "CL",
            "CN",
            "CX",
            "CC",
            "CO",
            "KM",
            "CG",
            "CD",
            "CK",
            "CR",
            "CI",
            "HR",
            "CU",
            "CW",
            "CY",
            "CZ",
            "DK",
            "DJ",
            "DM",
            "DO",
            "EC",
            "EG",
            "SV",
            "GQ",
            "ER",
            "EE",
            "ET",
            "FK",
            "FO",
            "FJ",
            "FI",
            "FR",
            "GF",
            "PF",
            "TF",
            "GA",
            "GM",
            "GE",
            "DE",
            "GH",
            "GI",
            "GR",
            "GL",
            "GD",
            "GP",
            "GU",
            "GT",
            "GG",
            "GN",
            "GW",
            "GY",
            "HT",
            "HM",
            "VA",
            "HN",
            "HK",
            "HU",
            "IS",
            "IN",
            "ID",
            "IR",
            "IQ",
            "IE",
            "IM",
            "IL",
            "IT",
            "JM",
            "JP",
            "JE",
            "JO",
            "KZ",
            "KE",
            "KI",
            "KP",
            "KR",
            "KW",
            "KG",
            "LA",
            "LV",
            "LB",
            "LS",
            "LR",
            "LY",
            "LI",
            "LT",
            "LU",
            "MO",
            "MK",
            "MG",
            "MW",
            "MY",
            "MV",
            "ML",
            "MT",
            "MH",
            "MQ",
            "MR",
            "MU",
            "YT",
            "MX",
            "FM",
            "MD",
            "MC",
            "MN",
            "ME",
            "MS",
            "MA",
            "MZ",
            "MM",
            "NA",
            "NR",
            "NP",
            "NL",
            "NC",
            "NZ",
            "NI",
            "NE",
            "NG",
            "NU",
            "NF",
            "MP",
            "NO",
            "OM",
            "PK",
            "PW",
            "PS",
            "PA",
            "PG",
            "PY",
            "PE",
            "PH",
            "PN",
            "PL",
            "PT",
            "PR",
            "QA",
            "RE",
            "RO",
            "RU",
            "RW",
            "BL",
            "SH",
            "KN",
            "LC",
            "MF",
            "PM",
            "VC",
            "WS",
            "SM",
            "ST",
            "SA",
            "SN",
            "RS",
            "SC",
            "SL",
            "SG",
            "SX",
            "SK",
            "SI",
            "SB",
            "SO",
            "ZA",
            "GS",
            "SS",
            "ES",
            "LK",
            "SD",
            "SR",
            "SJ",
            "SZ",
            "SE",
            "CH",
            "SY",
            "TW",
            "TJ",
            "TZ",
            "TH",
            "TL",
            "TG",
            "TK",
            "TO",
            "TT",
            "TN",
            "TR",
            "TM",
            "TC",
            "TV",
            "UG",
            "UA",
            "AE",
            "GB",
            "US",
            "UM",
            "UY",
            "UZ",
            "VU",
            "VE",
            "VN",
            "VG",
            "VI",
            "WF",
            "EH",
            "YE",
            "ZM",
            "ZW",
        ],
    },
)

_RequiredGeoMatchSetTypeDef = TypedDict(
    "_RequiredGeoMatchSetTypeDef",
    {"GeoMatchSetId": str, "GeoMatchConstraints": List[GeoMatchConstraintTypeDef]},
)
_OptionalGeoMatchSetTypeDef = TypedDict("_OptionalGeoMatchSetTypeDef", {"Name": str}, total=False)


class GeoMatchSetTypeDef(_RequiredGeoMatchSetTypeDef, _OptionalGeoMatchSetTypeDef):
    pass


CreateGeoMatchSetResponseTypeDef = TypedDict(
    "CreateGeoMatchSetResponseTypeDef",
    {"GeoMatchSet": GeoMatchSetTypeDef, "ChangeToken": str},
    total=False,
)

IPSetDescriptorTypeDef = TypedDict(
    "IPSetDescriptorTypeDef", {"Type": Literal["IPV4", "IPV6"], "Value": str}
)

_RequiredIPSetTypeDef = TypedDict(
    "_RequiredIPSetTypeDef", {"IPSetId": str, "IPSetDescriptors": List[IPSetDescriptorTypeDef]}
)
_OptionalIPSetTypeDef = TypedDict("_OptionalIPSetTypeDef", {"Name": str}, total=False)


class IPSetTypeDef(_RequiredIPSetTypeDef, _OptionalIPSetTypeDef):
    pass


CreateIPSetResponseTypeDef = TypedDict(
    "CreateIPSetResponseTypeDef", {"IPSet": IPSetTypeDef, "ChangeToken": str}, total=False
)

PredicateTypeDef = TypedDict(
    "PredicateTypeDef",
    {
        "Negated": bool,
        "Type": Literal[
            "IPMatch",
            "ByteMatch",
            "SqlInjectionMatch",
            "GeoMatch",
            "SizeConstraint",
            "XssMatch",
            "RegexMatch",
        ],
        "DataId": str,
    },
)

_RequiredRateBasedRuleTypeDef = TypedDict(
    "_RequiredRateBasedRuleTypeDef",
    {
        "RuleId": str,
        "MatchPredicates": List[PredicateTypeDef],
        "RateKey": Literal["IP"],
        "RateLimit": int,
    },
)
_OptionalRateBasedRuleTypeDef = TypedDict(
    "_OptionalRateBasedRuleTypeDef", {"Name": str, "MetricName": str}, total=False
)


class RateBasedRuleTypeDef(_RequiredRateBasedRuleTypeDef, _OptionalRateBasedRuleTypeDef):
    pass


CreateRateBasedRuleResponseTypeDef = TypedDict(
    "CreateRateBasedRuleResponseTypeDef",
    {"Rule": RateBasedRuleTypeDef, "ChangeToken": str},
    total=False,
)

RegexMatchTupleTypeDef = TypedDict(
    "RegexMatchTupleTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformation": Literal[
            "NONE",
            "COMPRESS_WHITE_SPACE",
            "HTML_ENTITY_DECODE",
            "LOWERCASE",
            "CMD_LINE",
            "URL_DECODE",
        ],
        "RegexPatternSetId": str,
    },
)

RegexMatchSetTypeDef = TypedDict(
    "RegexMatchSetTypeDef",
    {"RegexMatchSetId": str, "Name": str, "RegexMatchTuples": List[RegexMatchTupleTypeDef]},
    total=False,
)

CreateRegexMatchSetResponseTypeDef = TypedDict(
    "CreateRegexMatchSetResponseTypeDef",
    {"RegexMatchSet": RegexMatchSetTypeDef, "ChangeToken": str},
    total=False,
)

_RequiredRegexPatternSetTypeDef = TypedDict(
    "_RequiredRegexPatternSetTypeDef", {"RegexPatternSetId": str, "RegexPatternStrings": List[str]}
)
_OptionalRegexPatternSetTypeDef = TypedDict(
    "_OptionalRegexPatternSetTypeDef", {"Name": str}, total=False
)


class RegexPatternSetTypeDef(_RequiredRegexPatternSetTypeDef, _OptionalRegexPatternSetTypeDef):
    pass


CreateRegexPatternSetResponseTypeDef = TypedDict(
    "CreateRegexPatternSetResponseTypeDef",
    {"RegexPatternSet": RegexPatternSetTypeDef, "ChangeToken": str},
    total=False,
)

_RequiredRuleGroupTypeDef = TypedDict("_RequiredRuleGroupTypeDef", {"RuleGroupId": str})
_OptionalRuleGroupTypeDef = TypedDict(
    "_OptionalRuleGroupTypeDef", {"Name": str, "MetricName": str}, total=False
)


class RuleGroupTypeDef(_RequiredRuleGroupTypeDef, _OptionalRuleGroupTypeDef):
    pass


CreateRuleGroupResponseTypeDef = TypedDict(
    "CreateRuleGroupResponseTypeDef",
    {"RuleGroup": RuleGroupTypeDef, "ChangeToken": str},
    total=False,
)

_RequiredRuleTypeDef = TypedDict(
    "_RequiredRuleTypeDef", {"RuleId": str, "Predicates": List[PredicateTypeDef]}
)
_OptionalRuleTypeDef = TypedDict(
    "_OptionalRuleTypeDef", {"Name": str, "MetricName": str}, total=False
)


class RuleTypeDef(_RequiredRuleTypeDef, _OptionalRuleTypeDef):
    pass


CreateRuleResponseTypeDef = TypedDict(
    "CreateRuleResponseTypeDef", {"Rule": RuleTypeDef, "ChangeToken": str}, total=False
)

SizeConstraintTypeDef = TypedDict(
    "SizeConstraintTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformation": Literal[
            "NONE",
            "COMPRESS_WHITE_SPACE",
            "HTML_ENTITY_DECODE",
            "LOWERCASE",
            "CMD_LINE",
            "URL_DECODE",
        ],
        "ComparisonOperator": Literal["EQ", "NE", "LE", "LT", "GE", "GT"],
        "Size": int,
    },
)

_RequiredSizeConstraintSetTypeDef = TypedDict(
    "_RequiredSizeConstraintSetTypeDef",
    {"SizeConstraintSetId": str, "SizeConstraints": List[SizeConstraintTypeDef]},
)
_OptionalSizeConstraintSetTypeDef = TypedDict(
    "_OptionalSizeConstraintSetTypeDef", {"Name": str}, total=False
)


class SizeConstraintSetTypeDef(
    _RequiredSizeConstraintSetTypeDef, _OptionalSizeConstraintSetTypeDef
):
    pass


CreateSizeConstraintSetResponseTypeDef = TypedDict(
    "CreateSizeConstraintSetResponseTypeDef",
    {"SizeConstraintSet": SizeConstraintSetTypeDef, "ChangeToken": str},
    total=False,
)

SqlInjectionMatchTupleTypeDef = TypedDict(
    "SqlInjectionMatchTupleTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformation": Literal[
            "NONE",
            "COMPRESS_WHITE_SPACE",
            "HTML_ENTITY_DECODE",
            "LOWERCASE",
            "CMD_LINE",
            "URL_DECODE",
        ],
    },
)

_RequiredSqlInjectionMatchSetTypeDef = TypedDict(
    "_RequiredSqlInjectionMatchSetTypeDef",
    {"SqlInjectionMatchSetId": str, "SqlInjectionMatchTuples": List[SqlInjectionMatchTupleTypeDef]},
)
_OptionalSqlInjectionMatchSetTypeDef = TypedDict(
    "_OptionalSqlInjectionMatchSetTypeDef", {"Name": str}, total=False
)


class SqlInjectionMatchSetTypeDef(
    _RequiredSqlInjectionMatchSetTypeDef, _OptionalSqlInjectionMatchSetTypeDef
):
    pass


CreateSqlInjectionMatchSetResponseTypeDef = TypedDict(
    "CreateSqlInjectionMatchSetResponseTypeDef",
    {"SqlInjectionMatchSet": SqlInjectionMatchSetTypeDef, "ChangeToken": str},
    total=False,
)

ExcludedRuleTypeDef = TypedDict("ExcludedRuleTypeDef", {"RuleId": str})

WafActionTypeDef = TypedDict("WafActionTypeDef", {"Type": Literal["BLOCK", "ALLOW", "COUNT"]})

WafOverrideActionTypeDef = TypedDict("WafOverrideActionTypeDef", {"Type": Literal["NONE", "COUNT"]})

_RequiredActivatedRuleTypeDef = TypedDict(
    "_RequiredActivatedRuleTypeDef", {"Priority": int, "RuleId": str}
)
_OptionalActivatedRuleTypeDef = TypedDict(
    "_OptionalActivatedRuleTypeDef",
    {
        "Action": WafActionTypeDef,
        "OverrideAction": WafOverrideActionTypeDef,
        "Type": Literal["REGULAR", "RATE_BASED", "GROUP"],
        "ExcludedRules": List[ExcludedRuleTypeDef],
    },
    total=False,
)


class ActivatedRuleTypeDef(_RequiredActivatedRuleTypeDef, _OptionalActivatedRuleTypeDef):
    pass


_RequiredWebACLTypeDef = TypedDict(
    "_RequiredWebACLTypeDef",
    {"WebACLId": str, "DefaultAction": WafActionTypeDef, "Rules": List[ActivatedRuleTypeDef]},
)
_OptionalWebACLTypeDef = TypedDict(
    "_OptionalWebACLTypeDef", {"Name": str, "MetricName": str, "WebACLArn": str}, total=False
)


class WebACLTypeDef(_RequiredWebACLTypeDef, _OptionalWebACLTypeDef):
    pass


CreateWebACLResponseTypeDef = TypedDict(
    "CreateWebACLResponseTypeDef", {"WebACL": WebACLTypeDef, "ChangeToken": str}, total=False
)

XssMatchTupleTypeDef = TypedDict(
    "XssMatchTupleTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformation": Literal[
            "NONE",
            "COMPRESS_WHITE_SPACE",
            "HTML_ENTITY_DECODE",
            "LOWERCASE",
            "CMD_LINE",
            "URL_DECODE",
        ],
    },
)

_RequiredXssMatchSetTypeDef = TypedDict(
    "_RequiredXssMatchSetTypeDef",
    {"XssMatchSetId": str, "XssMatchTuples": List[XssMatchTupleTypeDef]},
)
_OptionalXssMatchSetTypeDef = TypedDict("_OptionalXssMatchSetTypeDef", {"Name": str}, total=False)


class XssMatchSetTypeDef(_RequiredXssMatchSetTypeDef, _OptionalXssMatchSetTypeDef):
    pass


CreateXssMatchSetResponseTypeDef = TypedDict(
    "CreateXssMatchSetResponseTypeDef",
    {"XssMatchSet": XssMatchSetTypeDef, "ChangeToken": str},
    total=False,
)

DeleteByteMatchSetResponseTypeDef = TypedDict(
    "DeleteByteMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteGeoMatchSetResponseTypeDef = TypedDict(
    "DeleteGeoMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteIPSetResponseTypeDef = TypedDict(
    "DeleteIPSetResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteRateBasedRuleResponseTypeDef = TypedDict(
    "DeleteRateBasedRuleResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteRegexMatchSetResponseTypeDef = TypedDict(
    "DeleteRegexMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteRegexPatternSetResponseTypeDef = TypedDict(
    "DeleteRegexPatternSetResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteRuleGroupResponseTypeDef = TypedDict(
    "DeleteRuleGroupResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteRuleResponseTypeDef = TypedDict(
    "DeleteRuleResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteSizeConstraintSetResponseTypeDef = TypedDict(
    "DeleteSizeConstraintSetResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteSqlInjectionMatchSetResponseTypeDef = TypedDict(
    "DeleteSqlInjectionMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteWebACLResponseTypeDef = TypedDict(
    "DeleteWebACLResponseTypeDef", {"ChangeToken": str}, total=False
)

DeleteXssMatchSetResponseTypeDef = TypedDict(
    "DeleteXssMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

GeoMatchSetUpdateTypeDef = TypedDict(
    "GeoMatchSetUpdateTypeDef",
    {"Action": Literal["INSERT", "DELETE"], "GeoMatchConstraint": GeoMatchConstraintTypeDef},
)

GetByteMatchSetResponseTypeDef = TypedDict(
    "GetByteMatchSetResponseTypeDef", {"ByteMatchSet": ByteMatchSetTypeDef}, total=False
)

GetChangeTokenResponseTypeDef = TypedDict(
    "GetChangeTokenResponseTypeDef", {"ChangeToken": str}, total=False
)

GetChangeTokenStatusResponseTypeDef = TypedDict(
    "GetChangeTokenStatusResponseTypeDef",
    {"ChangeTokenStatus": Literal["PROVISIONED", "PENDING", "INSYNC"]},
    total=False,
)

GetGeoMatchSetResponseTypeDef = TypedDict(
    "GetGeoMatchSetResponseTypeDef", {"GeoMatchSet": GeoMatchSetTypeDef}, total=False
)

GetIPSetResponseTypeDef = TypedDict("GetIPSetResponseTypeDef", {"IPSet": IPSetTypeDef}, total=False)

_RequiredLoggingConfigurationTypeDef = TypedDict(
    "_RequiredLoggingConfigurationTypeDef", {"ResourceArn": str, "LogDestinationConfigs": List[str]}
)
_OptionalLoggingConfigurationTypeDef = TypedDict(
    "_OptionalLoggingConfigurationTypeDef",
    {"RedactedFields": List[FieldToMatchTypeDef]},
    total=False,
)


class LoggingConfigurationTypeDef(
    _RequiredLoggingConfigurationTypeDef, _OptionalLoggingConfigurationTypeDef
):
    pass


GetLoggingConfigurationResponseTypeDef = TypedDict(
    "GetLoggingConfigurationResponseTypeDef",
    {"LoggingConfiguration": LoggingConfigurationTypeDef},
    total=False,
)

GetPermissionPolicyResponseTypeDef = TypedDict(
    "GetPermissionPolicyResponseTypeDef", {"Policy": str}, total=False
)

GetRateBasedRuleManagedKeysResponseTypeDef = TypedDict(
    "GetRateBasedRuleManagedKeysResponseTypeDef",
    {"ManagedKeys": List[str], "NextMarker": str},
    total=False,
)

GetRateBasedRuleResponseTypeDef = TypedDict(
    "GetRateBasedRuleResponseTypeDef", {"Rule": RateBasedRuleTypeDef}, total=False
)

GetRegexMatchSetResponseTypeDef = TypedDict(
    "GetRegexMatchSetResponseTypeDef", {"RegexMatchSet": RegexMatchSetTypeDef}, total=False
)

GetRegexPatternSetResponseTypeDef = TypedDict(
    "GetRegexPatternSetResponseTypeDef", {"RegexPatternSet": RegexPatternSetTypeDef}, total=False
)

GetRuleGroupResponseTypeDef = TypedDict(
    "GetRuleGroupResponseTypeDef", {"RuleGroup": RuleGroupTypeDef}, total=False
)

GetRuleResponseTypeDef = TypedDict("GetRuleResponseTypeDef", {"Rule": RuleTypeDef}, total=False)

HTTPHeaderTypeDef = TypedDict("HTTPHeaderTypeDef", {"Name": str, "Value": str}, total=False)

HTTPRequestTypeDef = TypedDict(
    "HTTPRequestTypeDef",
    {
        "ClientIP": str,
        "Country": str,
        "URI": str,
        "Method": str,
        "HTTPVersion": str,
        "Headers": List[HTTPHeaderTypeDef],
    },
    total=False,
)

_RequiredSampledHTTPRequestTypeDef = TypedDict(
    "_RequiredSampledHTTPRequestTypeDef", {"Request": HTTPRequestTypeDef, "Weight": int}
)
_OptionalSampledHTTPRequestTypeDef = TypedDict(
    "_OptionalSampledHTTPRequestTypeDef",
    {"Timestamp": datetime, "Action": str, "RuleWithinRuleGroup": str},
    total=False,
)


class SampledHTTPRequestTypeDef(
    _RequiredSampledHTTPRequestTypeDef, _OptionalSampledHTTPRequestTypeDef
):
    pass


TimeWindowTypeDef = TypedDict("TimeWindowTypeDef", {"StartTime": datetime, "EndTime": datetime})

GetSampledRequestsResponseTypeDef = TypedDict(
    "GetSampledRequestsResponseTypeDef",
    {
        "SampledRequests": List[SampledHTTPRequestTypeDef],
        "PopulationSize": int,
        "TimeWindow": TimeWindowTypeDef,
    },
    total=False,
)

GetSizeConstraintSetResponseTypeDef = TypedDict(
    "GetSizeConstraintSetResponseTypeDef",
    {"SizeConstraintSet": SizeConstraintSetTypeDef},
    total=False,
)

GetSqlInjectionMatchSetResponseTypeDef = TypedDict(
    "GetSqlInjectionMatchSetResponseTypeDef",
    {"SqlInjectionMatchSet": SqlInjectionMatchSetTypeDef},
    total=False,
)

GetWebACLResponseTypeDef = TypedDict(
    "GetWebACLResponseTypeDef", {"WebACL": WebACLTypeDef}, total=False
)

GetXssMatchSetResponseTypeDef = TypedDict(
    "GetXssMatchSetResponseTypeDef", {"XssMatchSet": XssMatchSetTypeDef}, total=False
)

IPSetUpdateTypeDef = TypedDict(
    "IPSetUpdateTypeDef",
    {"Action": Literal["INSERT", "DELETE"], "IPSetDescriptor": IPSetDescriptorTypeDef},
)

ListActivatedRulesInRuleGroupResponseTypeDef = TypedDict(
    "ListActivatedRulesInRuleGroupResponseTypeDef",
    {"NextMarker": str, "ActivatedRules": List[ActivatedRuleTypeDef]},
    total=False,
)

ByteMatchSetSummaryTypeDef = TypedDict(
    "ByteMatchSetSummaryTypeDef", {"ByteMatchSetId": str, "Name": str}
)

ListByteMatchSetsResponseTypeDef = TypedDict(
    "ListByteMatchSetsResponseTypeDef",
    {"NextMarker": str, "ByteMatchSets": List[ByteMatchSetSummaryTypeDef]},
    total=False,
)

GeoMatchSetSummaryTypeDef = TypedDict(
    "GeoMatchSetSummaryTypeDef", {"GeoMatchSetId": str, "Name": str}
)

ListGeoMatchSetsResponseTypeDef = TypedDict(
    "ListGeoMatchSetsResponseTypeDef",
    {"NextMarker": str, "GeoMatchSets": List[GeoMatchSetSummaryTypeDef]},
    total=False,
)

IPSetSummaryTypeDef = TypedDict("IPSetSummaryTypeDef", {"IPSetId": str, "Name": str})

ListIPSetsResponseTypeDef = TypedDict(
    "ListIPSetsResponseTypeDef",
    {"NextMarker": str, "IPSets": List[IPSetSummaryTypeDef]},
    total=False,
)

ListLoggingConfigurationsResponseTypeDef = TypedDict(
    "ListLoggingConfigurationsResponseTypeDef",
    {"LoggingConfigurations": List[LoggingConfigurationTypeDef], "NextMarker": str},
    total=False,
)

RuleSummaryTypeDef = TypedDict("RuleSummaryTypeDef", {"RuleId": str, "Name": str})

ListRateBasedRulesResponseTypeDef = TypedDict(
    "ListRateBasedRulesResponseTypeDef",
    {"NextMarker": str, "Rules": List[RuleSummaryTypeDef]},
    total=False,
)

RegexMatchSetSummaryTypeDef = TypedDict(
    "RegexMatchSetSummaryTypeDef", {"RegexMatchSetId": str, "Name": str}
)

ListRegexMatchSetsResponseTypeDef = TypedDict(
    "ListRegexMatchSetsResponseTypeDef",
    {"NextMarker": str, "RegexMatchSets": List[RegexMatchSetSummaryTypeDef]},
    total=False,
)

RegexPatternSetSummaryTypeDef = TypedDict(
    "RegexPatternSetSummaryTypeDef", {"RegexPatternSetId": str, "Name": str}
)

ListRegexPatternSetsResponseTypeDef = TypedDict(
    "ListRegexPatternSetsResponseTypeDef",
    {"NextMarker": str, "RegexPatternSets": List[RegexPatternSetSummaryTypeDef]},
    total=False,
)

RuleGroupSummaryTypeDef = TypedDict("RuleGroupSummaryTypeDef", {"RuleGroupId": str, "Name": str})

ListRuleGroupsResponseTypeDef = TypedDict(
    "ListRuleGroupsResponseTypeDef",
    {"NextMarker": str, "RuleGroups": List[RuleGroupSummaryTypeDef]},
    total=False,
)

ListRulesResponseTypeDef = TypedDict(
    "ListRulesResponseTypeDef", {"NextMarker": str, "Rules": List[RuleSummaryTypeDef]}, total=False
)

SizeConstraintSetSummaryTypeDef = TypedDict(
    "SizeConstraintSetSummaryTypeDef", {"SizeConstraintSetId": str, "Name": str}
)

ListSizeConstraintSetsResponseTypeDef = TypedDict(
    "ListSizeConstraintSetsResponseTypeDef",
    {"NextMarker": str, "SizeConstraintSets": List[SizeConstraintSetSummaryTypeDef]},
    total=False,
)

SqlInjectionMatchSetSummaryTypeDef = TypedDict(
    "SqlInjectionMatchSetSummaryTypeDef", {"SqlInjectionMatchSetId": str, "Name": str}
)

ListSqlInjectionMatchSetsResponseTypeDef = TypedDict(
    "ListSqlInjectionMatchSetsResponseTypeDef",
    {"NextMarker": str, "SqlInjectionMatchSets": List[SqlInjectionMatchSetSummaryTypeDef]},
    total=False,
)

SubscribedRuleGroupSummaryTypeDef = TypedDict(
    "SubscribedRuleGroupSummaryTypeDef", {"RuleGroupId": str, "Name": str, "MetricName": str}
)

ListSubscribedRuleGroupsResponseTypeDef = TypedDict(
    "ListSubscribedRuleGroupsResponseTypeDef",
    {"NextMarker": str, "RuleGroups": List[SubscribedRuleGroupSummaryTypeDef]},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str}, total=False)

TagInfoForResourceTypeDef = TypedDict(
    "TagInfoForResourceTypeDef", {"ResourceARN": str, "TagList": List[TagTypeDef]}, total=False
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {"NextMarker": str, "TagInfoForResource": TagInfoForResourceTypeDef},
    total=False,
)

WebACLSummaryTypeDef = TypedDict("WebACLSummaryTypeDef", {"WebACLId": str, "Name": str})

ListWebACLsResponseTypeDef = TypedDict(
    "ListWebACLsResponseTypeDef",
    {"NextMarker": str, "WebACLs": List[WebACLSummaryTypeDef]},
    total=False,
)

XssMatchSetSummaryTypeDef = TypedDict(
    "XssMatchSetSummaryTypeDef", {"XssMatchSetId": str, "Name": str}
)

ListXssMatchSetsResponseTypeDef = TypedDict(
    "ListXssMatchSetsResponseTypeDef",
    {"NextMarker": str, "XssMatchSets": List[XssMatchSetSummaryTypeDef]},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutLoggingConfigurationResponseTypeDef = TypedDict(
    "PutLoggingConfigurationResponseTypeDef",
    {"LoggingConfiguration": LoggingConfigurationTypeDef},
    total=False,
)

RegexMatchSetUpdateTypeDef = TypedDict(
    "RegexMatchSetUpdateTypeDef",
    {"Action": Literal["INSERT", "DELETE"], "RegexMatchTuple": RegexMatchTupleTypeDef},
)

RegexPatternSetUpdateTypeDef = TypedDict(
    "RegexPatternSetUpdateTypeDef",
    {"Action": Literal["INSERT", "DELETE"], "RegexPatternString": str},
)

RuleGroupUpdateTypeDef = TypedDict(
    "RuleGroupUpdateTypeDef",
    {"Action": Literal["INSERT", "DELETE"], "ActivatedRule": ActivatedRuleTypeDef},
)

RuleUpdateTypeDef = TypedDict(
    "RuleUpdateTypeDef", {"Action": Literal["INSERT", "DELETE"], "Predicate": PredicateTypeDef}
)

SizeConstraintSetUpdateTypeDef = TypedDict(
    "SizeConstraintSetUpdateTypeDef",
    {"Action": Literal["INSERT", "DELETE"], "SizeConstraint": SizeConstraintTypeDef},
)

SqlInjectionMatchSetUpdateTypeDef = TypedDict(
    "SqlInjectionMatchSetUpdateTypeDef",
    {
        "Action": Literal["INSERT", "DELETE"],
        "SqlInjectionMatchTuple": SqlInjectionMatchTupleTypeDef,
    },
)

UpdateByteMatchSetResponseTypeDef = TypedDict(
    "UpdateByteMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateGeoMatchSetResponseTypeDef = TypedDict(
    "UpdateGeoMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateIPSetResponseTypeDef = TypedDict(
    "UpdateIPSetResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateRateBasedRuleResponseTypeDef = TypedDict(
    "UpdateRateBasedRuleResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateRegexMatchSetResponseTypeDef = TypedDict(
    "UpdateRegexMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateRegexPatternSetResponseTypeDef = TypedDict(
    "UpdateRegexPatternSetResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateRuleGroupResponseTypeDef = TypedDict(
    "UpdateRuleGroupResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateRuleResponseTypeDef = TypedDict(
    "UpdateRuleResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateSizeConstraintSetResponseTypeDef = TypedDict(
    "UpdateSizeConstraintSetResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateSqlInjectionMatchSetResponseTypeDef = TypedDict(
    "UpdateSqlInjectionMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateWebACLResponseTypeDef = TypedDict(
    "UpdateWebACLResponseTypeDef", {"ChangeToken": str}, total=False
)

UpdateXssMatchSetResponseTypeDef = TypedDict(
    "UpdateXssMatchSetResponseTypeDef", {"ChangeToken": str}, total=False
)

WebACLUpdateTypeDef = TypedDict(
    "WebACLUpdateTypeDef",
    {"Action": Literal["INSERT", "DELETE"], "ActivatedRule": ActivatedRuleTypeDef},
)

XssMatchSetUpdateTypeDef = TypedDict(
    "XssMatchSetUpdateTypeDef",
    {"Action": Literal["INSERT", "DELETE"], "XssMatchTuple": XssMatchTupleTypeDef},
)
