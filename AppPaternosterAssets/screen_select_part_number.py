from tkinter import *
import tkinter as tk
from tkinter import ttk
from time import sleep


def frame(self):
    self.screen_state = "PARTNUMBER"
    # self.reset_variables()

    # Main Frame to hide/show this screen
    self.screenMain = tk.Frame(self.window, bg=self.setup_styles["scanStatus"])
    self.screenMain.place(relx=0, rely=0, relheight=1, relwidth=1)

    # Frame to organize widgets
    # screenPN = tk.Frame(self.window, bg=self.setup_styles['frame_bg'])
    screenPN = tk.Frame(self.window, bg="#f00")
    screenPN.place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.8, anchor="center")

    # quit button
    quitBtn = tk.Button(
        self.window, bg="red", text="X", font=self.setup_styles["btn_font"]
    )
    quitBtn.place(relx=0.9, rely=0.1, relheight=0.05, relwidth=0.05, anchor="center")
    quitBtn.config(command=quit)

    # Label for Status of the Screen
    status = tk.Label(
        self.window,
        text=f"Select Part Number",
        bg=self.setup_styles["frame_bg"],
        justify="center",
        font=self.setup_styles["scanLabelFont"],
    )
    status.place(relx=0.5, rely=0.15, relheight=0.1, relwidth=0.7, anchor="center")

    backBtn = tk.Button(
        self.window,
        bg=self.setup_styles["btn_color"],
        text="<",
        foreground=self.setup_styles["btn_fg"],
        font=self.setup_styles["btn_font"],
    )
    backBtn.place(relx=0.1, rely=0.1, relheight=0.05, relwidth=0.05, anchor="center")
    backBtn.config(command=self.show_menu_screen)

    search_text = tk.Text(screenPN)
    search_text.place(relx=0, rely=0, relheight=0.1, relwidth=0.5)

    search_btn = tk.Button(screenPN, text="Buscar")
    search_btn.place(relx=0.5, rely=0, relheight=0.1, relwidth=0.5)

    self.sync_filter_part_numbers(search_text.get("1.0",'end-1c'))

    # Creating the treeview
    self.table = ttk.Treeview(screenPN, columns=[" "], show="", style="mystyle.Treeview")
    self.table.place(relx=0, rely=0.1, relheight=0.9, relwidth=1)

    # Styling the Treeview
    self.tb_style = ttk.Style()
    self.tb_style.configure(
        "mystyle.Treeview",
        highlightthickness=0,
        bd=0,
        font=self.setup_styles["treeview_font"],
        height=60,
    )

    part_numbers = self.setup_variables["partNumbers"]

    for n in range(len(part_numbers)):
        self.table.insert("", tk.END, value=part_numbers[n])
        # print(n)

    # scrollbar = ttk.Scrollbar(screenPN, orient=tk.VERTICAL, command=self.table.yview)
    # scrollbar.grid(row=0, column=1, sticky='ns')
    # self.table.configure(yscroll=scrollbar.set)

    self.table.bind("<<TreeviewSelect>>", self.select_pn)
