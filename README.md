#  csv-doctor

![tests](https://github.com/YOUR_USERNAME/csv-doctor/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

**Find and fix the most common problems in messy CSV files, in one command.**

Real-world CSV exports are full of empty rows, duplicates, extra spaces, numbers like `"1,200"` or `"$350"`, and dates in mixed formats. These cause crashes and wrong results in scripts. `csv-doctor` diagnoses them and saves a clean copy.

##  What it fixes

| Problem | Example | Fix |
|---|---|---|
| Empty rows | `,,,` | Removed |
| Duplicate rows | same order twice | Removed |
| Extra spaces | `"  Arben "` | Trimmed to `"Arben"` |
| Formatted numbers | `"1,200"`, `"$350"` | Converted to `1200`, `350` |
| Mixed date formats | `2026-01-15`, `01/20/2026` | Converted to real dates |
| Invalid values | `"abc"`, `"not a date"` | Reported and set to empty |

##  Quick start

```bash
git clone https://github.com/YOUR_USERNAME/csv-doctor.git
cd csv-doctor
pip install -r requirements.txt
```

**Check a file** (nothing is changed):

```bash
python -m csv_doctor sample_data/messy_sales.csv --numbers amount --dates date
```

```
Rows: 7 -> 5
Empty rows removed:      1
Duplicate rows removed:  1
Cells with extra spaces: 2
Invalid numbers in 'amount': 1
Invalid dates in 'date':   1
Total issues: 6
```

**Save a cleaned copy:**

```bash
python -m csv_doctor sample_data/messy_sales.csv -n amount -d date -o cleaned.csv
```

##  Use it in Python

```python
import pandas as pd
from csv_doctor import clean

df = pd.read_csv("sales.csv", dtype=str)
cleaned, report = clean(df, number_cols=["amount"], date_cols=["date"])

print(report.summary())
```

##  Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

Tests run automatically on every push with GitHub Actions (Python 3.10 to 3.12).

##  Project structure

```
csv-doctor/
├── csv_doctor/
│   ├── core.py        # diagnose() and clean() logic
│   ├── cli.py         # command-line interface
│   └── __main__.py    # enables `python -m csv_doctor`
├── tests/             # pytest test suite
└── sample_data/       # example messy CSV
```

##  Ideas for the future

- [ ] Detect and fix wrong text encodings
- [ ] Support Excel (`.xlsx`) files
- [ ] Auto-detect number and date columns

##  Need help with your Python code?

I fix bugs and build scripts like this one. [Hire me on Fiverr](https://www.fiverr.com/YOUR_FIVERR_USERNAME).

## License

MIT
