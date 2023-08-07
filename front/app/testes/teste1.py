import tkinter as tk
from tkinter import *
from tkinter import ttk

# Créditos do código das classes TextLineNumbers e CustomText abaixo para Bryan Oakley
# (Com certas modificações minhas):
# https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget


class TextLineNumbers(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, _=None):
        self.configure(state=NORMAL)
        self.delete("1.0", END)

        # Obtém o conteúdo da Text box
        text = self.textwidget.get("1.0", END)

        # Divide o conteúdo em linhas e conta o número de linhas
        line_number = text.count("\n")

        # Insere os números das linhas no self
        line_numbers = "\n".join(str(i) for i in range(1, line_number + 1))
        self.insert(END, line_numbers)

        self.tag_configure("center", justify="center")
        self.tag_add("center", "1.0", END)

        self.configure(state=tk.DISABLED)


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        # avoid error when copying
        if (
            command == "get"
            and (args[0] == "sel.first" and args[1] == "sel.last")
            and not self.tag_ranges("sel")
        ):
            return

        # avoid error when deleting
        if (
            command == "delete"
            and (args[0] == "sel.first" and args[1] == "sel.last")
            and not self.tag_ranges("sel")
        ):
            return

        # let the actual widget perform the requested action
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (
            args[0] in ("insert", "replace", "delete")
            or args[0:3] == ("mark", "set", "insert")
            or args[0:2] == ("xview", "moveto")
            or args[0:2] == ("xview", "scroll")
            or args[0:2] == ("yview", "moveto")
            or args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


class Tab_editor:
    def __init__(self):
        self.root = Tk()
        self.root.title("TextPad")
        self.root.geometry("1200x680")

        self.root.option_add("*tearOff", False)

        self.root.resizable(False, False)

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=1)

        # Scrollbar vertical da Text box
        self.ver_scroll = ttk.Scrollbar(self.frame, orient="vertical")

        # Scrollbar horizontal da Text box
        self.hor_scroll = ttk.Scrollbar(self.frame, orient="horizontal")

        # Text Box
        self.my_text = CustomText(
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
        self.ver_scroll.config(command=self.viewboth)
        self.hor_scroll.config(command=self.my_text.xview)

        # Pack dos Scrollbars
        self.ver_scroll.pack(side="right", fill="y")
        self.hor_scroll.pack(side="bottom", fill="x")

        #
        self.linenumbers = TextLineNumbers(
            self.frame,
            width=3,
            font=("Helvetica", 16),
            state=DISABLED,
            yscrollcommand=self.ver_scroll.set,
        )
        self.linenumbers.configure(highlightthickness=0)
        self.linenumbers.attach(self.my_text)

        self.linenumbers.pack(side="left", fill="y", expand=True)
        self.my_text.pack(side="top", fill="both", expand=True)

        # Seta variável do texto selecionado
        self.selected = False

        self.fr_output = Frame()
        self.txt_box_output = Text()

        self.my_text.bind("<<Change>>", self._on_change)
        self.my_text.bind("<Configure>", self._on_change)

        self.my_text.bind("<MouseWheel>", self.on_mousewheel_scrollbar)
        self.my_text.bind("<Up>", self.up_scrollbar)
        self.my_text.bind("<Down>", self.down_scrollbar)
        self.my_text.bind("<Left>", self.up_scrollbar)
        self.my_text.bind("<Right>", self.down_scrollbar)

        self.my_text.focus_set()

        self.root.mainloop()

    def _on_change(self, _=None):
        self.linenumbers.redraw()

    def viewboth(self, *args):
        self.my_text.yview(*args)
        self.linenumbers.yview(*args)

    def on_mousewheel_scrollbar(self, event):
        self.my_text.yview_scroll(-1 * (event.delta // 120), "units")
        self.linenumbers.yview_scroll(-1 * (event.delta // 120), "units")
        return "break"

    """def verify_end_line(self):
        actual_local_cursor = self.my_text.index(INSERT)
        next_local_cursor = self.my_text.index(f"{actual_local_cursor} + 1 char")

        actual_line, actual_column = map(int, actual_local_cursor.split("."))
        next_line, next_column = map(int, next_local_cursor.split("."))

        # print("actual_local_cursor: ", actual_line)
        # print("next_local_cursor: ", next_line)

        if next_line > actual_line:
            return True  # , next_line, next_column
        else:
            return False  # , None, None

        # return True if next_line > actual_line else False"""

    def up_scrollbar(self, _=None):
        # Obtém a posição do cursor
        cursor_pos = self.my_text.index(INSERT)

        # Obtém o número de caracteres na linha atual
        line_end = self.my_text.index(f"{cursor_pos.line + 1}.end")

        # Se o cursor estiver no fim da linha, faz a rolagem
        if cursor_pos == line_end:
            self.my_text.yview_scroll(-1, "units")
            self.linenumbers.yview_scroll(-1, "units")
        return "break"

    def down_scrollbar(self, _=None):
        # Obtém a posição do cursor
        cursor_pos = self.my_text.index(INSERT)

        # Obtém o número de caracteres na linha atual
        line_end = self.my_text.index(f"{cursor_pos.line + 1}.end")

        # Se o cursor estiver no fim da linha, faz a rolagem
        if cursor_pos == line_end:
            self.my_text.yview_scroll(1, "units")
            self.linenumbers.yview_scroll(1, "units")
        return "break"

    """def up_scrollbar(self, _=None):
        result, next_line, next_column = self.verify_end_line()
        print(result)
        if result == True:
            self.my_text.yview_scroll(-1, "units")
            self.linenumbers.yview_scroll(-1, "units")

            self.my_text.see(f"{next_line}.{next_column}")
            self.my_text.focus_set()

            return "break"

    def down_scrollbar(self, _=None):
        result, next_line, next_column = self.verify_end_line()
        print(result)
        if result == True:
            self.my_text.yview_scroll(1, "units")
            self.linenumbers.yview_scroll(1, "units")

            self.my_text.see(f"{next_line}.{next_column}")
            self.my_text.focus_set()

            return "break"
"""


if __name__ == "__main__":
    Tab_editor()
