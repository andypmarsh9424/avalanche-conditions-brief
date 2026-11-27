# Colorado Avalanche Conditions Brief

> **Disclaimer:** This is a personal data project, not an avalanche forecast. Always check the official [CAIC forecast](https://avalanche.state.co.us/) before traveling in avalanche terrain.

## Problem
The Colorado Avalanche Information Center (CAIC) publishes a daily avalanche forecast for each backcountry zone. The forecast says how dangerous a zone is today, but it doesn't make it easy to see how conditions are trending, or which observations are behind the change. Someone planning tomorrow's terrain has to piece that together from the forecast, public field reports and weather station data, spread across several pages.

## User
A backcountry skier planning the next day's terrain.

## Question it helps answer
Which zones are trending worse, which are worth watching, and what's driving it.

## What the brief shows, per zone
- **Snowpack changes** from NRCS SNOTEL stations: new snow over 24 and 72 hours, and change in snow water content.
- **Recent avalanche activity and signs of instability** (cracking, collapsing) from CAIC field reports.
- **The trend over the past 7 days**, so a zone getting worse stands out before it peaks.
- **Links back to the observations** behind every flag.

## What "better" looks like
- One page instead of several sources.
- Every flag can be traced to the data behind it.
- Updated automatically every day.
- Quick enough for a morning conditions check.

## How to run
1. `python -m venv .venv` 
2. `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
3. `pip install -r requirements.txt` (Python 3.11, no API key needed)
4. Optional: edit stations_seed.csv to change which SNOTEL stations are tracked (ID, name, county, reason)
5. `python build_stations.py` 
6. Check the newest file in logs/ (build_stations_<timestamp>.json); "status" should be SUCCESS
7. More steps will be added as the pipeline grows

## Out of scope
Not a forecast and not safety advice. No accident or fatality data.

## Status
- **COMPLETED**
  - Repo and seed file
  - Station pipeline: validates the seed file, fetches metadata from the AWDB API with count checks and failure handling, writes stations.csv 
  - Run logs: each run writes a JSON log to logs/ with status, counts sent/returned/written, and any errors
- **IN PROGRESS**
  - SNOTEL backfill
- **NOT STARTED**
  - CAIC observations pull
  - Data cleaning + issues log
  - Zone trend flags
  - Warning-sign extraction from field reports, via LLM
  - App, publicly hosted, with a daily refresh

## How I built this
I designed and coded this project myself, using Claude as a coach, code reviewer and syntax reference.

## Data sources
- **CAIC**: avalanche observations and field reports, from the [Avalanche Explorer](https://forecasts.avalanche.state.co.us/explorer/)
- **NRCS SNOTEL**: daily snowpack readings, via the [AWDB REST API](https://wcc.sc.egov.usda.gov/awdbRestApi/swagger-ui/index.html)
