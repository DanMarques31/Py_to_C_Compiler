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
        }
        
        self.token_descriptions = {
            'COMMENT': 'Comentário',
            'NAME': 'Identificador',
            'NUMBER': 'Número',
            'STRING': 'String',
            'LPAR': 'Abre Parêntese',
            'RPAR': 'Fecha Parêntese',
            'LBRACE': 'Abre Chave',
            'RBRACE': 'Fecha Chave',
            'LSQB': 'Abre Colchete',
            'RSQB': 'Fecha Colchete',
            'COLON': 'Dois Pontos',
            'COMMA': 'Vírgula',
            'SEMI': 'Ponto e Vírgula',
            'PLUS': 'Operador +',
            'MINUS': 'Operador -',
            'STAR': 'Operador *',
            'SLASH': 'Operador /',
            'VBAR': 'Operador |',
            'AMPER': 'Operador &',
            'LESS': 'Operador <',
            'GREATER': 'Operador >',
            'EQUAL': 'Operador =',
            'PERCENT': 'Operador %',
            'EQEQUAL': 'Operador ==',
            'NOTEQUAL': 'Operador !=',
            'LESSEQUAL': 'Operador <=',
            'GREATEREQUAL': 'Operador >=',
            'LEFTSHIFT': 'Operador <<',
            'RIGHTSHIFT': 'Operador >>',
        }
        
        self.ignore_tokens = {'ENCODING', 'ENDMARKER', 'INDENT', 'DEDENT', 'NL'}

    def get_token_description(self, token_type, token_value):
        """Retorna a descrição do token"""
        if token_type == 'OP':
            if token_value == '(': return 'Abre Parêntese'
            if token_value == ')': return 'Fecha Parêntese'
            if token_value == '{': return 'Abre Chave'
            if token_value == '}': return 'Fecha Chave'
            if token_value == '[': return 'Abre Colchete'
            if token_value == ']': return 'Fecha Colchete'
            if token_value == ':': return 'Dois Pontos'
            if token_value == ',': return 'Vírgula'
            if token_value == ';': return 'Ponto e Vírgula'
            if token_value in self.keyword_map: return 'Operador ' + token_value
            return 'Operador'
        
        return self.token_descriptions.get(token_type, token_type)

    def tokenize(self, python_code):
        """Converte código Python para tokens C"""
        tokens = []
        try:
            code_bytes = BytesIO(python_code.encode('utf-8')).readline
            for tok in tokenize.tokenize(code_bytes):
                original_type = tokenize.tok_name[tok.type]
                value = tok.string
                
                if original_type in self.ignore_tokens:
                    continue
                
                if original_type == 'COMMENT':
                    tokens.append(('Comentário', '//' + value[1:]))
                elif original_type == 'NAME' and value in self.keyword_map:
                    tokens.append(('Palavra-chave C', self.keyword_map[value]))
                elif original_type == 'STRING':
                    tokens.append(('String', value))
                elif original_type == 'NUMBER':
                    tokens.append(('Número', value))
                elif original_type == 'OP':
                    desc = self.get_token_description(original_type, value)
                    if value in self.keyword_map:
                        tokens.append((desc, self.keyword_map[value]))
                    else:
                        tokens.append((desc, value))
                else:
                    desc = self.get_token_description(original_type, value)
                    tokens.append((desc, value))
        
        except tokenize.TokenError as e:
            print(f"Erro na tokenização: {e}", file=sys.stderr)
        return tokens

    def print_tokens(self, tokens):
        """Exibe os tokens formatados"""
        print("\nTOKENS GERADOS (Python → C):")
        print("="*70)
        print(f"{'Nº':<5} | {'TIPO':<25} | {'VALOR':<30}")
        print("="*70)
        for i, (token_type, value) in enumerate(tokens, 1):
            print(f"{i:<5} | {token_type:<25} | {value:<30}")
        print("="*70)

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