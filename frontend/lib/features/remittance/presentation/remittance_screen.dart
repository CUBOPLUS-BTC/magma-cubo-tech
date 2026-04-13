import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/utils/formatters.dart';
import '../../../core/models/remittance.dart';
import '../../../shared/widgets/channel_card.dart';
import '../../../shared/widgets/savings_card.dart';
import '../../../shared/widgets/loading_shimmer.dart';
import '../providers/remittance_provider.dart';

class RemittanceScreen extends ConsumerStatefulWidget {
  const RemittanceScreen({super.key});

  @override
  ConsumerState<RemittanceScreen> createState() => _RemittanceScreenState();
}

class _RemittanceScreenState extends ConsumerState<RemittanceScreen> {
  final _amountController = TextEditingController();
  String _frequency = 'monthly';

  static const _frequencyOptions = ['Monthly', 'Biweekly', 'Weekly'];

  @override
  void dispose() {
    _amountController.dispose();
    super.dispose();
  }

  void _handleCompare() {
    final amountText = _amountController.text.trim();
    if (amountText.isEmpty) return;

    final amount = double.tryParse(amountText);
    if (amount == null || amount <= 0) return;

    ref.read(remittanceProvider.notifier).compare(amount, _frequency);
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(remittanceProvider);

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(),
          const SizedBox(height: 24),
          _buildInputCard(),
          const SizedBox(height: 16),
          _buildCompareButton(state.isLoading),
          const SizedBox(height: 24),
          if (state.error != null) _buildError(state.error!),
          if (state.isLoading) _buildLoading(),
          if (state.result == null && !state.isLoading && state.error == null)
            _buildEmpty(),
          if (state.result != null && !state.isLoading) _buildResult(state),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: AppColors.primary.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(
                Icons.route_rounded,
                color: AppColors.primary,
                size: 24,
              ),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Remittance Optimizer', style: AppTypography.titleLarge),
                Text(
                  'Compare transfer channels and save on fees',
                  style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
                ),
              ],
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildInputCard() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Transfer Details', style: AppTypography.labelMedium),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                flex: 3,
                child: TextField(
                  controller: _amountController,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  style: AppTypography.mono.copyWith(fontSize: 18),
                  decoration: InputDecoration(
                    hintText: '0.00',
                    prefixText: '\$ ',
                    prefixStyle: AppTypography.mono.copyWith(
                      color: AppColors.textSecondary,
                      fontSize: 18,
                    ),
                    filled: true,
                    fillColor: AppColors.surfaceElevated,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                flex: 2,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12),
                  decoration: BoxDecoration(
                    color: AppColors.surfaceElevated,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: _frequency,
                      isExpanded: true,
                      dropdownColor: AppColors.surfaceElevated,
                      style: AppTypography.mono,
                      icon: Icon(Icons.keyboard_arrow_down_rounded, color: AppColors.textSecondary),
                      items: _frequencyOptions
                          .map(
                            (f) => DropdownMenuItem(
                              value: f.toLowerCase(),
                              child: Text(
                                f,
                                style: AppTypography.bodyMedium.copyWith(
                                  color: AppColors.textPrimary,
                                ),
                              ),
                            ),
                          )
                          .toList(),
                      onChanged: (v) {
                        if (v != null) setState(() => _frequency = v);
                      },
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildCompareButton(bool isLoading) {
    return SizedBox(
      width: double.infinity,
      height: 52,
      child: ElevatedButton(
        onPressed: isLoading ? null : _handleCompare,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          disabledBackgroundColor: AppColors.primary.withValues(alpha: 0.3),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
        child: isLoading
            ? const SizedBox(
                width: 22,
                height: 22,
                child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white),
              )
            : Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.compare_arrows_rounded, size: 22),
                  const SizedBox(width: 8),
                  Text(
                    'Compare Channels',
                    style: AppTypography.titleSmall.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
      ),
    );
  }

  Widget _buildEmpty() {
    return Column(
      children: [
        Container(
          margin: const EdgeInsets.only(top: 32),
          padding: const EdgeInsets.all(32),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppColors.borderSubtle),
          ),
          child: Column(
            children: [
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: AppColors.primary.withValues(alpha: 0.1),
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.account_balance_wallet_rounded,
                  size: 48,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(height: 20),
              Text('Save on every transfer', style: AppTypography.titleMedium),
              const SizedBox(height: 8),
              Text(
                'Compare fees across Lightning, on-chain,\nand traditional transfer methods',
                style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        _buildChannelPreview(),
      ],
    );
  }

  Widget _buildChannelPreview() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.speed_rounded, size: 16, color: AppColors.textSecondary),
              const SizedBox(width: 6),
              Text('Available Channels', style: AppTypography.labelMedium),
            ],
          ),
          const SizedBox(height: 16),
          _channelPreviewRow(
            icon: Icons.bolt_rounded,
            name: 'Lightning Network',
            time: '< 1 min',
            fee: '~0.5%',
            color: AppColors.primary,
          ),
          const SizedBox(height: 12),
          _channelPreviewRow(
            icon: Icons.link_rounded,
            name: 'Bitcoin On-chain',
            time: '~30 min',
            fee: '~1.2%',
            color: AppColors.info,
          ),
          const SizedBox(height: 12),
          _channelPreviewRow(
            icon: Icons.account_balance_rounded,
            name: 'Traditional',
            time: '1-5 days',
            fee: '5-8%',
            color: AppColors.danger,
          ),
        ],
      ),
    );
  }

  Widget _channelPreviewRow({
    required IconData icon,
    required String name,
    required String time,
    required String fee,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.06),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: color.withValues(alpha: 0.12)),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, size: 18, color: color),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(name, style: AppTypography.titleSmall),
                Text(
                  time,
                  style: AppTypography.labelSmall.copyWith(color: AppColors.textSecondary),
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              fee,
              style: AppTypography.mono.copyWith(
                color: color,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLoading() {
    return Padding(
      padding: const EdgeInsets.only(top: 16),
      child: Column(
        children: [
          LoadingShimmer.card(height: 100),
          const SizedBox(height: 12),
          LoadingShimmer.card(height: 80),
          const SizedBox(height: 12),
          LoadingShimmer.card(height: 80),
          const SizedBox(height: 12),
          LoadingShimmer.card(height: 80),
        ],
      ),
    );
  }

  Widget _buildError(String error) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.danger.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.danger.withValues(alpha: 0.2)),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: AppColors.danger.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(Icons.error_outline_rounded, size: 20, color: AppColors.danger),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              error,
              style: AppTypography.bodyMedium.copyWith(color: AppColors.danger),
            ),
          ),
          IconButton(
            onPressed: () {
              final amountText = _amountController.text.trim();
              if (amountText.isEmpty) return;
              final amount = double.tryParse(amountText);
              if (amount == null || amount <= 0) return;
              ref.read(remittanceProvider.notifier).compare(amount, _frequency);
            },
            icon: const Icon(Icons.refresh_rounded, color: AppColors.danger),
          ),
        ],
      ),
    );
  }

  Widget _buildResult(RemittanceState state) {
    final result = state.result!;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SavingsCard(
          annualSavings: result.annualSavings,
          vsChannel: 'worst channel',
          monthlyAmount: double.tryParse(_amountController.text.trim()) ?? 500,
        ),
        const SizedBox(height: 24),
        Row(
          children: [
            const Icon(Icons.hub_rounded, size: 18, color: AppColors.primary),
            const SizedBox(width: 8),
            Text('Transfer Channels', style: AppTypography.titleMedium),
          ],
        ),
        const SizedBox(height: 12),
        ...result.channels.map(
          (channel) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: ChannelCard(channel: channel),
          ),
        ),
        if (result.bestTime != null) ...[
          const SizedBox(height: 16),
          _buildBestTimeCard(result.bestTime!),
        ],
      ],
    );
  }

  Widget _buildBestTimeCard(SendTimeRecommendation bestTime) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            AppColors.surface,
            AppColors.surfaceElevated.withValues(alpha: 0.5),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: AppColors.info.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: const Icon(
                  Icons.access_time_rounded,
                  size: 20,
                  color: AppColors.info,
                ),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Best Time to Send', style: AppTypography.titleSmall),
                  Text(
                    'Optimize for lowest fees',
                    style: AppTypography.labelSmall.copyWith(color: AppColors.textSecondary),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.success.withValues(alpha: 0.08),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Text(
              bestTime.bestTime,
              style: AppTypography.bodyLarge.copyWith(
                color: AppColors.success,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(child: _feeTag('Current', Formatters.formatSatVb(bestTime.currentFeeSatVb), AppColors.textSecondary)),
              const SizedBox(width: 8),
              Expanded(child: _feeTag('Low', Formatters.formatSatVb(bestTime.estimatedLowFeeSatVb), AppColors.success)),
              const SizedBox(width: 8),
              Expanded(child: _feeTag('Save', '${bestTime.savingsPercent.toStringAsFixed(0)}%', AppColors.primary)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _feeTag(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color.withValues(alpha: 0.12)),
      ),
      child: Column(
        children: [
          Text(
            value,
            style: AppTypography.mono.copyWith(
              color: color,
              fontWeight: FontWeight.w600,
              fontSize: 13,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            label,
            style: AppTypography.labelSmall.copyWith(
              color: AppColors.textSecondary,
              fontSize: 10,
            ),
          ),
        ],
      ),
    );
  }
}
