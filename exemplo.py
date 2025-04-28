# Calculadora simples em Python
def calcular(a, b):
    soma = a + b
    diferenca = a - b
    produto = a * b
    
    if b != 0:
        divisao = a / b
    else:
        divisao = None
    
    resultados = {
        'soma': soma,
        'diferenca': diferenca,
        'produto': produto,
        'divisao': divisao
    }
    
    print("Resultados:", resultados)
    return resultados

# Teste
calcular(10, 5)