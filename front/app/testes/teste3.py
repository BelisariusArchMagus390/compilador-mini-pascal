import tkinter as tk
from tkinter import ttk


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        if (
            command == "get"
            and (args[0] == "sel.first" and args[1] == "sel.last")
            and not self.tag_ranges("sel")
        ):
            return

        if (
            command == "delete"
            and (args[0] == "sel.first" and args[1] == "sel.last")
            and not self.tag_ranges("sel")
        ):
            return

        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)
        if (
            args[0] in ("insert", "replace", "delete")
            or args[0:3] == ("mark", "set", "insert")
            or args[0:2] == ("xview", "moveto")
            or args[0:2] == ("xview", "scroll")
            or args[0:2] == ("yview", "moveto")
            or args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")
        return result


class Tab_editor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TextPad")
        self.root.geometry("800x400")

        self.root.option_add("*tearOff", False)
        self.root.resizable(False, False)

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=1)

        self.ver_scroll = ttk.Scrollbar(self.frame, orient="vertical")
        self.hor_scroll = ttk.Scrollbar(self.frame, orient="horizontal")

        self.my_text = CustomText(
            self.frame,
            width=60,
            height=20,
            font=("Helvetica", 12),
            selectbackground="#b2b2b2",
            yscrollcommand=self.ver_scroll.set,
            xscrollcommand=self.hor_scroll.set,
            wrap="none",
        )

        self.linenumbers = tk.Text(
            self.frame,
            width=3,
            font=("Helvetica", 12),
            state=tk.DISABLED,
            yscrollcommand=self.ver_scroll.set,
        )

        self.ver_scroll.config(command=self.viewboth)
        self.hor_scroll.config(command=self.my_text.xview)

        self.ver_scroll.pack(side="right", fill="y")
        self.hor_scroll.pack(side="bottom", fill="x")
        self.linenumbers.pack(side="left", fill="y", expand=True)
        self.my_text.pack(side="top", fill="both", expand=True)

        self.linenumbers.tag_configure("center", justify="center")
        self.linenumbers.bind("<MouseWheel>", self.on_mousewheel_scrollbar)
        self.my_text.bind("<MouseWheel>", self.on_mousewheel_scrollbar)
        self.my_text.bind("<Configure>", self._on_change)

        self.root.mainloop()

    def _on_change(self, _=None):
        self.linenumbers.configure(state=tk.NORMAL)
        self.linenumbers.delete("1.0", tk.END)
        self.linenumbers.insert(tk.END, self.get_line_numbers())
        self.linenumbers.tag_add("center", "1.0", tk.END)
        self.linenumbers.configure(state=tk.DISABLED)

    def get_line_numbers(self):
        text = self.my_text.get("1.0", tk.END)
        line_number = text.count("\n")
        line_numbers = "\n".join(str(i) for i in range(1, line_number + 1))
        return line_numbers

    def viewboth(self, *args):
        self.my_text.yview(*args)
        self.linenumbers.yview(*args)

    def on_mousewheel_scrollbar(self, event):
        self.my_text.yview_scroll(-1 * (event.delta // 120), "units")
        self.linenumbers.yview_scroll(-1 * (event.delta // 120), "units")


if __name__ == "__main__":
    Tab_editor()
