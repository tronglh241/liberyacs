import pytest
from cases.case import Case
from cases.config import (FileNotFoundCase, LackOfKeyExtralibCase, NotEvalCase,
                          RegularCase, UnwantedKeyExtralibCase)


@pytest.mark.parametrize(
    'case', [
        FileNotFoundCase,
        RegularCase,
        NotEvalCase,
        LackOfKeyExtralibCase,
        UnwantedKeyExtralibCase,
    ]
)
def test_cfgnode_load(case: Case) -> None:
    case().check()
