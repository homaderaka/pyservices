from bs4 import BeautifulSoup
import requests
import datetime


class Parser:
    def __init__(self):
        pass


    def getCurrencyNames(self):
        pass

    def getExchangeRate(self, currency1, currency2, date):
        """
        Parse relation between 2 given currencies from cbr.ru on given date and return it

        :param currency1 (str): currency name in format RUB
        :param currency2 (str): currency name in format RUB
        :param date (str): string in format DD.MM.YYYY (12.08.2003)
        :return result (float): relation between currency1 and currency2
        """
        url = 'http://cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=' + date
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        currencies = soup.findAll('tr')
        exchanges = {}
        exchanges['RUB'] = 1

        for currency in currencies:
            data = currency.findAll('td')
            # data[0] - some code
            # data[1] - currency name in format RUB
            # data[2] - currency amount
            # data[3] - currency full name
            # data[4] - currency relation to ruble
            if len(data) == 5:
                key = data[1].text
                value = float(data[4].text.replace(',', '.')) / float(data[2].text)
                exchanges[key] = value

        result = exchanges[currency1] / exchanges[currency2]
        return result


    def getExchangeRates(self, currency1, currency2, days):
        pass

    def parseDate(self, date):
        return date.strftime("%d.%m.%Y")