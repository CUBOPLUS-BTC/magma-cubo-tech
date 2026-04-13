import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/utils/formatters.dart';
import '../../../shared/widgets/loading_shimmer.dart';
import '../providers/price_provider.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final priceAsync = ref.watch(priceProvider);

    return SingleChildScrollView(
      physics: const BouncingScrollPhysics(),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _BalanceHero(priceAsync: priceAsync),
            const SizedBox(height: 24),
            _ToolsGrid(context: context),
            const SizedBox(height: 24),
            _WelcomeCard(),
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }
}

class _BalanceHero extends ConsumerWidget {
  final AsyncValue priceAsync;

  const _BalanceHero({required this.priceAsync});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.fromLTRB(16, 24, 16, 24),
      child: Column(
        children: [
          Text(
            'BTC/USD',
            style: AppTypography.labelLarge.copyWith(
              color: AppColors.textSecondary,
            ),
          ),
          const SizedBox(height: 8),
          priceAsync.when(
            data: (price) {
              return Column(
                children: [
                  Text(
                    Formatters.formatUSD(price.priceUsd),
                    style: AppTypography.displayLarge.copyWith(
                      fontSize: 32,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Bitcoin Price',
                    style: AppTypography.mono.copyWith(
                      color: AppColors.textSecondary,
                      fontSize: 14,
                    ),
                  ),
                ],
              );
            },
            loading: () => Column(
              children: [
                const LoadingShimmer(width: 160, height: 32),
                const SizedBox(height: 8),
                LoadingShimmer.text(width: 140),
              ],
            ),
            error: (err, _) => Column(
              children: [
                Text(
                  'Unable to load price',
                  style: AppTypography.bodyMedium.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: 8),
                TextButton(
                  onPressed: () => ref.invalidate(priceProvider),
                  child: Text(
                    'Retry',
                    style: AppTypography.labelLarge.copyWith(
                      color: AppColors.accent,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _ToolsGrid extends StatelessWidget {
  final BuildContext context;

  const _ToolsGrid({required this.context});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
              child: _ToolCard(
                icon: Icons.analytics_outlined,
                title: 'Score',
                subtitle: 'Address health analysis',
                accentColor: AppColors.accent,
                onTap: () => context.go('/score'),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: _ToolCard(
                icon: Icons.candlestick_chart_outlined,
                title: 'Simulator',
                subtitle: 'Volatility & timing',
                accentColor: AppColors.primary,
                onTap: () => context.go('/simulator'),
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        _ToolCardWide(
          icon: Icons.route_outlined,
          title: 'Remittance Optimizer',
          subtitle: 'Compare Lightning, on-chain, and traditional channels',
          accentColor: AppColors.success,
          onTap: () => context.go('/remittance'),
        ),
      ],
    );
  }
}

class _ToolCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color accentColor;
  final VoidCallback onTap;

  const _ToolCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.accentColor,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.surface,
      borderRadius: BorderRadius.circular(8),
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(icon, size: 20, color: accentColor),
              const SizedBox(height: 12),
              Text(
                title,
                style: AppTypography.titleSmall.copyWith(
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 4),
              Text(subtitle, style: AppTypography.bodySmall),
            ],
          ),
        ),
      ),
    );
  }
}

class _ToolCardWide extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color accentColor;
  final VoidCallback onTap;

  const _ToolCardWide({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.accentColor,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.surface,
      borderRadius: BorderRadius.circular(8),
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
          ),
          child: Row(
            children: [
              Icon(icon, size: 20, color: accentColor),
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
                    const SizedBox(height: 4),
                    Text(subtitle, style: AppTypography.bodySmall),
                  ],
                ),
              ),
              Icon(
                Icons.chevron_right_rounded,
                size: 20,
                color: AppColors.textSecondary,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _WelcomeCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            AppColors.primary.withValues(alpha: 0.15),
            AppColors.surface,
          ],
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.primary.withValues(alpha: 0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Image.asset(
                'assets/images/salvium.png',
                height: 36,
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Welcome to Salvium',
                      style: AppTypography.titleMedium.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    Text(
                      'Bitcoin Financial Intelligence for El Salvador',
                      style: AppTypography.bodySmall.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            'The financial intelligence layer that Bitcoin needed in El Salvador. Convert your on-chain activity into real financial decisions.',
            style: AppTypography.bodyMedium.copyWith(
              color: AppColors.textPrimary,
              height: 1.5,
            ),
          ),
          const SizedBox(height: 16),
          Text(
            'What can you do?',
            style: AppTypography.titleSmall.copyWith(
              fontWeight: FontWeight.w600,
              color: AppColors.primary,
            ),
          ),
          const SizedBox(height: 12),
          _WelcomeFeature(
            icon: Icons.analytics_outlined,
            text: 'Check your Bitcoin credit score (0–850)',
            color: AppColors.primary,
          ),
          const SizedBox(height: 8),
          _WelcomeFeature(
            icon: Icons.store_outlined,
            text: 'Optimize conversions if you are a merchant',
            color: AppColors.primary,
          ),
          const SizedBox(height: 8),
          _WelcomeFeature(
            icon: Icons.currency_exchange_outlined,
            text: 'Save on remittance fees',
            color: AppColors.primary,
          ),
          const SizedBox(height: 8),
          _WelcomeFeature(
            icon: Icons.account_balance_outlined,
            text: 'Project your retirement from the informal economy',
            color: AppColors.primary,
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: AppColors.surfaceElevated,
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(
                  Icons.verified_user_outlined,
                  size: 14,
                  color: AppColors.success,
                ),
                const SizedBox(width: 8),
                Text(
                  "Don't trust, verify.",
                  style: AppTypography.labelMedium.copyWith(
                    color: AppColors.success,
                    fontStyle: FontStyle.italic,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _WelcomeFeature extends StatelessWidget {
  final IconData icon;
  final String text;
  final Color color;

  const _WelcomeFeature({required this.icon, required this.text, required this.color});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(6),
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.15),
            borderRadius: BorderRadius.circular(6),
          ),
          child: Icon(icon, size: 16, color: color),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Text(
            text,
            style: AppTypography.bodyMedium.copyWith(
              color: AppColors.textPrimary,
            ),
          ),
        ),
      ],
    );
  }
}
