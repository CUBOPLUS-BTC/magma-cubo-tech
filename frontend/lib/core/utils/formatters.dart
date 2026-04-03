import 'package:intl/intl.dart';

abstract class Formatters {
  static final _usdFormat = NumberFormat.currency(symbol: '\$', decimalDigits: 2);
  static final _btcFormat = NumberFormat('0.00000000');
  static final _percentFormat = NumberFormat('+0.0;-0.0');

  static String formatBTC(double amount) => '${_btcFormat.format(amount)} BTC';

  static String formatSats(int sats) => '${NumberFormat('#,###').format(sats)} sats';

  static String formatUSD(double amount) => _usdFormat.format(amount);

  static String formatScore(int score) => score.toString();

  static String formatPercentage(double pct) => '${_percentFormat.format(pct)}%';

  static String formatSatVb(int sats) => '$sats sat/vB';

  static String formatCompact(double amount) {
    if (amount >= 1e9) return '\$${(amount / 1e9).toStringAsFixed(1)}B';
    if (amount >= 1e6) return '\$${(amount / 1e6).toStringAsFixed(1)}M';
    if (amount >= 1e3) return '\$${(amount / 1e3).toStringAsFixed(1)}K';
    return _usdFormat.format(amount);
  }
}
