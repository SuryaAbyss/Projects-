from tkinter import *
from tkinter import ttk
import requests

def data_get():
    city = city_combobox.get()
    if city:
        data = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=8f31d05d802c04297f73a005cd9414af").json()
        w_label1.config(text=data['weather'][0]["main"])
        wb_label1.config(text=data["weather"][0]["description"])
        temp_label1.config(text=str(data["main"]["temp"] - 273.15) + " °C")
        per_label1.config(text=str(data["main"]["pressure"]) + " hPa")

win = Tk()
win.title("Weather App - Surya")
win.config(bg="#2c3e50")
win.geometry("500x600")

name_label = Label(win, text="Weather App - Surya", bg="#1abc9c", fg="white",
                   font=("Verdana", 24, "bold"))
name_label.place(x=25, y=20, height=60, width=450)

city_name = StringVar()
states_cities = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Ziro", "Pasighat"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar", "Tezpur"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur"],
    "Chhattisgarh": ["Raipur", "Bilaspur", "Durg", "Korba"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Haryana": ["Chandigarh", "Gurgaon", "Faridabad", "Panipat"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Kullu"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Kollam"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Manipur": ["Imphal", "Bishnupur", "Thoubal", "Ukhrul"],
    "Meghalaya": ["Shillong", "Tura", "Cherrapunji", "Jowai"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Serchhip"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Mon"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Puri", "Sambalpur"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Ajmer"],
    "Sikkim": ["Gangtok", "Namchi", "Pelling", "Lachung"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailashahar"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Nainital", "Rishikesh"],
    "West Bengal": ["Kolkata", "Darjeeling", "Siliguri", "Durgapur"],
    "Andaman and Nicobar Islands": ["Port Blair", "Havelock Island", "Neil Island", "Diglipur"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Silvassa", "Daman", "Diu"],
    "Delhi": ["New Delhi", "Old Delhi"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Leh", "Pahalgam"],
    "Ladakh": ["Leh", "Kargil", "Nubra Valley"],
    "Lakshadweep": ["Kavaratti", "Agatti", "Minicoy"],
    "Puducherry": ["Pondicherry", "Karaikal", "Yanam"],
}

com = ttk.Combobox(win, values=list(states_cities.keys()),
                   font=("Verdana", 14), textvariable=city_name)
com.place(x=25, y=100, height=40, width=450)

# New combobox for cities
city_combobox = ttk.Combobox(win, font=("Verdana", 14))
city_combobox.place(x=25, y=160, height=40, width=450)

# Function to update city combobox based on selected state
def update_cities(event):
    selected_state = com.get()
    city_combobox['values'] = states_cities.get(selected_state, [])

com.bind("<<ComboboxSelected>>", update_cities)

w_label = Label(win, text="Weather Climate", bg="#34495e", fg="white",
                font=("Verdana", 14, "italic"))
w_label.place(x=25, y=220, height=40, width=220)

w_label1 = Label(win, text="", bg="#34495e", fg="white",
                 font=("Verdana", 14, "italic"))
w_label1.place(x=250, y=220, height=40, width=220)

wb_label = Label(win, text="Weather Description", bg="#34495e", fg="white",
                 font=("Verdana", 14, "italic"))
wb_label.place(x=25, y=280, height=40, width=220)

wb_label1 = Label(win, text="", bg="#34495e", fg="white",
                  font=("Verdana", 14, "italic"))
wb_label1.place(x=250, y=280, height=40, width=220)

temp_label = Label(win, text="Temperature", bg="#34495e", fg="white",
                   font=("Verdana", 14, "italic"))
temp_label.place(x=25, y=340, height=40, width=220)

temp_label1 = Label(win, text="", bg="#34495e", fg="white",
                    font=("Verdana", 14, "italic"))
temp_label1.place(x=250, y=340, height=40, width=220)

per_label = Label(win, text="Pressure", bg="#34495e", fg="white",
                  font=("Verdana", 14, "italic"))
per_label.place(x=25, y=400, height=40, width=220)

per_label1 = Label(win, text="", bg="#34495e", fg="white",
                   font=("Verdana", 14, "italic"))
per_label1.place(x=250, y=400, height=40, width=220)

done_button = Button(win, text="Get Weather", bg="#1abc9c", fg="white",
                     font=("Verdana", 14, "bold"), command=data_get)
done_button.place(y=480, height=50, width=200, x=150)

win.mainloop()