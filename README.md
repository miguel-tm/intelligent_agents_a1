# 📊 Wumpus World Simulator - Assignment 1

**University of Toronto - Intelligent Agents Course**  
**Student:** Miguel Morales (@miguelmog10)

---

## 🎯 Project Purpose

This project implements a **Wumpus World environment simulator** in Python using object-oriented design principles. The simulator is a classic AI problem that challenges agents to navigate a grid-based world, avoid hazards, and find treasure while operating under imperfect information.

### Assignment Scope
This is **Assignment 1 only**. It establishes the foundation for a clean, extensible Wumpus World implementation suitable for future assignments on agent learning and planning.

### Core Components
- **Configurable environment** with random pit, wumpus, and gold placement
- **Percept-based sensing** (stench, breeze, glitter, bump, scream, reward)
- **Action-based agent interface** enforcing separation of concerns
- **NaiveAgent baseline** for testing environment mechanics
- **Extensible architecture** prepared for intelligent agents (Assignment 2+)

---

## 📁 Repository Structure

```
intelligent_agents_a1/
│
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── main.py                        # Entry point for running the simulator
│
├── docs/
│   └── assignment1_requirements.md  # Detailed assignment specification
│
├── wumpus/                        # Core environment package
│   ├── __init__.py               # Package exports
│   ├── models.py                 # Data models (Direction, Action, Position, Percept, AgentState)
│   ├── environment.py            # WumpusWorld class managing hidden state
│   ├── visualization.py          # Visualizer for rendering game state
│   └── utils.py                  # Helper utilities
│
├── agents/                        # Agent package
│   ├── __init__.py               # Package exports
│   ├── base_agent.py             # Abstract Agent class (enforces percept-only interface)
│   └── naive_agent.py            # NaiveAgent (random action selection)
│
└── tests/                         # Test suite
    ├── test_environment.py        # Tests for WumpusWorld
    ├── test_actions.py            # Tests for action mechanics
    └── test_percepts.py           # Tests for percept generation
```

### Module Responsibilities

| Module | Responsibility |
|--------|-----------------|
| **models.py** | Enums and dataclasses: `Direction`, `Action`, `Position`, `Percept`, `AgentState` |
| **environment.py** | `WumpusWorld` class—manages hidden state, executes actions, generates percepts |
| **visualization.py** | `Visualizer` class—renders game state (grid, agent, percepts) |
| **base_agent.py** | Abstract `Agent` class—interface ensuring agents only see percepts |
| **naive_agent.py** | `NaiveAgent` implementation—uniform random action selection |
| **main.py** | Entry point—game loop, episode management, visualization integration |

---

## 🏗️ Design Philosophy

### Object-Oriented Design
- **Classes** model entities: `WumpusWorld`, `Agent`, `Percept`, `Position`, etc.
- **Enums** provide type-safe action and direction representations
- **Dataclasses** ensure immutability and clarity for data structures

### Separation of Concerns
- **Environment** (`WumpusWorld`) maintains hidden state exclusively
- **Agent** (`Agent` subclasses) operates only on percepts and internal beliefs
- **Agent cannot cheat** by accessing `WumpusWorld` directly
- **Visualizer** displays only known/observable information, not hidden state

### Extensibility
- Clean agent interface (`Agent` base class) allows easy addition of new agents
- No logic dependencies between environment and specific agents
- Structure supports adding belief tracking, planning, and learning in future assignments
- Test framework ready for validation of new agent behaviors

---

## 🚀 How to Run

### Prerequisites
Ensure Python 3.8+ and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Run a Single Episode
```bash
python main.py
```

This runs a standard game:
- 4×4 grid world
- Random wumpus and gold placement
- Pit probability of 0.2
- NaiveAgent making random moves
- Visualization (if implemented)

### Run Tests
```bash
pytest tests/
```

Run all unit tests with verbose output:
```bash
pytest tests/ -v
```

Run a specific test file:
```bash
pytest tests/test_environment.py -v
```

---

## 🎮 Game Mechanics

