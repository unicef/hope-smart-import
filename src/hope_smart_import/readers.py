import csv
from typing import TYPE_CHECKING, Any, Iterable

import openpyxl

if TYPE_CHECKING:
    from openpyxl.workbook.workbook import Workbook
    from openpyxl.worksheet.worksheet import Worksheet

    from .types import MultiSheetResult, SheetResult


def _read_worksheet(sheet: "Worksheet", start_at: int, headers: bool) -> Iterable[dict[str, Any]]:
    rows = sheet.rows
    if headers:
        field_names = [str(cell.value) for cell in next(rows)]
        for i, row in enumerate(rows):
            if i < start_at:
                continue
            yield dict(zip(field_names, (cell.value for cell in row)))  # pragma: no branch
    else:
        for i, row in enumerate(rows):
            field_names = [f"column{d + 1}" for d in range(len(row))]
            if i < start_at:
                continue
            yield dict(zip(field_names, (cell.value for cell in row)))  # pragma: no branch


def open_xls(filepath: str, *, sheet_index: int = 0, start_at: int = 0, headers: bool = True) -> "SheetResult":
    wb: "Workbook" = openpyxl.load_workbook(filepath)
    sh: "Worksheet" = wb.worksheets[sheet_index]
    for i in _read_worksheet(sh, start_at=start_at, headers=headers):
        yield i


def open_xls_multi(
    filepath: str, sheets: list[int] = (0,), start_at: list[int] | int = 0, headers: list[bool] | bool = True
) -> "MultiSheetResult":
    wb: "Workbook" = openpyxl.load_workbook(filepath)
    for si in sheets:
        sh: "Worksheet" = wb.worksheets[si]
        start_at = start_at if isinstance(start_at, int) else start_at[si]
        headers = headers if isinstance(headers, bool) else headers[si]
        yield si, _read_worksheet(sh, start_at=start_at, headers=headers)


def open_csv(filepath: str, *, start_at: int = 0, headers: bool = False) -> "SheetResult":
    with open(filepath) as f:
        if headers:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i < start_at:
                    continue
                yield row
        else:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i < start_at:
                    continue
                field_names = [f"column{d + 1}" for d in range(len(row))]
                yield dict(zip(field_names, row))
