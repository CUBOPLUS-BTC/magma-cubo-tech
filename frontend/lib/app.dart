import 'package:flutter/material.dart';
import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';

class SatsScoreApp extends StatelessWidget {
  const SatsScoreApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'SatsScore',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.dark,
      routerConfig: appRouter,
    );
  }
}
