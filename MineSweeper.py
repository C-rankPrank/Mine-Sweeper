import random
already_dug = set()

def generate_board(size, char):
    boardd = [[char for _ in range(size)] for _ in range(size)]
    return boardd

def players_board(main_board):
    size = len(main_board[0])
    player_board = generate_board(size, "-")
    for row in range(size):
        for col in range(size):
            if (row, col) in already_dug:
                player_board[row][col] = main_board[row][col]
    return player_board

def print_board(board_name):
    if len(board_name[0]) < 10:
        seperator = " "
    else:
        seperator = "  "
    first_line = "  " + seperator
    index = 0
    # Generate first line of numbers
    for i in range(len(board_name[0])):
        first_line += str(i) + seperator
    print(first_line)
    for row in board_name:
        # Add number for each row
        if index < 10:
            line = str(index) + " " + seperator
        else:
            line = str(index) + seperator
        for char in row:
            line += str(char) + seperator
        print(line)
        index += 1

def board_mining(board_name, mines, first_dig):
    size = len(board_name[0])
    planted_mines = 0
    while planted_mines < mines:
        rnd = random.randint(0, (size**2-1))
        row = rnd // size
        col = rnd % size
        if board_name[row][col] == "x" or (row, col) == first_dig:
            continue
        else:
            board_name[row][col] = "x"
            planted_mines += 1

def check_surrounding_boxes(row, col, size, board_name):
    count = 0
    # Scanning all fields around given field[row][col] in given board
    for r in range(max(0, row-1), min(row+2, size)):
        for c in range(max(0, col-1), min(col+2, size)):
            # Skipping given box
            if r == row and c == col:
                continue
            elif board_name[r][c] == 'x':
                count += 1
    return count

def count_mines(board_name, size):
    for row in range(size):
        for col in range(size):
            # Do not count surrounding mines for mines itself
            if board_name[row][col] == "x":
                continue
            else:
                # Count mines around box[row][column]
                board_name[row][col] = check_surrounding_boxes(row, col, size, board_name)

def user_input(board_size):
    input_user = input("Where would you like to dig? \nPlease insert coordinates: Row, Column: ").split(",")
    rng = range(board_size)
    try:
        if len(input_user) == 2:
            row = int(input_user[0].strip())
            col = int(input_user[1].strip())
            if row in rng and col in rng:
                if (row, col) not in already_dug:
                    return row, col
                else:
                    print("This field is already dug! Choose another!")
                    raise ValueError
            else:
                print("Out of range!")
                raise ValueError
        else:
            raise ValueError
    except:
        print("Please input correct numbers! For example: 0, 0\n")
        return user_input(board_size)

def dig(board, row, col):
    already_dug.add((row, col))
    if board[row][col] == 'x':
        return False
    elif board[row][col] > 0:
        is_number = True
        return True

    size = len(board[0])
    for r in range(max(0, row-1), min(row+2, size)):
        for c in range(max(0, col-1), min(col+2, size)):
            if (r, c) in already_dug:
                continue
            dig(board, r, c)
    return True

def gameplay(board_size=10, mines_num=15):
# 1. Generate a new board.
    main_board = generate_board(board_size, 0)

# 2. Generate secondary board, populated with any characters, this board will be represented for the player after each move.
    sec_board = players_board(main_board)

# 3. Print secondary board and ask user where to dig.
    print_board(sec_board)
    first_row, first_col = user_input(board_size)

# 4. Mine the field and fill fields with number of neighbour mines (first field can not be a mine)
    board_mining(main_board, mines_num, (first_row, first_col))
    count_mines(main_board, board_size)
    #print_board(main_board) # To be removed
    dig(main_board, first_row, first_col)

# 5. Ask user where to dig until mine is dug or there is no remaining not mined fields:
#    If player dug a bomb, reveal primary board and print game over.
#    If player dug empty box, dig until number is revealed, insert changes into secondary board
#    If player dug a number, insert number to secondary board
# 6. Continue steps 3 and 5 until there is no clear boxes left unrevealed.
    while (board_size ** 2 - mines_num) != len(already_dug):
        sec_board = players_board(main_board)
        print("\n")
        print_board(sec_board)
        row, column = user_input(board_size)
        success = dig(main_board, row, column)
        # Check if digging was successful. If not, break the loop
        if not success:
            break

    print("Game over")
    print_board(main_board)
    if success:
        print("You won!")
    else:
        print("You lost :/")


if __name__ == "__main__":
    gameplay()


