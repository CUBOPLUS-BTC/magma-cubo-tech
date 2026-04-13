import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/home/presentation/home_screen.dart';
import '../../features/score/presentation/score_screen.dart';
import '../../features/simulator/presentation/simulator_screen.dart';
import '../../features/remittance/presentation/remittance_screen.dart';
import '../services/nostr_auth_service.dart';
import '../theme/app_colors.dart';
import '../theme/app_typography.dart';
import '../utils/breakpoints.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _shellNavigatorKey = GlobalKey<NavigatorState>();

const _navItems = [
  ('/home', Icons.grid_view_rounded, Icons.grid_view_rounded, 'Home'),
  ('/score', Icons.analytics_outlined, Icons.analytics_rounded, 'Score'),
  (
    '/simulator',
    Icons.candlestick_chart_outlined,
    Icons.candlestick_chart_rounded,
    'Simulate',
  ),
  ('/remittance', Icons.route_outlined, Icons.route_rounded, 'Remit'),
];

final appRouter = GoRouter(
  navigatorKey: _rootNavigatorKey,
  initialLocation: '/login',
  routes: [
    GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
    ShellRoute(
      navigatorKey: _shellNavigatorKey,
      builder: (context, state, child) => ShellScaffold(child: child),
      routes: [
        GoRoute(
          path: '/home',
          pageBuilder: (context, state) =>
              const NoTransitionPage(child: HomeScreen()),
        ),
        GoRoute(
          path: '/score',
          pageBuilder: (context, state) =>
              const NoTransitionPage(child: ScoreScreen()),
        ),
        GoRoute(
          path: '/simulator',
          pageBuilder: (context, state) =>
              const NoTransitionPage(child: SimulatorScreen()),
        ),
        GoRoute(
          path: '/remittance',
          pageBuilder: (context, state) =>
              const NoTransitionPage(child: RemittanceScreen()),
        ),
      ],
    ),
  ],
);

class ShellScaffold extends StatelessWidget {
  final Widget child;

  const ShellScaffold({super.key, required this.child});

  int _getCurrentIndex(BuildContext context) {
    final location = GoRouterState.of(context).uri.path;
    final idx = _navItems.indexWhere((t) => location.startsWith(t.$1));
    return idx >= 0 ? idx : 0;
  }

  @override
  Widget build(BuildContext context) {
    final isDesktop = Breakpoints.isDesktop(context);

    if (isDesktop) {
      return _DesktopShell(
        currentIndex: _getCurrentIndex(context),
        child: child,
      );
    }

    return _MobileShell(currentIndex: _getCurrentIndex(context), child: child);
  }
}

class _DesktopShell extends StatelessWidget {
  final int currentIndex;
  final Widget child;

  const _DesktopShell({required this.currentIndex, required this.child});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Row(
        children: [
          _Sidebar(currentIndex: currentIndex),
          VerticalDivider(width: 1, color: AppColors.borderSubtle),
          Expanded(child: child),
        ],
      ),
    );
  }
}

class _MobileShell extends StatelessWidget {
  final int currentIndex;
  final Widget child;

  const _MobileShell({required this.currentIndex, required this.child});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(child: child),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: AppColors.surface,
          border: Border(
            top: BorderSide(color: AppColors.borderSubtle, width: 1),
          ),
        ),
        child: SafeArea(
          top: false,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: List.generate(_navItems.length, (i) {
                final isSelected = i == currentIndex;
                final item = _navItems[i];
                return _BottomNavItem(
                  icon: isSelected ? item.$3 : item.$2,
                  label: item.$4,
                  isSelected: isSelected,
                  onTap: () => context.go(item.$1),
                );
              }),
            ),
          ),
        ),
      ),
    );
  }
}

