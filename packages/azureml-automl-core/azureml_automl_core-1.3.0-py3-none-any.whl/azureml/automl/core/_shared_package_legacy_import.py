# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import importlib
import inspect
import os
import pkgutil
import sys
import types
from os.path import dirname
from typing import Any, cast, Iterable


def _add_module_to_current_env(
    name: str,
    module: types.ModuleType
) -> None:
    """Add a module to the current Python environment (and make it importable)."""
    # Add the module to sys.modules
    sys.modules[name] = module

    # Add the child module as a property of the parent module.
    # This is required when using the syntax 'import parent.child'
    last_period_idx = name.rfind('.')
    setattr(
        sys.modules[name[:last_period_idx]],
        name[last_period_idx + 1:],
        module
    )


def _add_stub_modules_for_prefixes_if_not_exist(
    name: str,
    stub_module_init_file_path: str
) -> None:
    """
    When importing a module using the syntax a.b.c.d, all prefixes of the namespace
    ('a', 'a.b', etc.) are required to exist as importable modules. This method adds
    the required prefix modules as stubs in the current Python environment if they don't exist.
    """
    module_chain = name.split('.')[:-1]
    curr = module_chain[0]
    if curr not in sys.modules:
        sys.modules[curr] = _generate_stub_module(curr, stub_module_init_file_path)
    for module in module_chain[1:]:
        prev = curr
        curr = curr + '.' + module
        if curr not in sys.modules:
            sys.modules[curr] = _generate_stub_module(curr, stub_module_init_file_path)
            setattr(sys.modules[prev], module, sys.modules[curr])


def _generate_stub_module(
    name: str,
    stub_module_init_file_path: str
) -> Any:
    loader = importlib.machinery.SourceFileLoader(name, stub_module_init_file_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def _handle_legacy_shared_package_imports() -> None:
    # Note: the code in the 'shared' package is used directly by some AutoML components that live in the
    # Jasmine repo. This shared package used to be importable under different namespaces.
    # For the sake of backwards compatibility (not breaking legacy code still using these imports),
    # we redirect legacy aliases to the 'shared' module they intend to reference.
    legacy_aliases = [
        "automl.client.core.common",
        "azureml.automl.core._vendor.automl.client.core.common",
    ]

    # Find azureml package's init file.
    # (Legacy stub package imports will be redirected to the top-level azureml stub package.)
    azureml_init_file_path = os.path.join(dirname(dirname(dirname(__file__))), "__init__.py")

    from . import shared

    _import_all_legacy_submodules(
        legacy_aliases,
        azureml_init_file_path,
        shared
    )


def _import_all_legacy_submodules(
    legacy_aliases: Iterable[str],
    azureml_init_file_path: str,
    shared_module: types.ModuleType
) -> None:
    for alias in legacy_aliases:
        _add_stub_modules_for_prefixes_if_not_exist(alias, azureml_init_file_path)
        _add_module_to_current_env(alias, shared_module)

    # Explicitly import all submodules of the shared package.
    # This ensures all types are loaded under a single namespace and makes Python
    # type equality work correctly across legacy and non-legacy namespaces.
    packages = [shared_module]
    prefixes = ['.']
    while packages:
        curr_package = packages.pop()
        curr_prefix = prefixes.pop()
        for _, name, ispkg in pkgutil.walk_packages(cast(Any, curr_package).__path__):
            module = pkgutil.importlib.import_module(curr_package.__name__ + '.' + name)
            # If a module did not load properly (perhaps because it requires other modules
            # not yet loaded into memory), scrub it from the module cache so future imports
            # could potentially work.
            if not ispkg and not inspect.getmembers(module, inspect.isclass):
                del sys.modules[curr_package.__name__ + '.' + name]
                delattr(sys.modules[curr_package.__name__], name)
                continue
            for alias in legacy_aliases:
                _add_module_to_current_env(alias + curr_prefix + name, module)
            if ispkg:
                packages.append(module)
                prefixes.append(curr_prefix + name + '.')
