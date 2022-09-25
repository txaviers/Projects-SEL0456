#include <stdio.h>
#include "fibonacci.h"

void main(){

    unsigned int n;
    int i;

    printf("Insira n maior que zero: ");
    scanf("%u", &n);
    printf("\n");

    //Mostra-se a sequência de Fibonacci até o n-ésimo termo escolhido 
    for(i = 1; i <= n; i++){
        printf("%u ", fibonacci(i));
    }

    printf("\n");
}