import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk
import sqlite3
from os import getenv
from dotenv import load_dotenv


load_dotenv()

bg_color_1 = '#404040'
bg_color_2 = '#808080'
interface_color = '#0A2642'
interface_fg_color = '#B8B9BA'
transfer_bg = '#376a56'
transfer_entry = '#024e30'
withdraw_bg = '#4b0222'


class Gui:
    def __init__(self, database):
        self.done_label_withdraw = None
        self.withdraw_amount = None
        self.withdraw_confirm_button = None
        self.receiver_confirm_button = None
        self.receiver_entry_amount = None
        self.receiver_entry = None
        self.password_to_transfer = None
        self.name_user = None
        self.password_entry_login = None
        self.login_entry_login = None
        self.confirm_data_button = None
        self.name_entry = None
        self.surname_entry = None
        self.age_entry = None
        self.login_entry = None
        self.password_entry = None
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

        self.font = Font(
            family='Courier',
            size=32,
            weight='bold',
            slant='roman',
            underline=False,
            overstrike=False,
        )
        self.info_font = Font(
            family='Courier',
            size=13,
            weight='bold',
            slant='italic',
            underline=False,
            overstrike=False,
        )
        self.button_font = Font(
            family='Courier',
            size=19,
            weight='bold',
            slant='roman',
            underline=False,
            overstrike=False,
        )
        self.disclaimer_font = Font(
            family='Courier',
            size=10,
            weight='normal',
            slant='italic',
            underline=False,
            overstrike=False,
        )
        self.disclaimer_font1 = Font(
            family='Courier',
            size=7,
            weight='normal',
            slant='italic',
            underline=False,
            overstrike=False,
        )
        self.balance_font = Font(
            family='Courier',
            size=45,
            weight='normal',
            slant='italic',
            underline=False,
            overstrike=False,
        )
        self.withdraw_font = Font(
            family='Courier',
            size=27,
            weight='bold',
            slant='italic',
            underline=False,
            overstrike=False,
        )
        self.transfer_font = Font(
            family='Courier',
            size=20,
            weight='bold',
            slant='italic',
            underline=False,
            overstrike=False,
        )
        self.login_font = Font(
            family='Courier',
            size=22,
            weight='normal',
            slant='italic',
            underline=False,
            overstrike=False,
        )

    def __del__(self):
        self.connection.close()

    def create_table(self, info: str):
        self.cursor.execute(info)
        self.connection.commit()

    def getting_data(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        age = self.age_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()

        print(name, surname, age, login, password)
        balance = 0
        self.cursor.execute(f" INSERT INTO bank_user (name, surname, age, login, password, balance) "
                            f"VALUES ('{name}','{surname}','{age}','{login}','{password}','{balance}')")
        self.connection.commit()

    def checking_data(self):
        login_to_check = None
        password_to_check = None
        login = self.login_entry_login.get()
        self.cursor.execute(f"SELECT login FROM bank_user WHERE login = '{login}'")
        temp_login = self.cursor.fetchall()
        for password in temp_login:
            login_to_check = password[0]

        # print(login_to_check)
        if login_to_check is not None:
            self.cursor.execute(f"SELECT password FROM bank_user WHERE login ='{login_to_check}'")
            temp_pass = self.cursor.fetchall()
            for password in temp_pass:
                password_to_check = password[0]
            print(password_to_check)

        if login_to_check == self.login_entry_login.get() and password_to_check == self.password_entry_login.get():
            print('logged loving fortnite')
            logged_label = tk.Label(login_frame, text="Logged",
                                    font=self.disclaimer_font, background=bg_color_2, foreground=bg_color_1)
            logged_label.grid()

            self.name_user = login_to_check
            self.password_to_transfer = password_to_check
            self.load_interface()

        else:
            print('Wrong login or password')
            wrong = tk.Label(login_frame, text="Wrong login or password",
                             font=self.disclaimer_font, background=bg_color_2, foreground=bg_color_1)
            wrong.grid()

   
    def balance(self, login):
        self.cursor.execute(f"SELECT balance FROM bank_user WHERE login = '{login}'")
        balances = self.cursor.fetchall()
        for i in balances:
            balance = i[0]
            return balance

    def logout(self):
        self.clear_frame(interface_frame)
        self.load_title_frame()

    def transfer(self):
        to_someone = self.receiver_entry.get()
        log = None
        balance = None
        is_done = False
        self.cursor.execute(f"SELECT login FROM bank_user WHERE login = '{to_someone}'")
        is_login = self.cursor.fetchall()
        exist = False
        if exist is False:
            print('working')
        print(is_login)
        if len(is_login) > 0:
            exist = True
        else:
            exist = False
            print('This user does not exist')

        if exist is True:
            for i in is_login:
                log = i[0]

        print(log)
        amount = self.receiver_entry_amount.get()
        print(amount)
        print(self.name_user)
        self.cursor.execute(f"SELECT balance FROM bank_user WHERE login ='{self.name_user}'")
        balances = self.cursor.fetchall()
        for i in balances:
            balance = i[0]

        if log is None:
            print('dont exist')
            no_user_label = tk.Label(transfer_frame, text='This user does not exist',
                                     font=self.disclaimer_font, foreground=interface_fg_color, background=transfer_bg)
            no_user_label.grid(row=0, column=0, sticky='n')
        else:

            if int(amount) > int(balance):
                print('y dont have money')
                no_money_label = tk.Label(transfer_frame,
                                          text='You do not have enough money to make the transfer',
                                          font=self.disclaimer_font, background=transfer_bg,
                                          foreground=interface_fg_color)
                no_money_label.grid(row=0, column=0, sticky='n', pady=320)

            else:
                balance_after_transfer_user = int(balance) - int(amount)
                self.cursor.execute(f"UPDATE bank_user SET balance = {balance_after_transfer_user} "
                                    f"WHERE login ='{self.name_user}'")
                self.cursor.execute(f"UPDATE bank_user SET balance = balance + {int(amount)} WHERE login ='{log}'")
                self.connection.commit()
                is_done = True

            if is_done is True:
                print('done')
                done_label = tk.Label(transfer_frame,
                                      text='Transfer done',
                                      font=self.disclaimer_font, background=transfer_bg, foreground=interface_fg_color)
                done_label.grid(row=0, column=0, sticky='n', pady=350)
                self.receiver_confirm_button.grid_forget()

    def withdraw(self):
        withdraw_amount = self.withdraw_amount.get()
        balance = None
        self.cursor.execute(f"SELECT balance FROM bank_user WHERE login = '{self.name_user}'")
        balances = self.cursor.fetchall()
        for i in balances:
            balance = i[0]
        if int(withdraw_amount) > int(balance):
            print('y dont have money')
            no_money = tk.Label(withdraw_frame,
                                text='You do not have enough money to withdraw',
                                font=self.disclaimer_font, background=withdraw_bg, border=0,
                                foreground=interface_fg_color)
            no_money.grid(row=0, column=0, sticky='n', pady=310)
        else:
            print('yes its working')

            self.cursor.execute(f"UPDATE bank_user SET balance = balance - {withdraw_amount} "
                                f"WHERE login = '{self.name_user}'")
            self.connection.commit()

            self.done_label_withdraw = tk.Label(withdraw_frame, text='DONE', font=self.disclaimer_font,
                                                foreground=interface_fg_color, background=withdraw_bg, border=0)
            self.done_label_withdraw.grid(row=0, column=0, sticky='n', pady=340)
            self.withdraw_confirm_button.grid_forget()

   
    def load_title_frame(self):
        self.clear_frame(sing_frame)
        title_frame.tkraise()
        title_frame.grid_propagate(False)

        im = tk.PhotoImage(file='icon.png')
        root.iconphoto(False, im)

        logo_img = ImageTk.PhotoImage(file="a2.png")
        logo_widget = tk.Label(title_frame, image=logo_img, bg=bg_color_1)
        logo_widget.image = logo_img
        logo_widget.grid(column=0, row=0, pady=160)

        head_label = tk.Label(title_frame, text='HELLO', font=self.font,
                              background=bg_color_1, foreground='#C0C0C0')
        head_label.grid(row=0, column=0, sticky='n', padx=385, pady=50)
        info_sing_label = tk.Label(title_frame, text='Are you a new user?',
                                   font=self.info_font, foreground='#C0C0C0', background=bg_color_1)
        info_sing_label.grid(row=0, column=0, sticky='nw', padx=150, pady=110)
        info_login_label = tk.Label(title_frame, text='Are you with us already?',
                                    font=self.info_font, foreground='#C0C0C0', background=bg_color_1)
        info_login_label.grid(row=0, column=0, sticky='ne', padx=110, pady=110)

        sing_button = tk.Button(title_frame, font=self.button_font, text='Sing UP',
                                foreground=bg_color_1, background='#C0C0C0', command=lambda: self.load_sing_frame())
        sing_button.grid(row=0, column=0, sticky='nw', pady=140, padx=250)

        login_button = tk.Button(title_frame, font=self.button_font, text='Login IN',
                                 foreground=bg_color_1, background='#C0C0C0', command=lambda: self.load_login_frame())
        login_button.grid(row=0, column=0, sticky='ne', pady=140, padx=250)

        '''disclaimers'''

        disclaimer_label = tk.Label(title_frame, text='© 2022 EAST BANK',
                                    font=self.disclaimer_font, background=bg_color_1)
        disclaimer_label.grid(row=0, column=0, sticky='sw', padx=300)
        disclaimer_label2 = tk.Label(title_frame, text='Privacy policy',
                                     font=self.disclaimer_font, background=bg_color_1)
        disclaimer_label2.grid(row=0, column=0, sticky='se', padx='300')
        disclaimer_label3 = tk.Label(title_frame, text='BIC Code (Swift): EASTBANKPLEN',
                                     font=self.disclaimer_font1, background=bg_color_1)
        disclaimer_label3.grid(row=0, column=0, sticky='sw', padx='0')

    def load_sing_frame(self):
        self.clear_frame(title_frame)
        sing_frame.tkraise()
        sing_frame.grid_propagate(False)

        head_labels = tk.Label(sing_frame, text='SING UP', font=self.font, foreground=bg_color_1, background=bg_color_2)
        head_labels.grid(row=0, column=0, sticky='ne', padx=350)

        name_label = tk.Label(sing_frame, text='Name',
                              font=self.disclaimer_font, background=bg_color_2, foreground=bg_color_1)
        name_label.grid(row=1, column=0)

        self.name_entry = tk.Entry(sing_frame, background=bg_color_1, foreground='white', )
        self.name_entry.grid(row=2, column=0, pady=10)

        surname_label = tk.Label(sing_frame, text='Surname',
                                 font=self.disclaimer_font, background=bg_color_2, foreground=bg_color_1)
        surname_label.grid(row=3, column=0)

        self.surname_entry = tk.Entry(sing_frame, background=bg_color_1, foreground='white', )
        self.surname_entry.grid(row=4, column=0, pady=10)

        age_label = tk.Label(sing_frame, text='Age',
                             font=self.disclaimer_font, background=bg_color_2, foreground=bg_color_1)
        age_label.grid(row=5, column=0)

        self.age_entry = tk.Entry(sing_frame, background=bg_color_1, foreground='white', )
        self.age_entry.grid(row=6, column=0, pady=10)

        login_label = tk.Label(sing_frame, text='Login',
                               font=self.disclaimer_font, background=bg_color_2, foreground=bg_color_1)
        login_label.grid(row=7, column=0)

        self.login_entry = tk.Entry(sing_frame, background=bg_color_1, foreground='white', )
        self.login_entry.grid(row=8, column=0, pady=10)

        password_label = tk.Label(sing_frame, text='Password',
                                  font=self.disclaimer_font, background=bg_color_2, foreground=bg_color_1)
        password_label.grid(row=9, column=0)

        self.password_entry = tk.Entry(sing_frame, background=bg_color_1, foreground='white', )
        self.password_entry.grid(row=10, column=0, pady=10)

        self.confirm_data_button = tk.Button(sing_frame, text='Confirm',
                                             font=self.button_font, foreground=bg_color_2, background=bg_color_1,
                                             command=lambda: [self.getting_data(), self.delete_button()])
        self.confirm_data_button.grid(row=11, column=0, sticky='nw', pady=20, padx=280)
        back_data_button = tk.Button(sing_frame, text='Back',
                                     font=self.button_font, foreground=bg_color_2, background=bg_color_1,
                                     command=lambda: self.load_title_frame())
        back_data_button.grid(row=11, column=0, sticky='ne', pady=20, padx=320)

        """disclaimers"""
        disclaimer_labels = tk.Label(sing_frame, text='© 2022 EAST BANK',
                                     font=self.disclaimer_font, background=bg_color_2)
        disclaimer_labels.grid(row=11, column=0, sticky='sw', padx=300, pady=200)
        disclaimer_label2s = tk.Label(sing_frame, text='Privacy policy',
                                      font=self.disclaimer_font, background=bg_color_2)
        disclaimer_label2s.grid(row=11, column=0, sticky='se', padx='300', pady=200)
        disclaimer_label3s = tk.Label(sing_frame, text='BIC Code (Swift): EASTBANKPLEN',
                                      font=self.disclaimer_font1, background=bg_color_2)
        disclaimer_label3s.grid(row=11, column=0, sticky='sw', padx='0', pady=200)

    def load_login_frame(self):
        self.clear_frame(title_frame)
        login_frame.tkraise()
        login_frame.grid_propagate(False)

        head_labels = tk.Label(login_frame, text='LOGIN IN', font=self.font, foreground=bg_color_1,
                               background=bg_color_2)
        head_labels.grid(row=0, column=0, sticky='ne', padx=350)

        login_label = tk.Label(login_frame, text='Login',
                               font=self.disclaimer_font, background=bg_color_2, foreground=bg_color_1)
        login_label.grid(row=7, column=0)

        self.login_entry_login = tk.Entry(login_frame, background=bg_color_1, foreground='white',
                                          font=self.login_font, border=0)
        self.login_entry_login.grid(row=8, column=0, pady=10)

        password_label = tk.Label(login_frame, text='Password',
                                  font=self.disclaimer_font, background=bg_color_2, foreground=bg_color_1)
        password_label.grid(row=9, column=0)

        self.password_entry_login = tk.Entry(login_frame, background=bg_color_1,
                                             foreground='white', font=self.login_font)
        self.password_entry_login.grid(row=10, column=0, pady=10)

        confirm_data_button = tk.Button(login_frame, text='Confirm',
                                        font=self.button_font, foreground=bg_color_2, background=bg_color_1,
                                        command=lambda: self.checking_data())
        confirm_data_button.grid(row=11, column=0, sticky='nw', pady=20, padx=300)

        confirm_data_button = tk.Button(login_frame, text='Back',
                                        font=self.button_font, foreground=bg_color_2, background=bg_color_1,
                                        command=lambda: self.load_title_frame())
        confirm_data_button.grid(row=11, column=0, sticky='ne', pady=20, padx=320)

    def load_interface(self):
        self.clear_frame(login_frame)
        interface_frame.tkraise()
        interface_frame.grid_propagate(False)

        head_label = tk.Label(interface_frame, text=f'HELLO {self.name_user} ',
                              font=self.font, background=interface_color, foreground=interface_fg_color)
        head_label.grid(row=0, column=0, sticky='nw', padx=180, pady=70)
        print(self.name_user)
        info_label = tk.Label(interface_frame, text='What would you like to do?',
                              font=self.disclaimer_font, background=interface_color, foreground=interface_fg_color)
        info_label.grid(row=0, column=0, sticky='n', padx=350, pady=150)

        payment_button = tk.Button(interface_frame, text='PAYMENT',
                                   font=self.button_font, background=interface_color,
                                   foreground=interface_fg_color, command=lambda: self.load_transfer_frame())
        payment_button.grid(row=0, column=0, sticky='nw', pady=200, padx=280)

        withdraw_button = tk.Button(interface_frame, text='WITHDRAW',
                                    font=self.button_font, background=interface_color,
                                    foreground=interface_fg_color, command=lambda: self.load_withdraw_frame())
        withdraw_button.grid(row=0, column=0, sticky='ne', pady=200, padx=280)

        balance_label = tk.Label(interface_frame, text='YOUR BALANCE  ',
                                 font=self.font, foreground=interface_fg_color, background=interface_color)
        balance_label.grid(row=0, column=0, sticky='nw', pady=300, padx=180)

        amount_balance = tk.Label(interface_frame,
                                  text=f'{self.balance(self.name_user)}',
                                  font=self.balance_font, foreground=interface_fg_color, background=interface_color)
        amount_balance.grid(row=0, column=0, sticky='n', pady=350, padx=260)

        """REFRESH BUTTON here"""
        ref = tk.Button(interface_frame, text='refresh', font=self.disclaimer_font,
                        foreground=interface_fg_color, background=interface_color)
        ref.grid(row=0, column=0, sticky='ne', pady=20, padx=50)

        back_button = tk.Button(interface_frame, text='LOGOUT',
                                font=self.button_font, foreground=interface_fg_color,
                                background=interface_color, command=lambda: self.logout())
        back_button.grid(row=0, column=0, sticky='ne', pady=550, padx=10)

        '''Disclaimers'''

        disclaimer_label = tk.Label(interface_frame, text='© 2022 EAST BANK',
                                    font=self.disclaimer_font,
                                    background=interface_color, foreground=interface_fg_color)
        disclaimer_label.grid(row=1, column=0, sticky='sw', padx=300, pady=70)
        disclaimer_label2 = tk.Label(interface_frame, text='Privacy policy',
                                     font=self.disclaimer_font,
                                     background=interface_color, foreground=interface_fg_color)
        disclaimer_label2.grid(row=1, column=0, sticky='se', padx='300', pady=70)
        disclaimer_label3 = tk.Label(interface_frame, text='BIC Code (Swift): EASTBANKPLEN',
                                     font=self.disclaimer_font1,
                                     background=interface_color, foreground=interface_fg_color)
        disclaimer_label3.grid(row=1, column=0, sticky='sw', padx='0', pady=70)

    def load_transfer_frame(self):
        self.clear_frame(interface_frame)
        transfer_frame.tkraise()
        transfer_frame.grid_propagate(False)

        head_label = tk.Label(transfer_frame, text='Transfer',
                              font=self.font, background=transfer_bg, foreground=interface_fg_color)
        head_label.grid(row=0, column=0, sticky='n', pady=50, padx=350)

        receiver_label = tk.Label(transfer_frame, text='Receiver',
                                  font=self.disclaimer_font, background=transfer_bg, foreground=interface_fg_color)
        receiver_label.grid(row=0, column=0, sticky='n', pady=120, padx=300)

        self.receiver_entry = tk.Entry(transfer_frame, background=transfer_entry, foreground=interface_fg_color,
                                       border=0, font=self.transfer_font)
        self.receiver_entry.grid(row=0, column=0, sticky='n', pady=140, padx=300)
        transfer_amount_label = tk.Label(transfer_frame,
                                         text='Transfer amount', font=self.disclaimer_font,
                                         foreground=interface_fg_color, background=transfer_bg)
        transfer_amount_label.grid(row=0, column=0, pady=190, padx=280, sticky='n')

        self.receiver_entry_amount = tk.Entry(transfer_frame,
                                              background=transfer_entry, foreground=interface_fg_color,
                                              border=0, font=self.transfer_font)
        self.receiver_entry_amount.grid(row=0, column=0, pady=220, padx=300, sticky='n')

        self.receiver_confirm_button = tk.Button(transfer_frame, text='Confirm',
                                                 font=self.button_font,
                                                 foreground=interface_fg_color, background=transfer_entry,
                                                 border=0, command=lambda: self.transfer())
        self.receiver_confirm_button.grid(row=0, column=0, pady=260, padx=300, sticky='n', )
        back_button = tk.Button(transfer_frame, text='BACK',
                                font=self.button_font,
                                foreground=interface_fg_color, background=transfer_entry,
                                border=0, command=lambda: self.load_interface())
        back_button.grid(row=0, column=0, sticky='n', pady=400)

    def load_withdraw_frame(self):
        self.clear_frame(interface_frame)
        withdraw_frame.tkraise()
        withdraw_frame.grid_propagate(False)

        head_label = tk.Label(withdraw_frame, text='Withdraw',
                              font=self.font, background=withdraw_bg, foreground=interface_fg_color)
        head_label.grid(row=0, column=0, sticky='n', pady=50, padx=350)

        withdraw_amount_label = tk.Label(withdraw_frame, text='Withdraw funds',
                                         font=self.disclaimer_font, background=withdraw_bg,
                                         foreground=interface_fg_color, border=0)
        withdraw_amount_label.grid(row=0, column=0, sticky='n', pady=150)

        self.withdraw_amount = tk.Entry(withdraw_frame, background='#470e27',
                                        foreground=interface_fg_color, border=0, font=self.withdraw_font, )
        self.withdraw_amount.grid(row=0, column=0, sticky='n', pady=170)

        self.withdraw_confirm_button = tk.Button(withdraw_frame, text='Confirm',
                                                 font=self.button_font, background='#470e27',
                                                 foreground=interface_fg_color, border=0,
                                                 command=lambda: self.withdraw())
        self.withdraw_confirm_button.grid(row=0, column=0, sticky='nw', pady=240, padx=280)

        back_button = tk.Button(withdraw_frame, text='BACK',
                                font=self.button_font,
                                foreground=interface_fg_color, background='#470e27',
                                border=0, command=lambda: self.load_interface())
        back_button.grid(row=0, column=0, sticky='ne', pady=240, padx=300)

    @staticmethod
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def delete_button(self):
        self.confirm_data_button.grid_forget()


root = tk.Tk()
root.title('Login')

title_frame = tk.Frame(root, width=900, height=600, background=bg_color_1)
title_frame.grid(row=0, column=0, sticky="nesw")
sing_frame = tk.Frame(root, background=bg_color_2)
sing_frame.grid(row=0, column=0, sticky="nesw")
login_frame = tk.Frame(root, background=bg_color_2)
login_frame.grid(row=0, column=0, sticky='nesw')
interface_frame = tk.Frame(root, background=interface_color, )
interface_frame.grid(row=0, column=0, sticky='nesw')
transfer_frame = tk.Frame(root, background=transfer_bg)
transfer_frame.grid(row=0, column=0, sticky='nesw')
withdraw_frame = tk.Frame(root, background=withdraw_bg)
withdraw_frame.grid(row=0, column=0, sticky='nesw')

d = Gui(getenv('DB_NAME'))
d.load_title_frame()

query = '''CREATE TABLE bank_user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, age DATE, login TEXT,
         password TEXT, balance INTEGER) '''


print(f'to jest entry login --->>{d.login_entry_login}')

root.mainloop()

"""make it cleaner"""
