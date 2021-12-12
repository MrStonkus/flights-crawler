import datetime
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
        # get flight year
        searchHeaderHTML = self.soup.find(
            name="div", class_="row row-eq-heights")
        tempDateArr = searchHeaderHTML.find(
            name='div', class_='col-md-4 cl-2').getText().replace(',', '').split(' ')
        flightYear = tempDateArr[5]
        # TODO if departure in one year and arrive in another, there will be departuring year, need solution

        # get depart - arrive dates
        dates = []
        flightDates = flightHTML.find_all(name='span', class_='fldate')
        for date in flightDates:
            dates.append(date.getText().replace(',', ' ').split(' '))

        # get depart and arrive times of flight
        times = []
        flightTimes = flightHTML.find_all(name='span', class_='fltime ftop')
        for time in flightTimes:
            times.append(time.getText().replace(' ', ''))

        departDate = (f'{dates[0][2]} {dates[0][4]}')
        departTime = times[0]

        arriveDate = (f'{dates[1][2]} {dates[1][4]}')
        arriveTime = times[1]

        departDateTime = (f"{flightYear} {departDate} {departTime}")
        returnDateTime = (f"{flightYear} {arriveDate} {arriveTime}")

        # to modify date we need convert date string to datetime format
        departDT = self.__strToDatetimeConvert(departDateTime)
        returnDT = self.__strToDatetimeConvert(returnDateTime)
        # convert time from local airport to UTC
        departDT = self.__timeToUTC(departDT)
        returnDT = self.__timeToUTC(returnDT)
        # convert datetime to string
        departDT = self.__convertDatetimeToString(departDT)
        returnDT = self.__convertDatetimeToString(returnDT)

        return departDT, returnDT

    def __getFlightPrice(self, flightHTML):
        return int(flightHTML.find(name='span', class_='flprice').getText())

    def __strToDatetimeConvert(self, dateString):
        return datetime.datetime.strptime(dateString, '%Y %d %b %I:%M%p')

    def __timeToUTC(self, dateObj):
        # airports time zone are +3, so we get back for 3 hours
        dateObj = dateObj - datetime.timedelta(hours=3)
        return dateObj.replace(tzinfo=datetime.timezone.utc)

    def __convertDatetimeToString(self, datetimeString):
        return datetimeString.strftime("%a %b %d %I:%M:%S GMT %Y")
