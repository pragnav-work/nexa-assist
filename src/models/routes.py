"""
Defines all possible routes inside the Office Assistant.
"""

from enum import Enum


class Route(str, Enum):
    RAG = "RAG"
    EMPLOYEE_DATA = "EMPLOYEE_DATA"
    ACTION = "ACTION"
    UNKNOWN = "UNKNOWN"