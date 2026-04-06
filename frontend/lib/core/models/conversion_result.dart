import 'package:freezed_annotation/freezed_annotation.dart';

part 'conversion_result.freezed.dart';
part 'conversion_result.g.dart';

@freezed
abstract class PurchaseStrategy with _$PurchaseStrategy {
  const factory PurchaseStrategy({
    @JsonKey(name: 'amount_btc') required double amountBtc,
    @JsonKey(name: 'risk_level') required String riskLevel,
    @JsonKey(name: 'sharpe_ratio') required double sharpeRatio,
  }) = _PurchaseStrategy;

  factory PurchaseStrategy.fromJson(Map<String, dynamic> json) =>
      _$PurchaseStrategyFromJson(json);
}

@freezed
abstract class DcaStrategy with _$DcaStrategy {
  const factory DcaStrategy({
    @JsonKey(name: 'amount_btc') required double amountBtc,
    @JsonKey(name: 'num_purchases') required int numPurchases,
    @JsonKey(name: 'risk_level') required String riskLevel,
    @JsonKey(name: 'sharpe_ratio') required double sharpeRatio,
  }) = _DcaStrategy;

  factory DcaStrategy.fromJson(Map<String, dynamic> json) =>
      _$DcaStrategyFromJson(json);
}

@freezed
abstract class ConversionResult with _$ConversionResult {
  const factory ConversionResult({
    required String strategy,
    required String explanation,
    @JsonKey(name: 'lump_sum') required PurchaseStrategy lumpSum,
    required DcaStrategy dca,
  }) = _ConversionResult;

  factory ConversionResult.fromJson(Map<String, dynamic> json) =>
      _$ConversionResultFromJson(json);
}
