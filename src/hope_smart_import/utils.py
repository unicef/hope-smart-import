from typing import TYPE_CHECKING, Any, Generator

import openpyxl
from hope_flex_fields.models import DataChecker, Fieldset

if TYPE_CHECKING:
    from openpyxl.workbook.workbook import Workbook
    from openpyxl.worksheet.worksheet import Worksheet


def import_simple_xls(filepath: str, sheet_index: int = 0, start_at: int = 0) -> Generator[dict[str, Any], None, None]:
    wb: "Workbook" = openpyxl.load_workbook(filepath)
    sh: "Worksheet" = wb.worksheets[sheet_index]
    rows = sh.rows
    headers = [str(cell.value) for cell in next(rows)]
    for i, row in enumerate(rows):
        if i < start_at:
            continue
        yield dict(zip(headers, (cell.value for cell in row)))  # pragma: no branch


def validate_xls(
    filepath: str,
    checker: DataChecker | Fieldset,
    sheet_index: int = 0,
    fail_if_alien: bool = False,
    start_at: int = 0,
) -> Generator[dict[str, Any], None, None]:
    return checker.validate(
        import_simple_xls(filepath, start_at=start_at, sheet_index=sheet_index), fail_if_alien=fail_if_alien
    )


def validate_xls_multi(
    filepath: str,
    checkers: list[DataChecker | Fieldset],
    fail_if_alien: bool = False,
    start_at: int = 0,
) -> dict[str, list[dict[str, Any]]]:
    errors = {}
    for i, checker in enumerate(checkers):
        errors[checker.name] = checker.validate(
            import_simple_xls(filepath, sheet_index=i, start_at=start_at), fail_if_alien=fail_if_alien
        )
    return errors
