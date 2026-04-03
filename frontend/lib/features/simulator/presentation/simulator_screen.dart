import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/utils/formatters.dart';
import '../../../core/models/simulation.dart';

class SimulatorScreen extends ConsumerStatefulWidget {
  const SimulatorScreen({super.key});

  @override
  ConsumerState<SimulatorScreen> createState() => _SimulatorScreenState();
}

class _SimulatorScreenState extends ConsumerState<SimulatorScreen> {
  final _amountController = TextEditingController();
  int _period = 90;
  bool _isLoading = false;
  SimulationResult? _result;
  String? _error;

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

  Future<void> _handleSimulate() async {
    final amountText = _amountController.text.trim();
    if (amountText.isEmpty) {
      setState(() => _error = 'Please enter an amount');
      return;
    }

    final amount = double.tryParse(amountText);
    if (amount == null || amount <= 0) {
      setState(() => _error = 'Enter a valid amount');
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
      _result = null;
    });

    await Future.delayed(const Duration(seconds: 2));

    if (!mounted) return;

    setState(() {
      _isLoading = false;
      _result = SimulationResult(
        dailyAnalysis: [
          const DayAnalysis(waitDays: 7, avgReturn: 1.2, stdDev: 3.1, worstCase: -5.8, bestCase: 8.2, riskZone: 'low'),
          const DayAnalysis(waitDays: 14, avgReturn: 2.1, stdDev: 4.5, worstCase: -7.2, bestCase: 11.4, riskZone: 'low'),
          const DayAnalysis(waitDays: 30, avgReturn: 3.8, stdDev: 6.2, worstCase: -9.1, bestCase: 16.7, riskZone: 'medium'),
          const DayAnalysis(waitDays: 60, avgReturn: 5.4, stdDev: 8.8, worstCase: -12.5, bestCase: 23.3, riskZone: 'medium'),
          const DayAnalysis(waitDays: 90, avgReturn: 7.2, stdDev: 11.3, worstCase: -15.8, bestCase: 30.2, riskZone: 'high'),
        ],
        recommendation: 'Based on historical volatility, waiting 30 days offers the best risk-adjusted return for this amount.',
        riskLevel: 'medium',
        optimalDay: 30,
        expectedReturn: 3.8,
      );
    });
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
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildInputSection(),
          const SizedBox(height: 16),
          _buildSimulateButton(),
          const SizedBox(height: 24),
          if (_error != null) _buildError(),
          if (_isLoading) _buildLoading(),
          if (_result == null && !_isLoading && _error == null) _buildInitial(),
          if (_result != null && !_isLoading) _buildResult(),
        ],
      ),
    );
  }

  Widget _buildInputSection() {
    return Row(
      children: [
        Expanded(
          child: TextField(
            controller: _amountController,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            style: AppTypography.mono,
            decoration: const InputDecoration(
              hintText: 'Amount',
              prefixText: '\$ ',
            ),
          ),
        ),
        const SizedBox(width: 12),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(4),
            border: Border.all(color: AppColors.borderSubtle),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<int>(
              value: _period,
              dropdownColor: AppColors.surfaceElevated,
              style: AppTypography.mono,
              items: _periodOptions.entries
                  .map((e) => DropdownMenuItem(
                        value: e.value,
                        child: Text(e.key, style: AppTypography.bodyMedium.copyWith(color: AppColors.textPrimary)),
                      ))
                  .toList(),
              onChanged: (v) {
                if (v != null) setState(() => _period = v);
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSimulateButton() {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: ElevatedButton(
        onPressed: _isLoading ? null : _handleSimulate,
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
                'Simulate',
                style: TextStyle(fontWeight: FontWeight.w600),
              ),
      ),
    );
  }

  Widget _buildInitial() {
    return Padding(
      padding: const EdgeInsets.only(top: 48),
      child: Center(
        child: Text(
          'Enter an amount and period to simulate BTC price volatility and find the optimal time to transact.',
          style: AppTypography.bodyMedium,
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  Widget _buildLoading() {
    return const Padding(
      padding: EdgeInsets.only(top: 64),
      child: Center(
        child: CircularProgressIndicator(color: AppColors.accent),
      ),
    );
  }

  Widget _buildError() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Text(
        _error!,
        style: AppTypography.bodyMedium.copyWith(color: AppColors.danger),
      ),
    );
  }

  Widget _buildResult() {
    final result = _result!;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildRecommendationCard(result),
        const SizedBox(height: 16),
        _buildChart(result),
        const SizedBox(height: 16),
        _buildDataTable(result),
      ],
    );
  }

  Widget _buildRecommendationCard(SimulationResult result) {
    final riskColor = _riskColor(result.riskLevel);

    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: Border(
          left: BorderSide(color: AppColors.accent, width: 3),
          top: BorderSide(color: AppColors.borderSubtle),
          right: BorderSide(color: AppColors.borderSubtle),
          bottom: BorderSide(color: AppColors.borderSubtle),
        ),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(
                'RECOMMENDATION',
                style: AppTypography.labelMedium.copyWith(color: AppColors.accent),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: riskColor.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  result.riskLevel.toUpperCase(),
                  style: AppTypography.labelSmall.copyWith(color: riskColor),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(result.recommendation, style: AppTypography.bodyLarge),
        ],
      ),
    );
  }

  Widget _buildChart(SimulationResult result) {
    final data = result.dailyAnalysis;
    if (data.isEmpty) return const SizedBox.shrink();

    return Container(
      height: 220,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: LineChart(
        LineChartData(
          gridData: FlGridData(
            show: true,
            drawVerticalLine: false,
            horizontalInterval: 10,
            getDrawingHorizontalLine: (value) => FlLine(
              color: AppColors.borderSubtle,
              strokeWidth: 1,
            ),
          ),
          titlesData: FlTitlesData(
            topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
            rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                reservedSize: 28,
                getTitlesWidget: (value, meta) {
                  return Text(
                    '${value.toInt()}d',
                    style: AppTypography.labelSmall,
                  );
                },
              ),
            ),
            leftTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                reservedSize: 40,
                getTitlesWidget: (value, meta) {
                  return Text(
                    '${value.toInt()}%',
                    style: AppTypography.labelSmall,
                  );
                },
              ),
            ),
          ),
          borderData: FlBorderData(show: false),
          lineTouchData: LineTouchData(
            touchTooltipData: LineTouchTooltipData(
              getTooltipColor: (_) => AppColors.surfaceElevated,
              tooltipBorder: const BorderSide(color: AppColors.borderSubtle),
              tooltipRoundedRadius: 4,
              getTooltipItems: (spots) => spots.map((spot) {
                final colors = [AppColors.accent, AppColors.success, AppColors.danger];
                final labels = ['Avg', 'Best', 'Worst'];
                return LineTooltipItem(
                  '${labels[spot.barIndex]}: ${spot.y.toStringAsFixed(1)}%',
                  AppTypography.monoSmall.copyWith(color: colors[spot.barIndex]),
                );
              }).toList(),
            ),
          ),
          lineBarsData: [
            LineChartBarData(
              spots: data.map((d) => FlSpot(d.waitDays.toDouble(), d.avgReturn)).toList(),
              isCurved: true,
              color: AppColors.accent,
              barWidth: 2,
              dotData: const FlDotData(show: false),
            ),
            LineChartBarData(
              spots: data.map((d) => FlSpot(d.waitDays.toDouble(), d.bestCase)).toList(),
              isCurved: true,
              color: AppColors.success,
              barWidth: 1,
              dashArray: [6, 4],
              dotData: const FlDotData(show: false),
            ),
            LineChartBarData(
              spots: data.map((d) => FlSpot(d.waitDays.toDouble(), d.worstCase)).toList(),
              isCurved: true,
              color: AppColors.danger,
              barWidth: 1,
              dashArray: [6, 4],
              dotData: const FlDotData(show: false),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDataTable(SimulationResult result) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: Row(
              children: [
                Expanded(flex: 2, child: Text('Day', style: AppTypography.labelMedium)),
                Expanded(flex: 3, child: Text('Avg Return', style: AppTypography.labelMedium)),
                Expanded(flex: 2, child: Text('Risk', style: AppTypography.labelMedium)),
                Expanded(flex: 3, child: Text('Worst Case', style: AppTypography.labelMedium)),
              ],
            ),
          ),
          const Divider(height: 1, color: AppColors.borderSubtle),
          ...result.dailyAnalysis.map((day) {
            final isOptimal = day.waitDays == result.optimalDay;
            final riskColor = _riskColor(day.riskZone);

            return Container(
              color: isOptimal ? AppColors.accent.withValues(alpha: 0.1) : null,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              child: Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: Text(
                      '${day.waitDays}',
                      style: AppTypography.mono.copyWith(
                        color: isOptimal ? AppColors.accent : null,
                      ),
                    ),
                  ),
                  Expanded(
                    flex: 3,
                    child: Text(
                      Formatters.formatPercentage(day.avgReturn),
                      style: AppTypography.mono.copyWith(
                        color: day.avgReturn >= 0 ? AppColors.success : AppColors.danger,
                      ),
                    ),
                  ),
                  Expanded(
                    flex: 2,
                    child: Text(
                      day.riskZone,
                      style: AppTypography.monoSmall.copyWith(color: riskColor),
                    ),
                  ),
                  Expanded(
                    flex: 3,
                    child: Text(
                      Formatters.formatPercentage(day.worstCase),
                      style: AppTypography.mono.copyWith(color: AppColors.danger),
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
