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

class Server:
    def __init__(self):
        self.templates = Jinja2Templates(directory="templates")
        self.parser = Parser()
        self.predictor = Predictor()
        self.router = APIRouter()
        self.__register_routes()
        self.counter = 1
        self.graph = None

    async def __index(self, request: Request):
        return self.templates.TemplateResponse('index.html', {'request': request, 'counter': self.counter})

    async def __plot_graph(self, currency_a: str, currency_b: str):
        start_time = time.time()  # Start measuring time

        print('Server.__plot_graph: plotting started')
        self.validate_currency_inputs(currency_a, currency_b)

        exchange_rate = await self.parser.getExchangeRates(currency_a, currency_b, 64)
        print('Server.__plot_graph.parser.getExchangeRates: got data, took: {:.2f} seconds'.format(time.time() - start_time))

        exchange_rate7days = exchange_rate[-7:]
        print(exchange_rate7days)

        extrapolated_exchange_rate = self.predictor.extrapolate_currency_rate(exchange_rate7days.copy())[7:]
        print('Server.__plot_graph.predictor.extrapolate_currency_rate: got a prediction, took: {:.2f} seconds'.format(
            time.time() - start_time))

        self.graph = self.generate_currency_plot(exchange_rate7days, extrapolated_exchange_rate)
        print('Server.__plot_graph.plotter.get_plot: plotted a graph, took: {:.2f} seconds'.format(
            time.time() - start_time))

        encoded = self.encode_graph()
        print('Server.__plot_graph: plotting end, overall took: {:.2f} seconds'.format(time.time() - start_time))
        return {
            'image': encoded,
            'currency_b_rate': exchange_rate7days[-1],
        }

    def validate_currency_inputs(self, currency_a, currency_b):
        raise 1
        if currency_a == currency_b:
            raise HTTPException(status_code=400, detail="Can't convert the same currency")

        if currency_a == "":
            raise HTTPException(status_code=400, detail="Currency A can't be empty")

        if currency_b == "":
            raise HTTPException(status_code=400, detail="Currency B can't be empty")

    def generate_currency_plot(self, exchange_rate7days, extrapolated_exchange_rate):
        plotter = Plotter(exchange_rate7days, extrapolated_exchange_rate)
        plotter.plotter_settings.apply_interpolation = True
        return plotter.get_plot()

    def encode_graph(self):
        tmpfile = BytesIO()
        self.graph.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return None

    async def __get_currencies(self):
        json = self.parser.getCurrencyNames()
        return None

    def __register_routes(self):
        self.router.add_api_route('/', self.__index, methods=['GET'], response_class=HTMLResponse)
        self.router.add_api_route('/plot', self.__plot_graph, methods=['GET'])
        self.router.add_api_route('/currencies', self.__get_currencies, methods=['GET'])
