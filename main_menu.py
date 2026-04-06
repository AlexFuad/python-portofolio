"""
Main Menu Launcher - Games & Applications
A modern, user-friendly menu to launch all Python projects
"""

import customtkinter as ctk  # type: ignore
import subprocess
import threading
import sys
import os


# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainMenuApp(ctk.CTk):
    """Main Menu Launcher Application"""
    
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("🚀 Python Projects Launcher")
        self.geometry("1300x850")
        self.resizable(True, True)
        self.minsize(1100, 750)
        
        # Store running processes
        self.running_processes = {}
        
        # Setup UI
        self.setup_ui()
        
        # Check available projects
        self.check_projects()
        
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
            text="🚀 Python Projects Collection",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="🎮 10 Games  •  🛠️ 3 Applications  •  Endless Fun!",
            font=ctk.CTkFont(size=18),
            text_color="gray"
        )
        self.subtitle_label.pack()
        
        # ========== TABS ==========
        self.tabs_frame = ctk.CTkFrame(self.main_frame)
        self.tabs_frame.pack(fill="x", pady=(0, 15))
        
        self.games_tab_btn = ctk.CTkButton(
            self.tabs_frame,
            text="🎮 Games (10)",
            command=lambda: self.show_tab("games"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color="#3498DB",
            hover_color="#2980B9"
        )
        self.games_tab_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.apps_tab_btn = ctk.CTkButton(
            self.tabs_frame,
            text="🛠️ Applications (3)",
            command=lambda: self.show_tab("apps"),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color="#27AE60",
            hover_color="#229954"
        )
        self.apps_tab_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        # ========== PROJECTS CONTAINER ==========
        self.projects_container = ctk.CTkScrollableFrame(self.main_frame, corner_radius=10)
        self.projects_container.pack(fill="both", expand=True, pady=(0, 15))
        
        # Project cards
        self.project_cards = {}
        self.current_tab = "games"
        
        # Add info label
        ctk.CTkLabel(
            self.main_frame,
            text="💡 Tip: Click '🚀 Launch' to open any game or application",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=(0, 5))
        
        # ========== STATUS PANEL ==========
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            self.status_frame,
            text="📊 Running Applications",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)
        
        self.status_scroll = ctk.CTkScrollableFrame(
            self.status_frame,
            corner_radius=10,
            height=100
        )
        self.status_scroll.pack(fill="x", padx=10, pady=5)
        
        self.status_placeholder = ctk.CTkLabel(
            self.status_scroll,
            text="No applications running",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.status_placeholder.pack(pady=15)
        
    def check_projects(self):
        """Check which projects are available"""
        self.projects = []
        
        # ===== GAMES =====
        games_config = [
            {
                "id": "hangman", "name": "Hangman", "icon": "🎯",
                "description": "Guess the word letter by letter!",
                "file": "game_hangman.py",
                "color": "#E74C3C", "hover_color": "#C0392B",
                "category": "Word Game", "type": "game"
            },
            {
                "id": "tictactoe", "name": "Tic-Tac-Toe", "icon": "⭕",
                "description": "Classic strategy game - get 3 in a row!",
                "file": "game_tictactoe.py",
                "color": "#3498DB", "hover_color": "#2980B9",
                "category": "Strategy", "type": "game"
            },
            {
                "id": "snake", "name": "Snake", "icon": "🐍",
                "description": "Eat food, grow longer, don't crash!",
                "file": "game_snake.py",
                "color": "#27AE60", "hover_color": "#229954",
                "category": "Arcade", "type": "game"
            },
            {
                "id": "pong", "name": "Pong", "icon": "🏓",
                "description": "Original arcade game - battle AI or friend!",
                "file": "game_pong.py",
                "color": "#F39C12", "hover_color": "#E67E22",
                "category": "Arcade", "type": "game"
            },
            {
                "id": "blackjack", "name": "Blackjack", "icon": "🃏",
                "description": "Beat the dealer! Get closest to 21!",
                "file": "game_blackjack.py",
                "color": "#8E44AD", "hover_color": "#7D3C98",
                "category": "Card Game", "type": "game"
            },
            {
                "id": "sudoku", "name": "Sudoku Solver", "icon": "🔢",
                "description": "Solve or generate Sudoku puzzles!",
                "file": "game_sudoku.py",
                "color": "#16A085", "hover_color": "#138D75",
                "category": "Puzzle", "type": "game"
            },
            {
                "id": "memory", "name": "Memory Puzzle", "icon": "🧠",
                "description": "Flip cards and match pairs!",
                "file": "game_memory.py",
                "color": "#D35400", "hover_color": "#BA4A00",
                "category": "Puzzle", "type": "game"
            },
            {
                "id": "tetris", "name": "Tetris", "icon": "🟦",
                "description": "Iconic block-stacking game!",
                "file": "game_tetris.py",
                "color": "#2980B9", "hover_color": "#2471A3",
                "category": "Arcade", "type": "game"
            },
            {
                "id": "ludo", "name": "Ludo", "icon": "🎲",
                "description": "Classic board game - race to home!",
                "file": "game_ludo.py",
                "color": "#C0392B", "hover_color": "#A93226",
                "category": "Board Game", "type": "game"
            },
            {
                "id": "tank", "name": "Tank Flight", "icon": "🚀",
                "description": "Fly through obstacles - Flappy Bird style!",
                "file": "game_tank_flight.py",
                "color": "#2C3E50", "hover_color": "#1C2833",
                "category": "Arcade", "type": "game"
            }
        ]
        
        # ===== APPLICATIONS =====
        apps_config = [
            {
                "id": "calculator", "name": "Calculator", "icon": "🧮",
                "description": "Modern calculator for everyday calculations",
                "file": "Calculator.py",
                "color": "#27AE60", "hover_color": "#229954",
                "category": "Utility", "type": "app"
            },
            {
                "id": "weather", "name": "Weather Checker", "icon": "🌤️",
                "description": "Real-time weather for any city worldwide",
                "file": "weather_checker.py",
                "color": "#3498DB", "hover_color": "#2980B9",
                "category": "Utility", "type": "app"
            },
            {
                "id": "recipe", "name": "Recipe Finder", "icon": "🍳",
                "description": "Discover delicious recipes from around the world",
                "file": "recipe_finder.py",
                "color": "#E67E22", "hover_color": "#D35400",
                "category": "Utility", "type": "app"
            }
        ]
        
        # Add games if files exist
        for project in games_config:
            if os.path.exists(project["file"]):
                self.projects.append(project)
        
        # Add applications if files exist
        for project in apps_config:
            if os.path.exists(project["file"]):
                self.projects.append(project)
        
        # Show games tab by default
        self.show_tab("games")
        
    def show_tab(self, tab):
        """Show games or apps tab"""
        self.current_tab = tab
        
        # Update tab buttons
        if tab == "games":
            self.games_tab_btn.configure(fg_color="#3498DB")
            self.apps_tab_btn.configure(fg_color="#7F8C8D")
        else:
            self.games_tab_btn.configure(fg_color="#7F8C8D")
            self.apps_tab_btn.configure(fg_color="#27AE60")
        
        # Clear container
        for widget in self.projects_container.winfo_children():
            widget.destroy()
        self.project_cards = {}
        
        # Filter projects
        filtered = [p for p in self.projects if p["type"] == tab]
        
        if not filtered:
            ctk.CTkLabel(
                self.projects_container,
                text=f"⚠️ No {tab} found",
                font=ctk.CTkFont(size=18),
                text_color="#E74C3C"
            ).pack(expand=True, pady=40)
            return
        
        # Create grid
        cols = 3
        rows = (len(filtered) + cols - 1) // cols
        
        for idx, project in enumerate(filtered):
            row = idx // cols
            col = idx % cols
            
            self.projects_container.grid_rowconfigure(row, weight=1)
            self.projects_container.grid_columnconfigure(col, weight=1)
            
            card = self.create_project_card(project)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        
    def create_project_card(self, project):
        """Create a card widget for a project"""
        card = ctk.CTkFrame(
            self.projects_container,
            corner_radius=15,
            border_width=2,
            border_color=project["color"]
        )
        
        # Inner container
        inner_frame = ctk.CTkFrame(card, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Category badge
        type_icon = "🎮" if project["type"] == "game" else "🛠️"
        category_badge = ctk.CTkLabel(
            inner_frame,
            text=f"{type_icon} {project['category']}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=project["color"],
            corner_radius=8
        )
        category_badge.pack(anchor="w", pady=(0, 5))
        
        # Icon
        ctk.CTkLabel(
            inner_frame,
            text=project["icon"],
            font=ctk.CTkFont(size=50)
        ).pack(pady=5)
        
        # Name
        ctk.CTkLabel(
            inner_frame,
            text=project["name"],
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=5)
        
        # Description
        ctk.CTkLabel(
            inner_frame,
            text=project["description"],
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=250
        ).pack(pady=(0, 10))
        
        # Launch button
        launch_btn = ctk.CTkButton(
            inner_frame,
            text="🚀 Launch",
            command=lambda p=project: self.launch_project(p),
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color=project["color"],
            hover_color=project["hover_color"]
        )
        launch_btn.pack(fill="x", pady=5)
        
        # Store reference
        self.project_cards[project["id"]] = {
            "card": card,
            "project": project,
            "launch_btn": launch_btn
        }
        
        return card
        
    def launch_project(self, project):
        """Launch a selected project"""
        project_id = project["id"]
        project_name = project["name"]
        
        # Check if already running
        if project_id in self.running_processes:
            process_info = self.running_processes[project_id]
            if process_info["process"].poll() is None:
                self.show_notification(f"⚠️ {project_name} is already running!", "#F39C12")
                return
        
        # Update UI
        card_data = self.project_cards.get(project_id)
        if card_data:
            card_data["launch_btn"].configure(
                text="⏳ Launching...",
                state="disabled"
            )
        
        # Launch in background thread
        thread = threading.Thread(
            target=self._launch_project_thread,
            args=(project,)
        )
        thread.daemon = True
        thread.start()
        
    def _launch_project_thread(self, project):
        """Launch project in background thread"""
        try:
            import platform
            
            # Get absolute path to the file
            file_path = os.path.abspath(project["file"])
            
            # Different launch method for Windows
            if platform.system() == "Windows":
                # Use startfile for Windows - opens in new window
                os.startfile(file_path)
            else:
                # Use subprocess for other OS
                subprocess.Popen(
                    [sys.executable, file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            game_id = project["id"]
            self.running_processes[game_id] = {
                "process": None,  # os.startfile doesn't return process
                "name": project["name"]
            }
            
            self.after(0, lambda: self.on_project_launched(project))
            
        except Exception as e:
            self.after(0, lambda: self.on_launch_error(project, str(e)))
            
    def on_project_launched(self, project):
        """Handle successful project launch"""
        project_id = project["id"]
        
        card_data = self.project_cards.get(project_id)
        if card_data:
            card_data["launch_btn"].configure(
                text="✅ Running",
                state="normal",
                fg_color="#27AE60",
                hover_color="#229954"
            )
        
        self.update_status_panel()
        
    def on_launch_error(self, project, error_message):
        """Handle launch error"""
        project_id = project["id"]
        
        card_data = self.project_cards.get(project_id)
        if card_data:
            card_data["launch_btn"].configure(
                text="🚀 Launch",
                state="normal",
                fg_color=project["color"],
                hover_color=project["hover_color"]
            )
        
        self.show_notification(f"❌ Failed to launch: {error_message}", "#E74C3C")
        
    def show_notification(self, message, color):
        """Show notification"""
        notif = ctk.CTkToplevel(self)
        notif.title("Notification")
        notif.geometry("400x100")
        notif.resizable(False, False)
        
        ctk.CTkLabel(
            notif,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color=color,
            wraplength=350
        ).pack(expand=True, padx=20, pady=20)
        
        notif.after(3000, notif.destroy)
        
    def update_status_panel(self):
        """Update the status panel"""
        for widget in self.status_scroll.winfo_children():
            widget.destroy()
        
        if not self.running_processes:
            self.status_placeholder = ctk.CTkLabel(
                self.status_scroll,
                text="No applications running",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            self.status_placeholder.pack(pady=15)
            return
        
        # Show all running projects
        for project_id, process_info in self.running_processes.items():
            status_frame = ctk.CTkFrame(self.status_scroll, fg_color="transparent")
            status_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                status_frame,
                text=f"✅ {process_info['name']}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#27AE60"
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                status_frame,
                text="Running (check taskbar)",
                font=ctk.CTkFont(size=11),
                text_color="#3498DB"
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                status_frame,
                text="⏹ Close",
                command=lambda pid=project_id: self.close_project(pid),
                font=ctk.CTkFont(size=11),
                height=25,
                width=60,
                corner_radius=5,
                fg_color="#E74C3C",
                hover_color="#C0392B"
            ).pack(side="right", padx=5)
            
    def close_project(self, project_id):
        """Remove a project from tracking (user should close it manually)"""
        if project_id in self.running_processes:
            del self.running_processes[project_id]
            
            # Reset launch button
            for project in self.projects:
                if project["id"] == project_id:
                    card_data = self.project_cards.get(project_id)
                    if card_data:
                        card_data["launch_btn"].configure(
                            text="🚀 Launch",
                            state="normal",
                            fg_color=project["color"],
                            hover_color=project["hover_color"]
                        )
                    break
            
            self.update_status_panel()
            self.show_notification("ℹ️ Please close the application window manually", "#3498DB")


if __name__ == "__main__":
    app = MainMenuApp()
    app.mainloop()
