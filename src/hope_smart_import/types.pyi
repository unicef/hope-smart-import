from typing import Any, Iterable

RowResult = dict[str, str]
SheetResult = Iterable[RowResult]
MultiSheetResult = Iterable[SheetResult]
