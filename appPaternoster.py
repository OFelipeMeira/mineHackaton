from tkinter import *
from tkinter import messagebox

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
        self.set_paternoster_screen(self)
        
        # tkinter mainloop
        self.window.mainloop()

    def set_paternoster_screen(self):
        self.screen_state = "scan"

    def key_pressed(self, key):
        self.text += key.char
        if len(self.text) == 1:
            self.text = self.text[0].upper()
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