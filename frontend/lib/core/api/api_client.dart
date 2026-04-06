import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import '../constants/api_constants.dart';
import '../services/secure_key_storage.dart';
import 'api_exceptions.dart';

Dio createApiClient({SecureKeyStorage? authStorage}) {
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
      onRequest: (options, handler) async {
        if (authStorage != null) {
          try {
            final key = await authStorage.getKey();
            if (key != null && key.isNotEmpty) {
              options.headers['Authorization'] = 'Nostr $key';
            }
          } catch (e) {
            debugPrint('Failed to load auth key: $e');
          }
        }
        return handler.next(options);
      },
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
