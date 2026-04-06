# 🚀 Setup Guide - Weather Checker API

## Quick Start Guide

Follow these steps to activate the Weather Checker API and make the application functional:

### Step 1: Get Your Free OpenWeatherMap API Key

1. **Visit OpenWeatherMap**
   - Go to: https://openweathermap.org/api

2. **Create an Account**
   - Click "Sign Up" in the top right corner
   - Fill in your details (username, email, password)
   - Click "Create Account"

3. **Generate API Key**
   - After signing in, go to your account dashboard
   - Navigate to "API keys" tab
   - Your default API key will be automatically generated
   - Copy this key (it looks like a long string of letters and numbers)

4. **Wait for Activation**
   - ⚠️ **Important**: New API keys can take up to 2 hours to activate
   - You'll receive an email when your key is ready
   - Check the status in your OpenWeatherMap dashboard

### Step 2: Configure Your API Key

1. **Open the Configuration File**
   - Open `config.py` in this project

2. **Replace the Placeholder**
   ```python
   # Change this line:
   OPENWEATHERMAP_API_KEY = "YOUR_API_KEY_HERE"
   
   # To your actual API key:
   OPENWEATHERMAP_API_KEY = "your_actual_api_key_here"
   ```

3. **Save the File**

### Step 3: Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python weather_checker.py
```

## ✅ Testing Your Setup

1. Launch the application
2. Enter a city name (e.g., "Jakarta", "London", "Tokyo")
3. Click "Search" or press Enter
4. You should see weather information displayed

## 🔍 Troubleshooting

### "Invalid API key" Error
- **Cause**: Wrong API key or key not yet activated
- **Solution**: 
  - Double-check your API key in `config.py`
  - Wait up to 2 hours if you just created the key
  - Verify the key works on https://openweathermap.org/api

### "City not found" Error
- **Cause**: Misspelled city name
- **Solution**: 
  - Check spelling
  - Try adding country code (e.g., "London,UK" or "Paris,FR")

### Network Error
- **Cause**: No internet connection or firewall blocking
- **Solution**:
  - Check your internet connection
  - Verify firewall settings allow Python internet access

### Module Import Error
- **Cause**: Dependencies not installed
- **Solution**: Run `pip install -r requirements.txt`

## 🔐 Security Best Practices

- ✅ **Never share** your API key publicly
- ✅ **Don't commit** `config.py` to public repositories
- ✅ **Keep backups** of your API key in a secure location
- ✅ **Regenerate** your key if it gets compromised

## 📊 API Usage Limits

- **Free tier**: 60 calls/minute, 1,000,000 calls/month
- **Current weather**: Unlimited within rate limits
- **Forecast data**: Limited to 5 days / 3 hour steps

## 🎯 Next Steps

Once your API is working, you can:
- Customize the UI colors in `config.py`
- Change temperature units (Celsius/Fahrenheit)
- Add more cities to your search history
- Explore weather forecast features

## 📞 Support

If you need help:
- OpenWeatherMap Docs: https://openweathermap.org/api
- Check the README.md for feature documentation
- Review error messages in the application

---

**Happy Weather Checking! 🌤️**
