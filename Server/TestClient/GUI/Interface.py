import datetime
import io

import customtkinter
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askopenfilenames
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk

from PROJECT.Utils.Event import Event

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.app_name = "Air DND"

        self.active = True

        self.map = None

        self.on_login = Event()
        self.on_logout = Event()
        self.on_signup = Event()
        self.on_map_create = Event()
        self.on_get_own_offers = Event()
        self.on_create_offer = Event()
        self.on_get_own_purchases = Event()
        self.on_update_search = Event()
        self.on_dispute_purchase = Event()
        self.on_review_purchase = Event()
        self.on_get_admin = Event()
        self.on_change_date = Event()
        self.on_close = Event()

        self.logo_path = 'GUI\logo.png'

        self.connecting_frame = None

        self.title(self.app_name)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        logo = PhotoImage(file=self.logo_path)
        self.iconphoto(False, logo)

        self.configure(background='gray10')

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0, 2, 3, 4, 5), weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5), weight=0)

    def connecting(self):
        """
        Shows connecting screen
        """
        self.current_frame_name = "CONNECTING"

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

        self.connecting_frame = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.connecting_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky='nswe')

        self.connecting_frame.grid_columnconfigure((0, 2), weight=1)
        self.connecting_frame.grid_rowconfigure(3, weight=1)
        self.connecting_frame.grid_rowconfigure((0, 5), weight=100)

        tk_image = ImageTk.PhotoImage(Image.open(self.logo_path).resize((250, 250)))
        image = Label(self.connecting_frame, image=tk_image)  # font name and size in px
        image.image = tk_image
        image.grid(row=1, column=1, pady=10, padx=10)

        title_label = customtkinter.CTkLabel(master=self.connecting_frame,
                                             text=self.app_name,
                                             text_font=("Roboto Medium", -36))  # font name and size in px
        title_label.grid(row=2, column=1, pady=10, padx=10)

        connecting_label = customtkinter.CTkLabel(master=self.connecting_frame,
                                                  text="Connecting...",
                                                  text_color='#1ba17b',
                                                  text_font=("Roboto Medium", -44))  # font name and size in px
        connecting_label.grid(row=4, column=1, pady=50, padx=30)

        self.mainloop()

    def start(self):
        """
        Builds the menu and goes to home page
        """
        if self.connecting_frame: self.connecting_frame.destroy()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_right = customtkinter.CTkFrame(master=self)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(50, weight=1)

        tk_image = ImageTk.PhotoImage(Image.open(self.logo_path).resize((100, 100)))

        self.image = Label(self.frame_left, image=tk_image)  # font name and size in px
        self.image.image = tk_image
        self.image.grid(row=0, column=0, pady=10, padx=10)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text=self.app_name,
                                              text_font=("Roboto Medium", -16))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.home_button = customtkinter.CTkButton(master=self.frame_left,
                                                   text="Home",
                                                   fg_color=("gray75", "gray30"),
                                                   command=self.home_frame)
        self.home_button.grid(row=2, column=0, pady=10, padx=20)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Login & SignUp",
                                                fg_color=("gray75", "gray30"),
                                                command=self.log_in_frame)
        self.button_1.grid(row=3, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Map",
                                                fg_color=("gray75", "gray30"),
                                                command=self.map_frame)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="My Offers",
                                                fg_color=("gray75", "gray30"),
                                                command=self.own_offers_frame)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="My Purchases",
                                                fg_color=("gray75", "gray30"),
                                                command=self.own_purchases_frame)

        self.admin_button = customtkinter.CTkButton(master=self.frame_left,
                                                    text="Admin",
                                                    text_color='blue',
                                                    fg_color=("gray75", "gray30"),
                                                    command=self.admin_info_frame)

        self.menu_buttons = [self.home_button, self.button_1, self.button_2, self.button_3, self.button_4]

        self.home_frame()

        self.frame_left.grid(row=0, column=0, sticky="nswe")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        if not self.connecting_frame: self.mainloop()

    def set_logged_in(self, logged, admin=False):
        """
        Enables/Disables parts of the menu depended of whether the user is logged in and whether he
        is an admin
        """
        if not logged:
            self.menu_buttons[1].configure(text=r"Login & SignUp",
                                           fg_color=("gray75", "gray30"),
                                           text_color="gray99",
                                           command=self.log_in_frame)
            for btn in self.menu_buttons[2:]:
                btn.grid_forget()
            self.admin_button.grid_forget()
        else:
            self.menu_buttons[1].configure(text="Logout",
                                           text_color='red',
                                           command=self.on_logout)

            for i, btn in enumerate(self.menu_buttons[2:]):
                btn.grid(row=4 + i, column=0, pady=10, padx=20)
            if admin: self.admin_button.grid(row=5 + i, column=0, pady=10, padx=20)

    def frame_switch(button=None):
        """
        Decorator used to destroy last frame and select buttons
        """

        def decorator(func):
            def applicator(self, *args, **kwargs):
                for b in self.menu_buttons: b.configure(state=NORMAL,
                                                        fg_color=("gray75", "gray30"))
                self.admin_button.configure(state=NORMAL, fg_color=("gray75", "gray30"))
                if button is not None:
                    if button == 'admin':
                        self.admin_button.configure(state=DISABLED, fg_color='#0a694e')
                    else:
                        self.menu_buttons[button].configure(state=DISABLED, fg_color='#0a694e')

                last_frame = self.frame_right
                self.frame_right = customtkinter.CTkFrame(master=self)
                val = func(self, *args, **kwargs)
                self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
                last_frame.grid_forget()
                last_frame.destroy()
                return val

            return applicator

        return decorator

    @frame_switch(button=0)
    def home_frame(self):
        """
        Displays home page
        """
        self.current_frame_name = 'HOME'
        tk_image = ImageTk.PhotoImage(Image.open(self.logo_path).resize((500, 500)))

        self.home_image = Label(self.frame_right, image=tk_image)  # font name and size in px
        self.home_image.image = tk_image
        self.home_image.pack(expand=1)

        self.minsize(self.WIDTH, self.HEIGHT + 60)

    @frame_switch(button=1)
    def sign_up_frame(self):
        """
        Displays sign up page
        """
        self.current_frame_name = 'SIGNUP'
        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1), weight=1)
        self.frame_right.rowconfigure(10, weight=10)
        self.frame_right.columnconfigure((1, 2), weight=1)
        self.frame_right.columnconfigure(0, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=3, rowspan=1, pady=20, padx=20, sticky="we")

        # ============ frame_info ============

        # configure grid layout (1x1)

        self.frame_info.columnconfigure((0, 3), weight=1)
        self.frame_info.rowconfigure((0, 1), weight=1)

        self.signup_error_label = None

        self.title_1 = customtkinter.CTkLabel(master=self.frame_info,
                                              text="Sign Up Page",
                                              text_font=("Roboto Medium", -60),
                                              height=100,
                                              fg_color=("white", "gray38"),  # <- custom tuple-color
                                              justify=LEFT)
        self.title_1.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="we")

        self.sub_title = customtkinter.CTkLabel(master=self.frame_info,
                                                text="Already have an account?",
                                                text_font=("Roboto Medium", -20),  # <- custom tuple-color
                                                justify=LEFT)
        self.sub_title.grid(row=1, column=1, columnspan=1, pady=10, padx=0, sticky="we")

        self.goto_login_frame_button = customtkinter.CTkButton(master=self.frame_info,
                                                               text="Login",
                                                               text_font=("Roboto Medium", -20),
                                                               fg_color=("gray75", "gray30"),
                                                               width=70,
                                                               command=self.log_in_frame)
        self.goto_login_frame_button.grid(row=1, column=2, columnspan=1, pady=10, padx=0, sticky="we")

        self.username_label = customtkinter.CTkLabel(master=self.frame_right,
                                                     text="Username",
                                                     text_font=("Roboto Medium", -22),
                                                     fg_color=("gray92", "gray30"))
        self.username_label.grid(row=2, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        self.username_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                     width=120,
                                                     placeholder_text="Enter username here...")
        self.username_entry.grid(row=3, column=0, columnspan=3, pady=5, padx=20, sticky="we")

        self.email_label = customtkinter.CTkLabel(master=self.frame_right,
                                                  text="Email",
                                                  text_font=("Roboto Medium", -22),
                                                  fg_color=("gray92", "gray30"))
        self.email_label.grid(row=4, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        self.email_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                  width=120,
                                                  placeholder_text="Enter email here...")
        self.email_entry.grid(row=5, column=0, columnspan=3, pady=5, padx=20, sticky="we")

        self.password_label = customtkinter.CTkLabel(master=self.frame_right,
                                                     text="Password",
                                                     text_font=("Roboto Medium", -22),
                                                     fg_color=("gray92", "gray30"))
        self.password_label.grid(row=6, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        self.password_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                     width=120,
                                                     placeholder_text="Enter password here...")
        self.password_entry.grid(row=7, column=0, columnspan=3, pady=5, padx=20, sticky="we")

        self.password_confirmation_label = customtkinter.CTkLabel(master=self.frame_right,
                                                                  text="Password Confirmation",
                                                                  text_font=("Roboto Medium", -22),
                                                                  fg_color=("gray92", "gray30"))
        self.password_confirmation_label.grid(row=8, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        self.password_confirmation_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                                  width=120,
                                                                  placeholder_text="Enter password again here...")
        self.password_confirmation_entry.grid(row=9, column=0, columnspan=3, pady=5, padx=20, sticky="we")

        def sign_up():
            if self.signup_error_label:
                self.signup_error_label.grid_forget()
                self.signup_error_label.destroy()
                self.signup_error_label = None
            username = self.username_entry.get()
            email = self.email_entry.get()
            password = self.password_entry.get()
            password_conf = self.password_confirmation_entry.get()
            if len(username) > 20:
                self.display_signup_error('Username is too long (must be no more than 20 characters)', 'red')
            elif len(email) > 30:
                self.display_signup_error('Email is too long (must be no more than 30 characters)', 'red')
            elif '@' not in email or '.' not in email:
                self.display_signup_error('Invalid Email', 'red')
            elif len(password) > 20:
                self.display_signup_error('Password is too long (must be no more than 20 characters)', 'red')
            elif not password == password_conf:
                self.display_signup_error('Password confirmation does not match the Password', 'red')
            else:
                self.on_signup(username, email, password)

        self.create_offer_button = customtkinter.CTkButton(
            master=self.frame_right,
            text="Sign Up",
            text_font=("Roboto Medium", -40),
            fg_color=("gray75", "gray30"),
            height=60,
            command=sign_up
        )

        self.create_offer_button.grid(row=12, column=0, columnspan=3, pady=20, padx=20, sticky="we")

        self.minsize(self.WIDTH, self.HEIGHT + 140)

    def display_signup_error(self, error: str, color):
        """
        Displays errors in the sign up page
        :param error: error to display
        :param color: color of error
        """
        if self.current_frame_name == 'SIGNUP':
            self.signup_error_label = customtkinter.CTkLabel(master=self.frame_right,
                                                             text=error,
                                                             text_color=color,
                                                             text_font=("Roboto Medium", -16))
            self.signup_error_label.grid(row=11, column=0, columnspan=3, pady=5, padx=20, sticky="we")

    @frame_switch(button=1)
    def log_in_frame(self):
        """
        Displays login page
        """
        self.current_frame_name = 'LOGIN'

        self.login_error_label = None
        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 7), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((1, 2), weight=1)
        self.frame_right.columnconfigure(0, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=3, rowspan=1, pady=20, padx=20, sticky="we")

        # ============ frame_info ============

        # configure grid layout (1x1)

        self.frame_info.columnconfigure((0, 3), weight=1)
        self.frame_info.rowconfigure((0, 1), weight=1)

        self.title_1 = customtkinter.CTkLabel(master=self.frame_info,
                                              text="Login Page",
                                              text_font=("Roboto Medium", -60),
                                              height=100,
                                              fg_color=("white", "gray38"),  # <- custom tuple-color
                                              justify=LEFT)
        self.title_1.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="we")

        self.sub_title = customtkinter.CTkLabel(master=self.frame_info,
                                                text="Don't have an account?",
                                                text_font=("Roboto Medium", -20),  # <- custom tuple-color
                                                justify=LEFT)
        self.sub_title.grid(row=1, column=1, columnspan=1, pady=10, padx=0, sticky="we")

        self.create_offer_button = customtkinter.CTkButton(master=self.frame_info,
                                                           text="Sign Up",
                                                           text_font=("Roboto Medium", -20),
                                                           fg_color=("gray75", "gray30"),
                                                           width=70,
                                                           command=self.sign_up_frame)
        self.create_offer_button.grid(row=1, column=2, columnspan=1, pady=10, padx=0, sticky="we")

        self.email_label = customtkinter.CTkLabel(master=self.frame_right,
                                                  text="Email",
                                                  text_font=("Roboto Medium", -22),
                                                  fg_color=("gray92", "gray30"))
        self.email_label.grid(row=2, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        self.email_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                  width=120,
                                                  placeholder_text="Enter email here...")
        self.email_entry.grid(row=3, column=0, columnspan=3, pady=5, padx=20, sticky="we")

        self.password_label = customtkinter.CTkLabel(master=self.frame_right,
                                                     text="Password",
                                                     text_font=("Roboto Medium", -22),
                                                     fg_color=("gray92", "gray30"))
        self.password_label.grid(row=5, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        self.password_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                     width=120,
                                                     placeholder_text="Enter password here...")
        self.password_entry.grid(row=6, column=0, columnspan=3, pady=5, padx=20, sticky="we")

        def login():
            if self.login_error_label:
                self.login_error_label.grid_forget()
                self.login_error_label.destroy()
                self.login_error_label = None
            self.on_login(self.email_entry.get(), self.password_entry.get())

        self.login_button = customtkinter.CTkButton(master=self.frame_right,
                                                    text="Login",
                                                    text_font=("Roboto Medium", -40),
                                                    fg_color=("gray75", "gray30"),
                                                    height=60,
                                                    command=login
                                                    )
        self.login_button.grid(row=9, column=0, columnspan=3, pady=20, padx=20, sticky="we")

        self.minsize(self.WIDTH, self.HEIGHT)

    def display_login_error(self, error: str, color):
        """
        Displays errors in the login page
        :param error: error to display
        :param color: color of error
        """
        if self.current_frame_name == 'LOGIN':
            self.login_error_label = customtkinter.CTkLabel(master=self.frame_right,
                                                            text=error,
                                                            text_color=color,
                                                            text_font=("Roboto Medium", -16))
            self.login_error_label.grid(row=8, column=0, columnspan=3, pady=0, padx=20, sticky="we")

    @frame_switch(button=2)
    def map_frame(self, preval=''):
        """
        Displays map page and creates the map
        """
        self.current_frame_name = 'MAP'

        self.offers = None

        self.search_var = StringVar()
        if preval: self.search_var.set(preval)

        self.frame_right.grid_rowconfigure(3, weight=1)
        self.frame_right.grid_rowconfigure((0, 4), minsize=20)
        self.frame_right.grid_rowconfigure((0, 1), weight=0)
        self.frame_right.grid_columnconfigure((0, 2, 5), minsize=20, weight=0)
        self.frame_right.grid_columnconfigure((3, 4), minsize=40, weight=0)
        self.frame_right.grid_columnconfigure(1, weight=1)

        self.search_entry = customtkinter.CTkEntry(master=self.frame_right, textvariable=self.search_var,
                                                   corner_radius=0)
        self.search_entry.grid(row=1, column=3, columnspan=2, padx=0, pady=0, sticky=EW)
        self.search_entry.bind('<Return>', lambda x: self.on_update_search())
        self.search_entry.bind("<KeyRelease>", lambda x: self.on_update_search())

        def press_button(btn):
            if btn == 1:
                self.sort_mode = 1
                self.sort_by_price_button.configure(state=DISABLED)
                self.sort_by_distance_button.configure(state=NORMAL)
            else:
                self.sort_mode = 2
                self.sort_by_price_button.configure(state=NORMAL)
                self.sort_by_distance_button.configure(state=DISABLED)
            self.on_update_search()

        self.sort_by_price_button = customtkinter.CTkButton(master=self.frame_right,
                                                            text='Cheapest',
                                                            command=lambda: press_button(1),
                                                            corner_radius=0)
        self.sort_by_price_button.grid(row=2, column=3, columnspan=1, padx=0, pady=0, sticky=EW)

        self.sort_by_distance_button = customtkinter.CTkButton(master=self.frame_right,
                                                               text='Closest',
                                                               command=lambda: press_button(2),
                                                               corner_radius=0)
        self.sort_by_distance_button.grid(row=2, column=4, columnspan=1, padx=0, pady=0, sticky=EW)

        self.sort_mode = 1
        self.sort_by_price_button.configure(state=DISABLED)
        self.sort_by_distance_button.configure(state=NORMAL)

        self.search_listbox = Listbox(master=self.frame_right)
        self.search_listbox.bind('<<ListboxSelect>>', lambda _: self.focus_on_map())
        self.search_listbox.grid(row=3, column=3, columnspan=2, padx=0, pady=0, sticky=NSEW)

        self.on_map_create(self.frame_right, preval)
        self.map.grid(row=1, column=1, rowspan=3, padx=0, pady=0, sticky=NSEW)

    def update_selected(self):
        """
        Selects the searched value in case of an offer update
        """
        for i in range(self.search_listbox.size()):
            if self.search_listbox.get(i) == self.search_var.get():
                self.search_listbox.selection_set(i)
                break
        self.focus_on_map()

    def focus_on_map(self):
        """
        Focuses on the selected offer in the map
        """
        if not self.offers: return
        try:
            name = self.search_listbox.get(self.search_listbox.curselection())
        except:
            return
        offer = list(filter(lambda o: o['name'] == name, self.offers))
        if not offer: return
        offer = offer[0]
        try:
            self.map.set_position(float(offer['x']), float(offer['y']))
            self.map.set_zoom(15)
        except:
            pass
        try:
            self.map.set_position(float(offer['x']), float(offer['y']))
            self.map.set_zoom(15)
        except:
            pass

    def update_search_listbox(self, offers):
        """
        Updates offers in listbox
        :param offers: new offers to update with
        """
        self.offers = offers
        self.search_listbox.delete(0, END)

        for offer in filter(lambda o: o['Triggered'], offers):
            self.search_listbox.insert(END, offer['name'])

    @frame_switch(button=3)
    def own_offers_frame(self):
        """
        Displays my offers page
        """
        self.current_frame_name = 'MYOFFERS'

        self.frame_right.grid_columnconfigure((0, 2), weight=100)
        self.frame_right.grid_rowconfigure((0, 2), weight=100)

        self.goto_create_offer_button = customtkinter.CTkButton(master=self.frame_right,
                                                                text="Create an Offer",
                                                                text_font=("Roboto Medium", -36),
                                                                command=self.create_offer_frame)
        self.goto_create_offer_button.grid(row=3, column=1, pady=10, padx=20)

        self.on_get_own_offers()

    def update_own_offers(self, own_offers):
        """
        Displays all of the information on the my offers page
        :param own_offers: received offers
        """
        if self.current_frame_name == 'MYOFFERS':
            if not own_offers:
                lbl = customtkinter.CTkLabel(master=self.frame_right,
                                             text="You have made 0 offers",
                                             text_color='#d45a22',
                                             text_font=("Roboto Medium", -36))
                lbl.grid(row=1, column=1, pady=10, padx=10)
            else:
                self.purchases_frame = customtkinter.CTkFrame(master=self.frame_right)

                main_font_size = -10

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Name",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=0, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Price Per Day",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=1, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Start Date",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=2, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="End Date",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=3, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Conditions",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=4, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Income",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=5, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="View",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=6, columnspan=1, pady=4, padx=2, sticky="nswe")

                def create_view_button(this_offer):
                    view_button = customtkinter.CTkButton(master=self.purchases_frame,
                                                          text="View",
                                                          text_font=("Roboto Medium", main_font_size),
                                                          fg_color=("gray75", "gray30"),
                                                          width=20,
                                                          command=lambda: self.map_frame(this_offer['name'])
                                                          if this_offer.get('name', None) else None)

                    view_button.grid(row=i + 1, column=6, columnspan=1, pady=2, padx=4, sticky="nswe")

                for i, offer in enumerate(own_offers):
                    name_lbl = customtkinter.CTkLabel(master=self.purchases_frame,
                                                      text=f"{offer.get('name', 'NAN')}",
                                                      text_font=("Roboto Medium", main_font_size),
                                                      fg_color=("gray92", "gray30"))
                    name_lbl.grid(row=i + 1, column=0, pady=2, padx=2, sticky="nswe")

                    price_per_day_label = customtkinter.CTkLabel(master=self.purchases_frame,
                                                                 text=f"{offer.get('price_per_day', 'NAN')}",
                                                                 text_font=("Roboto Medium", main_font_size),
                                                                 fg_color=("gray92", "gray30"))
                    price_per_day_label.grid(row=i + 1, column=1, columnspan=1, pady=2, padx=2, sticky="nswe")

                    start_date_label = customtkinter.CTkLabel(master=self.purchases_frame,
                                                              text=f"{offer.get('start_date', 'NAN')}",
                                                              text_font=("Roboto Medium", main_font_size),
                                                              fg_color=("gray92", "gray30"))
                    start_date_label.grid(row=i + 1, column=2, columnspan=1, pady=2, padx=2, sticky="nswe")

                    end_date_label = customtkinter.CTkLabel(master=self.purchases_frame,
                                                            text=f"{offer.get('end_date', 'NAN')}",
                                                            text_font=("Roboto Medium", main_font_size),
                                                            fg_color=("gray92", "gray30"))
                    end_date_label.grid(row=i + 1, column=3, columnspan=1, pady=2, padx=2, sticky="nswe")

                    conditions_label = customtkinter.CTkLabel(master=self.purchases_frame,
                                                              text=f"{offer.get('conditions', 'NAN')}",
                                                              text_font=("Roboto Medium", main_font_size),
                                                              fg_color=("gray92", "gray30"))
                    conditions_label.grid(row=i + 1, column=4, columnspan=1, pady=2, padx=2, sticky="nswe")

                    income_label = customtkinter.CTkLabel(master=self.purchases_frame,
                                                          text=f"{offer.get('total_income', '0')}",
                                                          text_font=("Roboto Medium", main_font_size),
                                                          fg_color=("gray92", "gray30"))
                    income_label.grid(row=i + 1, column=5, columnspan=1, pady=2, padx=2, sticky="nswe")

                    create_view_button(offer)

                self.purchases_frame.grid(row=1, column=1, pady=10, padx=10)

    @frame_switch(button=3)
    def create_offer_frame(self, loc=None):
        """
        Displays create offer page
        """
        self.current_frame_name = 'CREATEOFFER'

        self.frame_right.rowconfigure((0, 1), weight=1)
        self.frame_right.rowconfigure(20, weight=10)
        self.frame_right.columnconfigure(2, weight=1)
        self.frame_right.columnconfigure(0, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=3, rowspan=1, pady=20, padx=20, sticky="we")

        # ============ frame_info ============

        # configure grid layout (1x1)

        self.frame_info.columnconfigure((0, 3), weight=1)
        self.frame_info.rowconfigure((0, 1), weight=1)

        self.create_offer_error_label = None

        title_1 = customtkinter.CTkLabel(master=self.frame_info,
                                         text="Create Offer",
                                         text_font=("Roboto Medium", -60),
                                         height=100,
                                         fg_color=("white", "gray38"),  # <- custom tuple-color
                                         justify=LEFT)
        title_1.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="we")

        room_name_label = customtkinter.CTkLabel(master=self.frame_right,
                                                 text="Room Name",
                                                 text_font=("Roboto Medium", -22),
                                                 fg_color=("gray92", "gray30"))
        room_name_label.grid(row=2, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        self.room_name_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                      width=120,
                                                      placeholder_text="Enter room name here...")
        self.room_name_entry.grid(row=3, column=0, columnspan=3, pady=5, padx=20, sticky="we")

        location_label = customtkinter.CTkLabel(master=self.frame_right,
                                                text="Location ( x, y )",
                                                text_font=("Roboto Medium", -22),
                                                fg_color=("gray92", "gray30"))
        location_label.grid(row=4, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        if loc:
            location_label_2 = customtkinter.CTkLabel(master=self.frame_right,
                                                      width=120,
                                                      text_font=("Roboto Medium", -22),
                                                      fg_color=("gray92", "gray26"),
                                                      text=f'{loc[0]}, {loc[1]}')
            location_label_2.grid(row=5, column=0, columnspan=3, pady=5, padx=20, sticky="we")
        else:
            self.location_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                         width=120,
                                                         placeholder_text="Enter location here... ( x, y )")
            self.location_entry.grid(row=5, column=0, columnspan=3, pady=5, padx=20, sticky="we")

        price_label = customtkinter.CTkLabel(master=self.frame_right,
                                             text="Price per day",
                                             text_font=("Roboto Medium", -22),
                                             fg_color=("gray92", "gray30"))
        price_label.grid(row=6, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        self.price_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                  width=120,
                                                  placeholder_text="Enter price per day here...")
        self.price_entry.grid(row=7, column=0, columnspan=3, pady=5, padx=20, sticky="we")

        start_date_label = customtkinter.CTkLabel(master=self.frame_right,
                                                  text="Start date",
                                                  text_font=("Roboto Medium", -22),
                                                  fg_color=("gray92", "gray30"))
        start_date_label.grid(row=8, column=0, columnspan=1, pady=0, padx=20, sticky="we")

        self.start_date_entry = DateEntry(self.frame_right, locale='en_US', date_pattern='yyyy-mm-dd',
                                          mindate=datetime.datetime.now())
        self.start_date_entry.grid(row=9, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        end_date_label = customtkinter.CTkLabel(master=self.frame_right,
                                                text="End date",
                                                width=170,
                                                text_font=("Roboto Medium", -22),
                                                fg_color=("gray92", "gray30"))
        end_date_label.grid(row=8, column=1, columnspan=1, pady=0, padx=5, sticky="we")

        self.end_date_entry = DateEntry(self.frame_right, locale='en_US', date_pattern='yyyy-mm-dd',
                                        mindate=datetime.datetime.now())
        self.end_date_entry.grid(row=9, column=1, columnspan=1, pady=5, padx=5, sticky="we")

        conditions_label = customtkinter.CTkLabel(
            master=self.frame_right,
            text="Conditions",
            text_font=("Roboto Medium", -22),
            fg_color=("gray92", "gray30")
        )
        conditions_label.grid(row=10, column=0, columnspan=1, pady=10, padx=10, sticky="we")

        self.conditions_text = Text(
            master=self.frame_right,
            font=("Roboto Medium", -22),
            fg="gray30",
            height=6,
            width=40
        )
        self.conditions_text.grid(row=11, column=0, columnspan=3, pady=10, padx=10, sticky="we")

        self.selected_files = ()

        def get_files():
            self.selected_files = askopenfilenames(parent=self, title='Choose a file')

        customtkinter.CTkButton(
            master=self.frame_right,
            text="Select images",
            text_font=("Roboto Medium", -26),
            fg_color=("gray75", "gray30"),
            height=60,
            command=get_files
        ).grid(row=12, column=0, columnspan=3, pady=40, padx=40, sticky="we")

        def create_offer():
            if self.create_offer_error_label:
                self.create_offer_error_label.grid_forget()
                self.create_offer_error_label.destroy()
                self.create_offer_error_label = None
            room_name = self.room_name_entry.get()
            location = ', '.join(map(lambda l: str(l), loc)) if loc else self.location_entry.get()
            price_per_day = self.price_entry.get()
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()
            conditions = self.conditions_text.get(1.0, END)
            if not room_name:
                self.display_create_offer_error('You must supply a room name!', 'red')
            elif not location:
                self.display_create_offer_error('You must supply a location!', 'red')
            elif not price_per_day:
                self.display_create_offer_error('You must supply a price!', 'red')
            elif not start_date:
                self.display_create_offer_error('You must supply a starting date!', 'red')
            elif not end_date:
                self.display_create_offer_error('You must supply an ending date!', 'red')
            elif not self.selected_files:
                self.display_create_offer_error('You must supply a photo of the room!', 'red')
            elif len(room_name) > 20:
                self.display_create_offer_error('Room name is too long (must be no more than 20 characters)', 'red')
            elif len((coords := location.split(', '))) != 2:
                self.display_create_offer_error('Invalid location (it should be x, y)', 'red')
            elif not price_per_day.isdecimal():
                self.display_signup_error('Invalid Price (Must be a number)', 'red')
            elif datetime.datetime.strptime(start_date, '%Y-%m-%d') >= datetime.datetime.strptime(end_date, '%Y-%m-%d'):
                self.display_signup_error('Invalid dates (Start date must be after End date)', 'red')
            elif not all(map(lambda fl: fl.endswith('.png'), self.selected_files)):
                self.display_signup_error('Invalid photos (Images must be of type png)', 'red')
            else:
                try:
                    t = float(coords[0]), float(coords[1])
                except:
                    self.display_create_offer_error('Invalid location (it should be x, y)', 'red')
                    return
                images = []
                for file in self.selected_files:
                    with open(file, 'rb') as f:
                        images.append(f.read())
                self.on_create_offer(room_name, (coords[0], coords[1]), price_per_day, start_date, end_date,
                                     conditions, images)

        self.create_offer_button = customtkinter.CTkButton(
            master=self.frame_right,
            text="Create Offer",
            text_font=("Roboto Medium", -40),
            fg_color=("gray75", "gray30"),
            height=60,
            command=create_offer
        )

        self.create_offer_button.grid(row=22, column=0, columnspan=3, pady=20, padx=20, sticky="we")

        self.minsize(self.WIDTH, self.HEIGHT + 140)

    def display_create_offer_error(self, error: str, color):
        """
        Displays errors in the create offer page
        :param error: error to display
        :param color: color of error
        """
        if self.current_frame_name == 'CREATEOFFER':
            self.create_offer_error_label = customtkinter.CTkLabel(master=self.frame_right,
                                                                   text=error,
                                                                   text_color=color,
                                                                   text_font=("Roboto Medium", -16))
            self.create_offer_error_label.grid(row=21, column=0, columnspan=3, pady=5, padx=20, sticky="we")

    @frame_switch(button=4)
    def own_purchases_frame(self):
        """
        Displays my purchases page
        """
        self.current_frame_name = 'MYPURCHASES'

        self.frame_right.grid_columnconfigure((0, 2), weight=100)
        self.frame_right.grid_rowconfigure((0, 2), weight=100)

        self.goto_create_offer_button = customtkinter.CTkButton(master=self.frame_right,
                                                                text="Purchase Now",
                                                                text_font=("Roboto Medium", -36),
                                                                command=self.map_frame)
        self.goto_create_offer_button.grid(row=3, column=1, pady=10, padx=20)

        self.on_get_own_purchases()

    def update_own_purchases(self, own_purchases):
        """
        Displays all of the information on the my purchases page
        :param own_purchases: received purchases
        """
        if self.current_frame_name == 'MYPURCHASES':
            if not own_purchases:
                lbl = customtkinter.CTkLabel(master=self.frame_right,
                                             text="You have made 0 purchases",
                                             text_color='#d45a22',
                                             text_font=("Roboto Medium", -36))
                lbl.grid(row=1, column=1, pady=10, padx=10)
            else:
                self.purchases_frame = customtkinter.CTkFrame(master=self.frame_right)

                self.reviews = {}

                main_font_size = -10

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Name",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=0, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Start Date",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=1, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="End Date",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=2, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Conditions",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=3, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="State",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=4, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Review",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=5, columnspan=2, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="Dispute",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=7, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.purchases_frame,
                    text="View",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=8, columnspan=1, pady=4, padx=2, sticky="nswe")

                def create_buttons(this_purchase, i):
                    def on_dispute():
                        self.on_dispute_purchase(this_purchase['id'])
                        self.own_purchases_frame()

                    def on_review(arg):
                        def review(lvl, text_str):
                            self.on_review_purchase(this_purchase['id'], arg.get(), text_str)
                            lvl.destroy()
                            self.own_purchases_frame()
                        top_lvl = customtkinter.CTkToplevel()
                        text = Text(top_lvl)
                        text.pack(fill=BOTH, expand=1)
                        submit = customtkinter.CTkButton(master=top_lvl, command=lambda: review(top_lvl, text.get("1.0",END)), text='Submit')
                        submit.pack(fill=BOTH, expand=1)


                    dispute_button = customtkinter.CTkButton(master=self.purchases_frame,
                                                             text="Dispute",
                                                             text_font=("Roboto Medium", -12),
                                                             fg_color=("gray75", "gray30"),
                                                             command=on_dispute)

                    if this_purchase.get('state', 'Waiting') != 'Waiting': dispute_button.configure(state=DISABLED)

                    dispute_button.grid(row=i + 1, column=7, columnspan=1, pady=2, padx=2, sticky="nswe")

                    review_button = customtkinter.CTkButton(master=self.purchases_frame,
                                                            text='Review',
                                                            text_font=("Roboto Medium", -12),
                                                            fg_color=("gray75", "gray30"),
                                                            command=lambda: on_review(self.reviews[i]))

                    review_button.grid(row=i + 1, column=6, columnspan=1, pady=2, padx=2, sticky="nswe")

                    reviews = [
                        "10",
                        "9",
                        "8",
                        "7",
                        "6",
                        "5",
                        "4",
                        "3",
                        "2",
                        "1"
                    ]

                    reviews.insert(0, reviews.pop(reviews.index(this_purchase.get('review', reviews[0]))))

                    self.reviews[i] = StringVar()
                    self.reviews[i].set(this_purchase.get('review', reviews[0]))

                    review_options_menu = OptionMenu(self.purchases_frame, self.reviews[i], *reviews)

                    review_options_menu.grid(row=i + 1, column=5, columnspan=1, pady=2, padx=2, sticky="nswe")

                    if this_purchase.get('state', None) != "Ended":
                        review_button.configure(state=DISABLED)
                        review_options_menu.configure(state=DISABLED)

                    view_button = customtkinter.CTkButton(master=self.purchases_frame,
                                                          text="View",
                                                          text_font=("Roboto Medium", -12),
                                                          fg_color=("gray75", "gray30"),
                                                          command=lambda: self.map_frame(this_purchase['name'])
                                                          if this_purchase.get('name', None) else None)

                    view_button.grid(row=i + 1, column=8, columnspan=1, pady=2, padx=2, sticky="nswe")

                for i, purchase in enumerate(own_purchases):
                    name_lbl = customtkinter.CTkLabel(master=self.purchases_frame,
                                                      text=f"{purchase.get('name', 'NAN')}",
                                                      text_font=("Roboto Medium", -16),
                                                      fg_color=("gray92", "gray30"))
                    name_lbl.grid(row=i + 1, column=0, pady=2, padx=2, sticky="nswe")

                    start_date_label = customtkinter.CTkLabel(master=self.purchases_frame,
                                                              text=f"{purchase.get('start_date', 'NAN')}",
                                                              text_font=("Roboto Medium", -16),
                                                              fg_color=("gray92", "gray30"))
                    start_date_label.grid(row=i + 1, column=1, columnspan=1, pady=2, padx=2, sticky="nswe")

                    end_date_label = customtkinter.CTkLabel(master=self.purchases_frame,
                                                            text=f"{purchase.get('end_date', 'NAN')}",
                                                            text_font=("Roboto Medium", -16),
                                                            fg_color=("gray92", "gray30"))
                    end_date_label.grid(row=i + 1, column=2, columnspan=1, pady=2, padx=2, sticky="nswe")

                    conditions_label = customtkinter.CTkLabel(master=self.purchases_frame,
                                                              text=
                                                              f"{check if not str(check := purchase.get('conditions', '')).isspace() else 'NAN'}",
                                                              text_font=("Roboto Medium", -16),
                                                              fg_color=("gray92", "gray30"))
                    conditions_label.grid(row=i + 1, column=3, columnspan=1, pady=2, padx=2, sticky="nswe")

                    state_label = customtkinter.CTkLabel(master=self.purchases_frame,
                                                         text=f"{purchase.get('state', 'Waiting')}",
                                                         text_font=("Roboto Medium", -16),
                                                         fg_color=("gray92", "gray30"))
                    state_label.grid(row=i + 1, column=4, columnspan=1, pady=2, padx=2, sticky="nswe")

                    create_buttons(purchase, i)

                self.purchases_frame.grid(row=1, column=1, pady=10, padx=10)

    @frame_switch(button='admin')
    def admin_info_frame(self):
        """
        Displays admin page
        """
        self.current_frame_name = 'ADMIN'

        self.frame_right.grid_columnconfigure((0, 5), weight=100)
        self.frame_right.grid_rowconfigure((1, 4), weight=100)
        self.frame_right.grid_rowconfigure(2, minsize=60)

        options = [
            "Purchases",
            "Offers",
            "Users"
        ]

        self.admin_option = StringVar(self.frame_right)
        self.admin_option.set(options[0])

        self.options_menu = OptionMenu(self.frame_right, self.admin_option, *options,
                                       command=lambda _: self.update_admin())
        self.options_menu.grid(row=0, column=1, pady=20)

        self.date_change = DateEntry(self.frame_right, locale='en_US', date_pattern='yyyy-mm-dd')
        self.date_change.grid(row=0, column=2, pady=20)

        self.select_date = customtkinter.CTkButton(master=self.frame_right, text='Select Date', command=lambda: self.on_change_date(self.date_change.get()))
        self.select_date.grid(row=0, column=3, pady=20)

        self.admin_data = None
        self.admin_frame = None

        self.on_get_admin()

    def update_admin(self, admin_data=None):
        """
        Displays all of the information on the admin page
        :param admin_data: received information
        """
        if admin_data: self.admin_data = admin_data
        if self.current_frame_name == 'ADMIN':
            if self.admin_frame:
                self.admin_frame.destroy()
                self.admin_frame = None
            if self.admin_option.get() == "Purchases":
                self.admin_frame = customtkinter.CTkFrame(master=self.frame_right)

                main_font_size = -10

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="ID",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=0, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="OFFER ID",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="USER ID",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=2, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Name",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=3, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Duration(s)",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=4, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Conditions",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=5, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="State",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=6, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="View",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=7, columnspan=1, pady=4, padx=2, sticky="nswe")

                def create_buttons(this_purchase):

                    view_button = customtkinter.CTkButton(master=self.admin_frame,
                                                          text="View",
                                                          text_font=("Roboto Medium", -12),
                                                          fg_color=("gray75", "gray30"),
                                                          command=lambda: self.map_frame(this_purchase['name'])
                                                          if this_purchase.get('name', None) else None)

                    view_button.grid(row=i + 1, column=7, columnspan=1, pady=2, padx=2, sticky="nswe")

                for i, user in enumerate(self.admin_data[2]):
                    id_lbl = customtkinter.CTkLabel(master=self.admin_frame,
                                                    text=f"{user.get('id', 'NAN')}",
                                                    text_font=("Roboto Medium", -16),
                                                    fg_color=("gray92", "gray30"))
                    id_lbl.grid(row=i + 1, column=0, pady=2, padx=2, sticky="nswe")

                    offer_id_lbl = customtkinter.CTkLabel(master=self.admin_frame,
                                                          text=f"{user.get('offer_id', 'NAN')}",
                                                          text_font=("Roboto Medium", -16),
                                                          fg_color=("gray92", "gray30"))
                    offer_id_lbl.grid(row=i + 1, column=1, pady=2, padx=2, sticky="nswe")

                    user_id_lbl = customtkinter.CTkLabel(master=self.admin_frame,
                                                         text=f"{user.get('user_id', 'NAN')}",
                                                         text_font=("Roboto Medium", -16),
                                                         fg_color=("gray92", "gray30"))
                    user_id_lbl.grid(row=i + 1, column=2, pady=2, padx=2, sticky="nswe")

                    name_lbl = customtkinter.CTkLabel(master=self.admin_frame,
                                                      text=f"{user.get('name', 'NAN')}",
                                                      text_font=("Roboto Medium", -16),
                                                      fg_color=("gray92", "gray30"))
                    name_lbl.grid(row=i + 1, column=3, pady=2, padx=2, sticky="nswe")

                    start_date_label = customtkinter.CTkLabel(master=self.admin_frame,
                                                              text=f"{user.get('start_date', 'NAN')} - {user.get('end_date', 'NAN')}",
                                                              text_font=("Roboto Medium", -16),
                                                              fg_color=("gray92", "gray30"))
                    start_date_label.grid(row=i + 1, column=4, columnspan=1, pady=2, padx=2, sticky="nswe")

                    conditions_label = customtkinter.CTkLabel(master=self.admin_frame,
                                                              text=
                                                              f"{check if not str(check := user.get('conditions', '')).isspace() else 'NAN'}",
                                                              text_font=("Roboto Medium", -16),
                                                              fg_color=("gray92", "gray30"))
                    conditions_label.grid(row=i + 1, column=5, columnspan=1, pady=2, padx=2, sticky="nswe")

                    state_label = customtkinter.CTkLabel(master=self.admin_frame,
                                                         text=f"{user.get('state', 'Waiting')}",
                                                         text_font=("Roboto Medium", -16),
                                                         fg_color=("gray92", "gray30"))
                    state_label.grid(row=i + 1, column=6, columnspan=1, pady=2, padx=2, sticky="nswe")

                    create_buttons(user)

                self.admin_frame.grid(row=3, column=1, columnspan=3, pady=10, padx=10)
            elif self.admin_option.get() == "Offers":
                self.admin_frame = customtkinter.CTkFrame(master=self.frame_right)

                main_font_size = -10

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="ID",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=0, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="USER ID",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Name",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=2, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Duration(s)",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=3, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Conditions",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=4, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="State",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=5, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="View",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=6, columnspan=1, pady=4, padx=2, sticky="nswe")

                def create_buttons(this_offer):

                    view_button = customtkinter.CTkButton(master=self.admin_frame,
                                                          text="View",
                                                          text_font=("Roboto Medium", -12),
                                                          fg_color=("gray75", "gray30"),
                                                          command=lambda: self.map_frame(this_offer['name'])
                                                          if this_offer.get('name', None) else None)

                    view_button.grid(row=i + 1, column=6, columnspan=1, pady=2, padx=2, sticky="nswe")

                for i, user in enumerate(self.admin_data[1]):
                    id_lbl = customtkinter.CTkLabel(master=self.admin_frame,
                                                    text=f"{user.get('id', 'NAN')}",
                                                    text_font=("Roboto Medium", -16),
                                                    fg_color=("gray92", "gray30"))
                    id_lbl.grid(row=i + 1, column=0, pady=2, padx=2, sticky="nswe")

                    user_id_lbl = customtkinter.CTkLabel(master=self.admin_frame,
                                                         text=f"{user.get('user_id', 'NAN')}",
                                                         text_font=("Roboto Medium", -16),
                                                         fg_color=("gray92", "gray30"))
                    user_id_lbl.grid(row=i + 1, column=1, pady=2, padx=2, sticky="nswe")

                    name_lbl = customtkinter.CTkLabel(master=self.admin_frame,
                                                      text=f"{user.get('name', 'NAN')}",
                                                      text_font=("Roboto Medium", -16),
                                                      fg_color=("gray92", "gray30"))
                    name_lbl.grid(row=i + 1, column=2, pady=2, padx=2, sticky="nswe")

                    start_date_label = customtkinter.CTkLabel(master=self.admin_frame,
                                                              text=f"{user.get('start_date', 'NAN')} - {user.get('end_date', 'NAN')}",
                                                              text_font=("Roboto Medium", -16),
                                                              fg_color=("gray92", "gray30"))
                    start_date_label.grid(row=i + 1, column=3, columnspan=1, pady=2, padx=2, sticky="nswe")

                    conditions_label = customtkinter.CTkLabel(master=self.admin_frame,
                                                              text=
                                                              f"{check if not str(check := user.get('conditions', '')).isspace() else 'NAN'}",
                                                              text_font=("Roboto Medium", -16),
                                                              fg_color=("gray92", "gray30"))
                    conditions_label.grid(row=i + 1, column=4, columnspan=1, pady=2, padx=2, sticky="nswe")

                    state_label = customtkinter.CTkLabel(master=self.admin_frame,
                                                         text=f"{user.get('state', 'Waiting')}",
                                                         text_font=("Roboto Medium", -16),
                                                         fg_color=("gray92", "gray30"))
                    state_label.grid(row=i + 1, column=5, columnspan=1, pady=2, padx=2, sticky="nswe")

                    create_buttons(user)

                self.admin_frame.grid(row=3, column=1, columnspan=3, pady=10, padx=10)
            elif self.admin_option.get() == "Users":
                self.admin_frame = customtkinter.CTkFrame(master=self.frame_right)

                main_font_size = -10

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="ID",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=0, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Username",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Email",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=2, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Password",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=3, columnspan=1, pady=4, padx=2, sticky="nswe")

                customtkinter.CTkLabel(
                    master=self.admin_frame,
                    text="Admin",
                    text_font=("Roboto Medium", main_font_size - 7),
                    fg_color="gray40"
                ).grid(row=0, column=4, columnspan=1, pady=4, padx=2, sticky="nswe")

                for i, user in enumerate(self.admin_data[0]):
                    id_lbl = customtkinter.CTkLabel(master=self.admin_frame,
                                                    text=f"{user.get('id', 'NAN')}",
                                                    text_font=("Roboto Medium", -16),
                                                    fg_color=("gray92", "gray30"))
                    id_lbl.grid(row=i + 1, column=0, pady=2, padx=2, sticky="nswe")

                    name_lbl = customtkinter.CTkLabel(master=self.admin_frame,
                                                      text=f"{user.get('username', 'NAN')}",
                                                      text_font=("Roboto Medium", -16),
                                                      fg_color=("gray92", "gray30"))
                    name_lbl.grid(row=i + 1, column=1, pady=2, padx=2, sticky="nswe")

                    email_label = customtkinter.CTkLabel(master=self.admin_frame,
                                                         text=f"{user.get('email', 'NAN')}",
                                                         text_font=("Roboto Medium", -16),
                                                         fg_color=("gray92", "gray30"))
                    email_label.grid(row=i + 1, column=2, columnspan=1, pady=2, padx=2, sticky="nswe")

                    password_label = customtkinter.CTkLabel(master=self.admin_frame,
                                                            text=f"{user.get('password', 'NAN')}",
                                                            text_font=("Roboto Medium", -16),
                                                            fg_color=("gray92", "gray30"))
                    password_label.grid(row=i + 1, column=3, columnspan=1, pady=2, padx=2, sticky="nswe")

                    state_label = customtkinter.CTkLabel(master=self.admin_frame,
                                                         text=f"{user.get('admin', 'False')}",
                                                         text_font=("Roboto Medium", -16),
                                                         fg_color=("gray92", "gray30"))
                    state_label.grid(row=i + 1, column=4, columnspan=1, pady=2, padx=2, sticky="nswe")

                self.admin_frame.grid(row=3, column=1, columnspan=3, pady=10, padx=10)

    def display_message(self, message):
        """
        Displays message by opening a popup screen and writing it there
        :param message: message to display
        """
        test = messagebox.showinfo('Attention', message)

    def on_closing(self, event=0):
        """
        Asks the user if they want to quit before the program has been closed
        """
        if messagebox.askokcancel("Quit", "Do you wish to quit?\n"
                                          "Quitting might result in data not being saved."):
            try:
                self.safe_destroy()
            except:
                pass
            self.on_close()

    def safe_destroy(self):
        """
        Destroys App safely
        """
        try:
            self.destroy()
        except:
            pass
        self.active = False

    def disconnected(self):
        """
        Displays disconnected screen
        """
        self.current_frame_name = "DISCONNECTED"

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

        self.disconnected_frame = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.disconnected_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky='nswe')

        self.disconnected_frame.grid_columnconfigure((0, 2), weight=1)
        self.disconnected_frame.grid_rowconfigure(3, weight=1)
        self.disconnected_frame.grid_rowconfigure((0, 5), weight=100)

        tk_image = ImageTk.PhotoImage(Image.open(self.logo_path).resize((250, 250)))
        image = Label(self.disconnected_frame, image=tk_image)  # font name and size in px
        image.image = tk_image
        image.grid(row=1, column=1, pady=10, padx=10)

        title_label = customtkinter.CTkLabel(master=self.disconnected_frame,
                                             text=self.app_name,
                                             text_font=("Roboto Medium", -36))  # font name and size in px
        title_label.grid(row=2, column=1, pady=10, padx=10)

        disconnected_label = customtkinter.CTkLabel(master=self.disconnected_frame,
                                                    text="Disconnected",
                                                    text_color='red',
                                                    text_font=("Roboto Medium", -44))  # font name and size in px
        disconnected_label.grid(row=4, column=1, pady=50, padx=30)


