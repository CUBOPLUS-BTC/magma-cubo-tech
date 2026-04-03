import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app.dart';
import 'core/providers/auth_provider.dart';

final hasStoredKeyProvider = FutureProvider<bool>((ref) async {
  final authService = ref.watch(authServiceProvider);
  return await authService.hasStoredKey();
});

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: SatsScoreApp()));
}
