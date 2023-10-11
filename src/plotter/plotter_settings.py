
class PlotterSettings:
    def __init__(self):
        self.figure_size = (12, 5)

        self.apply_interpolation = False
        self.interpolation_kind = 'cubic'
        self.interpolation_amount = 500

        self.x_label = 'Дата'
        self.y_label = 'Цена'

        self.first_line_label = 'Курс'
        self.first_line_color = 'blue'
        self.first_line_marker = 'o'
        self.first_line_marker_size = 4

        self.second_line_label = 'Прогноз'
        self.second_line_color = 'orange'
        self.second_line_style = '--'
        self.second_line_width = 1.0

        self.legend_location = 'upper left'
        self.legend_ncol = 2

        self.strf_time = '%d-%m'
