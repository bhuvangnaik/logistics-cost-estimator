# Logistics Trip Cost Estimator

A Streamlit-based logistics analytics dashboard that estimates the total transportation cost between two locations.

## Features

- Route distance and travel time estimation
- Fuel consumption calculation
- Vehicle-based toll estimation
- Operational cost modeling
- Logistics KPIs
- Cost breakdown visualizations

## Inputs

- Origin and destination
- Vehicle type
- Fuel type
- Vehicle mileage
- Cargo weight
- Driver cost
- Labor cost
- Insurance cost
- Maintenance cost

## Outputs

- Total trip cost
- Distance and travel time
- Fuel cost
- Toll cost
- Operational cost
- Logistics KPIs (cost/km, cost/ton, cost/ton-km)
- Cost distribution charts

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- OpenStreetMap (Nominatim)
- OSRM Routing Engine

## Run Locally

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py