class Window(customtkinter.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.current_frame_name = 'DETAILS'

        self.title('Leasing Details')
        self.windows_set_titlebar_color('#0a694e')

        self.main_frame = customtkinter.CTkFrame(master=self, corner_radius=0)

    def start(self, details, on_purchase):
        self.details = details
        self.on_purchase = on_purchase

        self.rowconfigure((0, 1), weight=1)
        self.rowconfigure(10, weight=10)
        self.columnconfigure((0, 1, 2), weight=1)

        self.frame_info = customtkinter.CTkFrame(master=self.main_frame)
        self.frame_info.grid(row=0, column=0, columnspan=3, rowspan=1, pady=20, padx=20, sticky="we")

        self.frame_info.columnconfigure((0, 3), weight=1)
        self.frame_info.rowconfigure((0, 1), weight=1)

        self.title_1 = customtkinter.CTkLabel(master=self.frame_info,
                                              text=f"{details.get('name', 'Leasing Details')}",
                                              text_font=("Roboto Medium", -60),
                                              height=100,
                                              fg_color=("white", "gray38"),
                                              justify=LEFT)
        self.title_1.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="we")

        if details['images']:
            self.current = 0

            def move(delta):
                if not (0 <= self.current + delta - 1 < len(details['images'])):
                    self.prv.configure(state=DISABLED, fg_color='red')
                else:
                    self.prv.configure(state=NORMAL, fg_color=("gray75", "gray30"))
                if not (0 <= self.current + delta + 1 < len(details['images'])):
                    self.next.configure(state=DISABLED, fg_color='red')
                else:
                    self.next.configure(state=NORMAL, fg_color=("gray75", "gray30"))
                self.current += delta
                if self.label: self.label.destroy()
                img = ImageTk.PhotoImage(Image.open(io.BytesIO(details['images'][self.current])).resize((250, 250)))
                self.label = customtkinter.CTkLabel(self.main_frame, image=img)
                self.label.image = img
                self.label.grid(row=1, column=1, columnspan=1, pady=10, padx=20, sticky="we")

            self.label = None

            frame = customtkinter.CTkFrame(self.main_frame)
            frame.grid(row=2, column=1, columnspan=1, pady=10, padx=20, sticky="we")

            frame.columnconfigure((0, 1), weight=1)

            self.prv = customtkinter.CTkButton(frame, text='Previous picture', command=lambda: move(-1))
            self.prv.grid(row=0, column=0, sticky="we")

            self.next = customtkinter.CTkButton(frame, text='Next picture', command=lambda: move(+1))
            self.next.grid(row=0, column=1, sticky="we")

            move(0)

            """
            image = ImageTk.PhotoImage(Image.open(io.BytesIO(details['images'][0])))
            self.image = Label(master=self.main_frame, image=image)
            self.image.image = image
            self.image.grid(row=1, column=1, columnspan=1, pady=10, padx=20, sticky="we")
            """

        self.price_per_day_label = customtkinter.CTkLabel(master=self.main_frame,
                                                          text=f"Price Per Day: {details.get('price_per_day', 'NAN')}",
                                                          text_font=("Roboto Medium", -22),
                                                          fg_color=("gray92", "gray30"))
        self.price_per_day_label.grid(row=3, column=1, columnspan=1, pady=10, padx=20, sticky="we")

        self.start_date_label = customtkinter.CTkLabel(master=self.main_frame,
                                                       text=f"Start Date: {details.get('start_date', 'NAN')}",
                                                       text_font=("Roboto Medium", -22),
                                                       fg_color=("gray92", "gray30"))
        self.start_date_label.grid(row=4, column=1, columnspan=1, pady=10, padx=20, sticky="we")

        self.end_date_label = customtkinter.CTkLabel(master=self.main_frame,
                                                     text=f"End Date: {details.get('end_date', 'NAN')}",
                                                     text_font=("Roboto Medium", -22),
                                                     fg_color=("gray92", "gray30"))
        self.end_date_label.grid(row=5, column=1, columnspan=1, pady=10, padx=20, sticky="we")

        self.conditions_label = customtkinter.CTkLabel(master=self.main_frame,
                                                       text=f"Conditions: {details.get('conditions', 'NAN')}",
                                                       text_font=("Roboto Medium", -22),
                                                       fg_color=("gray92", "gray30"))
        self.conditions_label.grid(row=8, column=1, columnspan=1, pady=10, padx=20, sticky="we")

        self.buy_frame_button = customtkinter.CTkButton(master=self.main_frame,
                                                        text="BUY",
                                                        text_font=("Roboto Medium", -40),
                                                        fg_color=("gray75", "gray30"),
                                                        height=60,
                                                        command=self.buy_frame)

        self.buy_frame_button.grid(row=11, column=0, columnspan=3, pady=20, padx=20, sticky="we")

        self.main_frame.pack(fill=BOTH, expand=True)

        self.resizable(False, False)

    def buy_frame(self):
        self.current_frame_name = 'BUY'

        self.main_frame.destroy()
        self.main_frame = customtkinter.CTkFrame(master=self, corner_radius=0)

        self.start_date_button = customtkinter.CTkLabel(
            master=self.main_frame,
            text="Select Start Date",
            text_font=("Roboto Medium", -20),
            fg_color=("gray75", "gray30")
        )
        self.start_date_button.grid(row=1, column=1, columnspan=1, pady=10, padx=10, sticky="we")

        self.start_date_preview_label = DateEntry(
            self.main_frame, locale='en_US', date_pattern='yyyy-mm-dd',
            mindate=datetime.datetime.strptime(self.details.get('start_date', 'NAN'), '%Y-%m-%d'),
            maxdate=datetime.datetime.strptime(self.details.get('end_date', 'NAN'), '%Y-%m-%d')
        )
        self.start_date_preview_label.grid(row=1, column=2, columnspan=1, pady=10, padx=10, sticky="we")

        self.end_date_button = customtkinter.CTkLabel(
            master=self.main_frame,
            text="Select End Date",
            text_font=("Roboto Medium", -20),
            fg_color=("gray75", "gray30"),
        )
        self.end_date_button.grid(row=2, column=1, columnspan=1, pady=10, padx=10, sticky="we")

        self.end_date_preview_label = DateEntry(
            self.main_frame, locale='en_US', date_pattern='yyyy-mm-dd',
            mindate=datetime.datetime.strptime(self.details.get('start_date', 'NAN'), '%Y-%m-%d'),
            maxdate=datetime.datetime.strptime(self.details.get('end_date', 'NAN'), '%Y-%m-%d')
        )
        self.end_date_preview_label.grid(row=2, column=2, columnspan=1, pady=10, padx=10, sticky="we")

        self.conditions_label = customtkinter.CTkLabel(
            master=self.main_frame,
            text="Conditions",
            text_font=("Roboto Medium", -22),
            fg_color=("gray92", "gray30")
        )
        self.conditions_label.grid(row=3, column=1, columnspan=1, pady=10, padx=10, sticky="we")

        self.conditions_text = Text(
            master=self.main_frame,
            font=("Roboto Medium", -22),
            fg="gray30",
            height=6,
            width=40
        )
        self.conditions_text.grid(row=3, column=2, columnspan=1, pady=10, padx=10, sticky="we")

        self.buy_button = customtkinter.CTkButton(
            master=self.main_frame,
            text="BUY",
            text_font=("Roboto Medium", -40),
            fg_color=("gray75", "gray30"),
            height=60,
            command=lambda: self.on_purchase(self.details['id'], str(self.start_date_preview_label.get()),
                                             str(self.end_date_preview_label.get()), self.conditions_text.get(1.0, END))
        )
        self.buy_button.grid(row=4, column=1, columnspan=2, pady=10, padx=10, sticky="we")

        self.main_frame.pack(fill=BOTH, expand=1)


if __name__ == "__main__":
    app = App()
    app.start()
