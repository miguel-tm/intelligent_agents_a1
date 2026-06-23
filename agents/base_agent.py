"""
Abstract base class for all agents in the Wumpus World.

This module defines the Agent interface that all concrete agents must implement.
By requiring agents to inherit from this class, we ensure that agents can only
interact with the environment through percepts, preventing hidden-state cheating.

Key class:
- Agent: Abstract base class for all agent implementations
"""

from abc import ABC, abstractmethod
from wumpus.models import Action, Percept


class Agent(ABC):
    """
    Abstract base class for all Wumpus World agents.
    
    An agent interacts with the environment by:
    1. Receiving a Percept (sensory information)
    2. Computing an Action based on that percept and internal memory
    3. Sending the action to the environment
    
    An agent CANNOT:
    - Access the WumpusWorld object directly
    - Inspect hidden state (wumpus location, pit locations, etc.)
    - Look ahead to see results of actions
    
    Subclasses must implement:
    - get_action(percept): Select the next action based on sensory input
    - reset(): Prepare for a new episode
    
    Optional:
    - update_state(percept): Track beliefs or statistics (for stateful agents)
    
    Design note:
        By requiring all agents to inherit from this class and enforcing
        percept-only communication, we maintain the constraint that agents
        cannot cheat by inspecting the environment directly.
    """

    @abstractmethod
    def get_action(self, percept: Percept) -> Action:
        """
        Select an action based on the current percept.
        
        This is the main decision-making method. The agent receives sensory
        information and must choose an action. The implementation may maintain
        internal state (beliefs, memory, etc.) to inform the decision.
        
        Args:
            percept: Sensory information from the environment
                     (stench, breeze, glitter, bump, scream, reward)
            
        Returns:
            The selected action (from Action enum)
            
        Important:
            The agent has NO access to the world's hidden state. The only
            information available is the percept and the agent's memory.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the agent for a new episode.
        
        This method is called at the start of each new game to clear any
        internal state from the previous episode. Agents should reset:
        - Any beliefs about the world
        - Any memory of past actions
        - Any internal statistics
        
        Typically called by the main game loop before starting a new episode.
        """
        pass

    def update_state(self, percept: Percept) -> None:
        """
        Optional method for agents to update internal state based on percepts.
        
        Some agents may want to track beliefs or statistics. This method allows
        them to update that state when a percept is received. The default
        implementation does nothing.
        
        Args:
            percept: The most recent percept received
        """
        # Default: do nothing
        pass
