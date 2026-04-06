# 🍳 Recipe Finder Application

A modern, user-friendly recipe searching application built with Python and CustomTkinter, powered by TheMealDB API.

## ✨ Features

### 🔍 Multiple Search Options
- **Search by Name/Ingredient**: Find recipes by entering recipe names or ingredients
- **Filter by Category**: Browse by protein type (Beef, Chicken, Seafood, Vegetarian, etc.)
- **Filter by Cuisine**: Explore recipes from 27+ cuisines worldwide
- **Random Recipe**: Get inspired with random recipes from the database
- **Popular Recipes**: View the latest added recipes

### 📖 Detailed Recipe Information
- Complete ingredient list with measurements
- Step-by-step cooking instructions
- Recipe category and origin country
- Video tutorials (YouTube links)
- Source website links
- Recipe tags for easy browsing

### 🎨 Modern UI/UX
- Beautiful dark theme interface
- Responsive and resizable window
- Smooth animations and transitions
- Color-coded category and cuisine badges
- Intuitive navigation and layout
- Loading states and error handling

### 🌟 Dynamic Features
- Multi-threaded API calls (non-blocking UI)
- Real-time search results
- Quick action buttons for common tasks
- Clear results functionality
- External links open in browser

## 📋 Prerequisites

- Python 3.7 or higher
- Internet connection (for API access)
- **No API key required!** TheMealDB is completely free

## 🚀 Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python recipe_finder.py
   ```

That's it! No API key configuration needed! 🎉

## 🎯 How to Use

### Basic Search
1. Enter a recipe name or ingredient in the search box
   - Examples: "Chicken", "Pasta Carbonara", "Cake", "Salmon"
2. Click "🔍 Search" or press Enter
3. Browse through the results

### Filter by Category
1. Select a category from the Category dropdown
   - Options: Beef, Chicken, Dessert, Lamb, Pasta, Pork, Seafood, Vegan, Vegetarian, etc.
2. Results will automatically load

### Filter by Cuisine
1. Select a cuisine type from the Cuisine dropdown
   - Options: Italian, Japanese, Mexican, Thai, Indian, and 20+ more
2. Results will automatically load

### Quick Actions
- **🎲 Random Recipe**: Discover something new and exciting!
- **⭐ Popular Recipes**: View the latest recipes added to the database
- **🗑 Clear**: Reset all filters and results

### Viewing Recipe Details
1. Click "📖 View Full Recipe" on any recipe card
2. A detailed view will open showing:
   - Complete ingredients with measurements
   - Step-by-step instructions
   - Recipe tags
   - Category and cuisine badges
3. Click "🎥 Watch Video Tutorial" to see cooking videos (opens in browser)
4. Click "🔗 View Original Source" to visit the recipe source website

## 📊 Recipe Categories

- **Beef**: Delicious beef dishes
- **Chicken**: Versatile chicken recipes
- **Dessert**: Sweet treats and desserts
- **Lamb**: Tender lamb dishes
- **Pasta**: Italian pasta favorites
- **Pork**: Savory pork recipes
- **Seafood**: Fresh seafood dishes
- **Vegetarian**: Meat-free meals
- **Vegan**: Plant-based recipes
- **Breakfast**: Morning meals
- **Side**: Perfect side dishes
- **Starter**: Appetizers and starters
- **Misc**: Other delicious recipes
- **Goat**: Goat meat specialties

## 🌍 Available Cuisines

American, British, Canadian, Chinese, Croatian, Dutch, Egyptian, French, Greek, Indian, Irish, Italian, Jamaican, Japanese, Kenyan, Malaysian, Mexican, Moroccan, Polish, Portuguese, Russian, Spanish, Thai, Tunisian, Turkish, Vietnamese, and more!

## 🎨 UI Features

### Recipe Cards
Each recipe is displayed in a beautiful card with:
- Recipe name (large and bold)
- Category badge (blue)
- Cuisine badge (green)
- Quick action buttons

### Detailed Recipe View
Opens in a separate window with:
- Recipe title and metadata
- Organized ingredient list with checkmarks
- Formatted cooking instructions
- Video tutorial button (red)
- Source link button (blue)
- Recipe tags in purple

### Responsive Design
- Minimum window size for usability
- Fully resizable
- Scrollable content areas
- Proper text wrapping
- Clean spacing and padding

## 🔧 Technical Details

### API Information
- **Provider**: TheMealDB
- **Cost**: 100% FREE
- **API Key**: Not required
- **Rate Limit**: Generous free tier
- **Documentation**: https://www.themealdb.com/api.php

### Architecture
- **Frontend**: CustomTkinter (Modern Tkinter)
- **HTTP Client**: Requests library
- **Threading**: Background API calls for smooth UI
- **Image Handling**: Pillow for future image support

### API Endpoints Used
- `/search.php?s=` - Search by recipe name
- `/filter.php?c=` - Filter by category
- `/filter.php?a=` - Filter by cuisine/area
- `/random.php` - Get random recipe
- `/latest.php` - Get latest/popular recipes

## 💡 Tips & Tricks

1. **Quick Search**: Press Enter after typing to search faster
2. **Explore Random**: Click "Random Recipe" when you can't decide what to cook
3. **Check Videos**: Many recipes include YouTube video tutorials
4. **Browse by Cuisine**: Discover dishes from specific countries
5. **Mix Filters**: Combine search with category/cuisine filters
6. **Save Favorites**: Note down recipe names you like for future reference

## 🐛 Troubleshooting

**No recipes found:**
- Try different search terms
- Check your internet connection
- Some ingredients may not have recipes

**Application not loading:**
- Ensure all dependencies are installed
- Run: `pip install -r requirements.txt`

**Video links not working:**
- Videos open in your default browser
- Check your internet connection
- Some recipes may not have video tutorials

**Slow performance:**
- API calls depend on network speed
- Results typically load within 2-5 seconds
- Background loading keeps UI responsive

## 📸 Screenshots Features

The application includes:
- Modern header with emoji icons
- Search bar with placeholder text
- Filter dropdowns for categories and cuisines
- Quick action buttons with distinct colors
- Scrollable recipe cards
- Detailed recipe view with ingredients & instructions
- External links for videos and sources

## 🔄 Comparison with Other Apps

| Feature | Recipe Finder | Other Apps |
|---------|--------------|------------|
| API Key Required | ❌ No | ✅ Often Yes |
| Cost | ✅ Free | 💰 Sometimes Paid |
| Video Tutorials | ✅ Yes | ⚠️ Limited |
| Source Links | ✅ Yes | ❌ Not Always |
| Cuisines | ✅ 27+ | ⚠️ Varies |
| Offline Mode | ❌ No | ❌ Rarely |

## 📝 Future Enhancements

Potential improvements:
- Recipe image display
- Save/favorite recipes locally
- Export recipe to PDF
- Meal planning feature
- Shopping list generator
- Recipe rating system
- User recipe submissions

## 📄 License

This project is open source and available for educational purposes.

TheMealDB API is free to use and community-driven.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 🙏 Credits

- **Recipe Data**: [TheMealDB](https://www.themealdb.com/)
- **UI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Developer**: Built with ❤️ for cooking enthusiasts

---

**Happy Cooking! 🍽️👨‍🍳👩‍🍳**

Made with Python and CustomTkinter
