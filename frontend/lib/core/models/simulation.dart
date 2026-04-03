import 'package:freezed_annotation/freezed_annotation.dart';

part 'simulation.freezed.dart';
part 'simulation.g.dart';

@freezed
abstract class DayAnalysis with _$DayAnalysis {
  const factory DayAnalysis({
    @JsonKey(name: 'wait_days') required int waitDays,
    @JsonKey(name: 'avg_return') required double avgReturn,
    @JsonKey(name: 'std_dev') required double stdDev,
    @JsonKey(name: 'worst_case') required double worstCase,
    @JsonKey(name: 'best_case') required double bestCase,
    @JsonKey(name: 'risk_zone') required String riskZone,
  }) = _DayAnalysis;

  factory DayAnalysis.fromJson(Map<String, dynamic> json) =>
      _$DayAnalysisFromJson(json);
}

@freezed
abstract class SimulationResult with _$SimulationResult {
  const factory SimulationResult({
    @JsonKey(name: 'daily_analysis') required List<DayAnalysis> dailyAnalysis,
    required String recommendation,
    @JsonKey(name: 'risk_level') required String riskLevel,
    @JsonKey(name: 'optimal_day') required int optimalDay,
    @JsonKey(name: 'expected_return') required double expectedReturn,
  }) = _SimulationResult;

  factory SimulationResult.fromJson(Map<String, dynamic> json) =>
      _$SimulationResultFromJson(json);
}
