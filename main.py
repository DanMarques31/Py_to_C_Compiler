import sys
from py_to_c_lexer import PythonToCLexer
from py_to_c_parser import Parser
from semantic_analyzer import AnalisadorSemantico, SemanticError
from code_generator import CodeGenerator

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.py>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {input_file}")
        sys.exit(1)

    print(f"\nANALISANDO: {input_file}\n{'=' * 70}")
    print(code.strip())
    print("=" * 70)

    try:
        # --- FASE 1: ANÁLISE LÉXICA ---
        lexer = PythonToCLexer()
        tokens = lexer.tokenize(code)
        print("\n Fase 1: Análise Léxica concluída.")

        # --- FASE 2: ANÁLISE SINTÁTICA (parsing para AST) ---
        parser = Parser(tokens)
        ast_tree = parser.parse()
        print(" Fase 2: Análise Sintática concluída (AST gerada).")

        # --- FASE 3: ANÁLISE SEMÂNTICA ---
        semantic_analyzer = AnalisadorSemantico(ast_tree)
        tabela_de_simbolos = semantic_analyzer.analisar()
        print(" Fase 3: Análise Semântica concluída.")

        # --- FASE 4: GERAÇÃO DE CÓDIGO ---
        code_gen = CodeGenerator(tabela_de_simbolos)
        c_code = code_gen.generate(ast_tree)
        print(" Fase 4: Geração de Código C concluída.")
        
        print("\n CÓDIGO C FINAL GERADO:")
        print("-" * 70)
        print(c_code)
        print("-" * 70)

        output_file = input_file.replace('.py', '.c')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(c_code)
        print(f"\n Código salvo com sucesso em: {output_file}")

    except (SyntaxError, SemanticError) as e:
        print(f"\n ERRO DE COMPILAÇÃO: {e}")
    except Exception as e:
        print(f"\n Ocorreu um erro inesperado: {e}")
        
if __name__ == "__main__":
    main()