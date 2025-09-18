import requests

from models.location import Location


def fetch_location(ip: str) -> Location:

    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    return Location(
        ip=ip,
        city=data.get("city", "Unknown"),
        state=data.get("region", "Unknown"),
        lang=data.get("languages", "Unknown"),
    )
