import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../core/api/api_exceptions.dart';
import '../../../core/models/simulation.dart';
import '../../../core/models/conversion_result.dart';
import '../../../core/providers/dio_provider.dart';

part 'simulator_repository.g.dart';

class SimulatorRepository {
  final Dio _dio;

  SimulatorRepository(this._dio);

  Future<SimulationResult> simulateVolatility({
    required double amountUsd,
    required int daysHistory,
  }) async {
    try {
      final response = await _dio.post(
        '/simulate/volatility',
        data: {'amount_usd': amountUsd, 'days_history': daysHistory},
      );
      return SimulationResult.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw _mapDioException(e);
    }
  }

  Future<ConversionResult> simulateConversion({
    required double amountUsd,
    required int daysHistory,
  }) async {
    try {
      final response = await _dio.post(
        '/simulate/conversion',
        data: {'amount_usd': amountUsd, 'days_history': daysHistory},
      );
      return ConversionResult.fromJson(response.data as Map<String, dynamic>);
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
      e.response?.statusMessage ?? 'Failed to simulate',
      statusCode: e.response?.statusCode,
    );
  }
}

@riverpod
SimulatorRepository simulatorRepository(Ref ref) {
  final dio = ref.watch(dioProvider);
  return SimulatorRepository(dio);
}
