"""
Tetris Game - Modern GUI using customtkinter
Controls: Left/Right arrows to move, Up to rotate, Down for soft drop, Space for hard drop
"""

import customtkinter as ctk
import random
import time

# Configure appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Game constants
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 30
INITIAL_SPEED = 500  # ms per drop
SPEED_INCREMENT = 50  # ms faster per level
LINES_PER_LEVEL = 10

# Tetromino shapes (each rotation state)
TETROMINOES = {
    "I": {
        "shape": [
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(2, 0), (2, 1), (2, 2), (2, 3)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
        ],
        "color": "#00f0f0",
    },
    "O": {
        "shape": [
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
        ],
        "color": "#f0f000",
    },
    "T": {
        "shape": [
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
        ],
        "color": "#a000f0",
    },
    "S": {
        "shape": [
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
            [(1, 1), (2, 1), (0, 2), (1, 2)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
        ],
        "color": "#00f000",
    },
    "Z": {
        "shape": [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(2, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
        ],
        "color": "#f00000",
    },
    "J": {
        "shape": [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ],
        "color": "#0000f0",
    },
    "L": {
        "shape": [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ],
        "color": "#f0a000",
    },
}

# Scoring
SCORE_TABLE = {1: 100, 2: 300, 3: 500, 4: 800}


class TetrisGame:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Tetris")
        self.root.geometry("700x680")
        self.root.resizable(False, False)

        # Game state
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.paused = False
        self.running = False

        # Current piece
        self.current_piece = None
        self.current_piece_type = None
        self.current_rotation = 0
        self.piece_x = 0
        self.piece_y = 0

        # Next piece
        self.next_piece_type = None
        self.next_rotation = 0

        # Game loop
        self.game_loop_id = None
        self.last_drop_time = 0

        self._setup_ui()
        self._bind_keys()

    def _setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="TETRIS",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00ff88",
        )
        title.pack(pady=(10, 5))

        # Game area frame
        game_area = ctk.CTkFrame(main_frame, fg_color="#1a1a2e")
        game_area.pack(fill="both", expand=True)

        # Left panel - Stats
        stats_frame = ctk.CTkFrame(game_area, fg_color="#16213e", corner_radius=10)
        stats_frame.pack(side="left", padx=(10, 5), fill="y")

        # Score
        ctk.CTkLabel(stats_frame, text="SCORE", font=ctk.CTkFont(size=14, weight="bold"), text_color="#888").pack(
            pady=(20, 5)
        )
        self.score_label = ctk.CTkLabel(
            stats_frame, text="0", font=ctk.CTkFont(size=24, weight="bold"), text_color="#00ff88"
        )
        self.score_label.pack()

        # Level
        ctk.CTkLabel(stats_frame, text="LEVEL", font=ctk.CTkFont(size=14, weight="bold"), text_color="#888").pack(
            pady=(20, 5)
        )
        self.level_label = ctk.CTkLabel(
            stats_frame, text="1", font=ctk.CTkFont(size=24, weight="bold"), text_color="#00aaff"
        )
        self.level_label.pack()

        # Lines
        ctk.CTkLabel(stats_frame, text="LINES", font=ctk.CTkFont(size=14, weight="bold"), text_color="#888").pack(
            pady=(20, 5)
        )
        self.lines_label = ctk.CTkLabel(
            stats_frame, text="0", font=ctk.CTkFont(size=24, weight="bold"), text_color="#ffaa00"
        )
        self.lines_label.pack()

        # Next piece preview
        ctk.CTkLabel(stats_frame, text="NEXT", font=ctk.CTkFont(size=14, weight="bold"), text_color="#888").pack(
            pady=(20, 5)
        )
        self.next_canvas = ctk.CTkCanvas(
            stats_frame,
            width=120,
            height=120,
            bg="#0f0f23",
            highlightthickness=2,
            highlightcolor="#333",
        )
        self.next_canvas.pack(pady=5)

        # Controls info
        controls_frame = ctk.CTkFrame(game_area, fg_color="#16213e", corner_radius=10)
        controls_frame.pack(side="right", padx=(5, 10), fill="y")

        ctk.CTkLabel(
            controls_frame, text="CONTROLS", font=ctk.CTkFont(size=14, weight="bold"), text_color="#888"
        ).pack(pady=(20, 10))

        controls_text = [
            ("← →", "Move"),
            ("↑", "Rotate"),
            ("↓", "Soft Drop"),
            ("Space", "Hard Drop"),
            ("P", "Pause"),
        ]
        for key, action in controls_text:
            ctk.CTkLabel(
                controls_frame,
                text=f"{key}: {action}",
                font=ctk.CTkFont(size=12),
                text_color="#aaa",
            ).pack(pady=2)

        # Game canvas
        canvas_frame = ctk.CTkFrame(game_area, fg_color="#0f0f23", corner_radius=10, border_width=2, border_color="#333")
        canvas_frame.pack(side="left", padx=5)

        self.canvas = ctk.CTkCanvas(
            canvas_frame,
            width=BOARD_WIDTH * CELL_SIZE,
            height=BOARD_HEIGHT * CELL_SIZE,
            bg="#0f0f23",
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=10)

        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a2e")
        buttons_frame.pack(pady=(10, 10))

        self.start_btn = ctk.CTkButton(
            buttons_frame,
            text="START",
            command=self.start_game,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#00ff88",
            hover_color="#00cc6a",
            text_color="#000",
            width=100,
            height=35,
            corner_radius=8,
        )
        self.start_btn.pack(side="left", padx=10)

        self.pause_btn = ctk.CTkButton(
            buttons_frame,
            text="PAUSE",
            command=self.toggle_pause,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#00aaff",
            hover_color="#0088cc",
            text_color="#000",
            width=100,
            height=35,
            corner_radius=8,
            state="disabled",
        )
        self.pause_btn.pack(side="left", padx=10)

        self.restart_btn = ctk.CTkButton(
            buttons_frame,
            text="RESTART",
            command=self.restart_game,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#ff6644",
            hover_color="#cc5533",
            text_color="#000",
            width=100,
            height=35,
            corner_radius=8,
        )
        self.restart_btn.pack(side="left", padx=10)

        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Press START to play",
            font=ctk.CTkFont(size=14),
            text_color="#888",
        )
        self.status_label.pack(pady=(0, 10))

    def _bind_keys(self):
        self.root.bind("<Left>", lambda e: self._move_left())
        self.root.bind("<Right>", lambda e: self._move_right())
        self.root.bind("<Down>", lambda e: self._soft_drop())
        self.root.bind("<Up>", lambda e: self._rotate())
        self.root.bind("<space>", lambda e: self._hard_drop())
        self.root.bind("p", lambda e: self.toggle_pause())
        self.root.bind("P", lambda e: self.toggle_pause())

    def _get_drop_speed(self):
        return max(100, INITIAL_SPEED - (self.level - 1) * SPEED_INCREMENT)

    def _new_piece(self):
        if self.next_piece_type is None:
            self.next_piece_type = random.choice(list(TETROMINOES.keys()))
            self.next_rotation = 0

        self.current_piece_type = self.next_piece_type
        self.current_rotation = self.next_rotation

        # Generate next piece
        self.next_piece_type = random.choice(list(TETROMINOES.keys()))
        self.next_rotation = 0

        # Position new piece
        shape = TETROMINOES[self.current_piece_type]["shape"][self.current_rotation]
        min_x = min(x for x, y in shape)
        max_x = max(x for x, y in shape)
        piece_width = max_x - min_x + 1
        self.piece_x = (BOARD_WIDTH - piece_width) // 2 - min_x
        self.piece_y = -min(y for x, y in shape)

        # Check if piece can be placed
        if not self._is_valid_position(self.piece_x, self.piece_y, self.current_rotation):
            self.game_over = True
            self.running = False
            self.status_label.configure(text="GAME OVER!", text_color="#ff4444")
            self.pause_btn.configure(state="disabled")
            self._show_game_over()
            return False

        return True

    def _is_valid_position(self, x, y, rotation):
        shape = TETROMINOES[self.current_piece_type]["shape"][rotation]
        for sx, sy in shape:
            bx, by = x + sx, y + sy
            if bx < 0 or bx >= BOARD_WIDTH or by >= BOARD_HEIGHT:
                return False
            if by >= 0 and self.board[by][bx] is not None:
                return False
        return True

    def _lock_piece(self):
        shape = TETROMINOES[self.current_piece_type]["shape"][self.current_rotation]
        color = TETROMINOES[self.current_piece_type]["color"]
        for sx, sy in shape:
            bx, by = self.piece_x + sx, self.piece_y + sy
            if 0 <= by < BOARD_HEIGHT and 0 <= bx < BOARD_WIDTH:
                self.board[by][bx] = color

        # Check for completed lines
        self._clear_lines()

        # Spawn new piece
        if not self._new_piece():
            return

        # Reset drop timer
        self.last_drop_time = time.time()

    def _clear_lines(self):
        lines_cleared = 0
        new_board = []
        for row in self.board:
            if all(cell is not None for cell in row):
                lines_cleared += 1
            else:
                new_board.append(row)

        # Add empty rows at the top
        while len(new_board) < BOARD_HEIGHT:
            new_board.insert(0, [None for _ in range(BOARD_WIDTH)])

        self.board = new_board

        if lines_cleared > 0:
            self.lines += lines_cleared
            self.score += SCORE_TABLE.get(lines_cleared, 800) * self.level
            self.level = self.lines // LINES_PER_LEVEL + 1

            self._update_stats()

    def _move_piece(self, dx, dy):
        if not self.running or self.paused or self.game_over or self.current_piece is None:
            return False

        new_x = self.piece_x + dx
        new_y = self.piece_y + dy

        if self._is_valid_position(new_x, new_y, self.current_rotation):
            self.piece_x = new_x
            self.piece_y = new_y
            return True
        return False

    def _rotate_piece(self):
        if not self.running or self.paused or self.game_over or self.current_piece is None:
            return False

        if self.current_piece_type == "O":
            return True  # O piece doesn't rotate

        new_rotation = (self.current_rotation + 1) % 4

        # Try normal rotation
        if self._is_valid_position(self.piece_x, self.piece_y, new_rotation):
            self.current_rotation = new_rotation
            return True

        # Wall kick attempts
        for kick in [-1, 1, -2, 2]:
            if self._is_valid_position(self.piece_x + kick, self.piece_y, new_rotation):
                self.piece_x += kick
                self.current_rotation = new_rotation
                return True

        return False

    def _move_left(self):
        if self.running and not self.paused and not self.game_over:
            self._move_piece(-1, 0)
            self._draw()

    def _move_right(self):
        if self.running and not self.paused and not self.game_over:
            self._move_piece(1, 0)
            self._draw()

    def _soft_drop(self):
        if self.running and not self.paused and not self.game_over:
            if not self._move_piece(0, 1):
                self._lock_piece()
            self.score += 1
            self._update_stats()
            self._draw()
            self.last_drop_time = time.time()

    def _hard_drop(self):
        if self.running and not self.paused and not self.game_over:
            drop_distance = 0
            while self._move_piece(0, 1):
                drop_distance += 1
            self.score += drop_distance * 2
            self._update_stats()
            self._lock_piece()
            self._draw()

    def _rotate(self):
        if self.running and not self.paused and not self.game_over:
            self._rotate_piece()
            self._draw()

    def _update_stats(self):
        self.score_label.configure(text=str(self.score))
        self.level_label.configure(text=str(self.level))
        self.lines_label.configure(text=str(self.lines))

    def _draw_cell(self, x, y, color, size=CELL_SIZE):
        """Draw a single cell with a 3D effect"""
        padding = 1
        self.canvas.create_rectangle(
            x * size + padding,
            y * size + padding,
            (x + 1) * size - padding,
            (y + 1) * size - padding,
            fill=color,
            outline=color,
            width=1,
        )
        # Highlight
        self.canvas.create_rectangle(
            x * size + padding,
            y * size + padding,
            (x + 1) * size - padding,
            y * size + 4,
            fill=self._lighten_color(color, 30),
            outline="",
        )
        # Shadow
        self.canvas.create_rectangle(
            x * size + padding,
            (y + 1) * size - 4,
            (x + 1) * size - padding,
            (y + 1) * size - padding,
            fill=self._darken_color(color, 30),
            outline="",
        )

    def _lighten_color(self, color, amount):
        """Lighten a hex color"""
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        r = min(255, r + amount)
        g = min(255, g + amount)
        b = min(255, b + amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _darken_color(self, color, amount):
        """Darken a hex color"""
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        r = max(0, r - amount)
        g = max(0, g - amount)
        b = max(0, b - amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw(self):
        self.canvas.delete("all")

        # Draw grid lines
        for x in range(BOARD_WIDTH + 1):
            self.canvas.create_line(
                x * CELL_SIZE, 0, x * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE, fill="#1a1a3e", width=1
            )
        for y in range(BOARD_HEIGHT + 1):
            self.canvas.create_line(
                0, y * CELL_SIZE, BOARD_WIDTH * CELL_SIZE, y * CELL_SIZE, fill="#1a1a3e", width=1
            )

        # Draw locked pieces
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x] is not None:
                    self._draw_cell(x, y, self.board[y][x])

        # Draw ghost piece (shadow showing where piece will land)
        if self.current_piece_type and self.running and not self.game_over:
            ghost_y = self.piece_y
            while self._is_valid_position(self.piece_x, ghost_y + 1, self.current_rotation):
                ghost_y += 1
            if ghost_y != self.piece_y:
                shape = TETROMINOES[self.current_piece_type]["shape"][self.current_rotation]
                color = TETROMINOES[self.current_piece_type]["color"]
                for sx, sy in shape:
                    bx, by = self.piece_x + sx, ghost_y + sy
                    if 0 <= by < BOARD_HEIGHT and 0 <= bx < BOARD_WIDTH:
                        padding = 1
                        self.canvas.create_rectangle(
                            bx * CELL_SIZE + padding,
                            by * CELL_SIZE + padding,
                            (bx + 1) * CELL_SIZE - padding,
                            (by + 1) * CELL_SIZE - padding,
                            fill="",
                            outline=color,
                            width=1,
                            dash=(3, 3),
                        )

        # Draw current piece
        if self.current_piece_type and self.running and not self.game_over:
            shape = TETROMINOES[self.current_piece_type]["shape"][self.current_rotation]
            color = TETROMINOES[self.current_piece_type]["color"]
            for sx, sy in shape:
                bx, by = self.piece_x + sx, self.piece_y + sy
                if 0 <= by < BOARD_HEIGHT and 0 <= bx < BOARD_WIDTH:
                    self._draw_cell(bx, by, color)

        # Draw next piece preview
        self._draw_next_piece()

    def _draw_next_piece(self):
        self.next_canvas.delete("all")
        if not self.next_piece_type:
            return

        shape = TETROMINOES[self.next_piece_type]["shape"][0]
        color = TETROMINOES[self.next_piece_type]["color"]

        # Calculate bounds
        min_x = min(x for x, y in shape)
        max_x = max(x for x, y in shape)
        min_y = min(y for x, y in shape)
        max_y = max(y for x, y in shape)
        piece_w = (max_x - min_x + 1) * 25
        piece_h = (max_y - min_y + 1) * 25
        offset_x = (120 - piece_w) // 2
        offset_y = (120 - piece_h) // 2

        for sx, sy in shape:
            x = offset_x + (sx - min_x) * 25
            y = offset_y + (sy - min_y) * 25
            self.next_canvas.create_rectangle(
                x + 1, y + 1, x + 24, y + 24, fill=color, outline=color, width=1
            )
            # Highlight
            self.next_canvas.create_rectangle(
                x + 1, y + 1, x + 24, y + 4, fill=self._lighten_color(color, 30), outline=""
            )

    def _show_game_over(self):
        self.canvas.create_rectangle(
            50, BOARD_HEIGHT * CELL_SIZE // 2 - 40,
            BOARD_WIDTH * CELL_SIZE - 50, BOARD_HEIGHT * CELL_SIZE // 2 + 40,
            fill="#000000", outline="#ff4444", width=2, stipple="gray50"
        )
        self.canvas.create_text(
            BOARD_WIDTH * CELL_SIZE // 2,
            BOARD_HEIGHT * CELL_SIZE // 2 - 10,
            text="GAME OVER",
            fill="#ff4444",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.canvas.create_text(
            BOARD_WIDTH * CELL_SIZE // 2,
            BOARD_HEIGHT * CELL_SIZE // 2 + 20,
            text=f"Score: {self.score}",
            fill="#ffffff",
            font=ctk.CTkFont(size=16),
        )

    def _game_loop(self):
        if not self.running or self.game_over:
            return

        if not self.paused:
            current_time = time.time()
            drop_interval = self._get_drop_speed() / 1000.0

            if current_time - self.last_drop_time >= drop_interval:
                if not self._move_piece(0, 1):
                    self._lock_piece()
                self._draw()
                self.last_drop_time = current_time

        self.game_loop_id = self.root.after(50, self._game_loop)

    def start_game(self):
        if self.running:
            return

        self.running = True
        self.game_over = False
        self.paused = False
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines = 0
        self.next_piece_type = None
        self.last_drop_time = time.time()

        self._update_stats()
        self.start_btn.configure(state="disabled")
        self.pause_btn.configure(state="normal", text="PAUSE")
        self.status_label.configure(text="Game in progress", text_color="#00ff88")

        # Spawn first piece
        self._new_piece()
        self._draw()

        # Start game loop
        if self.game_loop_id:
            self.root.after_cancel(self.game_loop_id)
        self._game_loop()

    def toggle_pause(self):
        if not self.running or self.game_over:
            return

        self.paused = not self.paused
        if self.paused:
            self.pause_btn.configure(text="RESUME")
            self.status_label.configure(text="PAUSED", text_color="#ffaa00")
        else:
            self.pause_btn.configure(text="PAUSE")
            self.status_label.configure(text="Game in progress", text_color="#00ff88")
            self.last_drop_time = time.time()

    def restart_game(self):
        # Cancel existing loop
        if self.game_loop_id:
            self.root.after_cancel(self.game_loop_id)
            self.game_loop_id = None

        self.running = False
        self.paused = False
        self.game_over = False
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines = 0
        self.current_piece_type = None
        self.next_piece_type = None

        self._update_stats()
        self.start_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled", text="PAUSE")
        self.status_label.configure(text="Press START to play", text_color="#888")

        self._draw()

    def run(self):
        self._draw()
        self.root.mainloop()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()
