from tkinter import *
from tkinter import filedialog
from tkinter import font

from sys import exit
from pathlib import Path
import os

root = Tk()
root.title("TextPad")
root.geometry("1200x680")

# Caminho da pasta save_file
file_dir = Path(__file__).parent.parent.joinpath("save_file")

# Seta variável para o arquivo aberto
global open_status_name
open_status_name = False

# Seta variável do texto selecionado
global selected
selected = False


# Cria New File Function
def new_file(e=True):
    # se é ativado ou não o atalho
    if e:
        # Exclui o texto anterior
        my_text.delete("1.0", END)
        # Atualiza status bars
        root.title("New File - TextPad")
        status_bar.config(text="New File        ")

        global open_status_name
        open_status_name = False


# Abre arquivo
def open_file(e=True):
    # se é ativado ou não o atalho
    if e:
        # Pega Filename
        text_file = filedialog.askopenfilename(
            initialdir=file_dir,
            title="Open File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
        )

        # Checa se é o filename
        if text_file:
            # Exclui o texto anterior
            my_text.delete("1.0", END)

            # Torna o filename global para que possa ser acessado depois
            global open_status_name
            open_status_name = text_file

            # Atualizando Status Bars
            name = text_file
            status_bar.config(text=f"{name}        ")
            name = os.path.basename(name)
            root.title(f"{name} - TextPad")

            # Abrindo o arquivo
            text_file = open(text_file, "r")
            stuff = text_file.read()
            # Adiciona o conteúdo do arquivo no textbox
            my_text.insert(END, stuff)
            # Fecha o arquivo
            text_file.close()


# Salva como arquivo
def save_as_file(e=True):
    # se é ativado ou não o atalho
    if e:
        text_file = filedialog.asksaveasfilename(
            defaultextension=".*",
            initialdir=file_dir,
            title="Save File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
        )
        if text_file:
            # Atualiza Status Bars
            name = text_file
            status_bar.config(text=f"Saved: {name}        ")
            name = os.path.basename(name)
            root.title(f"{name} - TextPad")

            # Salva o arquivo
            text_file = open(text_file, "w")
            text_file.write(my_text.get(1.0, END))
            # Fecha o arquivo
            text_file.close()


def save_file(e=True):
    # se é ativado ou não o atalho
    if e:
        global open_status_name
        if open_status_name:
            # Salva o arquivo
            text_file = open(open_status_name, "w")
            text_file.write(my_text.get(1.0, END))
            # Fecha o arquivo
            text_file.close()

            status_bar.config(text=f"Saved: {open_status_name}        ")
        else:
            save_as_file()


# Cut Text
def cut_text(e):
    global selected
    # Checa se foi usado os atalhos do teclado
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            # Pega o texto selecionado da text box
            selected = my_text.selection_get()
            # Exclui o que foi selecidonado na text box
            my_text.delete("sel.first", "sel.last")
            # Limpa o que estiver no clipboard
            root.clipboard_clear()
            # Passa o que foi selecionado para o clipboard
            root.clipboard_append(selected)


# Copy Text
def copy_text(e):
    global selected
    # Checa se foi usado os atalhos do teclado
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        # Pega o texto selecionado da text box
        selected = my_text.selection_get()
        # Limpa o que estiver no clipboard
        root.clipboard_clear()
        # Passa o que foi selecionado para o clipboard
        root.clipboard_append(selected)


# Paste Text
def paste_text(e):
    global selected
    # Checa se foi usado os atalhos do teclado
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


# Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Scrollbar vertical da Text box
ver_scroll = Scrollbar(my_frame)
ver_scroll.pack(side=RIGHT, fill=Y)

# Scrollbar horizontal da Text box
hor_scroll = Scrollbar(my_frame, orient="horizontal")
hor_scroll.pack(side=BOTTOM, fill=X)

# Text Box
my_text = Text(
    my_frame,
    width=97,
    height=25,
    font=("Helvetica", 16),
    selectbackground="yellow",
    selectforeground="black",
    undo=True,
    yscrollcommand=ver_scroll.set,
    xscrollcommand=hor_scroll.set,
    wrap="none",
)
my_text.pack()

# Configuração das Scrollbars
ver_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Adiciona arquivo Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New File...", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open File...", command=open_file, accelerator="Ctrl+O")
file_menu.add_separator()
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(
    label="Save As...        ", command=save_as_file, accelerator="Ctrl+F"
)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Adiciona Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=edit_menu)
edit_menu.add_command(
    label="Cut", command=lambda: cut_text(False), accelerator="Ctrl+X"
)
edit_menu.add_command(
    label="Copy", command=lambda: copy_text(False), accelerator="Ctrl+C"
)
edit_menu.add_command(
    label="Paste        ", command=lambda: paste_text(False), accelerator="Ctrl+V"
)
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="Ctrl+Y")

# Adiciona Status Bar na parte de baixo da página
status_bar = Label(root, text="Ready        ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# Atalhos de Edit
root.bind("<Control-Key-x>", cut_text)
root.bind("<Control-Key-c>", copy_text)
root.bind("<Control-Key-v>", paste_text)

# Atalhos de File
root.bind("<Control-Key-n>", new_file)
root.bind("<Control-Key-o>", open_file)
root.bind("<Control-Key-s>", save_file)
root.bind("<Control-Key-f>", save_as_file)

root.mainloop()
