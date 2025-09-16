#include <stdio.h>
#include <stdbool.h>

int main() {
    double a;
    double b;
    double item;
    double soma;

    a = (5 + (3 * 2));
    b = ((a + 1) / 3);
    printf("%s %f\n", "O valor de a e:", a);
    printf("%s %f\n", "O valor de b e:", b);
    if ((b > 3)) {
        printf("%s\n", "b e maior que 3");
    } else {
        printf("%s\n", "b nao e maior que 3");
    }
    printf("%s\n", "--- Contagem ---");
    double numeros[] = {10.5, 20.2, 30.8, 40.1};
    soma = 0;
    int size_numeros = sizeof(numeros) / sizeof(numeros[0]);
    for (int i = 0; i < size_numeros; i++) {
        item = numeros[i];
        printf("%s %f\n", "Item atual:", item);
        soma = (soma + item);
    }
    printf("%s %f\n", "A soma dos itens e:", soma);

    return 0;
}