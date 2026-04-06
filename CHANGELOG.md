# Changelog

All notable changes to the Python Projects will be documented in this file.

## [2026-04-06] - Recipe Finder Bug Fixes

### 🐛 Fixed
- **AttributeError: 'str' object has no attribute 'get'**
  - Fixed API response validation issue where TheMealDB sometimes returns strings instead of dictionaries
  - Added type checking in `_fetch_recipes()` to validate meal data structure
  - Added defensive programming in `display_recipes()` to filter valid recipes
  - Added early return in `create_recipe_card()` for invalid recipe data
  - Added validation in `show_recipe_detail()` to prevent crashes

### 🔒 Improvements
- Better error handling for malformed API responses
- More robust data validation throughout the recipe loading pipeline
- Graceful degradation when individual recipe cards fail to create

### 📝 Code Changes
- `_fetch_recipes()`: Added validation loop to ensure all meals are dictionaries
- `display_recipes()`: Added filtering and try-catch for card creation
- `create_recipe_card()`: Added type check at function start
- `show_recipe_detail()`: Added type check before accessing recipe data

---

## [2026-04-06] - Main Menu Improvements

### 🐛 Fixed
- **TclError: cannot use geometry manager pack inside .!ctkframe which already has slaves managed by grid**
  - Fixed geometry manager conflict by using inner frames
  - Separated pack() and grid() usage to different container levels

### ✨ Added
- VSCode settings for better IntelliSense support
- `# type: ignore` comments for customtkinter imports
- TROUBLESHOOTING.md with comprehensive issue solutions

---

## [Initial Release] - Python Projects Collection

### 🌤️ Weather Checker
- Real-time weather data with OpenWeatherMap API
- Beautiful dynamic UI with weather-based themes
- Search by city name
- Temperature, humidity, wind, pressure, visibility data
- Sunrise/sunset times

### 🍳 Recipe Finder
- 1000+ recipes from TheMealDB API
- Search by recipe name or ingredient
- Filter by category and cuisine
- Random recipe generator
- Video tutorial links
- Detailed ingredient lists and instructions
- **NO API KEY REQUIRED**

### 🧮 Calculator
- Basic arithmetic operations
- Modern calculator interface
- Fast and responsive

### 🚀 Main Menu Launcher
- Centralized application launcher
- Beautiful project cards with icons
- Real-time status monitoring
- Process management (launch/stop)
- Auto-detection of available projects

---

## Notes

- All applications use CustomTkinter for modern UI
- Multi-threading for non-blocking API calls
- Dark theme by default
- Minimum Python version: 3.7
- Dependencies: customtkinter, requests, Pillow
