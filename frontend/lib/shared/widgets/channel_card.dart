import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
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
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
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
                  style: GoogleFonts.outfit(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary,
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
                    style: GoogleFonts.dmSans(
                      fontSize: 10,
                      fontWeight: FontWeight.w500,
                      letterSpacing: 0.04,
                      color: AppColors.accent,
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 10),
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
          Text(
            channel.estimatedTime,
            style: AppTypography.bodySmall,
          ),
        ],
      ),
    );
  }
}
