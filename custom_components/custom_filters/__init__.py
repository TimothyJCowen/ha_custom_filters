from homeassistant.const import (
    SERVICE_RELOAD,
)
from homeassistant.helpers import (
    template as hass_template,
)
import logging
from .const import (
    DOMAIN,
    FOLDER,
    LOGGER_PATH,
)
from .helpers import (
    refresh_filters,
)

_LOGGER = logging.getLogger(LOGGER_PATH)


async def async_setup(hass, hass_config):
    """Entrypoint to set up the component."""
    # There is nothing to do here, as the setup is done when the config entry is set up
    return True


async def async_setup_entry(hass, config_entry):
    """Entrypoint to set up the config entry."""

    hass.data.setdefault(DOMAIN, {})

    # Define the reload service
    def _reload_scripts_handler(call):
        """Handle reload service calls."""

        try:
            template = hass_template.Template("", hass)
            refresh_filters(FOLDER, template._env)

        except Exception:
            _LOGGER.error("Failed to load filters.", exc_info=True)

    # Register the reload service
    hass.services.async_register(DOMAIN, SERVICE_RELOAD, _reload_scripts_handler)

    # We need to call a synchronous function here, so we use the
    # hass.async_add_executor_job to handle that
    try:
        template = hass_template.Template("", hass)
        await hass.async_add_executor_job(refresh_filters, FOLDER, template._env)

    except Exception as ex:
        _LOGGER.error("Failed to load filters. %s", ex, exc_info=True)

    return True


# https://github.com/home-assistant/core/blob/baceb2a92ac6e0cb70639195c3ea205a378551ac/homeassistant/helpers/template.py#L2747
# A reference to the actual TemplateEnvironment class
_TEMPLATE_ENV_SUPER = hass_template.TemplateEnvironment


# Constructs a new TemplateEnvironment with custom filters
def _custom_template_environment_init(*args):
    """Initialize a new TemplateEnvironment with custom filters"""

    # Create a new environment and add all custom filters
    env = _TEMPLATE_ENV_SUPER(*args)
    refresh_filters(FOLDER, env)

    # Return the environment
    return env


# Override the TemplateEnvironment class with our custom implementation
hass_template.TemplateEnvironment = _custom_template_environment_init
