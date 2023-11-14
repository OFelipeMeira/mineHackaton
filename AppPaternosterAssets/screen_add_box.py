from tkinter import *
import tkinter as tk
from tkinter import ttk

def frame(self):
        self.screen_state = "ADDBOX"
        self.reset_variables()

        # Main Frame to hide/show this screen
        self.screenAddBoxes = tk.Frame(self.window, bg=self.setup_styles['frame_bg'])
        self.screenAddBoxes.place(relx=0, rely=0, relheight=1, relwidth=1)

        # Label Add boxes Title
        labelAddBoxTitle = tk.Label(self.screenAddBoxes,
                              text= self.setup_variables['addBoxTitle'],
                              bg=self.setup_styles['frame_bg'],
                              font=self.setup_styles['tile_font'])
        labelAddBoxTitle.place(relx=0.5, rely=0.2, relheight=0.2, relwidth=0.4, anchor='center')

        # Label Add boxes Label1
        labelAddBox = tk.Label(self.screenAddBoxes,
                               text= self.setup_variables['addBoxLabelCode'],
                               bg=self.setup_styles['frame_bg'],
                               font=self.setup_styles['entry_font'])
        labelAddBox.place(relx=0.28, rely=0.5, relheight=0.1, relwidth=0.1, anchor='center')

        # Entry Box code
        self.entryCode = tk.Entry(self.screenAddBoxes,
                             bg=self.setup_styles['entry_bg'],
                             foreground=self.setup_styles['entry_fg'],
                             justify='center',
                             font=self.setup_styles['entry_font'])
        self.entryCode.place(relx=0.41, rely=0.5, relheight=0.1, relwidth=0.15, anchor='center')

        # Label Add boxes Label2
        labelAddBox = tk.Label(self.screenAddBoxes,
                               text= self.setup_variables['addBoxLabelType'],
                               bg=self.setup_styles['frame_bg'],
                               font=self.setup_styles['entry_font'])
        labelAddBox.place(relx=0.54, rely=0.5, relheight=0.1, relwidth=0.1, anchor='center')

        #dropbox
        self.dropbox = ttk.Combobox(self.screenAddBoxes, values=self.setup_variables['boxTypes'], font=self.setup_styles['entry_font'], style="TCombobox")
        self.dropbox.place(relx=0.65, rely=0.5, relheight=0.1, relwidth=0.15, anchor='center')

        # Button to open the Scan Screen
        btnAdd = tk.Button(self.screenAddBoxes,
                            text=self.setup_variables['addBoxButton'],
                            font=self.setup_styles['btn_font'],
                            background=self.setup_styles['btn_color'],
                            fg=self.setup_styles['btn_fg'],
                            command="") 
        btnAdd.place(relx=0.5, rely=0.75, relheight=0.1, relwidth=0.15, anchor='center')