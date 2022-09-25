#include "fibonacci.h"

//Função para encontrar o n-ésimo termo da Seq. de Fibonacci começando por 0
unsigned int fibonacci(unsigned int n){

    //Primeiro termo da sequência
    if(n==1){
        return 0;        
    }
    //Segundo termo da sequência
    else if(n==2){
        return 1;        
    }
    else{
        //Utilizasse a expressão de recursão da sequência
        return fibonacci(n-1) + fibonacci(n-2); 
    }
}

