import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd 
import boto3
from joblib import load

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/data")
async def get_houses():
    print("Fetching Data")
    df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")
    location = df.loc[:, ["Latitude", "Longitude"]]
    return location.to_json(orient="split")

@app.get("/predictions")
async def get_predictions():
    df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")
    
    ## Splitting into X and y
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    ## Load model 
    s3 = boto3.client("s3")
    with open("house_prices_model.joblib", "wb") as data:

        s3.download_fileobj(
                Bucket='full-stack-assets', 
                Key='Deployment/house_prices_model.joblib', 
                Fileobj= data
            )

    model = load("house_prices_model.joblib")
    predictions = pd.DataFrame(model.predict(X))

    response = {
        "predictions": predictions.to_json(orient="split"),
        "score": model.score(X, y),
        "true_prices": y.to_json(orient="split")
    }

    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)