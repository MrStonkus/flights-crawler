import requests
from bs4 import BeautifulSoup

URL = 'https://www.fly540.com/flights/nairobi-to-mombasa?isoneway=0&depairportcode=NBO&arrvairportcode=MBA&date_from=Tue%2C+14+Dec+2021&date_to=Tue%2C+21+Dec+2021&adult_no=1&children_no=0&infant_no=0&currency=USD&searchFlight='

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")


departFlights = soup.find_all(name="div", class_="fly5-flights fly5-depart th")
print(departFlights.lenght)
