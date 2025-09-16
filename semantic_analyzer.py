# semantic_analyzer.py

from ast_nodes import *

TIPO_NUMERO = 'numero'
TIPO_STRING = 'string'
TIPO_ARRAY_NUMERO = 'array_numero'
TIPO_BOOL = 'booleano'
TIPO_INDEFINIDO = 'indefinido'

class SemanticError(Exception):
    def __init__(self, message, line=None, col=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col

    def __str__(self):
        if self.line is not None and self.col is not None:
            return f"Erro Semântico na linha {self.line}, coluna {self.col}: {self.message}"
        return f"Erro Semântico: {self.message}"

class TabelaDeSimbolos:
    def __init__(self):
        self.simbolos = {}

    def declarar(self, nome, tipo):
        if nome in self.simbolos:
            pass
        self.simbolos[nome] = {'tipo': tipo}

    def consultar(self, nome):
        simbolo = self.simbolos.get(nome)
        if not simbolo:
            # O erro é lançado aqui, mas será capturado e enriquecido com linha/coluna
            raise SemanticError(f"Variável '{nome}' não foi declarada antes do uso.")
        return simbolo

    def definir_tipo(self, nome, tipo):
        self.simbolos[nome] = {'tipo': tipo}

class AnalisadorSemantico:
    def __init__(self, ast):
        self.ast = ast
        self.tabela_de_simbolos = TabelaDeSimbolos()

    def analisar(self):
        self.visit(self.ast)
        return self.tabela_de_simbolos

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return

    def visit_ProgramNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_AssignmentNode(self, node):
        nome_variavel = node.variable.name
        tipo_expressao = self.visit(node.expression)
        self.tabela_de_simbolos.definir_tipo(nome_variavel, tipo_expressao)

    def visit_BinOpNode(self, node):
        tipo_esquerda = self.visit(node.left)
        tipo_direita = self.visit(node.right)
        
        operadores_numericos = ['+', '-', '*', '/', '%']
        operadores_logicos = ['<', '>', '==', '!=', '<=', '>=']

        if node.op in operadores_numericos:
            if tipo_esquerda != TIPO_NUMERO or tipo_direita != TIPO_NUMERO:
                raise SemanticError(
                    f"Operação '{node.op}' inválida entre os tipos '{tipo_esquerda}' e '{tipo_direita}'.",
                    line=node.line, col=node.col
                )
            return TIPO_NUMERO
        elif node.op in operadores_logicos:
            if tipo_esquerda != tipo_direita and (tipo_esquerda != TIPO_NUMERO or tipo_direita != TIPO_NUMERO):
                 raise SemanticError(
                    f"Comparação '{node.op}' inválida entre os tipos '{tipo_esquerda}' e '{tipo_direita}'.",
                    line=node.line, col=node.col
                )
            return TIPO_BOOL
        
        raise SemanticError(f"Operador desconhecido: {node.op}", line=node.line, col=node.col)

    def visit_IfNode(self, node):
        self.visit(node.condition)
        self.visit(node.if_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_ForNode(self, node):
        tipo_iteravel = self.visit(node.iterable_var)
        if tipo_iteravel != TIPO_ARRAY_NUMERO:
            raise SemanticError(f"Só é possível iterar sobre um array de números (a variável '{node.iterable_var.name}' é do tipo '{tipo_iteravel}').",
            line=node.iterable_var.line, col=node.iterable_var.col)
        self.tabela_de_simbolos.definir_tipo(node.iterator_var.name, TIPO_NUMERO)
        self.visit(node.body)

    def visit_PrintNode(self, node):
        for arg in node.args:
            self.visit(arg)

    def visit_VariableNode(self, node):
        try:
            simbolo = self.tabela_de_simbolos.consultar(node.name)
            return simbolo['tipo']
        except SemanticError as e:
            raise SemanticError(str(e), line=node.line, col=node.col)

    def visit_NumberNode(self, node):
        return TIPO_NUMERO

    def visit_StringNode(self, node):
        return TIPO_STRING

    def visit_ListNode(self, node):
        if not node.elements:
            return TIPO_ARRAY_NUMERO
        
        primeiro_tipo = self.visit(node.elements[0])
        if primeiro_tipo != TIPO_NUMERO:
            raise SemanticError("Listas só podem conter números nesta versão.", line=node.elements[0].line, col=node.elements[0].col)
        
        for elemento in node.elements[1:]:
            if self.visit(elemento) != primeiro_tipo:
                raise SemanticError("Todos os elementos da lista devem ser do mesmo tipo.", line=elemento.line, col=elemento.col)
        return TIPO_ARRAY_NUMERO
        
    def visit_DictNode(self, node):
        return TIPO_INDEFINIDO