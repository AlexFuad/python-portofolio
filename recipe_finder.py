"""
Recipe Finder Application
A modern, user-friendly recipe searching app using TheMealDB API
"""

import customtkinter as ctk
import requests
import json
import re
import threading
import webbrowser
from PIL import Image, ImageTk
import io
import urllib.request


# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class RecipeFinderApp(ctk.CTk):
    """Main Recipe Finder Application Class"""
    
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("🍳 Recipe Finder")
        self.geometry("1100x750")
        self.resizable(True, True)
        self.minsize(900, 650)
        
        # API Configuration (TheMealDB - Free, no API key needed!)
        self.BASE_URL = "https://www.themealdb.com/api/json/v1/1"
        
        # Recipe data cache
        self.current_recipes = []
        self.selected_recipe = None
        
        # Category mapping
        self.categories = [
            "Beef", "Chicken", "Dessert", "Lamb", "Misc",
            "Pasta", "Pork", "Seafood", "Side", "Starter", "Vegan", "Vegetarian", "Breakfast", "Goat"
        ]
        
        self.cuisines = [
            "American", "British", "Canadian", "Chinese", "Croatian",
            "Dutch", "Egyptian", "French", "Greek", "Indian", "Irish",
            "Italian", "Jamaican", "Japanese", "Kenyan", "Malaysian",
            "Mexican", "Moroccan", "Polish", "Portuguese", "Russian",
            "Spanish", "Thai", "Tunisian", "Turkish", "Unknown", "Vietnamese"
        ]
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the User Interface"""
        
        # Main container with padding
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # ========== HEADER SECTION ==========
        self.header_frame = ctk.CTkFrame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 15))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🍳 Recipe Finder",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Discover delicious recipes from around the world",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.subtitle_label.pack()
        
        # ========== SEARCH SECTION ==========
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.pack(fill="x", pady=(0, 15))
        
        # Search by name/ingredient
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Enter recipe name or ingredient (e.g., Chicken, Pasta, Cake)...",
            font=ctk.CTkFont(size=14),
            height=40,
            corner_radius=8
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        self.search_entry.bind("<Return>", lambda event: self.search_by_name())
        
        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="🔍 Search",
            command=self.search_by_name,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=120,
            corner_radius=8
        )
        self.search_btn.pack(side="right", padx=10, pady=10)
        
        # Quick action buttons
        self.actions_frame = ctk.CTkFrame(self.main_frame)
        self.actions_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        self.random_btn = ctk.CTkButton(
            self.actions_frame,
            text="🎲 Random Recipe",
            command=self.get_random_recipe,
            font=ctk.CTkFont(size=13),
            height=35,
            corner_radius=8,
            fg_color="#E67E22",
            hover_color="#D35400"
        )
        self.random_btn.pack(side="left", padx=10, pady=5, expand=True, fill="x")
        
        self.popular_btn = ctk.CTkButton(
            self.actions_frame,
            text="⭐ Popular Recipes",
            command=self.get_popular_recipes,
            font=ctk.CTkFont(size=13),
            height=35,
            corner_radius=8,
            fg_color="#27AE60",
            hover_color="#229954"
        )
        self.popular_btn.pack(side="left", padx=10, pady=5, expand=True, fill="x")
        
        self.clear_btn = ctk.CTkButton(
            self.actions_frame,
            text="🗑 Clear",
            command=self.clear_results,
            font=ctk.CTkFont(size=13),
            height=35,
            corner_radius=8,
            fg_color="#95A5A6",
            hover_color="#7F8C8D"
        )
        self.clear_btn.pack(side="left", padx=10, pady=5, expand=True, fill="x")
        
        # ========== FILTER SECTION ==========
        self.filter_frame = ctk.CTkFrame(self.main_frame)
        self.filter_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        # Category filter
        self.category_label = ctk.CTkLabel(
            self.filter_frame,
            text="📂 Category:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.category_label.grid(row=0, column=0, padx=(10, 5), pady=8, sticky="w")
        
        self.category_var = ctk.StringVar(value="All Categories")
        self.category_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["All Categories"] + self.categories,
            variable=self.category_var,
            command=self.filter_by_category,
            font=ctk.CTkFont(size=13),
            height=35,
            width=150,
            corner_radius=6
        )
        self.category_dropdown.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        
        # Cuisine filter
        self.cuisine_label = ctk.CTkLabel(
            self.filter_frame,
            text="🌍 Cuisine:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.cuisine_label.grid(row=0, column=2, padx=(20, 5), pady=8, sticky="w")
        
        self.cuisine_var = ctk.StringVar(value="All Cuisines")
        self.cuisine_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["All Cuisines"] + self.cuisines,
            variable=self.cuisine_var,
            command=self.filter_by_cuisine,
            font=ctk.CTkFont(size=13),
            height=35,
            width=150,
            corner_radius=6
        )
        self.cuisine_dropdown.grid(row=0, column=3, padx=5, pady=8, sticky="w")
        
        # ========== RESULTS SECTION ==========
        self.results_container = ctk.CTkFrame(self.main_frame)
        self.results_container.pack(fill="both", expand=True)
        
        # Results header
        self.results_header = ctk.CTkFrame(self.results_container)
        self.results_header.pack(fill="x", pady=(0, 10))
        
        self.results_title = ctk.CTkLabel(
            self.results_header,
            text="📋 Results",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.results_title.pack(side="left", padx=10, pady=8)
        
        self.results_count = ctk.CTkLabel(
            self.results_header,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.results_count.pack(side="right", padx=10, pady=8)
        
        # Scrollable results area
        self.results_scroll = ctk.CTkScrollableFrame(
            self.results_container,
            corner_radius=10
        )
        self.results_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initial placeholder
        self.show_placeholder()
        
        # ========== FOOTER ==========
        self.footer_frame = ctk.CTkFrame(self.main_frame)
        self.footer_frame.pack(fill="x", pady=(10, 0))
        
        self.footer_label = ctk.CTkLabel(
            self.footer_frame,
            text="💡 Powered by TheMealDB • Free Recipe API • No API Key Required!",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.footer_label.pack(pady=5)
        
    def show_placeholder(self):
        """Show initial placeholder message"""
        # Clear existing content
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        self.placeholder_frame = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
        self.placeholder_frame.pack(expand=True, fill="both", padx=20, pady=40)
        
        ctk.CTkLabel(
            self.placeholder_frame,
            text="🍽️",
            font=ctk.CTkFont(size=80)
        ).pack(pady=20)
        
        ctk.CTkLabel(
            self.placeholder_frame,
            text="Start your culinary adventure!",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            self.placeholder_frame,
            text="Search by recipe name, ingredient, category, or cuisine\nOr try a random recipe for inspiration!",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=10)
        
    def search_by_name(self):
        """Search recipes by name or ingredient"""
        query = self.search_entry.get().strip()
        
        if not query:
            self.show_error("Please enter a recipe name or ingredient")
            return
            
        # Show loading
        self.show_loading()
        
        # Search in background thread
        thread = threading.Thread(target=self._fetch_recipes, args=("search", {"s": query}))
        thread.daemon = True
        thread.start()
        
    def filter_by_category(self, category):
        """Filter recipes by category"""
        if category == "All Categories":
            return
            
        self.show_loading()
        
        thread = threading.Thread(target=self._fetch_recipes, args=("category", {"c": category}))
        thread.daemon = True
        thread.start()
        
    def filter_by_cuisine(self, cuisine):
        """Filter recipes by cuisine type"""
        if cuisine == "All Cuisines":
            return
            
        self.show_loading()
        
        thread = threading.Thread(target=self._fetch_recipes, args=("area", {"a": cuisine}))
        thread.daemon = True
        thread.start()
        
    def get_random_recipe(self):
        """Get a random recipe"""
        self.show_loading()
        
        thread = threading.Thread(target=self._fetch_recipes, args=("random", {}))
        thread.daemon = True
        thread.start()
        
    def get_popular_recipes(self):
        """Get popular recipes (latest recipes)"""
        self.show_loading()
        
        thread = threading.Thread(target=self._fetch_recipes, args=("latest", {}))
        thread.daemon = True
        thread.start()
        
    def _fetch_recipes(self, search_type, params):
        """Fetch recipes from API (runs in background thread)"""
        try:
            if search_type == "search":
                url = f"{self.BASE_URL}/search.php"
            elif search_type == "category":
                url = f"{self.BASE_URL}/filter.php"
            elif search_type == "area":
                url = f"{self.BASE_URL}/filter.php"
            elif search_type == "random":
                url = f"{self.BASE_URL}/random.php"
                params = {}
            elif search_type == "latest":
                url = f"{self.BASE_URL}/latest.php"
            else:
                url = f"{self.BASE_URL}/search.php"
                
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            meals = data.get("meals", [])
            
            # Validate and filter recipes
            recipes = []
            if meals:
                for meal in meals:
                    # Ensure meal is a dictionary, not a string
                    if isinstance(meal, dict):
                        recipes.append(meal)
                    elif isinstance(meal, str) and meal:
                        # Handle case where API returns just recipe names
                        recipes.append({"strMeal": meal})
            
            if recipes:
                self.after(0, lambda: self.display_recipes(recipes))
            else:
                self.after(0, lambda: self.show_error("No recipes found. Try a different search term!"))
                
        except requests.exceptions.Timeout:
            self.after(0, lambda: self.show_error("Request timed out. Please try again."))
            
        except requests.exceptions.RequestException as e:
            self.after(0, lambda: self.show_error(f"Network error: {str(e)}"))
            
        except Exception as e:
            self.after(0, lambda: self.show_error(f"Error: {str(e)}"))
            
    def display_recipes(self, recipes):
        """Display recipes in the results area"""
        # Filter valid recipes (must be dictionaries)
        valid_recipes = [r for r in recipes if isinstance(r, dict)]
        self.current_recipes = valid_recipes
        
        # Remove placeholder/error if exists
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        # Update results header
        self.results_count.configure(text=f"Found {len(valid_recipes)} recipe(s)")
        
        # Display each recipe
        for idx, recipe in enumerate(valid_recipes):
            try:
                recipe_card = self.create_recipe_card(recipe, idx)
                recipe_card.pack(fill="x", pady=8, padx=5)
            except Exception as e:
                print(f"Error creating card for recipe {idx}: {e}")
                continue
            
    def create_recipe_card(self, recipe, index):
        """Create a recipe card widget"""
        # Ensure recipe is a dictionary
        if not isinstance(recipe, dict):
            return None
            
        card = ctk.CTkFrame(self.results_scroll, corner_radius=12)
        card.pack(fill="x", pady=8, padx=5)
        
        # Recipe image and info container
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=12)
        
        # Recipe name
        name_label = ctk.CTkLabel(
            info_frame,
            text=recipe.get("strMeal", "Unknown"),
            font=ctk.CTkFont(size=20, weight="bold"),
            wraplength=600,
            justify="left"
        )
        name_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Category and Area badges
        badges_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        badges_frame.pack(side="right")
        
        category = recipe.get("strCategory", "")
        area = recipe.get("strArea", "")
        
        if category:
            category_badge = ctk.CTkLabel(
                badges_frame,
                text=f"📁 {category}",
                font=ctk.CTkFont(size=12),
                text_color="#3498DB",
                corner_radius=10
            )
            category_badge.pack(side="left", padx=3)
            
        if area:
            area_badge = ctk.CTkLabel(
                badges_frame,
                text=f"🌍 {area}",
                font=ctk.CTkFont(size=12),
                text_color="#27AE60",
                corner_radius=10
            )
            area_badge.pack(side="left", padx=3)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        # View Recipe button
        view_btn = ctk.CTkButton(
            btn_frame,
            text="📖 View Full Recipe",
            command=lambda r=recipe: self.show_recipe_detail(r),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color="#E67E22",
            hover_color="#D35400"
        )
        view_btn.pack(side="left", padx=(0, 10))
        
        # Watch Video button (if available)
        video_url = recipe.get("strYoutube", "")
        if video_url:
            video_btn = ctk.CTkButton(
                btn_frame,
                text="🎥 Watch Video",
                command=lambda url=video_url: self.open_link(url),
                font=ctk.CTkFont(size=14),
                height=40,
                corner_radius=8,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                width=130
            )
            video_btn.pack(side="left", padx=(0, 10))
            
        # Source link (if available)
        source_url = recipe.get("strSource", "")
        if source_url:
            source_btn = ctk.CTkButton(
                btn_frame,
                text="🔗 Source",
                command=lambda url=source_url: self.open_link(url),
                font=ctk.CTkFont(size=14),
                height=40,
                corner_radius=8,
                fg_color="#3498DB",
                hover_color="#2980B9",
                width=100
            )
            source_btn.pack(side="left")
            
        return card
        
    def show_recipe_detail(self, recipe):
        """Show detailed recipe view in a new window"""
        # Ensure recipe is a dictionary
        if not isinstance(recipe, dict):
            return
            
        detail_window = ctk.CTkToplevel(self)
        detail_window.title(f"Recipe: {recipe.get('strMeal', 'Unknown')}")
        detail_window.geometry("800x700")
        detail_window.resizable(True, True)
        
        # Main container
        main_frame = ctk.CTkFrame(detail_window, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text=recipe.get("strMeal", "Unknown Recipe"),
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Category and Area
        info_text = ""
        if recipe.get("strCategory"):
            info_text += f"📁 {recipe.get('strCategory')}"
        if recipe.get("strArea"):
            if info_text:
                info_text += "    •    "
            info_text += f"🌍 {recipe.get('strArea')}"
            
        if info_text:
            info_label = ctk.CTkLabel(
                main_frame,
                text=info_text,
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            info_label.pack(pady=(0, 10))
        
        # Tags (if available)
        tags = recipe.get("strTags", "")
        if tags:
            tags_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            tags_frame.pack(pady=(0, 10))
            
            for tag in tags.split(","):
                tag_label = ctk.CTkLabel(
                    tags_frame,
                    text=f"#{tag.strip()}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#9B59B6",
                    corner_radius=8
                )
                tag_label.pack(side="left", padx=3)
        
        # Scrollable content area
        scroll_frame = ctk.CTkScrollableFrame(main_frame, corner_radius=10)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Extract ingredients and measures
        ingredients = []
        for i in range(1, 21):
            ingredient = recipe.get(f"strIngredient{i}", "")
            measure = recipe.get(f"strMeasure{i}", "")
            
            if ingredient and ingredient.strip():
                ingredients.append({
                    "ingredient": ingredient.strip(),
                    "measure": measure.strip() if measure else ""
                })
        
        # Ingredients section
        ingredients_header = ctk.CTkLabel(
            scroll_frame,
            text="🥘 Ingredients",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        ingredients_header.pack(fill="x", pady=(10, 10), anchor="w")
        
        ingredients_list = ctk.CTkFrame(scroll_frame)
        ingredients_list.pack(fill="x", pady=5)
        
        for idx, ing in enumerate(ingredients):
            ingredient_text = f"✓  {ing['measure']} {ing['ingredient']}" if ing['measure'] else f"✓  {ing['ingredient']}"
            ing_label = ctk.CTkLabel(
                ingredients_list,
                text=ingredient_text,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            ing_label.pack(fill="x", padx=15, pady=6, anchor="w")
        
        # Instructions section
        instructions_header = ctk.CTkLabel(
            scroll_frame,
            text="📝 Instructions",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        instructions_header.pack(fill="x", pady=(15, 10), anchor="w")
        
        instructions = recipe.get("strInstructions", "No instructions available")
        # Clean up instructions (remove HTML tags if present)
        instructions = self.clean_instructions(instructions)
        
        instructions_box = ctk.CTkTextbox(
            scroll_frame,
            font=ctk.CTkFont(size=14),
            height=250,
            corner_radius=8,
            wrap="word"
        )
        instructions_box.pack(fill="both", pady=5, expand=True)
        instructions_box.insert("1.0", instructions)
        instructions_box.configure(state="disabled")
        
        # Action buttons at bottom
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 10))
        
        # Video tutorial
        video_url = recipe.get("strYoutube", "")
        if video_url:
            video_btn = ctk.CTkButton(
                btn_frame,
                text="🎥 Watch Video Tutorial",
                command=lambda: self.open_link(video_url),
                font=ctk.CTkFont(size=14, weight="bold"),
                height=45,
                corner_radius=8,
                fg_color="#E74C3C",
                hover_color="#C0392B"
            )
            video_btn.pack(side="left", padx=5, expand=True, fill="x")
            
        # Source
        source_url = recipe.get("strSource", "")
        if source_url:
            source_btn = ctk.CTkButton(
                btn_frame,
                text="🔗 View Original Source",
                command=lambda: self.open_link(source_url),
                font=ctk.CTkFont(size=14, weight="bold"),
                height=45,
                corner_radius=8,
                fg_color="#3498DB",
                hover_color="#2980B9"
            )
            source_btn.pack(side="left", padx=5, expand=True, fill="x")
        
    def clean_instructions(self, instructions):
        """Clean up recipe instructions"""
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', instructions)
        # Remove extra whitespace
        clean = ' '.join(clean.split())
        # Add line breaks after periods for better readability
        clean = clean.replace('. ', '.\n\n')
        return clean
        
    def open_link(self, url):
        """Open URL in default browser"""
        if url:
            webbrowser.open(url)
            
    def show_loading(self):
        """Show loading state"""
        # Clear previous results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        loading_frame = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
        loading_frame.pack(expand=True, fill="both", padx=20, pady=60)
        
        ctk.CTkLabel(
            loading_frame,
            text="⏳",
            font=ctk.CTkFont(size=60)
        ).pack(pady=20)
        
        ctk.CTkLabel(
            loading_frame,
            text="Searching for delicious recipes...",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            loading_frame,
            text="Please wait a moment",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
    def show_error(self, message):
        """Show error message"""
        # Clear previous results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        error_frame = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
        error_frame.pack(expand=True, fill="both", padx=20, pady=60)
        
        ctk.CTkLabel(
            error_frame,
            text="😕",
            font=ctk.CTkFont(size=60)
        ).pack(pady=20)
        
        ctk.CTkLabel(
            error_frame,
            text=message,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#E74C3C"
        ).pack(pady=10)
        
    def clear_results(self):
        """Clear all results and show placeholder"""
        self.search_entry.delete(0, 'end')
        self.category_var.set("All Categories")
        self.cuisine_var.set("All Cuisines")
        self.current_recipes = []
        
        # Clear results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        self.results_count.configure(text="")
        self.show_placeholder()


if __name__ == "__main__":
    # Create and run the application
    app = RecipeFinderApp()
    app.mainloop()
