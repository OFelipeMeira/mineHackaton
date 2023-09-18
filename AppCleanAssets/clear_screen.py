from tkinter import *
import tkinter as tk

def frame(self):
        """
        method to call the Scanning Screen
            where the user can Scan the QRCodes and see if he can use the box
        """
        # Main Frame to hide/show this screen
        self.screenScanMain = tk.Frame(self.window, bg=self.setup_styles['scanStatus'])
        self.screenScanMain.place(relx=0, rely=0, relheight=1, relwidth=1)

        # Frame to organize widgets
        screenScan = tk.Frame(self.window, bg=self.setup_styles['frame_bg'])
        screenScan.place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.6, anchor='center')

        # Label for Name of box
        labelName = tk.Label(screenScan,
                               text=f"{self.setup_variables['scanNameLabel']}\n{self.setup_variables['scanNameText']}",
                               bg=self.setup_styles['frame_bg'],
                               justify='center',
                               font=self.setup_styles['scanLabelFont'])
        labelName.place(relx=0, rely=0.05, relheight=0.3, relwidth=1)

        # Label for Type of box
        labelType = tk.Label(screenScan,
                               text=f"{self.setup_variables['scanTypeLabel']}\n{self.setup_variables['scanTypeText']}",
                               bg=self.setup_styles['frame_bg'],
                               justify='center',
                               font=self.setup_styles['scanLabelFont'])
        labelType.place(relx=0, rely=0.3, relheight=0.3, relwidth=1)

        # Label to show how many times this box was used after cleaning
        labelUsages = tk.Label(screenScan,
                               text=f"{self.setup_variables['scanUsagesLabel']} {self.setup_variables['scanUsagesQnt']}",
                               bg=self.setup_styles['frame_bg'],
                               justify='left',
                               font=self.setup_styles['scanLabelFont'])
        labelUsages.place(relx=0, rely=0.6, relheight=0.15, relwidth=1)

        # Label to show the next cleaning date
        labelClean = tk.Label(screenScan,
                              text=f"{self.setup_variables['scanCleaningLabel']} {self.setup_variables['scanCleaningDate']}",
                              bg=self.setup_styles['frame_bg'],
                              font=self.setup_styles['scanLabelFont'])
        labelClean.place(relx=0.5, rely=0.85, relheight=0.15, relwidth=1, anchor='center')
        
        useBoxBtn = tk.Button(screenScan,
                              bg=self.setup_styles['btn_color'],
                              fg=self.setup_styles['btn_fg'],
                              font=self.setup_styles['entry_font'],
                              text=self.setup_variables['scanUseBox'],
                              command=self.sync_use_box)
        useBoxBtn.place(relx=0.5, rely=0.85, relheight=0.1, relwidth=0.2, anchor='center')