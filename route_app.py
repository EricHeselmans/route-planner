import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Laad de .env met je API-key
load_dotenv()
API_KEY = os.getenv("TOMTOM_API_KEY")

def get_route_time(start, end, api_key, via=None):
    base_url = "https://api.tomtom.com/routing/1/calculateRoute/"
    if via:
        points = f"{start}:{via}:{end}"
    else:
        points = f"{start}:{end}"

    params = {
        "key": api_key,
        "traffic": "true",
        "travelMode": "car",
        "routeType": "fastest"
    }

    response = requests.get(base_url + points + "/json", params=params)
    data = response.json()

    if "routes" in data:
        travel_time_sec = data["routes"][0]["summary"]["travelTimeInSeconds"]
        delay_sec = data["routes"][0]["summary"]["trafficDelayInSeconds"]
        return travel_time_sec, delay_sec
    else:
        st.write("❌ API response:", data)
        return None, None

# 📍 Coördinaten
soitec = "50.95184,5.34962"
tessenderlo = "51.06503,5.08203"
via_ring_hasselt = "50.93742,5.33430"
via_zonhoven = "51.01523,5.27103"

# 🖥️ Streamlit interface
st.title("🚗 Slimste route naar huis (Hasselt → Tessenderlo)")

# Route 1: via ring Hasselt
time_route1, delay_route1 = get_route_time(soitec, tessenderlo, API_KEY, via=via_ring_hasselt)

# Route 2: via Zonhoven
time_route2, delay_route2 = get_route_time(soitec, tessenderlo, API_KEY, via=via_zonhoven)

if time_route1 and time_route2:
    st.write(f"🛣️ Route 1 (langs ring Hasselt): **{round(time_route1/60)} min** (file: {round(delay_route1/60)} min)")
    st.write(f"🛣️ Route 2 (langs Zonhoven): **{round(time_route2/60)} min** (file: {round(delay_route2/60)} min)")

    if time_route1 < time_route2:
        st.success("🏆 Beste route: via ring Hasselt")
    elif time_route2 < time_route1:
        st.success("🏆 Beste route: via Zonhoven")
    else:
        st.info("🔄 Beide routes zijn gelijkwaardig.")
else:
    st.error("❌ Kan route-data niet ophalen. Check API-key, internet of TomTom API status.")
