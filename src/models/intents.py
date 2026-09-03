"""
Intent definitions used across the NexaAssist application.

Every module (classifier, router, assistant, tests)
imports these intents to avoid hardcoded strings.
"""

from enum import Enum


class Intent(Enum):
    POLICY_QUERY = "POLICY_QUERY"
    EMPLOYEE_DATA = "EMPLOYEE_DATA"
    ACTION_REQUEST = "ACTION_REQUEST"
    UNKNOWN = "UNKNOWN"