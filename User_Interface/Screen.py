from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import asyncio
from tortoise.exceptions import DoesNotExist, DBConnectionError, IntegrityError
from Database import connector
from User_Interface.Screens import scan_screen, config_screen, add_box_screen

from datetime import datetime  
from datetime import timedelta  

_BOX_ADD_ERROR = "Box adding error"
_DUPLICATE_ERROR = "Box wit that serial number already exists"
_ILLEGAL_BOX_NAME = "Box type does not exist"
_ILLEGAL_BOX_VALUE = "For period (in days) and uses only integers are allowed."
_ILLEGAL_VALUE_ERROR = "Box value error"
_MISSING_DATABASE = "Database not connected"
_DATABASE_CONNECTION_ERROR = "Database connection error"
_UNKNOWN_BOX_ERROR = "Unkown box error"
_BOX_DOES_NOT_EXIST = "This box does not exist in the database"

class Screen:
    def __init__(self):
        self.window = Tk()
        self.window.attributes('-fullscreen', True)
        self.screen_state = "NULL"
        self.text = ""
        self.screen_width = self.window.winfo_screenwidth()
        self.setup_styles = {
            'frame_bg': '#D8D1CB',          # Frames - background color
            'tile_font': f'Arial, {self.screen_width*0.034:.0f}',       # Title - Label Main screen

            'scanLabelFont': f'Arial, {self.screen_width*0.025:.0f}', # Labels for the Scanning screen

            'btn_font': f'Arial, {self.screen_width*0.017:.0f}',        # Buttons - Font
            'btn_fg': '#BFB8B0',            # Buttons - text color
            'btn_color': '#3D3D3D',         # Buttons - colors
            'btn_close_color': '#731D24',   # Button close - color

            'scanStatus': 'green',          # bg color for Scanning frame

            'entry_bg': '#3D3D3D',          # Entry - background color
            'entry_fg': '#D8D1CB',          # Entry - text color (foreground)
            'entry_font': f'Arial, {self.screen_width*0.02:.0f}'       # Entry - Font
        }
        # Styling the treeview
        self.tvw_style = ttk.Style()
        self.tvw_style.configure("mystyle.Treeview",
                                 font=('Calibri', f"{self.screen_width*0.015:.0f}"),
                                 rowheight=100,  # Modify the font of the body
                                 hight=0)
        self.tvw_style.configure("mystyle.Treeview.Heading",
                                 font=('Calibri', f"{self.screen_width*0.02:.0f}", 'bold'))  # Modify the font of the headings
        self.styloso = ttk.Style()
        self.styloso.configure('TCombobox', foreground='entry_fg', font=self.setup_styles['entry_font'])

        # Setting up all the variables
        self.type_data = []
        self.box_types = []
        self.setup_variables = {
            'mainTitle': 'Beyond5S',
            'mainBtnScan': 'Scanear',
            'mainBtnClean': 'Limpar',
            'mainBtnConfig': 'Configurações',

            'scanNameLabel': 'Código da caixa',
            'scanNameText': '-',

            'scanTypeLabel': 'Tipo da caixa:',
            'scanTypeText': '-',

            'scanUsagesLabel': 'Usos:',
            'scanUsagesQnt': '-',

            'scanCleaningLabel': 'Ultima limpeza:',
            'scanCleaningDate': 'XX/XX/XXXX',
            'scanUseBox': 'Use Box',

            'configBtn': 'Atualizar',

            'addBoxTitle': 'Adicionar caixa',
            'addBoxLabelCode': 'Código',
            'addBoxLabelType': 'Tipo',
            'addBoxButton': 'Adicionar'
        }
        self.window.bind("<Key>", self.key_pressed)

        # calling the main screen and the scanning screen
        self.screen_main()
        #self.set_scan_screen()
        
        # tkinter mainloop
        self.window.mainloop()

    def backButton(self):
        """
        method to create a button at the top of the screen to go back to main menu
        """

        backBtn = tk.Button(self.window,
                            bg=self.setup_styles['btn_color'],
                            fg=self.setup_styles['btn_fg'],
                            font=self.setup_styles['btn_font'],
                            text='<',
                            command=self.screen_main)
        backBtn.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.05)
    
    def screen_main(self):

        """
        method to call the main menu

            where the user can choose between Scanning, Cleaning or Configure the database
        """
        
        self.screen_state = "main"

        # Main Frame to hide/show this screen
        self.screenMain = tk.Frame(self.window, bg=self.setup_styles['frame_bg'])
        self.screenMain.place(relx=0, rely=0, relheight=1, relwidth=1)




        # Button to close

        closeBtn = tk.Button(self.screenMain, bg=self.setup_styles['btn_close_color'], text='X', command=quit,
                             fg=self.setup_styles['btn_fg'], font=('Arial', f"{self.screen_width*0.017:.0f}"), borderwidth=0.1)

        closeBtn.place(relx=0.95, rely=0.05, relheight=0.05, relwidth=0.05, anchor='center')


        # Frame to organize widgets

        frame = tk.Frame(self.window, bg=self.setup_styles['frame_bg'])

        frame.place(relx=0.5, rely=0.5, relheight=0.8, relwidth=0.8, anchor='center')



        # Title of the project

        label = tk.Label(frame,
                         bg=self.setup_styles['frame_bg'],

                         text=self.setup_variables['mainTitle'],
                         font=self.setup_styles['tile_font'])

        label.place(relx=0.5, rely=0.33, relheight=0.2, relwidth=1, anchor='center')


        # Button to open the Scan Screen

        btnScan = tk.Button(frame,

                            text=self.setup_variables['mainBtnScan'],
                            font=self.setup_styles['btn_font'],

                            background=self.setup_styles['btn_color'],
                            fg=self.setup_styles['btn_fg'],

                            command=self.set_scan_screen)

        btnScan.place(relx=0.25, rely=0.66, relheight=0.2, relwidth=0.2, anchor='center')


        # Button to open the Cleaning Screen

        btnClean = tk.Button(frame,

                             text=self.setup_variables['mainBtnClean'],
                             font=self.setup_styles['btn_font'],

                             background=self.setup_styles['btn_color'],
                             fg=self.setup_styles['btn_fg'],

                             command=self.set_clean_screen)

        btnClean.place(relx=0.5, rely=0.66, relheight=0.2, relwidth=0.2, anchor='center')


        # Button to open the Config Screen

        btnConfig = tk.Button(frame,

                              text=self.setup_variables['mainBtnConfig'],
                              font=self.setup_styles['btn_font'],

                              background=self.setup_styles['btn_color'],
                              fg=self.setup_styles['btn_fg'],

                              command=self.set_config_screen)

        btnConfig.place(relx=0.75, rely=0.66, relheight=0.2, relwidth=0.2, anchor='center')
    
    def error_screen(self, error_title:str, msg: str):
        messagebox.showerror(error_title, msg)
        
    def show_screen_scan(self):
        """
        method used by the main menu buttons to hide the main menu and show the Scanning screen
        """
        # close the main menu
        self.screenMain.place_forget()
        # opens the scan screen
        scan_screen.screen_scan(self)
        # create the back button
        self.backButton()

    def show_screen_add_box(self):
        # close config
        self.screenConfiguration.place_forget()
        # opens the scan screen
        add_box_screen.screen_add_boxes(self)
        # create the back button
        self.backButton()
    
    def add_new_box(self):
        try:
            self.execute_async_method(self.add_new_box_async())
            self.screen_main()
        except IntegrityError:
            self.error_screen(_BOX_ADD_ERROR, _DUPLICATE_ERROR)
        except DoesNotExist:
            self.error_screen(_BOX_ADD_ERROR, _ILLEGAL_BOX_NAME)
        except DBConnectionError:
            self.error_screen(_DATABASE_CONNECTION_ERROR, _MISSING_DATABASE)

    def callback(self, evt):
        """
        method call every time an item from the treeview is selected
            cleans all the entries, and get the text from the selected item
        """
        # Cleaning all the Entries
        #self.entryType.delete(0, END)
        self.entryDays.delete(0, END)
        self.entryUses.delete(0, END)

        # Getting all the data
        selectedItem = self.treeview.selection()[0]

        # Setting the data on the Entries
        self.tmpName = self.treeview.item(selectedItem)['values'][0]
        self.entryType.config(text= self.treeview.item(selectedItem)['values'][0])
        self.entryDays.insert(0, self.treeview.item(selectedItem)['values'][1])
        self.entryUses.insert(0, self.treeview.item(selectedItem)['values'][2])

    async def add_new_box_async(self):   
        code = self.entryCode.get()
        box_type = self.dropbox.get()
        type_id = (await connector.get_type(box_type)).type_id
        await connector.create_box(type_id,code)

    async def get_data(self):
        await connector.connect()
        box = await connector.get_box(self.text)
        self.setup_variables["scanUsagesQnt"] = box.uses
        self.setup_variables["scanTypeText"] = box.box_type.name
        self.setup_variables["scanNameText"] = box.serial_number
        self.setup_variables["scanCleaningDate"] = box.last_cleand
        self.defining_status(box)
    
    async def use_box(self):
        await connector.connect()
        box = await connector.use_box(self.text)

    def defining_status(self, box):
        date = self.setup_variables["scanCleaningDate"]
        difference =  datetime.now().date() - date
        
        period = box.box_type.cleaning_period
        
        if (period < difference.days) or self.setup_variables["scanUsagesQnt"] >= box.box_type.max_num_uses :
            self.setup_styles['scanStatus'] = 'red'
        elif period >= difference.days and  (period - difference.days) < 3 or box.box_type.max_num_uses-self.setup_variables["scanUsagesQnt"] <= 5:
            self.setup_styles['scanStatus'] = 'yellow'
        elif period >= difference.days:
            self.setup_styles['scanStatus'] = 'green'
        
    async def clean_box(self):
        await connector.connect()
        box = await connector.clean_box(self.text)
        self.setup_variables["scanUsagesQnt"] = box.uses
        self.setup_variables["scanCleaningDate"] = box.last_cleand 
        self.setup_variables["scanTypeText"] = box.box_type.name
        self.setup_variables["scanNameText"] = box.serial_number
        self.setup_styles['scanStatus'] = 'blue'

    async def get_box_types(self):
        await connector.connect()
        box_types = await connector.get_types()
        self.type_data.clear()
        self.box_types.clear()
        for box_type in box_types:
            data_tuple = (box_type.get("name"), box_type.get("cleaning_period"), box_type.get("max_num_uses"))
            self.type_data.append(data_tuple)
            self.box_types.append(box_type.get("name"))

    async def update_box_data(self):
        await connector.connect()
        if self.tmpName == self.entryType.cget('text'):
            box_type = await connector.alter_period(self.entryType.cget('text'), self.entryDays.get(), self.entryUses.get())
        else:
            box_type = await connector.alter_box(self.tmpName, self.entryType.cget('text'), self.entryDays.get(), self.entryUses.get())

    def update_box(self):
        try:
            self.execute_async_method(self.update_box_data())
        except ValueError:
            self.error_screen(_ILLEGAL_VALUE_ERROR,_ILLEGAL_BOX_VALUE)
        except DBConnectionError:
            self.error_screen(_DATABASE_CONNECTION_ERROR, _MISSING_DATABASE)
        self.set_config_screen()

    def set_scan_screen(self):
        self.screen_state = "scan"
        try: 
            self.execute_async_method(self.get_box_types())
        except DBConnectionError:
            self.error_screen(_DATABASE_CONNECTION_ERROR, _MISSING_DATABASE)
        self.reset_text_variables()
        self.show_screen_scan()
    
    def set_clean_screen(self):
        self.screen_state = "clean"
        self.reset_text_variables()
        self.show_screen_scan()

    def set_config_screen(self):
        self.screen_state = "config"
        try: 
            self.execute_async_method(self.get_box_types())
        except DBConnectionError:
            self.error_screen(_DATABASE_CONNECTION_ERROR, _MISSING_DATABASE)
        config_screen.screen_config(self)

    def set_add_box_screen(self):
        self.screen_state = 'add_box'
        self.show_screen_add_box()

    def key_pressed(self, key):
        if (self.screen_state == "scan" or self.screen_state == "clean"):
            self.text += key.char
            #print(self.text)
            if len(self.text) == 4:
                if (self.screen_state == "scan"): 
                    coroutine = self.get_data()
                elif (self.screen_state == "clean"):
                    coroutine = self.clean_box()
                try:
                    self.execute_async_method(coroutine)
                except DoesNotExist:
                     self.error_screen(_UNKNOWN_BOX_ERROR, _BOX_DOES_NOT_EXIST)
                except DBConnectionError:
                    self.error_screen(_DATABASE_CONNECTION_ERROR, _MISSING_DATABASE)
                self.show_screen_scan()
                self.text = ""
            if len(self.text) > 4:
                self.text = ""
            #print(key.char)

    def execute_async_method(self, task):
        asyncio.get_event_loop().run_until_complete(task)

    def reset_text_variables(self):
        self.setup_variables["scanUsagesQnt"] = "-"
        self.setup_variables["scanTypeText"] = "-"
        self.setup_variables["scanNameText"] = "-"
        self.setup_variables["scanCleaningDate"] = "-"
        self.setup_styles['scanStatus'] = '#D8D1CB'
