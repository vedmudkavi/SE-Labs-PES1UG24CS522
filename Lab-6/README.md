# Lab 06: Code and Branch Coverage Analysis

**Student:** Ved Mudkavi (PES1UG24CS522)  
**Problem 32:** Weather Alert Classifier

Application source: [assigned starter repository](https://github.com/SETAPESU26/L6_L7_32_weather_alert/tree/main/lab6).
The application is unchanged. Tests exercise wind, rain, heat, and overall alert classification.

## Code coverage

The original two starter tests covered 32% of the application statements.
The expanded suite has 15 passing tests and covers all 38 statements (100% line coverage, zero missed statements).
It checks all alert levels, saturated and unsaturated soil, humidity adjustment, overall severity, and invalid alerts.

```bash
cd Lab-6
python -m pip install coverage pytest
python -m coverage run --source=weather_alert -m pytest CodeCoverageTest_weather_alert_application.py
python -m coverage report -m
```

![Code coverage results](code_coverage.png)

Figure 1: All 15 tests passed, achieving 100% statement coverage (38 statements, zero missed).
