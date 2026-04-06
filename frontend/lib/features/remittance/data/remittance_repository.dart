import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../core/api/api_exceptions.dart';
import '../../../core/models/remittance.dart';
import '../../../core/providers/dio_provider.dart';

part 'remittance_repository.g.dart';

class RemittanceRepository {
  final Dio _dio;

  RemittanceRepository(this._dio);

  Future<RemittanceResult> compareChannels({
    required double amountUsd,
    required String frequency,
  }) async {
    try {
      final response = await _dio.post(
        '/remittance/compare',
        data: {'amount_usd': amountUsd, 'frequency': frequency},
      );
      return RemittanceResult.fromJson(response.data as Map<String, dynamic>);
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
      e.response?.statusMessage ?? 'Failed to compare channels',
      statusCode: e.response?.statusCode,
    );
  }
}

@riverpod
RemittanceRepository remittanceRepository(Ref ref) {
  final dio = ref.watch(dioProvider);
  return RemittanceRepository(dio);
}
