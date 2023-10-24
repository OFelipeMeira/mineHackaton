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
        self.data = {
            'box_serial':'',
            'insert_pos': '',
            'box_insertable': False,
            'is_box': False
        }
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
                    # verifying if the readed code is a box: 
                    if self.sync_is_box(self.text):
                        try:
                            self.sync_get_box_data(self.text)
                        except Exception as e:
                            print("LINHA 102")
                            print(e)
                            # messagebox.showerror(title="Erro na inserção", message=e)
                                           
                    elif self.text == self.data['insert_pos']:
                        # verifying if the readed code is a positions on paternoster - insert
                        self.sync_insert_paternoster( self.data['box_serial'] )

                        self.setup_variables['paternosterBoxText'] = "-"
                        self.setup_variables['paternosterPosText'] = "-"
                        self.data['box_serial'] = ""

                    else:
                        messagebox.showerror("Erro na busca", "codigo não encontrado")                       
                    self.show_insert_screen()
                    self.text = ""
                
            case ("REMOVE"):
                if len(self.text) == 4:

                    # searching the position the box was inserted
                    if self.text[0] == "C":
                        self.sync_get_box_data(self.text)
                        self.setup_variables['paternosterBoxText'] = self.data['box_serial']
                        self.execute_async_method(self.show_used_pos(self.text))
                    
                    if self.text == self.data['insert_pos']:
                        self.sync_remove_paternoster( self.data['box_serial'] )
                        self.setup_variables['paternosterBoxText'] = "-"
                        self.setup_variables['paternosterPosText'] = "-"
                        self.data['box_serial'] = ""

                    self.text = ""
                self.show_remove_screen()

        #reseting self.text after 4 carachteres
        # if len(self.text) > 4:
        #     self.text = ""

    async def verify_paternoster(self, serial_number):
        await connector.connect()
        self.data['box_insertable'] = await connector.verify_paternoster(serial_number)

    async def show_first_pos(self):
        await connector.connect()
        first_pos = await connector.get_first_usable_pos()
        self.setup_variables['paternosterPosText'] = first_pos.pos_name
        self.data['insert_pos'] = first_pos.pos_name

    async def show_used_pos(self, box_name):
        await connector.connect()
        used_pos = await connector.get_used_pos(box_name=box_name)      
        self.setup_variables['paternosterPosText'] = used_pos.pos_name
        self.data['insert_pos'] = used_pos.pos_name

    async def get_box_data(self, serial):
        await connector.connect()
        box = await connector.get_box(box_serial_number=serial)
        self.data['box_serial'] = box.serial_number
        self.setup_variables['paternosterBoxText'] = box.serial_number
        await self.show_first_pos()

    def sync_get_box_data(self, serial_number:str):
        try:
            self.execute_async_method(self.get_box_data(serial_number))
        except Exception as e :
            print("LINHA 171")
            print(e)
            self.text = ""

    async def is_box(self, serial_number):
        await connector.connect()
        if await connector.get_box(serial_number):
            self.data['is_box'] = True
        else:
            self.data['is_box'] = False

    def sync_is_box(self, serial_number):
        self.execute_async_method(self.is_box(serial_number=serial_number))
        return self.data['is_box']

    async def get_pat_pos(self, pos_name):
        await connector.connect()
        pos = await connector.get_pat_pos(pos_name=pos_name)
        return pos
    
    def execute_async_method(self, task):
        asyncio.get_event_loop().run_until_complete(task)
        return task
    
    async def insert_paternoster(self, box_name:str):
        await connector.connect()
        await connector.insert_paternoster(box_name)
    
    def sync_insert_paternoster(self, box_name:str):
        try:
            return self.execute_async_method(self.insert_paternoster(box_name=box_name))
        except Exception as e:
            print("LINHA 191")
            # messagebox.showerror(title="Erro na inserção", message=e)
            print(e)
            self.text = ""


    async def remove_paternoster(self, box_name:str):
        await connector.connect()
        return await connector.remove_paternoster(box_name)

    def sync_remove_paternoster(self, box_name:str):
        try:
            return self.execute_async_method(self.remove_paternoster(box_name=box_name))
        except Exception as e:
            print("LINHA 202")
            # messagebox.showerror(title="Erro na remoção", message=e)
            print(e)
            self.text = ""



if __name__ == "__main__":
    asyncio.run(Paternoster())

    """ TO DO
    erros - documentação tortoise mostra quais exceptions cada codigo pode gerar
    ** pandas - não aceita com timezones, tem que tirar
    """