import pandas as pd
import pytest

from csv_doctor import clean, diagnose


@pytest.fixture
def messy():
    return pd.DataFrame(
        {
            "name": ["  Ana ", "Ben", None, "Ben"],
            "amount": ["1,200", "$30", None, "$30"],
            "date": ["2026-01-15", "01/20/2026", None, "01/20/2026"],
        }
    )


def test_removes_empty_rows(messy):
    _, report = clean(messy)
    assert report.empty_rows == 1


def test_removes_duplicates(messy):
    df, report = clean(messy, number_cols=["amount"], date_cols=["date"])
    assert report.duplicate_rows == 1
    assert len(df) == 2


def test_strips_whitespace(messy):
    df, report = clean(messy)
    assert df.loc[0, "name"] == "Ana"
    assert report.whitespace_cells == 1


def test_converts_numbers(messy):
    df, _ = clean(messy, number_cols=["amount"])
    assert df["amount"].tolist() == [1200, 30]


def test_counts_bad_numbers():
    df = pd.DataFrame({"amount": ["10", "abc", "20"]})
    _, report = clean(df, number_cols=["amount"])
    assert report.bad_numbers == {"amount": 1}


def test_parses_mixed_date_formats(messy):
    df, report = clean(messy, date_cols=["date"])
    assert df["date"].dt.month.tolist() == [1, 1]
    assert report.bad_dates == {}


def test_diagnose_does_not_change_data(messy):
    before = messy.copy()
    diagnose(messy, number_cols=["amount"], date_cols=["date"])
    pd.testing.assert_frame_equal(messy, before)


def test_clean_data_has_no_issues():
    df = pd.DataFrame({"a": ["1", "2"], "b": ["x", "y"]})
    assert diagnose(df, number_cols=["a"]).total_issues == 0
