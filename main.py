import datetime
from crawler import *
from url_generator import *


# search URL template
urlTemplate = 'https://www.fly540.com/flights/nairobi-to-mombasa?isoneway=0&depairportcode=NBO&arrvairportcode=MBA&date_from=Tue%2C+14+Dec+2021&date_to=Tue%2C+21+Dec+2021&adult_no=1&children_no=0&infant_no=0&currency=USD&searchFlight='

# dictionary of airports names
airportNames = {
    'NBO': 'nairobi',
    'MBA': 'mombasa',
    'WIL': 'nairobi',
    'EDL': 'eldoret'
}
timeZones = {
    'NBO': 3,
    'MBA': 3,
    'WIL': 3,
    'EDL': 3
}

# search data
depAirportCode = 'NBO'  # depparting from airport code, you can change by airportNames
arrvAirportCode = 'MBA'  # destination airport code, you can change by airportNames
departingDays = [10, 20]  # departing on dates after current date
returnAfter = 7  # days


class Console:
    def show_menu(self):

        exit_out = False
        while not exit_out:
            print('''
                ------ Flights Crawler menu ------
                
                This app will  collect all cheapest round trip flight combinations from website www.fly540.com.
                Flights from NBO (Nairobi) to MBA (Mombasa) departing 10 and 20 days from the current date and 
                returning 7 days after the departure date. Data will be saved in CSV format. 

                1. Execute data extraction
                2. Quit
                ''')
            try:
                menu_nr = int(input('Enter menu number (1-2): '))
            except ValueError:
                print('Choose from 1 to 2!')
            else:
                match menu_nr:
                    case 1:
                        # get flights data from website and write to csv file
                        roundTripCombs = self.getRoundTripCombinationsData()
                        self.writeToFile(roundTripCombs)
                    case 2:
                        # Quit
                        exit_out = True
                    case _:
                        print('Choose from 1 to 2!')

    def getRoundTripCombinationsData(self):
        currDate = datetime.datetime.now(datetime.timezone.utc)
        urlGen = URLGenerator(urlTemplate, airportNames)
        # print("Current Date: ", currDate.strftime(
        #     "%a %b %d %I:%M:%S GMT %Y"))
        for departday in departingDays:
            # get flight search URL
            departDate = currDate + datetime.timedelta(days=departday)
            returnDate = departDate + datetime.timedelta(days=returnAfter)
            URL = urlGen.getURL(
                depAirportCode, arrvAirportCode, departDate, returnDate)
            # get flights data
            crawler = Crawler(URL)
            outboundData = crawler.getFlights('depart')
            inboundData = crawler.getFlights('return')
            # print(outboundData, inboundData)

            # get all round trip combinations
            roundTripCombs = []
            for outboundFlight in outboundData:
                for inboundFlight in inboundData:
                    # the year of flight do not shown in website, so we getting from depart and returning dates
                    outboundYear = departDate.strftime("%Y")
                    inboundYear = returnDate.strftime("%Y")

                    # print(outboundFlight)
                    # TODO įvesti metus
                    roundTrip = []
                    for item in outboundFlight[:-1]:
                        roundTrip.append(item)
                    for item in inboundFlight[:-1]:
                        roundTrip.append(item)
                    # add price
                    roundTrip.append(outboundFlight[-1] + inboundFlight[-1])
                    roundTripCombs.append(roundTrip)
            for trip in roundTripCombs:
                print(trip)
                # TODO įrašyti į failą

    def writeToFile(self, tripCombinations):
        pass


# app start
if __name__ == '__main__':
    console = Console()

    console.show_menu()
