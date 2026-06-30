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

import random
from dataclasses import dataclass
from typing import List, Set, Tuple
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
        - Wumpus: Uniformly random from non-start squares (use random.choice())
        - Gold: Uniformly random from non-start squares (use random.choice())
        - Pits: Each non-start square has pit_probability chance of containing a pit
        - Wumpus, gold, and pits may overlap
        
        Agent starts at [1,1] (or [0,0] internally) facing right (EAST).
        
        Coordinate system: Internal uses [0,0] at bottom-left for array simplicity.
        """
        # Create list of all non-start positions
        non_start_positions = [
            Position(x, y)
            for x in range(self.width)
            for y in range(self.height)
            if not self._is_start_position(Position(x, y))
        ]
        
        # Place wumpus: uniformly random from non-start squares
        self._wumpus_pos = random.choice(non_start_positions)
        
        # Place gold: uniformly random from non-start squares
        self._gold_pos = random.choice(non_start_positions)
        
        # Generate pits: each non-start square independently has pitProb chance
        self._pit_positions = set()
        for pos in non_start_positions:
            if random.random() < self.pit_probability:
                self._pit_positions.add(pos)
        
        # Initialize agent at start position facing EAST
        self._agent_pos = Position(0, 0)  # Internal coordinates
        self._agent_direction = Direction.EAST
        self._arrow_used = False
        
        # Reset episode flags
        self._episode_ended = False
        self._agent_dead = False

    def _is_start_position(self, pos: Position) -> bool:
        """Check if a position is the starting position [1,1] (or [0,0] internally)."""
        return pos.x == 0 and pos.y == 0

    def reset(self) -> AgentState:
        """
        Reset the environment to initial state.
        
        Returns:
            AgentState representing the agent's initial state (position [1,1], facing EAST)
        """
        self._initialize_world()
        return AgentState(
            position=Position(1, 1),  # Return UI coordinates
            direction=Direction.EAST,
            has_gold=False,
            is_alive=True,
            has_arrow=True,
        )

    def step(self, action: Action) -> Tuple[Percept, bool]:
        """
        Execute one action in the environment and return sensory feedback.
        
        Args:
            action: The action to execute (from Action enum)
            
        Returns:
            Tuple of:
            - Percept: Sensory information (stench, breeze, glitter, bump, scream, reward)
            - bool: True if episode has ended (agent dead or climbed out), False otherwise
        """
        if self._episode_ended:
            # Episode already ended, return empty percept
            return Percept(reward=-1), True
        
        bump = False
        scream = False
        reward = -1  # Default time cost
        
        # Execute action
        if action == Action.FORWARD:
            # Try to move forward
            next_pos = self._agent_direction.get_forward_position(self._agent_pos)
            if next_pos.is_valid(self.width, self.height):
                self._agent_pos = next_pos
                # Check if died
                if self._check_death_condition(self._agent_pos):
                    self._agent_dead = True
                    self._episode_ended = True
                    reward = -1000  # Death penalty (pit or wumpus)
            else:
                bump = True
        
        elif action == Action.TURN_LEFT:
            self._agent_direction = self._agent_direction.turn_left()
        
        elif action == Action.TURN_RIGHT:
            self._agent_direction = self._agent_direction.turn_right()
        
        elif action == Action.SHOOT:
            if not self._arrow_used:
                self._arrow_used = True
                reward = -11  # Time cost (-1) + arrow penalty (-10)
                # Check if arrow hits wumpus
                if self._wumpus_in_direction(self._agent_direction):
                    self._wumpus_pos = None  # Wumpus is dead
                    scream = True
        
        elif action == Action.GRAB:
            if self._agent_pos == self._gold_pos:
                self._gold_pos = None  # Gold picked up
                reward = -1  # No bonus; only time cost
        
        elif action == Action.CLIMB:
            if self._is_start_position(self._agent_pos):
                # Agent is at start position [1,1]
                if self._gold_pos is None:
                    # Agent has gold: successful escape!
                    self._episode_ended = True
                    reward = 1000
                elif self.allow_climb_without_gold:
                    # No gold, but allowed to climb
                    self._episode_ended = True
                    reward = -1  # Only time cost
                # else: No gold and not allowed—climb fails silently, no effect
            # else: Not at start position—climb fails silently, no effect
        
        # Generate percept at current position
        if action == Action.CLIMB and self._episode_ended:
            # Special percept when exiting cave
            percept = Percept(
                stench=False,
                breeze=False,
                glitter=(self._gold_pos is None),  # True if agent picked up gold
                bump=False,
                scream=scream,
                reward=reward
            )
        else:
            percept = self.get_percepts_at(self._agent_pos)
            percept.bump = bump
            percept.scream = scream
            percept.reward = reward
        
        return percept, self._episode_ended

    def get_percepts_at(self, position: Position) -> Percept:
        """
        Generate the percept sensed at a given position.
        
        Detects:
        - Stench: If wumpus is in an adjacent square and alive
        - Breeze: If a pit is in an adjacent square
        - Glitter: If gold is at this position
        - Bump: Set by step() when movement is blocked
        - Scream: Set by step() when wumpus is killed
        - Reward: Set by step() based on action outcome
        
        Args:
            position: The position to sense from
            
        Returns:
            Percept object with sensory data
        """
        stench = False
        breeze = False
        glitter = False
        
        # Stench: wumpus is adjacent and alive
        if self._wumpus_pos is not None and self._is_adjacent(position, self._wumpus_pos):
            stench = True
        
        # Breeze: any pit is adjacent
        for pit_pos in self._pit_positions:
            if self._is_adjacent(position, pit_pos):
                breeze = True
                break
        
        # Glitter: gold is at this position
        if self._gold_pos is not None and position == self._gold_pos:
            glitter = True
        
        return Percept(stench=stench, breeze=breeze, glitter=glitter)

    def _is_adjacent(self, pos1: Position, pos2: Position) -> bool:
        """
        Check if two positions are adjacent (Manhattan distance = 1).
        
        Adjacent means horizontally or vertically neighboring, not diagonally.
        """
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y) == 1

    def _check_death_condition(self, pos: Position) -> bool:
        """Check if agent dies at this position (pit or living wumpus)."""
        if pos in self._pit_positions:
            return True
        if self._wumpus_pos is not None and pos == self._wumpus_pos:
            return True
        return False

    def _wumpus_in_direction(self, direction: Direction) -> bool:
        """Check if wumpus is in the given direction (in straight line from agent)."""
        if self._wumpus_pos is None:
            return False
        
        # Get all positions in the given direction until edge
        positions_in_direction = []
        current_pos = self._agent_pos
        
        while True:
            current_pos = direction.get_forward_position(current_pos)
            if not current_pos.is_valid(self.width, self.height):
                break
            positions_in_direction.append(current_pos)
        
        return self._wumpus_pos in positions_in_direction

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

    def get_death_cause(self) -> str | None:
        """
        Return the cause of death if agent is dead.
        
        Returns:
            "Wumpus" if killed by wumpus
            "Pit" if killed by pit
            None if agent is still alive
        """
        if self.is_agent_alive():
            return None
        
        # Check if agent is at wumpus position
        if self._wumpus_pos is not None and self._agent_pos == self._wumpus_pos:
            return "Wumpus"
        
        # Check if agent is at pit position
        if self._agent_pos in self._pit_positions:
            return "Pit"
        
        # Shouldn't reach here, but return None as fallback
        return None

    def get_wumpus_position(self) -> Position | None:
        """
        Return the true wumpus position (internal coordinates).
        
        WARNING: This exposes hidden world state. It is intended ONLY for
        visualization/debugging (e.g., a "reveal hidden world" overlay). Agents
        must NEVER use this; they receive information solely through Percepts.
        
        Returns:
            The wumpus Position in internal coordinates, or None if uninitialized.
        """
        return self._wumpus_pos

    def get_gold_position(self) -> Position | None:
        """
        Return the true gold position (internal coordinates).
        
        WARNING: Hidden world state, for visualization/debugging only. Agents
        must NEVER use this; they receive information solely through Percepts.
        
        Returns:
            The gold Position in internal coordinates, or None if uninitialized.
        """
        return self._gold_pos

    def get_pit_positions(self) -> Set[Position]:
        """
        Return the true set of pit positions (internal coordinates).
        
        WARNING: Hidden world state, for visualization/debugging only. Agents
        must NEVER use this; they receive information solely through Percepts.
        
        Returns:
            A copy of the set of pit Positions in internal coordinates.
        """
        return set(self._pit_positions)
