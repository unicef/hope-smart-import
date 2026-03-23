from __future__ import annotations

from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from collections.abc import Generator
    from hope_flex_fields.models import DataChecker, Fieldset
    from hope_flex_fields.models.base import ValidatorMixin
    from .types import MultiSheetResult, SheetResult


def validate_single(
    g: "SheetResult",
    checker: ValidatorMixin,
    *,
    include_success: bool = False,
    fail_if_alien: bool = False,
) -> Generator[dict[str, Any]]:
    return checker.validate(g, include_success=include_success, fail_if_alien=fail_if_alien)


def validate_xls_multi(
    g: "MultiSheetResult",
    checkers: list[DataChecker | Fieldset],
    include_success: bool = False,
    fail_if_alien: bool = False,
) -> dict[str, list[dict[str, Any]]]:
    errors = {}
    for sheet_index, sheet_generator in g:
        checker = checkers[sheet_index]
        errors[f"{sheet_index + 1}:{checker.name}"] = checker.validate(
            sheet_generator,
            include_success=include_success,
            fail_if_alien=fail_if_alien,
        )
    return errors
