import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_typography.dart';
import '../../core/utils/formatters.dart';
import '../../core/models/price_data.dart';

class PriceTicker extends StatelessWidget {
  final VerifiedPrice price;

  const PriceTicker({super.key, required this.price});

  @override
  Widget build(BuildContext context) {
    final formatted = Formatters.formatUSD(price.priceUsd);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        AnimatedSwitcher(
          duration: const Duration(milliseconds: 300),
          child: Text(
            formatted,
            key: ValueKey(formatted),
            style: AppTypography.displayMedium,
          ),
        ),
        const SizedBox(height: 4),
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (price.hasWarning) ...[
              const Icon(
                Icons.warning_amber_rounded,
                size: 14,
                color: AppColors.warning,
              ),
              const SizedBox(width: 4),
            ] else if (price.sourcesCount >= 3) ...[
              Container(
                width: 6,
                height: 6,
                decoration: const BoxDecoration(
                  color: AppColors.success,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 4),
              Text(
                'Verified',
                style: AppTypography.labelMedium.copyWith(
                  color: AppColors.success,
                ),
              ),
              const SizedBox(width: 8),
            ],
            Text(
              'from ${price.sourcesCount} sources',
              style: AppTypography.bodySmall,
            ),
          ],
        ),
      ],
    );
  }
}
