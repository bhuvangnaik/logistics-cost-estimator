import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import plotly.express as px
import pandas as pd

from services.route_service import get_route_details
from modules.fuel_engine import calculate_fuel, calculate_fuel_cost
from modules.toll_engine import calculate_toll


# Page configuration
st.set_page_config(
    page_title="Logistics Trip Cost Estimator A-B",
    page_icon="🚚",
    layout="wide"
)

# Title
st.title("🚚 Logistics Trip Cost Estimator A-B")

st.markdown("""
This tool estimates the **total logistics cost of a trip** based on route,
vehicle details, and operational expenses.
""")

st.divider()


# INPUT SECTION
st.header("Trip Input Details")

col1, col2 = st.columns(2)

with col1:

    origin = st.text_input("Location A (Origin)", placeholder="Example: Mumbai")

    destination = st.text_input("Location B (Destination)", placeholder="Example: Delhi")

    vehicle_type = st.selectbox(
        "Vehicle Type",
        [
            "Class 1 - Car/Jeep/Van",
            "Class 2 - LCV / Mini Bus",
            "Class 3 - Truck (2 Axle)",
            "Class 4 - 3 Axle Commercial Vehicle",
            "Class 5 - Multi Axle Vehicle",
            "Class 6 - Oversized Vehicle"
        ]
    )

    fuel_type = st.selectbox(
        "Fuel Type",
        ["Petrol", "Diesel"]
    )

    mileage = st.number_input(
        "Vehicle Mileage (km per liter)",
        min_value=1.0,
        value=4.0
    )

with col2:

    cargo_weight = st.number_input(
        "Cargo Weight (tons)",
        min_value=0.0,
        value=10.0
    )

    driver_cost = st.number_input(
        "Driver Cost",
        min_value=0,
        value=1500
    )

    labor_cost = st.number_input(
        "Labor Cost",
        min_value=0,
        value=1000
    )

    insurance_cost = st.number_input(
        "Insurance Cost per Trip",
        min_value=0,
        value=500
    )

    maintenance_cost = st.number_input(
        "Maintenance Cost per Trip",
        min_value=0,
        value=3000
    )

st.divider()


# BUTTON ACTION
if st.button("Calculate Trip Cost"):

    if origin and destination:

        try:

            # ROUTE INFORMATION
            distance, duration = get_route_details(origin, destination)

            hours = int(duration)
            minutes = int((duration - hours) * 60)

            # FUEL CALCULATIONS
            fuel_required = calculate_fuel(distance, mileage)
            fuel_price, fuel_cost = calculate_fuel_cost(fuel_required, fuel_type)

            # TOLL CALCULATION
            toll_count, toll_rate, toll_cost = calculate_toll(distance, vehicle_type)

            # OPERATIONAL COSTS
            operational_total = (
                driver_cost +
                labor_cost +
                insurance_cost +
                maintenance_cost
            )

            # TOTAL COST
            total_cost = fuel_cost + toll_cost + operational_total

            # KPI CALCULATIONS
            cost_per_km = total_cost / distance

            if cargo_weight > 0:
                cost_per_ton = total_cost / cargo_weight
                cost_per_ton_km = total_cost / (cargo_weight * distance)
            else:
                cost_per_ton = 0
                cost_per_ton_km = 0


            # ROUTE INFO DISPLAY
            st.subheader("📍 Route Information")

            c1, c2, c3 = st.columns(3)

            c1.metric("Distance", f"{distance:.2f} km")
            c2.metric("Travel Time", f"{hours}h {minutes}m")
            c3.metric("Fuel Required", f"{fuel_required:.2f} L")

            st.divider()


            # FUEL SECTION
            st.subheader("⛽ Fuel Analysis")

            f1, f2, f3 = st.columns(3)

            f1.metric("Fuel Type", fuel_type)
            f2.metric("Fuel Price", f"₹{fuel_price}/L")
            f3.metric("Fuel Cost", f"₹{fuel_cost:,.2f}")

            st.divider()


            # TOLL SECTION
            st.subheader("🛣 Toll Analysis")

            t1, t2, t3 = st.columns(3)

            t1.metric("Estimated Toll Plazas", toll_count)
            t2.metric("Average Toll / Plaza", f"₹{toll_rate}")
            t3.metric("Total Toll Cost", f"₹{toll_cost}")

            st.divider()


            # OPERATIONAL COSTS
            st.subheader("⚙ Operational Costs")

            o1, o2, o3, o4 = st.columns(4)

            o1.metric("Driver Cost", f"₹{driver_cost}")
            o2.metric("Labor Cost", f"₹{labor_cost}")
            o3.metric("Insurance", f"₹{insurance_cost}")
            o4.metric("Maintenance", f"₹{maintenance_cost}")

            st.divider()


            # TOTAL COST
            st.subheader("💰 Trip Cost Summary")

            st.metric(
                "Total Estimated Trip Cost",
                f"₹{total_cost:,.2f}"
            )


            # KPI DASHBOARD
            st.divider()
            st.subheader("📊 Logistics KPIs")

            k1, k2, k3 = st.columns(3)

            k1.metric("Cost per km", f"₹{cost_per_km:.2f}")
            k2.metric("Cost per ton", f"₹{cost_per_ton:.2f}")
            k3.metric("Cost per ton-km", f"₹{cost_per_ton_km:.4f}")


            # VISUALIZATION DATA
            cost_data = {
                "Category": ["Fuel Cost", "Toll Cost", "Operational Cost"],
                "Amount": [fuel_cost, toll_cost, operational_total]
            }

            df_cost = pd.DataFrame(cost_data)


            # PIE CHART
            st.divider()
            st.subheader("📊 Cost Breakdown Visualization")

            pie_chart = px.pie(
                df_cost,
                names="Category",
                values="Amount",
                title="Trip Cost Distribution",
                hole=0.4
            )

            st.plotly_chart(pie_chart, use_container_width=True)


            # BAR CHART
            bar_chart = px.bar(
                df_cost,
                x="Category",
                y="Amount",
                text="Amount",
                title="Cost Comparison",
                color="Category"
            )

            st.plotly_chart(bar_chart, use_container_width=True)


        except Exception as e:
            st.error(f"Error calculating route: {e}")

    else:
        st.error("Please enter both origin and destination.")