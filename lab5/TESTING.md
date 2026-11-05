# Lab 5 regression checks

Run these commands from the SE Labs repository root:

```sh
cd lab5
python3 -m unittest -v test_expense_tracker
```

The tests use Python's standard library; installing the static analysis tools
is not required to run them. A successful run reports six tests and `OK`.

The suite checks:

- Category totals, remaining budget, largest expense, and invalid amounts.
- Independent expense and budget state for separate tracker instances.
- Configured, missing, empty, and incorrect bank-sync passwords.
- Unique temporary report files and their permissions on POSIX systems.
- Statement paths passed as file URIs, with missing files and directories rejected.
- Demo output matching the original report across two consecutive runs.

The statement-opening test mocks the browser call. Temporary files created by
the tests are cleaned up. The saved test output from the source submission is
in [reports/after/tests_report.txt](reports/after/tests_report.txt).

For Pylint, Bandit, and Flake8 commands, see the [README](README.md).
