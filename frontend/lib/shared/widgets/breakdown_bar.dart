import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../core/theme/app_colors.dart';

class BreakdownBar extends StatelessWidget {
  final String label;
  final int score;
  final int maxScore;

  const BreakdownBar({
    super.key,
    required this.label,
    required this.score,
    required this.maxScore,
  });

  @override
  Widget build(BuildContext context) {
    final ratio = maxScore > 0 ? (score / maxScore).clamp(0.0, 1.0) : 0.0;

    Color fillColor;
    if (ratio > 0.8) {
      fillColor = AppColors.success;
    } else if (ratio > 0.5) {
      fillColor = AppColors.accent;
    } else {
      fillColor = AppColors.warning;
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: GoogleFonts.dmSans(
                fontSize: 13,
                color: AppColors.textSecondary,
              ),
            ),
            Text(
              '$score/$maxScore',
              style: GoogleFonts.jetBrainsMono(
                fontSize: 13,
                color: AppColors.textPrimary,
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        SizedBox(
          height: 4,
          child: TweenAnimationBuilder<double>(
            tween: Tween(begin: 0, end: ratio),
            duration: const Duration(milliseconds: 800),
            curve: Curves.easeOutCubic,
            builder: (context, value, _) {
              return CustomPaint(
                painter: _BarPainter(progress: value, color: fillColor),
                size: const Size(double.infinity, 4),
              );
            },
          ),
        ),
      ],
    );
  }
}

class _BarPainter extends CustomPainter {
  final double progress;
  final Color color;

  _BarPainter({required this.progress, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final trackRRect = RRect.fromRectAndRadius(
      Rect.fromLTWH(0, 0, size.width, size.height),
      const Radius.circular(2),
    );
    canvas.drawRRect(
      trackRRect,
      Paint()..color = AppColors.borderSubtle,
    );

    if (progress > 0) {
      final fillRRect = RRect.fromRectAndRadius(
        Rect.fromLTWH(0, 0, size.width * progress, size.height),
        const Radius.circular(2),
      );
      canvas.drawRRect(
        fillRRect,
        Paint()..color = color,
      );
    }
  }

  @override
  bool shouldRepaint(_BarPainter old) =>
      old.progress != progress || old.color != color;
}
