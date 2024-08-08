from homeassistant import config_entries
from .const import (
    DOMAIN,
)


class CompConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    # The version of the configuration schema.
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user step."""
        return self.async_create_entry(
            title="Custom Template Filters",
            data={},
        )
