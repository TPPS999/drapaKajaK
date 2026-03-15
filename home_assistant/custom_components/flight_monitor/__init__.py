"""Flight Monitor — track Kayak flight prices in Home Assistant."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_FLIGHT_NAME, CONF_KAYAK_URL, CONF_SCAN_INTERVAL, DOMAIN
from .coordinator import FlightCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a monitored flight from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Support options flow overriding scan_interval
    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, 30)
    )

    coordinator = FlightCoordinator(
        hass,
        flight_name=entry.data[CONF_FLIGHT_NAME],
        kayak_url=entry.data[CONF_KAYAK_URL],
        scan_interval=scan_interval,
    )

    # First refresh — if it raises UpdateFailed, HA will retry automatically.
    # We catch generic exceptions so a network hiccup doesn't block setup entirely.
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as exc:
        raise ConfigEntryNotReady(f"Initial flight scrape failed: {exc}") from exc

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Re-create coordinator when options (e.g. scan_interval) change
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)
