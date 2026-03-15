"""Config flow for Flight Monitor — add/remove flights via Kayak URL."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_FLIGHT_NAME,
    CONF_KAYAK_URL,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_FLIGHTS,
)
from .scraper import parse_kayak_url


class FlightMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle adding a new monitored flight."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> config_entries.FlowResult:
        errors: dict[str, str] = {}

        # Check global flight limit
        existing = self.hass.config_entries.async_entries(DOMAIN)
        if len(existing) >= MAX_FLIGHTS:
            return self.async_abort(reason="max_flights_reached")

        if user_input is not None:
            url = user_input[CONF_KAYAK_URL].strip()
            flight_info = parse_kayak_url(url)

            if flight_info is None:
                errors[CONF_KAYAK_URL] = "invalid_url"
            else:
                name = user_input.get(CONF_FLIGHT_NAME, "").strip()
                if not name:
                    name = (
                        f"{flight_info.origin}→{flight_info.destination} "
                        f"{flight_info.departure_date}/{flight_info.return_date}"
                    )

                # Prevent duplicate URLs
                await self.async_set_unique_id(url)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_KAYAK_URL: url,
                        CONF_FLIGHT_NAME: name,
                        CONF_SCAN_INTERVAL: user_input.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_KAYAK_URL): str,
                    vol.Optional(CONF_FLIGHT_NAME, default=""): str,
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=1440)),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> FlightMonitorOptionsFlow:
        return FlightMonitorOptionsFlow(config_entry)


class FlightMonitorOptionsFlow(config_entries.OptionsFlow):
    """Allow changing scan interval after initial setup."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> config_entries.FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self._entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_SCAN_INTERVAL, default=current_interval): vol.All(
                        vol.Coerce(int), vol.Range(min=5, max=1440)
                    ),
                }
            ),
        )
