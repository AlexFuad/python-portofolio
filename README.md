# 🚀 Python Projects Launcher - Main Menu

A modern, centralized launcher application for all Python projects in this directory. One menu to access all your tools!

## ✨ Features

### 🎯 Centralized Launcher
- **Single Entry Point**: Launch any project from one beautiful interface
- **Modern UI**: Dark theme with colorful project cards
- **Real-time Status**: Monitor which applications are currently running
- **Process Management**: Stop running applications directly from the menu

### 📦 Available Projects

#### 1. 🌤️ Weather Checker
**Real-time weather information for any city worldwide**
- Current weather data with temperature, humidity, wind speed
- 5-day forecast
- Beautiful dynamic UI with weather-based themes
- Search by city name

**File**: `weather_checker.py`  
**API**: OpenWeatherMap (Free API key required)

#### 2. 🍳 Recipe Finder
**Discover delicious recipes from around the world**
- 1000+ recipes in the database
- Search by recipe name or ingredient
- Filter by category (Beef, Chicken, Vegetarian, etc.)
- Filter by cuisine (Italian, Japanese, Mexican, etc.)
- Random recipe generator
- Video tutorial links
- **NO API KEY REQUIRED!**

**File**: `recipe_finder.py`  
**API**: TheMealDB (100% Free)

#### 3. 🧮 Calculator
**Modern calculator for everyday calculations**
- Basic arithmetic operations
- Clean, intuitive interface
- Fast and responsive

**File**: `Calculator.py`

## 🚀 Quick Start

### Method 1: Using Main Menu (Recommended)
```bash
python main_menu.py
```
Then click "Launch Application" on any project card!

### Method 2: Direct Launch
```bash
# Weather Checker
python weather_checker.py

# Recipe Finder
python recipe_finder.py

# Calculator
python Calculator.py
```

## 📋 Prerequisites

- Python 3.7 or higher
- Internet connection (for Weather Checker and Recipe Finder)
- OpenWeatherMap API key (for Weather Checker only)

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🎨 Main Menu Features

### Project Cards
Each project is displayed as a beautiful card with:
- **Large Icon**: Visual representation of the project
- **Project Name**: Clear, bold title
- **Description**: Brief explanation of what the app does
- **Feature List**: Key features highlighted
- **Launch Button**: One-click to start the application

### Status Panel
- **Real-time Monitoring**: See which apps are currently running
- **Process Status**: Visual indicator (Running/Stopped)
- **Stop Button**: Terminate running applications
- **Auto-refresh**: Status updates every 2 seconds

### Smart Detection
- Automatically detects available projects
- Grayed out buttons for missing files
- Prevents duplicate launches
- Error handling for failed launches

## 🎯 How to Use

### Launching an Application
1. Open `main_menu.py`
2. Browse the available projects
3. Click "🚀 Launch Application" on your desired project
4. The application will open in a new window
5. Status changes to "✅ Running"

### Monitoring Running Apps
1. Check the "Running Applications" panel at the bottom
2. See which apps are currently active
3. Click "⏹ Stop" to terminate any running app

### Managing Multiple Apps
- You can run multiple applications simultaneously
- Each app runs in its own window
- Monitor all from the main menu status panel

## 📁 Project Structure

```
python-project/
│
├── main_menu.py              # 🚀 Main Launcher (START HERE)
├── weather_checker.py        # 🌤️ Weather Application
├── recipe_finder.py          # 🍳 Recipe Finder Application
├── Calculator.py             # 🧮 Calculator Application
│
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── RECIPE_FINDER.md          # Recipe Finder documentation
└── SETUP.md                  # Setup instructions
```

## 🔧 Configuration

### Weather Checker API Setup
1. Get free API key from: https://openweathermap.org/api
2. Open `config.py`
3. Update `OPENWEATHERMAP_API_KEY` with your key

### Recipe Finder
No configuration needed! Works out of the box with TheMealDB API.

## 💡 Tips & Tricks

1. **Use Main Menu**: Always start from `main_menu.py` for easy access
2. **Check Status Panel**: See what's running before launching new apps
3. **Stop Old Apps**: Close apps you're not using to free up resources
4. **Keyboard Shortcuts**: Each app has its own keyboard shortcuts
5. **Multiple Monitors**: Drag app windows to different monitors

## 🎨 UI Features

### Modern Design
- Dark mode interface (easy on the eyes)
- Color-coded project cards
- Smooth animations and transitions
- Responsive layout (resizable windows)

### User-Friendly
- Clear visual hierarchy
- Intuitive icons and colors
- Helpful placeholder messages
- Error messages with solutions

### Performance
- Non-blocking UI (multi-threading)
- Fast project detection
- Lightweight resource usage
- Smooth scrolling

## 🐛 Troubleshooting

**Main menu shows no projects:**
- Ensure project files are in the same directory
- Check that filenames match exactly:
  - `weather_checker.py`
  - `recipe_finder.py`
  - `Calculator.py`

**Application won't launch:**
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.7+)
- For Weather Checker: Verify API key in `config.py`

**Status not updating:**
- Status panel refreshes every 2 seconds
- Close and reopen main menu if needed

**Multiple instances:**
- Main menu prevents duplicate launches
- Use Stop button to close before relaunching

## 🔄 Updates & Enhancements

Future improvements:
- [ ] Add project screenshots in launcher
- [ ] Settings panel for all apps
- [ ] Recent projects list
- [ ] Favorite/quick access pins
- [ ] Auto-update checker
- [ ] Custom project addition
- [ ] Launch arguments support

## 📊 Comparison

| Feature | Main Menu | Direct Launch |
|---------|-----------|---------------|
| Easy Access | ✅ One place | ❌ Need to remember filenames |
| Status Monitor | ✅ Real-time | ❌ No monitoring |
| Process Control | ✅ Stop apps | ❌ Manual taskkill |
| Project Info | ✅ Cards with details | ❌ No overview |
| Duplicate Prevention | ✅ Built-in | ❌ Can launch multiple |

## 📝 License

This project collection is open source and available for educational purposes.

## 🙏 Credits

- **Weather Data**: [OpenWeatherMap](https://openweathermap.org/)
- **Recipe Data**: [TheMealDB](https://www.themealdb.com/)
- **UI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## 🤝 Contributing

Feel free to add your own Python projects to this directory! They will automatically appear in the main menu.

---

**Happy Coding! 🚀**

Made with ❤️ using Python and CustomTkinter

*Start with: `python main_menu.py`*
