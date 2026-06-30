"""HTML/CSS rendering helpers for the Streamlit Wumpus World visualization.

These functions turn the plain-dict snapshots produced by
``utils.episode_runner.run_episode(..., record_history=True)`` into HTML
fragments that Streamlit can display with ``st.markdown(..., unsafe_allow_html=True)``.

Coordinate convention: snapshots and world_layout use USER coordinates
([1,1] at bottom-left, [width,height] at top-right). The board is drawn with
y decreasing down the page so that row [.,height] is on top and [.,1] at bottom.

Agents never use anything in this module; it is purely presentational.
"""

from __future__ import annotations

# Emoji / symbol mapping
_DIRECTION_EMOJI = {
    "EAST": "\u27a1\ufe0f",   # ➡️
    "WEST": "\u2b05\ufe0f",   # ⬅️
    "NORTH": "\u2b06\ufe0f",  # ⬆️
    "SOUTH": "\u2b07\ufe0f",  # ⬇️
}
_WUMPUS_EMOJI = "\U0001f479"   # 👹
_GOLD_EMOJI = "\U0001f4b0"     # 💰
_PIT_EMOJI = "\U0001f573\ufe0f"  # 🕳️
_DEAD_EMOJI = "\U0001f480"     # 💀
_START_EMOJI = "\U0001f6aa"    # 🚪


def direction_emoji(direction_name: str) -> str:
    """Return the arrow emoji for a Direction name (e.g. 'EAST')."""
    return _DIRECTION_EMOJI.get(direction_name, "\u2753")  # ❓ fallback


def render_board_html(
    snapshot: dict,
    world_layout: dict,
    reveal_hidden: bool = False,
    visited_cells: set[tuple[int, int]] | None = None,
) -> str:
    """Build an HTML grid for a single turn snapshot.

    Args:
        snapshot: One per-turn dict from the episode history.
        world_layout: The episode's world layout (user coords). Provides board
            size and the true wumpus/gold/pit positions for the reveal overlay.
        reveal_hidden: If True, draw the true wumpus/gold/pit positions.
        visited_cells: Optional set of (x, y) user-coord cells already visited;
            shaded lightly to show the agent's trail.

    Returns:
        An HTML string suitable for ``st.markdown(..., unsafe_allow_html=True)``.
    """
    width = world_layout["width"]
    height = world_layout["height"]
    visited_cells = visited_cells or set()

    agent_x, agent_y = snapshot["position"]
    agent_alive = snapshot["alive"]
    direction_name = snapshot["direction"]
    percept = snapshot["percept"]

    wumpus = world_layout.get("wumpus")
    gold = world_layout.get("gold")
    pits = set(tuple(p) for p in world_layout.get("pits", []))

    cell_size = 64  # px

    rows_html: list[str] = []
    # Draw top (y = height) down to bottom (y = 1)
    for y in range(height, 0, -1):
        cells_html: list[str] = []
        for x in range(1, width + 1):
            contents: list[str] = []
            is_agent = (x, y) == (agent_x, agent_y)
            is_start = (x, y) == (1, 1)

            # Background shading
            if is_agent:
                bg = "#ffe9a8" if agent_alive else "#f3b0b0"
            elif (x, y) in visited_cells:
                bg = "#eef3f7"
            else:
                bg = "#ffffff"

            # Reveal hidden hazards/objective
            if reveal_hidden:
                if (x, y) in pits:
                    contents.append(_PIT_EMOJI)
                if wumpus is not None and (x, y) == tuple(wumpus):
                    contents.append(_WUMPUS_EMOJI)
                if gold is not None and (x, y) == tuple(gold):
                    contents.append(_GOLD_EMOJI)

            # Agent marker (drawn last so it sits on top)
            if is_agent:
                contents.append(_DEAD_EMOJI if not agent_alive else direction_emoji(direction_name))
            elif is_start and not contents:
                contents.append(_START_EMOJI)

            inner = "".join(contents) if contents else "&nbsp;"

            # Percept badges on the agent's current cell
            badge = ""
            if is_agent:
                marks = []
                if percept.get("stench"):
                    marks.append("S")
                if percept.get("breeze"):
                    marks.append("B")
                if percept.get("glitter"):
                    marks.append("G")
                if marks:
                    badge = (
                        "<div style='position:absolute;top:2px;right:3px;"
                        "font-size:10px;font-weight:700;color:#555;'>"
                        + "".join(marks)
                        + "</div>"
                    )

            coord_label = (
                "<div style='position:absolute;bottom:1px;left:3px;"
                "font-size:9px;color:#aaa;'>"
                f"{x},{y}</div>"
            )

            cells_html.append(
                f"<td style='width:{cell_size}px;height:{cell_size}px;"
                f"border:1px solid #c9c9c9;text-align:center;vertical-align:middle;"
                f"font-size:26px;position:relative;background:{bg};'>"
                f"{badge}{coord_label}{inner}</td>"
            )
        rows_html.append("<tr>" + "".join(cells_html) + "</tr>")

    return (
        "<table style='border-collapse:collapse;margin:0 auto;'>"
        + "".join(rows_html)
        + "</table>"
    )


def visited_cells_up_to(history: list[dict], index: int) -> set[tuple[int, int]]:
    """Return the set of agent cells (user coords) visited up to and including ``index``."""
    cells: set[tuple[int, int]] = set()
    for snap in history[: index + 1]:
        cells.add(tuple(snap["position"]))
    return cells


def percept_badges(percept: dict) -> str:
    """Return a short human-readable string of active percepts (or 'None')."""
    active = [name.capitalize() for name in ("stench", "breeze", "glitter", "bump", "scream") if percept.get(name)]
    return " | ".join(active) if active else "None"
