# flights-crawler

This console UI app is a web flight crawler written in python.

The app, looks in www.fly540.com website and collect all cheapest round trip flight combinations from NBO (Nairobi) to MAB (Mombasa).

Standard departure are 10 and 20 days from current date and returning 7 days after the departure date, but you can freely modify its in code.

Install:

1. Install python >= v3.1
2. `pip install requests`
3. In file directory terminal run `py main.py`

```
---- Flights Crawler menu ------
  
This app will  collect all cheapest round trip flight combinations from website www.fly540.com.
Flights from NBO (Nairobi) to MBA (Mombasa) departing 10 and 20 days from the current date and returning 7 days after the departure date. 

                1. Execute data extraction
                2. Write flights data to csv file
                3. Quit
```
