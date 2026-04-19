Feature: Evaluate quiz answer
  As a student
  I want to submit an answer to a quiz question
  So that I receive feedback on my understanding

  Background:
    Given a quiz question "What is 2 + 2?" with the correct answer "4" exists

  Scenario: Student submits a correct answer and receives evaluation feedback
    Given the AI provider is available
    When the student submits the answer "4"
    Then ESBot marks the answer as correct
    And ESBot returns the feedback "Correct"
    And ESBot returns the explanation "2 + 2 equals 4."

  Scenario: Student submits an incorrect answer and receives corrective feedback
    Given the AI provider is available
    When the student submits the answer "5"
    Then ESBot marks the answer as incorrect
    And ESBot returns the feedback "Incorrect"
    And ESBot returns the explanation "2 + 2 equals 4."

  Scenario: Student submits an empty answer
    When the student submits an empty answer
    Then ESBot returns a validation message asking for an answer