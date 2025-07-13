import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 5

class FourInARowGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Exactly Four in a Row")
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.players = ['X', 'O']
        self.turn = 0
        self.create_widgets()

    def create_widgets(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                btn = tk.Button(self.root, text="", font=('Helvetica', 20), width=4, height=2,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.reset_button = tk.Button(self.root, text="Reset", font=('Helvetica', 14),
                                      command=self.reset_board)
        self.reset_button.grid(row=BOARD_SIZE, column=0, columnspan=BOARD_SIZE, sticky="we")

    def on_click(self, row, col):
        if self.board[row][col] is not None:
            return

        player = self.players[self.turn % 2]
        self.board[row][col] = player

        btn = self.buttons[row][col]
        btn['text'] = player
        btn['fg'] = 'red' if player == 'X' else 'blue'

        result = self.check_board(player)
        if result == "win":
            messagebox.showinfo("Game Over", f"Player {player} wins with exactly 4 in a row!")
            self.disable_board()
        elif result == "foul":
            other = self.players[(self.turn + 1) % 2]
            messagebox.showinfo("Foul!", f"Player {player} made a line of 5 — foul! Player {other} wins!")
            self.disable_board()
        elif self.turn == BOARD_SIZE * BOARD_SIZE - 1:
            messagebox.showinfo("Draw", "It's a draw!")
            self.disable_board()

        self.turn += 1

    def reset_board(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                btn = self.buttons[i][j]
                btn['text'] = ""
                btn['fg'] = 'black'
                btn['state'] = tk.NORMAL
        self.turn = 0

    def disable_board(self):
        for row in self.buttons:
            for btn in row:
                btn['state'] = tk.DISABLED

    def check_line(self, line, player):
        count = 0
        for cell in line:
            if cell == player:
                count += 1
                if count == 5:
                    return "foul"
            else:
                count = 0
        for i in range(len(line) - 3):
            segment = line[i:i + 4]
            if all(cell == player for cell in segment):
                left_ok = (i == 0 or line[i - 1] != player)
                right_ok = (i + 4 == len(line) or line[i + 4] != player)
                if left_ok and right_ok:
                    return "win"
        return None

    def check_board(self, player):
        for i in range(BOARD_SIZE):
            row = self.board[i]
            col = [self.board[j][i] for j in range(BOARD_SIZE)]
            for line in (row, col):
                result = self.check_line(line, player)
                if result:
                    return result

        # Diagonals — top-left to bottom-right
        for r in range(BOARD_SIZE - 3):
            for c in range(BOARD_SIZE - 3):
                diag = [self.board[r + i][c + i] for i in range(min(5, BOARD_SIZE - max(r, c)))]
                result = self.check_line(diag, player)
                if result:
                    return result

        # Diagonals — top-right to bottom-left
        for r in range(BOARD_SIZE - 3):
            for c in range(3, BOARD_SIZE):
                diag = [self.board[r + i][c - i] for i in range(min(5, min(BOARD_SIZE - r, c + 1)))]
                result = self.check_line(diag, player)
                if result:
                    return result

        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = FourInARowGUI(root)
    root.mainloop()
