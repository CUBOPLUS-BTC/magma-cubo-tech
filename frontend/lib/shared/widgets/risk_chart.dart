import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_typography.dart';
import '../../core/models/simulation.dart';

class RiskChart extends StatelessWidget {
  final List<DayAnalysis> data;

  const RiskChart({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    if (data.isEmpty) return const SizedBox.shrink();

    return Column(
      children: [
        SizedBox(
          height: 220,
          child: LineChart(_buildChart()),
        ),
        const SizedBox(height: 12),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _legend(AppColors.accent, 'Avg Return'),
            const SizedBox(width: 16),
            _legend(AppColors.success, 'Best Case'),
            const SizedBox(width: 16),
            _legend(AppColors.danger, 'Worst Case'),
          ],
        ),
      ],
    );
  }

  Widget _legend(Color color, String label) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 6,
          height: 6,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(width: 4),
        Text(label, style: AppTypography.labelMedium),
      ],
    );
  }

  LineChartData _buildChart() {
    final avgSpots = <FlSpot>[];
    final bestSpots = <FlSpot>[];
    final worstSpots = <FlSpot>[];

    for (final d in data) {
      final x = d.waitDays.toDouble();
      avgSpots.add(FlSpot(x, d.avgReturn));
      bestSpots.add(FlSpot(x, d.bestCase));
      worstSpots.add(FlSpot(x, d.worstCase));
    }

    return LineChartData(
      gridData: const FlGridData(show: false),
      borderData: FlBorderData(show: false),
      titlesData: FlTitlesData(
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles:
            const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            interval: 1,
            getTitlesWidget: (value, _) {
              return Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  '${value.toInt()}',
                  style: GoogleFonts.jetBrainsMono(
                    fontSize: 10,
                    color: AppColors.textTertiary,
                  ),
                ),
              );
            },
          ),
        ),
        leftTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 40,
            getTitlesWidget: (value, _) {
              return Text(
                '${value.toStringAsFixed(1)}%',
                style: GoogleFonts.jetBrainsMono(
                  fontSize: 10,
                  color: AppColors.textTertiary,
                ),
              );
            },
          ),
        ),
      ),
      lineTouchData: LineTouchData(
        touchTooltipData: LineTouchTooltipData(
          getTooltipColor: (_) => AppColors.surface,
          tooltipBorder: const BorderSide(color: AppColors.borderSubtle),
          tooltipRoundedRadius: 4,
          getTooltipItems: (spots) {
            return spots.map((spot) {
              final Color color;
              final String prefix;
              switch (spot.barIndex) {
                case 0:
                  color = AppColors.accent;
                  prefix = 'Avg';
                case 1:
                  color = AppColors.success;
                  prefix = 'Best';
                case 2:
                  color = AppColors.danger;
                  prefix = 'Worst';
                default:
                  color = AppColors.textPrimary;
                  prefix = '';
              }
              return LineTooltipItem(
                '$prefix: ${spot.y.toStringAsFixed(2)}%',
                GoogleFonts.jetBrainsMono(
                  fontSize: 11,
                  color: color,
                ),
              );
            }).toList();
          },
        ),
      ),
      lineBarsData: [
        LineChartBarData(
          spots: avgSpots,
          isCurved: true,
          color: AppColors.accent,
          barWidth: 2,
          dotData: const FlDotData(show: false),
          belowBarData: BarAreaData(show: false),
        ),
        LineChartBarData(
          spots: bestSpots,
          isCurved: true,
          color: AppColors.success,
          barWidth: 1,
          dotData: const FlDotData(show: false),
          belowBarData: BarAreaData(show: false),
          dashArray: [4, 4],
        ),
        LineChartBarData(
          spots: worstSpots,
          isCurved: true,
          color: AppColors.danger,
          barWidth: 1,
          dotData: const FlDotData(show: false),
          belowBarData: BarAreaData(show: false),
          dashArray: [4, 4],
        ),
      ],
    );
  }
}
