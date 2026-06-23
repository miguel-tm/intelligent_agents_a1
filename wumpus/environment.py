"""
Wumpus World environment simulator.

This module implements the WumpusWorld class, which manages the hidden game state
and the mechanics of the environment. The agent never has direct access to the
WumpusWorld object; it only receives Percept objects containing sensory information.

The environment is responsible for:
- Maintaining true positions of wumpus, gold, and pits
- Processing agent actions and updating world state
- Generating percepts based on agent's current position
- Detecting episode termination (death or climb out)
- Computing rewards

Key class:
- WumpusWorld: Main environment manager
"""

from dataclasses import dataclass
from typing import Set, Tuple
from wumpus.models import Action, Direction, Position, Percept, AgentState


# Default game configuration
DEFAULT_WIDTH = 4
DEFAULT_HEIGHT = 4
DEFAULT_ALLOW_CLIMB_WITHOUT_GOLD = True
DEFAULT_PIT_PROBABILITY = 0.2


class WumpusWorld:
    """
    Manages the Wumpus World environment and its hidden state.
    
    The environment maintains:
    - The true position of the wumpus
    - The true position of the gold
    - The true positions of all pits
    - Whether the arrow has been used
    - The agent's current position and direction (observable from the agent's actions)
    
    The agent CANNOT access these directly. The agent only receives Percepts through
    the step() method. This enforces the constraint that the agent learns about the
    world only through its senses.
    
    Attributes:
        width: Grid width (default 4)
        height: Grid height (default 4)
        allow_climb_without_gold: If True, agent can climb out at [1,1] anytime
        pit_probability: Probability that each non-start cell contains a pit
        
    TODO: Implement initialization, step logic, percept generation, and termination detection
    """

    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        allow_climb_without_gold: bool = DEFAULT_ALLOW_CLIMB_WITHOUT_GOLD,
        pit_probability: float = DEFAULT_PIT_PROBABILITY,
    ):
        """
        Initialize a new Wumpus World environment.
        
        Args:
            width: Grid width (must be > 1)
            height: Grid height (must be > 1)
            allow_climb_without_gold: If True, agent can climb out anytime at [1,1]
            pit_probability: Probability of pit at each non-start square (0.0 to 1.0)
        """
        self.width = width
        self.height = height
        self.allow_climb_without_gold = allow_climb_without_gold
        self.pit_probability = pit_probability

        # Hidden state (agent cannot access directly)
        self._wumpus_pos: Position | None = None
        self._gold_pos: Position | None = None
        self._pit_positions: Set[Position] = set()
        self._arrow_used: bool = False

        # Agent's current state (observable through actions/percepts)
        self._agent_pos: Position | None = None
        self._agent_direction: Direction | None = None

        # Episode state
        self._episode_ended: bool = False
        self._agent_dead: bool = False

        # Initialize the world
        self._initialize_world()

    def _initialize_world(self) -> None:
        """
        Initialize the world with random wumpus, gold, and pit placements.
        
        Placement rules:
        - Wumpus: Random position in non-start squares
        - Gold: Random position in non-start squares
        - Pits: Each non-start square has pit_probability chance of containing a pit
        - Wumpus, gold, and pits may overlap
        
        Agent starts at [1,1] facing right (EAST).
        
        TODO: Implement world initialization with random placements
        """
        # TODO: Implement
        pass

    def reset(self) -> AgentState:
        """
        Reset the environment to initial state.
        
        Returns:
            AgentState representing the agent's initial state (position [1,1], facing EAST)
            
        TODO: Implement reset logic
        """
        # TODO: Implement
        pass

    def step(self, action: Action) -> Tuple[Percept, bool]:
        """
        Execute one action in the environment and return sensory feedback.
        
        Args:
            action: The action to execute (from Action enum)
            
        Returns:
            Tuple of:
            - Percept: Sensory information (stench, breeze, glitter, bump, scream, reward)
            - bool: True if episode has ended (agent dead or climbed out), False otherwise
            
        Action effects:
        - FORWARD: Move one step forward (if within bounds)
        - TURN_LEFT: Rotate direction (no position change)
        - TURN_RIGHT: Rotate direction (no position change)
        - SHOOT: Fire arrow in facing direction (kills wumpus if hit)
        - GRAB: Pick up gold at current location
        - CLIMB: Exit environment (only at [1,1], returns success/failure)
        
        TODO: Implement action execution and state updates
        """
        # TODO: Implement
        pass

    def get_percepts_at(self, position: Position) -> Percept:
        """
        Generate the percept sensed at a given position.
        
        This is the core sensing function. It detects:
        - Stench: If wumpus is in an adjacent square
        - Breeze: If a pit is in an adjacent square
        - Glitter: If gold is at this position
        - Bump: Not generated here (set by step() when movement is blocked)
        - Scream: Not generated here (set by step() when wumpus is killed)
        - Reward: Computed based on action and outcome
        
        Args:
            position: The position to sense from
            
        Returns:
            Percept object with sensory data
            
        TODO: Implement sensory detection
        """
        # TODO: Implement
        pass

    def _is_adjacent(self, pos1: Position, pos2: Position) -> bool:
        """
        Check if two positions are adjacent (Manhattan distance = 1).
        
        Adjacent means horizontally or vertically neighboring, not diagonally.
        
        TODO: Implement adjacency check
        """
        # TODO: Implement
        pass

    def _compute_reward(self, action: Action, outcome: str) -> float:
        """
        Compute the reward for an action based on the outcome.
        
        Standard rewards (may be customized):
        - Each action: -1
        - Grabbing gold: +1 (or more)
        - Death (pit/wumpus): -10
        - Climbing with gold at [1,1]: +1000
        - Climbing without gold: 0 (or negative)
        
        Args:
            action: The action taken
            outcome: String describing the outcome ("success", "pit", "wumpus", etc.)
            
        Returns:
            Reward value
            
        TODO: Implement reward computation
        """
        # TODO: Implement
        pass

    def is_episode_ended(self) -> bool:
        """Return True if episode has ended (death or escape)."""
        return self._episode_ended

    def is_agent_alive(self) -> bool:
        """Return True if agent is still alive."""
        return not self._agent_dead

    def get_agent_position(self) -> Position:
        """Return agent's current position."""
        if self._agent_pos is None:
            raise RuntimeError("Agent position not initialized")
        return self._agent_pos

    def get_agent_direction(self) -> Direction:
        """Return agent's current facing direction."""
        if self._agent_direction is None:
            raise RuntimeError("Agent direction not initialized")
        return self._agent_direction
