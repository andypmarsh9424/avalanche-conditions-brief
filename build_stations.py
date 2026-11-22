import csv
def is_digit(seed_id):
    return seed_id.isdigit()


def stripped_id(seed_id):
    return seed_id.strip()

# Read in stations_seed.csv
# Validate seed rows
# Build triplets
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
            blank_value_dict = {
                "row": index,
                "value": clean_id,
                "reason": "blank value"
            }
            error_log_stations_id.append(blank_value_dict)
        elif not is_digit(clean_id):
            string_value_dict = {
                "row": index,
                "value": clean_id,
                "reason": "not a number"
            }
            error_log_stations_id.append(string_value_dict)
        elif clean_id in seen_id:
            dup_dict = {
                "row": index,
                "value": clean_id,
                "reason": "duplicate id"
            }
            error_log_stations_id.append(dup_dict)
        else:
            seen_id.add(clean_id)
            row['station_id'] = clean_id
            clean_stations.append(row)

print(f"Clean Stations: {len(clean_stations)} | Errors Logged: {len(error_log_stations_id)}")
print(error_log_stations_id)
print(clean_stations)


