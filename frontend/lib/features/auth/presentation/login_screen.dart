import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/providers/auth_provider.dart';
import '../../../core/theme/app_colors.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _keyController = TextEditingController();
  bool _isLoading = false;
  String? _error;

  @override
  void dispose() {
    _keyController.dispose();
    super.dispose();
  }

  Future<void> _handleConnect() async {
    final key = _keyController.text.trim();
    if (key.isEmpty) {
      setState(() => _error = 'Please enter your key');
      return;
    }

    if (!key.startsWith('nsec1') &&
        !key.startsWith('npub1') &&
        key.length != 64) {
      setState(() => _error = 'Invalid key format. Use nsec1... or npub1...');
      return;
    }

    if (key.startsWith('npub1')) {
      setState(() => _error = 'Please enter your private key (nsec1)');
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
    });

    final authService = ref.read(authServiceProvider);
    final success = await authService.login(key);

    if (!mounted) return;

    setState(() => _isLoading = false);

    if (success) {
      context.go('/home');
    } else {
      setState(() => _error = 'Authentication failed. Please try again.');
    }
  }

  Future<void> _handleGenerateKeys() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final authService = ref.read(authServiceProvider);
      final keyPair = authService.generateKeyPairSync();

      if (!mounted) return;

      final npub = authService.encodePublicKeyToBech32(keyPair.public);
      final nsec = authService.encodePrivateKeyToBech32(keyPair.private);

      final confirmed = await showDialog<bool>(
        context: context,
        barrierDismissible: false,
        builder: (context) => _KeyGeneratedDialog(npub: npub, nsec: nsec),
      );

      if (confirmed == true && mounted) {
        final success = await authService.login(nsec);
        if (success && mounted) {
          context.go('/home');
        } else {
          setState(() {
            _isLoading = false;
            _error = 'Authentication failed. Please try again.';
          });
        }
      } else {
        setState(() => _isLoading = false);
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoading = false;
          _error = 'Error generating keys: $e';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 400),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildLogo(),
                const SizedBox(height: 32),
                Text('SatsScore', style: _titleStyle),
                const SizedBox(height: 8),
                Text('Bitcoin Financial Intelligence', style: _subtitleStyle),
                const SizedBox(height: 48),
                _buildKeyInput(),
                if (_error != null) ...[
                  const SizedBox(height: 12),
                  Text(_error!, style: _errorStyle),
                ],
                const SizedBox(height: 24),
                _buildConnectButton(),
                const SizedBox(height: 16),
                _buildGenerateButton(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildLogo() {
    return Container(
      width: 48,
      height: 48,
      decoration: BoxDecoration(
        color: AppColors.accent,
        borderRadius: BorderRadius.circular(8),
      ),
      child: const Icon(Icons.bolt, size: 28, color: Colors.black),
    );
  }

  Widget _buildKeyInput() {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: TextField(
        controller: _keyController,
        style: const TextStyle(
          fontSize: 14,
          color: AppColors.textPrimary,
          fontFamily: 'monospace',
        ),
        decoration: InputDecoration(
          hintText: 'nsec1...',
          hintStyle: TextStyle(color: AppColors.textTertiary),
          prefixIcon: Icon(Icons.key, size: 18, color: AppColors.accent),
          border: InputBorder.none,
          contentPadding: const EdgeInsets.all(16),
        ),
      ),
    );
  }

  Widget _buildConnectButton() {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: ElevatedButton(
        onPressed: _isLoading ? null : _handleConnect,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.accent,
          foregroundColor: Colors.black,
          disabledBackgroundColor: AppColors.accent.withValues(alpha: 0.5),
        ),
        child: _isLoading
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(strokeWidth: 2),
              )
            : const Text(
                'Connect',
                style: TextStyle(fontWeight: FontWeight.w600),
              ),
      ),
    );
  }

  Widget _buildGenerateButton() {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: OutlinedButton(
        onPressed: _isLoading ? null : _handleGenerateKeys,
        style: OutlinedButton.styleFrom(
          side: BorderSide(color: AppColors.borderSubtle),
          foregroundColor: AppColors.textPrimary,
        ),
        child: const Text('Generate new keys'),
      ),
    );
  }

  TextStyle get _titleStyle => const TextStyle(
    fontSize: 28,
    fontWeight: FontWeight.w700,
    color: AppColors.textPrimary,
  );

  TextStyle get _subtitleStyle =>
      TextStyle(fontSize: 14, color: AppColors.textSecondary);

  TextStyle get _errorStyle => TextStyle(fontSize: 12, color: Colors.red[400]);
}

class _KeyGeneratedDialog extends StatefulWidget {
  final String npub;
  final String nsec;

  const _KeyGeneratedDialog({required this.npub, required this.nsec});

  @override
  State<_KeyGeneratedDialog> createState() => _KeyGeneratedDialogState();
}

class _KeyGeneratedDialogState extends State<_KeyGeneratedDialog> {
  bool _accepted = false;

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: AppColors.surface,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 420),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    Icons.warning_amber_rounded,
                    color: Colors.amber[600],
                    size: 28,
                  ),
                  const SizedBox(width: 12),
                  const Text(
                    'IMPORTANT - SAVE YOUR KEYS',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              const Text(
                'Public key (shareable):',
                style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
              ),
              const SizedBox(height: 8),
              _buildKeyBox(widget.npub, false),
              const SizedBox(height: 16),
              const Text(
                'Private key (NEVER share):',
                style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
              ),
              const SizedBox(height: 8),
              _buildKeyBox(widget.nsec, true),
              const SizedBox(height: 16),
              CheckboxListTile(
                value: _accepted,
                onChanged: (v) => setState(() => _accepted = v ?? false),
                controlAffinity: ListTileControlAffinity.leading,
                contentPadding: EdgeInsets.zero,
                title: Text(
                  'I understand that if I lose these keys I will lose access to my account',
                  style: TextStyle(
                    fontSize: 12,
                    color: AppColors.textSecondary,
                  ),
                ),
                activeColor: AppColors.accent,
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: () => Navigator.of(context).pop(false),
                    child: Text(
                      'Cancel',
                      style: TextStyle(color: AppColors.textSecondary),
                    ),
                  ),
                  const SizedBox(width: 12),
                  ElevatedButton(
                    onPressed: _accepted
                        ? () => Navigator.of(context).pop(true)
                        : null,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.accent,
                      foregroundColor: Colors.black,
                      disabledBackgroundColor: AppColors.accent.withValues(
                        alpha: 0.3,
                      ),
                    ),
                    child: const Text('Continue'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildKeyBox(String key, bool isPrivate) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.background,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Row(
        children: [
          Expanded(
            child: Text(
              key,
              style: TextStyle(
                fontSize: 12,
                fontFamily: 'monospace',
                color: isPrivate ? Colors.amber[300] : AppColors.textPrimary,
              ),
              overflow: TextOverflow.ellipsis,
            ),
          ),
          IconButton(
            icon: Icon(Icons.copy, size: 16, color: AppColors.textSecondary),
            onPressed: () {
              Clipboard.setData(ClipboardData(text: key));
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('Copied to clipboard'),
                  duration: const Duration(seconds: 2),
                ),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.download, size: 16, color: AppColors.accent),
            onPressed: () => _downloadKeys(key, isPrivate),
          ),
        ],
      ),
    );
  }

  Future<void> _downloadKeys(String key, bool isPrivate) async {
    await Clipboard.setData(ClipboardData(text: key));
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(isPrivate
              ? 'Private key copied - save it securely!'
              : 'Public key copied to clipboard'),
        ),
      );
    }
  }
}
