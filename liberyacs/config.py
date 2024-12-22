from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any, Union

from yacs.config import CfgNode as _CfgNode

EXTRALIBS = '_extralibs_'
MODULE = '_module_'
NAME = '_name_'
KWARGS = '_kwargs_'


class CfgNode(_CfgNode):
    @classmethod
    def load(cls, filepath: Union[str, Path]) -> CfgNode:
        '''
        Loads a configuration from a YAML file and converts dictionary-like objects
        recursively to instances of CfgNode.

        Args:
            filepath (str or Path): Path to the YAML configuration file.

        Returns:
            CfgNode: A CfgNode instance with loaded configuration.
        '''
        # Load the YAML file
        with open(filepath, 'r') as f:
            config_data = CfgNode.load_cfg(f)

        # Recursively convert dict-like objects to CfgNode instances
        config = cls._convert_to_cfg_node(config_data)

        assert isinstance(config, CfgNode)
        return config

    @classmethod
    def _convert_to_cfg_node(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Convert dictionary to CfgNode and recursively process each item
            cfg_node = cls()
            for key, value in data.items():
                cfg_node[key] = cls._convert_to_cfg_node(value)
            return cfg_node
        elif isinstance(data, list):
            # Recursively process each item in a list
            return [cls._convert_to_cfg_node(item) for item in data]
        else:
            # Return the item if it is not a dict or list
            return data

    def eval(self) -> CfgNode:
        config = org_config = self.clone()
        extralibs = {}

        for alias, lib_info in config.pop(EXTRALIBS, {}).items():
            if isinstance(lib_info, dict):
                module = lib_info[MODULE]
                name = lib_info[NAME]
                lib = getattr(import_module(module), name)
            else:
                lib = import_module(lib_info)

            extralibs[alias] = lib

        config = CfgNode._eval(config, extralibs, org_config)

        return config

    @staticmethod
    def _eval(config: Any, global_context: dict, local_context: dict) -> Any:
        if isinstance(config, dict):
            module = config.pop(MODULE)
            name = config.pop(NAME)

            for key, value in config.items():
                config[key] = CfgNode._eval(value, global_context, local_context)

            if module is not None and name is not None:
                kwargs = config.pop(KWARGS, {})
                config = eval(name, {}, vars(import_module(module)))(**kwargs)
            elif not isinstance(config, CfgNode):
                config = CfgNode(config)

        elif isinstance(config, (list, tuple)):
            config = type(config)(map(lambda ele: CfgNode._eval(ele, global_context, local_context), config))

        elif isinstance(config, str):
            config = eval(config, global_context, local_context)

        return config
