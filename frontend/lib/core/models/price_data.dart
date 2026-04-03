import 'package:freezed_annotation/freezed_annotation.dart';

part 'price_data.freezed.dart';
part 'price_data.g.dart';

@freezed
abstract class VerifiedPrice with _$VerifiedPrice {
  const factory VerifiedPrice({
    @JsonKey(name: 'price_usd') required double priceUsd,
    @JsonKey(name: 'sources_count') @Default(0) int sourcesCount,
    @Default(0.0) double deviation,
    @JsonKey(name: 'has_warning') @Default(false) bool hasWarning,
  }) = _VerifiedPrice;

  factory VerifiedPrice.fromJson(Map<String, dynamic> json) =>
      _$VerifiedPriceFromJson(json);
}
