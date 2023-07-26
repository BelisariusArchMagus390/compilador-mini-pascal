from tkinter import *
from tkinter import ttk
import os
import sys

parse_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parse_folder_path)

from models.parser_model import Parser


class Tab_lexic_table:
    def __init__(self, my_notebook: ttk.Notebook, root, code):
        self.my_notebook = my_notebook
        self.root = root
        self.code = code
        self.parse = Parser(self.code)
        self.parse.parse()

        self.tree_frame = ttk.Frame(self.my_notebook)
        self.tree_frame.pack()

        # Scrollbar vertical da Text box
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        # Pack da Scrollbar
        self.tree_scroll.pack(side="right", fill="y")

        self.my_tree = ttk.Treeview(
            self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended"
        )
        self.my_tree.pack()

        # Configuração da Scrollbar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define o nome das colunas
        self.my_tree["columns"] = (
            "Lexema",
            "Token",
            "Linha",
            "Coluna",
            "Tipo Token",
            "ID",
        )

        # Formatando as colunas
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Lexema", anchor="w", width=140)
        self.my_tree.column("Token", anchor="w", width=140)
        self.my_tree.column("Linha", anchor="w", width=140)
        self.my_tree.column("Coluna", anchor="w", width=140)
        self.my_tree.column("Tipo Token", anchor="w", width=140)
        self.my_tree.column("ID", anchor="center", width=100)

        # Criando Headings
        self.my_tree.heading("#0", text="", anchor="w")
        self.my_tree.heading("Lexema", text="Lexema", anchor="w")
        self.my_tree.heading("Token", text="Token", anchor="w")
        self.my_tree.heading("Linha", text="Linha", anchor="w")
        self.my_tree.heading("Coluna", text="Coluna", anchor="w")
        self.my_tree.heading("Tipo Token", text="Tipo Token", anchor="w")
        self.my_tree.heading("ID", text="ID", anchor="center")

        self.data = self.parse.get_matriz_tokens()

        # Inserindo dados na TreeView
        for token in self.data:
            self.my_tree.insert("", END, values=token)

        self.my_notebook.add(self.tree_frame, text="Lexic Table")
