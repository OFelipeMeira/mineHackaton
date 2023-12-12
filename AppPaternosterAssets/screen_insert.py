from tkinter import *
import tkinter as tk
from time import sleep


def frame(self):
    self.screen_state = "INSERT"
    # self.reset_variables()

    # Main Frame to hide/show this screen
    self.screenMain = tk.Frame(self.window, bg=self.setup_styles["scanStatus"])
    self.screenMain.place(relx=0, rely=0, relheight=1, relwidth=1)

    # Frame to organize widgets
    screenPat = tk.Frame(self.window, bg=self.setup_styles["frame_bg"])
    screenPat.place(relx=0.5, rely=0.5, relheight=0.7, relwidth=0.6, anchor="center")

    # quit button
    quitBtn = tk.Button(
        self.window, bg="red", text="X", font=self.setup_styles["btn_font"]
    )
    quitBtn.place(relx=0.9, rely=0.1, relheight=0.05, relwidth=0.05, anchor="center")
    quitBtn.config(command=quit)

    # Label for Status of the Screen
    status = tk.Label(
        self.window,
        text=f"{self.screen_state.capitalize()}",
        bg=self.setup_styles["frame_bg"],
        justify="center",
        font=self.setup_styles["scanLabelFont"],
    )
    status.place(relx=0.5, rely=0.1, relheight=0.1, relwidth=0.3, anchor="center")

    backBtn = tk.Button(
        self.window,
        bg=self.setup_styles["btn_color"],
        text="<",
        foreground=self.setup_styles["btn_fg"],
        font=self.setup_styles["btn_font"],
    )
    backBtn.place(relx=0.1, rely=0.1, relheight=0.05, relwidth=0.05, anchor="center")
    backBtn.config(command=self.show_menu_screen)

    # Label for Paternoster Row
    partNumber = tk.Label(
        screenPat,
        text=f"PartNumber: {self.setup_variables['part_number']}",
        bg=self.setup_styles["frame_bg"],
        justify="center",
        font=self.setup_styles["scanLabelFont"],
    )
    partNumber.place(relx=0.5, rely=0.15, relheight=0.3, relwidth=1, anchor="center")

    # Label for Name of box
    boxName = tk.Label(
        screenPat,
        text=f"{self.setup_variables['paternosterBoxLabel']}\n{self.setup_variables['paternosterBoxText']}",
        bg=self.setup_styles["frame_bg"],
        justify="center",
        font=self.setup_styles["scanLabelFont"],
    )
    boxName.place(relx=0.5, rely=0.40, relheight=0.3, relwidth=1, anchor="center")

    # Label for Paternoster Row
    patRow = tk.Label(
        screenPat,
        text=f"{self.setup_variables['paternosterPosLabel']}\n{self.setup_variables['paternosterPosText']}",
        bg=self.setup_styles["frame_bg"],
        justify="center",
        font=self.setup_styles["scanLabelFont"],
    )
    patRow.place(relx=0.5, rely=0.70, relheight=0.3, relwidth=1, anchor="center")
