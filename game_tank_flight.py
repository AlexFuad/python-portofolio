"""
Tank Flight - A Flappy Bird-style game with a tank.
Uses customtkinter for modern dark GUI and tkinter canvas for game rendering.

Controls: Spacebar or Mouse Click to fly/jump
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import math
import os
import time

# Set appearance theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GAME_WIDTH = 700
GAME_HEIGHT = 500
TANK_SIZE = 40
TANK_WIDTH = 50
OBSTACLE_WIDTH = 60
OBSTACLE_GAP = 160
OBSTACLE_SPEED_INITIAL = 3
GRAVITY = 0.45
JUMP_STRENGTH = -8.5
OBSTACLE_SPAWN_INTERVAL = 1800  # milliseconds
SCORE_INCREMENT = 1
HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tank_flight_high_score.txt")


class Tank:
    """Represents the flying tank."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 120
        self.y = GAME_HEIGHT // 2
        self.velocity = 0
        self.angle = 0
        self.id = None
        self.turret_id = None
        self.barrel_id = None
        self.tracks_id = None
        self.draw()

    def draw(self):
        """Draw the tank on canvas."""
        # Tank body
        body_color = "#4a7c59"
        body_dark = "#3a5f47"
        track_color = "#2d2d2d"
        track_detail = "#3d3d3d"
        turret_color = "#3d6b4a"
        barrel_color = "#555555"

        # Calculate rotation points
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)

        # Main body (rectangle)
        body_points = [
            (-TANK_WIDTH // 2, -TANK_SIZE // 3),
            (TANK_WIDTH // 2, -TANK_SIZE // 3),
            (TANK_WIDTH // 2, TANK_SIZE // 3),
            (-TANK_WIDTH // 2, TANK_SIZE // 3),
        ]

        # Rotate body points
        rotated_body = [(int(self.x + px * cos_a - py * sin_a),
                         int(self.y + px * sin_a + py * cos_a)) for px, py in body_points]

        self.id = self.canvas.create_polygon(rotated_body, fill=body_color, outline="#2a4f35", width=2)

        # Tracks (bottom)
        track_offset = TANK_SIZE // 3
        track_points = [
            (-TANK_WIDTH // 2 + 2, track_offset),
            (TANK_WIDTH // 2 - 2, track_offset),
            (TANK_WIDTH // 2 - 5, track_offset + 8),
            (-TANK_WIDTH // 2 + 5, track_offset + 8),
        ]

        rotated_tracks = [(int(self.x + px * cos_a - py * sin_a),
                           int(self.y + px * sin_a + py * cos_a)) for px, py in track_points]

        self.tracks_id = self.canvas.create_polygon(rotated_tracks, fill=track_color, outline="#1a1a1a", width=1)

        # Track details
        for i in range(-3, 4):
            tx = i * 7
            ty = track_offset + 4
            rtx = int(self.x + tx * cos_a - ty * sin_a)
            rty = int(self.y + tx * sin_a + ty * cos_a)
            self.canvas.create_oval(rtx - 2, rty - 2, rtx + 2, rty + 2, fill=track_detail)

        # Turret (top)
        turret_offset = -TANK_SIZE // 4
        turret_points = [
            (-12, turret_offset),
            (12, turret_offset),
            (10, turret_offset - 12),
            (-10, turret_offset - 12),
        ]

        rotated_turret = [(int(self.x + px * cos_a - py * sin_a),
                           int(self.y + px * sin_a + py * cos_a)) for px, py in turret_points]

        self.turret_id = self.canvas.create_polygon(rotated_turret, fill=turret_color, outline="#2a4f35", width=1)

        # Barrel
        barrel_length = 25
        barrel_end_x = barrel_length
        barrel_end_y = turret_offset - 6
        barrel_start_x = 5
        barrel_start_y = turret_offset - 3

        bex = int(self.x + barrel_end_x * cos_a - barrel_end_y * sin_a)
        bey = int(self.y + barrel_end_x * sin_a + barrel_end_y * cos_a)
        bsx = int(self.x + barrel_start_x * cos_a - barrel_start_y * sin_a)
        bsy = int(self.y + barrel_start_x * sin_a + barrel_start_y * cos_a)

        self.barrel_id = self.canvas.create_line(bsx, bsy, bex, bey, fill=barrel_color, width=5)

    def update(self):
        """Update tank position based on physics."""
        self.velocity += GRAVITY
        self.y += self.velocity

        # Calculate angle based on velocity
        self.angle = max(-0.5, min(0.5, self.velocity * 0.05))

        # Clamp position
        if self.y < TANK_SIZE:
            self.y = TANK_SIZE
            self.velocity = 0
        if self.y > GAME_HEIGHT - TANK_SIZE:
            self.y = GAME_HEIGHT - TANK_SIZE
            self.velocity = 0

    def jump(self):
        """Make the tank jump."""
        self.velocity = JUMP_STRENGTH

    def redraw(self):
        """Redraw the tank."""
        self.canvas.delete(self.id)
        self.canvas.delete(self.turret_id)
        self.canvas.delete(self.barrel_id)
        self.canvas.delete(self.tracks_id)
        self.draw()

    def get_bounds(self):
        """Get tank collision bounds (simplified rectangle)."""
        return (
            self.x - TANK_WIDTH // 2 + 5,
            self.y - TANK_SIZE // 2 + 5,
            self.x + TANK_WIDTH // 2 - 5,
            self.y + TANK_SIZE // 2 - 5,
        )


class Obstacle:
    """Represents a pair of obstacles (top and bottom barriers)."""

    def __init__(self, canvas, x, gap_center, speed):
        self.canvas = canvas
        self.x = x
        self.gap_center = gap_center
        self.gap_top = gap_center - OBSTACLE_GAP // 2
        self.gap_bottom = gap_center + OBSTACLE_GAP // 2
        self.speed = speed
        self.passed = False
        self.top_id = None
        self.bottom_id = None
        self.draw()

    def draw(self):
        """Draw the obstacles."""
        top_color = "#8b4513"
        top_light = "#a0522d"
        top_dark = "#6b3410"

        # Top obstacle
        self.top_id = self.canvas.create_rectangle(
            self.x, 0, self.x + OBSTACLE_WIDTH, self.gap_top,
            fill=top_color, outline="#4a2a0a", width=2
        )
        # Top obstacle bottom edge (lip)
        self.canvas.create_rectangle(
            self.x - 5, self.gap_top - 15, self.x + OBSTACLE_WIDTH + 5, self.gap_top,
            fill=top_light, outline="#4a2a0a", width=1
        )

        # Bottom obstacle
        self.bottom_id = self.canvas.create_rectangle(
            self.x, self.gap_bottom, self.x + OBSTACLE_WIDTH, GAME_HEIGHT,
            fill=top_color, outline="#4a2a0a", width=2
        )
        # Bottom obstacle top edge (lip)
        self.canvas.create_rectangle(
            self.x - 5, self.gap_bottom, self.x + OBSTACLE_WIDTH + 5, self.gap_bottom + 15,
            fill=top_light, outline="#4a2a0a", width=1
        )

        # Add some texture/details to top obstacle
        for i in range(0, int(self.gap_top), 40):
            self.canvas.create_rectangle(
                self.x + 5, i, self.x + OBSTACLE_WIDTH - 5, i + 3,
                fill=top_dark, outline=""
            )

        # Add some texture/details to bottom obstacle
        for i in range(int(self.gap_bottom), GAME_HEIGHT, 40):
            self.canvas.create_rectangle(
                self.x + 5, i, self.x + OBSTACLE_WIDTH - 5, i + 3,
                fill=top_dark, outline=""
            )

    def update(self):
        """Move the obstacle."""
        self.x -= self.speed
        self.canvas.move(self.top_id, -self.speed, 0)
        self.canvas.move(self.bottom_id, -self.speed, 0)
        # Move all child items (the lips and details)
        for item in self.canvas.find_all():
            # Items associated with this obstacle will move via canvas.move on their parent
            pass

    def is_off_screen(self):
        """Check if obstacle is off the left side."""
        return self.x + OBSTACLE_WIDTH < 0

    def collides_with(self, tank_bounds):
        """Check collision with tank."""
        tx1, ty1, tx2, ty2 = tank_bounds

        # Check top obstacle
        if tx2 > self.x and tx1 < self.x + OBSTACLE_WIDTH:
            if ty1 < self.gap_top or ty2 > self.gap_bottom:
                return True
        return False


class Particle:
    """Smoke/exhaust particle."""

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = random.randint(2, 5)
        self.life = 30
        self.max_life = 30
        self.vx = random.uniform(-2, -0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.id = canvas.create_oval(
            x - self.radius, y - self.radius,
            x + self.radius, y + self.radius,
            fill="#666666", outline=""
        )

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.radius += 0.2
        alpha = int(255 * (self.life / self.max_life))
        color = f"#{alpha // 17:02x}{alpha // 17:02x}{alpha // 17:02x}"
        self.canvas.coords(self.id,
                           self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius)
        self.canvas.itemconfig(self.id, fill=color)
        return self.life > 0

    def destroy(self):
        self.canvas.delete(self.id)


class TankFlightGame:
    """Main game class."""

    def __init__(self):
        # Main window
        self.root = ctk.CTk()
        self.root.title("Tank Flight")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # High score
        self.high_score = self.load_high_score()

        # Game state
        self.game_state = "menu"  # menu, playing, game_over
        self.score = 0
        self.obstacles = []
        self.particles = []
        self.speed = OBSTACLE_SPEED_INITIAL
        self.last_obstacle_time = 0
        self.game_start_time = 0

        # Layout
        self.setup_ui()

        # Bind events
        self.root.bind("<space>", self.on_jump)
        self.root.bind("<Return>", self.on_action)
        self.canvas.bind("<Button-1>", self.on_jump)
        self.canvas.bind("<Button-3>", self.on_jump)

        # Start game loop
        self.game_loop()
        self.root.mainloop()

    def setup_ui(self):
        """Set up the UI elements."""
        # Title frame
        title_frame = ctk.CTkFrame(self.root, width=WINDOW_WIDTH, height=50)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            title_frame, text="TANK FLIGHT",
            font=("Segoe UI", 28, "bold"),
            text_color="#4a9eff"
        )
        title_label.pack(pady=8)

        # Score frame
        score_frame = ctk.CTkFrame(self.root, width=WINDOW_WIDTH, height=40)
        score_frame.pack(fill="x", padx=0, pady=0)
        score_frame.pack_propagate(False)

        self.score_label = ctk.CTkLabel(
            score_frame, text="Score: 0  |  High Score: 0  |  Speed: 3",
            font=("Segoe UI", 16),
            text_color="#aaaaaa"
        )
        self.score_label.pack(pady=5)

        # Game canvas
        self.canvas = tk.Canvas(
            self.root,
            width=GAME_WIDTH,
            height=GAME_HEIGHT,
            bg="#1a1a2e",
            highlightthickness=2,
            highlightbackground="#2a2a4e"
        )
        self.canvas.pack(pady=10)

        # Background elements
        self.draw_background()

        # Instructions frame
        instr_frame = ctk.CTkFrame(self.root, width=WINDOW_WIDTH, height=50)
        instr_frame.pack(fill="x", padx=10, pady=5)
        instr_frame.pack_propagate(False)

        self.instr_label = ctk.CTkLabel(
            instr_frame,
            text="Press SPACE or CLICK to fly | Avoid the barriers | Survive as long as possible!",
            font=("Segoe UI", 13),
            text_color="#888888"
        )
        self.instr_label.pack(pady=12)

    def draw_background(self):
        """Draw static background elements."""
        # Stars
        for _ in range(50):
            x = random.randint(0, GAME_WIDTH)
            y = random.randint(0, GAME_HEIGHT)
            size = random.randint(1, 3)
            brightness = random.randint(100, 200)
            color = f"#{brightness:02x}{brightness:02x}{brightness + 55:02x}"
            self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")

        # Ground
        self.canvas.create_rectangle(
            0, GAME_HEIGHT - 30, GAME_WIDTH, GAME_HEIGHT,
            fill="#2d4a2d", outline="#1a2e1a", width=2
        )
        # Ground details
        for i in range(0, GAME_WIDTH, 20):
            self.canvas.create_line(
                i, GAME_HEIGHT - 30, i + 10, GAME_HEIGHT - 35,
                fill="#3a5f3a", width=2
            )
        self.canvas.create_line(
            0, GAME_HEIGHT - 30, GAME_WIDTH, GAME_HEIGHT - 30,
            fill="#4a7c4a", width=3
        )

    def start_game(self):
        """Start a new game."""
        self.game_state = "playing"
        self.score = 0
        self.speed = OBSTACLE_SPEED_INITIAL
        self.obstacles = []
        self.particles = []
        self.last_obstacle_time = time.time() * 1000
        self.game_start_time = time.time()

        # Clear canvas items except background
        self.canvas.delete("all")
        self.draw_background()

        # Create tank
        self.tank = Tank(self.canvas)

        # Show initial message briefly
        self.show_message("GO!", "#4a9eff", 500)

    def show_message(self, text, color, duration=1000):
        """Show a temporary message on the canvas."""
        msg_id = self.canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT // 2,
            text=text, fill=color,
            font=("Segoe UI", 48, "bold")
        )
        self.root.after(duration, lambda: self.canvas.delete(msg_id))

    def draw_menu_screen(self):
        """Draw the menu screen overlay."""
        self.canvas.delete("all")
        self.draw_background()

        # Title
        self.canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT // 3,
            text="TANK FLIGHT",
            fill="#4a9eff",
            font=("Segoe UI", 52, "bold")
        )

        # Subtitle
        self.canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT // 3 + 60,
            text="A Flappy Tank Game",
            fill="#888888",
            font=("Segoe UI", 18)
        )

        # Instructions
        instructions = [
            "SPACE / CLICK to fly",
            "Avoid the barriers",
            "Survive to score points",
            "Difficulty increases over time"
        ]
        for i, inst in enumerate(instructions):
            self.canvas.create_text(
                GAME_WIDTH // 2, GAME_HEIGHT // 2 + 40 + i * 30,
                text=inst,
                fill="#aaaaaa",
                font=("Segoe UI", 14)
            )

        # Start prompt
        self.canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT - 80,
            text="Press SPACE or CLICK to Start",
            fill="#4a9eff",
            font=("Segoe UI", 20, "bold")
        )

        # High score
        if self.high_score > 0:
            self.canvas.create_text(
                GAME_WIDTH // 2, GAME_HEIGHT - 40,
                text=f"High Score: {self.high_score}",
                fill="#ffd700",
                font=("Segoe UI", 16)
            )

    def draw_game_over_screen(self):
        """Draw the game over screen."""
        # Dim overlay
        self.canvas.create_rectangle(
            0, 0, GAME_WIDTH, GAME_HEIGHT,
            fill="#000000", stipple="gray50"
        )

        # Game Over text
        self.canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT // 3,
            text="GAME OVER",
            fill="#ff4444",
            font=("Segoe UI", 52, "bold")
        )

        # Score
        self.canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT // 2,
            text=f"Score: {self.score}",
            fill="#ffffff",
            font=("Segoe UI", 28)
        )

        # High score
        if self.score >= self.high_score and self.score > 0:
            self.canvas.create_text(
                GAME_WIDTH // 2, GAME_HEIGHT // 2 + 45,
                text="NEW HIGH SCORE!",
                fill="#ffd700",
                font=("Segoe UI", 22, "bold")
            )
        else:
            self.canvas.create_text(
                GAME_WIDTH // 2, GAME_HEIGHT // 2 + 45,
                text=f"High Score: {self.high_score}",
                fill="#ffd700",
                font=("Segoe UI", 18)
            )

        # Restart prompt
        self.canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT - 80,
            text="Press SPACE or CLICK to Restart",
            fill="#4a9eff",
            font=("Segoe UI", 18, "bold")
        )

    def spawn_obstacle(self):
        """Create a new obstacle pair."""
        min_gap_center = 80 + OBSTACLE_GAP // 2
        max_gap_center = GAME_HEIGHT - 30 - OBSTACLE_GAP // 2
        gap_center = random.randint(min_gap_center, max_gap_center)

        obstacle = Obstacle(self.canvas, GAME_WIDTH + 20, gap_center, self.speed)
        self.obstacles.append(obstacle)

    def on_jump(self, event=None):
        """Handle jump input."""
        if self.game_state == "menu":
            self.start_game()
        elif self.game_state == "playing":
            self.tank.jump()
            # Add exhaust particles
            for _ in range(3):
                particle = Particle(self.canvas, self.tank.x - 20, self.tank.y + 10)
                self.particles.append(particle)
        elif self.game_state == "game_over":
            self.start_game()

    def on_action(self, event=None):
        """Handle action key (Enter)."""
        if self.game_state == "menu":
            self.start_game()
        elif self.game_state == "game_over":
            self.start_game()

    def check_collision(self):
        """Check if tank collides with anything."""
        tank_bounds = self.tank.get_bounds()

        # Check ground/ceiling
        if self.tank.y >= GAME_HEIGHT - 30 - TANK_SIZE // 2 + 5:
            return True
        if self.tank.y <= TANK_SIZE // 2 - 5:
            return True

        # Check obstacles
        for obstacle in self.obstacles:
            if obstacle.collides_with(tank_bounds):
                return True

        return False

    def update_score_display(self):
        """Update the score label."""
        self.score_label.configure(
            text=f"Score: {self.score}  |  High Score: {self.high_score}  |  Speed: {self.speed:.1f}"
        )

    def load_high_score(self):
        """Load high score from file."""
        try:
            if os.path.exists(HIGH_SCORE_FILE):
                with open(HIGH_SCORE_FILE, "r") as f:
                    return int(f.read().strip())
        except (ValueError, IOError):
            pass
        return 0

    def save_high_score(self):
        """Save high score to file."""
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open(HIGH_SCORE_FILE, "w") as f:
                    f.write(str(self.high_score))
            except IOError:
                pass

    def game_loop(self):
        """Main game loop, runs every frame."""
        if self.game_state == "menu":
            self.draw_menu_screen()

        elif self.game_state == "playing":
            # Update tank
            self.tank.update()
            self.tank.redraw()

            # Spawn obstacles
            current_time = time.time() * 1000
            spawn_interval = max(800, OBSTACLE_SPAWN_INTERVAL - (self.speed - OBSTACLE_SPEED_INITIAL) * 100)
            if current_time - self.last_obstacle_time > spawn_interval:
                self.spawn_obstacle()
                self.last_obstacle_time = current_time

            # Update obstacles
            for obstacle in self.obstacles[:]:
                # Check if passed
                if not obstacle.passed and obstacle.x + OBSTACLE_WIDTH < self.tank.x:
                    obstacle.passed = True
                    self.score += SCORE_INCREMENT

                    # Increase difficulty
                    if self.score % 5 == 0:
                        self.speed += 0.3

                # Remove off-screen obstacles
                if obstacle.is_off_screen():
                    self.canvas.delete(obstacle.top_id)
                    self.canvas.delete(obstacle.bottom_id)
                    self.obstacles.remove(obstacle)

            # Update particles
            for particle in self.particles[:]:
                if not particle.update():
                    particle.destroy()
                    self.particles.remove(particle)

            # Add idle exhaust particles
            if random.random() < 0.3:
                particle = Particle(self.canvas, self.tank.x - 25, self.tank.y + 8)
                self.particles.append(particle)

            # Check collisions
            if self.check_collision():
                self.game_state = "game_over"
                self.save_high_score()
                self.draw_game_over_screen()

            # Update score display
            self.update_score_display()

        # Schedule next frame (approximately 60 fps)
        self.root.after(16, self.game_loop)


def main():
    """Entry point."""
    TankFlightGame()


if __name__ == "__main__":
    main()
