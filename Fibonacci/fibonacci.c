#include "fibonacci.h"

//Função para encontrar o n-ésimo termo da Seq. de Fibonacci começando por 0
unsigned int fibonacci(unsigned int n){
    if(n==1){
        //Primeiro termo 
        return 0;        
    }
    else if(n==2){
        //Segundo termo 
        return 1;        
    }
    else{
        //Utiliza-se a expressão de recursão da sequência
        return fibonacci(n-1) + fibonacci(n-2); 
    }
}