# from tabulate import tabulate as tb


class Data:
    def __init__(
        self, id, lexema, tipo, valor, tam_array, param, chamada, memory_position
    ):
        self.id = id
        self.lexema = lexema
        self.tipo = tipo
        self.valor = valor
        self.tam_array = tam_array
        self.param = param
        self.chamada = chamada
        self.memory_position = memory_position
        self.data = [
            self.id,
            self.lexema,
            self.tipo,
            self.valor,
            self.tam_array,
            self.param,
            self.chamada,
            self.memory_position,
        ]

    def __str__(self):
        return str(self.data)


class Node(Data):
    def __init__(
        self,
        id=None,
        lexema=None,
        tipo=None,
        valor=None,
        tam_array=None,
        param=None,
        chamada=None,
        memory_position=None,
    ):
        super().__init__(
            id, lexema, tipo, valor, tam_array, param, chamada, memory_position
        )
        self.left = None
        self.right = None


class SymbolTable:
    def __init__(self, node=None):
        if node:
            self.root = node
        else:
            self.root = None
        self.node_matr = []

    def inorder_traversal_tree(self, node=None):
        if node is None:
            node = self.root
        if node.left:
            self.inorder_traversal_tree(node.left)
        self.node_matr.append(node.data)
        if node.right:
            self.inorder_traversal_tree(node.right)

    def table_show(self):
        self.inorder_traversal_tree()

        print("\nTABELA DE SÍMBOLOS: \n")

        columns = [
            "ID",
            "Lexema",
            "Tipo",
            "Valor",
            "Tamanho array",
            "Parâmetros",
            "Chamada function/procedure",
            "Posição na memória",
        ]
        # print(tb(self.node_matr, headers=columns, tablefmt="fancy_grid"))

    def insert(self, _id, _lexema, _memory_position=None):
        symbol = None
        x = self.root
        while x:
            symbol = x
            if _id < x.id:
                x = x.left
            else:
                x = x.right
        if symbol is None:
            self.root = Node(id=_id, lexema=_lexema, memory_position=_memory_position)
        elif _id < symbol.id:
            symbol.left = Node(id=_id, lexema=_lexema, memory_position=_memory_position)
        else:
            symbol.right = Node(
                id=_id, lexema=_lexema, memory_position=_memory_position
            )

    def search(self, id):
        return self._search(id, self.root)

    def _search(self, id, node):
        if node is None:
            return node
        if node.id == id:
            return node
        if id < node.id:
            return self._search(id, node.left)
        return self._search(id, node.right)

    # ID - 0 | Lexema - 1 | Tipo - 2 | Valor - 3 | Tamanho array - 4 |
    # Parâmetros - 5 | Chamada function/procedure - 6 | Posição na memória - 7

    def edit(self, id, collumn, value):
        node = self.search(id)
        node.data[collumn] = value

    def get_node_matr(self):
        self.inorder_traversal_tree()
        return self.node_matr
