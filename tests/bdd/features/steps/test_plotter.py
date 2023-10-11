from behave import given, when, then

from src.plotter.plotter import Plotter


@given('there is a Plotter object')
def create_currency_plot(context):
    context.currency_plot = Plotter([1, 2, 3], [4, 5, 6])


@when('create_plot method is called')
def call_create_plot(context):
    context.plot = context.currency_plot._Plotter__create_plot()


@then('graph should be created without errors')
def check_plot_created(context):
    assert context.plot is not None, \
        "Plotter was not created"


@then('past values list must be correct')
def check_x_labels(context):
    assert context.currency_plot.get_ex_rate_values() == [1, 2, 3], \
        "Exchange rate values list is not correct"


@then('future predictions list must be correct')
def check_x_labels(context):
    assert context.currency_plot.get_predicted_ex_rate_values() == [3, 4, 5, 6], \
        "Predicted exchange rate values list is not correct"


@then('figure must contain any graph')
def check_x_labels(context):
    assert context.currency_plot.fig.axes is not None, \
        "Figure contains no graphics"
