# Py_to_C_Lexer

ANALISADOR LÉXICO PYTHON → C
=============================

COMO USAR:

1. Execute o lexer com um arquivo Python:
   python lexer.py exemplo.py

EXEMPLO DE SAÍDA:
  1 | COMMENT_C          → #
  2 | STRING_C           → Calculadora simples em Python
  3 | KEYWORD_C          → // Função:
  4 | NAME_C             → calcular
  ...