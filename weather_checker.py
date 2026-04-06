"""
Weather Checker Application
A modern, user-friendly weather app using CustomTkinter and OpenWeatherMap API
"""

import customtkinter as ctk
import requests
import json
from datetime import datetime
from PIL import Image, ImageTk
import io
import threading
import os
from config import OPENWEATHERMAP_API_KEY, BASE_URL, FORECAST_URL, WEATHER_UNITS

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class WeatherApp(ctk.CTk):
    """Main Weather Application Class"""

    def __init__(self):
        super().__init__()

        # Configure main window
        self.title("Weather Checker")
        self.geometry("900x700")
        self.resizable(True, True)
        self.minsize(700, 600)

        # API Configuration
        self.API_KEY = OPENWEATHERMAP_API_KEY
        self.BASE_URL = BASE_URL
        self.FORECAST_URL = FORECAST_URL
        
        # Weather data cache
        self.weather_data = None
        
        # Dynamic background colors based on weather
        self.weather_colors = {
            "Clear": "#FFA500",
            "Clouds": "#708090",
            "Rain": "#4682B4",
            "Drizzle": "#5F9EA0",
            "Thunderstorm": "#4B0082",
            "Snow": "#B0C4DE",
            "Mist": "#D3D3D3",
            "default": "#2C3E50"
        }
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the User Interface"""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header Section
        self.header_frame = ctk.CTkFrame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🌤 Weather Checker",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=15)
        
        # Search Section
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.pack(fill="x", pady=(0, 20))
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Enter city name (e.g., Jakarta, London, Tokyo)...",
            font=ctk.CTkFont(size=16),
            height=45,
            corner_radius=10
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda event: self.search_weather())
        
        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="🔍 Search",
            command=self.search_weather,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=120,
            corner_radius=10
        )
        self.search_btn.pack(side="right")
        
        # Weather Display Section
        self.display_frame = ctk.CTkFrame(self.main_frame)
        self.display_frame.pack(fill="both", expand=True)
        
        # Initial placeholder message
        self.placeholder_label = ctk.CTkLabel(
            self.display_frame,
            text="Search for a city to see weather information",
            font=ctk.CTkFont(size=18),
            text_color="gray"
        )
        self.placeholder_label.pack(expand=True)
        
        # Weather Info Container (initially hidden)
        self.weather_container = ctk.CTkFrame(self.display_frame)
        
        # City Name and Country
        self.city_label = ctk.CTkLabel(
            self.weather_container,
            text="",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.city_label.pack(pady=(10, 5))
        
        self.country_label = ctk.CTkLabel(
            self.weather_container,
            text="",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.country_label.pack()
        
        # Weather Icon
        self.icon_label = ctk.CTkLabel(
            self.weather_container,
            text="",
            font=ctk.CTkFont(size=80)
        )
        self.icon_label.pack(pady=10)
        
        # Temperature
        self.temp_frame = ctk.CTkFrame(self.weather_container, fg_color="transparent")
        self.temp_frame.pack(pady=10)
        
        self.temp_label = ctk.CTkLabel(
            self.temp_frame,
            text="",
            font=ctk.CTkFont(size=64, weight="bold")
        )
        self.temp_label.pack(side="left", padx=(0, 10))
        
        self.feels_like_label = ctk.CTkLabel(
            self.temp_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.temp_label.bind("<Configure>", lambda e: self.update_feels_like_position())
        
        # Weather Description
        self.desc_label = ctk.CTkLabel(
            self.weather_container,
            text="",
            font=ctk.CTkFont(size=18)
        )
        self.desc_label.pack(pady=5)
        
        # Weather Details Grid
        self.details_frame = ctk.CTkFrame(self.weather_container)
        self.details_frame.pack(fill="x", padx=20, pady=20)
        
        # Humidity
        self.humidity_label = ctk.CTkLabel(
            self.details_frame,
            text="💧 Humidity",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.humidity_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.humidity_value = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=ctk.CTkFont(size=16)
        )
        self.humidity_value.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
        # Wind Speed
        self.wind_label = ctk.CTkLabel(
            self.details_frame,
            text="💨 Wind Speed",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.wind_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.wind_value = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=ctk.CTkFont(size=16)
        )
        self.wind_value.grid(row=1, column=1, padx=20, pady=10, sticky="e")
        
        # Pressure
        self.pressure_label = ctk.CTkLabel(
            self.details_frame,
            text="🌡 Pressure",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.pressure_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        self.pressure_value = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=ctk.CTkFont(size=16)
        )
        self.pressure_value.grid(row=2, column=1, padx=20, pady=10, sticky="e")
        
        # Visibility
        self.visibility_label = ctk.CTkLabel(
            self.details_frame,
            text="👁 Visibility",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.visibility_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.visibility_value = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=ctk.CTkFont(size=16)
        )
        self.visibility_value.grid(row=3, column=1, padx=20, pady=10, sticky="e")
        
        # Sunrise/Sunset
        self.sunrise_label = ctk.CTkLabel(
            self.details_frame,
            text="🌅 Sunrise",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.sunrise_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        self.sunrise_value = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=ctk.CTkFont(size=16)
        )
        self.sunrise_value.grid(row=4, column=1, padx=20, pady=10, sticky="e")
        
        self.sunset_label = ctk.CTkLabel(
            self.details_frame,
            text="🌇 Sunset",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.sunset_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        
        self.sunset_value = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=ctk.CTkFont(size=16)
        )
        self.sunset_value.grid(row=5, column=1, padx=20, pady=10, sticky="e")
        
        # Last Updated
        self.updated_label = ctk.CTkLabel(
            self.weather_container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.updated_label.pack(pady=10)
        
        # Refresh Button
        self.refresh_btn = ctk.CTkButton(
            self.weather_container,
            text="🔄 Refresh",
            command=self.refresh_weather,
            font=ctk.CTkFont(size=14),
            width=120,
            height=35,
            corner_radius=8
        )
        self.refresh_btn.pack(pady=(0, 10))
        
        # API Key Info
        self.api_info = ctk.CTkLabel(
            self.main_frame,
            text="💡 Get your free API key from: https://openweathermap.org/api",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.api_info.pack(pady=(10, 0))
        
    def update_feels_like_position(self, event=None):
        """Update feels like label position"""
        pass
        
    def search_weather(self):
        """Search for weather by city name"""
        city = self.search_entry.get().strip()
        
        if not city:
            self.show_error("Please enter a city name")
            return
            
        if self.API_KEY == "YOUR_API_KEY_HERE":
            self.show_error("Please set your OpenWeatherMap API key in the code")
            return
            
        # Show loading state
        self.search_btn.configure(text="⏳ Loading...", state="disabled")
        self.placeholder_label.configure(text="Fetching weather data...", text_color="gray")
        
        # Fetch weather in background thread
        thread = threading.Thread(target=self._fetch_weather, args=(city,))
        thread.daemon = True
        thread.start()
        
    def _fetch_weather(self, city):
        """Fetch weather data from API (runs in background thread)"""
        try:
            params = {
                "q": city,
                "appid": self.API_KEY,
                "units": "metric"
            }
            
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            self.weather_data = response.json()
            
            # Update UI in main thread
            self.after(0, self.display_weather)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                self.after(0, lambda: self.show_error("City not found. Please check the name."))
            elif e.response.status_code == 401:
                self.after(0, lambda: self.show_error("Invalid API key. Please check your configuration."))
            else:
                self.after(0, lambda: self.show_error(f"HTTP Error: {e.response.status_code}"))
                
        except requests.exceptions.Timeout:
            self.after(0, lambda: self.show_error("Request timed out. Please try again."))
            
        except requests.exceptions.RequestException as e:
            self.after(0, lambda: self.show_error(f"Network error: {str(e)}"))
            
        except Exception as e:
            self.after(0, lambda: self.show_error(f"Error: {str(e)}"))
            
        finally:
            self.after(0, self.reset_search_button)
            
    def display_weather(self):
        """Display weather data in the UI"""
        if not self.weather_data:
            return
            
        # Hide placeholder
        self.placeholder_label.pack_forget()
        
        # Show weather container
        self.weather_container.pack(fill="both", expand=True)
        
        # Extract data
        data = self.weather_data
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "N/A")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        temp_min = data.get("main", {}).get("temp_min", 0)
        temp_max = data.get("main", {}).get("temp_max", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        pressure = data.get("main", {}).get("pressure", 0)
        visibility = data.get("visibility", 0)
        wind_speed = data.get("wind", {}).get("speed", 0)
        description = data.get("weather", [{}])[0].get("description", "N/A").title()
        weather_main = data.get("weather", [{}])[0].get("main", "default")
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        sunrise = data.get("sys", {}).get("sunrise", 0)
        sunset = data.get("sys", {}).get("sunset", 0)
        
        # Update UI
        self.city_label.configure(text=f"{city_name}")
        self.country_label.configure(text=f"📍 {country}")
        
        # Weather icon emoji
        icon_emoji = self.get_weather_icon(icon_code, weather_main)
        self.icon_label.configure(text=icon_emoji)
        
        # Temperature
        self.temp_label.configure(text=f"{temp:.1f}°C")
        self.feels_like_label.configure(text=f"Feels like: {feels_like:.1f}°C\nMin: {temp_min:.1f}°C | Max: {temp_max:.1f}°C")
        self.feels_like_label.pack(side="left")
        
        # Description
        self.desc_label.configure(text=description)
        
        # Details
        self.humidity_value.configure(text=f"{humidity}%")
        self.wind_value.configure(text=f"{wind_speed} m/s")
        self.pressure_value.configure(text=f"{pressure} hPa")
        self.visibility_value.configure(text=f"{visibility/1000:.1f} km" if visibility else "N/A")
        
        # Sunrise/Sunset
        if sunrise:
            sunrise_time = datetime.fromtimestamp(sunrise).strftime("%H:%M:%S")
            self.sunrise_value.configure(text=sunrise_time)
        else:
            self.sunrise_value.configure(text="N/A")
            
        if sunset:
            sunset_time = datetime.fromtimestamp(sunset).strftime("%H:%M:%S")
            self.sunset_value.configure(text=sunset_time)
        else:
            self.sunset_value.configure(text="N/A")
        
        # Last updated
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_label.configure(text=f"Last updated: {current_time}")
        
        # Update background color based on weather
        self.update_weather_theme(weather_main)
        
    def get_weather_icon(self, icon_code, weather_main):
        """Get weather icon emoji based on weather condition"""
        # Day/night icons
        if "n" in icon_code:
            return "🌙"
        
        icon_map = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Haze": "🌫️",
            "Fog": "🌫️",
            "Smoke": "💨",
            "default": "🌤️"
        }
        
        return icon_map.get(weather_main, icon_map["default"])
    
    def update_weather_theme(self, weather_main):
        """Update UI colors based on weather condition"""
        color = self.weather_colors.get(weather_main, self.weather_colors["default"])
        # Subtle color change to search button
        self.search_btn.configure(fg_color=color)
        
    def show_error(self, message):
        """Show error message"""
        self.placeholder_label.configure(text=f"❌ {message}", text_color="red")
        self.placeholder_label.pack(expand=True)
        self.weather_container.pack_forget()
        
    def reset_search_button(self):
        """Reset search button state"""
        self.search_btn.configure(text="🔍 Search", state="normal")
        
    def refresh_weather(self):
        """Refresh current weather data"""
        city = self.city_label.cget("text")
        if city:
            self.search_btn.configure(text="⏳ Refreshing...", state="disabled")
            thread = threading.Thread(target=self._fetch_weather, args=(city,))
            thread.daemon = True
            thread.start()


if __name__ == "__main__":
    # Create and run the application
    app = WeatherApp()
    app.mainloop()
