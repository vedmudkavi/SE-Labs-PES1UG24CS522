# Lab 07 - Fuzz Testing: Weather Alert Classifier

**Name:** Ved Mudkavi  
**SRN:** PES1UG24CS522

## Objective

Use Hypothesis to expose input-validation bugs in all three functions, fix the
application, and rerun the same tests.

The assigned starter is from
[SETAPESU26/L6_L7_32_weather_alert](https://github.com/SETAPESU26/L6_L7_32_weather_alert/tree/main/lab7).
The handout's generic filenames `processor.py` and `test_processor.py` correspond
to `weather_alert.py` and `test_weather_alert.py` in this assignment.

## Files

- `weather_alert.py`: fixed application.
- `test_weather_alert.py`: completed Hypothesis tests and regression checks.
- `original/weather_alert.py`: unchanged assigned application for reproducing failures.
- `requirements.txt`: testing dependencies.
- `Lab_07_Fuzz_Testing_Report.pdf`: final report containing all six supplied screenshots.
- `screenshots/`: the six original, unmodified terminal captures.

**Submission status:** This folder contains all handout deliverables: the
screenshot PDF, fixed application, and completed tests.

## Run the fixed application and tests

From `Lab-07`, use Python 3.8 or later:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python weather_alert.py
python -m pytest test_weather_alert.py -v --hypothesis-seed=732
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.
The compatible dependency releases are selected by pip for the Python version.
The recorded runs used Python 3.12.14, Hypothesis 6.170.15 and pytest 9.2.0.

## Reproduce the original failures

Keep the fixed code intact. In the activated environment on macOS/Linux, copy
the original application and the SAME test suite into a temporary directory:

```sh
before_dir=$(mktemp -d)
cp original/weather_alert.py "$before_dir/weather_alert.py"
cp test_weather_alert.py "$before_dir/test_weather_alert.py"
(
  cd "$before_dir"
  python weather_alert.py
  python -m pytest test_weather_alert.py -v --tb=short --hypothesis-seed=732
)
```

The original suite produced **6 failed, 10 passed**. The fixed application passed
**all 16 collected cases** with the same test file. Fuzz properties use up to
300 examples each; these are generated inputs, not 300 separately collected tests.

## Validation decisions

The starter does not define invalid-input results. This implementation returns
`None` for invalid input and prints a clear message in the interactive program.
It preserves valid outputs and the original wind-category thresholds.

| Function | Valid input | Invalid input behavior |
| --- | --- | --- |
| `parse_reading` | Finite temperature / integer humidity from 0 to 100 | Return `None` |
| `wind_category` | Nonnegative integer speed; 0-38 none, 39-88 advisory, 89+ warning | Return `None` |
| `rainfall_spread` | Nonempty CSV of finite, nonnegative rainfall values | Return `None` |

All functions accept strings with surrounding whitespace. Negative temperatures
are allowed. Wrong types, malformed delimiters, missing CSV fields, invalid
numbers, NaN and infinity are checked by the tests. Valid structured properties
also ensure the functions do not simply reject every input.

## Included screenshot evidence

1. `01_original_program.png`: original program with `35.5/80`, `45`, and `2,5.5,10`.
2. `02_original_test_results.png`: collected cases and failing-test status.
3. `03_fuzz_failure_details.png`: Hypothesis failures for all three functions.
4. `04_failure_summary.png`: remaining failures and `6 failed, 10 passed`.
5. `05_fixed_program.png`: `bad`, `-1`, and `2,,5` handled without crashing.
6. `06_passing_tests.png`: the SAME tests after fixing, with `16 passed`.

The handout requires four stages of screenshots, not necessarily exactly four
image files. These six captures cover all four stages. The fixed-program
capture demonstrates invalid-input handling; a second valid-input screenshot
is not an additional requirement in the handout. The PDF preserves each image
and uses larger landscape pages for readable terminal output.
