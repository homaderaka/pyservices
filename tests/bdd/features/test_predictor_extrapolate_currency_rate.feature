Feature: extrapolate_currency function

  Scenario: checking extrapolation
     Given there is a Predictor object
      When extrapolate_currency method is called
      Then currency values list must be correct

  Scenario: checking amount of predictions
     Given there is a Predictor object
      When extrapolate_currency method is called
      Then currency values list must be at least 9 elements
