import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:satsscore_app/app.dart';

void main() {
  testWidgets('App renders login screen', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(child: SatsScoreApp()),
    );
    expect(find.text('SatsScore'), findsOneWidget);
    expect(find.text('Connect'), findsOneWidget);
  });
}
