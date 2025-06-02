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

        self.ignore_tokens = {'ENCODING', 'ENDMARKER', 'INDENT', 'DEDENT', 'NL'}

    def get_token_description(self, token_type, token_value):
        if token_type == 'OP':
            return self.operator_descriptions.get(token_value, f'Operador {token_value}')
        
        if token_type == 'NAME' and token_value in self.keyword_map:
            return 'Palavra-chave C'
        
        return {
            'COMMENT': 'Comentário',
            'NAME': 'Identificador',
            'NUMBER': 'Número',
            'STRING': 'String',
        }.get(token_type, token_type)

    def tokenize(self, python_code):
        tokens = []
        try:
            code_bytes = BytesIO(python_code.encode('utf-8')).readline
            for tok in tokenize.tokenize(code_bytes):
                original_type = tokenize.tok_name[tok.type]
                value = tok.string
                line, column = tok.start

                if original_type in self.ignore_tokens:
                    continue

                if original_type == 'COMMENT':
                    tokens.append(('Comentário', '//' + value[1:], line, column))
                elif original_type == 'NAME' and value in self.keyword_map:
                    tokens.append(('Palavra-chave C', self.keyword_map[value], line, column))
                elif original_type == 'STRING':
                    tokens.append(('String', value, line, column))
                elif original_type == 'NUMBER':
                    tokens.append(('Número', value, line, column))
                elif original_type == 'OP':
                    desc = self.get_token_description(original_type, value)
                    if value in self.keyword_map:
                        tokens.append((desc, self.keyword_map[value], line, column))
                    else:
                        tokens.append((desc, value, line, column))
                else:
                    desc = self.get_token_description(original_type, value)
                    tokens.append((desc, value, line, column))

        except tokenize.TokenError as e:
            print(f"Erro na tokenização: {e}", file=sys.stderr)
        return tokens

    def print_tokens(self, tokens):
        print("\nTOKENS GERADOS (Python → C):")
        print("="*90)
        print(f"{'Nº':<5} | {'TIPO':<25} | {'VALOR EM C':<20} | {'LINHA':<5} | {'COLUNA':<6}")
        print("="*90)
        for i, (token_type, value, line, column) in enumerate(tokens, 1):
            print(f"{i:<5} | {token_type:<25} | {value:<20} | {line:<5} | {column:<6}")
        print("="*90)

def main():
    lexer = PythonToCLexer()
    input_file = sys.argv[1]

    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    print(f"\nANALISANDO: {input_file}")
    print("="*70)
    print(code.strip())
    print("="*70)

    tokens = lexer.tokenize(code)
    lexer.print_tokens(tokens)

if __name__ == "__main__":
    main()
