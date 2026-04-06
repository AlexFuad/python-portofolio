"""
Pong Game - Modern GUI Version
Classic two-player paddle game with beautiful UI
"""

import customtkinter as ctk
import tkinter as tk
import random


# Set appearance mode
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class PongGame(ctk.CTk):
    """Pong Game Application"""
    
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("🏓 Pong Game")
        self.geometry("900x650")
        self.resizable(False, False)
        
        # Game settings
        self.canvas_width = 800
        self.canvas_height = 500
        self.paddle_width = 100
        self.paddle_height = 15
        self.ball_size = 15
        self.paddle_speed = 20
        
        # Game state
        self.player1_score = 0
        self.player2_score = 0
        self.game_paused = False
        self.game_mode = "PvAI"  # PvAI or PvP
        
        # Setup UI
        self.setup_ui()
        self.start_new_game()
        
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
            text="🏓 Pong Game",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=8)
        
        # ========== GAME MODE ==========
        self.mode_frame = ctk.CTkFrame(self.main_frame)
        self.mode_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            self.mode_frame,
            text="Mode:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=(10, 5), pady=8)
        
        self.mode_var = ctk.StringVar(value="PvAI")
        
        ctk.CTkRadioButton(
            self.mode_frame,
            text="🤖 vs AI",
            variable=self.mode_var,
            value="PvAI",
            command=self.restart,
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=10, pady=8)
        
        ctk.CTkRadioButton(
            self.mode_frame,
            text="👥 2 Players",
            variable=self.mode_var,
            value="PvP",
            command=self.restart,
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=10, pady=8)
        
        # ========== SCORE BOARD ==========
        self.score_frame = ctk.CTkFrame(self.main_frame)
        self.score_frame.pack(fill="x", pady=(0, 10))
        
        self.score1_label = ctk.CTkLabel(
            self.score_frame,
            text="👤 Player 1: 0",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#3498DB"
        )
        self.score1_label.pack(side="left", padx=40, pady=5)
        
        self.score2_label = ctk.CTkLabel(
            self.score_frame,
            text="👤 Player 2: 0",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#E74C3C"
        )
        self.score2_label.pack(side="right", padx=40, pady=5)
        
        # ========== GAME CANVAS ==========
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#0a0a0a",
            highlightthickness=0
        )
        self.canvas.pack(pady=10, padx=10)
        
        # Bind events
        self.canvas.bind("<Motion>", self.move_paddle_mouse)
        self.canvas.bind("<Left>", lambda e: self.move_paddle_key("Left"))
        self.canvas.bind("<Right>", lambda e: self.move_paddle_key("Right"))
        self.canvas.bind("<a>", lambda e: self.move_paddle_key("a"))
        self.canvas.bind("<d>", lambda e: self.move_paddle_key("d"))
        self.canvas.bind("<space>", lambda e: self.toggle_pause())
        self.canvas.focus_set()
        
        # ========== STATUS ==========
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="🎮 Move mouse or use A/D keys to play | SPACE to pause",
            font=ctk.CTkFont(size=14),
            text_color="#3498DB"
        )
        self.status_label.pack(pady=5)
        
        # ========== CONTROLS ==========
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(fill="x")
        
        ctk.CTkButton(
            self.controls_frame,
            text="🔄 Restart",
            command=self.restart,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        ).pack(side="left", padx=10, pady=8, expand=True, fill="x")
        
    def start_new_game(self):
        """Initialize new game"""
        # Paddle positions
        self.paddle1_x = (self.canvas_width - self.paddle_width) / 2
        self.paddle2_x = (self.canvas_width - self.paddle_width) / 2
        
        # Ball position and velocity
        self.reset_ball()
        
        # Start game loop
        self.game_running = True
        self.game_loop()
        
    def reset_ball(self):
        """Reset ball to center"""
        self.ball_x = self.canvas_width / 2
        self.ball_y = self.canvas_height / 2
        self.ball_dx = random.choice([-5, 5])
        self.ball_dy = random.uniform(-3, 3)
        
    def move_paddle_mouse(self, event):
        """Move paddle with mouse"""
        if self.game_paused:
            return
        self.paddle1_x = event.x - self.paddle_width / 2
        self.paddle1_x = max(0, min(self.canvas_width - self.paddle_width, self.paddle1_x))
        
    def move_paddle_key(self, key):
        """Move paddle with keyboard"""
        if self.game_paused:
            return
        if key in ["Left", "a"]:
            self.paddle1_x = max(0, self.paddle1_x - self.paddle_speed)
        elif key in ["Right", "d"]:
            self.paddle1_x = min(self.canvas_width - self.paddle_width, self.paddle1_x + self.paddle_speed)
        
    def toggle_pause(self):
        """Toggle game pause"""
        self.game_paused = not self.game_paused
        if self.game_paused:
            self.status_label.configure(text="⏸️ Game Paused", text_color="#F39C12")
        else:
            self.status_label.configure(text="🎮 Game Running", text_color="#27AE60")
            self.game_loop()
        
    def update_ai(self):
        """Update AI paddle"""
        if self.game_mode != "PvAI" or self.game_paused:
            return
            
        # AI follows ball with some delay
        target_x = self.ball_x - self.paddle_width / 2
        diff = target_x - self.paddle2_x
        
        if abs(diff) > 10:
            self.paddle2_x += diff * 0.08
            
        self.paddle2_x = max(0, min(self.canvas_width - self.paddle_width, self.paddle2_x))
        
    def game_loop(self):
        """Main game loop"""
        if self.game_paused or not self.game_running:
            return
            
        # Update ball position
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Wall collisions (top/bottom)
        if self.ball_y <= 0 or self.ball_y >= self.canvas_height - self.ball_size:
            self.ball_dy = -self.ball_dy
            
        # Paddle 1 collision (bottom)
        if (self.ball_y + self.ball_size >= self.canvas_height - 30 and
            self.paddle1_x <= self.ball_x <= self.paddle1_x + self.paddle_width):
            self.ball_dy = -abs(self.ball_dy) * 1.05
            self.ball_dx *= 1.02
            
        # Paddle 2 collision (top)
        if (self.ball_y <= 30 and
            self.paddle2_x <= self.ball_x <= self.paddle2_x + self.paddle_width):
            self.ball_dy = abs(self.ball_dy) * 1.05
            self.ball_dx *= 1.02
            
        # Score
        if self.ball_y < 0:
            self.player1_score += 1
            self.update_score()
            self.reset_ball()
        elif self.ball_y > self.canvas_height:
            self.player2_score += 1
            self.update_score()
            self.reset_ball()
            
        # Update AI
        self.update_ai()
        
        # Draw everything
        self.draw()
        
        # Schedule next frame
        self.canvas.after(16, self.game_loop)  # ~60 FPS
        
    def update_score(self):
        """Update score display"""
        mode_text = "AI" if self.game_mode == "PvAI" else "2"
        self.score1_label.configure(text=f"👤 Player 1: {self.player1_score}")
        self.score2_label.configure(text=f"🤖 {mode_text}: {self.player2_score}")
        
    def draw(self):
        """Draw game elements"""
        self.canvas.delete("all")
        
        # Draw center line
        for i in range(0, self.canvas_height, 20):
            self.canvas.create_rectangle(
                self.canvas_width / 2 - 2, i,
                self.canvas_width / 2 + 2, i + 10,
                fill="#333"
            )
            
        # Draw paddles
        self.canvas.create_rectangle(
            self.paddle1_x, self.canvas_height - 30,
            self.paddle1_x + self.paddle_width, self.canvas_height - 30 + self.paddle_height,
            fill="#3498DB", outline="#2980B9", width=2
        )
        
        self.canvas.create_rectangle(
            self.paddle2_x, 20,
            self.paddle2_x + self.paddle_width, 20 + self.paddle_height,
            fill="#E74C3C", outline="#C0392B", width=2
        )
        
        # Draw ball
        self.canvas.create_oval(
            self.ball_x, self.ball_y,
            self.ball_x + self.ball_size, self.ball_y + self.ball_size,
            fill="#F39C12", outline="#E67E22", width=2
        )
        
    def restart(self):
        """Restart the game"""
        self.game_mode = self.mode_var.get()
        self.player1_score = 0
        self.player2_score = 0
        self.game_paused = False
        self.game_running = True
        self.update_score()
        self.start_new_game()
        self.status_label.configure(text="🎮 Game Running", text_color="#27AE60")


if __name__ == "__main__":
    app = PongGame()
    app.mainloop()
