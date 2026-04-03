import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/models/score_result.dart';
import '../../../core/providers/dio_provider.dart';

class ScoreState {
  final ScoreResult? result;
  final bool isLoading;
  final String? error;

  const ScoreState({this.result, this.isLoading = false, this.error});
}

class ScoreNotifier extends Notifier<ScoreState> {
  @override
  ScoreState build() => const ScoreState();

  Future<void> calculateScore(String address) async {
    state = const ScoreState(isLoading: true);
    try {
      final dio = ref.read(dioProvider);
      final response = await dio.get('/score/$address');
      final result = ScoreResult.fromJson(response.data as Map<String, dynamic>);
      state = ScoreState(result: result);
    } catch (e) {
      state = ScoreState(error: e.toString());
    }
  }
}

final scoreProvider = NotifierProvider<ScoreNotifier, ScoreState>(
  ScoreNotifier.new,
);
