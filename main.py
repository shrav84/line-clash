def print_board(board):
    print("  " + " ".join(str(i) for i in range(5)))
    for idx, row in enumerate(board):
        print(str(idx) + " " + " ".join(cell if cell else "." for cell in row))

def check_line(line, player):
    count = 0
    for i in range(len(line)):
        if line[i] == player:
            count += 1
        else:
            count = 0
        if count == 5:
            return "foul"  # Too many!
    # Check for exactly 4
    for i in range(len(line) - 3):
        segment = line[i:i+4]
        if all(cell == player for cell in segment):
            # Check edges to ensure it's exactly 4
            left_ok = (i == 0 or line[i-1] != player)
            right_ok = (i+4 == len(line) or line[i+4] != player)
            if left_ok and right_ok:
                return "win"
    return None

def check_board(board, player):
    # Rows and columns
    for i in range(5):
        result = check_line([board[i][j] for j in range(5)], player)
        if result: return result
        result = check_line([board[j][i] for j in range(5)], player)
        if result: return result

    # Diagonals
    diags = [
        [board[i][i] for i in range(5)],
        [board[i][4 - i] for i in range(5)]
    ]
    # Diagonals of length 4 (top-left to bottom-right)
    for i in range(2):
        diag1 = [board[j][j + i] for j in range(5 - i)]
        diag2 = [board[j + i][j] for j in range(5 - i)]
        diag3 = [board[j][4 - j - i] for j in range(5 - i)]
        diag4 = [board[j + i][4 - j] for j in range(5 - i)]
        diags.extend([diag1, diag2, diag3, diag4])
    
    for diag in diags:
        result = check_line(diag, player)
        if result: return result
    return None

def play_game():
    board = [[None]*5 for _ in range(5)]
    players = ['X', 'O']
    turn = 0

    while True:
        print_board(board)
        player = players[turn % 2]
        print(f"Player {player}'s turn.")

        try:
            row = int(input("Enter row (0-4): "))
            col = int(input("Enter col (0-4): "))
        except ValueError:
            print("Invalid input. Try again.")
            continue

        if not (0 <= row < 5 and 0 <= col < 5):
            print("Out of bounds. Try again.")
            continue
        if board[row][col]:
            print("Cell already taken. Try again.")
            continue

        board[row][col] = player
        result = check_board(board, player)
        if result == "win":
            print_board(board)
            print(f"Player {player} wins with exactly 4 in a row!")
            break
        elif result == "foul":
            print_board(board)
            print(f"Player {player} made a line of 5 — foul! Player {players[(turn + 1) % 2]} wins!")
            break

        turn += 1
        if turn == 25:
            print_board(board)
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()
