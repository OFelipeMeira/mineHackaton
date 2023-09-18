from tkinter import *
import tkinter as tk

def frame(self):
        """
        method to call the Scanning Screen
            where the user can Scan the QRCodes and see if he can use the box
        """
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

        # Label for Name of box
        boxName = tk.Label(screenPat,
                               text=f"{self.setup_variables['paternosterBoxLabel']}\n{self.setup_variables['paternosterBoxText']}",
                               bg=self.setup_styles['frame_bg'],
                               justify='center',
                               font=self.setup_styles['scanLabelFont'],
                               )
        boxName.place(relx=0.5, rely=0.25, relheight=0.5, relwidth=1, anchor='center')

        # Label for Paternoster Row
        patRow = tk.Label(screenPat,
                               text=f"{self.setup_variables['paternosterRowLabel']}\n{self.setup_variables['paternosterRowText']}",
                               bg=self.setup_styles['frame_bg'],
                               justify='center',
                               font=self.setup_styles['scanLabelFont'],
                               )
        patRow.place(relx=0.5, rely=0.75, relheight=0.5, relwidth=1, anchor='center')