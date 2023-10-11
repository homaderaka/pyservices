from bs4 import BeautifulSoup
import requests
import datetime

import asyncio
import aiohttp

class Parser:
    def __init__(self):
        self.exchange_rate_cache = {}

    def getCurrencyNames(self):
        url = 'http://cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=10.10.2023'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        currencies = soup.findAll('tr')
        names = {'RUB': "Российский рубль"}

        for currency in currencies:
            data = currency.findAll('td')
            # data[0] - some code
            # data[1] - currency name in format RUB
            # data[2] - currency amount
            # data[3] - currency full name
            # data[4] - currency relation to ruble
            if len(data) == 5:
                key = data[1].text
                value = data[3].text
                names[key] = value
        return names

    async def fetch_exchange_rate(self, session, currency1, currency2, date):
        url = 'http://cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=' + date
        async with session.get(url) as response:
            page = await response.text()
            soup = BeautifulSoup(page, "html.parser")
            currencies = soup.findAll('tr')
            exchanges = {}
            exchanges['RUB'] = 1

            for currency in currencies:
                data = currency.findAll('td')
                if len(data) == 5:
                    key = data[1].text
                    value = float(data[4].text.replace(',', '.')) / float(data[2].text)
                    exchanges[key] = value

            result = exchanges[currency1] / exchanges[currency2]

            # Store the result in the cache
            cache_key = (currency1, currency2, date)
            self.exchange_rate_cache[cache_key] = result

            return result

    async def getExchangeRate(self, currency1, currency2, date):
        cache_key = (currency1, currency2, date)
        if cache_key in self.exchange_rate_cache:
            return self.exchange_rate_cache[cache_key]

        async with aiohttp.ClientSession() as session:
            result = await self.fetch_exchange_rate(session, currency1, currency2, date)
            return result

    async def getExchangeRates(self, currency1, currency2, days):
        today = datetime.datetime.now()
        tasks = []

        for i in range(days):
            substraction = datetime.timedelta(days=i)
            date = self.parseDate(today - substraction)
            task = self.getExchangeRate(currency1, currency2, date)
            tasks.append(task)

        exchangeRates = await asyncio.gather(*tasks)
        exchangeRates.reverse()
        return exchangeRates

    def parseDate(self, date):
        return date.strftime("%d.%m.%Y")