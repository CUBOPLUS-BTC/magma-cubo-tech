import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';

class LoadingShimmer extends StatefulWidget {
  final double width;
  final double height;

  const LoadingShimmer({super.key, required this.width, required this.height});

  factory LoadingShimmer.card({Key? key, double height = 120}) =>
      LoadingShimmer(key: key, width: double.infinity, height: height);

  factory LoadingShimmer.text({Key? key, double width = 200}) =>
      LoadingShimmer(key: key, width: width, height: 14);

  factory LoadingShimmer.gauge({Key? key, double size = 200}) =>
      LoadingShimmer(key: key, width: size, height: size * 0.65);

  @override
  State<LoadingShimmer> createState() => _LoadingShimmerState();
}

class _LoadingShimmerState extends State<LoadingShimmer>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat();
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
        return ShaderMask(
          shaderCallback: (bounds) {
            return LinearGradient(
              begin: Alignment.centerLeft,
              end: Alignment.centerRight,
              colors: const [
                AppColors.surface,
                AppColors.surfaceElevated,
                AppColors.surface,
              ],
              stops: [
                (_controller.value - 0.3).clamp(0.0, 1.0),
                _controller.value,
                (_controller.value + 0.3).clamp(0.0, 1.0),
              ],
            ).createShader(bounds);
          },
          blendMode: BlendMode.srcATop,
          child: child,
        );
      },
      child: Container(
        width: widget.width,
        height: widget.height,
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );
  }
}
