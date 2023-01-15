import logging

import requests
import voluptuous as vol

from homeassistant import config_entries, core
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

from .const import CONF_API_KEY, CONF_CHANNEL_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_YOUTUBE_DATA_API = "https://www.googleapis.com/youtube/v3/channels"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_API_KEY): cv.string, vol.Required(CONF_CHANNEL_ID): cv.string}
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the YouTube sensor."""
    api_key = config.get(CONF_API_KEY)
    channel_id = config.get(CONF_CHANNEL_ID)

    add_entities([YoutubeSensor(api_key, channel_id)], True)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    session = async_create_clientsession(hass)

    async_add_entities(
        [YoutubeSensor(config[CONF_API_KEY], config[CONF_CHANNEL_ID])],
        update_before_add=True,
    )


class YoutubeSensor(Entity):
    """Representation of a YouTube sensor."""

    def __init__(self, api_key, channel_id):
        """Initialize the sensor."""
        self._api_key = api_key
        self._channel_id = channel_id
        self._state = None
        self.views = None
        self.video_count = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Youtube Subscriber Count"

    @property
    def icon(self):
        """Icon."""
        return "mdi:account-multiple"

    @property
    def scan_interval(self):
        """Return the scan interval."""
        return 10

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return unique ID for this sensor."""
        return self._channel_id

    @property
    def extra_state_attributes(self):
        """Attributes."""
        return {"views": self.views, "video Count": self.video_count}

    def update(self):

        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        params = {"part": "statistics", "id": self._channel_id, "key": self._api_key}
        try:
            response = requests.get(CONF_YOUTUBE_DATA_API, params=params)
            response.raise_for_status()
            data = response.json()
            self._state = data["items"][0]["statistics"]["subscriberCount"]
            self.views = data["items"][0]["statistics"]["viewCount"]
            self.video_count = data["items"][0]["statistics"]["videoCount"]
            _LOGGER.debug("UPDATED Stats")

        except requests.exceptions.RequestException as error:
            self._state = error

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.hass.async_create_task(self.async_update_interval())

    async def async_update_interval(self):
        await self.async_update()
        while True:
            await asyncio.sleep(10)
            await self.async_update()
