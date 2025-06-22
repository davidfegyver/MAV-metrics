import requests
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from pytz import timezone


# InfluxDB Configuration
INFLUXDB_URL = ""
INFLUXDB_TOKEN = ""
INFLUXDB_ORG = ""
INFLUXDB_BUCKET = ""

url = "https://vonatinfo.mav-start.hu/map.aspx/getData"
payload = {
    "a": "TRAINS",
    "jo": {
        "history": False,
        "id": False
    }
}

response = requests.post(
    url,
    headers={"Content-Type": "application/json"},
    json=payload
)

data = response.json()

trains = data['d']['result']['Trains']['Train']

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN)
write_api = client.write_api(write_options=SYNCHRONOUS)

hungary_tz = timezone('Europe/Budapest')
current_time = datetime.now(hungary_tz)

for train in trains:
    point = Point("trains") \
        .tag("TrainNumber", train["@TrainNumber"]) \
        .tag("Relation", train["@Relation"]) \
        .tag("Menetvonal", train["@Menetvonal"]) \
        .field("Delay", int(train.get("@Delay",0))) \
        .field("Lat", float(train["@Lat"])) \
        .field("Lon", float(train["@Lon"])) \
        .time(current_time.isoformat(), WritePrecision.MS)

    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG,record=point)

client.close()
