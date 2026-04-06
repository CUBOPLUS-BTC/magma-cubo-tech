import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../core/api/api_exceptions.dart';
import '../../../core/models/price_data.dart';
import '../../../core/providers/dio_provider.dart';

part 'price_repository.g.dart';

class PriceRepository {
  final Dio _dio;

  PriceRepository(this._dio);

  Future<VerifiedPrice> fetchPrice() async {
    try {
      final response = await _dio.get('/price');
      return VerifiedPrice.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw _mapDioException(e);
    }
  }

  ApiException _mapDioException(DioException e) {
    if (e.error is NetworkException) {
      return NetworkException();
    }
    if (e.error is UnauthorizedException) {
      return const UnauthorizedException();
    }
    return ApiException(
      e.response?.statusMessage ?? 'Failed to fetch price',
      statusCode: e.response?.statusCode,
    );
  }
}

@riverpod
PriceRepository priceRepository(Ref ref) {
  final dio = ref.watch(dioProvider);
  return PriceRepository(dio);
}
