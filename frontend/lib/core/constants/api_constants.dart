class ApiConstants {
  static const String baseUrl = 'http://localhost:8000';
  static const String authChallenge = '$baseUrl/auth/challenge';
  static const String authVerify = '$baseUrl/auth/verify';
  static const String authMe = '$baseUrl/auth/me';
  static const String score = '$baseUrl/score';
  static const String price = '$baseUrl/price';
  static const String simulateVolatility = '$baseUrl/simulate/volatility';
  static const String simulateConversion = '$baseUrl/simulate/conversion';
  static const String remittanceCompare = '$baseUrl/remittance/compare';
  static const String remittanceFees = '$baseUrl/remittance/fees';
}
