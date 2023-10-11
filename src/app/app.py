import random
import time

from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import base64
from io import BytesIO

from src.parser.parser import Parser
from src.plotter.plotter import Plotter
from src.predictor.predictor import Predictor


class Stub:
    def __init__(self, currency_a: str):
        self.cur_a = currency_a
        self.conversion_rate = 60  # Constant conversion rate of 60

    def to(self, currency_b):
        values = 6

        # Generate random data for currency_b based on conversion rate
        converted_data = [random.random() * self.conversion_rate for x in range(values)]

        fig = Plotter(converted_data, converted_data).get_plot()

        return fig


class Server:
    def __init__(self):
        self.templates = Jinja2Templates(directory="templates")
        self.parser = Parser()
        self.predictor = Predictor()
        self.router = APIRouter()
        self.__register_routes()
        self.counter = 1

    async def __index(self, request: Request):
        return self.templates.TemplateResponse('index.html', {'request': request, 'counter': self.counter})

    async def __plot_graph(self, currency_a: str, currency_b: str):
        start_time = time.time()  # Start measuring time

        print('Server.__plot_graph: plotting started')
        if currency_a == currency_b:
            raise HTTPException(status_code=400, detail="can't convert the same currency")

        if currency_a == "":
            raise HTTPException(status_code=400, detail="currency_a can't be empty")

        if currency_b == "":
            raise HTTPException(status_code=400, detail="currency_b can't be empty")

        days = 64
        exchange_rate = await self.parser.getExchangeRates(currency_a, currency_b, days)
        print('Server.__plot_graph.parser.getExchangeRates: got data for {} days, took: {:.2f} seconds'.format(
            days,
            time.time() - start_time))
        start_time = time.time()  # Update the start time

        exchange_rate7days = exchange_rate[-7:]

        extrapolated_exchange_rate = self.predictor.extrapolate_currency_rate(exchange_rate)[:7]
        print('Server.__plot_graph.predictor.extrapolate_currency_rate: got a prediction, took: {:.2f} seconds'.format(
            time.time() - start_time))
        start_time = time.time()  # Update the start time

        plotter = Plotter(exchange_rate7days, extrapolated_exchange_rate)
        plotter.plotter_settings.apply_interpolation = True
        graph = plotter.get_plot()
        print('Server.__plot_graph.plotter.get_plot: plotted a graph, took: {:.2f} seconds'.format(
            time.time() - start_time))

        tmpfile = BytesIO()
        graph.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

        print('Server.__plot_graph: plotting end, overall took: {:.2f} seconds'.format(time.time() - start_time))
        return {
            'image': encoded,
            'currency_b_rate': exchange_rate7days[-1],
        }

    async def __get_currencies(self):
        json = self.parser.getCurrencyNames()
        return json

    def __register_routes(self):
        self.router.add_api_route('/', self.__index, methods=['GET'], response_class=HTMLResponse)
        self.router.add_api_route('/plot', self.__plot_graph, methods=['GET'])
        self.router.add_api_route('/currencies', self.__get_currencies, methods=['GET'])
