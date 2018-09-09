//This file will merge with Main .c 
#include "Network.h"

// Method to generate weights for a network
int **generatedWeights(int N, int K, int L, int M) {
    
    int **weights = malloc(K*sizeof(int*));
    
     // This loop handles num of perceptrons
    for(int i = 0; i < K; i++){
        
        int *values = malloc(M*sizeof(int));
        
         //This loop handles num of inputs per perceptron
        for(int j = 0; j < M; j++){
            
            // Generate random weight for the perceptron i
            values[j] = (rand() % (2 * L + 1) - L);
            
        }
        
        weights[i] = values;
    }
    
    return weights;
}


int *generatedInputs(int N, int *inputsArray) {
        
    // Generating the Inputs
    for (int i = 0; i < N; i++) {
        
        int r = rand() % 2;
        
        if (r == 0) {
            r = -1;
        }
        inputsArray[i] = r;
    }
    
    return inputsArray;
}



// struct manipulation for Main.c
struct Outputs generatedOutputs(int K, int M, int *pOutputs, int **weights, int *inputsArray) {
    
    int networkOutput = 1;
    
    // Outer loop handles num of perceptrons
    for (int i = 0; i < K; i++) {
        
        pOutputs[i] = 0;
        
        // Inner loop handles num of inputs per perceptron
        for (int j = 0; j < M; j++) {
            
            // Getting perceptron output
            pOutputs[i] = pOutputs[i] + (weights[i][j] * inputsArray[(i*M)+j]);
            
        }
        
        // Sign the output of perceptron in A
        if (pOutputs[i] <= 0) {
            pOutputs[i] = -1;
        }
        else {
            pOutputs[i] = 1;
        }
        
        networkOutput = networkOutput * pOutputs[i];
    }
    
    struct Outputs outputs;
    outputs.networkOutput = networkOutput;
    outputs.pOutputs = pOutputs;
    
    return outputs;
}


void printOutputs(int K, int M, int **weights_of_A, int **weights_of_B, int networkAoutput, int networkBoutput) {
    
    // Printing the perceptron weights
    for (int i = 0; i < K; i++) {
        
        // Prints weights of network A
        printf("A.%d.weights: ", i);
        printf("[");
        for (int j = 0; j < M; j++) {
            
            printf("%d", weights_of_A[i][j]);
            
            if (j < M-1) {
                printf(", ");
            }
        }
        printf("]\n");
        
        // Prints weights of network A
        printf("B.%d.weights: ", i);
        printf("[");
        for (int j = 0; j < M; j++) {
            
            printf("%d", weights_of_B[i][j]);
            
            if (j < M-1) {
                printf(", ");
            }
        }
        printf("]\n");
    }
    
    // Printng the overall network outputs
    printf("\nOutput A: %d", networkAoutput);
    printf("\nOutput B: %d\n", networkBoutput);
}


void printAttackerOutputs(int attacker, int K, int M, int **weights, int networkOutput) {
    
    printf("\n.....................................\n");
    
    // Printing the perceptron weights
    for (int i = 0; i < K; i++) {
        
        printf("Attacker %d.%d.weights: ", attacker, i);
        printf("[");
        for (int j = 0; j < M; j++) {
            
            printf("%d", weights[i][j]);
            
            if (j < M-1) {
                printf(", ");
            }
        }
        printf("]\n");
    }
    
    // Printng the overall network output
    printf("\nOutput Attacker %d: %d", attacker, networkOutput);
    
}

int **changeWeights(int K, int L, int M, int networkOutput, int *pOutputs, int **weights, int *inputsArray) {
    
    for (int i = 0; i < K; i++) {
        
        if (pOutputs[i] == networkOutput) {
            
            for (int j = 0; j < M; j++) {
                
                int w = (weights[i][j] - (pOutputs[i] * inputsArray[(i*M)+j]));
                
                if (w < (0-L)) {
                    w = (0-L);
                }
                else if (w > L) {
                    w = L;
                }
                
                weights[i][j] = w;
            }
        }
        
    }
    
    return weights;
}
