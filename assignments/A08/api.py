from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import csv

description = """🚀
## 4883 Software Tools
### Where awesomeness happens
"""

app = FastAPI(
    description=description,
)

db = []

# Open the CSV file
with open('data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    i = 0
    # Read each row in the CSV file
    for row in reader:
        if i == 0:
            i += 1
            continue
        db.append(row)


def getUniqueCountries():
    global db
    country = {}

    for row in db:
        if not row[2] in country:
            country[row[2]] = 0

    return list(country.keys())


def getUniqueRegions():
    global db
    regions = {}

    for row in db:
        if not row[3] in regions:
            regions[row[3]] = 0

    return list(regions.keys())


def calculateDeaths(country=None, region=None, year=None):
    global db
    deaths = 0

    for row in db:
        if country is not None and row[2] != country:
            continue
        if region is not None and row[3] != region:
            continue
        if year is not None and row[0][:4] != year:
            continue

        deaths += int(row[6])

    return deaths


def calculateCases(country=None, region=None, year=None):
    global db
    cases = 0

    for row in db:
        if country is not None and row[2] != country:
            continue
        if region is not None and row[3] != region:
            continue
        if year is not None and row[0][:4] != year:
            continue

        cases += int(row[4])

    return cases


def findCountryWithMaxDeaths(min_date=None, max_date=None):
    global db
    max_deaths = 0
    country_with_max_deaths = None
    deathsByCountry = {}
    for row in db:
        if min_date is not None and row[0] < min_date:
            continue
        if max_date is not None and row[0] > max_date:
            continue

        if row[2] not in deathsByCountry.keys():
            deathsByCountry[row[2]]=int(row[5])
        else:
            deathsByCountry[row[2]]+=int(row[5])
    v = list(deathsByCountry.values())
    k = list(deathsByCountry.keys())
    return k[v.index(max(v))]

def findCountryWithMinDeaths(min_date=None, max_date=None):
    global db
    min_deaths = float('inf')
    country_with_min_deaths = None
    deathsByCountry={}
    for row in db:
        if min_date is not None and row[0] < min_date:
            continue
        if max_date is not None and row[0] > max_date:
            continue

        if row[2] not in deathsByCountry.keys():
            deathsByCountry[row[2]]=int(row[5])
        else:
            deathsByCountry[row[2]]+=int(row[5])
    v = list(deathsByCountry.values())
    k = list(deathsByCountry.keys())
    return k[v.index(min(v))]


def calculateAverageDeaths():
    global db
    total_deaths = 0
    num_countries = len(getUniqueCountries())

    for row in db:
        total_deaths += int(row[5])

    return total_deaths / num_countries


@app.get("/")
async def docs_redirect():
    """Retrieves the documentation provided by Swagger."""
    return RedirectResponse(url="/docs")


@app.get("/countries")
async def get_countries():
    """Retrieves a list of unique countries from the 'db'."""
    try:
        countries = getUniqueCountries()
        return {"success": True, "countries": countries}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/regions")
async def get_regions():
    """Retrieves a list of available WHO regions from the 'db'."""
    try:
        regions = getUniqueRegions()
        return {"success": True, "regions": regions}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/deaths")
async def get_total_deaths(country: str = Query(None), region: str = Query(None), year: str = Query(None)):
    """
    Retrieves the total deaths for the given country, region, and year.
    If no parameters are provided, returns the total deaths for all countries.
    """
    try:
        deaths = calculateDeaths(country, region, year)
        return {"success": True, "deaths": deaths}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/cases")
async def get_total_cases(country: str = Query(None), region: str = Query(None), year: str = Query(None)):
    """
    Retrieves the total deaths for the given country, region, and year.
    If no parameters are provided, returns the total deaths for all countries.
    """
    try:
        cases = calculateCases(country, region, year)
        return {"success": True, "cases": cases}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/max_deaths")
async def get_country_with_max_deaths(min_date: str = Query(None), max_date: str = Query(None)):
    """
    Finds the country with the most deaths.
    If min_date and max_date are provided, finds the country with the most deaths between the specified range of dates.
    """
    try:
        country = findCountryWithMaxDeaths(min_date, max_date)
        return {"success": True, "country": country}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/min_deaths")
async def get_country_with_min_deaths(min_date: str = Query(None), max_date: str = Query(None)):
    """
    Finds the country with the least deaths.
    If min_date and max_date are provided, finds the country with the least deaths between the specified range of dates.
    """
    try:
        country = findCountryWithMinDeaths(min_date, max_date)
        return {"success": True, "country": country}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/avg_deaths")
async def get_average_deaths():
    """Finds the average number of deaths between all countries."""
    try:
        avg_deaths = calculateAverageDeaths()
        return {"success": True, "average_deaths": avg_deaths}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=8080, log_level="debug", reload=True)
