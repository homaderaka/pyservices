import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.interpolate import interp1d
import numpy as np
from src.plotter.plotter_settings import PlotterSettings


class Plotter:
    def __init__(self, ex_rate_values, predicted_ex_rate_values):
        self.__ex_rate_values = None
        self.__predicted_ex_rate_values = None
        self.set_values(ex_rate_values, predicted_ex_rate_values)

        self.plotter_settings = PlotterSettings()

        self.fig = plt.figure(figsize=self.plotter_settings.figure_size)
        self.__ax = self.fig.add_subplot(1, 1, 1)

    def get_plot(self):
        self.__create_plot()
        return self.fig

    def set_values(self, ex_rate_values, predicted_ex_rate_values):
        self.__ex_rate_values = ex_rate_values.copy()
        self.__predicted_ex_rate_values = predicted_ex_rate_values.copy()

    def get_ex_rate_values(self):
        return self.__ex_rate_values

    def get_predicted_ex_rate_values(self):
        return self.__predicted_ex_rate_values

    def __validate_values(self):
        if not self.__ex_rate_values or not self.__predicted_ex_rate_values:
            raise ValueError("Lists of values cannot be empty")

    def __create_plot(self):
        self.__validate_values()

        last_element = self.__ex_rate_values[-1]
        self.__predicted_ex_rate_values.insert(0, last_element)

        past_dates = [(datetime.today().day - len(self.__ex_rate_values) + i + 1)
                      for i in range(len(self.__ex_rate_values))]
        future_dates = [(datetime.today().day + i)
                        for i in range(len(self.__predicted_ex_rate_values))]

        if self.plotter_settings.apply_interpolation:
            cubic_interpolation_model = interp1d(past_dates, self.__ex_rate_values,
                                                 kind=self.plotter_settings.interpolation_kind)
            x_interpolation = np.linspace(min(past_dates), max(past_dates),
                                          self.plotter_settings.interpolation_amount)
            y_interpolation = cubic_interpolation_model(x_interpolation)

            predicted_cubic_interpolation_model = interp1d(future_dates, self.__predicted_ex_rate_values,
                                                           kind=self.plotter_settings.interpolation_kind)
            predicted_x_interpolation = np.linspace(min(future_dates), max(future_dates),
                                                    self.plotter_settings.interpolation_amount)
            predicted_y_interpolation = predicted_cubic_interpolation_model(predicted_x_interpolation)

            self.__ax.plot(predicted_x_interpolation, predicted_y_interpolation,
                           label=self.plotter_settings.second_line_label,
                           linestyle=self.plotter_settings.second_line_style,
                           linewidth=self.plotter_settings.second_line_width,
                           color=self.plotter_settings.second_line_color)
            self.__ax.plot(x_interpolation, y_interpolation,
                           label=self.plotter_settings.first_line_label,
                           color=self.plotter_settings.first_line_color)
        else:
            self.__ax.plot(future_dates, self.__predicted_ex_rate_values,
                           label=self.plotter_settings.second_line_label,
                           linestyle=self.plotter_settings.second_line_style,
                           linewidth=self.plotter_settings.second_line_width,
                           color=self.plotter_settings.second_line_color)
            self.__ax.plot(past_dates, self.__ex_rate_values,
                           label=self.plotter_settings.first_line_label,
                           marker=self.plotter_settings.first_line_marker,
                           markersize=self.plotter_settings.first_line_marker_size,
                           color=self.plotter_settings.first_line_color)

        self.__ax.set_xlabel(self.plotter_settings.x_label)
        self.__ax.set_ylabel(self.plotter_settings.y_label)

        self.__ax.set_xticks(past_dates + future_dates[1:], self.__generate_xticks(datetime.now()))

        self.__ax.grid(True)

        handles = [plt.Line2D([], [],
                              label=self.plotter_settings.first_line_label,
                              color=self.plotter_settings.first_line_color),
                   plt.Line2D([], [],
                              label=self.plotter_settings.second_line_label,
                              linestyle=self.plotter_settings.second_line_style,
                              linewidth=self.plotter_settings.second_line_width,
                              color=self.plotter_settings.second_line_color)]
        self.__ax.legend(handles=handles,
                         loc=self.plotter_settings.legend_location,
                         ncol=self.plotter_settings.legend_ncol)

    def __generate_xticks(self, date_now):
        current_date = date_now
        start_date = current_date - timedelta(days=(len(self.__ex_rate_values) - 1))
        date_range = []
        for i in range(len(self.__ex_rate_values) + len(self.__predicted_ex_rate_values) - 1):
            date_range.append((start_date + timedelta(days=i)).strftime(self.plotter_settings.strf_time))
        return date_range
