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
        elif not is_digit(clean_id):
            error_log_stations_id.append({"row": index, "value": clean_id, "reason": "not a number"})
        elif clean_id in seen_id:
            error_log_stations_id.append({"row": index, "value": clean_id, "reason": "duplicate id"})
        else:
            seen_id.add(clean_id)
            row['station_id'] = clean_id
            clean_stations.append(row)

# Call stations
triplets = [
    build_triplets(
        row['station_id'],
        row.get('state', "CO"),
        row.get('network', "SNTL")
    )

    for row in clean_stations
]

url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/stations"
payholder = {"stationTriplets": ",".join(triplets)}

returned = []

try:
    response = requests.get(url, params=payholder, timeout=10)
    response.raise_for_status()
    print("Success", response.json())
    response_code = response.status_code
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as e:
    print("Request failed", e)


print(f"Clean Stations: {len(clean_stations)} | Errors Logged: {len(error_log_stations_id)}")
print(error_log_stations_id)


