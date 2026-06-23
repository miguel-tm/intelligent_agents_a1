"""
Main entry point for the Wumpus World simulator.

This script demonstrates running a single episode of the Wumpus World with
a NaiveAgent. It serves as a template for running experiments or testing.

Usage:
    python main.py

Output:
    - Agent decisions and percepts for each turn
    - Final score and episode summary
    - Statistics about the episode (turns taken, actions performed, etc.)

TODO: Implement game loop
TODO: Integrate visualization
TODO: Add command-line arguments for configuration
"""

from wumpus import WumpusWorld, Visualizer
from agents import NaiveAgent
from wumpus.models import Action


def run_episode(
    agent,
    environment: WumpusWorld,
    visualizer: Visualizer | None = None,
    max_turns: int = 1000,
    verbose: bool = True,
) -> dict:
    """
    Run a single episode of the Wumpus World game.
    
    Args:
        agent: The agent to control
        environment: The WumpusWorld environment
        visualizer: Optional Visualizer for rendering (None = no visualization)
        max_turns: Maximum number of turns before forcing episode end
        verbose: If True, print turn information
        
    Returns:
        Dictionary with episode statistics:
        - total_reward: Cumulative reward
        - turns_taken: Number of turns
        - gold_collected: Whether agent found gold
        - escaped: Whether agent escaped with/without gold
        - died: Whether agent died
        
    TODO: Implement episode loop
    """
    # TODO: Implement
    pass


def main() -> None:
    """
    Run the Wumpus World simulator.
    
    Default behavior:
    - Create a 4x4 Wumpus World with standard configuration
    - Run a NaiveAgent in the environment
    - Display output (optional visualization)
    - Print final statistics
    
    TODO: Implement main game loop
    TODO: Add command-line argument parsing for:
        - World size
        - Pit probability
        - Number of episodes
        - Agent type selection
        - Visualization on/off
    """
    # TODO: Implement main function
    print("Wumpus World Simulator - Assignment 1")
    print("=" * 50)
    print("TODO: Implement game loop and visualization")
    print("=" * 50)


if __name__ == "__main__":
    main()
