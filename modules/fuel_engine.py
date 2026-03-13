from services.fuel_service import get_fuel_price


def calculate_fuel(distance_km, mileage):

    fuel_required = distance_km / mileage

    return fuel_required


def calculate_fuel_cost(fuel_required, fuel_type):

    fuel_price = get_fuel_price(fuel_type)

    fuel_cost = fuel_required * fuel_price

    return fuel_price, fuel_cost