Feature: getCurrencyNames function

  Scenario: checking currencies short names
     Given there is a Parser object
      When getCurrencyNames method is called
      Then all dictionary keys (currencies short names) have length - 3

  Scenario: checking currencies full names
     Given there is a Parser object
      When getCurrencyNames method is called
      Then all dictionary values (currencies full names) have length bigger than 3

  Scenario: checking the presence of a dictionary
     Given there is a Parser object
      When getCurrencyNames method is called
      Then result should contain non-empty dictionary