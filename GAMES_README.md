# 🎮 Python Games Collection

A complete suite of 10 classic games with modern, beautiful GUIs built using Python and CustomTkinter!

## 🚀 Quick Start

### Launch the Games Menu
```bash
python main_menu.py
```

This will open a beautiful launcher where you can access all 10 games!

### Or Launch Games Directly
```bash
python game_hangman.py       # Word guessing game
python game_tictactoe.py     # Classic strategy game
python game_snake.py         # Arcade snake game
python game_pong.py          # Classic pong
python game_blackjack.py     # Card game
python game_sudoku.py        # Puzzle solver
python game_memory.py        # Memory card game
python game_tetris.py        # Block stacking
python game_ludo.py          # Board game
python game_tank_flight.py   # Flappy bird style
```

## 🎯 Games Collection

### 1. 🎯 Hangman
**Category:** Word Game  
**Description:** Classic word guessing game where you try to guess the word letter by letter before the hangman figure is complete.

**Features:**
- 35+ words across different categories
- Beautiful ASCII hangman art that builds as you play
- Letter buttons with color coding (green=correct, red=wrong)
- Score tracking and win/lose states
- Clean, modern interface

**How to Play:**
1. Click "New Game" to start
2. Click letter buttons to guess
3. Try to guess the word before 6 wrong guesses!

**Controls:** Click letters or use on-screen buttons

---

### 2. ⭕ Tic-Tac-Toe
**Category:** Strategy  
**Description:** The classic two-player strategy game where you try to get 3 in a row!

**Features:**
- **Two Game Modes:** Player vs Player OR Player vs AI
- Smart AI opponent using minimax algorithm
- Beautiful X (❌) and O (⭕) symbols
- Score tracking for both players and draws
- Color-coded player indicators

**How to Play:**
1. Select game mode (PvP or PvAI)
2. Click any cell to place your mark
3. Get 3 in a row to win!

**Controls:** Mouse click to place marks

---

### 3. 🐍 Snake
**Category:** Arcade  
**Description:** The iconic arcade game where you control a snake that grows longer as it eats food. Don't hit the walls or yourself!

**Features:**
- Smooth, responsive controls
- Score and high score tracking
- Adjustable game speed (Normal/Fast)
- Beautiful snake with gradient body
- Red food balls with glow effect
- Subtle grid background

**How to Play:**
1. Press SPACE or arrow keys to start
2. Use arrow keys to change direction
3. Eat food to grow and score points
4. Avoid walls and yourself!

**Controls:** Arrow keys to move, SPACE to start

---

### 4. 🏓 Pong
**Category:** Arcade  
**Description:** The original arcade game that started it all! Battle against AI or a friend in this classic paddle game.

**Features:**
- **Two Modes:** Player vs AI or Player vs Player
- Smooth 60 FPS gameplay
- AI opponent with intelligent tracking
- Mouse and keyboard controls
- Ball speed increases during rallies
- Score tracking

**How to Play:**
1. Select game mode
2. Move mouse or use A/D keys to control paddle
3. Bounce the ball past opponent's paddle to score!

**Controls:** Mouse movement or A/D keys, SPACE to pause

---

### 5. 🃏 Blackjack
**Category:** Card Game  
**Description:** The classic casino card game! Beat the dealer by getting closest to 21 without going over.

**Features:**
- Full Blackjack rules (Hit, Stand, Double Down)
- Chip betting system with quick-bet buttons
- Beautiful card display with Unicode suits
- Win/Loss/Push tracking
- Auto-recovery when out of chips
- Smooth dealing animations

**How to Play:**
1. Place your bet using chip buttons
2. Click "Deal" to start
3. Choose Hit, Stand, or Double Down
4. Beat the dealer without going over 21!

**Controls:** Mouse click for all actions

---

### 6. 🔢 Sudoku Solver
**Category:** Puzzle  
**Description:** Solve existing Sudoku puzzles or generate new ones with this elegant solver.

**Features:**
- Input your own puzzles to solve
- Random puzzle generation
- Fast backtracking algorithm
- Clean 9x9 grid with 3x3 box separators
- Input validation (1-9 only)
- Clear and Solve buttons

**How to Play:**
1. Enter numbers in the grid (or generate)
2. Click "Solve" to see the solution
3. Click "Generate Puzzle" for a new challenge!

**Controls:** Click cells to enter numbers

---

### 7. 🧠 Memory Puzzle
**Category:** Puzzle  
**Description:** Test your memory by flipping cards and finding matching pairs!

**Features:**
- 5 different emoji themes (animals, fruits, vehicles, etc.)
- Move counter and pair tracker
- Timer to challenge yourself
- Beautiful card flip animations
- Color-coded matched pairs
- Theme switching

**How to Play:**
1. Click "New Game" to start
2. Click cards to flip them
3. Find all matching pairs with fewest moves!

**Controls:** Mouse click to flip cards

---

### 8. 🟦 Tetris
**Category:** Arcade  
**Description:** The iconic block-stacking puzzle game! Clear lines and score points as blocks fall faster.

**Features:**
- All 7 classic Tetrominoes (I, O, T, S, Z, J, L)
- Ghost piece showing landing position
- Next piece preview
- Increasing difficulty with levels
- Line clearing with combo scoring
- Wall kick rotation system
- 3D cell effects

**How to Play:**
1. Click "Start" to begin
2. Arrow keys to move/rotate
3. Down for soft drop, Space for hard drop
4. Clear lines to score points!

