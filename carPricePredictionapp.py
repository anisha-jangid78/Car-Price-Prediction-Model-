from tkinter import *
import pickle

# Load model and scaler values

with open('saved_models/RandomForestRegressor.pkl', 'rb') as f:
    model = pickle.load(f)


with open('saved_scaling/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# radio btn values
seller_selected_value =""
fuel_selected_value =""
transmission_selected_value=""


def pred_price():

    try:
        input_values = []

        input_values.append(int(vehicle_age_entry.get()))
        input_values.append(int(km_driven_entry.get()))
        input_values.append(float(mileage_entry.get()))
        input_values.append(int(engine_entry.get()))
        input_values.append(float(max_power_entry.get()))

        if int(seats_entry.get())<=7:
            input_values.append(int(seats_entry.get()))
        else:
            print("Invalid seat selected")
            return

        # seller  type
        if seller_selected_value =='Dealer':
            input_values.extend([1,0,0])
        elif seller_selected_value =='Individual':
            input_values.extend([0,1,0])
        else:
            input_values.extend([0,0,1])

        # fuel  type
        if fuel_selected_value =='CNG':
            input_values.extend([1,0,0,0,0])
        elif fuel_selected_value =='Diesel':
            input_values.extend([0,1,0, 0, 0])
        elif fuel_selected_value =='Electric':
            input_values.extend([0,0, 1,0, 0])
        elif fuel_selected_value =='LPG':
            input_values.extend([0,0, 0, 1, 0])
        else:
            input_values.extend([0,0,0,0,1])

        # transmission type
        if transmission_selected_value =='Automatic':
            input_values.extend([1,0])
        else:
            input_values.extend([0,1])


        print(input_values)

        if len(input_values) == 16:
            input_scaled = scaler.transform([input_values])
            prediction = model.predict(input_scaled)[0]
            price_label.config(text=f'Predicted Price: Rs. {round(prediction, 2)}')
        else:
            print("Missing or incorrect Values")
    except Exception as e:
        print(f'Error: {e}')




# GUI Setup

root = Tk()
root.geometry('1080x720')
root.title("Car Price Prediction App")
root.config(bg='black')

title_label = Label(root, text='Car Price Prediction App',bg='black', fg='green',
                    font=("Times New Roman", 30, 'bold'))
title_label.pack(pady=30)

def create_labeled_entry(parent, label_text, padx=30):
    frame = Frame(parent, bg='black')
    frame.pack()
    label = Label(frame, text=label_text, bg='black', fg ='white', font=("Times New Roman", 20, 'bold'))
    label.pack(side=LEFT, padx=padx)
    entry = Entry(frame,font=("Times New Roman", 20, 'bold'))
    entry.pack(side=LEFT)
    return entry

# Entry widgets required
car_name_entry = create_labeled_entry(root, 'Car Name', 38)
vehicle_age_entry = create_labeled_entry(root, 'Vehicle Age', 30)
km_driven_entry = create_labeled_entry(root, 'KM Driven', 31)
mileage_entry = create_labeled_entry(root, 'Mileage', 52)
engine_entry = create_labeled_entry(root, 'Engine', 58)
max_power_entry = create_labeled_entry(root, 'Max Power', 32)
seats_entry = create_labeled_entry(root, 'Seats', 68)

# Radio Button: Seller Type
seller_type_frame = Frame(root, bg='black')
seller_type_frame.pack()

Label(seller_type_frame, text='Seller Type', bg='black', fg='white', font=("Times New Roman", 20, 'bold')).pack(side=LEFT, padx=30)

seller_type_values = {'Dealer': 'Dealer', 'Individual':"Individual", "Trustmark Dealer": "Trustmark Dealer"}
selected_seller =  StringVar(root, value='Dealer')
def on_seller_selected():
    global seller_selected_value
    seller_selected_value = selected_seller.get()

for (text, value) in seller_type_values.items():
    Radiobutton(seller_type_frame, text=text, variable=selected_seller, value=value, font=("Times New Roman", 10, 'bold'),
                command=on_seller_selected).pack(side=LEFT, ipady=5)


# Radio Button: Fuel Type
fuel_type_frame = Frame(root, bg='black')
fuel_type_frame.pack()

Label(fuel_type_frame, text='Fuel Type', bg='black', fg='white', font=("Times New Roman", 20, 'bold')).pack(side=LEFT, padx=52)

fuel_type_values = {'CNG':'CNG', 'Diesel':'Diesel', 'Electric':'Electric', 'LPG':'LPG', "Petrol":"Petrol"}
selected_fuel =  StringVar(root, value='Petrol')
def on_fuel_selected():
    global fuel_selected_value
    fuel_selected_value = selected_fuel.get()

for (text, value) in fuel_type_values.items():
    Radiobutton(fuel_type_frame, text=text, variable=selected_fuel, value=value, font=("Times New Roman", 10, 'bold'),
                command=on_fuel_selected).pack(side=LEFT, ipady=5)

# Radio Button: Transmission Type
transmission_type_frame = Frame(root, bg='black')
transmission_type_frame.pack()

Label(transmission_type_frame, text='Transmission Type', bg='black', fg='white', font=("Times New Roman", 20, 'bold')).pack(side=LEFT, padx=52)

transmission_type_values = {'Automatic':'Automatic','Manual':'Manual'}
selected_transmission =  StringVar(root, value='Manual')
def on_transmission_selected():
    global transmission_selected_value
    transmission_selected_value = selected_transmission.get()

for (text, value) in transmission_type_values.items():
    Radiobutton(transmission_type_frame, text=text, variable=selected_transmission, value=value, font=("Times New Roman", 10, 'bold'),
                command=on_transmission_selected).pack(side=LEFT, ipady=5)

# default values
on_seller_selected()
on_fuel_selected()
on_transmission_selected()


# Predict Button
pred_btn = Button(root, text='Predict Price', command=pred_price,
                  bg='green', fg='red', font=("Times New Roman", 20, 'bold'))
pred_btn.pack(pady=30)

# predict label
price_label = Label(root, text= 'Predicted Price: Rs. 0',
                    bg='black', fg='green', font=("Times New Roman", 20, 'bold'))
price_label.pack()
root.mainloop()