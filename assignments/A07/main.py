import PySimpleGUI as sg
import csv
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup



# Function to display daily weather data
def daily():
     # Parse HTML page source using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
# Find the table containing weather data
    table = soup.find('lib-city-history-observation')
# Extract table headers
    thead = table.find("thead")
    row = thead.find("tr")
    ths = row.find_all("th")

    headers = []
    for th in ths:
        headers.append(th.text)

    print(headers)
# Extract table rows
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")
    
# Extract row data
    rows_data = []
    for row in rows:
        ths = row.find_all("td")
        row_data = []
        for th in ths:
            row_data.append(th.text)
        rows_data.append(row_data)

    print(rows_data)

    data = rows_data[1:]
    print(data)
    # Create GUI layout with a table to display data
    layout = [
        [sg.Table(values=data, headings=headers, justification='left')]
    ]
# Create a window with the layout
    window = sg.Window('Weather Data', layout)
    event, _ = window.read()
    window.close()


# Function to display weekly weather data
def weekly():
    # Parse HTML page source using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
# Find the table containing weather data
    table = soup.find('lib-city-history-observation')
    # print(table)
    thead = table.find("thead")
    row = thead.find("tr")
    ths = thead.find_all("td")
    headers = []
   
    for th in ths:
        headers.append(th.text)
    
    print(headers)
 # Extract table rows
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")

    # Extract row data  
    rows_data = []
    #print(rows)
    for row in rows:
        ths = row.find_all("td")
        row_data = []    
        for th in ths:
            row_data.append(th.text)
        rows_data.append(row_data)
          
    
    # Transform data for display in GUI
    data = rows_data[1:]
    final_data=[]
    for i in data:
        s=""
        das="  "
        for j in i:
            s=s+das+j
        final_data.append(s)
# Reorganize data based on number of columns   
    d=int(len(final_data)/len(headers))
    find=[]
    for i in range(0,d):
        j=i
        a=[]
        while(j<len(final_data)):
            a.append(final_data[j])
            j=j+d
        find.append(a)
    print(find)
# Create GUI layout with a table to display data
    
    layout = [
        [sg.Table(values=find, headings=headers, justification='left')]
    ]

# Create a window with the layout
    window = sg.Window('Weather Data', layout)
    event, _ = window.read()
    window.close()

# Function to display monthly weather data

def monthly():
   # Parse HTML page source using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
# Find the table containing weather data
    table = soup.find('lib-city-history-observation')
 # Extract table headers
    thead = table.find("thead")
    row = thead.find("tr")
    ths = row.find_all("td")

    headers = []
    for th in ths:
        headers.append(th.text)

    print(headers)
# Extract table rows
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")
    
 # Extract row data
    rows_data = []
    for row in rows:
        ths = row.find_all("td")
        row_data = []
        for th in ths:
            
            row_data.append(th.text)
        rows_data.append(row_data)

   # print(rows_data)
# Transform data for display in GUI
    data = rows_data[1:]
    
    final_data=[]
    for i in data:
        s=""
        das="  "
        for j in i:
            s=s+das+j
        final_data.append(s)
    # Reorganize data based on number of columns
    d=int(len(final_data)/len(headers))
    find=[]
    for i in range(0,d):
        j=i
        a=[]
        while(j<len(final_data)):
            a.append(final_data[j])
            j=j+d
        find.append(a)
    print(find)
    # Reorganize data based on number of columns
    layout = [
        [sg.Table(values=find, headings=headers, justification='left')]
    ]
# Create a window with the layout
    window = sg.Window('Weather Data', layout)
    event, _ = window.read()
    window.close()
  
if __name__ == '__main__':
     # Read airport codes from a CSV file
    with open('airport-codes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        airport_data = list(reader)
        airport_codes = [airport['ident'] for airport in airport_data]
      # Create the GUI layout using PySimpleGUI
    layout = [
    [sg.Text('Month', size=(15, 1))],
    [sg.DropDown(values=list(range(1, 13)), key='-MONTH-', size=(15, 1))],
    [sg.Text('Day', size=(15, 1))],
    [sg.DropDown(values=list(range(1, 32)), key='-DAY-', size=(15, 1))],
    [sg.Text('Year', size=(15, 1))],
    [sg.DropDown(values=list(range(1900, datetime.now().year + 1)), key='-YEAR-', size=(15, 1))],
    [sg.Text('Code', size=(15, 1))],
    [sg.DropDown(values=airport_codes,  key='-CODE-', size=(15, 1))],
    [sg.Text('Daily / Weekly / Monthly', size=(15, 1))],
    [sg.DropDown(values=['daily', 'weekly', 'monthly'], key='-FILTER-', size=(15, 1))],
    [sg.Submit(), sg.Cancel()]
]
 # Create the GUI layout using PySimpleGUI
    window = sg.Window('Get The Weather', layout)

    # Event loop to capture user input 
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Close' or event == 'Submit':
            break
    window.close()

    month = int(values['-MONTH-'])
    day = int(values['-DAY-'])
    year = int(values['-YEAR-'])
    code = values['-CODE-']
    filter_type = values['-FILTER-']

    sg.popup('You entered', f"Month: {month}, Day: {day}, Year: {year}, Code: {code}, Filter: {filter_type}")

    base_url = "https://www.wunderground.com/history"
    url = f"{base_url}/{filter_type}/{code}/date/{year}-{month:02d}-{day:02d}"
    print("URL:", url)

    options = Options()
    options.add_argument('--headless')

    service = Service('nagaj\Downloads\chromedriver_win32')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(3)

    page_source = driver.page_source

    driver.quit()

    if filter_type == 'daily':
        daily()
    elif filter_type == 'weekly':
        weekly()
    elif filter_type == 'monthly':
        monthly()
