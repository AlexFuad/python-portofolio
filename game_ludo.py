"""
Ludo Board Game - Modern GUI using customtkinter
A simplified implementation with 4 players, dice rolling, and AI opponents.
"""

import customtkinter as ctk
import random
import time
from typing import List, Tuple, Optional

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Colors for players
PLAYER_COLORS = {
    0: "#FF4444",  # Red
    1: "#44FF44",  # Green
    2: "#FFDD44",  # Yellow
    3: "#4488FF",  # Blue
}

PLAYER_NAMES = {
    0: "Red",
    1: "Green",
    2: "Yellow",
    3: "Blue",
}

# Board layout constants
CELL_SIZE = 45
BOARD_OFFSET_X = 20
BOARD_OFFSET_Y = 80
DICE_SIZE = 70

# Path definitions for each player (52 main path cells + 6 home stretch cells)
# The main path goes around the board. Each player starts at a different position.
MAIN_PATH_CELLS = [
    # Red start area (bottom-left quadrant, going up then right)
    (6, 1), (6, 2), (6, 3), (6, 4), (6, 5),  # Up column
    (5, 6), (4, 6), (3, 6), (2, 6), (1, 6), (0, 6),  # Left to top
    (0, 7), (0, 8),  # Top middle
    (1, 8), (2, 8), (3, 8), (4, 8), (5, 8),  # Down column
    (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14),  # Right
    (7, 14), (8, 14),  # Right middle
    (8, 13), (8, 12), (8, 11), (8, 10), (8, 9),  # Left
    (9, 8), (10, 8), (11, 8), (12, 8), (13, 8), (14, 8),  # Down
    (14, 7), (14, 6),  # Bottom middle
    (13, 6), (12, 6), (11, 6), (10, 6), (9, 6),  # Up
    (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0),  # Left
    (7, 0), (6, 0),  # Left middle - back to near start
]

# Starting positions on the main path for each player
START_POSITIONS = [0, 13, 26, 39]

# Home stretch paths for each player (6 cells leading to center)
HOME_STRETCH_PATHS = [
    [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)],  # Red
    [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)],  # Green
    [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8)],  # Yellow
    [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7)],  # Blue
]

# Safe positions on the board (starting positions are safe)
SAFE_POSITIONS = {0, 8, 13, 21, 26, 34, 39, 47}

# Home base positions for each player (where tokens start)
HOME_BASES = [
    [(1, 1), (1, 4), (4, 1), (4, 4)],  # Red
    [(1, 10), (1, 13), (4, 10), (4, 13)],  # Green
    [(10, 10), (10, 13), (13, 10), (13, 13)],  # Yellow
    [(10, 1), (10, 4), (13, 1), (13, 4)],  # Blue
]

# Center position (finish)
CENTER_POS = (7, 7)


class Token:
    """Represents a single game token."""

    def __init__(self, player_id: int, token_id: int):
        self.player_id = player_id
        self.token_id = token_id
        self.position = -1  # -1 = home base, 0-51 = main path, 52-57 = home stretch, 58 = finished
        self.is_finished = False

    @property
    def is_home(self) -> bool:
        return self.position == -1

    @property
    def on_main_path(self) -> bool:
        return 0 <= self.position <= 51

    @property
    def on_home_stretch(self) -> bool:
        return 52 <= self.position <= 57

    def get_board_position(self) -> Optional[Tuple[int, int]]:
        """Get the actual board (row, col) for this token's position."""
        if self.is_home:
            return HOME_BASES[self.player_id][self.token_id]
        if self.on_main_path:
            idx = (self.position + START_POSITIONS[self.player_id]) % 52
            return MAIN_PATH_CELLS[idx]
        if self.on_home_stretch:
            idx = self.position - 52
            if idx < len(HOME_STRETCH_PATHS[self.player_id]):
                return HOME_STRETCH_PATHS[self.player_id][idx]
        return None  # Finished