### Standard Configuration
- **Grid:** 4×4
- **Start position:** [1,1] facing right (EAST)
- **Pit probability:** 0.2 per non-start cell
- **Allow climb without gold:** True
- **Wumpus, gold, pits:** Placed randomly, may overlap

### Agent Actions
| Action | Effect |
|--------|--------|
| **FORWARD** | Move one step in facing direction (blocked by walls) |
| **TURN_LEFT** | Rotate 90° counter-clockwise |
| **TURN_RIGHT** | Rotate 90° clockwise |
| **SHOOT** | Fire arrow in facing direction (kills wumpus) |
| **GRAB** | Pick up gold at current location |
| **CLIMB** | Exit environment (only at [1,1]) |

### Agent Percepts
| Percept | Triggered By |
|---------|--------------|
| **Stench** | Wumpus in adjacent cell |
| **Breeze** | Pit in adjacent cell |
| **Glitter** | Gold at current location |
| **Bump** | Attempted move outside grid |
| **Scream** | Wumpus killed by arrow |
| **Reward** | Immediate reward/penalty for action |

### Episode Termination
Episodes end when:
- **Agent climbs out at [1,1]:** Success (large reward if gold collected)
- **Agent falls in pit:** Death (large negative penalty)
- **Agent meets wumpus:** Death (large negative penalty)
- **Agent shoots wumpus:** Wumpus is eliminated but episode continues
- **Max turns exceeded:** Episode timeout (configurable)

### Rewards (Baseline)
- `-1` per action (time penalty)
- `+1` for grabbing gold
- `-10` for death
- `+1000` for escaping with gold at [1,1]
- `+500` for escaping with gold at [1,1] after many turns
- Penalties adjusted by max turn limit

---

## 📋 Implementation Status

### ✅ Scaffolding Complete
- [x] Class structure and module organization
- [x] Comprehensive docstrings for all classes
- [x] Type hints throughout
- [x] TODO comments marking unimplemented logic
- [x] Test skeleton with placeholders
- [x] `__init__.py` files for clean imports

### 🔧 Ready for Implementation
- [ ] **models.py:** Direction turn logic, Position validation
- [ ] **environment.py:** World initialization, action execution, percept generation
- [ ] **naive_agent.py:** Random action selection
- [ ] **visualization.py:** Grid rendering and output formatting
- [ ] **main.py:** Game loop and episode management
- [ ] **tests/:** Test method implementations

---

## 🧪 Testing Strategy

All tests follow this pattern:
1. **Setup:** Create environment and agent
2. **Execute:** Run actions or scenarios
3. **Verify:** Assert expected state changes and percepts

Test files include TODO placeholders for each test method. Implement tests incrementally as functionality is added.

**Run tests often:** `pytest tests/ -v`

---

## 📚 Key Files to Review

**Start here:**
- [wumpus/models.py](wumpus/models.py) — Data structure definitions
- [wumpus/environment.py](wumpus/environment.py) — Core environment logic
- [agents/base_agent.py](agents/base_agent.py) — Agent interface

**Then explore:**
- [agents/naive_agent.py](agents/naive_agent.py) — Example agent implementation
- [main.py](main.py) — Game loop structure
- [docs/assignment1_requirements.md](docs/assignment1_requirements.md) — Full specification

---

## 🎓 Learning Outcomes

By completing this assignment, you will:
- Practice object-oriented design with Python dataclasses and enums
- Understand the importance of separating environment from agent concerns
- Learn how percept-based interfaces prevent hidden-state cheating
- Build a foundation for intelligent agent algorithms
- Work with type hints and comprehensive documentation
- Structure code for extensibility and testing

---

## 📝 Notes for Assignment 2+

This scaffold is intentionally kept simple to support future extensions:
- No belief tracking or memory structures (ready for agent learning)
- No pathfinding or planning (ready for search algorithms)
- Modular design supports multiple agent types
- Environment logic independent of agent intelligence
- Test infrastructure ready for new agent validation

---

## 👥 Author
**Miguel Morales** (@miguelmog10)  
University of Toronto - Intelligent Agents Course
