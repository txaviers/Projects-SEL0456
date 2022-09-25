#include "fibonacci.h"

unsigned int fibonacci(unsigned int n){
    
    int i, fib, a = 0, b = 1;
    
    for(i=0; i<n; i++){
        if(i==0){
            fib = 0;
        }
        else if(i==1){
            fib = 1;
        }   
        else{
            fib = a + b;
            a = b;
            b = fib;
        }
    }
    
    return fib;

}