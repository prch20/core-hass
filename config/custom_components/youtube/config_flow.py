# # custom_components/youtube/config_flow.py
# import voluptuous as vol
# from homeassistant.config_entries import ConfigFlow

# from .const import CONF_API_KEY, CONF_CHANNEL_ID

# class YoutubeFlowHandler(ConfigFlow):
#     async def async_step_user(self, user_input=None):
#         if user_input is None:
#             # Show the form to the user to enter their YouTube API key and channel ID
#             return self.async_show_form(
#                 step_id="user",
#                 data_schema=vol.Schema({
#                     vol.Required(CONF_API_KEY): str,
#                     vol.Required(CONF_CHANNEL_ID): str,
#                 })
#             )

#         # Validate the user input
#         api_key = user_input[CONF_API_KEY]
#         channel_id = user_input[CONF_CHANNEL_ID]
#         try:
#             # Perform any necessary validation or verification here
#             # For example, you could use the requests library to make a request to the YouTube API
#             # and check the response to ensure the API key and channel ID are valid
#             pass
#         except ValueError as error:
#             # Handle any errors that occurred during validation
#             self.errors[CONF_API_KEY] = error

#         # Create the entry in the Home Assistant configuration
#         return self.async_create_entry(title="YouTube", data=user_input)

# def register_flow_handler(hass):
#     ConfigFlow.async_register(
#         "youtube", "youtube", YoutubeFlowHandler
#     )

import logging

import voluptuous as vol

from homeassistant import config_entries, core
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .const import CONF_API_KEY, CONF_CHANNEL_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_CHANNEL_ID): cv.string,
    }
)


class YoutubeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Youtube Custom config flow."""

    # data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input=None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            try:
                # write validation for checking valid input here
                pass
            except ValueError:
                errors["base"] = "invalid input"
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                # User is done adding repos, create the config entry.
                return self.async_create_entry(title="Youtube", data=self.data)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
