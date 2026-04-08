import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_typography.dart';
import '../../core/utils/formatters.dart';
import '../../core/models/remittance.dart';

class ChannelCard extends StatelessWidget {
  final ChannelComparison channel;

  const ChannelCard({super.key, required this.channel});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: channel.isRecommended
              ? AppColors.accent
              : AppColors.borderSubtle,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  channel.name,
                  style: AppTypography.titleSmall.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              if (channel.isRecommended)
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 6,
                    vertical: 2,
                  ),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(4),
                    border: Border.all(color: AppColors.accent),
                  ),
                  child: Text(
                    'RECOMMENDED',
                    style: AppTypography.labelSmall.copyWith(
                      color: AppColors.accent,
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: Text(
                  '${channel.feePercent.toStringAsFixed(2)}% fee',
                  style: AppTypography.bodyMedium,
                ),
              ),
              Text(
                Formatters.formatUSD(channel.amountReceived),
                style: AppTypography.mono,
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(channel.estimatedTime, style: AppTypography.bodySmall),
        ],
      ),
    );
  }
}
