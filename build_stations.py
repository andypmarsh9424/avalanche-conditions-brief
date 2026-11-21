import csv
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
    for row in reader:
        print(row['station_name'], row['station_id'], row['reason'])


