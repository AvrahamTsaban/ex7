# EX7 - Python Connect-N

**Author:** Avraham Tsaban  
**ID:** 207088733  
**Assignment:** 7

## Project Description

A Connect-N game implementation in Python, featuring dynamic board dimensions, automatic win sequence calculation, human and computer players, and a special tic-tac-toe mode for 3x3 boards.

This project is based on Exercise 3 written in C, but extended with additional capabilities:
- Board dimensions received from user input (instead of compilation flags)
- Dynamic calculation of the required win sequence length
- Special tic-tac-toe mode for 3x3 boards

## System Requirements

- Python 3.9.25 or higher
- Operating System: Linux / macOS / Windows

## Installation and Running

```bash
# Clone the project
git clone https://github.com/CSI-BIU/ex7.git
cd ex7

# Run the game
python3 ex7.py
```

## Game Rules

### Board Dimensions and Sequence Length

The game supports various board dimensions with dynamic rules:

| Board Size | Win Sequence Length | Notes |
|-----------|---------------------|-------|
| 2 | 2 | Very short game |
| 3 | 3 (Tic-Tac-Toe) | 3x3 board, two human players only |
| 4-5 | 3 | |
| 6-10 | 4 | |
| 11-100 | 5 | |

**Note:** If either dimension is 3, the game automatically switches to tic-tac-toe mode.

### Tic-Tac-Toe Mode

- 3x3 board only
- Two human players only
- Players directly choose row and column (no token dropping from top)
- Win by creating a sequence of 3 diagonally, horizontally, or vertically

### Connect-N Mode

- Players drop tokens into columns
- Tokens fall to the lowest available position in the column
- Win by creating a sequence of N consecutive tokens (vertical, horizontal, or diagonal)

## Player Types

### Human Player
- Prompted to enter column choice (or row and column in tic-tac-toe)
- Input undergoes validation checks:
  - Is the value numeric
  - Is it within valid range
  - Is the column not full

### Computer Player
The computer uses a smart priority strategy:

1. **Immediate Win** - If there's a winning move, execute it
2. **Block Opponent's Win** - If opponent is about to win, block them
3. **Create (N-1) Sequence** - Create a sequence one short of winning
4. **Block Opponent's (N-1) Sequence** - Block dangerous opponent sequence
5. **Choose by Center Priority** - Select columns from center outward

#### Center Priority Strategy

Columns are chosen based on proximity to center:
- Center column receives highest priority
- Adjacent columns checked alternately left and right
- For equidistant columns, left column is chosen first

**Example:** For a board with 7 columns:
```
Priority: [3, 4, 2, 5, 1, 6, 0]  # (0-based indices)
Display:  [4, 5, 3, 6, 2, 7, 1]   # (column numbers for user)
```

## Code Structure

### Constants

```python
EMPTY = '.'       # Empty cell on board
TOKEN_P1 = 'X'    # Player 1 token
TOKEN_P2 = 'O'    # Player 2 token

HUMAN = 1         # Player type code - human
COMPUTER = 2      # Player type code - computer

MIN_DIMENSION = 2    # Minimum board dimension
MAX_DIMENSION = 100  # Maximum board dimension
TTT_DIMENSION = 3    # Tic-tac-toe dimension

FAILURE = -1      # Failure return value
```

### Main Functions

#### `main()`
Program entry point:
- Gets board dimensions from user
- Determines game type (tic-tac-toe or connect-n)
- Gets player types
- Starts game loop

#### Input and Validation

- **`get_board_dimensions()`** - Prompts user for board dimensions
- **`get_valid_dimension(dimension_name)`** - Validates single dimension input
- **`get_player_type(player_number)`** - Prompts for player type selection
- **`human_choice(board, cols)`** - Prompts human for column choice
- **`human_input(cols)`** - Collects and validates numeric input
- **`tic_tac_toe_input(board, rows, cols)`** - Row and column input for tic-tac-toe

