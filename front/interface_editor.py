from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# from tkinter import font

from sys import exit
from pathlib import Path
import os


class Tab_editor:
    def __init__(
        self, my_notebook: ttk.Notebook, status_bar, root, open_status_name=False
    ):
        self.my_notebook = my_notebook
        self.status_bar = status_bar
        self.root = root
        # Caminho da pasta save_file
        self.file_dir = Path(__file__).parent.parent.joinpath("save_file")

        self.frame = Frame(self.my_notebook)
        self.frame.pack(fill="both", expand=1)

        # Scrollbar vertical da Text box
        self.ver_scroll = ttk.Scrollbar(self.frame, orient="vertical")
        self.ver_scroll.pack(side="right", fill="y")

        # Scrollbar horizontal da Text box
        self.hor_scroll = ttk.Scrollbar(self.frame, orient="horizontal")
        self.hor_scroll.pack(side="bottom", fill="x")

        # Text Box
        self.my_text = Text(
            self.frame,
            width=97,
            height=23,
            font=("Helvetica", 16),
            selectbackground="yellow",
            selectforeground="black",
            undo=True,
            yscrollcommand=self.ver_scroll.set,
            xscrollcommand=self.hor_scroll.set,
            wrap="none",
        )
        self.my_text.pack()

        # Configuração das Scrollbars
        self.ver_scroll.config(command=self.my_text.yview)
        self.hor_scroll.config(command=self.my_text.xview)

        self.my_notebook.add(self.frame, text="New File")

        # Seta variável para o arquivo aberto
        self.open_status_name = open_status_name

        # Seta variável do texto selecionado
        self.selected = False

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
            name = os.path.basename(name)
            self.root.title(f"{name} - TextPad")
            self.change_text(name)

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
            name = os.path.basename(name)
            self.root.title(f"{name} - TextPad")
            self.change_text(name)

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

    def close_tab(self, _=None):
        self.frame.destroy()

    def _edit_undo(self):
        self.my_text.edit_undo()

    def _edit_redo(self):
        self.my_text.edit_redo()

    def debug(self, _=None):
        self.my_text.config(height=13)

        fr = Frame(self.frame)
        fr.pack(fill="both", expand=1)
        # Scrollbar vertical da Text box
        ver_scroll = ttk.Scrollbar(fr, orient="vertical")
        ver_scroll.pack(side="right", fill="y")

        # Text Box
        my_text = Text(
            fr,
            width=97,
            height=10,
            font=("Helvetica", 16),
            selectbackground="yellow",
            selectforeground="black",
            undo=True,
            yscrollcommand=self.ver_scroll.set,
            wrap="none",
        )
        my_text.insert(INSERT, "Successful Execution!")
        my_text.config(state=DISABLED)
        my_text.pack(side="bottom")

        # Configuração das Scrollbars
        ver_scroll.config(command=my_text.yview)


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("TextPad")
        self.root.geometry("1200x680")

        self.root.option_add("*tearOff", False)

        self.style = ttk.Style(self.root)

        # dir_path = os.path.dirname(os.path.realpath(__file__))

        self.dir_path = Path(__file__).parent.joinpath("themes")
        self.root.tk.call("source", os.path.join(self.dir_path, "forest-dark.tcl"))

        self.style.theme_use("forest-dark")

        self.root.resizable(False, False)

        self.my_notebook = ttk.Notebook(self.root)
        self.my_notebook.pack(pady=15)

        # Adiciona Status Bar na parte de baixo da página
        self.status_bar = Label(self.root, text="Ready      ", anchor=E)
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=15)

        self.tabs = []

        tab = Tab_editor(self.my_notebook, self.status_bar, self.root)
        self.tabs.append(tab)

        # Menu
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)

        # Adiciona arquivo Menu
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(
            label="New File...", command=self.new_file, accelerator="Ctrl+N"
        )
        self.file_menu.add_command(
            label="Open File...", command=self.open_file, accelerator="Ctrl+O"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Save", command=self.save_file, accelerator="Ctrl+S"
        )
        self.file_menu.add_command(
            label="Save As...        ",
            command=self.save_as_file,
            accelerator="Ctrl+F",
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Close Tab", command=self.close_tab, accelerator="Ctrl+F4"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Adiciona Edit Menu
        self.edit_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="File", menu=self.edit_menu)
        self.edit_menu.add_command(
            label="Cut", command=lambda: self.cut_text(False), accelerator="Ctrl+X"
        )
        self.edit_menu.add_command(
            label="Copy",
            command=lambda: self.copy_text(False),
            accelerator="Ctrl+C",
        )
        self.edit_menu.add_command(
            label="Paste        ",
            command=lambda: self.paste_text(False),
            accelerator="Ctrl+V",
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Undo", command=self._edit_undo, accelerator="Ctrl+Z"
        )
        self.edit_menu.add_command(
            label="Redo", command=self._edit_redo, accelerator="Ctrl+Y"
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Select All", command=self.select_all, accelerator="Ctrl+A"
        )

        # Adiciona Run Menu
        self.run_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(
            label="Start Debugging", command=self.debug, accelerator="F5"
        )

        # Atalhos de Edit
        self.root.bind("<Control-Key-x>", self.cut_text)
        self.root.bind("<Control-Key-c>", self.copy_text)
        self.root.bind("<Control-Key-v>", self.paste_text)
        self.root.bind("<Control-Key-a>", self.select_all)

        # Atalhos de File
        self.root.bind("<Control-Key-n>", self.new_file)
        self.root.bind("<Control-Key-o>", self.open_file)
        self.root.bind("<Control-Key-s>", self.save_file)
        self.root.bind("<Control-Key-f>", self.save_as_file)
        self.root.bind("<Control-F4>", self.close_tab)

        # Atalhos de Run
        self.root.bind("<F5>", self.debug)

    def debug(self, _=None):
        tab = self.get_tab()
        tab.debug()

    def get_tab(self):
        idx = self.my_notebook.index(self.my_notebook.select())
        tab = self.tabs[idx]
        return tab

    def new_file(self, _=None):
        tab = Tab_editor(self.my_notebook, self.status_bar, self.root)
        self.tabs.append(tab)

        self.root.title("New File - TextPad")
        self.status_bar.config(text="New File        ")

    def open_file(self, _=None):
        tab = self.get_tab()
        tab.open_file()

    def save_file(self, _=None):
        tab = self.get_tab()
        tab.save_file()

    def save_as_file(self, _=None):
        tab = self.get_tab()
        tab.save_as_file()

    def close_tab(self, _=None):
        if len(self.tabs) != 1:
            tab = self.get_tab()
            tab.close_tab()

    def cut_text(self, e):
        # Se é ativado ou não o atalho
        if e:
            tab = self.get_tab()
            tab.cut_text(e)

    def copy_text(self, e):
        # Se é ativado ou não o atalho
        if e:
            tab = self.get_tab()
            tab.copy_text(e)

    def paste_text(self, e):
        # Se é ativado ou não o atalho
        if e:
            tab = self.get_tab()
            tab.paste_text(e)

    def _edit_undo(self):
        tab = self.get_tab()
        tab._edit_undo()

    def _edit_redo(self):
        tab = self.get_tab()
        tab._edit_redo()

    def select_all(self, _=None):
        tab = self.get_tab()
        tab.select_all()

    def startApp(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.startApp()
