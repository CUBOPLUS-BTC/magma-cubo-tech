import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/nostr_auth_service.dart';

final authServiceProvider = Provider<NostrAuthService>((ref) {
  return NostrAuthService();
});
