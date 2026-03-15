"""Constants for Flight Monitor integration."""

DOMAIN = "flight_monitor"
MAX_FLIGHTS = 100
DEFAULT_SCAN_INTERVAL = 30  # minutes

# Config entry keys
CONF_KAYAK_URL = "kayak_url"
CONF_FLIGHT_NAME = "flight_name"
CONF_SCAN_INTERVAL = "scan_interval"

# Entity attribute keys
ATTR_MIN_PRICE = "min_price"
ATTR_TOTAL_PRICE = "total_price"
ATTR_ROUTE = "route"
ATTR_DEPARTURE = "departure_date"
ATTR_RETURN = "return_date"
ATTR_PASSENGERS = "passengers"
ATTR_URL = "url"
ATTR_LAST_CHECKED = "last_checked"
ATTR_STATUS = "status"
ATTR_ERROR = "error"
ATTR_ORIGIN = "origin"
ATTR_DESTINATION = "destination"