class LudoGame:
    """Core Ludo game logic."""

    def __init__(self):
        self.players = []
        self.tokens = {0: [], 1: [], 2: [], 3: []}
        self.current_player = 0
        self.dice_value = 1
        self.consecutive_sixes = 0
        self.game_over = False
        self.winner = -1
        self.scores = {0: 0, 1: 0, 2: 0, 3: 0}

        # Initialize tokens for each player
        for player_id in range(4):
            for token_id in range(4):
                self.tokens[player_id].append(Token(player_id, token_id))

    def roll_dice(self) -> int:
        """Roll the dice and return the value."""
        self.dice_value = random.randint(1, 6)
        if self.dice_value == 6:
            self.consecutive_sixes += 1
            if self.consecutive_sixes >= 3:
                # Three sixes in a row - lose turn
                self.consecutive_sixes = 0
                self.next_turn()
                return self.dice_value
        else:
            self.consecutive_sixes = 0
        return self.dice_value

    def get_movable_tokens(self, player_id: int, dice: int) -> List[int]:
        """Get list of token IDs that can be moved."""
        movable = []
        for token in self.tokens[player_id]:
            if token.is_finished:
                continue
            if token.is_home:
                if dice == 6:
                    movable.append(token.token_id)
            elif token.on_main_path:
                new_pos = token.position + dice
                if new_pos <= 57:
                    movable.append(token.token_id)
            elif token.on_home_stretch:
                new_pos = token.position + dice
                if new_pos <= 57:
                    movable.append(token.token_id)
        return movable

    def move_token(self, player_id: int, token_id: int, dice: int) -> bool:
        """Move a token and return True if a capture occurred."""
        token = self.tokens[player_id][token_id]
        captured = False

        if token.is_home and dice == 6:
            token.position = 0
        elif token.on_main_path or token.on_home_stretch:
            token.position += dice
            if token.position == 57:
                token.is_finished = True
                self.scores[player_id] += 100

        # Check for captures (only on main path)
        if token.on_main_path and not token.is_home:
            token_board_pos = token.get_board_position()
            main_path_idx = (token.position + START_POSITIONS[player_id]) % 52
            if main_path_idx not in SAFE_POSITIONS:
                for other_player_id in range(4):
                    if other_player_id == player_id:
                        continue
                    for other_token in self.tokens[other_player_id]:
                        if other_token.on_main_path and not other_token.is_home:
                            other_main_idx = (other_token.position + START_POSITIONS[other_player_id]) % 52
                            if other_main_idx == main_path_idx:
                                # Capture!
                                other_token.position = -1
                                captured = True
                                self.scores[player_id] += 50

        # Check for home stretch bonus
        if token.on_home_stretch:
            self.scores[player_id] += 10

        # Check if player has won (all tokens finished)
        if all(t.is_finished for t in self.tokens[player_id]):
            self.game_over = True
            self.winner = player_id
            self.scores[player_id] += 500  # Bonus for winning

        return captured

    def next_turn(self):
        """Advance to the next player's turn."""
        if self.game_over:
            return
        self.current_player = (self.current_player + 1) % 4
        self.consecutive_sixes = 0


