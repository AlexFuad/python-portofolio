"""
Sudoku Solver - Modern GUI Version
Sudoku puzzle solver with beautiful UI
"""

import customtkinter as ctk
import random


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SudokuSolver(ctk.CTk):
    """Sudoku Solver Application"""
    
    def __init__(self):
        super().__init__()
        
        self.title("🔢 Sudoku Solver")
        self.geometry("700x750")
        self.resizable(False, False)
        
        self.entries = []
        self.setup_ui()
        
    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(
            self.main_frame,
            text="🔢 Sudoku Solver",
            font=ctk.CTkFont(size=36, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            self.main_frame,
            text="Enter numbers and click Solve, or generate a puzzle",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
        # Sudoku Grid
        self.grid_frame = ctk.CTkFrame(self.main_frame)
        self.grid_frame.pack(pady=20)
        
        self.create_grid()
        
        # Controls
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            self.controls_frame,
            text="✨ Solve",
            command=self.solve,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color="#27AE60",
            hover_color="#229954"
        ).pack(side="left", padx=5, expand=True, fill="x")
        
        ctk.CTkButton(
            self.controls_frame,
            text="🎲 Generate Puzzle",
            command=self.generate_puzzle,
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=10,
            fg_color="#3498DB",
            hover_color="#2980B9"
        ).pack(side="left", padx=5, expand=True, fill="x")
        
        ctk.CTkButton(
            self.controls_frame,
            text="🗑 Clear",
            command=self.clear_grid,
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=10,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        ).pack(side="left", padx=5, expand=True, fill="x")
        
        # Status
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Enter your puzzle and click Solve",
            font=ctk.CTkFont(size=16),
            text_color="#9B59B6"
        )
        self.status_label.pack(pady=10)
        
    def create_grid(self):
        """Create 9x9 Sudoku grid"""
        self.entries = []
        
        for row in range(9):
            self.grid_frame.grid_rowconfigure(row, weight=1)
            row_entries = []
            for col in range(9):
                self.grid_frame.grid_columnconfigure(col, weight=1)
                
                padx = 2
                pady = 2
                
                # Add extra spacing for 3x3 boxes
                if col % 3 == 0 and col > 0:
                    padx = (10, 2)
                if row % 3 == 0 and row > 0:
                    pady = (10, 2)
                
                entry = ctk.CTkEntry(
                    self.grid_frame,
                    width=50,
                    height=50,
                    font=ctk.CTkFont(size=20, weight="bold"),
                    justify="center"
                )
                entry.grid(row=row, column=col, padx=padx, pady=pady)
                
                # Validate input
                entry.configure(validate="key")
                entry.configure(validatecommand=(self.register(self.validate_input), '%P'))
                
                row_entries.append(entry)
            self.entries.append(row_entries)
            
    def validate_input(self, value):
        """Validate input is 1-9 or empty"""
        if value == "" or (value.isdigit() and 1 <= int(value) <= 9):
            return True
        return False
        
    def get_grid(self):
        """Get current grid values"""
        grid = []
        for row in range(9):
            grid_row = []
            for col in range(9):
                val = self.entries[row][col].get()
                grid_row.append(int(val) if val else 0)
            grid.append(grid_row)
        return grid
        
    def set_grid(self, grid):
        """Set grid values"""
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, 'end')
                if grid[row][col] != 0:
                    self.entries[row][col].insert(0, str(grid[row][col]))
                    
    def solve(self):
        """Solve the Sudoku puzzle"""
        grid = self.get_grid()
        
        if self.solve_sudoku(grid):
            self.set_grid(grid)
            self.status_label.configure(text="✅ Puzzle solved successfully!", text_color="#27AE60")
        else:
            self.status_label.configure(text="❌ No solution exists!", text_color="#E74C3C")
            
    def solve_sudoku(self, board):
        """Solve Sudoku using backtracking"""
        empty = self.find_empty(board)
        if not empty:
            return True
            
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(board, num, row, col):
                board[row][col] = num
                
                if self.solve_sudoku(board):
                    return True
                    
                board[row][col] = 0
                
        return False
        
    def find_empty(self, board):
        """Find empty cell"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
        
    def is_valid(self, board, num, row, col):
        """Check if number is valid in position"""
        # Check row
        if num in board[row]:
            return False
            
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
            
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
                    
        return True
        
    def generate_puzzle(self):
        """Generate a random Sudoku puzzle"""
        # Create solved grid first
        grid = [[0] * 9 for _ in range(9)]
        self.solve_sudoku(grid)
        
        # Remove random cells to create puzzle
        cells_to_remove = random.randint(40, 50)
        for _ in range(cells_to_remove):
            row, col = random.randint(0, 8), random.randint(0, 8)
            grid[row][col] = 0
            
        self.set_grid(grid)
        self.status_label.configure(text="🎲 New puzzle generated!", text_color="#3498DB")
        
    def clear_grid(self):
        """Clear all entries"""
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, 'end')
        self.status_label.configure(text="🗑 Grid cleared", text_color="gray")


if __name__ == "__main__":
    app = SudokuSolver()
    app.mainloop()
