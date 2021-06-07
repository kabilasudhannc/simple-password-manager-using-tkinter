from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_entry():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title='Oops!', message="Please don't leave any fields empty!")

    else:
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search_website():
    website = website_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            contents = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(title='Error', message='No Data File Found')

    else:
        if website in contents:
            website_data = contents[website]
            email = website_data['email']
            password = website_data['password']
            pyperclip.copy(password)
            messagebox.askokcancel(website, f"Email: {email} \nPassword: {password} \npassword copied to clipboard!")

        else:
            messagebox.showerror(title='Error', message=f'There is no Data for {website}')


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website_label = Label(text='Website:')
website_label.grid(row=1, column=0)

website_entry = Entry(width=20)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)

email_entry = Entry(width=39)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, '@gmail.com')

password_label = Label(text='Password:')
password_label.grid(row=3, column=0)

password_entry = Entry(width=21, highlightthickness=0)
password_entry.grid(row=3, column=1)

generate_button = Button(text='Generate Password', command=password_generator, highlightthickness=0)
generate_button.grid(row=3, column=2)

add_button = Button(text='Add', command=add_entry, width=33)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text='Search', command=search_website)
search_button.grid(column=2, row=1)

window.mainloop()
