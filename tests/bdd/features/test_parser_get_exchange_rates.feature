Feature: getExchangeRates function

  Scenario: checking exchange rates
     Given there is a Parser object
      When getExchangeRates method is called with variables 'USD', 'RUB' and 7
      Then Have list of 7 exchange rates for 7 days