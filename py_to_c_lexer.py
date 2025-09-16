import tokenize
from io import BytesIO
import sys

class PythonToCLexer:
    def __init__(self):
        self.keyword_map = {
            'print': 'printf',
            'and': '&&',
            'or': '||',
            'not': '!',
            'True': '1',
            'False': '0',
            'None': 'NULL',
            'def': 'Função',
            '#': '//',
            '**': 'pow',
            '//': '/',
            'if': 'if',
            'for': 'for',
            'else': 'else',
            'elif': 'else if',
            'while': 'while',
            'in': 'in'
        }

        self.operator_descriptions = {
            '+': 'Operador +',
            '-': 'Operador -',
            '*': 'Operador *',
            '/': 'Operador /',
            '%': 'Operador %',
            '=': 'Operador =',
            '<': 'Operador <',
            '>': 'Operador >',
            '==': 'Operador ==',
            '!=': 'Operador !=',
            '<=': 'Operador <=',
            '>=': 'Operador >=',
            '&&': 'Operador &&',
            '||': 'Operador ||',
            '!': 'Operador !',
            '(': 'Abre Parêntese',
            ')': 'Fecha Parêntese',
            '{': 'Abre Chave',
            '}': 'Fecha Chave',
            '[': 'Abre Colchete',
            ']': 'Fecha Colchete',
            ':': 'Dois Pontos',
            ',': 'Vírgula',
            ';': 'Ponto e Vírgula',
        }

        # MODIFICAÇÃO: 'INDENT' e 'DEDENT' não são mais ignorados.
        self.ignore_tokens = {'ENCODING', 'ENDMARKER', 'NL', 'NEWLINE', 'COMMENT'}

    def get_token_description(self, token_type, token_value):
        if token_type == 'OP':
            return self.operator_descriptions.get(token_value, f'Operador {token_value}')
        
        if token_type == 'NAME' and token_value in self.keyword_map:
            return 'Palavra-chave C'
        
        # Adicionado para reconhecer INDENT/DEDENT
        if token_type in ('INDENT', 'DEDENT'):
            return token_type

        return {
            'COMMENT': 'Comentário',
            'NAME': 'Identificador',
            'NUMBER': 'Número',
            'STRING': 'String',
        }.get(token_type, token_type)

    def tokenize(self, python_code):
        tokens = []
        try:
            # Adiciona uma nova linha no final para garantir que o último DEDENT seja gerado
            if not python_code.endswith('\n'):
                python_code += '\n'

            code_bytes = BytesIO(python_code.encode('utf-8')).readline
            for tok in tokenize.tokenize(code_bytes):
                original_type = tokenize.tok_name[tok.type]
                value = tok.string
                line, column = tok.start

                if original_type in self.ignore_tokens:
                    continue

                token_desc = self.get_token_description(original_type, value)

                if original_type == 'COMMENT':
                    tokens.append(('Comentário', '//' + value[1:], line, column))
                elif original_type == 'NAME' and value in self.keyword_map:
                    tokens.append(('Palavra-chave C', self.keyword_map[value], line, column))
                elif original_type == 'STRING':
                    tokens.append(('String', f'"{tok.string[1:-1]}"', line, column))
                else:
                    c_value = self.keyword_map.get(value, value)
                    tokens.append((token_desc, c_value, line, column))

        except tokenize.TokenError as e:
            print(f"Erro na tokenização: {e}", file=sys.stderr)
        return tokens