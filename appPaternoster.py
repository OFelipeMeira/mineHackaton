from tkinter import *
from tkinter import messagebox
import asyncio
from tortoise.exceptions import DoesNotExist, DBConnectionError, IntegrityError
from Database import connector
from AppPaternosterAssets import screen_insert, screen_remove, screen_menu

from time import sleep

from datetime import datetime

_MISSING_DATABASE = "Database not connected"
_DATABASE_CONNECTION_ERROR = "Database connection error"
_UNKNOWN_BOX_ERROR = "Unkown box error"
_BOX_DOES_NOT_EXIST = "This box does not exist in the database"
_NO_BOX_SEARCHED = 'No box searched'

_INSERT_ERROR = "Erro na inserção"
_REMOVE_ERROR = "Erro na remoção"
_SEARCH_ERROR = "Erro na busca"
_CODE_NOT_FOUNDED = "Codigo não registrado"

_WRONG_POSITION = "Prateleira Incorreta"

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
        self.setup_variables = {

            'paternosterBoxLabel': 'Codigo da Caixa',
            'paternosterBoxText': '-',

            'paternosterPosLabel': 'Posição',
            'paternosterPosText': '-',

        }

        self.window.bind("<Key>", self.key_pressed)

        self.show_menu_screen()
      
        # tkinter mainloop
        self.window.mainloop()


    def show_insert_screen(self):
        screen_insert.frame(self)
    
    def show_remove_screen(self):
        screen_remove.frame(self)  

    def show_menu_screen(self):
        screen_menu.frame(self)  

    def key_pressed(self, key):
        self.text += key.char
        
        #Letting allways the first letter to upper case
        if len(self.text) == 1:
            self.text = self.text[0].upper()
        print(self.text)

        match (self.screen_state):
            case ("INSERT"):

                if len(self.text) == 4:
                    # verifying if the readed code:
                    # if is a box:
                    if self.text[0] == "C":
                        try:
                            self.sync_get_box_data(self.text)
                        except Exception as e:
                            messagebox.showerror(title=_INSERT_ERROR, message=e)

                    # if is the paternoster position to insert
                    elif self.text == self.setup_variables['paternosterPosText']:
                        # verifying if the readed code is a positions on paternoster - insert
                        try:
                            self.sync_insert_paternoster( self.setup_variables['paternosterBoxText'] )
                            self.reset_variables()
                        except Exception as e:
                            messagebox.showerror(title=_INSERT_ERROR, message=e)

                    # if is a wrong paternoster position                                        
                    elif self.text[0] == "P" :
                        messagebox.showerror(title=_INSERT_ERROR, message=_WRONG_POSITION)

                    # or if is none of the above
                    else:
                        messagebox.showerror(title=_SEARCH_ERROR, message=_CODE_NOT_FOUNDED)                       
                    self.show_insert_screen()
                    self.text = ""
                
            case ("REMOVE"):
                if len(self.text) == 4:
                    # Verifying the readed code :
                    # If is a box:
                    if self.text[0] == "C":
                        try:
                            self.sync_get_box_data(self.text)
                            self.execute_async_method(self.show_used_pos(self.text))
                        except Exception as e:
                            messagebox.showerror(_SEARCH_ERROR, e) 
                    
                    # If is the paternoster postion is getting removed
                    elif self.text == self.setup_variables['paternosterPosText']:
                        try:
                            self.sync_remove_paternoster( self.setup_variables['paternosterBoxText'] )
                            self.reset_variables(self)
                        except Exception as e:
                            messagebox.showerror(_REMOVE_ERROR, message=e)

                    # If is a wrong paternoster position                                        
                    elif self.text[0] == "P" :
                        messagebox.showerror(_REMOVE_ERROR, message=_WRONG_POSITION)

                    # Or if is none of the above
                    else:                        
                        messagebox.showerror(title=_SEARCH_ERROR, message=_CODE_NOT_FOUNDED)                       
                    
                    self.text = ""
                self.show_remove_screen()

        # Reseting self.text after 4 carachteres
        if len(self.text) > 4:
            self.text = ""

    def reset_variables(self):
        self.setup_variables['paternosterBoxText'] = "-"
        self.setup_variables['paternosterPosText'] = "-"

    async def show_first_pos(self):
        await connector.connect()
        first_pos = await connector.get_first_usable_pos()
        self.setup_variables['paternosterPosText'] = first_pos.pos_name

    async def show_used_pos(self, box_name):
        await connector.connect()
        used_pos = await connector.get_used_pos(box_name=box_name)   
        if used_pos:
            self.setup_variables['paternosterPosText'] = used_pos.pos_name

    async def get_box_data(self, serial):
        await connector.connect()
        box = await connector.get_box(box_serial_number=serial)
        try:
            self.setup_variables['paternosterBoxText'] = box.serial_number
        except:
            pass
        await self.show_first_pos()

    def sync_get_box_data(self, serial_number:str):
        self.execute_async_method(self.get_box_data(serial_number))

    def execute_async_method(self, task):
        asyncio.get_event_loop().run_until_complete(task)
        return task
    
    async def insert_paternoster(self, box_name:str):
        await connector.connect()
        await connector.insert_paternoster(box_name)
    
    def sync_insert_paternoster(self, box_name:str):
        self.execute_async_method(self.insert_paternoster(box_name=box_name))

    async def remove_paternoster(self, box_name:str):
        await connector.connect()
        await connector.remove_paternoster(box_name)

    def sync_remove_paternoster(self, box_name:str):
        self.execute_async_method(self.remove_paternoster(box_name=box_name))



if __name__ == "__main__":
    asyncio.run(Paternoster())

    """ TO DO
    ** pandas - não aceita com timezones, tem que tirar
    """