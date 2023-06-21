# A07 - Web Scraping
## Naga Vamshi Krishna Jammalamadaka

### Sample input and output
1) Select Day, month, year, airport code and select daily to scrape daily data, weekly to scrape weakly data and montly to get montly data.
 
![dataInput](https://github.com/Nagavamshikrishna/4883-SoftwareTools-Naga/assets/70953975/f1d23139-e372-4207-9d8b-b852048253ab)

Above is the data input form GUI to provide the information to scrape data.
2) We can verify the input data from the pop up as follow

![inputDataVerification_Image](https://github.com/Nagavamshikrishna/4883-SoftwareTools-Naga/assets/70953975/67dc8ec2-c1bc-4681-90e3-c173556ae05b)


We can scrape data for daily, weekly and montly as follows:
### Day Weather Image

![dayWeatherData_Table](https://github.com/Nagavamshikrishna/4883-SoftwareTools-Naga/assets/70953975/bb94d578-779b-43ca-a5fd-69c3bf4b49e5)

### Week Weather Image


![weekWeatherData_Table](https://github.com/Nagavamshikrishna/4883-SoftwareTools-Naga/assets/70953975/84000e7b-b51e-4ff7-9f83-e557e6b214eb)


### Monthly Weather Image

![monthlyWeatherData_Table](https://github.com/Nagavamshikrishna/4883-SoftwareTools-Naga/assets/70953975/7e0642f7-68a3-48af-8002-f36442f8026f)

## Files

| S.No  | File  | Description |    
| :---:   | :---: | :---: |
| 1  | airport-codes.csv   | airport data for the GUI and scraping   |
| 2  | main.py   | python code to create GUI as well code to scrape the data from a dynamic website   |

## Summary
1) Design a user-friendly data entry form using PySimpleGUI to gather inputs for day, month, year, airport, and filter (daily, weekly, monthly).
2) Upon submitting the form, generate a URL specific to the entered details for querying weather data.
3) Use the Selenium library to interact with website, retrieve the asynchronous data, and handle dynamic content loading.
4) Utilize Beautiful Soup (BS4) to parse the received data and extract the relevant weather information.
5) Use PySimpleGUI present the extracted weather data in an organized and visually appealing manner.

