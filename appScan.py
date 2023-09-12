from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import asyncio
from tortoise.exceptions import DoesNotExist, DBConnectionError, IntegrityError
from Database import connector
from User_Interface.Screens import scan_screen
from time import sleep

from datetime import datetime

_MISSING_DATABASE = "Database not connected"
_DATABASE_CONNECTION_ERROR = "Database connection error"
_UNKNOWN_BOX_ERROR = "Unkown box error"
_BOX_DOES_NOT_EXIST = "This box does not exist in the database"
_SEARCH_ERROR = "Box searching error"
_NO_BOX_SEARCHED = 'No box searched'

class Screen:
    def __init__(self):
        self.window = Tk()
        #self.window.attributes('-fullscreen', True)
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

            'entry_font': f'Arial, {self.screen_width*0.02:.0f}'       # Entry - Font
        }

        # Setting up all the variables
        self.type_data = []
        self.box_types = []
        self.setup_variables = {

            'scanNameLabel': 'Código da caixa',
            'scanNameText': '-',

            'scanTypeLabel': 'Tipo da caixa:',
            'scanTypeText': '-',

            'scanUsagesLabel': 'Usos:',
            'scanUsagesQnt': '-',

            'scanCleaningLabel': 'Ultima limpeza:',
            'scanCleaningDate': 'XX/XX/XXXX',
            'scanUseBox': 'Use Box'
        }
        self.window.bind("<Key>", self.key_pressed)

        # calling the main screen and the scanning screen
        self.set_scan_screen()
        
        # tkinter mainloop
        self.window.mainloop()
    
    def error_screen(self, error_title:str, msg: str):
        messagebox.showerror(error_title, msg)
        
    def show_screen_scan(self):
        """
        method used by the main menu buttons to hide the main menu and show the Scanning screen
        """
        # opens the scan screen
        scan_screen.screen_scan(self)
    
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
        box = await connector.use_box(self.setup_variables["scanNameText"])

        self.setup_variables["scanUsagesQnt"] = box.uses
        self.setup_variables["scanTypeText"] = box.box_type.name
        self.setup_variables["scanNameText"] = box.serial_number
        self.setup_variables["scanCleaningDate"] = box.last_cleand
        self.defining_status(box)

    async def get_box_types(self):
        await connector.connect()
        box_types = await connector.get_types()
        self.type_data.clear()
        self.box_types.clear()
        for box_type in box_types:
            data_tuple = (box_type.get("name"), box_type.get("cleaning_period"), box_type.get("max_num_uses"))
            self.type_data.append(data_tuple)
            self.box_types.append(box_type.get("name"))

    def btn_use_box(self):
        try:
            coroutine = self.use_box()
            self.execute_async_method(coroutine)
            self.show_screen_scan()
        except DoesNotExist:
            self.error_screen(_SEARCH_ERROR, _NO_BOX_SEARCHED)

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

    def set_scan_screen(self):
        self.screen_state = "scan"
        try: 
            self.execute_async_method(self.get_box_types())
        except DBConnectionError:
            self.error_screen(_DATABASE_CONNECTION_ERROR, _MISSING_DATABASE)
        self.reset_text_variables()
        self.show_screen_scan()

    def execute_async_method(self, task):
        asyncio.get_event_loop().run_until_complete(task)

    def reset_text_variables(self):
        self.setup_variables["scanUsagesQnt"] = "-"
        self.setup_variables["scanTypeText"] = "-"
        self.setup_variables["scanNameText"] = "-"
        self.setup_variables["scanCleaningDate"] = "-"
        self.setup_styles['scanStatus'] = '#D8D1CB'

    def key_pressed(self, key):
        self.text += key.char
        if len(self.text) == 1:
            self.text = self.text[0].upper()
            print(self.text+ ":Tamanho1" )
        print(self.text)
        if len(self.text) == 4:
            if self.text == self.setup_variables['scanNameText']:
                coroutine = self.use_box()
                print("A")
            else:
                coroutine = self.get_data()
                print("text:" + self.text)
                print("variable:"+ self.setup_variables['scanNameText'] )
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

    def sync_use_box(self):
        try:
            self.execute_async_method(self.use_box())
            self.show_screen_scan()
        except:
            self.error_screen(_UNKNOWN_BOX_ERROR, _BOX_DOES_NOT_EXIST)

if __name__ == "__main__":
    asyncio.run(Screen())