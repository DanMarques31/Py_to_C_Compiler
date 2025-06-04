from py_to_c_lexer import PythonToCLexer
from py_to_c_parser import Parser
import sys

def main():
    lexer = PythonToCLexer()

    if len(sys.argv) < 2:
        print("Uso: python script.py <arquivo.py>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {input_file}")
        sys.exit(1)

    print(f"\nANALISANDO: {input_file}")
    print("=" * 70)
    print(code.strip())
    print("=" * 70)

    tokens = lexer.tokenize(code)
    lexer.print_tokens(tokens)

    # Parser
    try:
        parser = Parser(tokens)
        parser.parse()
        print("\n✅ Código válido sintaticamente!")
    except SyntaxError as e:
        print(f"\n❌ Erro de sintaxe: {e}")

if __name__ == "__main__":
    main()
