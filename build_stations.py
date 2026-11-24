import csv
import requests
def is_digit(seed_id):
    return seed_id.isdigit()


def stripped_id(seed_id):
    return seed_id.strip()

def build_triplets(station_id, state="CO", network="SNTL"):
    return f"{station_id}:{state}:{network}"

# Read in stations_seed.csv
# Validate seed rows
# Build triplets (see function above)
# Call /stations once with all triplets
# Check stations returned matches stations sent
# Write stations.csv
# Write logs

# 1. Read in stations_seed.csv
with open('stations_seed.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    clean_stations = []
    error_log_stations_id = []
    seen_id = set()
    for index, row in enumerate(reader, start=2):
        # 2. Validate seed rows
        clean_id = stripped_id(row['station_id'])
        if clean_id == "":
            error_log_stations_id.append({"row": index, "value": clean_id, "reason": "blank value"})
            print(error_log_stations_id)
        elif not is_digit(clean_id):
            error_log_stations_id.append({"row": index, "value": clean_id, "reason": "not a number"})
            print(error_log_stations_id)
        elif clean_id in seen_id:
            error_log_stations_id.append({"row": index, "value": clean_id, "reason": "duplicate id"})
            print(error_log_stations_id)
        else:
            seen_id.add(clean_id)
            row['station_id'] = clean_id
            clean_stations.append(row)

# Call /stations once with all triplets
triplets = [
    build_triplets(
        row['station_id'],
    )
    for row in clean_stations
]

url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/stations"
payload = {"stationTriplets": ",".join(triplets)}


error_log_api = []
station_id_misaligned = []
api_return = []
response_code = []

try:
    response = requests.get(url, params=payload, timeout=10)
    response.raise_for_status()
    response_code.append(response.status_code)
    # Check stations returned matches stations sent
    api_response = response.json()
    response_check =len(api_response)
    for returnedId in api_response:
        # Still provide api response, so one misaligned id does not impact chain
        api_return.append({"StationName": returnedId['name'], "Elevation": returnedId["elevation"]})
    if response_check != len(clean_stations):
        # If an id that was sent, was not returned, log it
        print("Response count does not match clean stations count")
        error_log_api.append({"reason": "Response count does not match clean stations count", "sent": len(clean_stations), "returned": response_check, "triplets": payload['stationTriplets']})
        returned_ids = []
        sent_ids = []
        for returnedId in api_response:
            returned_ids.append(returnedId['stationId'])
        for sentId in clean_stations:
            sent_ids.append(sentId['station_id'])
        misaligned_id = list(set(sent_ids) - set(returned_ids))
        station_id_misaligned.append({"misalignedId": misaligned_id, "action": "Remove this id from the stations_seed.csv"})
        print(station_id_misaligned)
    # Write stations.csv
    look_up = {}
    for station in clean_stations:
        look_up.update({station['station_id']: station})

    station_output = []
    for station in api_response:
        station_dict = {
            "station_name": station['name'],
            "station_id": look_up[station['stationId']]['station_id'],
            "elevation_ft": station['elevation'],
            "latitude": station['latitude'],
            "longitude": station['longitude'],
            "county": station['countyName'],
            "caic_zone": "",
            "reason": look_up[station['stationId']]['reason']
        }
        station_output.append(station_dict)
except requests.exceptions.Timeout:
    error_log_api.append({"reason": "Request timed out"})
    print(error_log_api)
except requests.exceptions.RequestException as e:
    error_log_api.append({"reason": "request failed", "detail": str(e)})
    print(error_log_api)



print(f"Clean Stations: {len(clean_stations)} | Errors Logged: {len(error_log_stations_id) +len(error_log_api)}")










