import os
import requests
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Base URLs
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


def build_geocode_url(address: str, limit: int = 1, types: str = "place,poi") -> str:
    """
    Returns a properly encoded Mapbox Geocoding API URL for the given address.

    :param address: The place name or street address to geocode.
    :param limit:   Maximum number of results to return (default: 1).
    :param types:   Comma-separated feature types to filter (default: "place,poi").
    """
    if not MAPBOX_TOKEN:
        raise RuntimeError("MAPBOX_TOKEN not set in environment variables")
    # URL-encode the address
    encoded = quote_plus(address)
    # Build and return the full request URL
    return (
        f"{MAPBOX_BASE_URL}/{encoded}.json"
        f"?access_token={MAPBOX_TOKEN}"
        f"&limit={limit}"
        f"&types={types}"
    )


def geocode(address: str) -> tuple[float, float]:
    """
    Convert an address or place name into latitude and longitude using Mapbox Geocoding API.

    Args:
        address: The address or place name to geocode.

    Returns:
        A tuple (latitude, longitude).

    Raises:
        RuntimeError: If the API request fails or no result is found.
    """
    # Build the Mapbox geocoding URL
    url = build_geocode_url(address)

    resp = requests.get(url)
    resp.raise_for_status()

    data = resp.json()
    features = data.get("features", [])
    if not features:
        raise RuntimeError(f"No geocoding result for address: {address}")

    coords = features[0]["center"]  # [lon, lat]
    lon, lat = coords[0], coords[1]
    return lat, lon


def get_nearest_stop(lat: float, lon: float) -> tuple[str, bool]:
    """
    Find the nearest MBTA stop to the given coordinates.

    Args:
        lat: Latitude of the location.
        lon: Longitude of the location.

    Returns:
        A tuple (stop_name, wheelchair_accessible).
        wheelchair_accessible is True if accessible, False otherwise.

    Raises:
        RuntimeError: If the API request fails or no stop is found.
    """
    if not MBTA_API_KEY:
        raise RuntimeError("MBTA_API_KEY not found in environment variables")

    params = {
        "api_key": MBTA_API_KEY,
        "filter[latitude]": lat,
        "filter[longitude]": lon,
        "sort": "distance",
        "page[limit]": 1
    }
    resp = requests.get(MBTA_BASE_URL, params=params)
    resp.raise_for_status()

    data = resp.json()
    stops = data.get("data", [])
    if not stops:
        raise RuntimeError(f"No MBTA stops found near ({lat}, {lon})")

    stop = stops[0]
    name = stop.get("attributes", {}).get("name", "Unknown")
    wheelchair_code = stop.get("attributes", {}).get("wheelchair_boarding", 0)
    # wheelchair_boarding codes: 0 = unknown, 1 = accessible, 2 = not accessible
    accessible = wheelchair_code == 1
    return name, accessible


def find_stop_near(place: str) -> str:
    """
    For a given address or place name, return the nearest MBTA stop and whether it is wheelchair accessible.

    Args:
        place: The address or place name to search.

    Returns:
        A formatted string: "<Stop Name> (Wheelchair Accessible: Yes/No)"
    """
    lat, lon = geocode(place)
    stop_name, accessible = get_nearest_stop(lat, lon)
    access_str = "Yes" if accessible else "No"
    return f"{stop_name} (Wheelchair Accessible: {access_str})"


if __name__ == "__main__":
    # Quick test
    try:
        place = input("Enter a place or address: ")
        print("Mapbox geocode URL:", build_geocode_url(place))
        result = find_stop_near(place)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
