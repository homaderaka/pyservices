import datetime
import random

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import matplotlib.pyplot as plt
import base64
from io import BytesIO


class Stub:
    def __init__(self, currency_a: str):
        self.cur_a = currency_a
        self.conversion_rate = 60  # Constant conversion rate of 60

    def to(self, currency_b):
        values = 5

        # Generate random data for currency_b based on conversion rate
        converted_data = [random.random() * self.conversion_rate for x in range(values)]

        # Generate date labels for x-axis (assumed one data point per day)
        start_date = datetime.date(2023, 1, 1)
        date_labels = [start_date + datetime.timedelta(days=i) for i in range(values)]

        # Create a figure
        fig, ax = plt.subplots()

        # Plot the converted data
        ax.plot(date_labels, converted_data, label=f'{currency_b} Data')

        # Set labels and title
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.set_title('Currency Conversion Stub Graph')

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Add a legend
        ax.legend()

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
