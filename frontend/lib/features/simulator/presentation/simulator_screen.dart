import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/utils/formatters.dart';
import '../../../core/models/simulation.dart';
import '../../../shared/widgets/loading_shimmer.dart';
import '../../../shared/widgets/risk_chart.dart';
import '../providers/simulator_provider.dart';

class SimulatorScreen extends ConsumerStatefulWidget {
  const SimulatorScreen({super.key});

  @override
  ConsumerState<SimulatorScreen> createState() => _SimulatorScreenState();
}

class _SimulatorScreenState extends ConsumerState<SimulatorScreen> {
  final _amountController = TextEditingController();
  int _period = 90;

  static const _periodOptions = {
    '30 days': 30,
    '90 days': 90,
    '180 days': 180,
    '1 year': 365,
  };

  @override
  void dispose() {
    _amountController.dispose();
    super.dispose();
  }

  void _handleSimulate() {
    final amountText = _amountController.text.trim();
    if (amountText.isEmpty) return;

    final amount = double.tryParse(amountText);
    if (amount == null || amount <= 0) return;

    ref.read(simulatorProvider.notifier).simulate(amount, _period);
  }

  Color _riskColor(String riskZone) {
    switch (riskZone.toLowerCase()) {
      case 'low':
        return AppColors.success;
      case 'medium':
        return AppColors.warning;
      case 'high':
        return AppColors.danger;
      default:
        return AppColors.textTertiary;
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(simulatorProvider);

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(),
          const SizedBox(height: 24),
          _buildInputCard(),
          const SizedBox(height: 16),
          _buildSimulateButton(state.isLoading),
          const SizedBox(height: 24),
          if (state.error != null) _buildError(state.error!),
          if (state.isLoading) _buildLoading(),
          if (state.result == null && !state.isLoading && state.error == null)
            _buildEmpty(),
          if (state.result != null && !state.isLoading) _buildResult(state),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: AppColors.primary.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(
                Icons.candlestick_chart_rounded,
                color: AppColors.primary,
                size: 24,
              ),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Volatility Simulator', style: AppTypography.titleLarge),
                Text(
                  'Predict optimal timing for Bitcoin transactions',
                  style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
                ),
              ],
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildInputCard() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Simulation Parameters', style: AppTypography.labelMedium),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                flex: 3,
                child: TextField(
                  controller: _amountController,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  style: AppTypography.mono.copyWith(fontSize: 18),
                  decoration: InputDecoration(
                    hintText: '0.00',
                    prefixText: '\$ ',
                    prefixStyle: AppTypography.mono.copyWith(
                      color: AppColors.textSecondary,
                      fontSize: 18,
                    ),
                    filled: true,
                    fillColor: AppColors.surfaceElevated,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                flex: 2,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12),
                  decoration: BoxDecoration(
                    color: AppColors.surfaceElevated,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<int>(
                      value: _period,
                      isExpanded: true,
                      dropdownColor: AppColors.surfaceElevated,
                      style: AppTypography.mono,
                      icon: Icon(Icons.keyboard_arrow_down_rounded, color: AppColors.textSecondary),
                      items: _periodOptions.entries
                          .map(
                            (e) => DropdownMenuItem(
                              value: e.value,
                              child: Text(
                                e.key,
                                style: AppTypography.bodyMedium.copyWith(
                                  color: AppColors.textPrimary,
                                ),
                              ),
                            ),
                          )
                          .toList(),
                      onChanged: (v) {
                        if (v != null) setState(() => _period = v);
                      },
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSimulateButton(bool isLoading) {
    return SizedBox(
      width: double.infinity,
      height: 52,
      child: ElevatedButton(
        onPressed: isLoading ? null : _handleSimulate,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          disabledBackgroundColor: AppColors.primary.withValues(alpha: 0.3),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
        child: isLoading
            ? const SizedBox(
                width: 22,
                height: 22,
                child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white),
              )
            : Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.play_arrow_rounded, size: 22),
                  const SizedBox(width: 8),
                  Text(
                    'Run Simulation',
                    style: AppTypography.titleSmall.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
      ),
    );
  }

  Widget _buildEmpty() {
    return Container(
      margin: const EdgeInsets.only(top: 32),
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: AppColors.primary.withValues(alpha: 0.1),
              shape: BoxShape.circle,
            ),
            child: const Icon(
              Icons.auto_graph_rounded,
              size: 48,
              color: AppColors.primary,
            ),
          ),
          const SizedBox(height: 20),
          Text('Predict the best moment', style: AppTypography.titleMedium),
          const SizedBox(height: 8),
          Text(
            'Simulate Bitcoin volatility to find when\nto buy, sell, or send with less risk',
            style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildLoading() {
    return Padding(
      padding: const EdgeInsets.only(top: 16),
      child: Column(
        children: [
          LoadingShimmer.card(height: 100),
          const SizedBox(height: 12),
          LoadingShimmer.card(height: 240),
          const SizedBox(height: 12),
          LoadingShimmer.card(height: 200),
        ],
      ),
    );
  }

  Widget _buildError(String error) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.danger.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.danger.withValues(alpha: 0.2)),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: AppColors.danger.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(Icons.error_outline_rounded, size: 20, color: AppColors.danger),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              error,
              style: AppTypography.bodyMedium.copyWith(color: AppColors.danger),
            ),
          ),
          IconButton(
            onPressed: () {
              final amountText = _amountController.text.trim();
              if (amountText.isEmpty) return;
              final amount = double.tryParse(amountText);
              if (amount == null || amount <= 0) return;
              ref.read(simulatorProvider.notifier).simulate(amount, _period);
            },
            icon: const Icon(Icons.refresh_rounded, color: AppColors.danger),
          ),
        ],
      ),
    );
  }

  Widget _buildResult(SimulatorState state) {
    final result = state.result!;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildRecommendationCard(result),
        const SizedBox(height: 16),
        _buildQuickStats(result),
        const SizedBox(height: 16),
        _buildChartCard(result),
        const SizedBox(height: 16),
        _buildDataTable(result),
      ],
    );
  }

  Widget _buildQuickStats(SimulationResult result) {
    return Row(
      children: [
        _statChip(
          icon: Icons.calendar_today_rounded,
          label: 'Optimal',
          value: '${result.optimalDay}d',
          color: AppColors.primary,
        ),
        const SizedBox(width: 10),
        _statChip(
          icon: Icons.trending_up_rounded,
          label: 'Expected',
          value: Formatters.formatPercentage(result.expectedReturn),
          color: AppColors.success,
        ),
        const SizedBox(width: 10),
        _statChip(
          icon: Icons.shield_rounded,
          label: 'Risk',
          value: result.riskLevel.toUpperCase(),
          color: _riskColor(result.riskLevel),
        ),
      ],
    );
  }

  Widget _statChip({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
  }) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 10),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withValues(alpha: 0.15)),
        ),
        child: Column(
          children: [
            Icon(icon, size: 18, color: color),
            const SizedBox(height: 6),
            Text(
              value,
              style: AppTypography.mono.copyWith(
                color: color,
                fontWeight: FontWeight.w600,
                fontSize: 14,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              label,
              style: AppTypography.labelSmall.copyWith(
                color: AppColors.textSecondary,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRecommendationCard(SimulationResult result) {
    final riskColor = _riskColor(result.riskLevel);

    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            AppColors.surface,
            AppColors.surfaceElevated.withValues(alpha: 0.5),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.primary.withValues(alpha: 0.08),
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(15),
                topRight: Radius.circular(15),
              ),
            ),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: AppColors.primary.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(
                    Icons.lightbulb_rounded,
                    size: 18,
                    color: AppColors.primary,
                  ),
                ),
                const SizedBox(width: 10),
                Text(
                  'RECOMMENDATION',
                  style: AppTypography.labelMedium.copyWith(
                    color: AppColors.primary,
                    letterSpacing: 1.2,
                  ),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: riskColor.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        result.riskLevel.toLowerCase() == 'low'
                            ? Icons.check_circle
                            : result.riskLevel.toLowerCase() == 'medium'
                                ? Icons.warning_rounded
                                : Icons.error,
                        size: 12,
                        color: riskColor,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        result.riskLevel.toUpperCase(),
                        style: AppTypography.labelSmall.copyWith(color: riskColor),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text(
              result.recommendation,
              style: AppTypography.bodyLarge.copyWith(height: 1.5),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildChartCard(SimulationResult result) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.show_chart_rounded, size: 18, color: AppColors.primary),
              const SizedBox(width: 8),
              Text('Daily Analysis', style: AppTypography.titleSmall),
            ],
          ),
          const SizedBox(height: 16),
          RiskChart(data: result.dailyAnalysis),
        ],
      ),
    );
  }

  Widget _buildDataTable(SimulationResult result) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: AppColors.surfaceElevated,
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(15),
                topRight: Radius.circular(15),
              ),
            ),
            child: Row(
              children: [
                Expanded(flex: 2, child: Text('Day', style: AppTypography.labelMedium)),
                Expanded(flex: 3, child: Text('Avg Return', style: AppTypography.labelMedium)),
                Expanded(flex: 2, child: Text('Risk', style: AppTypography.labelMedium)),
                Expanded(flex: 3, child: Text('Worst Case', style: AppTypography.labelMedium)),
              ],
            ),
          ),
          ...result.dailyAnalysis.map<Widget>((day) {
            final isOptimal = day.waitDays == result.optimalDay;
            final riskColor = _riskColor(day.riskZone);

            return Container(
              color: isOptimal ? AppColors.primary.withValues(alpha: 0.06) : null,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: Row(
                      children: [
                        if (isOptimal)
                          Container(
                            padding: const EdgeInsets.all(4),
                            margin: const EdgeInsets.only(right: 6),
                            decoration: BoxDecoration(
                              color: AppColors.primary.withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: const Icon(
                              Icons.star,
                              size: 10,
                              color: AppColors.primary,
                            ),
                          ),
                        Text(
                          '${day.waitDays}',
                          style: AppTypography.mono.copyWith(
                            color: isOptimal ? AppColors.primary : null,
                            fontWeight: isOptimal ? FontWeight.w600 : null,
                          ),
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    flex: 3,
                    child: Text(
                      Formatters.formatPercentage(day.avgReturn),
                      style: AppTypography.mono.copyWith(
                        color: day.avgReturn >= 0 ? AppColors.success : AppColors.danger,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                  Expanded(
                    flex: 2,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: riskColor.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        day.riskZone.toUpperCase(),
                        style: AppTypography.monoSmall.copyWith(
                          color: riskColor,
                          fontSize: 10,
                        ),
                      ),
                    ),
                  ),
                  Expanded(
                    flex: 3,
                    child: Text(
                      Formatters.formatPercentage(day.worstCase),
                      style: AppTypography.mono.copyWith(
                        color: AppColors.danger,
                      ),
                    ),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }
}
