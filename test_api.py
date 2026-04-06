"""
Test script to verify OpenWeatherMap API key
"""
import requests
from config import OPENWEATHERMAP_API_KEY, BASE_URL, WEATHER_UNITS

def test_api_key():
    """Test if the API key is valid and working"""
    
    print("=" * 60)
    print("🔍 Testing OpenWeatherMap API Key")
    print("=" * 60)
    print()
    
    # Check if API key is still placeholder
    if OPENWEATHERMAP_API_KEY == "YOUR_API_KEY_HERE":
        print("❌ ERROR: API key is still set to placeholder!")
        print("   Please update config.py with your actual API key")
        print("   Get one from: https://openweathermap.org/api")
        return False
    
    print(f"📋 API Key: {OPENWEATHERMAP_API_KEY[:8]}...{OPENWEATHERMAP_API_KEY[-4:]}")
    print()
    
    # Test API call with a simple city
    test_city = "London"
    print(f"🌍 Testing with city: {test_city}")
    print()
    
    try:
        params = {
            "q": test_city,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": WEATHER_UNITS
        }
        
        print("⏳ Sending request to OpenWeatherMap API...")
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        # Check response status
        if response.status_code == 200:
            data = response.json()
            
            print("✅ SUCCESS! API key is valid and working!")
            print()
            print("-" * 60)
            print("📊 Test Weather Data:")
            print("-" * 60)
            print(f"🏙️  City: {data.get('name')}")
            print(f"🌡️  Temperature: {data['main']['temp']}°C")
            print(f"🌤️  Description: {data['weather'][0]['description'].title()}")
            print(f"💧 Humidity: {data['main']['humidity']}%")
            print(f"💨 Wind Speed: {data['wind']['speed']} m/s")
            print("-" * 60)
            print()
            print("🎉 Your API key is ready to use!")
            print("   You can now run: python weather_checker.py")
            return True
            
        elif response.status_code == 401:
            print("❌ ERROR: Invalid API key!")
            print()
            print("   Possible causes:")
            print("   1. API key is incorrect")
            print("   2. API key not yet activated (wait up to 2 hours)")
            print("   3. API key has been revoked")
            print()
            print("   Solutions:")
            print("   1. Check your API key at: https://openweathermap.org/api")
            print("   2. Wait 2 hours if you just created it")
            print("   3. Generate a new API key if needed")
            return False
            
        elif response.status_code == 404:
            print("❌ ERROR: City not found (but API key is valid!)")
            print("   This means your API key works, but there's a different issue")
            return True
            
        else:
            print(f"⚠️  WARNING: Unexpected response (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timed out")
        print("   Check your internet connection")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Network error")
        print(f"   Details: {str(e)}")
        print("   Check your internet connection")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: Unexpected error")
        print(f"   Details: {str(e)}")
        return False

if __name__ == "__main__":
    test_api_key()
    print()
