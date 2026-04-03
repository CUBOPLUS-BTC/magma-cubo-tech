import 'package:dio/dio.dart';
import '../constants/api_constants.dart';
import 'api_exceptions.dart';

Dio createApiClient() {
  final dio = Dio(
    BaseOptions(
      baseUrl: ApiConstants.baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 15),
      headers: {'Content-Type': 'application/json'},
    ),
  );

  dio.interceptors.add(
    InterceptorsWrapper(
      onError: (error, handler) {
        if (error.type == DioExceptionType.connectionTimeout ||
            error.type == DioExceptionType.connectionError) {
          return handler.reject(
            DioException(
              requestOptions: error.requestOptions,
              error: const NetworkException(),
            ),
          );
        }
        if (error.response?.statusCode == 401) {
          return handler.reject(
            DioException(
              requestOptions: error.requestOptions,
              error: const UnauthorizedException(),
            ),
          );
        }
        return handler.next(error);
      },
    ),
  );

  return dio;
}
