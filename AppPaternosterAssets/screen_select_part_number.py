from tkinter import *
import tkinter as tk
from tkinter import ttk
from time import sleep

def frame(self):

    self.screen_state = "PARTNUMBER"
    # self.reset_variables()

    # Main Frame to hide/show this screen
    self.screenMain = tk.Frame(self.window, bg=self.setup_styles['scanStatus'])
    self.screenMain.place(relx=0, rely=0, relheight=1, relwidth=1)

    # Frame to organize widgets
    # screenPN = tk.Frame(self.window, bg=self.setup_styles['frame_bg'])
    screenPN = tk.Frame(self.window, bg="#f00")
    screenPN.place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.8, anchor='center')

    #quit button
    quitBtn = tk.Button(self.window, bg='red', text="X", font=self.setup_styles['btn_font'])
    quitBtn.place(relx=0.9, rely=0.1 , relheight=0.05, relwidth=0.05, anchor='center')
    quitBtn.config(command=quit)

    # Label for Status of the Screen
    status = tk.Label(self.window,
                        text=f"Select Part Number",
                        bg=self.setup_styles['frame_bg'],
                        justify='center',
                        font=self.setup_styles['scanLabelFont'],
                        )
    status.place(relx=0.5, rely=0.15, relheight=0.1, relwidth=0.3, anchor='center')

    backBtn = tk.Button(self.window,
                        bg=self.setup_styles['btn_color'],
                        text="<",
                        foreground=self.setup_styles['btn_fg'],
                        font=self.setup_styles['btn_font'])
    backBtn.place(relx=0.1, rely=0.1 , relheight=0.05, relwidth=0.05, anchor='center')
    backBtn.config(command=self.show_menu_screen)

    # self.entry = tk.Entry(screenPN)
    # self.entry.place(relx=0.5, rely=0.1 , relheight=0.2, relwidth=0.9, anchor='center')

    columns = ['col1']
    self.table = ttk.Treeview(screenPN, columns=columns, show="headings")
    # self.PN_list = ["palavra", "umas", "duas","palavra", "umas", "duas","palavra", "umas", "duas","palavra", "umas", "duas"]

    for pn in self.setup_variables['partNumbers']:
        self.table.insert("", tk.END, value=pn)

    self.table.place(relx=0.5, rely=0.5 , relheight=1, relwidth=1, anchor='center')
    scrollbar = ttk.Scrollbar(screenPN, orient=tk.VERTICAL, command=self.table.yview) 
    self.table.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    
    self.table.bind("<<TreeviewSelect>>", self.select_pn)


    # # Label for Name of box
    # boxName = tk.Label(screenPN,
    #                     text=f"{self.setup_variables['paternosterBoxLabel']}\n{self.setup_variables['paternosterBoxText']}",
    #                     bg=self.setup_styles['frame_bg'],
    #                     justify='center',
    #                     font=self.setup_styles['scanLabelFont'],
    #                     )
    # boxName.place(relx=0.5, rely=0.25, relheight=0.5, relwidth=1, anchor='center')

    # # Label for Paternoster Row
    # patRow = tk.Label(screenPN,
    #                     text=f"{self.setup_variables['paternosterPosLabel']}\n{self.setup_variables['paternosterPosText']}",
    #                     bg=self.setup_styles['frame_bg'],
    #                     justify='center',
    #                     font=self.setup_styles['scanLabelFont'],
    #                     )
    # patRow.place(relx=0.5, rely=0.75, relheight=0.5, relwidth=1, anchor='center')

    # selected_option = tk.StringVar()
    # options = self.setup_variables['partNumbers']
    # dropdown = tk.OptionMenu(screenPN, selected_option, *options)
    # dropdown.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=1, anchor='center')

    # return selected_option.get()
