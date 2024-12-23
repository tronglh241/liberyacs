import pytest
from cases.case import Case
from cases.config import FileNotFoundCase, NotEvalCase, RegularCase


@pytest.mark.parametrize(
    'case', [
        FileNotFoundCase,
        RegularCase,
        NotEvalCase,
    ]
)
def test_cfgnode_load(case: Case) -> None:
    case().check()
