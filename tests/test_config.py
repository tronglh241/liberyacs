import pytest
from cases.case import Case
from cases.config import FileNotFoundCase, RegularCase


@pytest.mark.parametrize(
    'case', [
        FileNotFoundCase,
        RegularCase,
    ]
)
def test_cfgnode_load(case: Case) -> None:
    case().check()
