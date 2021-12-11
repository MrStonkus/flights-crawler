# from datetime import date


class URLGenerator:
    def __init__(self, urlTemplate, airportNames):
        self.urlTemplate = urlTemplate
        self.airNames = airportNames

    def getURL(self, depAirCode, arrAirCode, departDate, arrivalDate):
        tempURL = self.urlTemplate

        # update airport names
        replFrom = '/nairobi-to-mombasa?'
        replTo = f'/{self.airNames[depAirCode]}-to-{self.airNames[arrAirCode]}?'
        tempURL = tempURL.replace(replFrom, replTo)

        # update depart airport code
        replFrom = 'depairportcode=NBO'
        replTo = f'depairportcode={depAirCode}'
        tempURL = tempURL.replace(replFrom, replTo)

        # update arrival airport code
        replFrom = 'arrvairportcode=MBA'
        replTo = f'arrvairportcode={arrAirCode}'
        tempURL = tempURL.replace(replFrom, replTo)

        # update depart date
        replFrom = 'date_from=Tue%2C+14+Dec+2021'
        dateStr1 = departDate.strftime("%a")
        dateStr2 = departDate.strftime("%d+%b+%Y")
        replTo = ("date_from=" + dateStr1 + "%2C+" + dateStr2)
        tempURL = tempURL.replace(replFrom, replTo)

        # update arrival date
        replFrom = 'date_to=Tue%2C+21+Dec+2021'
        dateStr1 = arrivalDate.strftime("%a")
        dateStr2 = arrivalDate.strftime("%d+%b+%Y")
        replTo = ("date_to=" + dateStr1 + "%2C+" + dateStr2)
        tempURL = tempURL.replace(replFrom, replTo)

        return tempURL
