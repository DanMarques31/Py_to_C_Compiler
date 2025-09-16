# py_to_c_parser.py

from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def error(self, mensagem):
        if self.current_token:
            _, valor, linha, coluna = self.current_token
            raise SyntaxError(f"{mensagem} na linha {linha}, coluna {coluna} ('{valor}')")
        else:
            raise SyntaxError(f"{mensagem} no final do arquivo")

    def expect(self, tipo_esperado, valor_esperado=None):
        token = self.current_token
        if token and token[0] == tipo_esperado and (valor_esperado is None or token[1] == valor_esperado):
            self.advance()
            return token
        else:
            valor_encontrado = f"'{token[1]}'" if token else "EOF"
            tipo_encontrado = f"'{token[0]}'" if token else ""
            self.error(f"Esperado '{valor_esperado or tipo_esperado}', encontrado {valor_encontrado} do tipo {tipo_encontrado}")

    def parse(self):
        statements = []
        while self.current_token and self.current_token[0] != 'DEDENT':
            statements.append(self.parse_comando())
        return ProgramNode(statements)

    def parse_bloco(self):
        self.expect('INDENT')
        statements = []
        while self.current_token and self.current_token[0] != 'DEDENT':
            statements.append(self.parse_comando())
        self.expect('DEDENT')
        return ProgramNode(statements)

    def parse_comando(self):
        token_type = self.current_token[0]
        if token_type == 'Identificador':
            return self.parse_atribuicao()
        if token_type == 'Palavra-chave C':
            if self.current_token[1] == 'if': return self.parse_if()
            if self.current_token[1] == 'for': return self.parse_for()
            if self.current_token[1] == 'printf': return self.parse_print()
        self.error("Comando ou declaração inválida")

    def parse_atribuicao(self):
        var_node = VariableNode(self.expect('Identificador'))
        op_token = self.expect('Operador =')
        expr_node = self.parse_expressao()
        return AssignmentNode(var_node, expr_node, token=op_token)

    def parse_expressao(self):
        return self.parse_comparacao()

    def parse_comparacao(self):
        node = self.parse_soma_sub()
        while self.current_token and self.current_token[1] in ('<', '>', '==', '!=', '<=', '>='):
            op_token = self.current_token; self.advance()
            right_node = self.parse_soma_sub()
            node = BinOpNode(left=node, op_token=op_token, right=right_node)
        return node

    def parse_soma_sub(self):
        node = self.parse_mult_div()
        while self.current_token and self.current_token[1] in ('+', '-'):
            op_token = self.current_token; self.advance()
            right_node = self.parse_mult_div()
            node = BinOpNode(left=node, op_token=op_token, right=right_node)
        return node

    def parse_mult_div(self):
        node = self.parse_fator()
        while self.current_token and self.current_token[1] in ('*', '/', '%'):
            op_token = self.current_token; self.advance()
            right_node = self.parse_fator()
            node = BinOpNode(left=node, op_token=op_token, right=right_node)
        return node

    def parse_fator(self):
        token = self.current_token
        if token[0] == 'Número': self.advance(); return NumberNode(token)
        if token[0] == 'String': self.advance(); return StringNode(token)
        if token[0] == 'Identificador': self.advance(); return VariableNode(token)
        if token[0] == 'Abre Parêntese':
            self.advance(); node = self.parse_expressao(); self.expect('Fecha Parêntese'); return node
        if token[0] == 'Abre Colchete': return self.parse_lista()
        self.error(f"Fator inesperado na expressão: {token[1]}")

    def parse_if(self):
        if_token = self.expect('Palavra-chave C', 'if')
        condicao = self.parse_expressao()
        self.expect('Dois Pontos')
        if_block = self.parse_bloco()
        else_block = None
        if self.current_token and self.current_token[1] == 'else':
            self.advance()
            self.expect('Dois Pontos')
            else_block = self.parse_bloco()
        return IfNode(condicao, if_block, else_block, token=if_token)

    def parse_for(self):
        for_token = self.expect('Palavra-chave C', 'for')
        iterator_var = VariableNode(self.expect('Identificador'))
        self.expect('Palavra-chave C', 'in')
        iterable_var = VariableNode(self.expect('Identificador'))
        self.expect('Dois Pontos')
        body = self.parse_bloco()
        return ForNode(iterator_var, iterable_var, body, token=for_token)

    def parse_print(self):
        print_token = self.expect('Palavra-chave C', 'printf')
        self.expect('Abre Parêntese')
        args = [self.parse_expressao()]
        while self.current_token and self.current_token[0] == 'Vírgula':
            self.advance()
            args.append(self.parse_expressao())
        self.expect('Fecha Parêntese')
        return PrintNode(args, token=print_token)

    def parse_lista(self):
        open_bracket_token = self.expect('Abre Colchete')
        elementos = []
        if self.current_token[0] != 'Fecha Colchete':
            elementos.append(self.parse_expressao())
            while self.current_token and self.current_token[0] == 'Vírgula':
                self.advance()
                elementos.append(self.parse_expressao())
        self.expect('Fecha Colchete')
        return ListNode(elementos, token=open_bracket_token)