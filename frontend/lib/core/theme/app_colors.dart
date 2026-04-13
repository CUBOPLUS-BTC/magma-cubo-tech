import 'package:flutter/material.dart';

abstract class AppColors {
  static const background = Color(0xFF111318);
  static const surface = Color(0xFF191C24);
  static const surfaceElevated = Color(0xFF232836);

  static const primary = Color(0xFFC8702E);
  static const accent = Color(0xFFC8702E);
  static const accentVariant = Color(0xFFD88540);
  static const accentMuted = Color(0x33C8702E);

  static const textPrimary = Colors.white;
  static Color get textSecondary => Colors.white.withValues(alpha: 0.6);
  static Color get textTertiary => Colors.white.withValues(alpha: 0.4);

  static const error = Color(0xFFEF4444);
  static const success = Color(0xFF428A62);
  static const warning = Color(0xFFF59E0B);
  static const info = Color(0xFF3B82F6);
  static const danger = Color(0xFFEF4444);

  static const borderSubtle = Color(0x1AFFFFFF);
  static const borderStrong = Color(0x33FFFFFF);
  static const surfaceHighlight = Color(0x0DFFFFFF);
}
