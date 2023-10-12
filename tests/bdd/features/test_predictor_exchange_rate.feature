Feature: exchange_rates function

  Scenario: checking exchange rates
     Given there is a Predictor object
      When exchange_rates method is called
      Then exchange rate must be correct
