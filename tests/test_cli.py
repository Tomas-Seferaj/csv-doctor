from pathlib import Path

import pandas as pd

from csv_doctor.cli import main

SAMPLE = Path(__file__).parent.parent / "sample_data" / "messy_sales.csv"


def test_cli_diagnose(capsys):
    assert main([str(SAMPLE), "-n", "amount", "-d", "date"]) == 0
    out = capsys.readouterr().out
    assert "Duplicate rows removed:  1" in out


def test_cli_saves_clean_file(tmp_path):
    out_file = tmp_path / "clean.csv"
    assert main([str(SAMPLE), "-n", "amount", "-d", "date", "-o", str(out_file)]) == 0
    df = pd.read_csv(out_file)
    assert len(df) == 5


def test_cli_missing_file():
    assert main(["does_not_exist.csv"]) == 1


def test_cli_missing_column():
    assert main([str(SAMPLE), "-n", "price"]) == 1
