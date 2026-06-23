# Assignment 1 Requirements - Wumpus World Simulator

## Objective
Build a Python simulator for the Wumpus World environment and a NaiveAgent.

## Coordinate System

The grid uses **mathematical coordinates** (not screen coordinates):

- **User Interface Display:**
  - x ranges from 1 to width (left to right)
  - y ranges from 1 to height (bottom to top)
  - [1, 1] = bottom-left corner
  - [4, 4] = top-right corner (for standard 4×4 grid)

- **Internal Code:**
  - For simplicity with array indexing, the environment code may use [0, 0] as the bottom-left corner
  - All direction logic remains consistent with mathematical coordinates

- **Direction Mapping:**
  - NORTH: y increases (move toward top of grid)
  - SOUTH: y decreases (move toward bottom of grid)
  - EAST: x increases (move toward right of grid)
  - WEST: x decreases (move toward left of grid)

## Functional Requirements
- Configurable environment with:
  - width
  - height
  - allowClimbWithoutGold
  - pitProb
- Standard configuration: (4, 4, true, 0.2)
- Agent starts at [1,1] facing right
- Random placement of Wumpus and gold in non-start squares
- Independent pit generation for non-start squares
- Wumpus, gold, and pit may overlap
- Actions:
  - Forward
  - TurnLeft
  - TurnRight
  - Shoot
  - Grab
  - Climb
- Percepts:
  - Stench
  - Breeze
  - Glitter
  - Bump
  - Scream
  - Reward
- Environment returns reward as part of percept
- Agent cannot directly inspect hidden environment state
- Episode ends on death or climb
- Include a simple visualizer
- Include a NaiveAgent with uniform random action selection

## Non-Functional Requirements
- Python
- object-oriented style
- maintain separation between environment state and agent knowledge
- code should be extensible for Assignment 2

## Proposed Modules
- models
- environment
- visualization
- agents
- tests

## Out of Scope for Assignment 1
- safe-cell memory
- planning
- graph search
- shortest path escape logic
- Assignment 2 functionality
