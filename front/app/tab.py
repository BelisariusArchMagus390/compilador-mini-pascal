import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import os
import sys
import re
from .fr_tables import Frame_tables


parse_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parse_folder_path)

from models.parser_model import Parser


class Tab_editor:
    def __init__(
        self, my_notebook: ttk.Notebook, status_bar, root, open_status_name=False
    ):
        self.my_notebook = my_notebook
        self.status_bar = status_bar
        self.root = root
        self.bg_color = "#313131"
        self.fg_color = "#ffffff"
        self.text_status_bar = "Ready      "
        self.text_title = "New File - TextPad"
        # Caminho da pasta save_file
        self.file_dir = Path(__file__).parent.parent.joinpath("save_file")

        self.frame = ttk.Frame(self.my_notebook)
        self.frame.pack(fill="both", expand=1)

        # Scrollbar vertical da Text box
        self.ver_scroll = ttk.Scrollbar(self.frame, orient="vertical")

        # Scrollbar horizontal da Text box
        self.hor_scroll = ttk.Scrollbar(self.frame, orient="horizontal")

        # Text Box
        self.my_text = tk.Text(
            self.frame,
            width=97,
            height=23,
            font=("Helvetica", 16),
            selectbackground="#b2b2b2",
            undo=True,
            yscrollcommand=self.ver_scroll.set,
            xscrollcommand=self.hor_scroll.set,
            wrap="none",
        )

        # Configuração das Scrollbars
        self.ver_scroll.config(command=self.my_text.yview)
        self.hor_scroll.config(command=self.my_text.xview)

        # Pack dos Scrollbars
        self.ver_scroll.pack(side="right", fill="y")
        self.hor_scroll.pack(side="bottom", fill="x")

        self.my_text.pack(side="top", fill="both", expand=True)

        self.my_notebook.add(self.frame, text="New File")

        # Seta variável para o arquivo aberto
        self.open_status_name = open_status_name

        # Seta variável do texto selecionado
        self.selected = False

        self.fr_output = Frame()
        self.txt_box_output = Text()

    def change_text(self, tittle):
        self.my_notebook.tab(self.frame, text=tittle)

    # Abre arquivo
    def open_file(self):
        # Pega Filename
        text_file = filedialog.askopenfilename(
            initialdir=self.file_dir,
            title="Open File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
        )

        # Checa se é o filename
        if text_file:
            # Exclui o texto anterior
            self.my_text.delete("1.0", END)

            # Torna o filename global para que possa ser acessado depois
            self.open_status_name = text_file

            # Atualizando Status Bars
            name = text_file
            self.status_bar.config(text=f"{name}        ")
            self.text_status_bar = name
            name = os.path.basename(name)
            self.root.title(f"{name} - TextPad")
            self.change_text(name)
            self.text_title = name
            # Abrindo o arquivo
            text_file = open(text_file, "r")
            stuff = text_file.read()
            # Adiciona o conteúdo do arquivo no textbox
            self.my_text.insert(END, stuff)
            # Fecha o arquivo
            text_file.close()

    # Salva como arquivo
    def save_as_file(self):
        text_file = filedialog.asksaveasfilename(
            defaultextension=".*",
            initialdir=self.file_dir,
            title="Save File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
        )
        if text_file:
            # Atualiza Status Bars
            name = text_file
            self.status_bar.config(text=f"Saved: {name}        ")
            self.text_status_bar = name
            name = os.path.basename(name)
            self.root.title(f"{name} - TextPad")
            self.change_text(name)
            self.text_title = name

            # Salva o arquivo
            text_file = open(text_file, "w")
            text_file.write(self.my_text.get(1.0, END))
            # Fecha o arquivo
            text_file.close()

    def save_file(self):
        if self.open_status_name:
            # Salva o arquivo
            text_file = open(self.open_status_name, "w")
            text_file.write(self.my_text.get(1.0, END))
            # Fecha o arquivo
            text_file.close()

            self.status_bar.config(text=f"Saved: {self.open_status_name}        ")
        else:
            self.save_as_file()

    # Cut Text
    def cut_text(self, e):
        # Checa se foi usado os atalhos do teclado
        if e:
            self.selected = self.root.clipboard_get()
        else:
            if self.my_text.selection_get():
                # Pega o texto selecionado da text box
                self.selected = self.my_text.selection_get()
                # Exclui o que foi selecidonado na text box
                self.my_text.delete("sel.first", "sel.last")
                # Limpa o que estiver no clipboard
                self.root.clipboard_clear()
                # Passa o que foi selecionado para o clipboard
                self.root.clipboard_append(self.selected)

    # Copy Text
    def copy_text(self, e):
        # Checa se foi usado os atalhos do teclado
        if e:
            self.selected = self.root.clipboard_get()

        if self.my_text.selection_get():
            # Pega o texto selecionado da text box
            self.selected = self.my_text.selection_get()
            # Limpa o que estiver no clipboard
            self.root.clipboard_clear()
            # Passa o que foi selecionado para o clipboard
            self.root.clipboard_append(self.selected)

    # Paste Text
    def paste_text(self, e):
        # Checa se foi usado os atalhos do teclado
        if e:
            self.selected = self.root.clipboard_get()
        else:
            if self.selected:
                position = self.my_text.index(INSERT)
                self.my_text.insert(position, self.selected)

    # Select all text
    def select_all(self, _=None):
        # Adiciona sel tag ao select all text
        self.my_text.tag_add("sel", "1.0", "end")

    def _edit_undo(self):
        self.my_text.edit_undo()

    def _edit_redo(self):
        self.my_text.edit_redo()

    def execute(self, _=None):
        self.my_text.config(height=13)
        fr = ttk.Frame(self.frame)
        fr.pack(fill="both", expand=1)
        # Scrollbar vertical da Text box
        ver_scroll_output = ttk.Scrollbar(fr, orient="vertical")
        ver_scroll_output.pack(side="right", fill="y")

        # Text Box
        output_txt = Text(
            fr,
            width=97,
            height=10,
            font=("Helvetica", 16),
            selectbackground="yellow",
            selectforeground="black",
            undo=True,
            yscrollcommand=ver_scroll_output.set,
            wrap="none",
            bg=self.bg_color,
            fg=self.fg_color,
        )
        output_txt.pack(side="bottom")

        # Configuração das Scrollbars
        ver_scroll_output.config(command=output_txt.yview)

        self.fr_output = fr
        self.txt_box_output = output_txt

        code = self.my_text.get("1.0", "end-1c")

        if (re.compile(r"[^\n\s]").search(code)) != None:
            parse = Parser(code)
            try:
                parse.parse()
            except ValueError:
                error = parse._get_mensagem_erro()
                for line in error:
                    output_txt.insert(tk.END, line + "\n")

            if parse.get_erro_request() == False:
                output_txt.insert(INSERT, "--- Successful Execution! ---")

                Frame_tables(self.root, parse, self.bg_color)
        else:
            output_txt.insert(INSERT, "--- Successful Execution! ---")

        output_txt.config(state=DISABLED)

    def close_tab(self, _=None):
        self.frame.destroy()

    def close_output_terminal(self, _=None):
        self.fr_output.destroy()
        self.my_text.config(height=23)

    def change_color(self, bg_color, fg_color):
        self.my_text.config(background=bg_color, fg=fg_color)
        self.txt_box_output.config(background=bg_color, fg=fg_color)
        self.bg_color = bg_color
        self.fg_color = fg_color

    def get_text_status_bar(self):
        return self.text_status_bar

    def get_text_title(self):
        return self.text_title
