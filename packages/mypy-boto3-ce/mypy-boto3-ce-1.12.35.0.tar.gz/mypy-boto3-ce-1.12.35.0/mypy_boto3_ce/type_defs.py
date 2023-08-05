"""
Main interface for ce service type definitions.

Usage::

    from mypy_boto3.ce.type_defs import CostCategoryValuesTypeDef

    data: CostCategoryValuesTypeDef = {...}
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
    "CostCategoryValuesTypeDef",
    "DimensionValuesTypeDef",
    "TagValuesTypeDef",
    "ExpressionTypeDef",
    "CostCategoryRuleTypeDef",
    "CreateCostCategoryDefinitionResponseTypeDef",
    "DateIntervalTypeDef",
    "DeleteCostCategoryDefinitionResponseTypeDef",
    "CostCategoryTypeDef",
    "DescribeCostCategoryDefinitionResponseTypeDef",
    "GroupDefinitionTypeDef",
    "MetricValueTypeDef",
    "GroupTypeDef",
    "ResultByTimeTypeDef",
    "GetCostAndUsageResponseTypeDef",
    "GetCostAndUsageWithResourcesResponseTypeDef",
    "ForecastResultTypeDef",
    "GetCostForecastResponseTypeDef",
    "DimensionValuesWithAttributesTypeDef",
    "GetDimensionValuesResponseTypeDef",
    "CoverageCostTypeDef",
    "CoverageHoursTypeDef",
    "CoverageNormalizedUnitsTypeDef",
    "CoverageTypeDef",
    "ReservationCoverageGroupTypeDef",
    "CoverageByTimeTypeDef",
    "GetReservationCoverageResponseTypeDef",
    "ReservationPurchaseRecommendationMetadataTypeDef",
    "EC2InstanceDetailsTypeDef",
    "ESInstanceDetailsTypeDef",
    "ElastiCacheInstanceDetailsTypeDef",
    "RDSInstanceDetailsTypeDef",
    "RedshiftInstanceDetailsTypeDef",
    "InstanceDetailsTypeDef",
    "ReservationPurchaseRecommendationDetailTypeDef",
    "ReservationPurchaseRecommendationSummaryTypeDef",
    "EC2SpecificationTypeDef",
    "ServiceSpecificationTypeDef",
    "ReservationPurchaseRecommendationTypeDef",
    "GetReservationPurchaseRecommendationResponseTypeDef",
    "ReservationAggregatesTypeDef",
    "ReservationUtilizationGroupTypeDef",
    "UtilizationByTimeTypeDef",
    "GetReservationUtilizationResponseTypeDef",
    "RightsizingRecommendationMetadataTypeDef",
    "RightsizingRecommendationSummaryTypeDef",
    "EC2ResourceDetailsTypeDef",
    "ResourceDetailsTypeDef",
    "EC2ResourceUtilizationTypeDef",
    "ResourceUtilizationTypeDef",
    "CurrentInstanceTypeDef",
    "TargetInstanceTypeDef",
    "ModifyRecommendationDetailTypeDef",
    "TerminateRecommendationDetailTypeDef",
    "RightsizingRecommendationTypeDef",
    "GetRightsizingRecommendationResponseTypeDef",
    "SavingsPlansCoverageDataTypeDef",
    "SavingsPlansCoverageTypeDef",
    "GetSavingsPlansCoverageResponseTypeDef",
    "SavingsPlansPurchaseRecommendationMetadataTypeDef",
    "SavingsPlansDetailsTypeDef",
    "SavingsPlansPurchaseRecommendationDetailTypeDef",
    "SavingsPlansPurchaseRecommendationSummaryTypeDef",
    "SavingsPlansPurchaseRecommendationTypeDef",
    "GetSavingsPlansPurchaseRecommendationResponseTypeDef",
    "SavingsPlansAmortizedCommitmentTypeDef",
    "SavingsPlansSavingsTypeDef",
    "SavingsPlansUtilizationTypeDef",
    "SavingsPlansUtilizationAggregatesTypeDef",
    "SavingsPlansUtilizationDetailTypeDef",
    "GetSavingsPlansUtilizationDetailsResponseTypeDef",
    "SavingsPlansUtilizationByTimeTypeDef",
    "GetSavingsPlansUtilizationResponseTypeDef",
    "GetTagsResponseTypeDef",
    "GetUsageForecastResponseTypeDef",
    "CostCategoryReferenceTypeDef",
    "ListCostCategoryDefinitionsResponseTypeDef",
    "UpdateCostCategoryDefinitionResponseTypeDef",
)

CostCategoryValuesTypeDef = TypedDict(
    "CostCategoryValuesTypeDef", {"Key": str, "Values": List[str]}, total=False
)

DimensionValuesTypeDef = TypedDict(
    "DimensionValuesTypeDef",
    {
        "Key": Literal[
            "AZ",
            "INSTANCE_TYPE",
            "LINKED_ACCOUNT",
            "OPERATION",
            "PURCHASE_TYPE",
            "REGION",
            "SERVICE",
            "USAGE_TYPE",
            "USAGE_TYPE_GROUP",
            "RECORD_TYPE",
            "OPERATING_SYSTEM",
            "TENANCY",
            "SCOPE",
            "PLATFORM",
            "SUBSCRIPTION_ID",
            "LEGAL_ENTITY_NAME",
            "DEPLOYMENT_OPTION",
            "DATABASE_ENGINE",
            "CACHE_ENGINE",
            "INSTANCE_TYPE_FAMILY",
            "BILLING_ENTITY",
            "RESERVATION_ID",
            "RESOURCE_ID",
            "RIGHTSIZING_TYPE",
            "SAVINGS_PLANS_TYPE",
            "SAVINGS_PLAN_ARN",
            "PAYMENT_OPTION",
        ],
        "Values": List[str],
    },
    total=False,
)

TagValuesTypeDef = TypedDict("TagValuesTypeDef", {"Key": str, "Values": List[str]}, total=False)

ExpressionTypeDef = TypedDict(
    "ExpressionTypeDef",
    {
        "Or": List["ExpressionTypeDef"],
        "And": List["ExpressionTypeDef"],
        "Not": "ExpressionTypeDef",
        "Dimensions": DimensionValuesTypeDef,
        "Tags": TagValuesTypeDef,
        "CostCategories": CostCategoryValuesTypeDef,
    },
    total=False,
)

CostCategoryRuleTypeDef = TypedDict(
    "CostCategoryRuleTypeDef", {"Value": str, "Rule": ExpressionTypeDef}
)

CreateCostCategoryDefinitionResponseTypeDef = TypedDict(
    "CreateCostCategoryDefinitionResponseTypeDef",
    {"CostCategoryArn": str, "EffectiveStart": str},
    total=False,
)

DateIntervalTypeDef = TypedDict("DateIntervalTypeDef", {"Start": str, "End": str})

DeleteCostCategoryDefinitionResponseTypeDef = TypedDict(
    "DeleteCostCategoryDefinitionResponseTypeDef",
    {"CostCategoryArn": str, "EffectiveEnd": str},
    total=False,
)

_RequiredCostCategoryTypeDef = TypedDict(
    "_RequiredCostCategoryTypeDef",
    {
        "CostCategoryArn": str,
        "EffectiveStart": str,
        "Name": str,
        "RuleVersion": Literal["CostCategoryExpression.v1"],
        "Rules": List[CostCategoryRuleTypeDef],
    },
)
_OptionalCostCategoryTypeDef = TypedDict(
    "_OptionalCostCategoryTypeDef", {"EffectiveEnd": str}, total=False
)


class CostCategoryTypeDef(_RequiredCostCategoryTypeDef, _OptionalCostCategoryTypeDef):
    pass


DescribeCostCategoryDefinitionResponseTypeDef = TypedDict(
    "DescribeCostCategoryDefinitionResponseTypeDef",
    {"CostCategory": CostCategoryTypeDef},
    total=False,
)

GroupDefinitionTypeDef = TypedDict(
    "GroupDefinitionTypeDef",
    {"Type": Literal["DIMENSION", "TAG", "COST_CATEGORY"], "Key": str},
    total=False,
)

MetricValueTypeDef = TypedDict("MetricValueTypeDef", {"Amount": str, "Unit": str}, total=False)

GroupTypeDef = TypedDict(
    "GroupTypeDef", {"Keys": List[str], "Metrics": Dict[str, MetricValueTypeDef]}, total=False
)

ResultByTimeTypeDef = TypedDict(
    "ResultByTimeTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Total": Dict[str, MetricValueTypeDef],
        "Groups": List[GroupTypeDef],
        "Estimated": bool,
    },
    total=False,
)

GetCostAndUsageResponseTypeDef = TypedDict(
    "GetCostAndUsageResponseTypeDef",
    {
        "NextPageToken": str,
        "GroupDefinitions": List[GroupDefinitionTypeDef],
        "ResultsByTime": List[ResultByTimeTypeDef],
    },
    total=False,
)

GetCostAndUsageWithResourcesResponseTypeDef = TypedDict(
    "GetCostAndUsageWithResourcesResponseTypeDef",
    {
        "NextPageToken": str,
        "GroupDefinitions": List[GroupDefinitionTypeDef],
        "ResultsByTime": List[ResultByTimeTypeDef],
    },
    total=False,
)

ForecastResultTypeDef = TypedDict(
    "ForecastResultTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "MeanValue": str,
        "PredictionIntervalLowerBound": str,
        "PredictionIntervalUpperBound": str,
    },
    total=False,
)

GetCostForecastResponseTypeDef = TypedDict(
    "GetCostForecastResponseTypeDef",
    {"Total": MetricValueTypeDef, "ForecastResultsByTime": List[ForecastResultTypeDef]},
    total=False,
)

DimensionValuesWithAttributesTypeDef = TypedDict(
    "DimensionValuesWithAttributesTypeDef",
    {"Value": str, "Attributes": Dict[str, str]},
    total=False,
)

_RequiredGetDimensionValuesResponseTypeDef = TypedDict(
    "_RequiredGetDimensionValuesResponseTypeDef",
    {
        "DimensionValues": List[DimensionValuesWithAttributesTypeDef],
        "ReturnSize": int,
        "TotalSize": int,
    },
)
_OptionalGetDimensionValuesResponseTypeDef = TypedDict(
    "_OptionalGetDimensionValuesResponseTypeDef", {"NextPageToken": str}, total=False
)


class GetDimensionValuesResponseTypeDef(
    _RequiredGetDimensionValuesResponseTypeDef, _OptionalGetDimensionValuesResponseTypeDef
):
    pass


CoverageCostTypeDef = TypedDict("CoverageCostTypeDef", {"OnDemandCost": str}, total=False)

CoverageHoursTypeDef = TypedDict(
    "CoverageHoursTypeDef",
    {
        "OnDemandHours": str,
        "ReservedHours": str,
        "TotalRunningHours": str,
        "CoverageHoursPercentage": str,
    },
    total=False,
)

CoverageNormalizedUnitsTypeDef = TypedDict(
    "CoverageNormalizedUnitsTypeDef",
    {
        "OnDemandNormalizedUnits": str,
        "ReservedNormalizedUnits": str,
        "TotalRunningNormalizedUnits": str,
        "CoverageNormalizedUnitsPercentage": str,
    },
    total=False,
)

CoverageTypeDef = TypedDict(
    "CoverageTypeDef",
    {
        "CoverageHours": CoverageHoursTypeDef,
        "CoverageNormalizedUnits": CoverageNormalizedUnitsTypeDef,
        "CoverageCost": CoverageCostTypeDef,
    },
    total=False,
)

ReservationCoverageGroupTypeDef = TypedDict(
    "ReservationCoverageGroupTypeDef",
    {"Attributes": Dict[str, str], "Coverage": CoverageTypeDef},
    total=False,
)

CoverageByTimeTypeDef = TypedDict(
    "CoverageByTimeTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Groups": List[ReservationCoverageGroupTypeDef],
        "Total": CoverageTypeDef,
    },
    total=False,
)

_RequiredGetReservationCoverageResponseTypeDef = TypedDict(
    "_RequiredGetReservationCoverageResponseTypeDef",
    {"CoveragesByTime": List[CoverageByTimeTypeDef]},
)
_OptionalGetReservationCoverageResponseTypeDef = TypedDict(
    "_OptionalGetReservationCoverageResponseTypeDef",
    {"Total": CoverageTypeDef, "NextPageToken": str},
    total=False,
)


class GetReservationCoverageResponseTypeDef(
    _RequiredGetReservationCoverageResponseTypeDef, _OptionalGetReservationCoverageResponseTypeDef
):
    pass


ReservationPurchaseRecommendationMetadataTypeDef = TypedDict(
    "ReservationPurchaseRecommendationMetadataTypeDef",
    {"RecommendationId": str, "GenerationTimestamp": str},
    total=False,
)

EC2InstanceDetailsTypeDef = TypedDict(
    "EC2InstanceDetailsTypeDef",
    {
        "Family": str,
        "InstanceType": str,
        "Region": str,
        "AvailabilityZone": str,
        "Platform": str,
        "Tenancy": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

ESInstanceDetailsTypeDef = TypedDict(
    "ESInstanceDetailsTypeDef",
    {
        "InstanceClass": str,
        "InstanceSize": str,
        "Region": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

ElastiCacheInstanceDetailsTypeDef = TypedDict(
    "ElastiCacheInstanceDetailsTypeDef",
    {
        "Family": str,
        "NodeType": str,
        "Region": str,
        "ProductDescription": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

RDSInstanceDetailsTypeDef = TypedDict(
    "RDSInstanceDetailsTypeDef",
    {
        "Family": str,
        "InstanceType": str,
        "Region": str,
        "DatabaseEngine": str,
        "DatabaseEdition": str,
        "DeploymentOption": str,
        "LicenseModel": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

RedshiftInstanceDetailsTypeDef = TypedDict(
    "RedshiftInstanceDetailsTypeDef",
    {
        "Family": str,
        "NodeType": str,
        "Region": str,
        "CurrentGeneration": bool,
        "SizeFlexEligible": bool,
    },
    total=False,
)

InstanceDetailsTypeDef = TypedDict(
    "InstanceDetailsTypeDef",
    {
        "EC2InstanceDetails": EC2InstanceDetailsTypeDef,
        "RDSInstanceDetails": RDSInstanceDetailsTypeDef,
        "RedshiftInstanceDetails": RedshiftInstanceDetailsTypeDef,
        "ElastiCacheInstanceDetails": ElastiCacheInstanceDetailsTypeDef,
        "ESInstanceDetails": ESInstanceDetailsTypeDef,
    },
    total=False,
)

ReservationPurchaseRecommendationDetailTypeDef = TypedDict(
    "ReservationPurchaseRecommendationDetailTypeDef",
    {
        "AccountId": str,
        "InstanceDetails": InstanceDetailsTypeDef,
        "RecommendedNumberOfInstancesToPurchase": str,
        "RecommendedNormalizedUnitsToPurchase": str,
        "MinimumNumberOfInstancesUsedPerHour": str,
        "MinimumNormalizedUnitsUsedPerHour": str,
        "MaximumNumberOfInstancesUsedPerHour": str,
        "MaximumNormalizedUnitsUsedPerHour": str,
        "AverageNumberOfInstancesUsedPerHour": str,
        "AverageNormalizedUnitsUsedPerHour": str,
        "AverageUtilization": str,
        "EstimatedBreakEvenInMonths": str,
        "CurrencyCode": str,
        "EstimatedMonthlySavingsAmount": str,
        "EstimatedMonthlySavingsPercentage": str,
        "EstimatedMonthlyOnDemandCost": str,
        "EstimatedReservationCostForLookbackPeriod": str,
        "UpfrontCost": str,
        "RecurringStandardMonthlyCost": str,
    },
    total=False,
)

ReservationPurchaseRecommendationSummaryTypeDef = TypedDict(
    "ReservationPurchaseRecommendationSummaryTypeDef",
    {
        "TotalEstimatedMonthlySavingsAmount": str,
        "TotalEstimatedMonthlySavingsPercentage": str,
        "CurrencyCode": str,
    },
    total=False,
)

EC2SpecificationTypeDef = TypedDict(
    "EC2SpecificationTypeDef", {"OfferingClass": Literal["STANDARD", "CONVERTIBLE"]}, total=False
)

ServiceSpecificationTypeDef = TypedDict(
    "ServiceSpecificationTypeDef", {"EC2Specification": EC2SpecificationTypeDef}, total=False
)

ReservationPurchaseRecommendationTypeDef = TypedDict(
    "ReservationPurchaseRecommendationTypeDef",
    {
        "AccountScope": Literal["PAYER", "LINKED"],
        "LookbackPeriodInDays": Literal["SEVEN_DAYS", "THIRTY_DAYS", "SIXTY_DAYS"],
        "TermInYears": Literal["ONE_YEAR", "THREE_YEARS"],
        "PaymentOption": Literal[
            "NO_UPFRONT",
            "PARTIAL_UPFRONT",
            "ALL_UPFRONT",
            "LIGHT_UTILIZATION",
            "MEDIUM_UTILIZATION",
            "HEAVY_UTILIZATION",
        ],
        "ServiceSpecification": ServiceSpecificationTypeDef,
        "RecommendationDetails": List[ReservationPurchaseRecommendationDetailTypeDef],
        "RecommendationSummary": ReservationPurchaseRecommendationSummaryTypeDef,
    },
    total=False,
)

GetReservationPurchaseRecommendationResponseTypeDef = TypedDict(
    "GetReservationPurchaseRecommendationResponseTypeDef",
    {
        "Metadata": ReservationPurchaseRecommendationMetadataTypeDef,
        "Recommendations": List[ReservationPurchaseRecommendationTypeDef],
        "NextPageToken": str,
    },
    total=False,
)

ReservationAggregatesTypeDef = TypedDict(
    "ReservationAggregatesTypeDef",
    {
        "UtilizationPercentage": str,
        "UtilizationPercentageInUnits": str,
        "PurchasedHours": str,
        "PurchasedUnits": str,
        "TotalActualHours": str,
        "TotalActualUnits": str,
        "UnusedHours": str,
        "UnusedUnits": str,
        "OnDemandCostOfRIHoursUsed": str,
        "NetRISavings": str,
        "TotalPotentialRISavings": str,
        "AmortizedUpfrontFee": str,
        "AmortizedRecurringFee": str,
        "TotalAmortizedFee": str,
    },
    total=False,
)

ReservationUtilizationGroupTypeDef = TypedDict(
    "ReservationUtilizationGroupTypeDef",
    {
        "Key": str,
        "Value": str,
        "Attributes": Dict[str, str],
        "Utilization": ReservationAggregatesTypeDef,
    },
    total=False,
)

UtilizationByTimeTypeDef = TypedDict(
    "UtilizationByTimeTypeDef",
    {
        "TimePeriod": DateIntervalTypeDef,
        "Groups": List[ReservationUtilizationGroupTypeDef],
        "Total": ReservationAggregatesTypeDef,
    },
    total=False,
)

_RequiredGetReservationUtilizationResponseTypeDef = TypedDict(
    "_RequiredGetReservationUtilizationResponseTypeDef",
    {"UtilizationsByTime": List[UtilizationByTimeTypeDef]},
)
_OptionalGetReservationUtilizationResponseTypeDef = TypedDict(
    "_OptionalGetReservationUtilizationResponseTypeDef",
    {"Total": ReservationAggregatesTypeDef, "NextPageToken": str},
    total=False,
)


class GetReservationUtilizationResponseTypeDef(
    _RequiredGetReservationUtilizationResponseTypeDef,
    _OptionalGetReservationUtilizationResponseTypeDef,
):
    pass


RightsizingRecommendationMetadataTypeDef = TypedDict(
    "RightsizingRecommendationMetadataTypeDef",
    {
        "RecommendationId": str,
        "GenerationTimestamp": str,
        "LookbackPeriodInDays": Literal["SEVEN_DAYS", "THIRTY_DAYS", "SIXTY_DAYS"],
    },
    total=False,
)

RightsizingRecommendationSummaryTypeDef = TypedDict(
    "RightsizingRecommendationSummaryTypeDef",
    {
        "TotalRecommendationCount": str,
        "EstimatedTotalMonthlySavingsAmount": str,
        "SavingsCurrencyCode": str,
        "SavingsPercentage": str,
    },
    total=False,
)

EC2ResourceDetailsTypeDef = TypedDict(
    "EC2ResourceDetailsTypeDef",
    {
        "HourlyOnDemandRate": str,
        "InstanceType": str,
        "Platform": str,
        "Region": str,
        "Sku": str,
        "Memory": str,
        "NetworkPerformance": str,
        "Storage": str,
        "Vcpu": str,
    },
    total=False,
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef", {"EC2ResourceDetails": EC2ResourceDetailsTypeDef}, total=False
)

EC2ResourceUtilizationTypeDef = TypedDict(
    "EC2ResourceUtilizationTypeDef",
    {
        "MaxCpuUtilizationPercentage": str,
        "MaxMemoryUtilizationPercentage": str,
        "MaxStorageUtilizationPercentage": str,
    },
    total=False,
)

ResourceUtilizationTypeDef = TypedDict(
    "ResourceUtilizationTypeDef",
    {"EC2ResourceUtilization": EC2ResourceUtilizationTypeDef},
    total=False,
)

CurrentInstanceTypeDef = TypedDict(
    "CurrentInstanceTypeDef",
    {
        "ResourceId": str,
        "Tags": List[TagValuesTypeDef],
        "ResourceDetails": ResourceDetailsTypeDef,
        "ResourceUtilization": ResourceUtilizationTypeDef,
        "ReservationCoveredHoursInLookbackPeriod": str,
        "SavingsPlansCoveredHoursInLookbackPeriod": str,
        "OnDemandHoursInLookbackPeriod": str,
        "TotalRunningHoursInLookbackPeriod": str,
        "MonthlyCost": str,
        "CurrencyCode": str,
    },
    total=False,
)

TargetInstanceTypeDef = TypedDict(
    "TargetInstanceTypeDef",
    {
        "EstimatedMonthlyCost": str,
        "EstimatedMonthlySavings": str,
        "CurrencyCode": str,
        "DefaultTargetInstance": bool,
        "ResourceDetails": ResourceDetailsTypeDef,
        "ExpectedResourceUtilization": ResourceUtilizationTypeDef,
    },
    total=False,
)

ModifyRecommendationDetailTypeDef = TypedDict(
    "ModifyRecommendationDetailTypeDef",
    {"TargetInstances": List[TargetInstanceTypeDef]},
    total=False,
)

TerminateRecommendationDetailTypeDef = TypedDict(
    "TerminateRecommendationDetailTypeDef",
    {"EstimatedMonthlySavings": str, "CurrencyCode": str},
    total=False,
)

RightsizingRecommendationTypeDef = TypedDict(
    "RightsizingRecommendationTypeDef",
    {
        "AccountId": str,
        "CurrentInstance": CurrentInstanceTypeDef,
        "RightsizingType": Literal["TERMINATE", "MODIFY"],
        "ModifyRecommendationDetail": ModifyRecommendationDetailTypeDef,
        "TerminateRecommendationDetail": TerminateRecommendationDetailTypeDef,
    },
    total=False,
)

GetRightsizingRecommendationResponseTypeDef = TypedDict(
    "GetRightsizingRecommendationResponseTypeDef",
    {
        "Metadata": RightsizingRecommendationMetadataTypeDef,
        "Summary": RightsizingRecommendationSummaryTypeDef,
        "RightsizingRecommendations": List[RightsizingRecommendationTypeDef],
        "NextPageToken": str,
    },
    total=False,
)

SavingsPlansCoverageDataTypeDef = TypedDict(
    "SavingsPlansCoverageDataTypeDef",
    {
        "SpendCoveredBySavingsPlans": str,
        "OnDemandCost": str,
        "TotalCost": str,
        "CoveragePercentage": str,
    },
    total=False,
)

SavingsPlansCoverageTypeDef = TypedDict(
    "SavingsPlansCoverageTypeDef",
    {
        "Attributes": Dict[str, str],
        "Coverage": SavingsPlansCoverageDataTypeDef,
        "TimePeriod": DateIntervalTypeDef,
    },
    total=False,
)

_RequiredGetSavingsPlansCoverageResponseTypeDef = TypedDict(
    "_RequiredGetSavingsPlansCoverageResponseTypeDef",
    {"SavingsPlansCoverages": List[SavingsPlansCoverageTypeDef]},
)
_OptionalGetSavingsPlansCoverageResponseTypeDef = TypedDict(
    "_OptionalGetSavingsPlansCoverageResponseTypeDef", {"NextToken": str}, total=False
)


class GetSavingsPlansCoverageResponseTypeDef(
    _RequiredGetSavingsPlansCoverageResponseTypeDef, _OptionalGetSavingsPlansCoverageResponseTypeDef
):
    pass


SavingsPlansPurchaseRecommendationMetadataTypeDef = TypedDict(
    "SavingsPlansPurchaseRecommendationMetadataTypeDef",
    {"RecommendationId": str, "GenerationTimestamp": str},
    total=False,
)

SavingsPlansDetailsTypeDef = TypedDict(
    "SavingsPlansDetailsTypeDef",
    {"Region": str, "InstanceFamily": str, "OfferingId": str},
    total=False,
)

SavingsPlansPurchaseRecommendationDetailTypeDef = TypedDict(
    "SavingsPlansPurchaseRecommendationDetailTypeDef",
    {
        "SavingsPlansDetails": SavingsPlansDetailsTypeDef,
        "AccountId": str,
        "UpfrontCost": str,
        "EstimatedROI": str,
        "CurrencyCode": str,
        "EstimatedSPCost": str,
        "EstimatedOnDemandCost": str,
        "EstimatedOnDemandCostWithCurrentCommitment": str,
        "EstimatedSavingsAmount": str,
        "EstimatedSavingsPercentage": str,
        "HourlyCommitmentToPurchase": str,
        "EstimatedAverageUtilization": str,
        "EstimatedMonthlySavingsAmount": str,
        "CurrentMinimumHourlyOnDemandSpend": str,
        "CurrentMaximumHourlyOnDemandSpend": str,
        "CurrentAverageHourlyOnDemandSpend": str,
    },
    total=False,
)

SavingsPlansPurchaseRecommendationSummaryTypeDef = TypedDict(
    "SavingsPlansPurchaseRecommendationSummaryTypeDef",
    {
        "EstimatedROI": str,
        "CurrencyCode": str,
        "EstimatedTotalCost": str,
        "CurrentOnDemandSpend": str,
        "EstimatedSavingsAmount": str,
        "TotalRecommendationCount": str,
        "DailyCommitmentToPurchase": str,
        "HourlyCommitmentToPurchase": str,
        "EstimatedSavingsPercentage": str,
        "EstimatedMonthlySavingsAmount": str,
        "EstimatedOnDemandCostWithCurrentCommitment": str,
    },
    total=False,
)

SavingsPlansPurchaseRecommendationTypeDef = TypedDict(
    "SavingsPlansPurchaseRecommendationTypeDef",
    {
        "AccountScope": Literal["PAYER", "LINKED"],
        "SavingsPlansType": Literal["COMPUTE_SP", "EC2_INSTANCE_SP"],
        "TermInYears": Literal["ONE_YEAR", "THREE_YEARS"],
        "PaymentOption": Literal[
            "NO_UPFRONT",
            "PARTIAL_UPFRONT",
            "ALL_UPFRONT",
            "LIGHT_UTILIZATION",
            "MEDIUM_UTILIZATION",
            "HEAVY_UTILIZATION",
        ],
        "LookbackPeriodInDays": Literal["SEVEN_DAYS", "THIRTY_DAYS", "SIXTY_DAYS"],
        "SavingsPlansPurchaseRecommendationDetails": List[
            SavingsPlansPurchaseRecommendationDetailTypeDef
        ],
        "SavingsPlansPurchaseRecommendationSummary": SavingsPlansPurchaseRecommendationSummaryTypeDef,
    },
    total=False,
)

GetSavingsPlansPurchaseRecommendationResponseTypeDef = TypedDict(
    "GetSavingsPlansPurchaseRecommendationResponseTypeDef",
    {
        "Metadata": SavingsPlansPurchaseRecommendationMetadataTypeDef,
        "SavingsPlansPurchaseRecommendation": SavingsPlansPurchaseRecommendationTypeDef,
        "NextPageToken": str,
    },
    total=False,
)

SavingsPlansAmortizedCommitmentTypeDef = TypedDict(
    "SavingsPlansAmortizedCommitmentTypeDef",
    {
        "AmortizedRecurringCommitment": str,
        "AmortizedUpfrontCommitment": str,
        "TotalAmortizedCommitment": str,
    },
    total=False,
)

SavingsPlansSavingsTypeDef = TypedDict(
    "SavingsPlansSavingsTypeDef", {"NetSavings": str, "OnDemandCostEquivalent": str}, total=False
)

SavingsPlansUtilizationTypeDef = TypedDict(
    "SavingsPlansUtilizationTypeDef",
    {
        "TotalCommitment": str,
        "UsedCommitment": str,
        "UnusedCommitment": str,
        "UtilizationPercentage": str,
    },
    total=False,
)

_RequiredSavingsPlansUtilizationAggregatesTypeDef = TypedDict(
    "_RequiredSavingsPlansUtilizationAggregatesTypeDef",
    {"Utilization": SavingsPlansUtilizationTypeDef},
)
_OptionalSavingsPlansUtilizationAggregatesTypeDef = TypedDict(
    "_OptionalSavingsPlansUtilizationAggregatesTypeDef",
    {
        "Savings": SavingsPlansSavingsTypeDef,
        "AmortizedCommitment": SavingsPlansAmortizedCommitmentTypeDef,
    },
    total=False,
)


class SavingsPlansUtilizationAggregatesTypeDef(
    _RequiredSavingsPlansUtilizationAggregatesTypeDef,
    _OptionalSavingsPlansUtilizationAggregatesTypeDef,
):
    pass


SavingsPlansUtilizationDetailTypeDef = TypedDict(
    "SavingsPlansUtilizationDetailTypeDef",
    {
        "SavingsPlanArn": str,
        "Attributes": Dict[str, str],
        "Utilization": SavingsPlansUtilizationTypeDef,
        "Savings": SavingsPlansSavingsTypeDef,
        "AmortizedCommitment": SavingsPlansAmortizedCommitmentTypeDef,
    },
    total=False,
)

_RequiredGetSavingsPlansUtilizationDetailsResponseTypeDef = TypedDict(
    "_RequiredGetSavingsPlansUtilizationDetailsResponseTypeDef",
    {
        "SavingsPlansUtilizationDetails": List[SavingsPlansUtilizationDetailTypeDef],
        "TimePeriod": DateIntervalTypeDef,
    },
)
_OptionalGetSavingsPlansUtilizationDetailsResponseTypeDef = TypedDict(
    "_OptionalGetSavingsPlansUtilizationDetailsResponseTypeDef",
    {"Total": SavingsPlansUtilizationAggregatesTypeDef, "NextToken": str},
    total=False,
)


class GetSavingsPlansUtilizationDetailsResponseTypeDef(
    _RequiredGetSavingsPlansUtilizationDetailsResponseTypeDef,
    _OptionalGetSavingsPlansUtilizationDetailsResponseTypeDef,
):
    pass


_RequiredSavingsPlansUtilizationByTimeTypeDef = TypedDict(
    "_RequiredSavingsPlansUtilizationByTimeTypeDef",
    {"TimePeriod": DateIntervalTypeDef, "Utilization": SavingsPlansUtilizationTypeDef},
)
_OptionalSavingsPlansUtilizationByTimeTypeDef = TypedDict(
    "_OptionalSavingsPlansUtilizationByTimeTypeDef",
    {
        "Savings": SavingsPlansSavingsTypeDef,
        "AmortizedCommitment": SavingsPlansAmortizedCommitmentTypeDef,
    },
    total=False,
)


class SavingsPlansUtilizationByTimeTypeDef(
    _RequiredSavingsPlansUtilizationByTimeTypeDef, _OptionalSavingsPlansUtilizationByTimeTypeDef
):
    pass


_RequiredGetSavingsPlansUtilizationResponseTypeDef = TypedDict(
    "_RequiredGetSavingsPlansUtilizationResponseTypeDef",
    {"Total": SavingsPlansUtilizationAggregatesTypeDef},
)
_OptionalGetSavingsPlansUtilizationResponseTypeDef = TypedDict(
    "_OptionalGetSavingsPlansUtilizationResponseTypeDef",
    {"SavingsPlansUtilizationsByTime": List[SavingsPlansUtilizationByTimeTypeDef]},
    total=False,
)


class GetSavingsPlansUtilizationResponseTypeDef(
    _RequiredGetSavingsPlansUtilizationResponseTypeDef,
    _OptionalGetSavingsPlansUtilizationResponseTypeDef,
):
    pass


_RequiredGetTagsResponseTypeDef = TypedDict(
    "_RequiredGetTagsResponseTypeDef", {"Tags": List[str], "ReturnSize": int, "TotalSize": int}
)
_OptionalGetTagsResponseTypeDef = TypedDict(
    "_OptionalGetTagsResponseTypeDef", {"NextPageToken": str}, total=False
)


class GetTagsResponseTypeDef(_RequiredGetTagsResponseTypeDef, _OptionalGetTagsResponseTypeDef):
    pass


GetUsageForecastResponseTypeDef = TypedDict(
    "GetUsageForecastResponseTypeDef",
    {"Total": MetricValueTypeDef, "ForecastResultsByTime": List[ForecastResultTypeDef]},
    total=False,
)

CostCategoryReferenceTypeDef = TypedDict(
    "CostCategoryReferenceTypeDef",
    {"CostCategoryArn": str, "Name": str, "EffectiveStart": str, "EffectiveEnd": str},
    total=False,
)

ListCostCategoryDefinitionsResponseTypeDef = TypedDict(
    "ListCostCategoryDefinitionsResponseTypeDef",
    {"CostCategoryReferences": List[CostCategoryReferenceTypeDef], "NextToken": str},
    total=False,
)

UpdateCostCategoryDefinitionResponseTypeDef = TypedDict(
    "UpdateCostCategoryDefinitionResponseTypeDef",
    {"CostCategoryArn": str, "EffectiveStart": str},
    total=False,
)
