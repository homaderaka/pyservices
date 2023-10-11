from behave import given, when, then

from src.parser.parser import Parser


@given('there is a Parser object')
def create_parser_object(context):
    context.parser = Parser()


@when('getCurrencyNames method is called')
def call_get_currency_names(context):
    context.result = context.parser.getCurrencyNames()


@then('all dictionary keys (currencies short names) have length - 3')
def check_keys(context):
    all_keys_have_length_3 = True
    for key, value in context.result.items():
        if len(key) != 3:
            all_keys_have_length_3 = False

    assert all_keys_have_length_3 is True, \
        "Not all dictionary keys (currencies short names) have length - 3"


@then('all dictionary values (currencies full names) have length bigger than 3')
def check_values(context):
    all_values_have_length_bigger_than_3 = True
    for key, value in context.result.items():
        if len(value) <= 3:
            all_values_have_length_bigger_than_3 = False

    assert all_values_have_length_bigger_than_3 is True, \
        "Not all dictionary values (currencies full names) have length bigger than 3"


@then('result should contain non-empty dictionary')
def check_dictionary(context):
    is_dictionary = isinstance(context.result, dict)
    non_empty = len(context.result) > 0
    assert is_dictionary and non_empty is True, \
        "result is not a non-empty dictionary"


@when("getExchangeRates method is called with variables 'USD', 'RUB' and 7")
def call_get_exchange_rates(context):
    context.exchange_rates = context.parser.getExchangeRates('USD', 'RUB', 7)


@then('Have list of 7 exchange rates for 7 days')
def check_dictionary(context):
    len_of_array_is_7 = len(context.exchange_rates) == 7
    assert len_of_array_is_7 is True, \
        "result is not an array of 7 exchange rates"