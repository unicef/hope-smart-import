# mypy: disable-error-code="no-untyped-def"
from pathlib import Path

import pytest

from hope_flex_fields.models import Fieldset

from hope_smart_import.utils import validate_xls

from hope_flex_fields.models.definition import FieldDefinition
from hope_flex_fields.models.flexfield import FlexField
from django import forms


@pytest.fixture()
def xls_simple() -> str:
    return str((Path(__file__).parent / "data" / "simple2.xlsx").absolute())


def test_code_sample(db, xls_simple):
    fs, __ = Fieldset.objects.get_or_create(name="test.xlsx")

    charfield = FieldDefinition.objects.get(field_type=forms.CharField)
    choicefield = FieldDefinition.objects.get(field_type=forms.ChoiceField)

    FlexField.objects.get_or_create(name="name", fieldset=fs, field=charfield)
    FlexField.objects.get_or_create(name="last_name", fieldset=fs, field=charfield)
    FlexField.objects.get_or_create(name="gender", fieldset=fs, field=choicefield,
                                    attrs={"choices": [["M", "M"], ["F", "F"]]})

    errors = validate_xls(xls_simple, fs, fail_if_alien=True)
    assert errors == {3: {'gender': ['Select a valid choice. X is not one of the available choices.']}}
