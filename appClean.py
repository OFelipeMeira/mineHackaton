from tkinter import *
from tkinter import messagebox
import asyncio
from tortoise.exceptions import DoesNotExist, DBConnectionError
from Database import connector
from AppCleanAssets import clear_screen 

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
            'scanCleaningDate': 'XX/XX/XXXX'
        }
        self.window.bind("<Key>", self.key_pressed)

        # calling the main screen and the scanning screen
        self.set_clean_screen()
        
        # tkinter mainloop
        self.window.mainloop()
    
    def error_screen(self, error_title:str, msg: str):
        messagebox.showerror(error_title, msg)
    
    async def get_data(self):
        await connector.connect()
        box = await connector.get_box(self.text)
        self.setup_variables["scanUsagesQnt"] = box.uses
        self.setup_variables["scanTypeText"] = box.box_type.name
        self.setup_variables["scanNameText"] = box.serial_number
        self.setup_variables["scanCleaningDate"] = box.last_cleand
        
        self.defining_status(box)

    async def clean_box(self):
        await connector.connect()
        box = await connector.clean_box(self.text)
        self.setup_variables["scanUsagesQnt"] = box.uses
        self.setup_variables["scanCleaningDate"] = box.last_cleand 
        self.setup_variables["scanTypeText"] = box.box_type.name
        self.setup_variables["scanNameText"] = box.serial_number
        self.setup_styles['scanStatus'] = 'blue'

    def set_clean_screen(self):
        self.screen_state = "clean"
        self.reset_text_variables()
        clear_screen.frame(self)

    def execute_async_method(self, task):
        asyncio.get_event_loop().run_until_complete(task)

    def reset_text_variables(self):
        self.setup_variables["scanUsagesQnt"] = "-"
        self.setup_variables["scanTypeText"] = "-"
        self.setup_variables["scanNameText"] = "-"
        self.setup_variables["scanCleaningDate"] = "-"
        self.setup_styles['scanStatus'] = '#D8D1CB'

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
                clear_screen.frame(self)
                self.text = ""
            if len(self.text) > 4:
                self.text = ""

if __name__ == "__main__":
    asyncio.run(Screen())