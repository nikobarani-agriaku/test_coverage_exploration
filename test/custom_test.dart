import 'package:flutter_test/flutter_test.dart';

void main() {
  test("test unit test", () {
    var x = 1;
    var y = 2;

    var res = x + y;

    expect(res, 3);
  });
}
