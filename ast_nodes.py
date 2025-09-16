# ast_nodes.py

class Node:
    """Nó base para todos os nós da AST. Agora armazena o token de origem."""
    def __init__(self, token):
        self.token = token
        # Extrai linha e coluna para acesso fácil
        if token:
            self.line = token[2]
            self.col = token[3]
        else:
            self.line = 0
            self.col = 0

class ProgramNode(Node):
    """Representa o programa inteiro."""
    def __init__(self, statements):
        super().__init__(token=None) # Nó raiz não corresponde a um token específico
        self.statements = statements

class AssignmentNode(Node):
    """Representa uma atribuição: variavel = expressao."""
    def __init__(self, variable_node, expression_node, token):
        super().__init__(token) # O token do operador '='
        self.variable = variable_node
        self.expression = expression_node

class BinOpNode(Node):
    """Representa uma operação binária: esquerda OPERADOR direita."""
    def __init__(self, left, op_token, right):
        super().__init__(op_token) # O token do operador: '+', '*', etc.
        self.left = left
        self.op = op_token[1]
        self.right = right

class IfNode(Node):
    """Representa um comando if-else."""
    def __init__(self, condition, if_block, else_block, token):
        super().__init__(token) # O token 'if'
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block
        
class ForNode(Node):
    """Representa um laço for."""
    def __init__(self, iterator_var, iterable_var, body, token):
        super().__init__(token) # O token 'for'
        self.iterator_var = iterator_var
        self.iterable_var = iterable_var
        self.body = body

class PrintNode(Node):
    """Representa uma chamada a printf."""
    def __init__(self, args, token):
        super().__init__(token) # O token 'printf'
        self.args = args

class VariableNode(Node):
    """Representa o uso de uma variável."""
    def __init__(self, token):
        super().__init__(token)
        self.name = token[1]

class NumberNode(Node):
    """Representa um literal numérico."""
    def __init__(self, token):
        super().__init__(token)
        self.value = token[1]

class StringNode(Node):
    """Representa um literal de string."""
    def __init__(self, token):
        super().__init__(token)
        self.value = token[1]

class ListNode(Node):
    """Representa a criação de uma lista."""
    def __init__(self, elements, token):
        super().__init__(token) # O token '['
        self.elements = elements

class DictNode(Node):
    """Representa a criação de um dicionário (não traduzível)."""
    def __init__(self, pairs, token):
        super().__init__(token)
        self.pairs = pairs

class DictItemNode(Node):
    """Representa um par chave-valor em um dicionário."""
    def __init__(self, key, value, token):
        super().__init__(token) # O token ':'
        self.key = key
        self.value = value