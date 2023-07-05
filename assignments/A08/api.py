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
    DeathsData=[]
    for row in db:
        if min_date is not None and row[0] < min_date:
            continue
        if max_date is not None and row[0] > max_date:
            continue

        DeathsData.append(row)


        if row[2] not in deathsByCountry.keys():
            deathsByCountry[row[2]]=int(row[7])
        else:
            deathsByCountry[row[2]]+=int(row[7])
    max_death_row=DeathsData[0]
    for row in DeathsData:
        if int(row[7])>int(max_death_row[7]):
            max_death_row=row
    v = list(deathsByCountry.values())
    k = list(deathsByCountry.keys())
    return{
         max_death_row[2],
         max_death_row[7]

    }
    

def findCountryWithMinDeaths(min_date=None, max_date=None):
    global db
    min_deaths = float('inf')
    country_with_min_deaths = None
    deathsByCountry={}
    DeathsData=[]
    for row in db:
        if min_date is not None and row[0] < min_date:
            continue
        if max_date is not None and row[0] > max_date:
            continue
        DeathsData.append(row)
    
    min_death_row=DeathsData[0]
    for row in DeathsData:
        if int(row[7])<int(min_death_row[7]):
            min_death_row=row

    return{
         min_death_row[2],
         min_death_row[7]
    }


def calculateAverageDeaths():
    global db
    total_deaths = 0
    num_countries = len(db)

    for row in db:
        total_deaths += int(row[6])

    return total_deaths / num_countries


@app.get("/")
async def docs_redirect():
    """Retrieves the documentation provided by Swagger."""
    return RedirectResponse(url="/docs")


@app.get("/countries")
async def get_countries():
    """
    This method will return a total countrirs count.
    
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/countries]

    #### Response 1:

        {
            "total": 1000000,
            "params": {
                "country": null,
                "year": null
            }
            "success": true,
        }

    
    """
    try:
        countries = getUniqueCountries()
        return {"countries": countries, "success": True }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/regions")
async def get_regions():
    """
    This method will return a regions .
    
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/regions/]

    #### Response 1:

        {
             "success": true,
             "regions": [
                    "EMRO",
                    "EURO",
                    "AFRO",
                    "WPRO",
                    "AMRO",
                    "SEARO",
                    "Other"
                  ]
        }

    """
    try:
        regions = getUniqueRegions()
        return {"success": True, "regions": regions}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/deaths")
async def get_total_deaths(country: str = Query(None), region: str = Query(None), year: str = Query(None)):
    """
    This method will return a total death count or can be filtered by country and year.

    - **Params:**

      - country (str) : A country name

      - year (int) : A 4 digit year

    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/deaths/](http://localhost:8080/deaths/)

    #### Response 1:

                    {
                        "success": true,
                        "deaths": {
                            "total_deaths": 6945714,
                            "params": {
                                "country": null,
                                "region": null,
                                "year": null
                            },
                            "success": true
                
            }
                    }

    #### Example 2:

    [http://localhost:8080/deaths/?country=India&year=2020](http://localhost:8080/deaths/?country=India&year=2020)

    #### Response 2:

                    {
                                
                        "success": true,
                        "deaths": {
                            "total_deaths": 148738,
                            "params": {
                            "country": "India",
                            "region": null,
                            "year": "2020"
                            },
                            "success": true
            
            }
                    }

    """
    try:
        deaths = calculateDeaths(country, region, year)
        deaths={
            "total_deaths":  int(deaths),
            "params": {
                    "country": country,
                    "region": region,
                    "year": year
                },
                "success": True,
            }
        return {"success": True, "deaths": deaths}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/cases")
