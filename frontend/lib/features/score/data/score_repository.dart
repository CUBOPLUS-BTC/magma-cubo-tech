import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../core/api/api_exceptions.dart';
import '../../../core/models/score_result.dart';
import '../../../core/providers/dio_provider.dart';

part 'score_repository.g.dart';

class ScoreRepository {
  final Dio _dio;

  ScoreRepository(this._dio);

  Future<ScoreResult> fetchScore(String address) async {
    try {
      final response = await _dio.get('/score/$address');
      return ScoreResult.fromJson(response.data as Map<String, dynamic>);
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
    if (e.response?.statusCode == 404) {
      return const ApiException('Address not found', statusCode: 404);
    }
    return ApiException(
      e.response?.statusMessage ?? 'Failed to fetch score',
      statusCode: e.response?.statusCode,
    );
  }
}

@riverpod
ScoreRepository scoreRepository(Ref ref) {
  final dio = ref.watch(dioProvider);
  return ScoreRepository(dio);
}
