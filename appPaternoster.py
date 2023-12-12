from tkinter import *
from tkinter import messagebox
import tkinter as tk
import asyncio
from tortoise.exceptions import DoesNotExist, DBConnectionError, IntegrityError
from Database import connector
from AppPaternosterAssets import (
    screen_insert,
    screen_remove,
    screen_menu,
    screen_add_box,
    screen_select_part_number,
)

from time import sleep

from datetime import datetime

_MISSING_DATABASE = "Database not connected"
_DATABASE_CONNECTION_ERROR = "Database connection error"
_UNKNOWN_BOX_ERROR = "Unkown box error"
_BOX_DOES_NOT_EXIST = "This box does not exist in the database"
_NO_BOX_SEARCHED = "No box searched"

_INSERT_ERROR = "Erro na inserção"
_REMOVE_ERROR = "Erro na remoção"
_SEARCH_ERROR = "Erro na busca"
_CODE_NOT_FOUNDED = "Codigo não registrado"

_WRONG_POSITION = "Prateleira Incorreta"


class Paternoster:
    def __init__(self):
        self.window = Tk()
        # self.window.attributes('-fullscreen', True)
        self.screen_state = "NULL"
        self.text = ""
        self.screen_width = self.window.winfo_screenwidth()
        self.window.geometry("1280x720")
        self.setup_styles = {
            "frame_bg": "#D8D1CB",  # Frames - background color
            "tile_font": f"Arial, {self.screen_width*0.034:.0f}",  # Title - Label Main screen
            "scanLabelFont": f"Arial, {self.screen_width*0.025:.0f}",  # Labels for the Scanning screen
            "btn_font": f"Arial, {self.screen_width*0.015:.0f}",  # Buttons - Font
            "btn_fg": "#BFB8B0",  # Buttons - text color
            "btn_color": "#3D3D3D",  # Buttons - colors
            "btn_close_color": "#731D24",  # Button close - color
            "entry_font": f"Arial, {self.screen_width*0.02:.0f}",  # Entry - Font
            "entry_bg": "red",
            "entry_fg": "yellow",
            "treeview_font": f"Arial, {self.screen_width*0.01:.0f}",
            "scanStatus": "#D8D1CB",
        }

        # Setting up all the variables
        self.setup_variables = {
            "paternosterBoxLabel": "Codigo da Caixa",
            "paternosterBoxText": "-",
            "paternosterPosLabel": "Posição",
            "paternosterPosText": "-",
            "addBoxTitle": "Adicionar Caixa",
            "addBoxLabelCode": "Codigo:",
            "addBoxLabelType": "Tipo:",
            "part_number": "",
            "addBoxButton": "Add",
            "boxTypes": [],
            "partNumbers": [],
        }

        self.window.bind("<Key>", self.key_pressed)

        self.sync_get_types()
        self.sync_get_part_numbers()
        self.sync_filter_part_numbers("")

        self.show_menu_screen()
        # self.show_select_part_number()

        # tkinter mainloop
        self.window.mainloop()

    def select_pn(self, a):
        self.setup_variables["part_number"] = self.table.item(self.table.focus())["values"][0]
        print(type(self.setup_variables["part_number"]))
        self.show_insert_screen()

    def show_insert_screen(self):
        screen_insert.frame(self)

    def show_select_part_number(self):
        screen_select_part_number.frame(self)

    def show_remove_screen(self):
        screen_remove.frame(self)

    def show_menu_screen(self):
        screen_menu.frame(self)

    def show_insert_box_screen(self):
        screen_add_box.frame(self)

    def key_pressed(self, key):
        self.text += key.char

        # Letting allways the first letter to upper case
        if len(self.text) == 1:
            self.text = self.text[0].upper()
        print(self.text)

        match (self.screen_state):
            case ("PARTNUMBER"):
                self.show_select_part_number()

            case ("INSERT"):
                # if reads a Box:
                if self.text[0] == "C" and len(self.text) == 4:
                    try:
                        self.sync_get_box_data(self.text)
                        self.text = ""
                        print("reaload cause box found")
                        self.show_insert_screen()

                    except Exception as e:
                        messagebox.showerror(title=_INSERT_ERROR, message=e)
                        response = messagebox.askyesno(
                            title=_INSERT_ERROR,
                            message=f"Gostaria de registrar a caixa {self.text}?",
                        )
                        if response:
                            print(self.text)
                            self.sync_create_box(self.text)
                            messagebox.showinfo(
                                title=_INSERT_ERROR,
                                message=f"Caixa {self.text} adicionada",
                            )
                            print(f"BOX {self.text} ADDED")
                            self.text = ""
                            # self.show_insert_box_screen()

                # if reads a Position
                elif self.text[0] == "P":
                    # if is correct:
                    if self.text == self.setup_variables["paternosterPosText"]:
                        try:
                            self.sync_insert_paternoster(
                                box_name=self.setup_variables["paternosterBoxText"],
                                part_number=self.setup_variables["part_number"],
                            )
                            self.reset_variables()
                            self.text = ""
                            print("reaload cause position was found")
                            print("inserted")
                            self.show_insert_screen()
                        except Exception as e:
                            messagebox.showerror(title=_INSERT_ERROR, message=e)
                            self.text = ""
                    elif len(self.text) == 5:
                        messagebox.showerror(
                            title=_INSERT_ERROR, message=_WRONG_POSITION
                        )
                        self.reset_variables()
                        self.text = ""
                        print("reaload cause position NOT was found")
                        self.show_insert_screen()

                if len(self.text) >= 5:
                    messagebox.showerror(title="no code founded", message="Try again")
                    self.text = ""

            case ("REMOVE"):
                if len(self.text) == 4 and self.text[0] == "C":
                    # Verifying the readed code :
                    # If is a box:
                        try:
                            self.sync_get_box_data(self.text)
                            self.execute_async_method(self.show_used_pos(self.text))
                            print(self.setup_variables['paternosterBoxText'])
                            self.text = ""
                            self.show_remove_screen()
                        except Exception as e:
                            messagebox.showerror(_SEARCH_ERROR, e)

                # If is the paternoster postion is getting removed
                elif self.text[0] == "P":
                    # if is correct:
                    if self.text == self.setup_variables["paternosterPosText"]:
                        # try:
                            self.sync_remove_paternoster(
                                self.setup_variables["paternosterBoxText"]
                            )
                            self.reset_variables(self)
                            self.text = ""
                            print("reaload cause position was found")
                            print("removed")
                            self.show_remove_screen()
                        # except Exception as e:
                        #     messagebox.showerror(_REMOVE_ERROR, message=e)

                    # If is a wrong paternoster position
                    elif len(self.text) == 5:
                        messagebox.showerror(
                            title=_INSERT_ERROR, message=_WRONG_POSITION
                        )
                        self.reset_variables()
                        self.text = ""
                        print("reaload cause position NOT was found")
                        self.show_remove_screen()

                if len(self.text) >= 5:
                    messagebox.showerror(title="no code founded", message="Try again")
                    self.text = ""

        # # Reseting self.text after 4 carachteres
        # if len(self.text) > 4:
        #     self.text = ""

    def execute_async_method(self, task):
        asyncio.get_event_loop().run_until_complete(task)
        return task

    def reset_variables(self):
        self.setup_variables["paternosterBoxText"] = "-"
        self.setup_variables["paternosterPosText"] = "-"

    async def show_first_pos(self):
        await connector.connect()
        first_pos = await connector.get_first_usable_pos()
        self.setup_variables["paternosterPosText"] = first_pos.pos_name

    async def show_used_pos(self, box_name):
        await connector.connect()
        used_pos = await connector.get_used_pos(box_name=box_name)
        if used_pos:
            self.setup_variables["paternosterPosText"] = used_pos.pos_name

    async def get_box_data(self, serial):
        await connector.connect()
        box = await connector.get_box(box_serial_number=serial)
        print("="*30)
        print(box.serial_number)
        if box:
            self.setup_variables["paternosterBoxText"] = box.serial_number
        await self.show_first_pos()

    async def get_types(self):
        await connector.connect()
        for i in await connector.get_types():
            self.setup_variables["boxTypes"].append(i["name"])
        return 0

    def sync_get_types(self):
        self.execute_async_method(self.get_types())

    async def get_part_numbers(self):
        await connector.connect()
        for i in await connector.get_part_numbers():
            self.setup_variables["partNumbers"].append(i["number"])
        return 0

    def sync_get_part_numbers(self):
        self.execute_async_method(self.get_part_numbers())

    def sync_get_box_data(self, serial_number: str):
        self.execute_async_method(self.get_box_data(serial_number))

    async def insert_paternoster(self, box_name: str, part_number: str):
        await connector.connect()
        await connector.insert_paternoster(box_name, part_number)

    def sync_insert_paternoster(self, box_name: str, part_number: str):
        self.execute_async_method(
            self.insert_paternoster(box_name=box_name, part_number=part_number)
        )

    async def remove_paternoster(self, box_name: str):
        await connector.connect()
        await connector.remove_paternoster(box_name)

    def sync_remove_paternoster(self, box_name: str):
        self.execute_async_method(self.remove_paternoster(box_name=box_name))

    async def create_box(self, box_name: str):
        await connector.connect()
        await connector.create_box(box_name)

    def sync_create_box(self, box_name: str):
        self.execute_async_method(self.create_box(box_name=box_name))

    async def filter_part_numbers(self, search_text:str):
        # self.setup_variables["partNumbers"].append(i["number"])
        await connector.connect()
        for i in await connector.get_part_numbers():
            if search_text in i['number'] or search_text == "":
                print(i['number'])

    def sync_filter_part_numbers(self, search_text):
        self.execute_async_method(self.filter_part_numbers(search_text))


if __name__ == "__main__":
    asyncio.run(Paternoster())

    """ TO DO
    ** pandas - não aceita com timezones, tem que tirar
    """