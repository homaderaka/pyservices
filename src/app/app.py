import random

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import base64
from io import BytesIO

from src.plotter.plotter import Plotter


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
        self.router = APIRouter()
        self.__register_routes()
        self.counter = 1

    async def __index(self, request: Request):
        return self.templates.TemplateResponse('index.html', {'request': request, 'counter': self.counter})

    async def __plot_graph(self, currency_a: str, currency_b: str):
        graph = Stub(currency_a).to(currency_b)

        tmpfile = BytesIO()
        graph.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

        return {'image': encoded}

    def __register_routes(self):
        self.router.add_api_route('/', self.__index, methods=['GET'], response_class=HTMLResponse)
        self.router.add_api_route('/plot', self.__plot_graph, methods=['GET'])
