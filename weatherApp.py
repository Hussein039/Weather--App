import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=7374a84a25c0ae3849072bfe175bc276"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != "404":
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_info = f"Weather in {city}:\n\n" \
                       f"Description: {weather_description}\n" \
                       f"Temperature: {temperature} K\n" \
                       f"Humidity: {humidity}%\n" \
                       f"Wind Speed: {wind_speed} m/s"

        # Clear previous weather info
        weather_text.delete(1.0, tk.END)
        weather_text.insert(tk.END, weather_info)
    else:
        messagebox.showerror("Error", f"City '{city}' not found.")

def get_weather_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=7374a84a25c0ae3849072bfe175bc276"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != "404":
        forecast_list = data["list"]

        # Clear previous forecast info
        forecast_text.delete(1.0, tk.END)

        # Initialize lists to store forecast data
        forecast_dates = []
        forecast_temps = []
        forecast_humidity = []

        # Get the forecast for the next 7 days
        today = datetime.today().date()
        for i in range(7):
            forecast_date = today + timedelta(days=i)
            forecast_info = f"{forecast_date}:\n"

            # Find the weather data for the forecast date
            for forecast in forecast_list:
                forecast_dt = datetime.fromtimestamp(forecast["dt"]).date()
                if forecast_dt == forecast_date:
                    weather_description = forecast["weather"][0]["description"]
                    temperature = forecast["main"]["temp"]
                    humidity = forecast["main"]["humidity"]
                    wind_speed = forecast["wind"]["speed"]
                    forecast_info += f"Description: {weather_description}\n" \
                                     f"Temperature: {temperature} K\n" \
                                     f"Humidity: {humidity}%\n" \
                                     f"Wind Speed: {wind_speed} m/s\n\n"

                    # Append forecast data to lists
                    forecast_dates.append(forecast_date)
                    forecast_temps.append(temperature)
                    forecast_humidity.append(humidity)

            forecast_text.insert(tk.END, forecast_info)

        # Plot the forecast data
        plot_forecast(forecast_dates, forecast_temps, forecast_humidity)
    else:
        messagebox.showerror("Error", f"City '{city}' not found.")

def plot_forecast(dates, temps, humidity):
    plt.figure(figsize=(8, 6))
    plt.plot(dates, temps, marker='o', label='Temperature (K)')
    plt.plot(dates, humidity, marker='o', label='Humidity (%)')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('7-Day Weather Forecast')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def get_weather_button_click():
    city = city_entry.get()
    if city:
        get_weather(city)
        get_weather_forecast(city)
    else:
        messagebox.showwarning("Warning", "Please enter a city name.")

# Create the main window
window = tk.Tk()
window.title("Weather App")
window.geometry("500x500")
window.configure(background="light gray")

# Create and pack the widgets
title_label = tk.Label(window, text="Weather App", bg="light gray", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

city_label = tk.Label(window, text="Enter a city name:", bg="light gray", font=("Arial", 12))
city_label.pack()

city_entry = tk.Entry(window, width=30, font=("Arial", 12))
city_entry.pack()

get_weather_button = tk.Button(window, text="Get Weather", command=get_weather_button_click, font=("Arial", 12))
get_weather_button.pack(pady=10)

weather_frame = tk.LabelFrame(window, text="Current Weather", bg="light gray", font=("Arial", 12))
weather_frame.pack(pady=10)

weather_text = tk.Text(weather_frame, width=50, height=6, font=("Arial", 12))
weather_text.pack()

forecast_frame = tk.LabelFrame(window, text="7-Day Forecast", bg="light gray", font=("Arial", 12))
forecast_frame.pack(pady=10)

forecast_text = tk.Text(forecast_frame, width=50, height=10, font=("Arial", 12))
forecast_text.pack()

# Start the main event loop
window.mainloop()
