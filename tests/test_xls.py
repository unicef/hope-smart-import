# from pathlib import Path
#
# import pytest
#
# from hope_smart_import.utils import import_simple_xls
#
#
# @pytest.fixture()
# def xls_simple() -> str:
#     return str((Path(__file__).parent / "data" / "simple1.xlsx").absolute())
#
#
# def test_read_xls(xls_simple: str) -> None:
#     for e in import_simple_xls(xls_simple):
#         assert list(e.keys()) == ["name", "last_name", "gender"]
