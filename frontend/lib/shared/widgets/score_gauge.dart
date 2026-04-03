import 'dart:math';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_typography.dart';

class ScoreGauge extends StatelessWidget {
  final int score;
  final int maxScore;
  final double size;

  const ScoreGauge({
    super.key,
    required this.score,
    this.maxScore = 750,
    this.size = 200,
  });

  Color _scoreColor(int s) {
    if (s >= 600) return AppColors.success;
    if (s >= 400) return AppColors.accent;
    if (s >= 200) return AppColors.warning;
    return AppColors.danger;
  }

  String _rank(int s) {
    if (s >= 750) return 'Excellent';
    if (s >= 600) return 'Good';
    if (s >= 400) return 'Fair';
    if (s >= 200) return 'Developing';
    return 'New';
  }

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0, end: score.toDouble()),
      duration: const Duration(milliseconds: 1200),
      curve: Curves.easeOutCubic,
      builder: (context, animatedScore, _) {
        final currentScore = animatedScore.round();
        return SizedBox(
          width: size,
          height: size * 0.65,
          child: CustomPaint(
            painter: _GaugePainter(
              progress: animatedScore / maxScore,
              color: _scoreColor(currentScore),
            ),
            child: Center(
              child: Padding(
                padding: EdgeInsets.only(top: size * 0.12),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      '$currentScore',
                      style: GoogleFonts.outfit(
                        fontSize: size * 0.2,
                        fontWeight: FontWeight.w700,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      _rank(currentScore),
                      style: AppTypography.bodyMedium,
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}

class _GaugePainter extends CustomPainter {
  final double progress;
  final Color color;

  _GaugePainter({required this.progress, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height * 0.85);
    final radius = min(size.width / 2, size.height * 0.85) - 8;
    const startAngle = pi;
    const sweepAngle = pi;
    const strokeWidth = 8.0;

    final trackPaint = Paint()
      ..color = AppColors.borderSubtle
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      startAngle,
      sweepAngle,
      false,
      trackPaint,
    );

    if (progress > 0) {
      final fillPaint = Paint()
        ..color = color
        ..style = PaintingStyle.stroke
        ..strokeWidth = strokeWidth
        ..strokeCap = StrokeCap.round;

      canvas.drawArc(
        Rect.fromCircle(center: center, radius: radius),
        startAngle,
        sweepAngle * progress.clamp(0.0, 1.0),
        false,
        fillPaint,
      );
    }
  }

  @override
  bool shouldRepaint(_GaugePainter old) =>
      old.progress != progress || old.color != color;
}
