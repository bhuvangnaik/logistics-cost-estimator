def calculate_toll(distance_km, vehicle_type):

    toll_rates = {
        "Class 1 - Car/Jeep/Van": 95,
        "Class 2 - LCV / Mini Bus": 155,
        "Class 3 - Truck (2 Axle)": 315,
        "Class 4 - 3 Axle Commercial Vehicle": 495,
        "Class 5 - Multi Axle Vehicle": 495,
        "Class 6 - Oversized Vehicle": 495
    }

    toll_rate = toll_rates.get(vehicle_type, 315)

    # average toll every 100 km
    toll_count = round(distance_km / 100)

    total_toll = toll_count * toll_rate

    return toll_count, toll_rate, total_toll