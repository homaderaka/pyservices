Feature: Testing the Server class

  Background:
    Given a Server instance

  Scenario: Valid currency inputs
    When we validate currency inputs for "USD" and "EUR"
    Then there should be no HTTPException

  Scenario: Same currency inputs
    When we validate currency inputs for "USD" and "USD"
    Then there should be an HTTPException with status code 400

  Scenario: Empty currency A
    When we validate currency inputs for "" and "EUR"
    Then there should be an HTTPException with status code 400

  Scenario: Empty currency B
    When we validate currency inputs for "USD" and ""
    Then there should be an HTTPException with status code 400
