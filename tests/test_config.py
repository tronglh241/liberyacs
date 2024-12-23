import pytest
from pathlib import Path
from liberyacs import CfgNode


@pytest.mark.parametrize(
    'filepath, evaluate', [
        ('tests/configs/simple.yaml', True),
        ('tests/configs/simple.yaml', False),
        ('tests/configs/complex.yaml', True),
        ('tests/configs/complex.yaml', False),
    ]
)
def test_cfgnode_load(filepath, evaluate):
    '''
    Test the CfgNode.load method with different configurations.

    Args:
        filepath (str): Path to the configuration file.
        evaluate (bool): Whether to evaluate the configuration dynamically.
    '''
    # Ensure the filepath exists
    config_path = Path(filepath)
    assert config_path.exists(), f'Config file {filepath} does not exist.'

    # Load the configuration
    cfg = CfgNode.load(filepath=config_path, evaluate=evaluate)

    # Check that the result is a CfgNode instance
    assert isinstance(cfg, CfgNode), 'Loaded config is not a CfgNode instance.'

    # Optionally, perform specific checks based on the content of the configuration
    if evaluate:
        # Add assertions for evaluated configurations if applicable
        assert '_module_' not in cfg, 'Dynamic keys should be resolved during evaluation.'
    else:
        # Ensure the original structure is preserved without evaluation
        assert '_module_' in cfg, 'Dynamic keys should not be resolved without evaluation.'
