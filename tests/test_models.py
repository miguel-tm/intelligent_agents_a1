"""
Tests for the core data models.

This module contains unit tests for all model classes defined in wumpus.models:
- Direction: Enum for agent facing direction
- Action: Enum for agent actions
- Position: Dataclass for grid coordinates
- Percept: Dataclass for sensory information
- AgentState: Dataclass for agent's internal state

These tests ensure the foundational data structures work correctly in isolation.
"""

import pytest
from wumpus import Direction, Action, Position, Percept, AgentState


class TestDirection:
    """Tests for the Direction enum and its methods."""

    def test_all_directions_defined(self):
        """
        Test that all four cardinal directions are defined.
        
        Required directions: NORTH, EAST, SOUTH, WEST
        """
        assert hasattr(Direction, 'NORTH')
        assert hasattr(Direction, 'EAST')
        assert hasattr(Direction, 'SOUTH')
        assert hasattr(Direction, 'WEST')

    def test_direction_values_unique(self):
        """
        Test that direction values are unique.
        """
        directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        assert len(directions) == len(set(directions))

    def test_turn_left_from_east(self):
        """
        Test that turning left from EAST results in NORTH.
        
        NORTH
          ^
          |
        W-+-E  (EAST turns left to NORTH)
          |
          v
        SOUTH
        """
        assert Direction.EAST.turn_left() == Direction.NORTH

    def test_turn_left_from_north(self):
        """Test that turning left from NORTH results in WEST."""
        assert Direction.NORTH.turn_left() == Direction.WEST

    def test_turn_left_from_west(self):
        """Test that turning left from WEST results in SOUTH."""
        assert Direction.WEST.turn_left() == Direction.SOUTH

    def test_turn_left_from_south(self):
        """Test that turning left from SOUTH results in EAST."""
        assert Direction.SOUTH.turn_left() == Direction.EAST

    def test_turn_right_from_east(self):
        """
        Test that turning right from EAST results in SOUTH.
        
        NORTH
          ^
          |
        W-+-E  (EAST turns right to SOUTH)
          |
          v
        SOUTH
        """
        assert Direction.EAST.turn_right() == Direction.SOUTH

    def test_turn_right_from_south(self):
        """Test that turning right from SOUTH results in WEST."""
        assert Direction.SOUTH.turn_right() == Direction.WEST

    def test_turn_right_from_west(self):
        """Test that turning right from WEST results in NORTH."""
        assert Direction.WEST.turn_right() == Direction.NORTH

    def test_turn_right_from_north(self):
        """Test that turning right from NORTH results in EAST."""
        assert Direction.NORTH.turn_right() == Direction.EAST

    def test_four_left_turns_full_circle(self):
        """Test that four left turns return to original direction."""
        direction = Direction.EAST
        for _ in range(4):
            direction = direction.turn_left()
        assert direction == Direction.EAST

    def test_four_right_turns_full_circle(self):
        """Test that four right turns return to original direction."""
        direction = Direction.NORTH
        for _ in range(4):
            direction = direction.turn_right()
        assert direction == Direction.NORTH

    def test_get_forward_position_facing_east(self):
        """
        Test forward position when facing EAST (moving right).
        
        From [1, 1] facing EAST, forward should be [2, 1]
        """
        pos = Position(1, 1)
        next_pos = Direction.EAST.get_forward_position(pos)
        assert next_pos.x == 2
        assert next_pos.y == 1

    def test_get_forward_position_facing_west(self):
        """
        Test forward position when facing WEST (moving left).
        
        From [2, 1] facing WEST, forward should be [1, 1]
        """
        pos = Position(2, 1)
        next_pos = Direction.WEST.get_forward_position(pos)
        assert next_pos.x == 1
        assert next_pos.y == 1

    def test_get_forward_position_facing_north(self):
        """
        Test forward position when facing NORTH (moving up).
        
        From [1, 2] facing NORTH, forward should be [1, 3].
        Mathematical coordinates: y increases upward.
        """
        pos = Position(1, 2)
        next_pos = Direction.NORTH.get_forward_position(pos)
        assert next_pos.x == 1
        assert next_pos.y == 3

    def test_get_forward_position_facing_south(self):
        """
        Test forward position when facing SOUTH (moving down).
        
        From [1, 2] facing SOUTH, forward should be [1, 1].
        Mathematical coordinates: y decreases downward.
        """
        pos = Position(1, 2)
        next_pos = Direction.SOUTH.get_forward_position(pos)
        assert next_pos.x == 1
        assert next_pos.y == 1

    def test_get_forward_position_doesnt_modify_original(self):
        """Test that get_forward_position doesn't modify the original position."""
        pos = Position(1, 1)
        Direction.EAST.get_forward_position(pos)
        assert pos.x == 1
        assert pos.y == 1


