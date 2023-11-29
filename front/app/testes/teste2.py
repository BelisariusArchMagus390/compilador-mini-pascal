import tkinter as tk


def on_scroll(*args):
    text.yview(*args)
    contador.yview(*args)


def on_mousewheel(event):
    text.yview_scroll(-1 * (event.delta // 120), "units")
    contador.yview_scroll(-1 * (event.delta // 120), "units")
    return "break"


def on_up_arrow(_=None):
    text.yview_scroll(-1, "units")
    contador.yview_scroll(-1, "units")
    return "break"


def on_down_arrow(_=None):
    text.yview_scroll(1, "units")
    contador.yview_scroll(1, "units")
    return "break"


def atualizar_contador(event):
    contador.configure(state=tk.NORMAL)
    contador.delete("1.0", tk.END)

    # Obtém o conteúdo da Text box
    conteudo = text.get("1.0", tk.END)

    # Divide o conteúdo em linhas e conta o número de linhas
    numero_linhas = conteudo.count("\n")

    # Insere os números das linhas no contador
    numeros_linhas = "\n".join(str(i) for i in range(1, numero_linhas + 1))
    contador.insert(tk.END, numeros_linhas)

    contador.configure(state=tk.DISABLED)


root = tk.Tk()
root.geometry("400x300")

# Cria uma scrollbar vertical
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
# Configura a scrollbar para controlar as duas Text boxes
scrollbar.config(command=on_scroll)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Cria uma Text box para o contador
contador = tk.Text(
    root, width=3, bg="lightgray", state=tk.DISABLED, yscrollcommand=scrollbar.set
)
contador.pack(side=tk.LEFT, fill=tk.Y)

# Cria uma Text box para o conteúdo do texto
text = tk.Text(root, wrap=tk.NONE, yscrollcommand=scrollbar.set)
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Cria o contador inicial
atualizar_contador(None)

# Configura os bindings para a rolagem do mouse e das setas do teclado
text.bind("<MouseWheel>", on_mousewheel)
# text.bind("<Up>", on_up_arrow)
# text.bind("<Down>", on_down_arrow)

# Configura o binding para atualizar o contador sempre que o conteúdo da Text box for modificado
text.bind("<KeyRelease>", atualizar_contador)

root.mainloop()
