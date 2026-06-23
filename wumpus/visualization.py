"""
Visualization utilities for the Wumpus World environment.

This module provides tools to display the game state in a human-readable format.
The visualizer shows:
- The agent's position and facing direction
- The agent's current percepts
- The grid with visible symbols
- Game status (alive, dead, gold collected, etc.)

Important: The visualizer only displays what the agent KNOWS or CAN SEE,
not the hidden world state (wumpus location, pit locations, etc.).

Key class:
- Visualizer: Renders the game state
"""

from wumpus.models import AgentState, Direction, Percept


class Visualizer:
    """
    Displays the Wumpus World game state to the user.
    
    The Visualizer shows:
    - The grid with the agent's position
    - The agent's current percepts
    - Game status information
    - Turn count and other statistics
    
    Note:
        The visualizer respects the agent's information constraints and only
        displays information the agent can perceive or deduce.
    
    TODO: Implement grid rendering, symbol drawing, and formatted output
    """

    def __init__(self, width: int, height: int):
        """
        Initialize the Visualizer.
        
        Args:
            width: Grid width
            height: Grid height
        """
        self.width = width
        self.height = height

    def render(
        self,
        agent_state: AgentState,
        percept: Percept,
        turn: int = 0,
        alive: bool = True,
    ) -> None:
        """
        Render the current game state to console output.
        
        Args:
            agent_state: The agent's current state (position, direction, items)
            percept: The agent's current percepts (stench, breeze, glitter, etc.)
            turn: Current turn number (for display purposes)
            alive: Whether the agent is still alive
            
        Displayed information:
        - Grid with agent position and direction arrow
        - Current position and inventory
        - Current percepts
        - Game status
        
        TODO: Implement grid rendering and formatting
        """
        # TODO: Implement
        pass

    def _draw_grid(self, agent_state: AgentState) -> str:
        """
        Generate a string representation of the grid.
        
        Grid symbols:
        - A: Agent (with direction: > ^ v <)
        - .: Empty cell (no known hazards)
        - ?: Unknown cell (not yet visited)
        
        Returns:
            Formatted grid as a string
            
        TODO: Implement grid drawing
        """
        # TODO: Implement
        pass

    def _direction_symbol(self, direction: Direction) -> str:
        """
        Get the symbol representing a direction.
        
        TODO: Implement direction to symbol conversion
        """
        # TODO: Implement
        pass

    def _render_percepts(self, percept: Percept) -> str:
        """
        Format percepts into a readable string.
        
        Returns:
            String like "Stench, Breeze, Glitter" or "No percepts"
            
        TODO: Implement percept formatting
        """
        # TODO: Implement
        pass
