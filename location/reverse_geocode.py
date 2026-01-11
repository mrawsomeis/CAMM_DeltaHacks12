import requests

def reverse_geocode(lat: float, lng: float) -> str | None:
    """
    Reverse geocode using OpenStreetMap Nominatim.
    No API key required.
    """
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "format": "jsonv2",
            "lat": lat,
            "lon": lng
        }

        headers = {
            "User-Agent": "CommunityAlertSystem/1.0 (hackathon project)"
        }

        res = requests.get(url, params=params, headers=headers, timeout=5)
        res.raise_for_status()

        data = res.json()
        return data.get("display_name")

    except Exception as e:
        print("Reverse geocoding failed:", e)
        return None