**Controls:** ← → to move, ↑ to rotate, ↓ soft drop, Space hard drop, P pause

---

### 9. 🎲 Ludo
**Category:** Board Game  
**Description:** The beloved classic board game! Race your tokens around the board and be first to get all 4 home!

**Features:**
- 4-player gameplay (You vs 3 AI)
- Beautiful cross-shaped board
- Dice rolling animations
- Token capture mechanics
- Safe positions
- Home stretch paths
- Score tracking

**How to Play:**
1. Click "Roll Dice" to start your turn
2. Roll a 6 to exit home base
3. Click tokens to move them
4. Capture opponents and race to finish!

**Controls:** Mouse click to roll dice and move tokens

---

### 10. 🚀 Tank Flight
**Category:** Arcade  
**Description:** Flappy Bird reimagined with a flying tank! Navigate through obstacles and beat your high score.

**Features:**
- Cute flying tank with exhaust particles
- Gravity physics with smooth animations
- Obstacles with increasing difficulty
- High score persistence
- Starfield background
- Game over celebration screen

**How to Play:**
1. Press SPACE or click to start
2. Press SPACE/click to make tank jump
3. Fly through gaps in obstacles
4. See how far you can go!

**Controls:** SPACE or mouse click to jump

---

## 📋 Requirements

- Python 3.7 or higher
- customtkinter
- requests (for some games)
- Pillow (for image handling)

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🎨 Features

### Common Across All Games
✅ Modern dark theme UI  
✅ Beautiful color schemes  
✅ Responsive layouts  
✅ Intuitive controls  
✅ Score tracking  
✅ Win/lose states  
✅ Restart functionality  
✅ Smooth animations  

### Variety of Genres
- **Word Games:** Hangman
- **Strategy:** Tic-Tac-Toe, Sudoku
- **Arcade:** Snake, Pong, Tetris, Tank Flight
- **Card Games:** Blackjack
- **Puzzle:** Memory Puzzle
- **Board Games:** Ludo

## 🎯 Controls Summary

| Game | Primary Controls |
|------|-----------------|
| Hangman | Mouse click on letter buttons |
| Tic-Tac-Toe | Mouse click on cells |
| Snake | Arrow keys, SPACE to start |
| Pong | Mouse/A-D keys, SPACE to pause |
| Blackjack | Mouse click on action buttons |
| Sudoku | Mouse click to enter numbers |
| Memory | Mouse click to flip cards |
| Tetris | Arrow keys, SPACE for hard drop |
| Ludo | Mouse click to roll/move |
| Tank Flight | SPACE or mouse click to jump |

## 🏆 Tips & Tricks

### Hangman
- Start with common letters: E, A, R, I, O, N
- Look for word patterns and common suffixes

### Tic-Tac-Toe
- Center is the most powerful position
- Corners are second best
- Play defensively against AI

### Snake
- Plan your route ahead
- Don't trap yourself in corners
- Use the full board space

### Pong
- Anticipate ball trajectory
- Don't overcommit to one side
- AI adapts to ball speed

### Blackjack
- Stand on 17 or higher
- Hit on 11 or lower
- Double down on 10 or 11 when dealer shows low card

### Tetris
- Keep your stack low and flat
- Save I-piece for Tetris (4 lines)
- Use ghost piece to plan placement

### Tank Flight
- Tap lightly, don't hold
- Watch for pattern in obstacles
- Practice makes perfect!

## 🐛 Troubleshooting

**Games won't launch:**
```bash
pip install -r requirements.txt
```

**Slow performance:**
- Close other applications
- Reduce screen resolution if needed

**Import errors:**
- Ensure customtkinter is installed
- Try: `pip install --upgrade customtkinter`

**Key bindings not working:**
- Click on game window to focus
- Some games require window to be active

## 📁 File Structure

```
python-project/
│
├── main_menu.py              # 🎮 Games Launcher (START HERE!)
│
├── game_hangman.py           # 🎯 Hangman
├── game_tictactoe.py         # ⭕ Tic-Tac-Toe
├── game_snake.py             # 🐍 Snake
├── game_pong.py              # 🏓 Pong
├── game_blackjack.py         # 🃏 Blackjack
├── game_sudoku.py            # 🔢 Sudoku Solver
├── game_memory.py            # 🧠 Memory Puzzle
├── game_tetris.py            # 🟦 Tetris
├── game_ludo.py              # 🎲 Ludo
├── game_tank_flight.py       # 🚀 Tank Flight
│
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## 🎓 Learning Resources

These games are great examples for learning:
- **GUI Programming:** CustomTkinter widgets
- **Game Loops:** Real-time updates and rendering
- **Event Handling:** Keyboard and mouse input
- **Algorithms:** AI, pathfinding, backtracking
- **Physics:** Gravity, collision detection
- **State Management:** Game states and transitions

## 🔄 Future Enhancements

- [ ] Online multiplayer support
- [ ] Leaderboards
- [ ] Achievements system
- [ ] More game themes
- [ ] Sound effects
- [ ] Save game states
- [ ] Mobile touch support

## 📝 License

This games collection is open source and available for educational purposes.

## 🙏 Credits

- **UI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Game Logic:** Custom implementations
- **Design:** Modern dark theme with beautiful colors

## 🤝 Contributing

Feel free to add your own games to this collection! Follow the same structure and add them to the main menu launcher.

---

**Have Fun Playing! 🎮🎉**

Made with ❤️ using Python and CustomTkinter

*Start with: `python main_menu.py`*
