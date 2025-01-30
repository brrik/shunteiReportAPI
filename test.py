import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware # CORS

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def getDatas():
    return_data = ""

    now = datetime.now()
    formatted_time = now.strftime("%Y%m%d%H%M")
    object_date = now.strftime("%Y-%m-%d")

    request = requests.get(f"https://www.kansai-td.co.jp/interchange/teiden-info/ja/instantaneous.json?_={formatted_time}")
    response = request.json()
    ivd = response["list"]
    #print(ivd)
    for inc in ivd:
        #if inc["date"] == object_date:
        if inc["date"] == "2025-01-29":
            if inc["list"] != []:
                incidents = inc["list"]
                for incident in incidents:
                    areas = incident["areas"]
                    time = incident["offdatetime"]
                    for area in areas:
                        children = area["children"]
                        return_data += time + "\n"
                        for child in children:
                            return_data += area["name"] + " : " + child["name"] + "\n"
                        return_data += "\n\n"
            else:
                return_data = "nodata"
            break
    else:
        return_data = "error"
    print(return_data)
    return return_data