#### Board Management

- **`init_board(rows, cols)`** - Creates new empty board
- **`print_board(board, rows, cols, ttt_mode)`** - Displays the board
- **`make_move(board, column, token)`** - Executes a move
- **`get_free_row(board, column)`** - Finds available row in column

#### Game Loops

- **`run_connect_n(board, rows, cols, connect_n, p1_type, p2_type)`** - Main loop for connect-n mode
- **`run_tic_tac_toe(board, rows, cols)`** - Loop for tic-tac-toe mode

#### State Checks

- **`is_column_full(board, column)`** - Checks if column is full
- **`is_board_full(board, cols)`** - Checks if entire board is full
- **`is_board_full_ttt(board, rows, cols)`** - Full board check for tic-tac-toe
- **`is_in_bounds(cols, column, rows, row)`** - Checks if index is within bounds

#### Win Detection

- **`line_length(board, rows, cols, row, column, connect_n, token)`** - Checks maximum sequence length in all 4 directions (horizontal, vertical, two diagonals)

#### Artificial Intelligence

- **`computer_choose(board, rows, cols, connect_n, token)`** - Chooses column for computer
- **`set_priority(cols)`** - Creates column priority list
- **`calculate_connect_n(rows, cols)`** - Calculates required sequence length for win

## Usage Examples

### Classic 6x7 Game (Connect-4)

```
$ python3 ex7.py
Enter number of rows (2-100): 6
Enter number of columns (2-100): 7

Connect-4 (6 rows x 7 cols)
Sequence to win: 4

Choose type for player 1: h - human, c - computer: h
Choose type for player 2: h - human, c - computer: c

|.|.|.|.|.|.|.|
|.|.|.|.|.|.|.|
|.|.|.|.|.|.|.|
|.|.|.|.|.|.|.|
|.|.|.|.|.|.|.|
|.|.|.|.|.|.|.|
 1 2 3 4 5 6 7

Player 1 (X) turn.
Enter column (1-7): 4
...
```

### Tic-Tac-Toe Game

```
$ python3 ex7.py
Enter number of rows (2-100): 3
Enter number of columns (2-100): 5

Tic-Tac-Toe mode! (3 rows x 3 cols)
Sequence to win: 3

|.|.|.|
|.|.|.|
|.|.|.|

Player 1 (X) turn.
Enter row (1-3): 2
Enter column (1-3): 2
...
```

### Large Game (Connect-5)

```
$ python3 ex7.py
Enter number of rows (2-100): 12
Enter number of columns (2-100): 15

Connect-5 (12 rows x 15 cols)
Sequence to win: 5

Choose type for player 1: h - human, c - computer: c
Choose type for player 2: h - human, c - computer: c
...
```

## Input Validation

The program performs comprehensive validation:

1. **Board Dimensions:**
   - Must be integers
   - Within range 2-100
   - Appropriate error messages with retry guidance

2. **Column Selection:**
   - Must be a number
   - Within range 1 to number of columns
   - Column cannot be full

3. **Player Type Selection:**
   - Only 'h' or 'c' (case-insensitive)
   - Error message with retry guidance

## Project Files

- **`ex7.py`** - Main game code file
- **`ex3.c`** - Original C code (for reference)
- **`ex3_instructions.md`** - Original exercise instructions
- **`policy.file`** - Specific requirements policy for exercise 7
- **`prompts.md`** - Documentation of AI code creation process
- **`readme.md`** - This file

## AI-Assisted Development

This project was developed with Claude (via GitHub Copilot) through several iterations:
1. Initial creation based on the C code
2. Fix tic-tac-toe mode for correct operation
3. Additional adjustments and documentation development

The complete process is documented in [prompts.md](prompts.md).

## License

See [LICENSE](LICENSE) file for details.

## Author

Avraham Tsaban - Exercise 7 for Introduction to Computer Science, BIU
