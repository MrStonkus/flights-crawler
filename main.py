from crawler import *

# console class (main)


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
                        self.executeDateExtraction()
                    case 2:
                        # Quit
                        exit_out = True
                    case _:
                        print('Choose from 1 to 2!')

    def executeDateExtraction(self):
        self.getURLs()
        URL = 'https://www.fly540.com/flights/nairobi-to-mombasa?isoneway=0&depairportcode=NBO&arrvairportcode=MBA&date_from=Tue%2C+14+Dec+2021&date_to=Tue%2C+21+Dec+2021&adult_no=1&children_no=0&infant_no=0&currency=USD&searchFlight='
        crawler = Crawler(URL)
        flightsD = crawler.getFlights('depart')
        flightsR = crawler.getFlights('return')
        print(flightsD, flightsR)

    def getURLs(self):
        self.getURLs()


# app start
if __name__ == '__main__':
    console = Console()

    console.show_menu()
