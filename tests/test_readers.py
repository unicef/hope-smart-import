from pathlib import Path

import pytest

from hope_smart_import.readers import open_csv, open_xls, open_xls_multi


@pytest.fixture()
def xls() -> str:
    return str((Path(__file__).parent / "data" / "r1.xlsx").absolute())


@pytest.fixture()
def csv() -> str:
    return str((Path(__file__).parent / "data" / "r1.csv").absolute())


@pytest.mark.parametrize("start_at", [0, 1])
def test_read_csv_headers(csv: str, start_at: int) -> None:
    for e in open_csv(csv, start_at=start_at, headers=True):
        assert list(e.keys()) == ["name", "last_name", "gender"]


@pytest.mark.parametrize("start_at", [0, 1])
def test_read_csv_no_headers(csv: str, start_at: int) -> None:
    for e in open_csv(csv, start_at=start_at, headers=False):
        assert list(e.keys()) == ["column1", "column2", "column3"]


@pytest.mark.parametrize("start_at", [0, 1])
def test_read_xls_headers(xls: str, start_at: int) -> None:
    for e in open_xls(xls, start_at=start_at):
        assert list(e.keys()) == ["name", "last_name", "gender"]


@pytest.mark.parametrize("start_at", [0, 1])
def test_read_xls_no_headers(xls: str, start_at: int) -> None:
    for e in open_xls(xls, start_at=start_at, headers=False):
        assert list(e.keys()) == ["column1", "column2", "column3"]


@pytest.mark.parametrize("start_at", [0, 1])
def test_read_multi_xls_headers(xls: str, start_at: int) -> None:
    ret = []
    for e, sh in open_xls_multi(xls, sheets=[0, 1], start_at=start_at, headers=True):
        for row in sh:
            ret.append((e, row))
    if start_at == 0:
        # Sheet 0 - Row 0
        assert ret[0] == (0, {"name": "John", "last_name": "Doe", "gender": "M"})
        # Sheet 0 - Row 1
        assert ret[1] == (0, {"name": "Jane", "last_name": "Doe", "gender": "F"})
        # Sheet 1 - Row 0
        assert ret[2] == (1, {"name": "John1", "last_name": "Doe1", "gender": "m"})
        # Sheet 1 - Row 1
        assert ret[3] == (1, {"name": "Jane1", "last_name": "Doe1", "gender": "f"})
    if start_at == 1:
        # Sheet 0 - Row 0
        assert ret[0] == (0, {"name": "Jane", "last_name": "Doe", "gender": "F"})
        # Sheet 0 - Row 1
        # assert ret[0] == (1, {"name": "John", "last_name": "Doe", "gender": "M"})
        # Sheet 1 - Row 1
        assert ret[1] == (1, {"name": "Jane1", "last_name": "Doe1", "gender": "f"})
