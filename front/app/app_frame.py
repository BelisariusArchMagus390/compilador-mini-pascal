from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from .tab import Tab_editor
import os


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("TextPad")
        self.root.geometry("1200x680")

        self.root.option_add("*tearOff", False)

        self.style = ttk.Style(self.root)

        self.dir_path = Path(__file__).parent.joinpath("themes")
        self.root.tk.call("source", os.path.join(self.dir_path, "forest-light.tcl"))
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
            label="Execute", command=self.execute, accelerator="F5"
        )
        self.run_menu.add_separator()
        self.run_menu.add_command(
            label="Close Terminal",
            command=self.close_output_terminal,
            accelerator="Ctrl+F3",
        )

        # Adiciona View Menu
        self.view = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="View", menu=self.view)
        self.view.add_command(
            label="Dark Mode", command=self.change_theme_dark, accelerator="Crtl+D"
        )
        self.view.add_command(
            label="Light Mode",
            command=self.change_theme_light,
            accelerator="Ctrl+L",
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
        self.root.bind("<F5>", self.execute)
        self.root.bind("<Control-F3>", self.close_output_terminal)

        # Atalhos de View
        self.root.bind("<Control-Key-d>", self.change_theme_dark)
        self.root.bind("<Control-Key-l>", self.change_theme_light)

        # Associando a função ao evento de mudança de tab
        self.my_notebook.bind("<<NotebookTabChanged>>", self.on_tab_text_change)

    def on_tab_text_change(self, event):
        tab = self.get_tab()
        self.status_bar.config(text=f"{tab.get_text_status_bar()}        ")
        self.root.title(f"{tab.get_text_title()} - TextPad")

    def execute(self, _=None):
        tab = self.get_tab()
        tab.execute()

    def close_output_terminal(self, _=None):
        tab = self.get_tab()
        tab.close_output_terminal()

    def get_tab(self):
        idx = self.my_notebook.index(self.my_notebook.select())
        tab = self.tabs[idx]
        return tab

    def new_file(self, _=None):
        tab = Tab_editor(self.my_notebook, self.status_bar, self.root)
        self.tabs.append(tab)

        # self.root.title("New File - TextPad")
        # self.status_bar.config(text="New File        ")

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

    def change_theme_light(self):
        bg_color = "#ffffff"
        fg_color = "#313131"

        self.style.theme_use("forest-light")
        self.root.configure(background=bg_color)
        self.status_bar.configure(background=bg_color, fg=fg_color)
        tab = self.get_tab()
        tab.change_color(bg_color, fg_color)

    def change_theme_dark(self):
        bg_color = "#313131"
        fg_color = "#ffffff"

        self.style.theme_use("forest-dark")
        self.root.configure(background=bg_color)
        self.status_bar.configure(background=bg_color, fg=fg_color)
        tab = self.get_tab()
        tab.change_color(bg_color, fg_color)

    def startApp(self):
        self.root.mainloop()
