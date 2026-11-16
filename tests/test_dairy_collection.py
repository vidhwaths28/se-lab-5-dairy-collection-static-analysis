"""Regression tests for the dairy collection ledger."""

import io
import unittest
from contextlib import redirect_stdout

from dairy_collection import (
    create_connection,
    daily_total,
    farmer_token,
    low_fat,
    print_slip,
    record_milk,
    top_farmer,
)


class DairyCollectionTests(unittest.TestCase):
    """Exercise normal behavior and previously unsafe edge cases."""

    def setUp(self) -> None:
        self.connection = create_connection()

    def tearDown(self) -> None:
        self.connection.close()

    def test_parameterized_insert_preserves_sql_like_farmer_name(self) -> None:
        farmer = "O'Neil'); DROP TABLE milk; --"
        record_milk(self.connection, farmer, 4.0, 3.7, "Mon")
        row = self.connection.execute("SELECT farmer FROM milk").fetchone()
        self.assertEqual(row[0], farmer)
        self.assertEqual(
            daily_total(self.connection, "Mon"), "Total: 4.0 litres"
        )

    def test_empty_day_total_is_zero(self) -> None:
        self.assertEqual(
            daily_total(self.connection, "Tue"), "Total: 0.0 litres"
        )

    def test_top_farmer_is_none_when_ledger_is_empty(self) -> None:
        self.assertIsNone(top_farmer(self.connection))

    def test_top_farmer_uses_total_delivery(self) -> None:
        record_milk(self.connection, "Asha", 12.0, 4.0, "Mon")
        record_milk(self.connection, "Bala", 10.0, 3.8, "Mon")
        record_milk(self.connection, "Bala", 5.0, 3.9, "Tue")
        self.assertEqual(top_farmer(self.connection), "Bala")

    def test_low_fat_includes_missing_measurements(self) -> None:
        record_milk(self.connection, "Asha", 2.0, None, "Mon")
        record_milk(self.connection, "Bala", 3.0, 3.2, "Mon")
        record_milk(self.connection, "Chitra", 4.0, 4.0, "Mon")
        self.assertEqual(low_fat(self.connection), ["Asha", "Bala"])

    def test_invalid_delivery_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            record_milk(self.connection, "Asha", -1.0, 4.0, "Mon")

    def test_farmer_token_uses_sha256(self) -> None:
        self.assertEqual(
            farmer_token("Lata"),
            "39c7991402a975ff68d16747d0fbb21806c339a035d22512301c5eef1dc9122b",
        )

    def test_print_slip_treats_shell_metacharacters_as_text(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            print_slip("Asha; touch /tmp/unwanted")
        self.assertEqual(
            output.getvalue(),
            "Printing slip for Asha; touch /tmp/unwanted\n",
        )


if __name__ == "__main__":
    unittest.main()
