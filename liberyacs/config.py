from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any, Union

from yacs.config import CfgNode as _CfgNode

# Special keys used for dynamic configuration evaluation
EXTRALIBS = 'extralibs'
MODULE = 'module'
NAME = 'name'
KWARGS = 'kwargs'


class CfgNode(_CfgNode):
    '''
    A subclass of yacs.config.CfgNode that adds dynamic evaluation features.
    '''

    @classmethod
    def load(
        cls,
        filepath: Union[str, Path],
        evaluate: bool = True,
    ) -> CfgNode:
        '''
        Loads a configuration from a YAML file and optionally evaluates it.

        Args:
            filepath (str or Path): Path to the YAML configuration file.
            evaluate (bool): Whether to evaluate dynamic elements in the configuration.

        Returns:
            CfgNode: A CfgNode instance with the loaded configuration.
        '''
        # Open and read the YAML file, loading it as a configuration object
        with open(filepath, 'r') as f:
            config = CfgNode.load_cfg(f)

        # Convert dictionary-like elements recursively to CfgNode instances
        config = cls._convert_to_cfg_node(config)

        if evaluate:
            # Evaluate dynamic expressions
            config = config.eval()

        # Ensure the resulting object is of type CfgNode
        assert isinstance(config, CfgNode)
        return config

    @classmethod
    def _convert_to_cfg_node(cls, data: Any) -> Any:
        '''
        Recursively converts dictionary-like objects to instances of CfgNode.

        Args:
            data (Any): Data to be converted.

        Returns:
            Any: Converted data as CfgNode or the same type if not applicable.
        '''
        if isinstance(data, dict):
            # Convert dictionary to CfgNode and recursively convert its values
            cfg_node = cls()
            for key, value in data.items():
                cfg_node[key] = cls._convert_to_cfg_node(value)
            return cfg_node
        elif isinstance(data, list):
            # Recursively convert list elements
            return [cls._convert_to_cfg_node(item) for item in data]
        else:
            # Return the data unchanged if it is not a dict or list
            return data

    def eval(self) -> CfgNode:
        '''
        Evaluates the configuration to resolve dynamic elements such as modules and objects.

        Returns:
            CfgNode: A new evaluated configuration.
        '''
        config = org_config = self.clone()
        extralibs = {}

        # Process the external libraries defined in the configuration
        for alias, lib_info in config.pop(EXTRALIBS, {}).items():
            if isinstance(lib_info, dict):
                # Import a specific object from a module
                module = lib_info.pop(MODULE)
                name = lib_info.pop(NAME)

                if module is None or name is None:
                    raise ValueError(
                        f'`{MODULE}` and `{NAME}` must be both specified in `{EXTRALIBS}`, '
                        f'found {MODULE}: {module}, {NAME}: {name}.'
                    )

                if lib_info:
                    raise ValueError(f'Only {MODULE} and {NAME} are allowed, found {[key for key in lib_info.keys()]}.')

                lib = getattr(import_module(module), name)
            else:
                # Import the entire module
                lib = import_module(lib_info)

            extralibs[alias] = lib  # Store the imported library

        # Evaluate the configuration with the imported libraries
        config = CfgNode._eval(config, extralibs, org_config)

        return config

    @staticmethod
    def _eval(config: Any, global_context: dict, local_context: dict) -> Any:
        '''
        Recursively evaluates the configuration to resolve dynamic values.

        Args:
            config (Any): Configuration object to evaluate.
            global_context (dict): Global context for evaluation (e.g., imported modules).
            local_context (dict): Local context for evaluation (e.g., configuration itself).

        Returns:
            Any: Evaluated configuration object.
        '''
        if isinstance(config, dict):
            initialized = (
                len(config) == 2 and MODULE in config and NAME in config
                or len(config) == 3 and MODULE in config and NAME in config and KWARGS in config
            )

            if initialized:
                # Process dictionary configuration items
                module = config.pop(MODULE, None)
                name = config.pop(NAME, None)

            # Recursively evaluate dictionary values
            for key, value in config.items():
                config[key] = CfgNode._eval(value, global_context, local_context)

            # If both module and name are specified, construct the object with kwargs
            if initialized:
                kwargs = config.pop(KWARGS, {})  # Extract arguments for the callable
                config = eval(name, {}, vars(import_module(module)))(**kwargs)
            elif not isinstance(config, CfgNode):
                # Convert the dict back to a CfgNode if it is not already
                config = CfgNode(config)

        elif isinstance(config, (list, tuple)):
            # Recursively evaluate list or tuple items
            config = type(config)(map(lambda ele: CfgNode._eval(ele, global_context, local_context), config))

        elif isinstance(config, str):
            # Evaluate strings as expressions
            config = eval(config, global_context, local_context)

            # If the result is not a string, evaluate it further
            if not isinstance(config, str):
                config = CfgNode._eval(config, global_context, local_context)

        return config
