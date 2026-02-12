"""
EX7 - Python Connect-N
Name: Avraham Tsaban
Assignment: 7

A Connect-N game implementation in Python, supporting:
- Dynamic board dimensions (validated input)
- Automatic sequence length calculation based on board size
- Human and Computer players
- Special tic-tac-toe mode for 3x3 boards
"""

# Constants
EMPTY = '.'
TOKEN_P1 = 'X'
TOKEN_P2 = 'O'

HUMAN = 1
COMPUTER = 2

# Board size limits
MIN_DIMENSION = 2
MAX_DIMENSION = 100
TTT_DIMENSION = 3

# Return values
FAILURE = -1


def main():
    """Main function: gets board dimensions, player types, and runs the game."""
    rows, cols = get_board_dimensions()
    
    # Special case: tic-tac-toe mode (3x3 board)
    if rows == TTT_DIMENSION or cols == TTT_DIMENSION:
        rows, cols = TTT_DIMENSION, TTT_DIMENSION
        print("Tic Tac Toe (Human vs Human)")
        board = init_board(rows, cols)
        print_board_ttt(board)
        run_tic_tac_toe(board, rows, cols)
    else:
        connect_n = calculate_connect_n(rows, cols)
        print(f"Connect Four - Or More [Or Less] ({rows} rows x {cols} cols, connect {connect_n})")
        p1_type = get_player_type(1)
        p2_type = get_player_type(2)
        board = init_board(rows, cols)
        print_board(board, rows, cols)
        run_connect_n(board, rows, cols, connect_n, p1_type, p2_type)


def get_board_dimensions():
    """
    Prompts user for board dimensions and validates them.
    Returns tuple (rows, cols) with valid dimensions.
    """
    rows = get_valid_dimension("rows")
    cols = get_valid_dimension("columns")
    return rows, cols


def get_valid_dimension(dimension_name):
    """
    Prompts user for a single dimension value and validates it.
    Repeats until valid input (integer between MIN_DIMENSION and MAX_DIMENSION).
    """
    while True:
        try:
            value = int(input(f"Enter number of {dimension_name}\n"))
            if MIN_DIMENSION <= value <= MAX_DIMENSION:
                return value
            print(f"Invalid input. Choose between {MIN_DIMENSION} and {MAX_DIMENSION}.")
        except ValueError:
            print("Invalid input. Enter a number.")


def calculate_connect_n(rows, cols):
    """Calculates sequence length needed to win based on the smaller dimension."""
    min_dim = min(rows, cols)
    if min_dim == 2:
        return 2
    elif 4 <= rows or cols <= 5:
        return 3
    elif 6 <= rows or cols <= 10:
        return 4
    else:  # 11 and above
        return 5


def get_player_type(player_number):
    """
    Prompts user to select player type (human or computer) for given player.
    Returns HUMAN or COMPUTER constant.
    """
    while True:
        choice = input(f"Choose type for player {player_number}: h - human, r - random/simple computer, s - strategic computer: ").strip()
        if choice.lower() == 'h':
            return HUMAN
        elif choice.lower() in ('r', 's', 'c'):
            return COMPUTER
        print("Invalid selection. Enter h, r, or s.")


