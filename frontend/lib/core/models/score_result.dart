import 'package:freezed_annotation/freezed_annotation.dart';

part 'score_result.freezed.dart';
part 'score_result.g.dart';

@freezed
abstract class ScoreComponent with _$ScoreComponent {
  const factory ScoreComponent({required int score, required int max}) =
      _ScoreComponent;

  factory ScoreComponent.fromJson(Map<String, dynamic> json) =>
      _$ScoreComponentFromJson(json);
}

@freezed
abstract class ScoreBreakdown with _$ScoreBreakdown {
  const factory ScoreBreakdown({
    required ScoreComponent consistency,
    @JsonKey(name: 'relative_volume') required ScoreComponent relativeVolume,
    required ScoreComponent diversification,
    @JsonKey(name: 'savings_pattern') required ScoreComponent savingsPattern,
    @JsonKey(name: 'payment_history') required ScoreComponent paymentHistory,
    @JsonKey(name: 'lightning_activity')
    required ScoreComponent lightningActivity,
  }) = _ScoreBreakdown;

  factory ScoreBreakdown.fromJson(Map<String, dynamic> json) =>
      _$ScoreBreakdownFromJson(json);
}

@freezed
abstract class ScoreResult with _$ScoreResult {
  const factory ScoreResult({
    @JsonKey(name: 'total_score') required int totalScore,
    required String rank,
    required String address,
    required ScoreBreakdown breakdown,
    required List<String> recommendations,
  }) = _ScoreResult;

  factory ScoreResult.fromJson(Map<String, dynamic> json) =>
      _$ScoreResultFromJson(json);
}
