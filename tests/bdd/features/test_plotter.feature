Feature: create_plot function

  Scenario: checking past values
     Given there is a Plotter object
      When create_plot method is called
      Then past values list must be correct

  Scenario: checking future values
     Given there is a Plotter object
      When create_plot method is called
      Then future predictions list must be correct

  Scenario: checking the presence of a graph
     Given there is a Plotter object
      When create_plot method is called
      Then figure must contain any graph