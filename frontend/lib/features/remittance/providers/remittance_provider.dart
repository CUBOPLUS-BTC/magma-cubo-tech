import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/models/remittance.dart';
import '../../../core/providers/dio_provider.dart';

class RemittanceState {
  final RemittanceResult? result;
  final bool isLoading;
  final String? error;

  const RemittanceState({this.result, this.isLoading = false, this.error});
}

class RemittanceNotifier extends Notifier<RemittanceState> {
  @override
  RemittanceState build() => const RemittanceState();

  Future<void> compare(double amountUsd, String frequency) async {
    state = const RemittanceState(isLoading: true);
    try {
      final dio = ref.read(dioProvider);
      final response = await dio.post(
        '/remittance/compare',
        data: {
          'amount_usd': amountUsd,
          'frequency': frequency,
        },
      );
      final result =
          RemittanceResult.fromJson(response.data as Map<String, dynamic>);
      state = RemittanceState(result: result);
    } catch (e) {
      state = RemittanceState(error: e.toString());
    }
  }
}

final remittanceProvider =
    NotifierProvider<RemittanceNotifier, RemittanceState>(
  RemittanceNotifier.new,
);
