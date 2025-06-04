class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def error(self, mensagem):
        if self.current_token:
            _, valor, linha, coluna = self.current_token
            raise SyntaxError(f"{mensagem} na linha {linha}, coluna {coluna}")
        else:
            raise SyntaxError(f"{mensagem} no final do arquivo")

    def expect(self, tipo_esperado, valor_esperado=None):
        if self.current_token and self.current_token[0] == tipo_esperado:
            if valor_esperado is None or self.current_token[1] == valor_esperado:
                self.advance()
            else:
                valor = self.current_token[1]
                self.error(f"Esperado '{valor_esperado}', encontrado '{valor}'")
        else:
            valor = self.current_token[1] if self.current_token else "EOF"
            self.error(f"Esperado '{tipo_esperado}', encontrado '{valor}'")

    def parse(self):
        while self.current_token is not None:
            self.parse_comando()

    def parse_comando(self):
        if self.current_token[0] == 'Identificador':
            self.parse_atribuicao()
        elif self.current_token[0] == 'Palavra-chave C' and self.current_token[1] == 'if':
            self.parse_if()
        elif self.current_token[0] == 'Palavra-chave C' and self.current_token[1] == 'for':
            self.parse_for()
        elif self.current_token[0] == 'Palavra-chave C' and self.current_token[1] == 'printf':
            self.parse_print()
        else:
            valor = self.current_token[1]
            self.error(f"Comando inesperado: '{valor}'")

    def parse_atribuicao(self):
        self.expect('Identificador')
        self.expect('Operador =')
        self.parse_expressao()

    def parse_if(self):
        self.expect('Palavra-chave C', 'if')
        self.parse_expressao()
        self.expect('Dois Pontos')
        self.parse_comando()

        if self.current_token and self.current_token[0] == 'Palavra-chave C' and self.current_token[1] == 'else':
            self.expect('Palavra-chave C', 'else')
            self.expect('Dois Pontos')
            self.parse_comando()

    def parse_for(self):
        self.expect('Palavra-chave C', 'for')
        self.expect('Identificador')
        self.expect('Palavra-chave C', 'in')
        self.expect('Identificador')
        self.expect('Dois Pontos')
        self.parse_comando()

    def parse_print(self):
        self.expect('Palavra-chave C', 'printf')
        self.expect('Abre Parêntese')
        self.parse_print_args()
        self.expect('Fecha Parêntese')

    def parse_print_args(self):
        self.parse_expressao()
        while self.current_token and self.current_token[0] == 'Vírgula':
            self.expect('Vírgula')
            self.parse_expressao()

    def parse_expressao(self):
        self.parse_termo()
        while self.current_token and (
            self.current_token[0] in ('Operador +', 'Operador -', 'Operador *', 'Operador /', 
                                      'Operador %', 'Operador <', 'Operador >', 
                                      'Operador !=', 'Operador ==') or 
            (self.current_token[0] == 'Palavra-chave C' and self.current_token[1] in ('and', 'or'))
        ):
            self.advance()
            self.parse_termo()

    def parse_termo(self):
        if self.current_token[0] in ('Número', 'String'):
            self.advance()
        elif self.current_token[0] == 'Identificador':
            self.advance()
        elif self.current_token[0] == 'Abre Parêntese':
            self.expect('Abre Parêntese')
            self.parse_expressao()
            self.expect('Fecha Parêntese')
        elif self.current_token[0] == 'Abre Colchete':
            self.parse_lista()
        elif self.current_token[0] == 'Abre Chave':
            self.parse_dicionario()
        else:
            valor = self.current_token[1]
            self.error(f"Termo inesperado: '{valor}'")

    def parse_lista(self):
        self.expect('Abre Colchete')
        if self.current_token and self.current_token[0] != 'Fecha Colchete':
            self.parse_expressao()
            while self.current_token and self.current_token[0] == 'Vírgula':
                self.expect('Vírgula')
                self.parse_expressao()
        self.expect('Fecha Colchete')

    def parse_dicionario(self):
        self.expect('Abre Chave')
        if self.current_token and self.current_token[0] != 'Fecha Chave':
            self.parse_chave_valor()
            while self.current_token and self.current_token[0] == 'Vírgula':
                self.expect('Vírgula')
                self.parse_chave_valor()
        self.expect('Fecha Chave')

    def parse_chave_valor(self):
        if self.current_token[0] in ('String', 'Identificador'):
            self.advance()
        else:
            valor = self.current_token[1]
            self.error(f"Esperado chave em dicionário, encontrado '{valor}'")
        self.expect('Dois Pontos')
        self.parse_expressao()