def init_board(rows, cols):
    """Initializes and returns a board with all cells set to EMPTY."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board, rows, cols, ttt_mode=False):
    """Prints the current state of the board to the console."""
    print()
    for r in range(rows):
        print("|", end="")
        for c in range(cols):
            print(f"{board[r][c]}|", end="")
        print()
    
    # Print column numbers (using modulo 10 for double-digit columns)
    if not ttt_mode:
        for c in range(1, cols + 1):
            print(f" {c % 10}", end="")
    print("\n")


def print_board_ttt(board):
    """Prints the tic-tac-toe board without leading newline or column numbers."""
    for r in range(3):
        print("|", end="")
        for c in range(3):
            print(f"{board[r][c]}|", end="")
        print()


def run_tic_tac_toe(board, rows, cols):
    """
    Tic-tac-toe game loop. Two human players, position-based input (1-9).
    Assumes no one marks a taken cell (per policy.file).
    """
    current_player = 1
    
    while True:
        token = TOKEN_P1 if current_player == 1 else TOKEN_P2
        
        row, col = tic_tac_toe_input(board)
        
        # Place token directly in chosen cell
        board[row][col] = token
        print_board_ttt(board)
        
        # Check for win
        if line_length(board, rows, cols, row, col, TTT_DIMENSION, token) >= TTT_DIMENSION:
            print(f"Player {current_player} ({token}) wins!")
            return
        
        # Check for tie
        if is_board_full_ttt(board, rows, cols):
            print("Board full and no winner. It's a tie!")
            return
        
        # Swap players
        current_player = 2 if current_player == 1 else 1


def tic_tac_toe_input(board):
    """
    Prompts human player to enter position (1-9) for tic-tac-toe.
    Positions map: 1-3 top row, 4-6 middle row, 7-9 bottom row.
    Returns (row, col) as 0-based indices.
    """
    while True:
        try:
            pos = int(input("Enter position (1-9):\n"))
            if not (1 <= pos <= 9):
                print("Invalid position. Choose 1-9.")
                continue
            row = (pos - 1) // 3
            col = (pos - 1) % 3
            if board[row][col] != EMPTY:
                print("Cell already taken. Choose another cell.")
                continue
            return row, col
        except ValueError:
            print("Invalid input. Enter a number.")


def is_board_full_ttt(board, rows, cols):
    """
    Checks if entire board is full for tic-tac-toe.
    Returns True if full, False otherwise.
    """
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == EMPTY:
                return False
    return True


def run_connect_n(board, rows, cols, connect_n, p1_type, p2_type):
    """
    Main game loop. Alternates turns between players until win or tie.
    """
    current_player = 1
    
    while True:
        # Determine current player's token and type
        if current_player == 1:
            token = TOKEN_P1
            is_human = (p1_type == HUMAN)
        else:
            token = TOKEN_P2
            is_human = (p2_type == HUMAN)
        
        # Announce current player's turn and get column choice
        print(f"Player {current_player} ({token}) turn.")
        
        if is_human:
            column = human_choice(board, cols)
        else:
            column = computer_choose(board, rows, cols, connect_n, token)
            print(f"Computer chose column {column + 1}")
        
        # Make the move and get the row where token was placed
        row = make_move(board, column, token)
        print_board(board, rows, cols)
        
        # Check for win
        if line_length(board, rows, cols, row, column, connect_n, token) >= connect_n:
            print(f"Player {current_player} ({token}) wins!")
            return
        
        # Check for tie
        if is_board_full(board, cols):
            print("Board full and no winner. It's a tie!")
            return
        
        # Swap players
        current_player = 2 if current_player == 1 else 1


def make_move(board, column, token):
    """Places token in the lowest free row of specified column. Returns row index."""
    free_row = get_free_row(board, column)
    if free_row != FAILURE:
        board[free_row][column] = token
    return free_row


def get_free_row(board, column):
    """Finds the lowest free row in specified column. Returns row index or FAILURE."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][column] == EMPTY:
            return r
    return FAILURE


def is_column_full(board, column):
    """
    Checks if specified column is full by checking the topmost row.
    Returns True if full, False otherwise.
    """
    return board[0][column] != EMPTY


def is_board_full(board, cols):
    """
    Checks if entire board is full by checking each column.
    Returns True if full, False otherwise.
    """
    for column in range(cols):
        if not is_column_full(board, column):
            return False
    return True


def is_in_bounds(cols, column, rows=None, row=None):
    """Validates if indices are within bounds. Optionally checks row if provided."""
    if rows is not None and row is not None and (row < 0 or row >= rows):
        return False
    return 0 <= column < cols


