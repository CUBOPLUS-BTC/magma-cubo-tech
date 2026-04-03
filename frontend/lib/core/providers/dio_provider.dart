import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_client.dart';

final dioProvider = Provider<Dio>((ref) {
  return createApiClient();
});
