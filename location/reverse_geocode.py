import requests

def reverse_geocode(lat: float, lon: float) -> str | None:
    try:
        # Validate input early
        if lat is None or lon is None:
            return None

        lat = float(lat)
        lon = float(lon)

        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "format": "jsonv2",
            "lat": lat,
            "lon": lon,
            "zoom": 18,
            "addressdetails": 1,
            "email": "your-email@example.com"  # REQUIRED by policy
        }

        headers = {
            "User-Agent": "CommunityAlertSystem/1.0 (contact: your-email@example.com)"
        }

        res = requests.get(url, params=params, headers=headers, timeout=5)
        res.raise_for_status()

        data = res.json()
        return data.get("display_name")

    except Exception as e:
        print("Reverse geocoding failed:", e)
        return None



