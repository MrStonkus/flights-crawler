import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, url):
        self.URL = url
        self.soup = BeautifulSoup(
            requests.get(self.URL).text,
            "html.parser"
        )

    def getFlights(self, action):  # action can be only 'depart' or 'return'
        flights = []
        # extract only depart or return flights HTML by specifed html class name
        flightsHTML = self.soup.find(
            name="div", class_=f"fly5-flights fly5-{action} th")
        # get depart or return flights table
        flightsTableHTML = flightsHTML.find_all(name='table', class_='table')
        for flightHTML in flightsTableHTML:
            # get flightHTML details -> departAir, ArriveAir, deaprtDate, ArriveDate, flightPrice
            outDepAirport = self.__getAirportCode(flightsHTML, "fly5-flfrom")
            outArrAirport = self.__getAirportCode(flightsHTML, "fly5-flto")
            [departsDate, arrivesDate] = self.__getFlightDateStamp(flightHTML)
            flightPrice = self.__getFlightPrice(flightHTML)

            flights.append([outDepAirport, outArrAirport,
                            departsDate, arrivesDate, flightPrice])
        return flights

    def __getAirportCode(self, flightsHTML, className):
        return flightsHTML.find(class_=className).getText().split(' ')[2].replace('(', '').replace(')', '')

    def __getFlightDateStamp(self, flightHTML):
        dates = []
        flightDates = flightHTML.find_all(name='span', class_='fldate')
        for date in flightDates:
            dates.append(date.getText().replace(',', ' ').split(' '))

        times = []
        flightTimes = flightHTML.find_all(name='span', class_='fltime ftop')
        for time in flightTimes:
            times.append(time.getText().replace(' ', ''))

        departsDateStamp = f'{dates[0][1]} {dates[0][4]} {dates[0][2]} {times[0]}'
        arrivesDateStamp = f'{dates[1][1]} {dates[1][4]} {dates[1][2]} {times[1]}'
        return departsDateStamp, arrivesDateStamp

    def __getFlightPrice(self, flightHTML):
        return int(flightHTML.find(name='span', class_='flprice').getText())
