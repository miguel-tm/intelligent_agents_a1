"""
Agents package.

Exports agent classes for the Wumpus World.
"""

from agents.base_agent import Agent
from agents.naive_agent import NaiveAgent

__all__ = [
    "Agent",
    "NaiveAgent",
]
