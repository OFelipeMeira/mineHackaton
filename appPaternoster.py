from tkinter import *
from tkinter import messagebox
import asyncio
from tortoise.exceptions import DoesNotExist, DBConnectionError, IntegrityError
from Database import connector
from AppPaternosterAssets import screen_insert

from time import sleep

from datetime import datetime

_MISSING_DATABASE = "Database not connected"
_DATABASE_CONNECTION_ERROR = "Database connection error"
_UNKNOWN_BOX_ERROR = "Unkown box error"
_BOX_DOES_NOT_EXIST = "This box does not exist in the database"
_SEARCH_ERROR = "Box searching error"
_NO_BOX_SEARCHED = 'No box searched'

class Paternoster:
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

            'entry_font': f'Arial, {self.screen_width*0.02:.0f}',       # Entry - Font

            'scanStatus': '#D8D1CB'
        }

        # Setting up all the variables
        self.type_data = []
        self.box_types = []
        self.setup_variables = {

            'paternosterBoxLabel': 'Codigo da Caixa',
            'paternosterBoxText': '-',

            'paternosterPosLabel': 'Posição',
            'paternosterPosText': '-',

        }

        self.window.bind("<Key>", self.key_pressed)

        # calling the main screen and the scanning screen
        self.show_paternoster_screen()
        
        # tkinter mainloop
        self.window.mainloop()


    def show_paternoster_screen(self):
        screen_insert.frame(self)
        

    def key_pressed(self, key):
        self.text += key.char
        
        #Letting allways the first letter to upper case
        if len(self.text) == 1:
            self.text = self.text[0].upper()
        print(self.text)

        match (self.screen_state):
            case ("INSERT"):

                #reading box
                if len(self.text) == 4:
                    # READING THE BOX and showing position to insert: 
                    if self.get_box(self.text):
                        self.setup_variables['paternosterBoxText'] = self.text
                        self.execute_async_method(self.show_first_pos())

                        self.box_code = self.text

                        self.text = ""

                # ADDING:
                if self.text == self.setup_variables['paternosterPosText'] and self.setup_variables['paternosterBoxText'] != "-":
                    self.execute_async_method(self.insert_paternoster( box_name= self.setup_variables['paternosterBoxText'] ))
                    self.setup_variables['paternosterBoxText'] = "-"
                    self.setup_variables['paternosterPosText'] = "-"
                    print("AADDED")
                
            case ("REMOVE"):
                pass

        self.show_paternoster_screen()
        #reseting self.text after 4 carachteres
        if len(self.text) > 4:
            self.text = ""

    async def show_first_pos(self):
        await connector.connect()
        first_pos = await connector.get_first_usable_pos()
        self.setup_variables['paternosterPosText'] = first_pos.pos_name

    async def get_box(self, serial):
        box = await connector.get_box(box_serial_number=serial)
        return box
    
    async def get_pat_pos(self, pos_name):
        pos = await connector.get_pat_pos(pos_name=pos_name)
        return pos
    
    def execute_async_method(self, task):
        asyncio.get_event_loop().run_until_complete(task)
        return task
    
    async def insert_paternoster(self, box_name:str):
        if await connector.verify_box_paternoster(box_name):
            await connector.insert_paternoster(box_name)

if __name__ == "__main__":
    asyncio.run(Paternoster())