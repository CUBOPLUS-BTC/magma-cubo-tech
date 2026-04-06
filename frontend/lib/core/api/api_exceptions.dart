class ApiException implements Exception {
  final String message;
  final int? statusCode;

  const ApiException(this.message, {this.statusCode});

  @override
  String toString() => message;
}

class UnauthorizedException extends ApiException {
  const UnauthorizedException() : super('Session expired', statusCode: 401);
}

class NetworkException extends ApiException {
  const NetworkException() : super('No connection to server');
}

class ServerException extends ApiException {
  const ServerException([super.message = 'Server error'])
    : super(statusCode: 500);
}
