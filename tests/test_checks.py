import pandas as pd

from policylens.checks import blank_cells, duplicates


def test_blank_cells_flagged_not_filled():
    df = pd.DataFrame({"Customer Name": ["A", "B"], "Phone": ["1", None]})
    assert blank_cells(df) == {"Phone": [1]}


def test_no_blanks_returns_empty():
    df = pd.DataFrame({"Customer Name": ["A"], "Phone": ["1"]})
    assert blank_cells(df) == {}


def test_duplicates_found():
    df = pd.DataFrame({"Customer Name": ["A", "A"], "Phone": ["1", "1"]})
    assert duplicates(df, ["Customer Name", "Phone"]) == [0, 1]


def test_missing_key_column_ignored():
    df = pd.DataFrame({"Customer Name": ["A"]})
    assert duplicates(df, ["Phone"]) == []
