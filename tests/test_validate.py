# mypy: disable-error-code="no-untyped-def"
from pathlib import Path
from typing import Any

import pytest

from demo.factories import FieldsetFactory, FlexFieldFactory
from hope_flex_fields.models import Fieldset

from hope_smart_import.utils import validate_xls


@pytest.fixture()
def xls_simple() -> str:
    return str((Path(__file__).parent / "data" / "simple1.xlsx").absolute())


@pytest.fixture()
def simple_validator(db: Any) -> Fieldset:
    fs = FieldsetFactory()
    FlexFieldFactory(name="name", fieldset=fs)
    FlexFieldFactory(name="last_name", fieldset=fs)
    return fs


def test_validate_simple(xls_simple: str, simple_validator: Fieldset):
    errors = validate_xls(xls_simple, simple_validator, fail_if_alien=False)
    assert not errors

    errors = validate_xls(xls_simple, simple_validator, fail_if_alien=True)
    assert errors == {1: {"-": ["Alien values found {'gender'}"]}, 2: {"-": ["Alien values found {'gender'}"]}}
