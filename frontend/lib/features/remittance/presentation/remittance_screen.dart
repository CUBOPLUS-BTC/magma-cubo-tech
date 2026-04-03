import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/utils/formatters.dart';
import '../../../core/models/remittance.dart';

class RemittanceScreen extends ConsumerStatefulWidget {
  const RemittanceScreen({super.key});

  @override
  ConsumerState<RemittanceScreen> createState() => _RemittanceScreenState();
}

class _RemittanceScreenState extends ConsumerState<RemittanceScreen> {
  final _amountController = TextEditingController();
  String _frequency = 'monthly';
  bool _isLoading = false;
  RemittanceResult? _result;
  String? _error;

  static const _frequencyOptions = ['Monthly', 'Biweekly', 'Weekly'];

  @override
  void dispose() {
    _amountController.dispose();
    super.dispose();
  }

  Future<void> _handleCompare() async {
    final amountText = _amountController.text.trim();
    if (amountText.isEmpty) {
      setState(() => _error = 'Please enter an amount');
      return;
    }

    final amount = double.tryParse(amountText);
    if (amount == null || amount <= 0) {
      setState(() => _error = 'Enter a valid amount');
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
      _result = RemittanceResult(
        channels: const [
          ChannelComparison(
            name: 'Lightning Network',
            feePercent: 0.5,
            feeUsd: 2.50,
            amountReceived: 497.50,
            estimatedTime: '< 1 min',
            isRecommended: true,
          ),
          ChannelComparison(
            name: 'Bitcoin On-chain',
            feePercent: 1.2,
            feeUsd: 6.00,
            amountReceived: 494.00,
            estimatedTime: '~30 min',
          ),
          ChannelComparison(
            name: 'Western Union',
            feePercent: 7.5,
            feeUsd: 37.50,
            amountReceived: 462.50,
            estimatedTime: '1-3 days',
          ),
          ChannelComparison(
            name: 'Bank Wire',
            feePercent: 5.0,
            feeUsd: 25.00,
            amountReceived: 475.00,
            estimatedTime: '2-5 days',
          ),
        ],
        annualSavings: 420.00,
        bestChannel: 'Lightning Network',
        bestTime: const SendTimeRecommendation(
          bestTime: 'Sunday 02:00-06:00 UTC',
          currentFeeSatVb: 18,
          estimatedLowFeeSatVb: 6,
          savingsPercent: 66.7,
        ),
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
          _buildInputSection(),
          const SizedBox(height: 16),
          _buildCompareButton(),
          const SizedBox(height: 24),
          if (_error != null) _buildError(),
          if (_isLoading) _buildLoading(),
          if (_result == null && !_isLoading && _error == null) _buildInitial(),
          if (_result != null && !_isLoading) _buildResult(),
        ],
      ),
    );
  }

  Widget _buildInputSection() {
    return Row(
      children: [
        Expanded(
          child: TextField(
            controller: _amountController,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            style: AppTypography.mono,
            decoration: const InputDecoration(
              hintText: 'Amount',
              prefixText: '\$ ',
            ),
          ),
        ),
        const SizedBox(width: 12),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(4),
            border: Border.all(color: AppColors.borderSubtle),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: _frequency,
              dropdownColor: AppColors.surfaceElevated,
              style: AppTypography.mono,
              items: _frequencyOptions
                  .map((f) => DropdownMenuItem(
                        value: f.toLowerCase(),
                        child: Text(f, style: AppTypography.bodyMedium.copyWith(color: AppColors.textPrimary)),
                      ))
                  .toList(),
              onChanged: (v) {
                if (v != null) setState(() => _frequency = v);
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildCompareButton() {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: ElevatedButton(
        onPressed: _isLoading ? null : _handleCompare,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.accent,
          foregroundColor: Colors.black,
          disabledBackgroundColor: AppColors.accent.withValues(alpha: 0.5),
        ),
        child: _isLoading
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(strokeWidth: 2),
              )
            : const Text(
                'Compare Channels',
                style: TextStyle(fontWeight: FontWeight.w600),
              ),
      ),
    );
  }

  Widget _buildInitial() {
    return Padding(
      padding: const EdgeInsets.only(top: 48),
      child: Center(
        child: Text(
          'Enter a remittance amount and frequency to compare transfer channels and find the lowest fees.',
          style: AppTypography.bodyMedium,
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  Widget _buildLoading() {
    return const Padding(
      padding: EdgeInsets.only(top: 64),
      child: Center(
        child: CircularProgressIndicator(color: AppColors.accent),
      ),
    );
  }

  Widget _buildError() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Text(
        _error!,
        style: AppTypography.bodyMedium.copyWith(color: AppColors.danger),
      ),
    );
  }

  Widget _buildResult() {
    final result = _result!;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildSavingsHero(result),
        const SizedBox(height: 16),
        ...result.channels.map((channel) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: _buildChannelCard(channel),
            )),
        if (result.bestTime != null) ...[
          const SizedBox(height: 8),
          _buildBestTimeCard(result.bestTime!),
        ],
      ],
    );
  }

  Widget _buildSavingsHero(RemittanceResult result) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: Border(
          left: BorderSide(color: AppColors.accent, width: 3),
          top: BorderSide(color: AppColors.borderSubtle),
          right: BorderSide(color: AppColors.borderSubtle),
          bottom: BorderSide(color: AppColors.borderSubtle),
        ),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'ANNUAL SAVINGS',
            style: AppTypography.labelMedium.copyWith(color: AppColors.accent),
          ),
          const SizedBox(height: 8),
          Text(
            Formatters.formatUSD(result.annualSavings),
            style: AppTypography.displayMedium.copyWith(
              color: AppColors.success,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'vs worst channel',
            style: AppTypography.bodySmall,
          ),
        ],
      ),
    );
  }

  Widget _buildChannelCard(ChannelComparison channel) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(
          color: channel.isRecommended ? AppColors.accent : AppColors.borderSubtle,
        ),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  channel.name,
                  style: AppTypography.titleSmall.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              if (channel.isRecommended) ...[
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: AppColors.accent.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    'BEST',
                    style: AppTypography.labelSmall.copyWith(color: AppColors.accent),
                  ),
                ),
                const SizedBox(width: 8),
              ],
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.surfaceElevated,
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  '${channel.feePercent}%',
                  style: AppTypography.monoSmall,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Text(
                'Receives: ${Formatters.formatUSD(channel.amountReceived)}',
                style: AppTypography.mono,
              ),
              const Spacer(),
              Text(
                channel.estimatedTime,
                style: AppTypography.bodySmall,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildBestTimeCard(SendTimeRecommendation bestTime) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: AppColors.borderSubtle),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.access_time, size: 18, color: AppColors.accent),
              const SizedBox(width: 8),
              Text(
                'Best Time to Send',
                style: AppTypography.titleSmall,
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            bestTime.bestTime,
            style: AppTypography.bodyLarge,
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Text(
                'Current: ${Formatters.formatSatVb(bestTime.currentFeeSatVb)}',
                style: AppTypography.mono,
              ),
              const SizedBox(width: 16),
              Text(
                'Low: ${Formatters.formatSatVb(bestTime.estimatedLowFeeSatVb)}',
                style: AppTypography.mono.copyWith(color: AppColors.success),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            'Save ${bestTime.savingsPercent.toStringAsFixed(1)}% on fees',
            style: AppTypography.bodySmall.copyWith(color: AppColors.success),
          ),
        ],
      ),
    );
  }
}
