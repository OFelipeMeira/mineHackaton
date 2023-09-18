from tkinter import *
import tkinter as tk
from tkinter import ttk

def screen_config(self):
        """
        method to call the Configuration Screen
            where the user can see all the types of boxes and change
        """

        # Main Frame to hide/show this screen
        self.screenConfiguration = tk.Frame(self.window, bg=self.setup_styles['frame_bg'])
        self.screenConfiguration.place(relx=0, rely=0, relheight=1, relwidth=1)

        # Method to create a button on the top, to get back to Main Screen
        self.backButton()

        # Frame to organize widgets
        screenConfig = tk.Frame(self.screenConfiguration, bg=self.setup_styles['frame_bg'])
        screenConfig.place(relx=0.5, rely=0.5, relheight=0.8, relwidth=0.8, anchor='center')

        # Creating a treeview
        self.treeview = ttk.Treeview(screenConfig, columns=('0', '1', '2'), show='headings', style='mystyle.Treeview')

        # Setting treeview Columns
        self.treeview.column(0, anchor='center', width=100)
        self.treeview.column(1, anchor='center', width=200)
        self.treeview.column(2, anchor='center', width=150)

        # Setting treeview headings
        self.treeview.heading(0, text='Tipo')
        self.treeview.heading(1, text='Frequência (dias)')
        self.treeview.heading(2, text='Máximo de usos')

        # Inserting treeview items from "self.setup_variables['treeviewData']"
        for item in self.type_data:
            self.treeview.insert("", END, values=item)

        # Placing the treeview
        self.treeview.place(relx=0, rely=0, relheight=0.695, relwidth=1)

        # Binding a function to every time select an item
        self.treeview.bind("<<TreeviewSelect>>", self.callback)

        #Scrollbar
        scrollbar = ttk.Scrollbar(self.treeview, orient='vertical', command=self.treeview.yview, style='My.Vertical.TScrollbar')
        scrollbar.place(relx=1, rely=0.5, relheight=1, anchor='e')
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        # Entry to edit the name of the Type of box
        self.entryType = tk.Label(screenConfig,
                                  bg=self.setup_styles['entry_bg'],
                                  foreground=self.setup_styles['entry_fg'],
                                  justify='center',
                                  font=self.setup_styles['entry_font'])
        self.entryType.place(relx=0.17, rely=0.75, relheight=0.1, relwidth=0.35, anchor='center', )

        # Entry to edit the frequency the box need to be cleaned
        self.entryDays = tk.Entry(screenConfig,
                                  bg=self.setup_styles['entry_bg'],
                                  foreground=self.setup_styles['entry_fg'],
                                  justify='center',
                                  font=self.setup_styles['entry_font'])
        self.entryDays.place(relx=0.48, rely=0.75, relheight=0.1, relwidth=0.15, anchor='center')

        # Entry to edit the max usages before cleaning
        self.entryUses = tk.Entry(screenConfig,
                                  bg=self.setup_styles['entry_bg'],
                                  foreground=self.setup_styles['entry_fg'],
                                  justify='center',
                                  font=self.setup_styles['entry_font'])
        self.entryUses.place(relx=0.83, rely=0.75, relheight=0.1, relwidth=0.15, anchor='center')

        # Button to add boxes
        btnAddBoxes = tk.Button(screenConfig,
                              text=self.setup_variables['addBoxTitle'],
                              font=self.setup_styles['btn_font'],
                              background=self.setup_styles['btn_color'],
                              fg=self.setup_styles['btn_fg'],
                              command=self.show_screen_add_box)
        btnAddBoxes.place(relx=0, rely=1, relheight=0.1, relwidth=0.2, anchor='sw')

        # Button to update the database
        btnUpdate = tk.Button(screenConfig,
                              text=self.setup_variables['configBtn'],
                              font=self.setup_styles['btn_font'],
                              background=self.setup_styles['btn_color'],
                              fg=self.setup_styles['btn_fg'],
                              command=self.update_box)
        btnUpdate.place(relx=1, rely=1, relheight=0.1, relwidth=0.2, anchor='se')