import csv
from collections.abc import Callable
from itertools import islice
from typing import TYPE_CHECKING, Any, Iterable, overload

import openpyxl

if TYPE_CHECKING:
    from openpyxl.workbook.workbook import Workbook
    from openpyxl.worksheet.worksheet import Worksheet

    from .types import MultiSheetResult, SheetResult, ValueMapper


def identity(x: Any) -> Any:
    return x


def _read_worksheet(
    sheet: "Worksheet",
    start_at_row: int,
    has_header: bool,
    value_mapper: Callable[[Any], Any] = identity,
) -> Iterable[dict[str, Any]]:
    rows = sheet.rows

    field_names = None
    generate_field_names = False
    if has_header:
        field_names = [str(cell.value) for cell in next(rows)]
    else:
        generate_field_names = True

    rows = islice(rows, start_at_row, None)
    for row in rows:
        if generate_field_names:
            field_names = [f"column{d + 1}" for d in range(len(row))]

        yield dict(zip(field_names, (value_mapper(cell.value) for cell in row), strict=True))


@overload
def open_xls(filepath: str, *, sheet_index: int = ..., start_at_row: int = ..., has_header: bool = ...,
             value_mapper: "ValueMapper" = ...) -> "SheetResult": ...


@overload
def open_xls(filepath: str, *, sheet_name: str, start_at_row: int = ..., has_header: bool = ...,
             value_mapper: "ValueMapper" = ...) -> "SheetResult": ...


def open_xls(
    filepath: str,
    *,
    sheet_index: int = 0,
    sheet_name: str | None = None,
    start_at_row: int = 0,
    has_header: bool = True,
    value_mapper: "ValueMapper" = identity,
) -> "SheetResult":
    wb: "Workbook" = openpyxl.load_workbook(filepath)
    if sheet_name is not None:
        sheet_index = wb.sheetnames.index(sheet_name)
    sh: "Worksheet" = wb.worksheets[sheet_index]
    yield from _read_worksheet(sh, start_at_row=start_at_row, has_header=has_header, value_mapper=value_mapper)


@overload
def open_xls_multi(filepath: str, sheet_indices: list[int] = ..., *, start_at_row: list[int] | int = ...,
                   have_header: list[bool] | bool = ..., value_mapper: "ValueMapper" = ...) -> "MultiSheetResult": ...


@overload
def open_xls_multi(filepath: str, *, sheet_names: list[str], start_at_row: list[int] | int = ...,
                   have_header: list[bool] | bool = ..., value_mapper: "ValueMapper" = ...) -> "MultiSheetResult": ...


def open_xls_multi(
    filepath: str,
    sheet_indices: list[int] = (0,),
    sheet_names: list[str] | None = None,
    start_at_row: list[int] | int = 0,
    have_header: list[bool] | bool = True,
    value_mapper: "ValueMapper" = identity,
) -> "MultiSheetResult":
    wb: "Workbook" = openpyxl.load_workbook(filepath)
    if sheet_names is not None:
        sheet_indices = [wb.sheetnames.index(sheet_name) for sheet_name in sheet_names]
    for si in sheet_indices:
        sh: "Worksheet" = wb.worksheets[si]
        start_at_row = start_at_row if isinstance(start_at_row, int) else start_at_row[si]
        have_header = have_header if isinstance(have_header, bool) else have_header[si]
        yield (
            si,
            _read_worksheet(sh, start_at_row=start_at_row, has_header=have_header, value_mapper=value_mapper),
        )


def open_csv(
    filepath: str,
    *,
    start_at_row: int = 0,
    has_header: bool = False,
    value_mapper: "ValueMapper" = identity,
) -> "SheetResult":
    with open(filepath) as f:
        if has_header:
            reader = csv.DictReader(f)
            reader = islice(reader, start_at_row, None)
            for row in reader:
                yield {k: value_mapper(v) for k, v in row.items()}
        else:
            reader = csv.reader(f)
            reader = islice(reader, start_at_row, None)
            for row in reader:
                field_names = [f"column{d + 1}" for d in range(len(row))]
                yield dict(zip(field_names, map(value_mapper, row), strict=True))
