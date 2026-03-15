"""DataUpdateCoordinator for a single monitored flight."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .scraper import FlightInfo, ScrapeResult, parse_kayak_url, scrape_price

_LOGGER = logging.getLogger(__name__)


class FlightCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Manages scraping for one monitored flight."""

    def __init__(
        self,
        hass: HomeAssistant,
        flight_name: str,
        kayak_url: str,
        scan_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{flight_name}",
            update_interval=timedelta(minutes=scan_interval),
        )
        self.flight_name = flight_name
        self.kayak_url = kayak_url
        self.flight_info: Optional[FlightInfo] = parse_kayak_url(kayak_url)

        # Persistent across updates
        self.min_price: Optional[float] = None
        self.last_checked: Optional[str] = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch current price. Runs in executor thread via async_add_executor_job."""
        self.last_checked = dt_util.now().isoformat()

        try:
            result: ScrapeResult = await self.hass.async_add_executor_job(
                scrape_price, self.kayak_url
            )
        except Exception as exc:
            raise UpdateFailed(f"Unexpected error scraping {self.kayak_url}: {exc}") from exc

        if result.success and result.price_per_person is not None:
            price = result.price_per_person

            # Track historical minimum
            if self.min_price is None or price < self.min_price:
                self.min_price = price

            return {
                "price": price,
                "total_price": result.total_price,
                "status": "ok",
                "error": None,
                "last_checked": self.last_checked,
            }

        # On error — keep last known price so sensor doesn't become None
        previous_price = self.data.get("price") if self.data else None
        return {
            "price": previous_price,
            "total_price": self.data.get("total_price") if self.data else None,
            "status": "error",
            "error": result.error,
            "last_checked": self.last_checked,
        }
