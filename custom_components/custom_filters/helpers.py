import pkgutil
import importlib
from inspect import getmembers, isfunction
import logging
from .const import (
    LOGGER_PATH,
)

_LOGGER = logging.getLogger(LOGGER_PATH)


def _find_modules(package_path):
    """Find all modules in the specified package"""

    _LOGGER.debug("Scanning %s...", package_path)
    all_modules = pkgutil.iter_modules([package_path])

    for _, module_name, _ in all_modules:
        yield module_name


def _import_module(package_path, module_name):
    """Import the specified module from the specified package"""

    _LOGGER.debug("Importing %s...", module_name)
    try:
        module = importlib.import_module(f"{package_path}.{module_name}")
        _LOGGER.debug("Successfully imported %s.", module_name)
        return module

    except Exception:
        _LOGGER.error(
            "Failed to import %s.",
            module_name,
            exc_info=True,
        )
        return None


def _import_functions(module):
    """Import all functions from the provided module"""

    _LOGGER.debug("Importing functions from %s...", module.__name__)
    try:
        functions = getmembers(module, isfunction)
        _LOGGER.debug(
            "Successfully imported %s functions from %s.",
            len(functions),
            module.__name__,
        )
        for _, func in functions:
            yield func

    except Exception:
        _LOGGER.error(
            "Failed to import functions from %s.",
            module.__name__,
            exc_info=True,
        )
        return []


def refresh_filters(package_path, env):
    """Refresh the custom filters in the specified environment"""

    # Find all modules in the specified path
    module_names = list(_find_modules(package_path))
    _LOGGER.debug("Found %s modules.", len(module_names))

    # Find all functions in the specified modules
    filters = []
    for module_name in module_names:
        module = _import_module(package_path, module_name)

        if module is None:
            continue

        functions = list(_import_functions(module))
        filters.extend(functions)

    _LOGGER.debug("Attaching custom filters to environment...")
    # Attach the filters to the environment
    for filter in filters:
        env.globals[filter.__name__] = filter
        env.filters[filter.__name__] = filter
    _LOGGER.info("Successfully loaded %s custom filters.", len(filters))
