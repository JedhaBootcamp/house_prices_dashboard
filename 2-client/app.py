import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import requests
import os

### Config
st.set_page_config(
    page_title="California Housing",
    page_icon="🏘️ "
)

API_URL=os.environ.get("API_URL")

### App
st.title("House Prices Dashboard 🎨")

st.markdown("""
    Welcome to this awesome `streamlit` dashboard on **Californian Housing**. Here, we wanted to show you the power of Docker Compose. 
    With this app, we are using **two services**:
    1. A client, which is a Dashboard that shows a map of Californian houses.
    2. an API (built in Fast API) that the client uses to fetch data and predictions

    You can download the whole code here 👉 [Source code](https://github.com/JedhaBootcamp/house_prices_dashboard)

    Also, if you want to have a real quick overview of what streamlit is all about, feel free to watch the below video 👇
""")

with st.expander("⏯️ Watch this 15min tutorial"):
    st.video("https://youtu.be/B2iAodr0fOo")

st.markdown("---")


# Use `st.cache` when loading data is extremly useful
# because it will cache your data so that your app 
# won't have to reload it each time you refresh your app
@st.cache
def load_data(nrows):
    r = requests.get(f"{API_URL}/data")
    locations = pd.read_json(r.json(), orient="split")
    r = requests.get(f"{API_URL}/predictions")
    predictions = pd.read_json(r.json()["predictions"], orient="split")
    true_prices = pd.read_json(r.json()["true_prices"])

    data = pd.concat([locations, predictions, true_prices.data], axis=1)
    data = data.rename(columns={0: "Predicted_Prices", "data": "True_prices"})
    return data

st.subheader("Load and showcase data")
st.markdown("""

    You can use the usual Data Science libraries like `pandas` or `numpy` to load data. 
    Then simply use [`st.write()`](https://docs.streamlit.io/library/api-reference/write-magic/st.write) to showcase it on your web app. 

""")

data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)    

st.subheader("Map prices predictions accross California")
st.markdown(
    """
    Here we are using the power of our API to predict prices accross California!
    """
)

fig = px.scatter_mapbox(data, lat="Latitude", lon="Longitude",     color="Predicted_Prices",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=4)
fig.update_mapboxes(accesstoken=os.environ.get("MAPBOX_ACCESS_TOKEN"))

st.plotly_chart(fig, use_container_width=True)

### Footer 
st.markdown("""
    🍇
    If you want to learn more, check out [streamlit's documentation](https://docs.streamlit.io/) 📖
""")