"""Regression checks for the lab fixes."""

import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from expense_tracker import (
    ExpenseTracker, check_sync_password, export_report, main, open_statement,
)


class ExpenseTrackerTests(unittest.TestCase):
    """Check normal behaviour and security-related helper changes."""

    def test_totals_budget_and_invalid_amounts(self):
        tracker = ExpenseTracker()
        self.assertIsNone(tracker.biggest_expense())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(tracker.add_expense(0))
            self.assertFalse(tracker.add_expense(-50))
        self.assertTrue(tracker.add_expense(450, "Food"))
        tracker.add_expense(300, "Food")
        tracker.add_expense(1200, "Travel", "Cab")
        tracker.set_budget(5000)
        self.assertEqual(tracker.total_by_category(),
                         {"Food": 750, "Travel": 1200})
        self.assertEqual(tracker.remaining_budget(), 3050)
        self.assertEqual(tracker.biggest_expense()["note"], "Cab")

    def test_trackers_do_not_share_state(self):
        first, second = ExpenseTracker(), ExpenseTracker()
        first.add_expense(100)
        first.set_budget(500)
        self.assertEqual(second.expenses, [])
        self.assertEqual(second.remaining_budget(), 20000)

    def test_password_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(check_sync_password(""))
            self.assertFalse(check_sync_password("guess"))
        with patch.dict(os.environ, {"BANK_SYNC_PASSWORD": "test-\u20b9-value"}):
            self.assertTrue(check_sync_password("test-\u20b9-value"))
            self.assertFalse(check_sync_password("wrong"))
        with patch.dict(os.environ, {"BANK_SYNC_PASSWORD": ""}):
            self.assertFalse(check_sync_password(""))

    def test_report_files_are_created_and_unique(self):
        paths = []
        try:
            paths.append(Path(export_report()))
            paths.append(Path(export_report()))
            self.assertNotEqual(paths[0], paths[1])
            for path in paths:
                self.assertTrue(path.is_file())
                self.assertEqual(path.read_bytes(), b"")
                if os.name == "posix":
                    self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        finally:
            for path in paths:
                path.unlink(missing_ok=True)

    def test_statement_path_is_passed_as_a_file_uri(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "statement ; echo injected.txt"
            path.write_text("Statement", encoding="utf-8")
            with patch("expense_tracker.webbrowser.open", return_value=True) as opener:
                self.assertTrue(open_statement(path))
                opener.assert_called_once_with(path.resolve().as_uri())
                with self.assertRaises(FileNotFoundError):
                    open_statement(Path(directory) / "missing.txt")
                with self.assertRaises(ValueError):
                    open_statement(directory)
                self.assertEqual(opener.call_count, 1)

    def test_demo_output_matches_original_even_on_second_run(self):
        original = (Path(__file__).parent / "reports/before/demo_report.txt")
        expected = original.read_text(encoding="utf-8")
        with patch.dict(os.environ, {}, clear=True):
            for _ in range(2):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    main()
                self.assertEqual(output.getvalue(), expected)


if __name__ == "__main__":
    unittest.main()
