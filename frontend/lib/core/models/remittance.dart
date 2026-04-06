import 'package:freezed_annotation/freezed_annotation.dart';

part 'remittance.freezed.dart';
part 'remittance.g.dart';

@freezed
abstract class ChannelComparison with _$ChannelComparison {
  const factory ChannelComparison({
    required String name,
    @JsonKey(name: 'fee_percent') required double feePercent,
    @JsonKey(name: 'fee_usd') required double feeUsd,
    @JsonKey(name: 'amount_received') required double amountReceived,
    @JsonKey(name: 'estimated_time') required String estimatedTime,
    @JsonKey(name: 'is_recommended') @Default(false) bool isRecommended,
  }) = _ChannelComparison;

  factory ChannelComparison.fromJson(Map<String, dynamic> json) =>
      _$ChannelComparisonFromJson(json);
}

@freezed
abstract class SendTimeRecommendation with _$SendTimeRecommendation {
  const factory SendTimeRecommendation({
    @JsonKey(name: 'best_time') required String bestTime,
    @JsonKey(name: 'current_fee_sat_vb') required int currentFeeSatVb,
    @JsonKey(name: 'estimated_low_fee_sat_vb')
    required int estimatedLowFeeSatVb,
    @JsonKey(name: 'savings_percent') required double savingsPercent,
  }) = _SendTimeRecommendation;

  factory SendTimeRecommendation.fromJson(Map<String, dynamic> json) =>
      _$SendTimeRecommendationFromJson(json);
}

@freezed
abstract class RemittanceResult with _$RemittanceResult {
  const factory RemittanceResult({
    required List<ChannelComparison> channels,
    @JsonKey(name: 'annual_savings') required double annualSavings,
    @JsonKey(name: 'best_channel') required String bestChannel,
    @JsonKey(name: 'best_time') SendTimeRecommendation? bestTime,
  }) = _RemittanceResult;

  factory RemittanceResult.fromJson(Map<String, dynamic> json) =>
      _$RemittanceResultFromJson(json);
}
