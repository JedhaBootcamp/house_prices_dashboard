# House Prices Dashboard

Welcome to this awesome streamlit dashboard on Californian Housing. Here, we wanted to show you the power of Docker Compose. With this app, we are using two services:

1. A client, which is a Dashboard that shows a map of Californian houses.
2. an API (built in Fast API) that the client uses to fetch data and predictions

## To make it work

You will need a `.env` file containing 3 environment variables:

- `PORT`
- `API_URL`
- `MAPBOX_ACCESS_TOKEN`

Ask Jedha to provide you with the right values here. 