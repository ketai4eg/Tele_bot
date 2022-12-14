"""This code used for running of simple telegram bot for scheduling of the manicure appointment.
Config file should be properly formatted.
The booking will be saved to JSON file."""


import telebot
from telebot import types
import config
import datetime
import json

bot = telebot.TeleBot(config.token)

#messages list
msg_hi="👋 Hi!"
msg_go_booking="❓ Let's go to the booking"
msg_contact="📞 Do you want my contacts"
msg_address="🌍 My address"
msg_gel="Gel"
msg_extension="Extension"
msg_simple="Simple Manicure"
msg_back="Go back"
msg_book_it="💅 Let's book it!"



#start screen
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(msg_hi)
    btn2 = types.KeyboardButton(msg_go_booking)
    btn3 = types.KeyboardButton(msg_contact)
    btn4 = types.KeyboardButton(msg_address)
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(message.chat.id,
                     text="Hi, {0.first_name}! I am bot, and I will help you to book your manicure! \n "
                          "👉 Remember, you have 15% of discount for your first visit! \n"
                          "😍 Additionally, I have loyalty card with discount for each 4th visit!".format(
                         message.from_user), reply_markup=markup)

#delliting of the appointment
@bot.message_handler(commands=['delete'])
def delete(message):
    with open("clients.json", "r") as a:
        data = a.read()
        clients = json.loads(data)
        comp = list(clients.keys())
        usrname = message.from_user.username
        if usrname in comp:
            del clients[usrname]
            bot.send_message(message.chat.id,
                             text=f"Dear {message.from_user.first_name},your appointment successfully deleted. Use comand \"/start\" to start your booking again.")
        else:
            bot.send_message(message.chat.id,
                             text=f"Dear {message.from_user.first_name}, you should book your appointment firstly. Use comand \"/start\" to start your booking.")
    with open("clients.json", "w") as f:
        data_json = json.dumps(clients)
        f.write(data_json)


#message Hi!
def hi(message:str) -> None:
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("My insta", url='https://instagram.com/marinastar.nails?igshid=YmMyMTA2M2Y=')
    markup.add(button1)
    bot.send_message(message.chat.id,
                     "Hi, {0.first_name}! Thank you for your interest! You can see examples of my work by link: ".format(
                         message.from_user),
                     reply_markup=markup)

#message Nail Type
def nail_types(message:str) -> None:
    if (message.text == msg_go_booking):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(msg_gel))
        markup.add(types.KeyboardButton(msg_extension))
        markup.add(types.KeyboardButton(msg_simple))
        markup.add(types.KeyboardButton(msg_back))
        bot.send_message(message.chat.id, text="What do you want to have?", reply_markup=markup)

#message Contacts
def contact(message:str) -> None:
    bot.send_message(message.chat.id,
                     text=f"☎️ My phone: {config.phone}. \n I also have WhatsApp. \n and Telegram {config.telega}")

#my address
def address(message:str) -> None:
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("My location",
                                         url=f'{config.google_link}')
    markup.add(button1)
    bot.send_message(message.chat.id, text=f"{config.address}",
                     reply_markup=markup)

#Prices
def prices(message:str) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(msg_book_it)
    button2 = types.KeyboardButton(msg_back)
    markup.add(button1)
    markup.add(button2)
    if message.text == msg_gel:
        price=config.gel_price
    elif message.text == msg_extension:
        price=config.extension_price
    elif message.text == msg_simple:
        price=config.simple_price
    bot.send_message(message.chat.id, text=f"Price is {price} €. Do you want to book an apointment?", reply_markup=markup)

#Go to the first page
def go_back(message:str) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(msg_hi))
    markup.add(types.KeyboardButton(msg_go_booking))
    markup.add(types.KeyboardButton(msg_contact))
    markup.add(types.KeyboardButton(msg_address))
    bot.send_message(message.chat.id, text="Again we are here: what do you want to have?", reply_markup=markup)

