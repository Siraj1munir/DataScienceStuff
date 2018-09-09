//including standard header files

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct Outputs {
    int *pOutputs;
    int networkOutput;
} Outputs;

//Some declarations 
int **generatedWeights(int N, int K, int L, int M);
int *generatedInputs(int N, int *inputsArray);
struct Outputs generatedOutputs(int K, int M, int *pOutputs, int **weights, int *inputsArray);
void printOutputs(int K, int M, int **weights_of_A, int **weights_of_B, int networkAoutput, int networkBoutput);
void printAttackerOutputs(int attacker, int K, int M, int **weights, int networkOutput);
int **changeWeights(int K, int L, int M, int networkOutput, int *pOutputs, int **weights, int *inputsArray);
