Feature: adding behave tests

  Scenario: run a simple test
     Given plotter
      When we use get_plot function
      Then it does not return None