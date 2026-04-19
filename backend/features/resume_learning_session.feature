Feature: Resume existing learning session
  As a student
  I want to continue an earlier learning session
  So that I can keep working with my previous context

  Scenario: Student resumes an existing session and previous context is available
    Given a learning session with the title "Testing Basics" exists
    And the session contains the previous message "What is black box testing?"
    When the student resumes the learning session
    Then ESBot loads the existing learning session
    And the previous message "What is black box testing?" is available

  Scenario: Student tries to resume a non-existing session
    Given no learning session exists for the requested session identifier
    When the student tries to resume the learning session
    Then ESBot returns a message that the session could not be found