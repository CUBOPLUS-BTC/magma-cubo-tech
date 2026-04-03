import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_typography.dart';
import '../../core/utils/formatters.dart';

class SavingsCard extends StatelessWidget {
  final double annualSavings;
  final String vsChannel;
  final double monthlyAmount;

  const SavingsCard({
    super.key,
    required this.annualSavings,
    required this.vsChannel,
    required this.monthlyAmount,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: const Border(
          left: BorderSide(color: AppColors.accent, width: 3),
          top: BorderSide(color: AppColors.borderSubtle),
          right: BorderSide(color: AppColors.borderSubtle),
          bottom: BorderSide(color: AppColors.borderSubtle),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'ANNUAL SAVINGS',
            style: AppTypography.labelMedium.copyWith(
              color: AppColors.accent,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            Formatters.formatUSD(annualSavings),
            style: GoogleFonts.outfit(
              fontSize: 28,
              fontWeight: FontWeight.w700,
              color: AppColors.success,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'vs $vsChannel, sending \$${monthlyAmount.toStringAsFixed(0)}/month',
            style: AppTypography.bodySmall,
          ),
        ],
      ),
    );
  }
}
