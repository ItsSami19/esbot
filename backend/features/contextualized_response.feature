Feature: Get contextualized response
  As a student
  I want to ask a course-related question
  So that I receive a structured and understandable explanation

  Background:
    Given a student has an active learning session

  Scenario: Student asks a course-related question and receives a structured explanation
    Given the explanation AI provider is available
    When the student asks the question "What is unit testing?"
    Then ESBot returns a structured explanation about "unit testing"
    And the explanation contains the sentence "Unit testing verifies small isolated parts of code."

  Scenario: Student asks a vague question and receives a clarification response
    Given the explanation AI provider is available
    When the student asks the question "Can you explain this?"
    Then ESBot returns a clarification response
    And the response asks the student to provide more context

  Scenario: Explanation generation fails and ESBot returns a fallback message
    Given the explanation AI provider is unavailable
    When the student asks the question "What is unit testing?"
    Then ESBot returns a fallback message
    And the response contains the message "The explanation could not be generated at the moment. Please try again later."