class TestAction:
    """Tests for the Action enum."""

    def test_all_actions_defined(self):
        """
        Test that all six required actions are defined.
        
        Required actions:
        - FORWARD
        - TURN_LEFT
        - TURN_RIGHT
        - SHOOT
        - GRAB
        - CLIMB
        """
        assert hasattr(Action, 'FORWARD')
        assert hasattr(Action, 'TURN_LEFT')
        assert hasattr(Action, 'TURN_RIGHT')
        assert hasattr(Action, 'SHOOT')
        assert hasattr(Action, 'GRAB')
        assert hasattr(Action, 'CLIMB')

    def test_action_values_unique(self):
        """Test that all action values are unique."""
        actions = [
            Action.FORWARD,
            Action.TURN_LEFT,
            Action.TURN_RIGHT,
            Action.SHOOT,
            Action.GRAB,
            Action.CLIMB,
        ]
        assert len(actions) == len(set(actions))

    def test_action_count(self):
        """Test that there are exactly 6 actions."""
        assert len(list(Action)) == 6

    def test_forward_action_exists(self):
        """Test that FORWARD action is defined and accessible."""
        action = Action.FORWARD
        assert action is not None
        assert isinstance(action, Action)

    def test_turn_actions_exist(self):
        """Test that TURN_LEFT and TURN_RIGHT actions exist."""
        assert Action.TURN_LEFT is not None
        assert Action.TURN_RIGHT is not None

    def test_special_actions_exist(self):
        """Test that SHOOT, GRAB, CLIMB actions exist."""
        assert Action.SHOOT is not None
        assert Action.GRAB is not None
        assert Action.CLIMB is not None


class TestPosition:
    """Tests for the Position dataclass."""

    def test_position_creation(self):
        """Test that Position can be created with x and y coordinates."""
        pos = Position(1, 1)
        assert pos.x == 1
        assert pos.y == 1

    def test_position_with_zero_coordinates(self):
        """Test Position with [0, 0] coordinates."""
        pos = Position(0, 0)
        assert pos.x == 0
        assert pos.y == 0

    def test_position_with_large_coordinates(self):
        """Test Position with large coordinates."""
        pos = Position(100, 200)
        assert pos.x == 100
        assert pos.y == 200

    def test_position_is_immutable(self):
        """Test that Position is frozen (immutable)."""
        pos = Position(1, 1)
        with pytest.raises(AttributeError):
            pos.x = 2

    def test_position_equality(self):
        """Test that two positions with same coordinates are equal."""
        pos1 = Position(1, 1)
        pos2 = Position(1, 1)
        assert pos1 == pos2

    def test_position_inequality(self):
        """Test that positions with different coordinates are not equal."""
        pos1 = Position(1, 1)
        pos2 = Position(1, 2)
        assert pos1 != pos2

    def test_position_hashable(self):
        """Test that Position can be used in sets and as dict keys."""
        pos1 = Position(1, 1)
        pos2 = Position(1, 1)
        pos3 = Position(2, 2)
        
        # Test in set
        positions = {pos1, pos2, pos3}
        assert len(positions) == 2  # pos1 and pos2 are equal
        
        # Test as dict key
        pos_dict = {pos1: "start", pos3: "elsewhere"}
        assert pos_dict[pos2] == "start"  # pos2 equals pos1

    def test_is_valid_within_bounds(self):
        """Test is_valid returns True for positions within bounds."""
        pos = Position(1, 1)
        assert pos.is_valid(4, 4) is True

    def test_is_valid_at_boundary(self):
        """Test is_valid for positions at boundaries."""
        # At corner [0, 0]
        assert Position(0, 0).is_valid(4, 4) is True
        # At corner [3, 3] (max for 4x4)
        assert Position(3, 3).is_valid(4, 4) is True

    def test_is_valid_negative_x(self):
        """Test is_valid returns False for negative x."""
        assert Position(-1, 1).is_valid(4, 4) is False

    def test_is_valid_negative_y(self):
        """Test is_valid returns False for negative y."""
        assert Position(1, -1).is_valid(4, 4) is False

    def test_is_valid_out_of_bounds_x(self):
        """Test is_valid returns False for x outside bounds."""
        assert Position(4, 1).is_valid(4, 4) is False

    def test_is_valid_out_of_bounds_y(self):
        """Test is_valid returns False for y outside bounds."""
        assert Position(1, 4).is_valid(4, 4) is False

    def test_is_valid_different_dimensions(self):
        """Test is_valid with different grid dimensions."""
        pos = Position(5, 3)
        assert pos.is_valid(6, 4) is True
        assert pos.is_valid(5, 4) is False  # x out of bounds
        assert pos.is_valid(6, 3) is False  # y out of bounds

    def test_position_string_representation(self):
        """Test that Position can be converted to string."""
        pos = Position(1, 1)
        str_repr = str(pos)
        assert "1" in str_repr