class _BottomNavItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  const _BottomNavItem({
    required this.icon,
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeOutCubic,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected ? AppColors.accentMuted : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              size: 20,
              color: isSelected ? AppColors.accent : AppColors.textTertiary,
            ),
            if (isSelected) ...[
              const SizedBox(width: 8),
              Text(
                label,
                style: AppTypography.labelLarge.copyWith(
                  color: AppColors.accent,
                  fontWeight: FontWeight.w600,
                  fontSize: 13,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

Future<void> _handleLogout(BuildContext context) async {
  final confirmed = await showDialog<bool>(
    context: context,
    builder: (context) => AlertDialog(
      backgroundColor: AppColors.surfaceElevated,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      title: Text(
        'Logout',
        style: AppTypography.titleLarge.copyWith(fontSize: 18),
      ),
      content: Text(
        'Are you sure you want to logout?',
        style: AppTypography.bodyMedium,
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(false),
          child: Text(
            'Cancel',
            style: TextStyle(color: AppColors.textSecondary),
          ),
        ),
        ElevatedButton(
          onPressed: () => Navigator.of(context).pop(true),
          child: const Text('Logout'),
        ),
      ],
    ),
  );

  if (confirmed == true && context.mounted) {
    await NostrAuthService().logout();
    if (context.mounted) {
      context.go('/login');
    }
  }
}

class _Sidebar extends ConsumerWidget {
  final int currentIndex;

  const _Sidebar({required this.currentIndex});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      width: 240,
      color: AppColors.surface,
      child: Column(
        children: [
          const SizedBox(height: 24),
          _SidebarHeader(),
          const SizedBox(height: 32),
          ...List.generate(_navItems.length, (i) {
            return _SidebarItem(
              icon: _navItems[i].$2,
              activeIcon: _navItems[i].$3,
              label: _navItems[i].$4,
              isSelected: i == currentIndex,
              onTap: () => context.go(_navItems[i].$1),
            );
          }),
          const Spacer(),
          _SidebarItem(
            icon: Icons.help_outline_rounded,
            activeIcon: Icons.help_rounded,
            label: 'About',
            isSelected: false,
            onTap: () => _showAboutDialog(context),
          ),
          const SizedBox(height: 4),
          const Divider(color: AppColors.borderSubtle),
          _SidebarItem(
            icon: Icons.logout_outlined,
            activeIcon: Icons.logout,
            label: 'Logout',
            isSelected: false,
            onTap: () => _handleLogout(context),
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}

class _SidebarHeader extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 16),
      child: Image.asset(
        'assets/images/salvium.png',
        height: 80,
        fit: BoxFit.contain,
      ),
    );
  }
}

class _SidebarItem extends StatefulWidget {
  final IconData icon;
  final IconData activeIcon;
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  const _SidebarItem({
    required this.icon,
    required this.activeIcon,
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  State<_SidebarItem> createState() => _SidebarItemState();
}

class _SidebarItemState extends State<_SidebarItem> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 2),
      child: MouseRegion(
        onEnter: (_) => setState(() => _isHovered = true),
        onExit: (_) => setState(() => _isHovered = false),
        child: GestureDetector(
          onTap: widget.onTap,
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 150),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
            decoration: BoxDecoration(
              color: widget.isSelected
                  ? AppColors.accentMuted
                  : _isHovered
                  ? AppColors.surfaceElevated
                  : Colors.transparent,
              borderRadius: BorderRadius.circular(10),
            ),
            child: Row(
              children: [
                Icon(
                  widget.isSelected ? widget.activeIcon : widget.icon,
                  size: 18,
                  color: widget.isSelected
                      ? AppColors.accent
                      : AppColors.textSecondary,
                ),
                const SizedBox(width: 12),
                Text(
                  widget.label,
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: widget.isSelected
                        ? FontWeight.w600
                        : FontWeight.w400,
                    color: widget.isSelected
                        ? AppColors.accent
                        : AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

Future<void> _showAboutDialog(BuildContext context) async {
  await showDialog(
    context: context,
    builder: (context) => Dialog(
      backgroundColor: AppColors.surface,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 800, maxHeight: 600),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                children: [
                  Image.asset('assets/images/salvium.png', height: 40),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'About Salvium',
                          style: AppTypography.titleLarge.copyWith(
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        Text(
                          'BITCOIN FINANCIAL INTELLIGENCE · EL SALVADOR',
                          style: AppTypography.labelSmall.copyWith(
                            color: AppColors.primary,
                            letterSpacing: 1,
                          ),
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    onPressed: () => Navigator.pop(context),
                    icon: Icon(Icons.close, color: AppColors.textSecondary),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              Text(
                'The financial intelligence layer that Bitcoin needed in El Salvador. Convert your on-chain activity into concrete and verifiable financial decisions.',
                style: AppTypography.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                  height: 1.5,
                ),
              ),
              const SizedBox(height: 24),
              Text('Modules', style: AppTypography.titleMedium.copyWith(fontWeight: FontWeight.w600)),
              const SizedBox(height: 16),
              _AboutModule(
                icon: Icons.analytics_outlined,
                title: 'Bitcoin Score',
                description: 'Your credit history built transaction by transaction. No bank.',
                badge: '0 – 850',
                color: AppColors.primary,
              ),
              const SizedBox(height: 12),
              _AboutModule(
                icon: Icons.candlestick_chart_outlined,
                title: 'Simulator',
                description: 'Analyze the best time to convert BTC with real historical data.',
                badge: 'CoinGecko · Kraken',
                color: AppColors.info,
              ),
              const SizedBox(height: 12),
              _AboutModule(
                icon: Icons.route_outlined,
                title: 'Remittances',
                description: 'Compare Lightning vs Western Union vs MoneyGram in real time.',
                badge: '\$185 saved/year',
                color: AppColors.success,
              ),
              const SizedBox(height: 12),
              _AboutModule(
                icon: Icons.account_balance_outlined,
                title: 'Pension',
                description: 'Detect on-chain savings patterns and project your retirement at 20 years.',
                badge: 'IPR 0 – 100',
                color: AppColors.warning,
              ),
              const SizedBox(height: 24),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surfaceElevated,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.verified_user_outlined, size: 16, color: AppColors.success),
                        const SizedBox(width: 8),
                        Text(
                          "Don't trust, verify.",
                          style: AppTypography.titleSmall.copyWith(
                            color: AppColors.success,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Every data verifiable directly on the blockchain',
                      style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      '"The nature of Bitcoin is such that once the version 0.1 was released, the core design was set in stone for all time."',
                      style: AppTypography.bodySmall.copyWith(
                        color: AppColors.textTertiary,
                        fontStyle: FontStyle.italic,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '— Satoshi Nakamoto',
                      style: AppTypography.labelSmall.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    ),
  );
}

class _AboutModule extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;
  final String badge;
  final Color color;

  const _AboutModule({
    required this.icon,
    required this.title,
    required this.description,
    required this.badge,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, size: 20, color: color),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: AppTypography.titleSmall.copyWith(fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 2),
                Text(
                  description,
                  style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              badge,
              style: AppTypography.monoSmall.copyWith(
                color: color,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
