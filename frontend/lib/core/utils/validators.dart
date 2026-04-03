abstract class Validators {
  static final _btcAddressRegex = RegExp(
    r'^(bc1[a-zA-HJ-NP-Z0-9]{25,62}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$',
  );

  static bool isValidBTCAddress(String addr) => _btcAddressRegex.hasMatch(addr);

  static String? validateBTCAddress(String? value) {
    if (value == null || value.isEmpty) return 'Enter a Bitcoin address';
    if (!isValidBTCAddress(value)) return 'Invalid Bitcoin address';
    return null;
  }
}
