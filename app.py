from fastapi import FastAPI, HTTPException, Depends
from walmart import scraper_v2
from dotenv import load_dotenv
from fastapi.security import APIKeyQuery
import os

load_dotenv()

query_scheme = APIKeyQuery(name="X-API-Key")


# verif we are using the right api key
def verify_api_key(api_key: str = Depends(query_scheme)):
    if api_key != os.getenv("API_KEY"):
        return HTTPException(status_code=404, detail="Invalid API Key")


app = FastAPI(dependencies=[Depends(verify_api_key)])


# get the upc code from walmart
@app.get("/get-walmart-upc")
def get_walmart_upc(url: str) -> dict:
    try:
        upc = scraper_v2(url)
        return {"upc": upc, "url": url}
    except Exception as e:
        return HTTPException(status_code=500, detail=e)
