"""Sensor entity for a monitored flight."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_DEPARTURE,
    ATTR_DESTINATION,
    ATTR_ERROR,
    ATTR_LAST_CHECKED,
    ATTR_MIN_PRICE,
    ATTR_ORIGIN,
    ATTR_PASSENGERS,
    ATTR_RETURN,
    ATTR_ROUTE,
    ATTR_STATUS,
    ATTR_TOTAL_PRICE,
    ATTR_URL,
    CONF_FLIGHT_NAME,
    DOMAIN,
)
from .coordinator import FlightCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: FlightCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([FlightPriceSensor(coordinator, entry)])


class FlightPriceSensor(CoordinatorEntity[FlightCoordinator], SensorEntity):
    """Single sensor representing the current cheapest price for one flight."""

    _attr_native_unit_of_measurement = "PLN"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:airplane"

    def __init__(self, coordinator: FlightCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_price"
        self._attr_name = entry.data[CONF_FLIGHT_NAME]

    @property
    def native_value(self) -> float | None:
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("price")

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data or {}
        fi = self.coordinator.flight_info

        attrs: dict = {
            ATTR_URL: self.coordinator.kayak_url,
            ATTR_MIN_PRICE: self.coordinator.min_price,
            ATTR_TOTAL_PRICE: data.get("total_price"),
            ATTR_STATUS: data.get("status", "unknown"),
            ATTR_LAST_CHECKED: self.coordinator.last_checked,
        }

        if fi:
            attrs[ATTR_ROUTE] = fi.route
            attrs[ATTR_ORIGIN] = fi.origin
            attrs[ATTR_DESTINATION] = fi.destination
            attrs[ATTR_DEPARTURE] = fi.departure_date
            attrs[ATTR_RETURN] = fi.return_date
            attrs[ATTR_PASSENGERS] = fi.passengers

        if data.get("error"):
            attrs[ATTR_ERROR] = data["error"]

        return attrs

    @property
    def available(self) -> bool:
        # Sensor is available even when scraping errors out (keeps last price)
        return self.coordinator.last_updated is not None