class TestPercept:
    """Tests for the Percept dataclass."""

    def test_percept_creation_with_defaults(self):
        """Test that Percept can be created with default values."""
        percept = Percept()
        assert percept.stench is False
        assert percept.breeze is False
        assert percept.glitter is False
        assert percept.bump is False
        assert percept.scream is False
        assert percept.reward == 0.0

    def test_percept_has_all_fields(self):
        """Test that Percept has all required fields."""
        percept = Percept(
            stench=True,
            breeze=True,
            glitter=True,
            bump=True,
            scream=True,
            reward=10.5,
        )
        assert percept.stench is True
        assert percept.breeze is True
        assert percept.glitter is True
        assert percept.bump is True
        assert percept.scream is True
        assert percept.reward == 10.5

    def test_percept_default_values(self):
        """Test that Percept defaults to no sensing and zero reward."""
        percept = Percept()
        assert percept.stench is False
        assert percept.breeze is False
        assert percept.glitter is False
        assert percept.bump is False
        assert percept.scream is False
        assert percept.reward == 0.0

    def test_percept_partial_init(self):
        """Test creating Percept with only some fields specified."""
        percept = Percept(glitter=True, reward=1.0)
        assert percept.glitter is True
        assert percept.reward == 1.0
        assert percept.stench is False
        assert percept.breeze is False

    def test_percept_with_negative_reward(self):
        """Test Percept with negative reward."""
        percept = Percept(reward=-10.0)
        assert percept.reward == -10.0

    def test_percept_with_large_reward(self):
        """Test Percept with large positive reward."""
        percept = Percept(reward=1000.0)
        assert percept.reward == 1000.0

    def test_percept_all_true(self):
        """Test Percept with all boolean fields set to True."""
        percept = Percept(
            stench=True,
            breeze=True,
            glitter=True,
            bump=True,
            scream=True,
        )
        assert all([percept.stench, percept.breeze, percept.glitter, percept.bump, percept.scream])

    def test_percept_equality(self):
        """Test that two identical Percepts are equal."""
        p1 = Percept(stench=True, breeze=False, reward=1.0)
        p2 = Percept(stench=True, breeze=False, reward=1.0)
        assert p1 == p2

    def test_percept_inequality(self):
        """Test that different Percepts are not equal."""
        p1 = Percept(stench=True)
        p2 = Percept(stench=False)
        assert p1 != p2


class TestAgentState:
    """Tests for the AgentState dataclass."""

    def test_agent_state_creation(self):
        """Test that AgentState can be created with required fields."""
        pos = Position(1, 1)
        direction = Direction.EAST
        state = AgentState(position=pos, direction=direction)
        
        assert state.position == pos
        assert state.direction == direction

    def test_agent_state_default_beliefs(self):
        """Test that AgentState defaults to alive with no gold/arrow."""
        pos = Position(1, 1)
        state = AgentState(position=pos, direction=Direction.EAST)
        
        assert state.has_gold is False
        assert state.is_alive is True
        assert state.has_arrow is True

    def test_agent_state_with_gold(self):
        """Test AgentState when agent has picked up gold."""
        pos = Position(2, 2)
        state = AgentState(
            position=pos,
            direction=Direction.NORTH,
            has_gold=True,
        )
        
        assert state.has_gold is True
        assert state.position == pos

    def test_agent_state_dead(self):
        """Test AgentState when agent is dead."""
        pos = Position(1, 1)
        state = AgentState(
            position=pos,
            direction=Direction.EAST,
            is_alive=False,
        )
        
        assert state.is_alive is False

    def test_agent_state_no_arrow(self):
        """Test AgentState after arrow is used."""
        pos = Position(1, 1)
        state = AgentState(
            position=pos,
            direction=Direction.EAST,
            has_arrow=False,
        )
        
        assert state.has_arrow is False

    def test_agent_state_full_specification(self):
        """Test AgentState with all fields specified."""
        pos = Position(3, 3)
        state = AgentState(
            position=pos,
            direction=Direction.SOUTH,
            has_gold=True,
            is_alive=True,
            has_arrow=False,
        )
        
        assert state.position == pos
        assert state.direction == Direction.SOUTH
        assert state.has_gold is True
        assert state.is_alive is True
        assert state.has_arrow is False

    def test_agent_state_different_positions(self):
        """Test AgentState tracks different positions correctly."""
        pos1 = Position(1, 1)
        pos2 = Position(2, 2)
        
        state1 = AgentState(position=pos1, direction=Direction.EAST)
        state2 = AgentState(position=pos2, direction=Direction.EAST)
        
        assert state1.position != state2.position

    def test_agent_state_different_directions(self):
        """Test AgentState tracks different directions correctly."""
        pos = Position(1, 1)
        
        state1 = AgentState(position=pos, direction=Direction.EAST)
        state2 = AgentState(position=pos, direction=Direction.NORTH)
        
        assert state1.direction != state2.direction
