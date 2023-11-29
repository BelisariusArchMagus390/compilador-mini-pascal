from tkinter import *
from tkinter import ttk


class Tab_symbol_table:
    def __init__(self, my_notebook: ttk.Notebook, root, data):
        self.my_notebook = my_notebook
        self.root = root
        self.data = data

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
            "ID",
            "Lexema",
            "Tipo",
            "Valor",
            "Tamanho array",
            "Parâmetros",
            "Chamada function/procedure",
            "Posição na memória",
        )

        # Formatando as colunas
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", anchor="center", width=100)
        self.my_tree.column("Lexema", anchor="w", width=140)
        self.my_tree.column("Tipo", anchor="w", width=140)
        self.my_tree.column("Valor", anchor="center", width=140)
        self.my_tree.column("Tamanho array", anchor="w", width=140)
        self.my_tree.column("Parâmetros", anchor="w", width=140)
        self.my_tree.column("Chamada function/procedure", anchor="w", width=170)
        self.my_tree.column("Posição na memória", anchor="w", width=140)

        # Criando Headings
        self.my_tree.heading("#0", text="", anchor="w")
        self.my_tree.heading("ID", text="ID", anchor="center")
        self.my_tree.heading("Lexema", text="Lexema", anchor="w")
        self.my_tree.heading("Tipo", text="Tipo", anchor="w")
        self.my_tree.heading("Valor", text="Valor", anchor="center")
        self.my_tree.heading("Tamanho array", text="Tamanho array", anchor="w")
        self.my_tree.heading("Parâmetros", text="Parâmetros", anchor="w")
        self.my_tree.heading(
            "Chamada function/procedure", text="Chamada function/procedure", anchor="w"
        )
        self.my_tree.heading(
            "Posição na memória", text="Posição na memória", anchor="center"
        )

        # Inserindo dados na TreeView
        for token in self.data:
            self.my_tree.insert("", END, values=token)

        self.my_notebook.add(self.tree_frame, text="Symbol Table")
