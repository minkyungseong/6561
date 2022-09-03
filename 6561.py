import tkinter as tk
import random

class Colors:
    CELL_COLORS = {
        1: "#fcefe6",
        3: "#fcefe6",
        9: "#f2e8cb",
        81: "#f5b682",
        243: "#f29446",
        726: "#ff775c",
        2187: "#e64c2e",
        6561: "#ede291"
    }
    
    CELL_NUMBER_COLORS = {
        1: "#ff7256",
        3: "#695c57",
        9: "#695c57",
        81: "#ffffff",
        243: "#ffffff",
        726: "#ffffff",
        2187: "#ffffff",
        6561: "#ffffff"
    }
    
    CELL_NUMBER_FONTS = {
        1: ("Helvetica", 70, "bold"),
        3: ("Helvetica", 70, "bold"),
        9: ("Helvetica", 70, "bold"),
        81: ("Helvetica", 70, "bold"),
        243: ("Helvetica", 65, "bold"),
        726: ("Helvetica", 65, "bold"),
        2187: ("Helvetica", 60, "bold"),
        6561: ("Helvetica", 60, "bold")
    }
    
    GRID_COLOR = "#a39489"
    EMPTY_CELL_COLOR = "#c2b3a9"
    SCORE_LABEL_FONT = ("Gill Sans MT", 30, "bold")
    SCORE_FONT = ("Gill Sans MT", 45, "bold")
    check_status_FONT = ("Gill Sans MT", 48, "bold")
    RESTART_FONT = ("Gill Sans MT", 15)
    RESTART_FONT_COLOR = '#8b8878'
    check_status_FONT_COLOR = "#ffffff"
    WINNER_BG = "#ffcc00"
    LOSER_BG = "#a39489"