def line_length(board, rows, cols, row, column, connect_n, token):
    """
    Given the last placed token at (row, column), checks in all 4 directions
    (horizontal, vertical, two diagonals) for consecutive tokens of same type.
    Returns the length of the longest line found.
    """
    # Direction vectors: right, down-right, down, down-left (as (dy, dx) pairs)
    directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
    max_length = 1
    
    for dy, dx in directions:
        length = 1
        
        # Check forward direction
        for i in range(1, connect_n):
            check_row = row + (i * dy)
            check_col = column + (i * dx)
            
            if not is_in_bounds(cols, check_col, rows, check_row):
                break
            
            if board[check_row][check_col] == token:
                length += 1
            else:
                break
        
        # Check backward direction (reverse)
        for i in range(1, connect_n):
            check_row = row - (i * dy)
            check_col = column - (i * dx)
            
            if not is_in_bounds(cols, check_col, rows, check_row):
                break
            
            if board[check_row][check_col] == token:
                length += 1
            else:
                break
        
        # Early return if winning length found
        if length >= connect_n:
            return length
        
        if length > max_length:
            max_length = length
    
    return max_length


def human_choice(board, cols):
    """
    Prompts human player to enter a valid column number that is not full.
    Returns the chosen column index (0-based).
    """
    while True:
        choice = human_input(cols)
        column = choice - 1  # Convert to 0-based index
        
        if not is_in_bounds(cols, column):
            print(f"Invalid column. Choose between 1 and {cols}.")
            continue
        
        if is_column_full(board, column):
            print(f"Column {choice} is full. Choose another column.")
            continue
        
        return column


def human_input(cols):
    """
    Prompts human player to enter a column number between 1 and cols.
    Validates input is a number. Returns the chosen column number (1-based).
    """
    while True:
        try:
            choice = int(input(f"Enter column (1-{cols}): "))
            return choice
        except ValueError:
            print("Invalid input. Enter a number.")


def set_priority(cols):
    """
    Creates and returns a priority list for column selection by computer.
    Middle column has highest priority, then adjacent columns moving outward.
    Left column is prioritized when two columns have equal distance from center.
    """
    priority = []
    middle_column = cols // 2
    is_length_odd = cols % 2 == 1
    
    if is_length_odd:
        left_middle = middle_column
        priority.append(middle_column)
    else:
        left_middle = middle_column - 1
        priority.append(left_middle)
        priority.append(middle_column)
    
    # Add pairs of columns on either side of middle, moving outward
    for distance in range(1, left_middle + 1):
        priority.append(left_middle - distance)
        priority.append(middle_column + distance)
    
    return priority


def computer_choose(board, rows, cols, connect_n, token):
    """Chooses column for computer based on priority strategy. Returns column index."""
    priority = set_priority(cols)
    rival = TOKEN_P2 if token == TOKEN_P1 else TOKEN_P1
    
    # Priority 1: Find winning move
    for col in priority:
        row = get_free_row(board, col)
        if row == FAILURE:
            continue
        if line_length(board, rows, cols, row, col, connect_n, token) >= connect_n:
            return col
    
    # Priority 2: Block opponent's winning move
    for col in priority:
        row = get_free_row(board, col)
        if row == FAILURE:
            continue
        if line_length(board, rows, cols, row, col, connect_n, rival) >= connect_n:
            return col
    
    # Priority 3: Create sequence of (connect_n - 1)
    for col in priority:
        row = get_free_row(board, col)
        if row == FAILURE:
            continue
        if line_length(board, rows, cols, row, col, connect_n, token) >= connect_n - 1:
            return col
    
    # Priority 4: Block opponent's sequence of (connect_n - 1)
    for col in priority:
        row = get_free_row(board, col)
        if row == FAILURE:
            continue
        if line_length(board, rows, cols, row, col, connect_n, rival) >= connect_n - 1:
            return col
    
    # Priority 5: Choose first available column by priority
    for col in priority:
        if get_free_row(board, col) != FAILURE:
            return col
    
    return FAILURE  # All columns full


if __name__ == "__main__":
    main()
