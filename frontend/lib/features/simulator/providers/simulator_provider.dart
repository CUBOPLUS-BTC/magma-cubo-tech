import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/models/simulation.dart';
import '../../../core/providers/dio_provider.dart';

class SimulatorState {
  final SimulationResult? result;
  final bool isLoading;
  final String? error;

  const SimulatorState({this.result, this.isLoading = false, this.error});
}

class SimulatorNotifier extends Notifier<SimulatorState> {
  @override
  SimulatorState build() => const SimulatorState();

  Future<void> simulate(double amountUsd, int daysHistory) async {
    state = const SimulatorState(isLoading: true);
    try {
      final dio = ref.read(dioProvider);
      final response = await dio.post(
        '/simulate/volatility',
        data: {
          'amount_usd': amountUsd,
          'days_history': daysHistory,
        },
      );
      final result =
          SimulationResult.fromJson(response.data as Map<String, dynamic>);
      state = SimulatorState(result: result);
    } catch (e) {
      state = SimulatorState(error: e.toString());
    }
  }
}

final simulatorProvider =
    NotifierProvider<SimulatorNotifier, SimulatorState>(
  SimulatorNotifier.new,
);