#Next week drawing
def next_week_days(message:str) -> None:
    my_datetime = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1,8):
        day_formated=(my_datetime + delta * i).strftime("%a")
        markup.add(types.KeyboardButton(f"{day_formated}"))
    back = types.KeyboardButton(msg_back)
    markup.add(back)
    bot.send_message(message.chat.id,
                     text="Choose any day of next week",
                     reply_markup=markup)

#Time drawing
def time_av(message:str) -> None:
    my_datetime = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(1, 8):
        if message.text == ((datetime.datetime.now() + delta * i).strftime("%a")):
            delta_date = datetime.timedelta(days=int(i))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for time_str in ["09:00-12:00", "13:00-16:00", "17:00-20:00"]:
        time_formated=(my_datetime + delta_date).strftime("%d.%m")
        markup.add(types.KeyboardButton(f"{message.text}, {time_formated},  {time_str}"))
    back = types.KeyboardButton(msg_back)
    markup.add(back)
    bot.send_message(message.chat.id,
                     text="Choose time",
                     reply_markup=markup)

#other
def other(message:str) -> None:
    bot.send_message(message.chat.id,
                     text="Sorry, I am very young and still don't know this command. Please, try to start with\"/start\"")

#Booking
def booking(message:str) -> None:
    line = message.text.split(", ")
    with open("clients.json", "r") as a:
        data = a.read()
        clients = json.loads(data)
        day = line[0]
        date = line[1]
        time = line[2]
        first_name = message.from_user.first_name
        comp = list(clients.keys())
        usrname = message.from_user.username
        val = list(clients.values())
        print(type(usrname))
        print(line)
        if clients:
            for val_list in val:
                if line == val_list[0:3]:
                    bot.send_message(message.chat.id,
                                     text=f"This time is already booked, sorry")
                    return
            if not usrname:
                bot.send_message(message.chat.id,
                                 text=f"Dear {message.from_user.first_name}, please add username in Telegram setting in order to continue booking process.")
            elif usrname in comp:
                if clients[message.from_user.username]:
                    bot.send_message(message.chat.id,
                                     text=f"Dear {message.from_user.first_name}, you already have an appointment at {clients[message.from_user.username]}. Use command \"/delete\" to delete your current appointment.")
            else:
                clients[message.from_user.username] = [day, date, time, first_name]
                bot.send_message(message.chat.id,
                                 text=f"Dear {message.from_user.first_name}, your appointment is booked for {clients[message.from_user.username]}, you will be contacted soon in order to confirm booking by Marina.")
                bot.send_message(config.telega_id,
                                 text=f"Marinochka! {message.from_user.first_name}, is booked for {clients[message.from_user.username]}, contact by @{message.from_user.username}")
        else:
            clients[message.from_user.username] = [day, date, time, first_name]
            bot.send_message(message.chat.id,
                             text=f"Dear {message.from_user.first_name}, your appointment is booked for {clients[message.from_user.username]}, you will be contacted soon in order to confirm booking by Marina.")
            bot.send_message(config.telega_id,
                             text=f"Marinochka! {message.from_user.first_name}, is booked for {clients[message.from_user.username]}, contact by @{message.from_user.username}")
    with open("clients.json", "w") as f:
        data_json = json.dumps(clients)
        f.write(data_json)

#main message treatment
@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == msg_hi):
        hi(message)
    elif (message.text == msg_go_booking):
        nail_types(message)
    elif (message.text == msg_contact):
        contact(message)
    elif (message.text == msg_address):
        address(message)
    elif (message.text == msg_gel or message.text == msg_extension or message.text == msg_simple):
        prices(message)
    elif (message.text == msg_back):
        go_back(message)
    elif (message.text == msg_book_it):
        next_week_days(message)
    elif (message.text in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        time_av(message)
    elif " 09:00-12:00" in message.text.split(", ") or " 13:00-16:00" in message.text.split(", ") or " 17:00-20:00" in message.text.split(", "):
        booking(message)
    else:
        other(message)
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
