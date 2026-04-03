import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureKeyStorage {
  static const _keyName = 'nostr_key';

  final FlutterSecureStorage _storage;

  SecureKeyStorage({FlutterSecureStorage? storage})
    : _storage =
          storage ??
          const FlutterSecureStorage(
            aOptions: AndroidOptions(),
            iOptions: IOSOptions(
              accessibility: KeychainAccessibility.first_unlock,
            ),
          );

  Future<void> saveKey(String key) async {
    await _storage.write(key: _keyName, value: key);
  }

  Future<String?> getKey() async {
    return await _storage.read(key: _keyName);
  }

  Future<void> deleteKey() async {
    await _storage.delete(key: _keyName);
  }

  Future<bool> hasKey() async {
    final key = await _storage.read(key: _keyName);
    return key != null && key.isNotEmpty;
  }
}
