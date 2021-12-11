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
                        self.executeDataExtraction()
                    case 2:
                        # Quit
                        exit_out = True
                    case _:
                        print('Choose from 1 to 2!')

    def executeDataExtraction(self):
        currDate = datetime.datetime.now(datetime.timezone.utc)
        urlGen = URLGenerator(urlTemplate, airportNames)
        # print("Current Date: ", currDate.strftime(
        #     "%a %b %d %I:%M:%S GMT %Y"))
        for departday in departingDays:
            departDate = currDate + datetime.timedelta(days=departday)
            returnDate = departDate + datetime.timedelta(days=returnAfter)
            URL = urlGen.getURL(
                depAirportCode, arrvAirportCode, departDate, returnDate)

    # for URL in URLs:
    #     crawler = Crawler(URL)
    #     flightsD = crawler.getFlights('depart')
    #     flightsR = crawler.getFlights('return')
    #     print(flightsD, flightsR)


# app start
if __name__ == '__main__':
    console = Console()

    console.show_menu()
