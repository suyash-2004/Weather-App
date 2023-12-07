from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import requests
import tkinter as tk

img = None
weather_img = None

def on_entry_click(event):
    if location_entry.get() == "Enter location":
        location_entry.delete(0, "end")
        location_entry.config(fg='black')

def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            display_weather(data)
        else:
            messagebox.showerror("Error", f"Failed to retrieve weather data. {data['message']}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_weather(data):
    global img, weather_img

    temperature = data['main']['temp']
    description = data['weather'][0]['description'].capitalize()
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    result_text = f"Weather: {description}\n"
    tmp_text = f"{temperature:.1f}°C\n"
    feels_like_text = f"Feels like: {feels_like:.1f}°C"
    result_text += f"\nHumidity: {humidity}%\n\n"
    result_text += f"Wind Speed: {wind_speed} m/s"

    result_label.config(text=result_text)
    temperature_label.config(text=tmp_text)
    temperature_label2.config(text=feels_like_text)

    update_weather_image(description)

def get_weather_button_click():
    location = location_entry.get()
    if location and location != "Enter location":
        get_weather(api_key, location)
    else:
        messagebox.showwarning("Warning", "Please enter a location.")

def update_weather_image(description):
    global weather_img  

    if "clear" in description.lower():
        img_path = "clear.png"
    elif "cloud" in description.lower():
        img_path = "cloud.png"
    elif "rain" in description.lower():
        img_path = "rain.png"
    elif "drizzle" in description.lower():
        img_path = "drizzle.png"
    elif "thunderstorm" in description.lower():
        img_path = "thunderstorm.png"
    elif "snow" in description.lower():
        img_path = "snow.png"
    elif "mist" in description.lower():
        img_path = "mist.png"
    elif "fog" in description.lower():
        img_path = "fog.png"
    elif "smoke" in description.lower():
        img_path = "smoke.png"
    elif "haze" in description.lower():
        img_path = "haze.png"
    else:
        img_path = "default_image.png"

    weather_img = Image.open(img_path)
    weather_img = ImageTk.PhotoImage(weather_img, master=frame)
    label_img.configure(image=weather_img)
    label_img.image = weather_img

#api key
api_key = '18ea492f00ac8f26d384b15e690b5043'

# instance of tkinter window
win = Tk()
win.title("Weather App")
# efining the geometry of the window
win.geometry("275x590")
win.resizable(width=False, height=False)

font_style = ("Arial", 9)

# object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("template.png"), master=win)

# Frame for the widgets
frame = Frame(win, width=275, height=590)
frame.pack()

# Label Widget to display the image
label = Label(frame, image=img)

# Label Widget to display the weather image
label_img = Label(win, image=img)
label_img.place(relx=0.5, rely=0.7, anchor="center")

# Separator to mimic a thin line
separator = ttk.Separator(frame, orient='horizontal')
separator.place(x=20, y=33, width=237, height=1)
label.pack()
label_img.pack()

# Entry Widget for location input
location_entry = Entry(frame, width=20, bg='#E7DCD8', bd=0, highlightthickness=0, fg='grey')
location_entry.insert(0, "Enter location")
location_entry.bind("<FocusIn>", on_entry_click)
location_entry.place(x=110, y=16)

# Button Widget to trigger weather retrieval
get_weather_button = tk.Button(frame, text="Get Weather", bg="#E7DCD8", command=get_weather_button_click)
get_weather_button.place(x=100, y=50)

# Result label for other details
result_label = tk.Label(frame, text="", font=("Courier New", 13, "bold"), bg="#E7DCD8", wraplength=400)
result_label.place(relx=0.5, y=430, anchor="center")

# label for large temperature digits
temperature_label = tk.Label(frame, text="", font=("Courier New", 30, "bold"), bg="#DACBC4", wraplength=400)
temperature_label.place(relx=0.5, y=150, anchor="center")

# lable for "feels like...."
temperature_label2 = tk.Label(win, text="", font=("Courier New", 10), bg="#DACBC4")
temperature_label2.place(relx=0.5, y=170, anchor="center")

win.mainloop()
