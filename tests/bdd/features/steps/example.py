from behave import *

from src.plotter.plotter import Plotter

use_step_matcher("re")


@given("plotter")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.plotter = Plotter([1, 2], [3, 4])


@when("we use get_plot function")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.res = context.plotter.get_plot()


@then("it does not return None")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.res is not None
