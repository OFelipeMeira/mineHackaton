from tkinter import *
import tkinter as tk
from time import sleep

def frame(self):
    self.screen_state = "Menu"

    # Main Frame to hide/show this screen
    self.screenMain = tk.Frame(self.window, bg=self.setup_styles['scanStatus'])
    self.screenMain.place(relx=0, rely=0, relheight=1, relwidth=1)

    # Frame to organize widgets
    screenPat = tk.Frame(self.window, bg=self.setup_styles['frame_bg'])
    screenPat.place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.6, anchor='center')

    #quit button
    quitBtn = tk.Button(self.window, bg='red', text="X", font=self.setup_styles['btn_font'])
    quitBtn.place(relx=0.9, rely=0.1 , relheight=0.05, relwidth=0.05, anchor='center')
    quitBtn.config(command=quit)

    # title
    title = tk.Label(self.window,
                        text=f"Paternoster",
                        bg=self.setup_styles['frame_bg'],
                        justify='center',
                        font=self.setup_styles['scanLabelFont'],
                        )
    title.place(relx=0.5, rely=0.15, relheight=0.1, relwidth=0.3, anchor='center')

    # insert Button
    insertBtn = tk.Button(self.window, bg=self.setup_styles['btn_color'], text="Insert", font=self.setup_styles['btn_font'], fg=self.setup_styles['btn_fg'])
    insertBtn.place(relx=0.3, rely=0.7 , relheight=0.2, relwidth=0.2, anchor='center')
    insertBtn.config(command=self.show_insert_screen)

    # remove Button
    removeBtn = tk.Button(self.window, bg=self.setup_styles['btn_color'], text="Remove", font=self.setup_styles['btn_font'], fg=self.setup_styles['btn_fg'])
    removeBtn.place(relx=0.7, rely=0.7 , relheight=0.2, relwidth=0.2, anchor='center')
    removeBtn.config(command=self.show_remove_screen)