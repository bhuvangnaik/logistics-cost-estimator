import requests


def get_coordinates(city):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "logistics-cost-estimator"
    }

    response = requests.get(url, params=params, headers=headers)

    data = response.json()

    if len(data) == 0:
        raise Exception("Location not found")

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    return lon, lat


def get_route_details(origin, destination):

    origin_lon, origin_lat = get_coordinates(origin)
    dest_lon, dest_lat = get_coordinates(destination)

    url = f"https://router.project-osrm.org/route/v1/driving/{origin_lon},{origin_lat};{dest_lon},{dest_lat}?overview=false"

    response = requests.get(url)

    data = response.json()

    distance_km = data["routes"][0]["distance"] / 1000
    duration_hours = data["routes"][0]["duration"] / 3600

    return distance_km, duration_hours