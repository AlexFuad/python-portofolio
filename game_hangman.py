"""
Hangman Game - Modern GUI Version
Classic word guessing game with beautiful UI
"""

import customtkinter as ctk
import random
import os


# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class HangmanGame(ctk.CTk):
    """Hangman Game Application"""
    
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("🎯 Hangman Game")
        self.geometry("900x650")
        self.resizable(True, True)
        self.minsize(800, 600)
        
        # Game state
        self.word_list = [
            "PYTHON", "PROGRAMMING", "COMPUTER", "ALGORITHM", "DEVELOPER",
            "FUNCTION", "VARIABLE", "DATABASE", "INTERFACE", "NETWORK",
            "SOFTWARE", "HARDWARE", "KEYBOARD", "MONITOR", "PROCESSOR",
            "TECHNOLOGY", "INTERNET", "WEBSITE", "BROWSER", "SERVER",
            "GALAXY", "UNIVERSE", "PLANET", "ASTRONAUT", "ROCKET",
            "MOUNTAIN", "OCEAN", "FOREST", "DESERT", "ISLAND",
            "CHOCOLATE", "PINEAPPLE", "STRAWBERRY", "VANILLA", "CINNAMON"
        ]
        self.current_word = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong = 6
        self.game_over = False
        self.game_won = False
        
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
            text="🎯 Hangman Game",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        # ========== HANGMAN DISPLAY ==========
        self.hangman_frame = ctk.CTkFrame(self.main_frame)
        self.hangman_frame.pack(fill="x", pady=(0, 15))
        
        self.hangman_display = ctk.CTkLabel(
            self.hangman_frame,
            text="",
            font=ctk.CTkFont(size=14, family="monospace"),
            justify="left"
        )
        self.hangman_display.pack(pady=10)
        
        # ========== WORD DISPLAY ==========
        self.word_frame = ctk.CTkFrame(self.main_frame)
        self.word_frame.pack(fill="x", pady=(0, 15))
        
        self.word_label = ctk.CTkLabel(
            self.word_frame,
            text="",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        self.word_label.pack(pady=15)
        
        # ========== STATUS ==========
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", pady=(0, 15))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=18)
        )
        self.status_label.pack(pady=5)
        
        self.wrong_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.wrong_label.pack(pady=5)
        
        # ========== GUESSED LETTERS ==========
        self.guessed_frame = ctk.CTkFrame(self.main_frame)
        self.guessed_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            self.guessed_frame,
            text="Guessed Letters:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(5, 5))
        
        self.guessed_label = ctk.CTkLabel(
            self.guessed_frame,
            text="",
            font=ctk.CTkFont(size=14),
            wraplength=700
        )
        self.guessed_label.pack(pady=5)
        
        # ========== LETTER BUTTONS ==========
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.pack(fill="x", pady=(0, 15))
        
        self.letter_buttons = {}
        self.create_letter_buttons()
        
        # ========== CONTROL BUTTONS ==========
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(fill="x")
        
        self.new_game_btn = ctk.CTkButton(
            self.controls_frame,
            text="🎮 New Game",
            command=self.new_game,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color="#27AE60",
            hover_color="#229954"
        )
        self.new_game_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
    def create_letter_buttons(self):
        """Create letter buttons grid"""
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        button_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=5)
        
        for i, letter in enumerate(letters):
            row = i // 9
            col = i % 9
            
            btn = ctk.CTkButton(
                button_frame,
                text=letter,
                command=lambda l=letter: self.guess_letter(l),
                font=ctk.CTkFont(size=16, weight="bold"),
                width=60,
                height=45,
                corner_radius=8,
                fg_color="#3498DB",
                hover_color="#2980B9"
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.letter_buttons[letter] = btn
            
    def new_game(self):
        """Start a new game"""
        self.current_word = random.choice(self.word_list)
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.game_won = False
        
        # Reset UI
        for letter, btn in self.letter_buttons.items():
            btn.configure(state="normal", fg_color="#3498DB", hover_color="#2980B9")
            
        self.update_display()
        
    def guess_letter(self, letter):
        """Guess a letter"""
        if self.game_over or letter in self.guessed_letters:
            return
            
        self.guessed_letters.add(letter)
        
        # Disable the button
        btn = self.letter_buttons.get(letter)
        if btn:
            if letter in self.current_word:
                btn.configure(fg_color="#27AE60", hover_color="#229954", state="disabled")
            else:
                btn.configure(fg_color="#E74C3C", hover_color="#C0392B", state="disabled")
        
        # Check if letter is in word
        if letter not in self.current_word:
            self.wrong_guesses += 1
            
        # Check win/lose
        self.check_game_status()
        self.update_display()
        
    def check_game_status(self):
        """Check if game is won or lost"""
        # Check win
        word_letters = set(self.current_word)
        if word_letters.issubset(self.guessed_letters):
            self.game_over = True
            self.game_won = True
            return
            
        # Check lose
        if self.wrong_guesses >= self.max_wrong:
            self.game_over = True
            self.game_won = False
            
    def update_display(self):
        """Update all displays"""
        # Update hangman ASCII art
        self.hangman_display.configure(text=self.get_hangman_art())
        
        # Update word display
        display_word = " ".join([
            letter if letter in self.guessed_letters else "_"
            for letter in self.current_word
        ])
        self.word_label.configure(text=display_word)
        
        # Update status
        if self.game_over:
            if self.game_won:
                self.status_label.configure(text="🎉 Congratulations! You Won!", text_color="#27AE60")
            else:
                self.status_label.configure(
                    text=f"💀 Game Over! The word was: {self.current_word}",
                    text_color="#E74C3C"
                )
        else:
            self.status_label.configure(text="🤔 Guess a letter!", text_color="#3498DB")
            
        # Update wrong guesses
        self.wrong_label.configure(
            text=f"Wrong: {self.wrong_guesses}/{self.max_wrong}"
        )
        
        # Update guessed letters
        if self.guessed_letters:
            self.guessed_label.configure(text=", ".join(sorted(self.guessed_letters)))
        else:
            self.guessed_label.configure(text="No letters guessed yet")
            
    def get_hangman_art(self):
        """Get hangman ASCII art based on wrong guesses"""
        stages = [
            """
               _______
              |/      |
              |      
              |      
              |      
              |      
              |
           ___|___
          |       |___
          |___________|
            """,
            """
               _______
              |/      |
              |      (_)
              |      
              |      
              |      
              |
           ___|___
          |       |___
          |___________|
            """,
            """
               _______
              |/      |
              |      (_)
              |       |
              |       |
              |      
              |
           ___|___
          |       |___
          |___________|
            """,
            """
               _______
              |/      |
              |      (_)
              |      /|
              |       |
              |      
              |
           ___|___
          |       |___
          |___________|
            """,
            """
               _______
              |/      |
              |      (_)
              |      /|\\
              |       |
              |      
              |
           ___|___
          |       |___
          |___________|
            """,
            """
               _______
              |/      |
              |      (_)
              |      /|\\
              |       |
              |      /
              |
           ___|___
          |       |___
          |___________|
            """,
            """
               _______
              |/      |
              |      (_)
              |      /|\\
              |       |
              |      / \\
              |
           ___|___
          |       |___
          |___________|
            """
        ]
        return stages[self.wrong_guesses]


if __name__ == "__main__":
    # Create and run the application
    app = HangmanGame()
    app.mainloop()