class Play(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("6561")
        self.main_grid = tk.Frame(
            self, bg=Colors.GRID_COLOR, bd=3, width=600, height=600)
        self.main_grid.grid(pady=(100, 0))
        self.load_GUI()
        self.start_state()

        # bind arrow key events to corresponding functions
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind(" <Up>", self.up)
        self.master.bind("<Down>", self.down)
        self.master.bind("r", self.restart)
        self.master.bind("R", self.restart)
        self.mainloop()

    def load_GUI(self):
        # create a grid that represents a state space for the game
        self.cells = []
        for i in range(3):
            row = []
            for j in range(3):
                grid_frame = tk.Frame(
                    self.main_grid,
                    bg=Colors.EMPTY_CELL_COLOR,
                    width=150,
                    height=150)
                grid_frame.grid(row=i, column=j, padx=7, pady=7)
                grid_num = tk.Label(self.main_grid, bg=Colors.EMPTY_CELL_COLOR)
                grid_num.grid(row=i, column=j)
                row.append({"frame": grid_frame, "number": grid_num})
            self.cells.append(row)

        # create a score header and place score below header; place these in center
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=50, anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=Colors.SCORE_LABEL_FONT).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=Colors.SCORE_FONT)
        self.score_label.grid(row=1)

        # add restart label
        restart_frame = tk.Frame(self)
        restart_frame.place(relx=0.68, y=10)
        tk.Label(
            restart_frame,
            text="Press R to RESTART",
            font=Colors.RESTART_FONT,
            fg=Colors.RESTART_FONT_COLOR).grid(row=0)




    def start_state(self):
        # create a zero-filled matrix
        self.matrix = [[0] * 3 for _ in range(3)]

        # randomly fill 2 cells with 3
        row, col = random.randint(0, 2), random.randint(0, 2)
        self.matrix[row][col] = 3
        self.cells[row][col]["frame"].configure(bg=Colors.CELL_COLORS[3])
        self.cells[row][col]["number"].configure(
            bg=Colors.CELL_COLORS[3],
            fg=Colors.CELL_NUMBER_COLORS[3],
            font=Colors.CELL_NUMBER_FONTS[3],
            text="3")
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 2)
            col = random.randint(0, 2)
        self.matrix[row][col] = 3
        self.cells[row][col]["frame"].configure(bg=Colors.CELL_COLORS[3])
        self.cells[row][col]["number"].configure(
            bg=Colors.CELL_COLORS[3],
            fg=Colors.CELL_NUMBER_COLORS[3],
            font=Colors.CELL_NUMBER_FONTS[3],
            text="3")
        self.score = 0

    # Functions that manages the grid 
    
    def stack(self):
        tmp_matrix = [[0] * 3 for _ in range(3)]
        for i in range(3):
            position = 0
            for j in range(3):
                if self.matrix[i][j] != 0:
                    tmp_matrix[i][position] = self.matrix[i][j]
                    position += 1
        self.matrix = tmp_matrix


    def multiply(self):
        for i in range(3):
            for j in range(2):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= self.matrix[i][j]
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]


    def reverse(self):
        tmp_matrix = []
        for i in range(3):
            tmp_matrix.append([])
            for j in range(3):
                tmp_matrix[i].append(self.matrix[i][2 - j])
        self.matrix = tmp_matrix


    def transpose(self):
        tmp_matrix = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                tmp_matrix[i][j] = self.matrix[j][i]
        self.matrix = tmp_matrix


    # Add a new 3 or an obstacle to the grid
    def update_state(self):
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 2)
            col = random.randint(0, 2)
        # adds 1, an obstacle, with 40% probability
        self.matrix[row][col] = random.choice([3, 3, 3, 1, 1])

        for i in range(3):
            for j in range(3):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=Colors.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=Colors.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(
                        bg=Colors.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=Colors.CELL_COLORS[cell_value],
                        fg=Colors.CELL_NUMBER_COLORS[cell_value],
                        font=Colors.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def update_GUI(self):
        for i in range(3):
            for j in range(3):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=Colors.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=Colors.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(
                        bg=Colors.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=Colors.CELL_COLORS[cell_value],
                        fg=Colors.CELL_NUMBER_COLORS[cell_value],
                        font=Colors.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()


    # arrow functions

    def left(self, event):
        self.stack()
        self.multiply()
        self.stack()
        self.update_state()
        self.check_status()


    def right(self, event):
        self.reverse()
        self.stack()
        self.multiply()
        self.stack()
        self.reverse()
        self.update_state()
        self.check_status()


    def up(self, event):
        self.transpose()
        self.stack()
        self.multiply()
        self.stack()
        self.transpose()
        self.update_state()
        self.check_status()


    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.multiply()
        self.stack()
        self.reverse()
        self.transpose()
        self.update_state()
        self.check_status()

    # empty the game space and revert it back to the start state
    def restart(self, event):
        self.matrix = [[0] * 3 for _ in range(3)]
        self.score = 0
        self.start_state()
        self.update_GUI()


    # Once the game is over, disable all moves by unbinding events
    def disable_moves(self):
        self.master.unbind("<Right>")
        self.master.unbind("<Left>")
        self.master.unbind(" <Up> ")
        self.master.unbind("<Down>")
        self.master.unbind("r")
        self.master.unbind("R")

    # Check if the user has won or lost
    def check_status(self):
        if any(6561 in row for row in self.matrix):
            win_frame = tk.Frame(self.main_grid, borderwidth=4)
            win_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                win_frame,
                text="You won!",
                bg=Colors.WINNER_BG,
                fg=Colors.check_status_FONT_COLOR,
                font=Colors.check_status_FONT).pack()
            self.disable_moves()
        elif not any(0 in row for row in self.matrix):
            lost_frame = tk.Frame(self.main_grid, borderwidth=4)
            lost_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                lost_frame,
                text="Game over!",
                bg=Colors.LOSER_BG,
                fg=Colors.check_status_FONT_COLOR,
                font=Colors.check_status_FONT).pack()
            self.disable_moves()



def main():
    Play()


if __name__ == "__main__":
    main()