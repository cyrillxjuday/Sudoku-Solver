import tkinter as tk
import time

class Label(tk.Label):
    def __init__(self, master):
        self.string = tk.StringVar()
        tk.Label.__init__(self, master, textvariable = self.string, font = ('Arial', 14, 'normal'))

class Solver(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Sudoku Solver')
        self.board_frame = tk.Frame(self, bd = 1, relief = tk.SOLID, height = 501)
        self.button_frame = tk.Frame(self, bd = 1, relief = tk.SOLID, height = 100)
        self.grids = []
        self.cells = []
        self.actual_cell_selected = None
        self.entry_matrix = [[None for i in range(9)] for i in range(9)]
        self.grids_list = [[] for i in range(9)]
        self.rows_list = []
        self.columns_list = []

        self.board_frame.pack()
        self.button_frame.pack(fill = tk.X)
        self.generate_grids_and_cellls()
        self.produce_buttons()
    
    def produce_buttons(self):
        self.inner_panel = tk.Frame(self.button_frame)
        self.inner_panel.pack(padx = 10, pady = 10, fill = tk.X)

        self.solve_button = tk.Button(self.inner_panel, text = 'Solve', font = ('Arial', 14, 'normal'), command = self.pre_solve)
        self.clear_button = tk.Button(self.inner_panel, text = 'Clear', font = ('Arial', 14, 'normal'), command = self.clear)
        self.solve_button.grid(row = 0, column = 0)
        self.clear_button.grid(row = 0, column = 1)

    def clear(self):
        """
        clears the board
        """
        for i in self.cells:
    	    i.text.set('')
    	    i.config(bg = '#ffffff', fg = '#000000')

    def pre_solve(self):
        """
        wrapper for the solve method.
        i have surrounded the solve method with try catch because
        the exception that it raises will be responsible for breakin out of the recursion
        as soon as all of the cells in the puzzle are populated with valid numbers. 
        """
        try:
            self.solve()
        except:
            return

    def solve(self):
        """
        solves the sudoku puzzle using recursion
        """
        actual_cell_selected = self.get_next_cell()
        for i in range(1, 10):
            actual_cell_selected.text.set(i)
            self.update()
            if self.valid(actual_cell_selected):
                actual_cell_selected.config(bg = '#993344', fg = '#ffffff')
                self.solve()
            else:
            	actual_cell_selected.text.set('')
            	actual_cell_selected.config(bg = '#ffffff', fg = '#000000')

    def get_next_cell(self):
        for i in self.grids_list:
            for j in i:
                if j.get() == '':
                    return j

    def generate_grids_and_cellls(self):
        """
        Generation of Grids (left to right, top to bottom)
        """
        for i in range(9):
            self.grids.append(
                tk.Frame(self.board_frame, bd = 1, relief = tk.SOLID, width = 167, height = 165))
        index = 0
        for i in range(3):
            for j in range(3):
                self.grids[index].grid(row = i, column = j)
                index += 1
        
        # Generation of Cells by GridWise distribution
        grid_index = 0
        for i in range(1, 82):
            var = tk.StringVar()
            cell = tk.Entry(self.grids[grid_index], textvariable = var, width = 5, justify = tk.CENTER, font = ('Arial', 15, 'normal'))
            cell.text = var
            cell.grid_number = grid_index
            self.cells.append(cell)
            # append the cell/tk.Entry into the grid matrix
            self.grids_list[grid_index].append(cell)
            if i % 9 == 0:
                grid_index += 1
                cell_index = 0
        # add the cells into the grid layout
        cell_index = 0
        for i in range(9):
            for i in range(3):
                for j in range(3):
                    self.cells[cell_index].grid(row = i, column = j, ipady = 13)
                    cell_index += 1

        # arrange the cells into a matrix
        index = 0
        for i in range(9):
            for j in range(9):
                self.entry_matrix[j][i] = self.cells[index]
                index += 1

        # finally assign each cells into their corresponding row and group column
        # this will be important for answer validation and backtracking algo
        list_index = 0
        for outer_col in range(0,9,3):
            for outer_row in range(0,9,3):
                l = []
                for inner_col in range(3):
                    for inner_row in range(3):
                        self.entry_matrix[inner_row+outer_row][inner_col+outer_col].row_number = list_index
                        l.append(self.entry_matrix[inner_row+outer_row][inner_col+outer_col])
                list_index += 1
                self.rows_list.append(l)

        for i in range(9):
            self.columns_list.append([])
            for j in range(9):
                self.rows_list[j][i].column_number = i
                self.columns_list[i].append(self.rows_list[j][i])

    def valid(self, actual_cell_selected):
        """
        checks the validity of the number in the current cell
        """
        validity = True
        num = actual_cell_selected.get()
        row = actual_cell_selected.row_number
        col = actual_cell_selected.column_number
        grid = actual_cell_selected.grid_number
        
        instance = 0
        temp = self.rows_list[row]
        for i in temp:
            if i.get() == num:
                instance += 1
    
        if instance > 1:
            validity =  False

        instance = 0
        temp = self.columns_list[col]
        for i in temp:
            if i.get() == num:
                instance += 1
        if instance > 1:
            validity = False

        instance = 0
        temp = self.grids_list[grid]
        for i in temp:
            if i.get() == num:
                instance += 1
        if instance > 1:
            validity =  False

        return validity

if __name__ == '__main__':
    Sudoku_Solver = Solver()        
    Sudoku_Solver.mainloop()
