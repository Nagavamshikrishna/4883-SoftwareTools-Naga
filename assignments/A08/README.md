
# Description:

Implementation of a RESTful API using FastAPI to provide access to COVID-19 data. Please note that this example assumes you have a publicly available data source from which you can fetch the COVID-19 statistics

## Column Descriptions:


|   #   | Column |  Description |
| :---: | ----------- | ---------------------- |
|    01  | Date_reported | date in yyyy-mm-dd format|  
|    02  |  Country_code |A unique 2 digit country code| 
|    03 |  country | Name of Country| 
|    04 | WHO_region	|World Health Organization region | 
|    05|  New_cases| Number of new cases on this date|
|    06|  Cumulative_cases| Cumulative cases up to this date |
|    07|  New_deaths| Number of new deaths on this date |
|    08|  Cumulative_deaths| Cumulative deaths up to this date |

## Routes:
* http://localhost:8080
http://localhost:8080 redirect to the homepage of the FastApi Swagger UI like below snip

![image](https://github.com/Nagavamshikrishna/4883-SoftwareTools-Naga/assets/70953975/8e5bf6cc-ce12-40dd-aa94-f610c45115bd)

* /country
  
  http://localhost:8080/countries will provide the data of the country list like below

  ```python
   {
          "countries": [
              "Afghanistan",
              "Albania",
              "Algeria",
              "American Samoa",
              "Andorra",
              "Angola",
              "Anguilla",
              "Antigua and Barbuda",
              "ETC"
          ],
          "success": true
    }
  ```

* /regions
    
http://localhost:8080/regions will provide the information of tjhe country codes we have in the csv
```python
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
```

* /deaths
  
http://localhost:8080/deaths will provide the information of thr total death rates in each countries
```python
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
```
We can also filter the death rates depending on the country, region and year as below

[http://localhost:8080/deaths/?country=India&year=2020](http://localhost:8080/deaths/?country=India&region=In&year=2020)
```python
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

```
* /cases
http://localhost:8080/cases will provide the cases present in all countries
```python
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
```
we can also search via country, region or year like below
http://localhost:8080/cases/?country=India&region=IN 
```python
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
```

* /max_deaths
  
http://localhost:8080/max_deaths/
It can find the  most deaths counts. If min_date and max_date are provided, finds the country with the most deaths between the specified range of dates.

```python
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
```
http://localhost:8080/max_deaths/?min_date=2020-01-01&max_date=2022-01-01

```python
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
```

* /min_deaths

  It will fetch the countries with low deaths
  http://localhost:8080/min_deaths

```python
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


  
```

* /avg_deaths

http://localhost:8080/avg_deaths/. Finds the average number of deaths between all countries.

```python
{
  "success": true,
  "average_deaths": 23.149139120523127
}
```
## Files:

|  #  | Column            | Description                       |
| :-: | :---------------- | :-------------------------------- |
|  0  | data.csv | file that holds covid data       |
|  1  | api.py     |  python code for api routes     |

## commands:
* pip install fastapi
* python3 api.py
