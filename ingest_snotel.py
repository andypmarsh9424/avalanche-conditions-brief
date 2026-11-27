import csv
import requests
from datetime import date, timedelta, datetime
import json

def build_triplets(station_id, state="CO", network="SNTL"):
    return f"{station_id}:{state}:{network}"

def get_l7d():
    return date.today() - timedelta(days=7)

def get_l1d():
    return date.today() - timedelta(days=1)

def date_match(response_date):
    check_date = date.today() - timedelta(days=1)
    if str(response_date) == str(check_date):
        return True
    else:
        return False

# 1. Read in stations.csv
with open('stations.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    stations = []
    for index, row in enumerate(reader, start=2):
        stations.append(row)

# 2. Build Triplets
triplets = [
    build_triplets(row['station_id'])
    for row in stations
]

# 3. Stage begin and end date
begin_date = get_l7d()
end_date = get_l1d()

error_log_api = []

# 4. API Requests
url = 'https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data'
payload = {'stationTriplets': ",".join(triplets),
           'elements': 'WTEQ',
           'beginDate': begin_date,
           'endDate': end_date
           }

try:
    response = requests.get(url, params=payload, timeout=10)
    response.raise_for_status()
    api_response = response.json()
    response_date = api_response[0]['data'][0]['values'][-1]['date']
    if date_match(response_date) == False:
        error_log_api.append({"reason": "date returned does not match expected value"})
        print(error_log_api)
    else:
        print(api_response)
except requests.exceptions.Timeout:
    print("timeout")
except requests.exceptions.RequestException as e:
    print(e)



