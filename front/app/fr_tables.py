from tkinter import *
from tkinter import ttk
from .tab_lexic_table import Tab_lexic_table
from .tab_symbol_table import Tab_symbol_table


class Frame_tables:
    def __init__(self, root, data, bg_color):
        self.data = data
        self.root = root
        self.bg_color = bg_color
        self.fr_tb = Toplevel(root, background=self.bg_color)
        self.fr_tb.title("Tables")
        self.fr_tb.geometry("1100x300")
        self.fr_tb.option_add("*tearOff", False)

        self.fr_tb.resizable(False, False)

        self.my_notebook = ttk.Notebook(self.fr_tb)
        self.my_notebook.pack(pady=10)

        self.tab_lexic = Tab_lexic_table(
            self.my_notebook, self.fr_tb, self.data.get_matriz_tokens()
        )
        self.tab_symbol = Tab_symbol_table(
            self.my_notebook, self.fr_tb, self.data.get_table_symbol_values()
        )
