## Note:

# Call this function upon detection of distress --> /body

# Call reverse_geocode from reverse_geocode.py to get address string

# FRONTEND FOR APP SHOULD HAVE A FILE TO DISPLAY LOCATION INFO
# FROM THIS MODULE ON A MAP VIEW

# Frontend Alert System: Get info from /location/reverse_geocode to
# display "person in disress near {address string}"

# Frontend Alert System: Get info from /moorcheh/generate_alerts to 
# display STATUS + INSTRUCTIONS to community responders.


import requests

def get_laptop_location_ip():
    """
    Approximate laptop location using IP address.
    Suitable fallback for MVP demo.
    """
    try:
        res = requests.get("https://ipapi.co/json/", timeout=3)
        data = res.json()

        return {
            "lat": data.get("latitude"),
            "lng": data.get("longitude"),
            "city": data.get("city"),
            "region": data.get("region"),
            "source": "ip"
        }
    except Exception:
        return None
