"""
NaiveAgent implementation for the Wumpus World.

This module implements a simple agent that selects actions uniformly at random
from the set of available actions. It has no memory and makes no attempt to
learn or plan. This serves as a baseline agent for testing the environment.

Key class:
- NaiveAgent: Random action selection agent
"""

import random
from agents.base_agent import Agent
from wumpus.models import Action, Percept


class NaiveAgent(Agent):
    """
    A simple agent that selects actions uniformly at random.
    
    The NaiveAgent makes no attempt to learn about the environment or plan ahead.
    It simply picks one of the six available actions at random for each decision.
    
    This agent is useful for:
    - Testing that the environment works correctly
    - Establishing a baseline for agent performance
    - Verifying that the environment properly enforces action constraints
    
    Note:
        This agent's behavior is completely stateless (aside from the required
        interface). It does not remember anything about previous percepts.
    """

    def __init__(self):
        """Initialize the NaiveAgent."""
        self._episode_count = 0

    def get_action(self, percept: Percept) -> Action:
        """
        Select a random action from the available actions.
        
        Args:
            percept: The current percept (ignored by this agent)
            
        Returns:
            A randomly selected action
        """
        return random.choice(list(Action))

    def reset(self) -> None:
        """
        Reset the agent for a new episode.
        
        For the NaiveAgent, this is a no-op since it has no internal state.
        It's implemented to satisfy the Agent interface.
        """
        pass
