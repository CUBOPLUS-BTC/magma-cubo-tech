import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_typography.dart';
import '../../core/utils/validators.dart';

class BTCAddressInput extends StatefulWidget {
  final ValueChanged<String> onSubmit;
  final bool isLoading;

  const BTCAddressInput({
    super.key,
    required this.onSubmit,
    this.isLoading = false,
  });

  @override
  State<BTCAddressInput> createState() => _BTCAddressInputState();
}

class _BTCAddressInputState extends State<BTCAddressInput> {
  final _controller = TextEditingController();
  String? _error;

  void _submit() {
    final value = _controller.text.trim();
    final validation = Validators.validateBTCAddress(value);
    if (validation != null) {
      setState(() => _error = validation);
      return;
    }
    setState(() => _error = null);
    widget.onSubmit(value);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: _error != null ? AppColors.danger : AppColors.borderSubtle,
            ),
          ),
          child: TextField(
            controller: _controller,
            style: AppTypography.mono,
            decoration: InputDecoration(
              hintText: 'bc1q...',
              hintStyle: AppTypography.mono.copyWith(
                color: AppColors.textTertiary,
              ),
              prefixIcon: const Icon(
                Icons.currency_bitcoin,
                color: AppColors.accent,
                size: 18,
              ),
              suffixIcon: Padding(
                padding: const EdgeInsets.only(right: 4),
                child: TextButton(
                  onPressed: widget.isLoading ? null : _submit,
                  style: TextButton.styleFrom(
                    foregroundColor: AppColors.accent,
                    disabledForegroundColor: AppColors.textTertiary,
                    padding: const EdgeInsets.symmetric(horizontal: 12),
                    minimumSize: Size.zero,
                    tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  ),
                  child: widget.isLoading
                      ? const SizedBox(
                          width: 14,
                          height: 14,
                          child: CircularProgressIndicator(
                            strokeWidth: 1.5,
                            color: AppColors.accent,
                          ),
                        )
                      : Text(
                          'Verify',
                          style: AppTypography.bodyMedium.copyWith(
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                ),
              ),
              border: InputBorder.none,
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 14,
              ),
            ),
            onSubmitted: (_) => _submit(),
          ),
        ),
        if (_error != null) ...[
          const SizedBox(height: 4),
          Text(
            _error!,
            style: AppTypography.bodySmall.copyWith(color: AppColors.danger),
          ),
        ],
      ],
    );
  }
}
