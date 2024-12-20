import pytest
from cases.case import Case
from cases.config import (FileNotFoundCase, LackOfKeyExtralibCase, NotEvalCase,
                          RegularCase, UnwantedKeyExtralibCase)

from liberyacs import CfgNode


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


def test_dict_assignment() -> None:
    cfg = CfgNode()
    cfg.key1 = {
        'key2': {
            'key3': 123,
        }
    }

    assert cfg.key1.key2.key3 == 123
