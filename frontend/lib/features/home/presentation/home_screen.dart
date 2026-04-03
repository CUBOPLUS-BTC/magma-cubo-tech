import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/utils/formatters.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  final double _btcPrice = 84231.00;
  final int _sourcesCount = 5;
  final bool _priceVerified = true;
  final int? _score = null;
  final String? _rank = null;
  final int _networkFee = 12;
  final String _feePriority = 'medium';

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildPriceSection(),
          const SizedBox(height: 12),
          _buildMetricCards(),
          const SizedBox(height: 24),
          Text('Quick Actions', style: AppTypography.titleSmall),
          const SizedBox(height: 12),
          _buildActionCard(
            icon: Icons.speed,
            title: 'Analyze Address',
            subtitle: 'Check any Bitcoin address score',
            route: '/score',
          ),
          const SizedBox(height: 8),
          _buildActionCard(
            icon: Icons.show_chart,
            title: 'Volatility Simulator',
            subtitle: 'Simulate BTC price scenarios',
            route: '/simulator',
          ),
          const SizedBox(height: 8),
          _buildActionCard(
            icon: Icons.send,
            title: 'Remittance Optimizer',
            subtitle: 'Compare transfer channels',
            route: '/remittance',
          ),
        ],
      ),
    );
  }

  Widget _buildPriceSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          Formatters.formatUSD(_btcPrice),
          style: AppTypography.displayMedium,
        ),
        const SizedBox(height: 4),
        Row(
          children: [
            Text(
              'from $_sourcesCount sources',
              style: AppTypography.bodySmall,
            ),
            if (_priceVerified) ...[
              const SizedBox(width: 8),
              Icon(Icons.verified, size: 14, color: AppColors.success),
              const SizedBox(width: 4),
              Text(
                'verified',
                style: AppTypography.bodySmall.copyWith(
                  color: AppColors.success,
                ),
              ),
            ],
          ],
        ),
      ],
    );
  }

  Widget _buildMetricCards() {
    return Row(
      children: [
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.surface,
              borderRadius: BorderRadius.circular(4),
              border: Border.all(color: AppColors.borderSubtle),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Score',
                  style: AppTypography.labelMedium,
                ),
                const SizedBox(height: 8),
                Text(
                  _score != null ? Formatters.formatScore(_score) : '---',
                  style: AppTypography.titleLarge,
                ),
                const SizedBox(height: 4),
                Text(
                  _rank ?? 'No data',
                  style: AppTypography.bodySmall,
                ),
              ],
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.surface,
              borderRadius: BorderRadius.circular(4),
              border: Border.all(color: AppColors.borderSubtle),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Network Fee',
                  style: AppTypography.labelMedium,
                ),
                const SizedBox(height: 8),
                Text(
                  Formatters.formatSatVb(_networkFee),
                  style: AppTypography.mono,
                ),
                const SizedBox(height: 4),
                Text(
                  _feePriority,
                  style: AppTypography.bodySmall,
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildActionCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required String route,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(4),
          onTap: () => context.go(route),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Icon(icon, size: 20, color: AppColors.accent),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: AppTypography.titleSmall.copyWith(
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(subtitle, style: AppTypography.bodySmall),
                    ],
                  ),
                ),
                Icon(
                  Icons.chevron_right,
                  size: 20,
                  color: AppColors.textTertiary,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
