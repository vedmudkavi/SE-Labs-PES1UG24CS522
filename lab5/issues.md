# Lab 5: Static Code Analysis

Name: Ved Mudkavi

SRN: PES1UG24CS522

Program: Personal Expense Tracker

Line numbers below refer to the original `expense_tracker.py` in commit `ece3ac7`.
Security issues are listed in descending Bandit severity.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| B605: shell command | Security - High | 61 | The statement path is joined to a shell command. Shell characters in a filename could run another command. | Resolve an existing file and pass its file URI to `webbrowser.open`, without constructing a shell command. |
| B108: fixed temporary directory | Security - Medium | 8 | The report directory is hardcoded under `/tmp`. It may not exist and its ownership is not controlled by the program. | Remove the fixed directory and use Python's temporary-file facility. |
| B306: `tempfile.mktemp` | Security - Medium | 55 | `mktemp` returns a filename without creating it. Another process could create that file first. | Use `NamedTemporaryFile(delete=False)` to create the file securely and return its path. |
| B105: hardcoded password | Security - Low | 5 | The bank-sync password is visible in the source. | Read `BANK_SYNC_PASSWORD` from the environment, reject unset/empty values, and compare using `hmac.compare_digest`. |
| W0718: broad exception | Code quality | 39-42 | Catching every `Exception` can hide unexpected errors. The expected case is an empty expense list. | Use `max(..., default=None)` to handle the empty list directly. |
| W0603: global statement | Code quality | 29 | Updating a global budget makes tracker state shared across calls. | Keep expenses and budget in an `ExpenseTracker` object. Each tracker has separate state. |
| C0103: inconsistent names | Naming | 7, 11, 20, 28, 33, 38, 44, 49, 53, 55, 59 | Functions and variables use mixed naming styles. | Use snake_case for methods, functions, and variables. |
| C0114 / C0116: missing docstrings | Documentation | 1 and function definitions | The module and functions do not describe their purpose. | Add short module, class, and function docstrings. |
| C0200: index-based loop | Code quality | 45-46 | The ledger loops over `range(len(expenses))` and indexes the list repeatedly. | Use `enumerate(..., start=1)` to get the number and expense together. |
| E203: extra space | Formatting | 15 | There is whitespace before a dictionary colon. | Remove the extra space. |
| E302: missing blank line | Formatting | 44 | Top-level functions need two blank lines between definitions. | Use correct spacing in the reorganized file. |
| E261: inline comment spacing | Formatting | 74 | The inline comment has only one preceding space. | Use two spaces before the comment. |
| E501: long line | Formatting | 77 | The summary print exceeds 79 characters. | Split the call across two lines. |

An additional change puts the demo under `if __name__ == "__main__"` so importing the module does not print output or add expenses.

## Results

| Tool | Before | After |
|---|---|---|
| Pylint | 5.27/10; 26 messages | 10.00/10; no messages |
| Bandit | 4 issues: 1 High, 2 Medium, 1 Low | No issues |
| Flake8 | 4 errors | No errors |

Reports are in `reports/before/` and `reports/after/`. The empty after-Flake8 report means the tool found no errors. No rules were disabled to obtain these results.

The demo output matches before and after: four accepted expenses, Food 750, Travel 1200, Bills 999, remaining budget 2051, and the largest expense is the cab ride. Six regression tests also pass.

## Helper behaviour

- `export_report()` still returns a report path. It now creates an empty file at that path instead of just inventing a filename. The caller must remove the file when finished.
- `open_statement()` opens a local file in the default browser rather than using Linux's `xdg-open` through a shell. Missing files raise `FileNotFoundError`; directories are rejected. The browser call was mocked in tests, so no actual browser launch was verified.
- Password checks return false unless `BANK_SYNC_PASSWORD` is configured. The demo uses `guess`, which should not be used as the configured password.
- State-related functions are now methods of `ExpenseTracker`; this removes the global budget and keeps repeated demo runs independent.
