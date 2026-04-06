"""
Snake Game - Modern GUI Version
Classic arcade snake game with beautiful UI
"""

import customtkinter as ctk
import tkinter as tk
import random


# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SnakeGame(ctk.CTk):
    """Snake Game Application"""
    
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("🐍 Snake Game")
        self.geometry("700x750")
        self.resizable(False, False)
        
        # Game settings
        self.grid_size = 20
        self.cell_size = 25
        self.canvas_size = self.grid_size * self.cell_size
        
        # Game state
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "Right"
        self.food = None
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_started = False
        self.speed = 100
        
        # Setup UI
        self.setup_ui()
        self.create_food()
        self.draw()
        
    def setup_ui(self):
        """Setup the User Interface"""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # ========== HEADER ==========
        self.header_frame = ctk.CTkFrame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🐍 Snake Game",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=8)
        
        # ========== SCORE BOARD ==========
        self.score_frame = ctk.CTkFrame(self.main_frame)
        self.score_frame.pack(fill="x", pady=(0, 10))
        
        self.score_label = ctk.CTkLabel(
            self.score_frame,
            text="Score: 0",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#27AE60"
        )
        self.score_label.pack(side="left", padx=20, pady=5)
        
        self.high_score_label = ctk.CTkLabel(
            self.score_frame,
            text="🏆 High Score: 0",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F39C12"
        )
        self.high_score_label.pack(side="right", padx=20, pady=5)
        
        # ========== GAME CANVAS ==========
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#1E1E1E",
            highlightthickness=0
        )
        self.canvas.pack(pady=10, padx=10)
        
        # Bind keyboard events
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.change_direction)
        self.canvas.bind("<space>", self.start_game)
        
        # ========== STATUS ==========
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Press SPACE to start or Arrow keys to play",
            font=ctk.CTkFont(size=16),
            text_color="#3498DB"
        )
        self.status_label.pack(pady=5)
        
        # ========== CONTROLS ==========
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(fill="x")
        
        self.restart_btn = ctk.CTkButton(
            self.controls_frame,
            text="🔄 Restart Game",
            command=self.restart,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        self.restart_btn.pack(side="left", padx=10, pady=8, expand=True, fill="x")
        
        self.speed_btn = ctk.CTkButton(
            self.controls_frame,
            text="⚡ Speed: Normal",
            command=self.toggle_speed,
            font=ctk.CTkFont(size=14),
            height=40,
            corner_radius=8,
            fg_color="#9B59B6",
            hover_color="#8E44AD"
        )
        self.speed_btn.pack(side="left", padx=10, pady=8, expand=True, fill="x")
        
    def create_food(self):
        """Create food at random position"""
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
                
    def draw(self):
        """Draw the game state"""
        self.canvas.delete("all")
        
        # Draw grid lines (subtle)
        for i in range(self.grid_size + 1):
            self.canvas.create_line(
                i * self.cell_size, 0,
                i * self.cell_size, self.canvas_size,
                fill="#2C2C2C", width=1
            )
            self.canvas.create_line(
                0, i * self.cell_size,
                self.canvas_size, i * self.cell_size,
                fill="#2C2C2C", width=1
            )
            
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                # Head
                color = "#27AE60"
            else:
                # Body
                color = "#2ECC71"
                
            self.canvas.create_rectangle(
                x * self.cell_size + 1,
                y * self.cell_size + 1,
                (x + 1) * self.cell_size - 1,
                (y + 1) * self.cell_size - 1,
                fill=color,
                outline="#1E1E1E",
                width=2
            )
            
        # Draw food
        if self.food:
            x, y = self.food
            self.canvas.create_oval(
                x * self.cell_size + 2,
                y * self.cell_size + 2,
                (x + 1) * self.cell_size - 2,
                (y + 1) * self.cell_size - 2,
                fill="#E74C3C",
                outline="#C0392B",
                width=2
            )
            
    def change_direction(self, event):
        """Change snake direction"""
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            # Prevent 180-degree turns
            opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if event.keysym != opposites.get(self.direction):
                self.direction = event.keysym
                
            if not self.game_started:
                self.start_game(event)
                
    def start_game(self, event=None):
        """Start the game"""
        if not self.game_started and not self.game_over:
            self.game_started = True
            self.status_label.configure(text="🎮 Game in progress!", text_color="#27AE60")
            self.move_snake()
            
    def move_snake(self):
        """Move the snake"""
        if not self.game_started or self.game_over:
            return
            
        # Get head position
        head_x, head_y = self.snake[0]
        
        # Calculate new head position
        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        else:  # Right
            new_head = (head_x + 1, head_y)
            
        # Check collisions
        if self.check_collision(new_head):
            self.game_over = True
            self.status_label.configure(
                text=f"💀 Game Over! Score: {self.score}",
                text_color="#E74C3C"
            )
            if self.score > self.high_score:
                self.high_score = self.score
                self.high_score_label.configure(text=f"🏆 High Score: {self.high_score}")
            return
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.score_label.configure(text=f"Score: {self.score}")
            self.create_food()
        else:
            # Remove tail
            self.snake.pop()
            
        # Draw and schedule next move
        self.draw()
        self.canvas.after(self.speed, self.move_snake)
        
    def check_collision(self, position):
        """Check if position causes collision"""
        x, y = position
        
        # Wall collision
        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return True
            
        # Self collision
        if position in self.snake:
            return True
            
        return False
        
    def restart(self):
        """Restart the game"""
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "Right"
        self.score = 0
        self.game_over = False
        self.game_started = False
        
        self.score_label.configure(text="Score: 0")
        self.status_label.configure(
            text="Press SPACE to start or Arrow keys to play",
            text_color="#3498DB"
        )
        
        self.create_food()
        self.draw()
        
    def toggle_speed(self):
        """Toggle game speed"""
        if self.speed == 100:
            self.speed = 60
            self.speed_btn.configure(text="⚡ Speed: Fast")
        else:
            self.speed = 100
            self.speed_btn.configure(text="⚡ Speed: Normal")


if __name__ == "__main__":
    # Create and run the application
    app = SnakeGame()
    app.mainloop()
