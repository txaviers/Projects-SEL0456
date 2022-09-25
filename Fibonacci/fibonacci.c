#include "fibonacci.h"

//Função para encontrar o n-ésimo termo da Seq. de Fibonacci começando por 0
unsigned int fibonacci(unsigned int n){
    
    int i, fib, a = 0, b = 1;
    
    for(i=0; i<n; i++){
        //O primeiro termo é considerado como 0
        if(i==0){
            fib = 0;
        }
        //O segundo termo é então 1
        else if(i==1){
            fib = 1;
        }   
        //Segue-se os demais termos da sequência
        else{
            fib = a + b;
            a = b;
            b = fib;
        }
    }
    //Retorna-se o n-ésimo termo
    return fib;

}