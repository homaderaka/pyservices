from behave import *
from src.app.app import Server  # Replace 'your_module' with the actual module path

use_step_matcher("re")

# Initialize the context.server instance in the Background
@given("a Server instance")
def initialize_server_instance(context):
    context.server = Server()

@when('we validate currency inputs for "USD" and "EUR"')
def validate_currency_inputs_usd_eur(context):
    try:
        context.server.validate_currency_inputs("USD", "EUR")
        context.exception = None  # No exception raised
    except Exception as e:
        context.exception = e

@then("there should be no HTTPException")
def check_no_http_exception(context):
    assert context.exception is None


@when('we validate currency inputs for "USD" and "USD"')
def step_impl(context):
    try:
        context.server.validate_currency_inputs("USD", "USD")
        context.exception = None  # No exception raised
    except Exception as e:
        context.exception = e

@then("there should be an HTTPException with status code 400")
def step_impl(context):
    assert context.exception is not None
    assert context.exception.status_code == 400

@when('we validate currency inputs for "" and "EUR"')
def step_impl(context):
    try:
        context.server.validate_currency_inputs("", "EUR")
        context.exception = None  # No exception raised
    except Exception as e:
        context.exception = e

@when('we validate currency inputs for "USD" and ""')
def step_impl(context):
    try:
        context.server.validate_currency_inputs("USD", "")
        context.exception = None  # No exception raised
    except Exception as e:
        context.exception = e