async def get_total_cases(country: str = Query(None), region: str = Query(None), year: str = Query(None)):
    """
    This method will return a total casest or can be filtered by country, region and year.

    - **Params:**

      - country (str) : A country name

      - region : A region name

      - year (int) : A 4 digit year

    - **Returns:**

      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/deaths/](http://localhost:8080/deaths/)

    #### Response 1:

                    {
                        "success": true,
                        "cases": {
                            "cases": 768187096,
                            "params": {
                                "country": null,
                                "region": null,
                                "year": null
                            },
                            "success": true
                        }
            }

    #### Example 2:

    [http://localhost:8080/cases/?country=India&region=IN](http://localhost:8080/cases/?country=India&region=IN)

    #### Response 2:

                        {
                        "success": true,
                        "cases": {
                            "cases": 0,
                            "params": {
                                "country": "India",
                                "region": "IN",
                                "year": null
                            },
                            "success": true
                }
            }

    """
    try:
        cases = calculateCases(country, region, year)
        #total_cases = remaining_data['New_cases'].sum()
        new_cases={
            "cases":  int(cases),
            "params": {
                    "country": country,
                    "region": region,
                    "year": year
                },
                "success": True,
            }
        return {"success": True, "cases": new_cases}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/max_deaths")
async def get_country_with_max_deaths(min_date: str = Query(None), max_date: str = Query(None)):
    """
    This method will return a maximum death count or can be filtered by min_date and max_date.

    - **Params:**

      - min_date (str) : minimum date

      - max_date (int) : maximum date

    - **Returns:**

      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/deaths/](http://localhost:8080/deaths/)

    #### Response 1:

                    {
                "cases": [
                    "1127152",
                    "United States of America"
                ],
                "params": {
                    "min_date": null,
                    "max_date": null
                },
                "success": true
                }

    #### Example 2:

    [http://localhost:8080/max_deaths/?min_date=2020-01-01&max_date=2022-01-01](http://localhost:8080/max_deaths/?min_date=2020-01-01&max_date=2022-01-01)

    #### Response 2:
                {
                "cases": [
                    "United States of America",
                    "820389"
                ],
                "params": {
                    "min_date": "2020-01-01",
                    "max_date": "2022-01-01"
                },
                "success": true
                }

    """
    try:
        country = findCountryWithMaxDeaths(min_date, max_date)
        max_death={
            "cases":  country,
            "params": {
                    "min_date": min_date,
                    "max_date": max_date
                },
                "success": True,
            }
        
        return max_death
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/min_deaths")
async def get_country_with_min_deaths(min_date: str = Query(None), max_date: str = Query(None)):
    """
    This method will return a min death count or can be filtered by min_date and max_date.

    - **Params:**

      - min_date (str) : min date

      - max_date (int) : max date

    - **Returns:**

      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/min_deaths/](http://localhost:8080/min_deaths/)

    #### Response 1:

                    {
                "cases": [
                    "Afghanistan",
                    "0"
                ],
                "params": {
                    "min_date": null,
                    "max_date": null
                },
                "success": true
            }

    #### Example 2:

    [http://localhost:8080/max_deaths/?min_date=2020-01-01&max_date=2022-01-01](http://localhost:8080/max_deaths/?min_date=2020-01-01&max_date=2022-01-01)

    #### Response 2:

                        {
                "cases": [
                    "United States of America",
                    "820389"
                ],
                "params": {
                    "min_date": "2020-01-01",
                    "max_date": "2022-01-01"
                },
                "success": true
                }

    """
    try:
        country = findCountryWithMinDeaths(min_date, max_date)
        min_death={
            "cases":  country,
            "params": {
                    "min_date": min_date,
                    "max_date": max_date
                },
                "success": True,
            }
        
        return min_death
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/avg_deaths")
async def get_average_deaths():
    """
    This method will return a total death count or can be filtered by country and year.

    - **Params:**

      - country (str) : A country name

      - year (int) : A 4 digit year

    - **Returns:**

      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/avg_deaths/](http://localhost:8080/avg_deaths/)

    #### Response 1:

                {
        "success": true,
        "average_deaths": 23.149139120523127
        }

    """
    try:
        avg_deaths = calculateAverageDeaths()
        
        return {"success": True, "average_deaths": avg_deaths}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=8080, log_level="debug", reload=True)
