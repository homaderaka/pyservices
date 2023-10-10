import matplotlib.pyplot as plt

from datetime import datetime, timedelta


class Plotter:
    def __init__(self, past_values, future_predictions):
        self.__past_values = None
        self.__future_predictions = None
        self.set_values(past_values, future_predictions)

        self.fig = plt.figure(figsize=(12, 5))
        self.__ax = self.fig.add_subplot(1, 1, 1)

    def get_plot(self):
        self.__create_plot()
        return self.fig

    def set_values(self, past_values, future_predictions):
        self.__past_values = past_values.copy()
        self.__future_predictions = future_predictions.copy()

    def __validate_values(self):
        if not self.__past_values or not self.__future_predictions:
            raise ValueError("Списки значений не могут быть пустыми")

    def __create_plot(self):
        self.__validate_values()

        past_dates = [(datetime.today().day - len(self.__past_values) + i + 1) for i in range(len(self.__past_values))]
        future_dates = [(datetime.today().day + i) for i in range(len(self.__future_predictions) + 1)]

        last_element = self.__past_values[-1]
        self.__future_predictions.insert(0, last_element) # здесь изменяешь элемент по ссылке на слайс, это небезопасно

        self.__ax.plot(past_dates, self.__past_values, marker='o', markersize=4)
        self.__ax.plot(future_dates, self.__future_predictions, marker='o', markersize=4)

        self.__ax.set_xlabel('Дата')
        self.__ax.set_ylabel('Цена')

        self.__ax.set_xticks(past_dates + future_dates[1:], self.__generate_xticks())

        self.__ax.grid(True)

        return plt

    def __generate_xticks(self):
        current_date = datetime.now()
        start_date = current_date - timedelta(days=(len(self.__past_values) - 1))
        date_range = []
        for i in range(len(self.__past_values) + len(self.__future_predictions) - 1):
            date_range.append((start_date + timedelta(days=i)).strftime("%d-%m"))
        return date_range
