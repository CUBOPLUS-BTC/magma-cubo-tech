import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/providers/auth_provider.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_typography.dart';

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

  Widget _buildLoginForm() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Welcome Back',
          style: AppTypography.titleLarge.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          'Connect with your Nostr identity',
          style: AppTypography.bodyMedium.copyWith(
            color: AppColors.textSecondary,
          ),
        ),
        const SizedBox(height: 32),
        Text(
          'Private Key',
          style: AppTypography.labelMedium.copyWith(
            color: AppColors.textSecondary,
          ),
        ),
        const SizedBox(height: 8),
        TextField(
          controller: _keyController,
          style: AppTypography.mono.copyWith(
            fontSize: 13,
            color: AppColors.textPrimary,
          ),
          decoration: InputDecoration(
            hintText: 'nsec1...',
            hintStyle: TextStyle(color: AppColors.textTertiary),
            prefixIcon: Padding(
              padding: const EdgeInsets.only(left: 12, right: 8),
              child: Icon(
                Icons.key_outlined,
                size: 16,
                color: AppColors.textTertiary,
              ),
            ),
            prefixIconConstraints: const BoxConstraints(minWidth: 0),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 12,
              vertical: 14,
            ),
            filled: true,
            fillColor: AppColors.surfaceElevated,
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: BorderSide.none,
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: BorderSide(color: AppColors.primary, width: 1),
            ),
          ),
        ),
        if (_error != null) ...[
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.danger.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: AppColors.danger.withValues(alpha: 0.3)),
            ),
            child: Row(
              children: [
                Icon(Icons.error_outline, size: 16, color: AppColors.danger),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _error!,
                    style: AppTypography.bodySmall.copyWith(
                      color: AppColors.danger,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
        const SizedBox(height: 24),
        SizedBox(
          width: double.infinity,
          height: 48,
          child: ElevatedButton(
            onPressed: _isLoading ? null : _handleConnect,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              foregroundColor: Colors.white,
              disabledBackgroundColor: AppColors.primary.withValues(alpha: 0.3),
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            child: _isLoading
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      color: Colors.white,
                    ),
                  )
                : Text(
                    'Connect',
                    style: AppTypography.titleSmall.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
          ),
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(child: Divider(color: AppColors.borderSubtle)),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Text(
                'or',
                style: AppTypography.bodySmall.copyWith(
                  color: AppColors.textTertiary,
                ),
              ),
            ),
            Expanded(child: Divider(color: AppColors.borderSubtle)),
          ],
        ),
        const SizedBox(height: 16),
        SizedBox(
          width: double.infinity,
          height: 48,
          child: OutlinedButton.icon(
            onPressed: _isLoading ? null : _handleGenerateKeys,
            style: OutlinedButton.styleFrom(
              foregroundColor: AppColors.textPrimary,
              side: BorderSide(color: AppColors.borderStrong),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            icon: const Icon(Icons.add_rounded, size: 18),
            label: Text(
              'Generate New Keys',
              style: AppTypography.titleSmall.copyWith(
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ),
        const SizedBox(height: 24),
        Text(
          'Your keys never leave your device',
          style: AppTypography.bodySmall.copyWith(
            color: AppColors.textTertiary,
          ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Container(
            constraints: const BoxConstraints(maxWidth: 900),
            decoration: BoxDecoration(
              color: AppColors.surface,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: AppColors.borderSubtle),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.3),
                  blurRadius: 30,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: LayoutBuilder(
                builder: (context, constraints) {
                  final isWide = constraints.maxWidth > 600;
                  if (isWide) {
                    return Row(
                      children: [
                        Expanded(
                          flex: 5,
                          child: Container(
                            padding: const EdgeInsets.all(40),
                            color: AppColors.surface,
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                Image.asset(
                                  'assets/images/salvium.png',
                                  height: 140,
                                ),
                                const SizedBox(height: 24),
                                Text(
                                  'Bitcoin Financial\nIntelligence',
                                  style: AppTypography.displayMedium.copyWith(
                                    fontSize: 28,
                                    fontWeight: FontWeight.w600,
                                    color: AppColors.textPrimary,
                                    height: 1.3,
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 16),
                                Text(
                                  'Take control of your financial future with intelligent Bitcoin analytics',
                                  style: AppTypography.bodyMedium.copyWith(
                                    color: AppColors.textSecondary,
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                              ],
                            ),
                          ),
                        ),
                        Expanded(
                          flex: 5,
                          child: Container(
                            padding: const EdgeInsets.all(40),
                            child: _buildLoginForm(),
                          ),
                        ),
                      ],
                    );
                  }
                  return Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Container(
                        padding: const EdgeInsets.all(32),
                        color: AppColors.surface,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Image.asset(
                              'assets/images/salvium.png',
                              height: 100,
                            ),
                            const SizedBox(height: 16),
                            Text(
                              'Bitcoin Financial\nIntelligence',
                              style: AppTypography.displayMedium.copyWith(
                                fontSize: 22,
                                fontWeight: FontWeight.w600,
                                color: AppColors.textPrimary,
                                height: 1.3,
                              ),
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.all(24),
                        child: _buildLoginForm(),
                      ),
                    ],
                  );
                },
              ),
            ),
          ),
        ),
      ),
    );
  }
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
      backgroundColor: AppColors.surfaceElevated,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: AppColors.borderStrong),
      ),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 480),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: AppColors.primary.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Icon(
                      Icons.key_rounded,
                      size: 20,
                      color: AppColors.primary,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    'Save Your Keys',
                    style: AppTypography.titleLarge.copyWith(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                      color: AppColors.textPrimary,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.warning.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: AppColors.warning.withValues(alpha: 0.3)),
                ),
                child: Row(
                  children: [
                    Icon(Icons.warning_rounded, size: 18, color: AppColors.warning),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Never share your private key. We cannot recover it if lost.',
                        style: AppTypography.bodySmall.copyWith(
                          color: AppColors.warning,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),
              Text(
                'Public Key (shareable)',
                style: AppTypography.labelLarge.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: 8),
              _KeyBox(keyValue: widget.npub, isPrivate: false),
              const SizedBox(height: 16),
              Text(
                'Private Key (never share)',
                style: AppTypography.labelLarge.copyWith(
                  color: AppColors.danger,
                ),
              ),
              const SizedBox(height: 8),
              _KeyBox(keyValue: widget.nsec, isPrivate: true),
              const SizedBox(height: 20),
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(
                    width: 20,
                    height: 20,
                    child: Checkbox(
                      value: _accepted,
                      onChanged: (v) => setState(() => _accepted = v ?? false),
                      activeColor: AppColors.primary,
                      side: BorderSide(color: AppColors.borderStrong),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(4),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: GestureDetector(
                      onTap: () => setState(() => _accepted = !_accepted),
                      child: Text(
                        'I have saved my keys and understand I cannot recover them if lost',
                        style: AppTypography.bodySmall.copyWith(
                          color: AppColors.textSecondary,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: () => Navigator.of(context).pop(false),
                    style: TextButton.styleFrom(
                      foregroundColor: AppColors.textSecondary,
                    ),
                    child: const Text('Cancel'),
                  ),
                  const SizedBox(width: 12),
                  ElevatedButton(
                    onPressed: _accepted ? () => Navigator.of(context).pop(true) : null,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primary,
                      foregroundColor: Colors.white,
                      disabledBackgroundColor: AppColors.primary.withValues(alpha: 0.3),
                      elevation: 0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
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
}

class _KeyBox extends StatelessWidget {
  final String keyValue;
  final bool isPrivate;

  const _KeyBox({required this.keyValue, required this.isPrivate});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: AppColors.background,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: isPrivate ? AppColors.danger.withValues(alpha: 0.3) : AppColors.borderStrong,
        ),
      ),
      child: Row(
        children: [
          Expanded(
            child: Text(
              keyValue,
              style: AppTypography.monoSmall.copyWith(
                color: AppColors.textPrimary,
              ),
              overflow: TextOverflow.ellipsis,
            ),
          ),
          const SizedBox(width: 8),
          _CopyButton(text: keyValue, isPrivate: isPrivate),
        ],
      ),
    );
  }
}

class _CopyButton extends StatelessWidget {
  final String text;
  final bool isPrivate;

  const _CopyButton({required this.text, required this.isPrivate});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(6),
      onTap: () {
        Clipboard.setData(ClipboardData(text: text));
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              isPrivate ? 'Private key copied - store it securely' : 'Public key copied',
              style: TextStyle(color: AppColors.textPrimary),
            ),
            duration: const Duration(seconds: 2),
            backgroundColor: AppColors.surface,
          ),
        );
      },
      child: Container(
        padding: const EdgeInsets.all(6),
        decoration: BoxDecoration(
          color: AppColors.surfaceElevated,
          borderRadius: BorderRadius.circular(6),
        ),
        child: Icon(
          Icons.copy_outlined,
          size: 14,
          color: AppColors.textSecondary,
        ),
      ),
    );
  }
}
