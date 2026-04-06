"""
Tic-Tac-Toe Game - Modern GUI Version
Classic two-player strategy game with beautiful UI
"""

import customtkinter as ctk
import random
from tkinter import messagebox


# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class TicTacToeGame(ctk.CTk):
    """Tic-Tac-Toe Game Application"""
    
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("⭕ Tic-Tac-Toe ❌")
        self.geometry("700x750")
        self.resizable(True, True)
        self.minsize(600, 650)
        
        # Game state
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.player_x_score = 0
        self.player_o_score = 0
        self.draws = 0
        self.game_mode = "PvP"  # PvP or PvAI
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the User Interface"""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ========== HEADER ==========
        self.header_frame = ctk.CTkFrame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 15))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="⭕ Tic-Tac-Toe ❌",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        # ========== GAME MODE SELECTOR ==========
        self.mode_frame = ctk.CTkFrame(self.main_frame)
        self.mode_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            self.mode_frame,
            text="Game Mode:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=(10, 5), pady=10)
        
        self.mode_var = ctk.StringVar(value="PvP")
        
        self.pvp_radio = ctk.CTkRadioButton(
            self.mode_frame,
            text="👥 Player vs Player",
            variable=self.mode_var,
            value="PvP",
            command=self.reset_game,
            font=ctk.CTkFont(size=13)
        )
        self.pvp_radio.pack(side="left", padx=10, pady=10)
        
        self.pvai_radio = ctk.CTkRadioButton(
            self.mode_frame,
            text="🤖 Player vs AI",
            variable=self.mode_var,
            value="PvAI",
            command=self.reset_game,
            font=ctk.CTkFont(size=13)
        )
        self.pvai_radio.pack(side="left", padx=10, pady=10)
        
        # ========== SCORE BOARD ==========
        self.score_frame = ctk.CTkFrame(self.main_frame)
        self.score_frame.pack(fill="x", pady=(0, 15))
        
        # Player X Score
        self.score_x_label = ctk.CTkLabel(
            self.score_frame,
            text="❌ Player X: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#E74C3C"
        )
        self.score_x_label.grid(row=0, column=0, padx=20, pady=10)
        
        # Draws
        self.draw_label = ctk.CTkLabel(
            self.score_frame,
            text="🤝 Draws: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#95A5A6"
        )
        self.draw_label.grid(row=0, column=1, padx=20, pady=10)
        
        # Player O Score
        self.score_o_label = ctk.CTkLabel(
            self.score_frame,
            text="⭕ Player O: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#3498DB"
        )
        self.score_o_label.grid(row=0, column=2, padx=20, pady=10)
        
        # ========== STATUS ==========
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", pady=(0, 15))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="❌ Player X's turn",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.status_label.pack(pady=10)
        
        # ========== GAME BOARD ==========
        self.board_frame = ctk.CTkFrame(self.main_frame)
        self.board_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.buttons = []
        self.create_board()
        
        # ========== CONTROL BUTTONS ==========
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(fill="x")
        
        self.reset_btn = ctk.CTkButton(
            self.controls_frame,
            text="🔄 Reset Game",
            command=self.reset_game,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color="#F39C12",
            hover_color="#E67E22"
        )
        self.reset_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.new_game_btn = ctk.CTkButton(
            self.controls_frame,
            text="📊 Reset Scores",
            command=self.reset_scores,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        self.new_game_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
    def create_board(self):
        """Create the game board buttons"""
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)
            
        for i in range(9):
            row = i // 3
            col = i % 3
            
            btn = ctk.CTkButton(
                self.board_frame,
                text="",
                command=lambda idx=i: self.make_move(idx),
                font=ctk.CTkFont(size=48, weight="bold"),
                width=150,
                height=150,
                corner_radius=12,
                fg_color="#2C3E50",
                hover_color="#34495E"
            )
            btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            self.buttons.append(btn)
            
    def make_move(self, index):
        """Make a move on the board"""
        if self.board[index] != "" or self.game_over:
            return
            
        # Update board
        self.board[index] = self.current_player
        self.buttons[index].configure(
            text=self.get_player_symbol(self.current_player),
            fg_color=self.get_player_color(self.current_player)
        )
        
        # Check for winner
        if self.check_winner():
            self.game_over = True
            winner = self.current_player
            self.update_score(winner)
            self.status_label.configure(
                text=f"🎉 Player {self.get_player_symbol(winner)} wins!",
                text_color=self.get_player_color(winner)
            )
            self.disable_board()
            return
            
        # Check for draw
        if self.check_draw():
            self.game_over = True
            self.draws += 1
            self.update_score_display()
            self.status_label.configure(text="🤝 It's a draw!", text_color="#95A5A6")
            return
            
        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_status()
        
        # AI move if in PvAI mode
        if self.game_mode == "PvAI" and self.current_player == "O" and not self.game_over:
            self.after(500, self.ai_move)
            
    def ai_move(self):
        """AI makes a move using minimax algorithm"""
        if self.game_over:
            return
            
        # Try to win first
        move = self.find_best_move("O")
        if move == -1:
            # Block opponent
            move = self.find_best_move("X")
        if move == -1:
            # Take center
            if self.board[4] == "":
                move = 4
        if move == -1:
            # Take corner
            corners = [0, 2, 6, 8]
            available_corners = [c for c in corners if self.board[c] == ""]
            if available_corners:
                move = random.choice(available_corners)
        if move == -1:
            # Take any available
            available = [i for i, x in enumerate(self.board) if x == ""]
            if available:
                move = random.choice(available)
                
        if move != -1:
            self.make_move(move)
            
    def find_best_move(self, player):
        """Find winning move for a player"""
        win_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        
        for combo in win_combos:
            marks = [self.board[i] for i in combo]
            if marks.count(player) == 2 and marks.count("") == 1:
                return combo[marks.index("")]
        return -1
        
    def get_player_symbol(self, player):
        """Get player symbol"""
        return "❌" if player == "X" else "⭕"
        
    def get_player_color(self, player):
        """Get player color"""
        return "#E74C3C" if player == "X" else "#3498DB"
        
    def check_winner(self):
        """Check if there's a winner"""
        win_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        
        for combo in win_combos:
            if self.board[combo[0]] != "" and all(
                self.board[i] == self.board[combo[0]] for i in combo
            ):
                return True
        return False
        
    def check_draw(self):
        """Check if game is a draw"""
        return all(cell != "" for cell in self.board)
        
    def update_status(self):
        """Update status label"""
        self.status_label.configure(
            text=f"{self.get_player_symbol(self.current_player)} Player {self.current_player}'s turn",
            text_color=self.get_player_color(self.current_player)
        )
        
    def update_score(self, winner):
        """Update score display"""
        if winner == "X":
            self.player_x_score += 1
        else:
            self.player_o_score += 1
        self.update_score_display()
        
    def update_score_display(self):
        """Update score labels"""
        self.score_x_label.configure(text=f"❌ Player X: {self.player_x_score}")
        self.score_o_label.configure(text=f"⭕ Player O: {self.player_o_score}")
        self.draw_label.configure(text=f"🤝 Draws: {self.draws}")
        
    def disable_board(self):
        """Disable all buttons"""
        for btn in self.buttons:
            btn.configure(state="disabled")
            
    def enable_board(self):
        """Enable all buttons"""
        for btn in self.buttons:
            if self.board[self.buttons.index(btn)] == "":
                btn.configure(state="normal", fg_color="#2C3E50", text="")
                
    def reset_game(self):
        """Reset the game"""
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        
        for btn in self.buttons:
            btn.configure(text="", fg_color="#2C3E50", state="normal")
            
        self.update_status()
        
    def reset_scores(self):
        """Reset all scores"""
        self.player_x_score = 0
        self.player_o_score = 0
        self.draws = 0
        self.update_score_display()
        self.reset_game()


if __name__ == "__main__":
    # Create and run the application
    app = TicTacToeGame()
    app.mainloop()
