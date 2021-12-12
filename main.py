from crawler import *
from url_generator import *
import csv


# search URL template
urlTemplate = 'https://www.fly540.com/flights/nairobi-to-mombasa?isoneway=0&depairportcode=NBO&arrvairportcode=MBA&date_from=Tue%2C+14+Dec+2021&date_to=Tue%2C+21+Dec+2021&adult_no=1&children_no=0&infant_no=0&currency=USD&searchFlight='

# dictionary of airports names
airportNames = {
    'NBO': 'nairobi',
    'MBA': 'mombasa',
    'WIL': 'nairobi',
    'EDL': 'eldoret'
}

# search data
depAirportCode = 'NBO'  # depparting from airport code, you can change by airportNames
arrvAirportCode = 'MBA'  # destination airport code, you can change by airportNames
departingDays = [0, 10, 20]  # departing on dates after current date
returnAfter = 7  # days


class Console:
    def show_menu(self):

        exit_out = False
        while not exit_out:
            print('''
                ------ Flights Crawler menu ------
                
                This app will  collect all cheapest round trip flight combinations from website www.fly540.com.
                Flights from NBO (Nairobi) to MBA (Mombasa) departing 10 and 20 days from the current date and 
                returning 7 days after the departure date. 

                1. Execute flights data extraction
                2. Write flights data to csv file
                3. Quit
                ''')
            try:
                menu_nr = int(input('Enter menu number (1-3): '))
            except ValueError:
                print('Choose from 1 to 3!')
            else:
                match menu_nr:
                    case 1:
                        # get flights data from website and write to csv file
                        roundTripCombs = self.getRoundTripCombinationsData()
                    case 2:
                        # write crawled data to csv file
                        self.writeToFile(roundTripCombs)
                    case 3:
                        # Quit
                        exit_out = True
                    case _:
                        print('Choose from 1 to 3!')

    def getRoundTripCombinationsData(self):
        currDate = datetime.datetime.now(datetime.timezone.utc)
        urlGen = URLGenerator(urlTemplate, airportNames)
        roundTripCombs = []
        for departday in departingDays:
            # get flight search URL from URL generator
            departDate = currDate + datetime.timedelta(days=departday)
            returnDate = departDate + datetime.timedelta(days=returnAfter)
            URL = urlGen.getURL(
                depAirportCode, arrvAirportCode, departDate, returnDate)
            # get flights data from wensite
            crawler = Crawler(URL)
            outboundData = crawler.getFlights('depart')
            inboundData = crawler.getFlights('return')
            # mixing data to get all available round trip combinations
            for outboundFlight in outboundData:
                for inboundFlight in inboundData:
                    roundTrip = []
                    for item in outboundFlight[:-1]:
                        roundTrip.append(item)
                    for item in inboundFlight[:-1]:
                        roundTrip.append(item)
                    # add price
                    roundTrip.append(outboundFlight[-1] + inboundFlight[-1])
                    roundTripCombs.append(roundTrip)

        # print data to console
        for trip in roundTripCombs:
            print(trip)

        return roundTripCombs

    def writeToFile(self, tripCombinations):
        header = ['outbound_departure_airport', 'outbound_arrival_airport', 'outbound_departure_time',	'outbound_arrival_time',
                  'inbound_departure_airport',	'inbound_arrival_airport',	'inbound_departure_time',	'inbound_arrival_time',	'total_price',	'taxes']

        with open('./exported_flights/flights.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(tripCombinations)


# app start
if __name__ == '__main__':
    console = Console()

    console.show_menu()
