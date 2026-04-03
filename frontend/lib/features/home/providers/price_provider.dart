import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/models/price_data.dart';
import '../../../core/providers/dio_provider.dart';

final priceProvider = FutureProvider.autoDispose<VerifiedPrice>((ref) async {
  final dio = ref.read(dioProvider);
  final response = await dio.get('/price');
  return VerifiedPrice.fromJson(response.data as Map<String, dynamic>);
});
