# Exercise 7 — Python Connect-N

## Overview

A Connect-N game implemented in Python, extending the C-based Exercise 3 with dynamic board dimensions from user input, automatic win-sequence calculation, human and computer players, and a special tic-tac-toe mode for 3×3 boards. This exercise was developed using AI tools (Claude via GitHub Copilot) as required by the assignment.

## Author

Avraham Tsaban

## Requirements

- Python 3.9 or higher

## Running

```bash
python3 ex7.py
```

## Game Modes

### Connect-N Mode

Standard gravity-based game where tokens drop to the lowest available position. Win sequence length depends on board dimensions:

| Board Size | Win Sequence |
|-----------|-------------|
| 2 | 2 |
| 3 | Tic-tac-toe mode (see below) |
| 4–5 | 3 |
| 6–10 | 4 |
| 11–100 | 5 |

Players choose columns (1-based). Computer AI uses priority strategy: win → block → threaten → block threat → center preference.

### Tic-Tac-Toe Mode

Activates when either dimension is 3 (forces a 3×3 board). Human vs. Human only. Players enter positions 1–9 mapped as:

```
1|2|3
4|5|6
7|8|9
```

## Player Types

- **`h`** — Human (manual input)
- **`r`** — Computer (random/simple strategy)
- **`s`** — Computer (strategic — same priority logic as `r`)

## Code Structure

All code is in a single file `ex7.py` (437 lines).

### Entry Point

| Function | Description |
|----------|-------------|
| `main()` | Gets board dimensions and player types, determines game mode, starts the game loop. |

### Input and Validation

| Function | Description |
|----------|-------------|
| `get_board_dimensions()` → `(rows, cols)` | Prompts for board dimensions, validates range 2–100. |
| `get_valid_dimension(dimension_name)` → `int` | Validates a single dimension input. |
| `get_player_type(player_number)` → `int` | Prompts for player type (`h`/`r`/`s`). |
| `human_choice(board, cols)` → `int` | Gets a valid, non-full column from the human (0-based). |
| `human_input(cols)` → `int` | Reads and validates numeric column input. |
| `tic_tac_toe_input(board)` → `(row, col)` | Reads position 1–9 for tic-tac-toe mode; rejects taken cells. |

### Board Operations

| Function | Description |
|----------|-------------|
| `init_board(rows, cols)` → `list` | Creates a 2D board filled with `EMPTY` (`.`). |
| `print_board(board, rows, cols, ttt_mode)` | Prints the board with column numbers (mod 10 for wide boards). |
| `print_board_ttt(board)` | Prints the 3×3 tic-tac-toe board. |
| `make_move(board, column, token)` → `int` | Drops token into the lowest free row; returns row index. |
| `get_free_row(board, column)` → `int` | Finds lowest empty row in a column (`FAILURE` if full). |
| `is_column_full(board, column)` → `bool` | Checks if top cell is occupied. |
| `is_board_full(board, cols)` → `bool` | Checks if all columns are full (Connect-N). |
| `is_board_full_ttt(board, rows, cols)` → `bool` | Checks if all cells are occupied (tic-tac-toe). |
| `is_in_bounds(cols, column, rows, row)` → `bool` | Validates indices are within board boundaries. |

### Game Loops

| Function | Description |
|----------|-------------|
| `run_connect_n(board, rows, cols, connect_n, p1_type, p2_type)` | Main Connect-N loop — alternates turns until win or tie. |
| `run_tic_tac_toe(board, rows, cols)` | Tic-tac-toe loop — two human players, position-based input. |

### Win Detection

| Function | Description |
|----------|-------------|
| `line_length(board, rows, cols, row, col, connect_n, token)` → `int` | Checks all 4 directions from a placed token; returns longest consecutive chain. |
| `calculate_connect_n(rows, cols)` → `int` | Determines win sequence length based on board dimensions (2–5). |

### Computer AI

| Function | Description |
|----------|-------------|
| `computer_choose(board, rows, cols, connect_n, token)` → `int` | 5-tier strategy: win → block win → extend to N−1 → block N−1 → center-first fallback. |
| `set_priority(cols)` → `list[int]` | Column priority list: center outward, left-first on ties. |

## Project Files

| File | Description |
|------|-------------|
| `ex7.py` | Source code |
| `ex7.example` | Reference Linux executable provided by the TA |
| `ex7_instructions.md` | Exercise instructions |
| `ex3_instructions.md` | Original C exercise instructions (for reference) |
| `policy.file` | Requirements policy for this exercise |
| `prompts.md` | Documentation of the AI-assisted development process |

## AI-Assisted Development

This project was developed with Claude (via GitHub Copilot) as required by the exercise. The complete prompt history is documented in [prompts.md](prompts.md).

## Attribution

The exercise design, specifications, and instructions were created by **Shalom Adoram**, the Teaching Assistant responsible for this assignment. The instructions file (`ex7_instructions.md`) and the reference executable (`ex7.example`) are his work. Any license in this repository applies only to the student's code implementation.
