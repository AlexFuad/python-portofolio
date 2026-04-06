"""
Memory Puzzle Game - Modern GUI Version
Card matching memory game with beautiful UI
"""

import customtkinter as ctk
import random


# Set appearance mode
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MemoryPuzzleGame(ctk.CTk):
    """Memory Puzzle Game Application"""
    
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("🧠 Memory Puzzle")
        self.geometry("800x750")
        self.resizable(True, True)
        self.minsize(700, 650)
        
        # Game state
        self.emojis = ["🎮", "🎯", "🎪", "🎨", "🎭", "🎸", "🎺", "🎻"]
        self.cards = []
        self.flipped_cards = []
        self.matched_pairs = 0
        self.moves = 0
        self.total_pairs = len(self.emojis)
        self.game_started = False
        
        # Setup UI
        self.setup_ui()
        self.new_game()
        
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
            text="🧠 Memory Puzzle",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        # ========== STATS ==========
        self.stats_frame = ctk.CTkFrame(self.main_frame)
        self.stats_frame.pack(fill="x", pady=(0, 15))
        
        self.moves_label = ctk.CTkLabel(
            self.stats_frame,
            text="Moves: 0",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#3498DB"
        )
        self.moves_label.pack(side="left", padx=30, pady=8)
        
        self.pairs_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"Pairs: 0/{self.total_pairs}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#27AE60"
        )
        self.pairs_label.pack(side="left", padx=30, pady=8)
        
        self.timer_label = ctk.CTkLabel(
            self.stats_frame,
            text="⏱️ Time: 0s",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F39C12"
        )
        self.timer_label.pack(side="right", padx=30, pady=8)
        
        # ========== STATUS ==========
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="🎮 Click cards to find matching pairs!",
            font=ctk.CTkFont(size=18),
            text_color="#9B59B6"
        )
        self.status_label.pack(pady=(0, 15))
        
        # ========== GAME BOARD ==========
        self.board_frame = ctk.CTkFrame(self.main_frame)
        self.board_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.card_buttons = []
        self.create_board()
        
        # ========== CONTROLS ==========
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(fill="x")
        
        ctk.CTkButton(
            self.controls_frame,
            text="🔄 New Game",
            command=self.new_game,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color="#27AE60",
            hover_color="#229954"
        ).pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        ctk.CTkButton(
            self.controls_frame,
            text="🎨 Change Theme",
            command=self.change_theme,
            font=ctk.CTkFont(size=16),
            height=45,
            corner_radius=10,
            fg_color="#9B59B6",
            hover_color="#8E44AD"
        ).pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
    def create_board(self):
        """Create the game board"""
        # Clear existing buttons
        self.card_buttons = []
        
        # Configure grid
        rows, cols = 4, 4
        for i in range(rows):
            self.board_frame.grid_rowconfigure(i, weight=1)
            for j in range(cols):
                self.board_frame.grid_columnconfigure(j, weight=1)
                
        # Create card pairs
        card_values = self.emojis * 2
        random.shuffle(card_values)
        
        # Create buttons
        for i in range(rows * cols):
            row = i // cols
            col = i % cols
            
            btn = ctk.CTkButton(
                self.board_frame,
                text="❓",
                command=lambda idx=i: self.flip_card(idx),
                font=ctk.CTkFont(size=40),
                corner_radius=12,
                fg_color="#34495E",
                hover_color="#2C3E50"
            )
            btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            self.card_buttons.append(btn)
            
        self.cards = card_values
        
    def flip_card(self, index):
        """Flip a card"""
        # Prevent flipping if already 2 cards flipped or card already matched
        if len(self.flipped_cards) >= 2:
            return
            
        if index in self.flipped_cards:
            return
            
        card_btn = self.card_buttons[index]
        if card_btn.cget("text") != "❓":
            return
            
        # Flip the card
        card_btn.configure(
            text=self.cards[index],
            fg_color="#ECF0F1",
            hover_color="#BDC3C7"
        )
        self.flipped_cards.append(index)
        
        # Check for match when 2 cards are flipped
        if len(self.flipped_cards) == 2:
            self.moves += 1
            self.moves_label.configure(text=f"Moves: {self.moves}")
            self.after(1000, self.check_match)
            
    def check_match(self):
        """Check if flipped cards match"""
        idx1, idx2 = self.flipped_cards
        
        if self.cards[idx1] == self.cards[idx2]:
            # Match found
            self.matched_pairs += 1
            self.pairs_label.configure(text=f"Pairs: {self.matched_pairs}/{self.total_pairs}")
            
            # Keep cards revealed with green color
            self.card_buttons[idx1].configure(fg_color="#27AE60", state="disabled")
            self.card_buttons[idx2].configure(fg_color="#27AE60", state="disabled")
            
            # Check win
            if self.matched_pairs == self.total_pairs:
                self.status_label.configure(
                    text=f"🎉 Congratulations! You won in {self.moves} moves!",
                    text_color="#27AE60"
                )
        else:
            # No match - flip back
            self.card_buttons[idx1].configure(
                text="❓",
                fg_color="#34495E",
                hover_color="#2C3E50"
            )
            self.card_buttons[idx2].configure(
                text="❓",
                fg_color="#34495E",
                hover_color="#2C3E50"
            )
            
        self.flipped_cards = []
        
    def new_game(self):
        """Start a new game"""
        self.flipped_cards = []
        self.matched_pairs = 0
        self.moves = 0
        
        self.moves_label.configure(text="Moves: 0")
        self.pairs_label.configure(text=f"Pairs: 0/{self.total_pairs}")
        self.status_label.configure(
            text="🎮 Click cards to find matching pairs!",
            text_color="#9B59B6"
        )
        
        self.create_board()
        
    def change_theme(self):
        """Change card emoji theme"""
        themes = [
            ["🎮", "🎯", "🎪", "🎨", "🎭", "🎸", "🎺", "🎻"],
            ["🍎", "🍊", "🍋", "🍇", "🍓", "🍒", "🍑", "🍍"],
            ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"],
            ["🚗", "🚕", "🚙", "🚌", "🚎", "🏎️", "🚓", "🚑"],
            ["⚽", "🏀", "🏈", "⚾", "🎾", "🏐", "🎱", "🏓"]
        ]
        current_idx = themes.index(self.emojis) if self.emojis in themes else 0
        self.emojis = themes[(current_idx + 1) % len(themes)]
        self.total_pairs = len(self.emojis)
        self.new_game()


if __name__ == "__main__":
    app = MemoryPuzzleGame()
    app.mainloop()
