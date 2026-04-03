import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

class AppTheme {
  static ThemeData get dark {
    return ThemeData(
      brightness: Brightness.dark,
      useMaterial3: true,
      scaffoldBackgroundColor: AppColors.background,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.accent,
        onPrimary: Colors.black,
        secondary: AppColors.surfaceElevated,
        surface: AppColors.surface,
        onSurface: AppColors.textPrimary,
        error: AppColors.danger,
        onError: Colors.white,
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.background,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: false,
        systemOverlayStyle: SystemUiOverlayStyle.light,
        titleTextStyle: GoogleFonts.outfit(
          fontSize: 16,
          fontWeight: FontWeight.w500,
          color: AppColors.textPrimary,
        ),
        iconTheme: const IconThemeData(color: AppColors.textPrimary, size: 20),
      ),
      cardTheme: CardThemeData(
        color: AppColors.surface,
        elevation: 0,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(4),
          side: const BorderSide(color: AppColors.borderSubtle, width: 1),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.surface,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(4),
          borderSide: const BorderSide(color: AppColors.borderSubtle, width: 1),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(4),
          borderSide: const BorderSide(color: AppColors.borderSubtle, width: 1),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(4),
          borderSide: const BorderSide(color: AppColors.accent, width: 1),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(4),
          borderSide: const BorderSide(color: AppColors.danger, width: 1),
        ),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 12,
          vertical: 12,
        ),
        hintStyle: GoogleFonts.dmSans(
          color: AppColors.textTertiary,
          fontSize: 13,
          fontWeight: FontWeight.w400,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.accent,
          foregroundColor: Colors.black,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
          textStyle: GoogleFonts.dmSans(
            fontSize: 14,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: AppColors.textPrimary,
          side: const BorderSide(color: AppColors.borderStrong, width: 1),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
          textStyle: GoogleFonts.dmSans(
            fontSize: 14,
            fontWeight: FontWeight.w500,
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: AppColors.accent,
          textStyle: GoogleFonts.dmSans(
            fontSize: 14,
            fontWeight: FontWeight.w500,
          ),
        ),
      ),
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        backgroundColor: AppColors.surface,
        selectedItemColor: AppColors.accent,
        unselectedItemColor: AppColors.textTertiary,
        type: BottomNavigationBarType.fixed,
        elevation: 0,
        showSelectedLabels: true,
        showUnselectedLabels: true,
      ),
      navigationRailTheme: const NavigationRailThemeData(
        backgroundColor: AppColors.surface,
        selectedIconTheme: IconThemeData(color: AppColors.accent, size: 22),
        unselectedIconTheme: IconThemeData(
          color: AppColors.textTertiary,
          size: 22,
        ),
        selectedLabelTextStyle: TextStyle(
          color: AppColors.accent,
          fontSize: 12,
          fontWeight: FontWeight.w500,
        ),
        unselectedLabelTextStyle: TextStyle(
          color: AppColors.textTertiary,
          fontSize: 12,
        ),
        indicatorColor: Colors.transparent,
      ),
      dividerTheme: const DividerThemeData(
        color: AppColors.borderSubtle,
        thickness: 1,
        space: 1,
      ),
      dialogTheme: DialogThemeData(
        backgroundColor: AppColors.surfaceElevated,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(4),
          side: const BorderSide(color: AppColors.borderSubtle, width: 1),
        ),
      ),
      snackBarTheme: SnackBarThemeData(
        backgroundColor: AppColors.surfaceElevated,
        contentTextStyle: GoogleFonts.dmSans(
          color: AppColors.textPrimary,
          fontSize: 13,
        ),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
        behavior: SnackBarBehavior.floating,
      ),
      progressIndicatorTheme: const ProgressIndicatorThemeData(
        color: AppColors.accent,
        linearTrackColor: AppColors.borderSubtle,
      ),
    );
  }
}
