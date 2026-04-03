import 'dart:developer' as developer;
import 'package:dart_nostr/dart_nostr.dart';
import 'package:dio/dio.dart';
import '../constants/api_constants.dart';
import 'secure_key_storage.dart';

class NostrAuthService {
  final Dio _dio;
  final SecureKeyStorage _keyStorage;
  final _keys = Nostr.instance.services.keys;
  final _bech32 = Nostr.instance.services.bech32;

  NostrAuthService({Dio? dio, SecureKeyStorage? keyStorage})
    : _dio = dio ?? Dio(),
      _keyStorage = keyStorage ?? SecureKeyStorage();

  String decodePrivateKey(String nsec) {
    if (nsec.startsWith('nsec1')) {
      return _bech32.decodeNsecKeyToPrivateKey(nsec);
    }
    if (nsec.length == 64 && RegExp(r'^[0-9a-fA-F]+$').hasMatch(nsec)) {
      return nsec.toLowerCase();
    }
    throw const FormatException('Invalid private key format');
  }

  String decodePublicKey(String npub) {
    if (npub.startsWith('npub1')) {
      return _bech32.decodeNpubKeyToPublicKey(npub);
    }
    if (npub.length == 64 && RegExp(r'^[0-9a-fA-F]+$').hasMatch(npub)) {
      return npub.toLowerCase();
    }
    throw const FormatException('Invalid public key format');
  }

  String encodePublicKeyToBech32(String hexPubkey) {
    return _bech32.encodePublicKeyToNpub(hexPubkey);
  }

  String encodePrivateKeyToBech32(String hexPrivkey) {
    return _bech32.encodePrivateKeyToNsec(hexPrivkey);
  }

  String getPublicKeyFromHex(String privateKeyHex) {
    return _keys.derivePublicKey(privateKey: privateKeyHex);
  }

  NostrKeyPairs generateKeyPairSync() {
    return _keys.generateKeyPair();
  }

  Future<String> getChallenge(String pubkey) async {
    final response = await _dio.post(
      ApiConstants.authChallenge,
      data: {'pubkey': pubkey},
    );
    return response.data['challenge'] as String;
  }

  Future<bool> verifyAuth(
    String privateKeyHex,
    String url,
    String method,
  ) async {
    try {
      final keyPair = _keys.generateKeyPairFromExistingPrivateKey(privateKeyHex);
      final challenge = await getChallenge(keyPair.public);

      final event = NostrEvent.fromPartialData(
        kind: 27235,
        content: challenge,
        keyPairs: keyPair,
        tags: [
          ['u', url],
          ['method', method],
        ],
      );

      final response = await _dio.post(
        ApiConstants.authVerify,
        data: {
          'signed_event': event.toMap(),
          'challenge': challenge,
        },
        options: Options(headers: {'Content-Type': 'application/json'}),
      );
      return response.data['success'] == true;
    } on DioException catch (e) {
      developer.log(
        'Auth verification failed',
        name: 'NostrAuth',
        error: e.response?.data ?? e.message,
      );
      return false;
    } catch (e) {
      developer.log('Auth error', name: 'NostrAuth', error: e);
      return false;
    }
  }

  Future<bool> login(String nsecBech32) async {
    try {
      final hexKey = decodePrivateKey(nsecBech32);
      final isValid = await verifyAuth(hexKey, ApiConstants.authVerify, 'POST');
      if (isValid) {
        await _keyStorage.saveKey(hexKey);
      }
      return isValid;
    } catch (e) {
      developer.log('Login failed', name: 'NostrAuth', error: e);
      return false;
    }
  }

  Future<String?> getStoredKeyHex() async {
    return _keyStorage.getKey();
  }

  Future<bool> hasStoredKey() async {
    return _keyStorage.hasKey();
  }

  Future<void> logout() async {
    await _keyStorage.deleteKey();
  }

  Future<String?> getPublicKeyFromStored() async {
    final hexKey = await _keyStorage.getKey();
    if (hexKey == null) return null;
    return getPublicKeyFromHex(hexKey);
  }
}
