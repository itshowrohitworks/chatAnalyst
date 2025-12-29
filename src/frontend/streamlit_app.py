import streamlit as st
import requests

st.set_page_config(page_title="Chat Analyst", page_icon="🎥")

st.title("Chat Analyst – Donation Predictor")
st.write(
    "Estimate the **expected donation amount** for a stream "
    "based on engagement metrics."
)

st.divider()

# --- Input Fields ---
avg_viewers = st.number_input("Average Viewers", min_value=0, value=1000)
peak_viewers = st.number_input("Peak Viewers", min_value=0, value=2000)
chat_rate = st.number_input("Chat Rate", min_value=0, value=200)
like_count = st.number_input("Like Count", min_value=0, value=800)
duration_minutes = st.number_input("Stream Duration (minutes)", min_value=1, value=120)

niche = st.selectbox(
    "Stream Niche",
    ["Gaming", "Tech", "Music", "Education", "IRL"]
)

country = st.selectbox(
    "Country",
    ["India", "USA", "UK", "Canada", "Germany"]
)

st.divider()

# --- Predict Button ---
if st.button("Predict Donation 💰"):
    payload = {
        "avg_viewers": avg_viewers,
        "peak_viewers": peak_viewers,
        "chat_rate": chat_rate,
        "like_count": like_count,
        "duration_minutes": duration_minutes,
        "niche": niche,
        "country": country
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict/",
            json=payload,
            timeout=5
        )

        if response.status_code == 200:
            result = response.json()
            st.success(
                f"💰 Expected Donation: ₹ {result['predicted_stream_donation']}"
            )
        else:
            st.error("Prediction failed. Check FastAPI logs.")

    except Exception as e:
        st.error(f"Could not connect to API: {e}")
