# Py_to_C_Lexer

ANALISADOR LÉXICO PYTHON → C
=============================

COMO USAR:

1. Execute o lexer com um arquivo Python:
   python lexer.py exemplo.py

2. Para salvar os tokens em um arquivo:
   python lexer.py exemplo.py --output

ARQUIVOS GERADOS:
- exemplo_tokens.txt (quando usar --output)

EXEMPLO DE SAÍDA:
  1 | COMMENT_C          → #
  2 | STRING_C           → Calculadora simples em Python
  3 | KEYWORD_C          → // Função:
  4 | NAME_C             → calcular
  ...