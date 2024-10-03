from typing import TYPE_CHECKING, Any, Generator

import openpyxl
from hope_flex_fields.models import DataChecker, Fieldset

if TYPE_CHECKING:
    from openpyxl.workbook.workbook import Workbook
    from openpyxl.worksheet.worksheet import Worksheet


def import_simple_xls(filepath: str) -> Generator[dict[str, Any], None, None]:
    wb: "Workbook" = openpyxl.load_workbook(filepath)
    sh: "Worksheet" = wb.worksheets[0]
    rows = sh.rows
    headers = [str(cell.value) for cell in next(rows)]
    for row in rows:
        yield dict(zip(headers, (cell.value for cell in row)))


def validate_xls(
    filepath: str, checker: DataChecker | Fieldset, fail_if_alien: bool = False
) -> Generator[dict[str, Any], None, None]:
    return checker.validate(import_simple_xls(filepath), fail_if_alien=fail_if_alien)
