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
import '../utils/breakpoints.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _shellNavigatorKey = GlobalKey<NavigatorState>();

const _navItems = [
  ('/home', Icons.home_outlined, Icons.home, 'Home'),
  ('/score', Icons.speed_outlined, Icons.speed, 'Score'),
  ('/simulator', Icons.show_chart_outlined, Icons.show_chart, 'Simulate'),
  ('/remittance', Icons.send_outlined, Icons.send, 'Remittances'),
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
      appBar: AppBar(
        backgroundColor: AppColors.surface,
        elevation: 0,
        title: const Text(
          'SatsScore',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            color: AppColors.textPrimary,
          ),
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.logout_outlined, size: 20, color: AppColors.textSecondary),
            onPressed: () => _handleLogout(context),
          ),
        ],
      ),
      body: child,
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          border: Border(
            top: BorderSide(color: AppColors.borderSubtle, width: 1),
          ),
        ),
        child: BottomNavigationBar(
          currentIndex: currentIndex,
          onTap: (i) => context.go(_navItems[i].$1),
          backgroundColor: AppColors.surface,
          selectedItemColor: AppColors.accent,
          unselectedItemColor: AppColors.textTertiary,
          type: BottomNavigationBarType.fixed,
          elevation: 0,
          selectedLabelStyle: const TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.3,
          ),
          unselectedLabelStyle: const TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w500,
          ),
          items: _navItems
              .map(
                (t) => BottomNavigationBarItem(
                  icon: Icon(t.$2, size: 22),
                  activeIcon: Icon(t.$3, size: 22),
                  label: t.$4,
                ),
              )
              .toList(),
        ),
      ),
    );
  }
}

Future<void> _handleLogout(BuildContext context) async {
  final confirmed = await showDialog<bool>(
    context: context,
    builder: (context) => AlertDialog(
      backgroundColor: AppColors.surface,
      title: const Text(
        'Logout',
        style: TextStyle(color: AppColors.textPrimary),
      ),
      content: const Text(
        'Are you sure you want to logout?',
        style: TextStyle(color: AppColors.textSecondary),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(false),
          child: Text('Cancel', style: TextStyle(color: AppColors.textSecondary)),
        ),
        ElevatedButton(
          onPressed: () => Navigator.of(context).pop(true),
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.accent,
            foregroundColor: Colors.black,
          ),
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
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Row(
        children: [
          Container(
            width: 32,
            height: 32,
            decoration: BoxDecoration(
              color: AppColors.accent,
              borderRadius: BorderRadius.circular(6),
            ),
            child: const Icon(Icons.bolt, size: 18, color: Colors.black),
          ),
          const SizedBox(width: 12),
          const Text(
            'SatsScore',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w600,
              color: AppColors.textPrimary,
            ),
          ),
        ],
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
                  ? AppColors.accent.withValues(alpha: 0.1)
                  : _isHovered
                  ? AppColors.surfaceElevated
                  : Colors.transparent,
              borderRadius: BorderRadius.circular(4),
            ),
            child: Row(
              children: [
                if (widget.isSelected)
                  Container(
                    width: 3,
                    height: 16,
                    margin: const EdgeInsets.only(right: 10),
                    decoration: BoxDecoration(
                      color: AppColors.accent,
                      borderRadius: BorderRadius.circular(1),
                    ),
                  )
                else
                  const SizedBox(width: 13),
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