class LudoBoard(ctk.CTkCanvas):
    """Custom canvas for drawing the Ludo board."""

    def __init__(self, parent, game: LudoGame):
        super().__init__(parent, width=700, height=700, bg="#1a1a2e", highlightthickness=0)
        self.game = game
        self.token_widgets = {}
        self.draw_board()

    def draw_board(self):
        """Draw the complete Ludo board."""
        self.delete("all")

        # Draw background
        self.create_rectangle(0, 0, 700, 700, fill="#1a1a2e", outline="")

        # Draw home bases
        self.draw_home_bases()

        # Draw main path
        self.draw_main_path()

        # Draw home stretches
        self.draw_home_stretches()

        # Draw center
        self.draw_center()

        # Draw tokens
        self.update_tokens()

    def draw_home_bases(self):
        """Draw the four home base squares."""
        base_configs = [
            (0, 0, PLAYER_COLORS[0], "Red"),
            (0, 9, PLAYER_COLORS[1], "Green"),
            (9, 9, PLAYER_COLORS[2], "Yellow"),
            (9, 0, PLAYER_COLORS[3], "Blue"),
        ]

        for row, col, color, name in base_configs:
            x = BOARD_OFFSET_X + col * CELL_SIZE
            y = BOARD_OFFSET_Y + row * CELL_SIZE
            size = 6 * CELL_SIZE

            # Main square
            self.create_rectangle(
                x, y, x + size, y + size,
                fill=color, outline="#ffffff", width=2
            )

            # Inner white square
            inner_margin = CELL_SIZE
            self.create_rectangle(
                x + inner_margin, y + inner_margin,
                x + size - inner_margin, y + size - inner_margin,
                fill="#f0f0f0", outline="#333333", width=1
            )

            # Label
            self.create_text(
                x + size // 2, y + size // 2,
                text=name, fill="#000000",
                font=("Arial", 14, "bold")
            )

    def draw_main_path(self):
        """Draw the main path cells."""
        for idx, (row, col) in enumerate(MAIN_PATH_CELLS):
            x = BOARD_OFFSET_X + col * CELL_SIZE
            y = BOARD_OFFSET_Y + row * CELL_SIZE

            # Determine cell color
            fill_color = "#e8e8e8"

            # Color the starting positions
            for player_id, start_idx in enumerate(START_POSITIONS):
                if idx == start_idx:
                    fill_color = PLAYER_COLORS[player_id]
                    break

            self.create_rectangle(
                x, y, x + CELL_SIZE, y + CELL_SIZE,
                fill=fill_color, outline="#666666", width=1
            )

    def draw_home_stretches(self):
        """Draw the home stretch paths."""
        for player_id, path in enumerate(HOME_STRETCH_PATHS):
            color = PLAYER_COLORS[player_id]
            for row, col in path:
                x = BOARD_OFFSET_X + col * CELL_SIZE
                y = BOARD_OFFSET_Y + row * CELL_SIZE
                self.create_rectangle(
                    x, y, x + CELL_SIZE, y + CELL_SIZE,
                    fill=color, outline="#ffffff", width=1
                )

    def draw_center(self):
        """Draw the center home triangle."""
        cx = BOARD_OFFSET_X + 7.5 * CELL_SIZE
        cy = BOARD_OFFSET_Y + 7.5 * CELL_SIZE

        # Draw triangles for each player
        triangles = [
            [(cx, cy), (BOARD_OFFSET_X + 6 * CELL_SIZE, BOARD_OFFSET_Y + 6 * CELL_SIZE),
             (BOARD_OFFSET_X + 6 * CELL_SIZE, BOARD_OFFSET_Y + 9 * CELL_SIZE)],  # Red
            [(cx, cy), (BOARD_OFFSET_X + 6 * CELL_SIZE, BOARD_OFFSET_Y + 6 * CELL_SIZE),
             (BOARD_OFFSET_X + 9 * CELL_SIZE, BOARD_OFFSET_Y + 6 * CELL_SIZE)],  # Green
            [(cx, cy), (BOARD_OFFSET_X + 9 * CELL_SIZE, BOARD_OFFSET_Y + 6 * CELL_SIZE),
             (BOARD_OFFSET_X + 9 * CELL_SIZE, BOARD_OFFSET_Y + 9 * CELL_SIZE)],  # Yellow
            [(cx, cy), (BOARD_OFFSET_X + 6 * CELL_SIZE, BOARD_OFFSET_Y + 9 * CELL_SIZE),
             (BOARD_OFFSET_X + 9 * CELL_SIZE, BOARD_OFFSET_Y + 9 * CELL_SIZE)],  # Blue
        ]

        for i, triangle in enumerate(triangles):
            self.create_polygon(
                triangle,
                fill=PLAYER_COLORS[i],
                outline="#ffffff",
                width=1
            )

        # Center circle
        self.create_oval(
            cx - 15, cy - 15, cx + 15, cy + 15,
            fill="#ffffff", outline="#333333", width=2
        )

        self.create_text(
            cx, cy,
            text="HOME",
            fill="#000000",
            font=("Arial", 8, "bold")
        )

    def update_tokens(self):
        """Update token positions on the board."""
        # Clear old token widgets
        for widget in self.token_widgets.values():
            widget.destroy()
        self.token_widgets.clear()

        # Draw tokens for each player
        for player_id in range(4):
            tokens_at_pos = {}

            for token in self.game.tokens[player_id]:
                pos = token.get_board_position()
                if pos is None:
                    continue

                row, col = pos
                if (row, col) not in tokens_at_pos:
                    tokens_at_pos[(row, col)] = []
                tokens_at_pos[(row, col)].append(token)

            for (row, col), tokens in tokens_at_pos.items():
                x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2

                offset_count = len(tokens)
                for i, token in enumerate(tokens):
                    if offset_count > 1:
                        offsets = [(-8, -8), (8, -8), (-8, 8), (8, 8)]
                        dx, dy = offsets[i]
                    else:
                        dx, dy = 0, 0

                    token_id = (player_id, token.token_id)
                    radius = 12 if offset_count <= 2 else 10

                    widget = self.create_oval(
                        x - radius + dx, y - radius + dy,
                        x + radius + dx, y + radius + dy,
                        fill=PLAYER_COLORS[player_id],
                        outline="#ffffff",
                        width=2
                    )

                    # Add token number
                    self.create_text(
                        x + dx, y + dy,
                        text=str(token.token_id + 1),
                        fill="#000000",
                        font=("Arial", 8, "bold")
                    )

                    self.token_widgets[token_id] = widget


