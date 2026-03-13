import requests


def get_fuel_price(fuel_type):

    try:

        url = "https://api.fuelsapi.com/price"

        response = requests.get(url)

        data = response.json()

        if fuel_type == "Petrol":
            return data["petrol"]

        elif fuel_type == "Diesel":
            return data["diesel"]

    except:

        # fallback prices if API fails
        fallback_prices = {
            "Petrol": 103,
            "Diesel": 94
        }

        return fallback_prices[fuel_type]