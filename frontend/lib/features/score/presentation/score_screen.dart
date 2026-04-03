import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/models/score_result.dart';

class ScoreScreen extends ConsumerStatefulWidget {
  const ScoreScreen({super.key});

  @override
  ConsumerState<ScoreScreen> createState() => _ScoreScreenState();
}

class _ScoreScreenState extends ConsumerState<ScoreScreen> {
  final _addressController = TextEditingController();
  bool _isLoading = false;
  ScoreResult? _result;
  String? _error;

  @override
  void dispose() {
    _addressController.dispose();
    super.dispose();
  }

  Color _scoreColor(int score) {
    if (score >= 600) return AppColors.success;
    if (score >= 400) return AppColors.accent;
    if (score >= 200) return AppColors.warning;
    return AppColors.danger;
  }

  Future<void> _handleAnalyze() async {
    final addr = _addressController.text.trim();
    if (addr.isEmpty) {
      setState(() => _error = 'Please enter a Bitcoin address');
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
      _result = const ScoreResult(
        totalScore: 542,
        rank: 'Good',
        address: 'bc1q...placeholder',
        breakdown: ScoreBreakdown(
          consistency: ScoreComponent(score: 145, max: 200),
          relativeVolume: ScoreComponent(score: 98, max: 150),
          diversification: ScoreComponent(score: 67, max: 100),
          savingsPattern: ScoreComponent(score: 102, max: 150),
          paymentHistory: ScoreComponent(score: 88, max: 150),
          lightningActivity: ScoreComponent(score: 42, max: 100),
        ),
        recommendations: [
          'Increase Lightning Network usage to improve score',
          'Maintain consistent transaction patterns',
          'Diversify transaction types for better scoring',
        ],
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildAddressInput(),
          const SizedBox(height: 24),
          if (_error != null) _buildError(),
          if (_isLoading) _buildLoading(),
          if (_result == null && !_isLoading && _error == null) _buildInitial(),
          if (_result != null && !_isLoading) _buildResult(),
        ],
      ),
    );
  }

  Widget _buildAddressInput() {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Row(
        children: [
          const SizedBox(width: 12),
          Icon(Icons.currency_bitcoin, size: 18, color: AppColors.accent),
          Expanded(
            child: TextField(
              controller: _addressController,
              style: AppTypography.mono,
              decoration: const InputDecoration(
                hintText: 'bc1q...',
                border: InputBorder.none,
                enabledBorder: InputBorder.none,
                focusedBorder: InputBorder.none,
                contentPadding: EdgeInsets.all(12),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(right: 4),
            child: SizedBox(
              height: 36,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _handleAnalyze,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.accent,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
                child: const Text(
                  'Analyze',
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInitial() {
    return Padding(
      padding: const EdgeInsets.only(top: 64),
      child: Center(
        child: Text(
          'Enter a Bitcoin address to analyze',
          style: AppTypography.bodyMedium,
        ),
      ),
    );
  }

  Widget _buildLoading() {
    return Padding(
      padding: const EdgeInsets.only(top: 32),
      child: Column(
        children: List.generate(3, (i) {
          return Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: _ShimmerBlock(
              width: double.infinity,
              height: i == 0 ? 120 : 48,
            ),
          );
        }),
      ),
    );
  }

  Widget _buildError() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        children: [
          Text(
            _error!,
            style: AppTypography.bodyMedium.copyWith(color: AppColors.danger),
          ),
          const SizedBox(height: 12),
          OutlinedButton(
            onPressed: _handleAnalyze,
            style: OutlinedButton.styleFrom(
              side: const BorderSide(color: AppColors.borderStrong),
            ),
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  }

  Widget _buildResult() {
    final result = _result!;
    final color = _scoreColor(result.totalScore);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildScoreGauge(result.totalScore, color, result.rank),
        const SizedBox(height: 24),
        Text('Breakdown', style: AppTypography.titleSmall),
        const SizedBox(height: 12),
        _buildBreakdownItem('Consistency', result.breakdown.consistency),
        _buildBreakdownItem('Volume', result.breakdown.relativeVolume),
        _buildBreakdownItem('Diversification', result.breakdown.diversification),
        _buildBreakdownItem('Savings', result.breakdown.savingsPattern),
        _buildBreakdownItem('Payment History', result.breakdown.paymentHistory),
        _buildBreakdownItem('Lightning', result.breakdown.lightningActivity),
        const SizedBox(height: 24),
        Text('Recommendations', style: AppTypography.titleSmall),
        const SizedBox(height: 12),
        ...result.recommendations.map((r) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Padding(
                    padding: EdgeInsets.only(top: 2),
                    child: Icon(
                      Icons.info_outline,
                      size: 16,
                      color: AppColors.accent,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(r, style: AppTypography.bodyMedium),
                  ),
                ],
              ),
            )),
      ],
    );
  }

  Widget _buildScoreGauge(int score, Color color, String rank) {
    return Center(
      child: Column(
        children: [
          SizedBox(
            width: 200,
            height: 120,
            child: CustomPaint(
              painter: _ScoreArcPainter(
                score: score,
                maxScore: 750,
                color: color,
              ),
              child: Padding(
                padding: const EdgeInsets.only(top: 40),
                child: Column(
                  children: [
                    Text(
                      score.toString(),
                      style: AppTypography.displayLarge.copyWith(
                        color: color,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          Text(
            rank,
            style: AppTypography.titleMedium.copyWith(
              color: score >= 400 ? AppColors.accent : AppColors.textSecondary,
            ),
          ),
          const SizedBox(height: 4),
          Text('of 750 possible', style: AppTypography.bodySmall),
        ],
      ),
    );
  }

  Widget _buildBreakdownItem(String label, ScoreComponent component) {
    final progress = component.max > 0 ? component.score / component.max : 0.0;

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(label, style: AppTypography.bodyMedium),
              Text(
                '${component.score}/${component.max}',
                style: AppTypography.mono,
              ),
            ],
          ),
          const SizedBox(height: 6),
          ClipRRect(
            borderRadius: BorderRadius.circular(2),
            child: LinearProgressIndicator(
              value: progress,
              minHeight: 4,
              backgroundColor: AppColors.borderSubtle,
              valueColor: AlwaysStoppedAnimation<Color>(
                _scoreColor((component.score / component.max * 750).round()),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _ScoreArcPainter extends CustomPainter {
  final int score;
  final int maxScore;
  final Color color;

  _ScoreArcPainter({
    required this.score,
    required this.maxScore,
    required this.color,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height);
    final radius = size.width / 2 - 12;
    const strokeWidth = 8.0;

    final bgPaint = Paint()
      ..color = AppColors.borderSubtle
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      math.pi,
      math.pi,
      false,
      bgPaint,
    );

    final progressPaint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;

    final sweepAngle = (score / maxScore).clamp(0.0, 1.0) * math.pi;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      math.pi,
      sweepAngle,
      false,
      progressPaint,
    );
  }

  @override
  bool shouldRepaint(covariant _ScoreArcPainter oldDelegate) {
    return oldDelegate.score != score || oldDelegate.color != color;
  }
}

class _ShimmerBlock extends StatefulWidget {
  final double width;
  final double height;

  const _ShimmerBlock({required this.width, required this.height});

  @override
  State<_ShimmerBlock> createState() => _ShimmerBlockState();
}

class _ShimmerBlockState extends State<_ShimmerBlock>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Container(
          width: widget.width,
          height: widget.height,
          decoration: BoxDecoration(
            color: AppColors.surface
                .withValues(alpha: 0.5 + _controller.value * 0.5),
            borderRadius: BorderRadius.circular(4),
          ),
        );
      },
    );
  }
}