class DiceWidget(ctk.CTkFrame):
    """Animated dice widget."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="#2a2a4a", corner_radius=15)
        self.dice_value = 1
        self.is_rolling = False

        self.canvas = ctk.CTkCanvas(
            self, width=DICE_SIZE, height=DICE_SIZE,
            bg="#2a2a4a", highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        self.draw_dice(1)

    def draw_dice(self, value: int):
        """Draw the dice with the given value."""
        self.canvas.delete("all")

        # Dice background
        self.canvas.create_rectangle(
            5, 5, DICE_SIZE - 5, DICE_SIZE - 5,
            fill="#ffffff", outline="#666666", width=2, radius=10
        )

        # Dot positions for each value
        dot_positions = {
            1: [(35, 35)],
            2: [(20, 20), (50, 50)],
            3: [(20, 20), (35, 35), (50, 50)],
            4: [(20, 20), (50, 20), (20, 50), (50, 50)],
            5: [(20, 20), (50, 20), (35, 35), (20, 50), (50, 50)],
            6: [(20, 18), (50, 18), (20, 35), (50, 35), (20, 52), (50, 52)],
        }

        for x, y in dot_positions.get(value, []):
            self.canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5,
                fill="#1a1a2e", outline=""
            )

    async def animate_roll(self) -> int:
        """Animate the dice rolling and return the final value."""
        self.is_rolling = True
        rolls = 10
        delay = 50

        for _ in range(rolls):
            temp_value = random.randint(1, 6)
            self.draw_dice(temp_value)
            self.update()
            await self._async_sleep(delay / 1000)
            delay += 20

        self.is_rolling = False
        return self.dice_value

    def _async_sleep(self, seconds: float):
        """Simple async sleep using after."""
        import asyncio
        loop = asyncio.new_event_loop()
        loop.run_until_complete(asyncio.sleep(seconds))
        loop.close()


class LudoApp(ctk.CTk):
    """Main Ludo game application."""

    def __init__(self):
        super().__init__()

        self.title("Ludo Game")
        self.geometry("1100x750")
        self.resizable(False, False)

        self.game = LudoGame()
        self.is_player_turn = True
        self.is_ai_game = True  # AI controls players 1-3

        self.setup_ui()
        self.update_status()

    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=0)
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            main_frame, text="LUDO",
            font=("Arial", 32, "bold"),
            text_color="#ffffff"
        )
        title_label.place(x=350, y=15)

        # Game board
        self.board = LudoBoard(main_frame, self.game)
        self.board.place(x=20, y=60)

        # Control panel
        control_frame = ctk.CTkFrame(main_frame, width=320, height=650, fg_color="#1a1a2e", corner_radius=15)
        control_frame.place(x=750, y=20)

        # Dice section
        dice_label = ctk.CTkLabel(
            control_frame, text="DICE",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        dice_label.place(x=130, y=15)

        self.dice_widget = DiceWidget(control_frame)
        self.dice_widget.place(x=115, y=55)

        # Roll button
        self.roll_button = ctk.CTkButton(
            control_frame, text="ROLL DICE",
            font=("Arial", 16, "bold"),
            fg_color="#e94560", hover_color="#c73e54",
            width=200, height=45,
            corner_radius=10,
            command=self.roll_dice_clicked
        )
        self.roll_button.place(x=60, y=155)

        # Current player indicator
        self.player_frame = ctk.CTkFrame(control_frame, fg_color="#2a2a4a", corner_radius=10)
        self.player_frame.place(x=20, y=220, width=280, height=80)

        self.player_label = ctk.CTkLabel(
            self.player_frame, text="Current Player:",
            font=("Arial", 14),
            text_color="#aaaaaa"
        )
        self.player_label.place(x=70, y=10)

        self.current_player_label = ctk.CTkLabel(
            self.player_frame, text="Red",
            font=("Arial", 24, "bold"),
            text_color=PLAYER_COLORS[0]
        )
        self.current_player_label.place(x=120, y=35)

        # Scores section
        scores_label = ctk.CTkLabel(
            control_frame, text="SCORES",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        scores_label.place(x=120, y=320)

        self.score_frames = {}
        for i in range(4):
            frame = ctk.CTkFrame(control_frame, fg_color="#2a2a4a", corner_radius=8)
            frame.place(x=20, y=360 + i * 65, width=280, height=55)

            color_indicator = ctk.CTkLabel(
                frame, text="",
                width=15, height=40,
                fg_color=PLAYER_COLORS[i],
                corner_radius=5
            )
            color_indicator.place(x=15, y=7)

            name_label = ctk.CTkLabel(
                frame, text=PLAYER_NAMES[i],
                font=("Arial", 14, "bold"),
                text_color="#ffffff",
                anchor="w"
            )
            name_label.place(x=45, y=5)

            score_label = ctk.CTkLabel(
                frame, text="Tokens: 0/4",
                font=("Arial", 12),
                text_color="#aaaaaa",
                anchor="w"
            )
            score_label.place(x=45, y=28)

            self.score_frames[i] = {"frame": frame, "score_label": score_label}

        # Status label
        self.status_label = ctk.CTkLabel(
            control_frame, text="Click 'ROLL DICE' to start",
            font=("Arial", 12),
            text_color="#888888",
            wraplength=280
        )
        self.status_label.place(x=20, y=620, width=280)

        # New game button
        new_game_button = ctk.CTkButton(
            control_frame, text="NEW GAME",
            font=("Arial", 14, "bold"),
            fg_color="#4a4a6a", hover_color="#5a5a7a",
            width=150, height=35,
            corner_radius=8,
            command=self.new_game
        )
        new_game_button.place(x=85, y=580)

    def update_status(self):
        """Update the status display."""
        player_id = self.game.current_player
        color = PLAYER_COLORS[player_id]
        name = PLAYER_NAMES[player_id]

        self.current_player_label.configure(text=name, text_color=color)

        # Update scores
        for i in range(4):
            finished = sum(1 for t in self.game.tokens[i] if t.is_finished)
            self.score_frames[i]["score_label"].configure(
                text=f"Tokens: {finished}/4 | Score: {self.game.scores[i]}"
            )

        # Update player frame color
        self.player_frame.configure(fg_color=self._darken_color(color, 0.3))

    def _darken_color(self, color: str, factor: float) -> str:
        """Darken a hex color by the given factor."""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    def roll_dice_clicked(self):
        """Handle roll dice button click."""
        if not self.is_player_turn or self.game.game_over:
            return

        self.roll_dice_and_play()

    def roll_dice_and_play(self):
        """Roll dice and process the turn."""
        self.roll_button.configure(state="disabled")

        # Simple dice roll (no animation for simplicity)
        dice = self.game.roll_dice()
        self.dice_widget.dice_value = dice
        self.dice_widget.draw_dice(dice)

        player_id = self.game.current_player
        movable = self.game.get_movable_tokens(player_id, dice)

        if not movable:
            self.status_label.configure(text=f"{PLAYER_NAMES[player_id]} rolled {dice}. No moves available!")
            self.after(1500, lambda: self.end_turn(False))
        elif len(movable) == 1:
            # Auto-move if only one option
            self.move_token_and_continue(player_id, movable[0], dice)
        else:
            # Player needs to choose
            if player_id == 0:  # Human player
                self.status_label.configure(text=f"Rolled {dice}! Click a token to move.")
                self.enable_token_selection(player_id, movable, dice)
            else:
                # AI chooses
                token_id = self.ai_choose_token(player_id, movable, dice)
                self.move_token_and_continue(player_id, token_id, dice)

    def move_token_and_continue(self, player_id: int, token_id: int, dice: int):
        """Move a token and continue the game."""
        captured = self.game.move_token(player_id, token_id, dice)

        token = self.game.tokens[player_id][token_id]
        pos_text = "Home" if token.is_home else f"Position {token.position}"
        if token.is_finished:
            pos_text = "Finished!"

        msg = f"{PLAYER_NAMES[player_id]} moved token {token_id + 1} to {pos_text}"
        if captured:
            msg += " - CAPTURED!"
        self.status_label.configure(text=msg)

        self.board.update_tokens()
        self.update_status()

        # Check for extra turn (rolled 6 or captured)
        if dice == 6 or captured:
            if not self.game.game_over:
                self.status_label.configure(text=msg + " - Extra turn!")
                self.after(1500, lambda: self.start_turn())
        else:
            self.after(1500, lambda: self.end_turn(False))

    def enable_token_selection(self, player_id: int, movable: List[int], dice: int):
        """Enable token selection for human player."""
        self.selecting_tokens = True
        self.selectable_tokens = movable
        self.select_dice = dice

        # Highlight selectable tokens on board
        self.board.bind("<Button-1>", self.on_board_click)

    def on_board_click(self, event):
        """Handle click on the board for token selection."""
        if not hasattr(self, 'selecting_tokens') or not self.selecting_tokens:
            return

        # Find which token was clicked
        x = event.x
        y = event.y

        for token_id in self.selectable_tokens:
            token = self.game.tokens[0][token_id]
            pos = token.get_board_position()
            if pos is None:
                continue

            row, col = pos
            tx = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
            ty = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2

            if abs(x - tx) < 20 and abs(y - ty) < 20:
                self.board.unbind("<Button-1>")
                self.selecting_tokens = False
                self.move_token_and_continue(0, token_id, self.select_dice)
                return

    def ai_choose_token(self, player_id: int, movable: List[int], dice: int) -> int:
        """AI logic to choose which token to move."""
        # Priority:
        # 1. Move token out of home (if rolled 6)
        # 2. Capture opponent if possible
        # 3. Move token closest to home stretch
        # 4. Move token that is furthest along

        # Check if can move out of home
        if dice == 6:
            home_tokens = [t for t in movable if self.game.tokens[player_id][t].is_home]
            if home_tokens:
                return home_tokens[0]

        # Check for captures
        best_capture = None
        for token_id in movable:
            token = self.game.tokens[player_id][token_id]
            if token.on_main_path:
                new_main_idx = (token.position + dice + self.game.START_POSITIONS[player_id]) % 52
                for other_id in range(4):
                    if other_id == player_id:
                        continue
                    for other_token in self.game.tokens[other_id]:
                        if other_token.on_main_path:
                            other_idx = (other_token.position + self.game.START_POSITIONS[other_id]) % 52
                            if new_main_idx == other_idx and new_main_idx not in SAFE_POSITIONS:
                                best_capture = token_id
                                break
                    if best_capture is not None:
                        break
            if best_capture is not None:
                break

        if best_capture is not None:
            return best_capture

        # Move the token furthest along (closest to finishing)
        return max(movable, key=lambda t: self.game.tokens[player_id][t].position)

    def start_turn(self):
        """Start a new turn."""
        self.roll_button.configure(state="normal")

        player_id = self.game.current_player
        self.is_player_turn = (player_id == 0)

        if self.game.game_over:
            self.handle_game_over()
            return

        if not self.is_player_turn and self.is_ai_game:
            # AI turn
            self.roll_button.configure(state="disabled")
            self.status_label.configure(text=f"{PLAYER_NAMES[player_id]} is thinking...")
            self.after(1000, self.roll_dice_and_play)
        else:
            self.status_label.configure(text=f"{PLAYER_NAMES[player_id]}'s turn - Roll the dice!")

    def end_turn(self, extra_turn: bool):
        """End the current turn."""
        if self.game.game_over:
            self.handle_game_over()
            return

        if not extra_turn:
            self.game.next_turn()

        self.start_turn()

    def handle_game_over(self):
        """Handle game completion."""
        winner = self.game.winner
        self.status_label.configure(
            text=f"GAME OVER! {PLAYER_NAMES[winner]} wins!",
            text_color=PLAYER_COLORS[winner]
        )
        self.roll_button.configure(state="disabled")

    def new_game(self):
        """Start a new game."""
        self.game = LudoGame()
        self.board = LudoBoard(self, self.game)
        self.board.place(x=20, y=60)
        self.dice_widget.draw_dice(1)
        self.is_player_turn = True
        self.board.unbind("<Button-1>")
        if hasattr(self, 'selecting_tokens'):
            self.selecting_tokens = False
        self.update_status()
        self.status_label.configure(text="New game! Click 'ROLL DICE' to start.", text_color="#888888")
        self.roll_button.configure(state="normal")


def main():
    """Main entry point."""
    app = LudoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
