 //including Basic required libraries
 // Network.h is responsible for managing weights and smooth execution.


#include <stdio.h>
#include <string.h>
#include <mpi.h>
#include "Network.h"
#include <time.h>
#include <stdlib.h>


    //main method Start here
    int main(void) {
    
    //defining structs
    int comm_size;
    int state;
    MPI_Init(NULL, NULL);
    MPI_Comm_size(MPI_COMM_WORLD, &comm_size);
    MPI_Comm_rank(MPI_COMM_WORLD, &state);
    // Initializing MPI Library and using it's resources
    // Other initializations
    int N, L, K, numberofAttackers, M;
    clock_t begin, end;
    double time_taken;
    
    srand (time(NULL)+state);
    
    if (state == 0) { 
    // Taking user input
        printf("Enter number of inputs for Network: ");
        fflush(stdout);
        scanf("%d", &N);

        printf("Enter number of perceptrons for each Network: ");
        fflush(stdout);
        scanf("%d", &K);

        printf("Enter weights for Networks: ");
        fflush(stdout);
        scanf("%d", &L);

        printf("Enter number Attackers on Network: ");
        fflush(stdout);
        scanf("%d", &numberofAttackers);



        //increase until divisible by no. of perceptrons
        while (N % K != 0) {
            N = N + 1;
        }
        printf("\nCorrected number of inputs by algo: %d\n", N);

        //Calculating perceptrons individually
        M = N/K;
        }
    
        // Broadcasting the user inputs to all other processes
	    MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
	    MPI_Bcast(&K, 1, MPI_INT, 0, MPI_COMM_WORLD);
	    MPI_Bcast(&L, 1, MPI_INT, 0, MPI_COMM_WORLD);
	    MPI_Bcast(&numberofAttackers, 1, MPI_INT, 0, MPI_COMM_WORLD);
	    MPI_Bcast(&M, 1, MPI_INT, 0, MPI_COMM_WORLD);
	    
       //initializing weights of starting network
	    int **weights_of_A;
	    int **weights_of_B;
	    int **weights_of_C;
	       
    if (state == 0) {
        printf("\n............................................\n");
        printf("\nINITIAL STATE OF NETWORK BEFORE ATTACK\n\n");

//initializing  remaining required variables 
        weights_of_A = generatedWeights(N, K, L, M);
        weights_of_B = generatedWeights(N, K, L, M);
        weights_of_C = generatedWeights(N, K, L, M);
       
    }
    
   //initializing  remaining required variables 

    int localSize = 0;
    int remainder = numberofAttackers % comm_size;
    if (remainder == 0) {
        localSize = numberofAttackers/comm_size;
    }
    else {
        localSize = numberofAttackers/comm_size;
        if (state < remainder) {
            localSize++;
        }
        }
    //total steps taken by network
    int ***attackerWeights = malloc(localSize*sizeof(int**));
    for (int i = 0; i < localSize; i++) {
         attackerWeights[i] = generatedWeights(N, K, L, M);
    }

   
   //using resources for InputStore and OutputStore
    int steps = 0;
    int S = 0;
    int* S_attacker = calloc(localSize, sizeof(int));
    int* inputsArray = malloc(N*sizeof(int));
    int networkAoutput = 0;
    int networkBoutput = 0;
    int networkCoutput = 0;
   
  //making pointers  of network
    int* pOutputsA = malloc(K*sizeof(int));
    int* pOutputsB = malloc(K*sizeof(int));
    int* pOutputsC = malloc(K*sizeof(int));
 
     Outputs outputsAttackers[localSize];
    
     int **pOutputsAttackers = malloc(localSize*sizeof(int*));
     for (int i = 0; i < localSize; i++) {
        pOutputsAttackers[i] = malloc(K*sizeof(int));
    }
    
  //Noticing timelapsed for complete execution    
    if (state == 0) {
    
        begin = clock();
    }
    while ((S < 50) && (steps < 1000000)) {
        
        if (state == 0) {
            inputsArray = generatedInputs(N, inputsArray);
            Outputs outputsA = generatedOutputs(K, M, pOutputsA, weights_of_A, inputsArray);
            networkAoutput = outputsA.networkOutput;
            pOutputsA = outputsA.pOutputs;

            Outputs outputsB = generatedOutputs(K, M, pOutputsB, weights_of_B, inputsArray);
            networkBoutput = outputsB.networkOutput;
            pOutputsB = outputsB.pOutputs;

            inputsArray = generatedInputs(N, inputsArray);
            Outputs outputsC = generatedOutputs(K, M, pOutputsC, weights_of_C, inputsArray);
            networkCoutput = outputsC.networkOutput;
            pOutputsC = outputsC.pOutputs;
        }
        // Broadcasting the inputsArray to all other processes
        MPI_Bcast(&(inputsArray[0]), N, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&networkAoutput, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&networkBoutput, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&networkCoutput, 1, MPI_INT, 0, MPI_COMM_WORLD);
        
        // ATTACKER: Output for each attacker network
       for (int i = 0; i < localSize; i++) {
       outputsAttackers[i] = generatedOutputs(K, M, pOutputsAttackers[i], attackerWeights[i], inputsArray);
       }
        
       if (state == 0) {
            // Printing the initial perceptron weights and network outputs
            if (steps == 0) {
                printOutputs(K, M, weights_of_A, weights_of_B, networkAoutput, networkBoutput);
            }
        }
                
        if (state == 0) {
            // Check network outputs and apply learning rule if neccessary
            if (networkAoutput == networkBoutput) {

                // Change A & B weights
            weights_of_A = changeWeights(K, L, M, networkAoutput, pOutputsA, weights_of_A, inputsArray);
            weights_of_C = changeWeights(K, L, M, networkCoutput, pOutputsC, weights_of_C, inputsArray);
            S++;
            }
            else {
                S = 0;
		weights_of_A = changeWeights(K, L, M, networkAoutput, pOutputsA, weights_of_A, inputsArray);
                weights_of_B = changeWeights(K, L, M, networkBoutput, pOutputsB, weights_of_B, inputsArray);    
                
            }
        }
                
        // ATTACKER: Check outputs for each attacker and apply learning rule if equal
        for (int i = 0; i < localSize; i++) {
            
            if (outputsAttackers[i].networkOutput == networkAoutput) {
                
                if (networkAoutput == networkBoutput) {
                attackerWeights[i] = changeWeights(K, L, M, outputsAttackers[i].networkOutput, outputsAttackers[i].pOutputs, attackerWeights[i], inputsArray);
                }
                
                S_attacker[i] = S_attacker[i] + 1;
            }
            else {
                if (networkAoutput == networkBoutput) {
                
                    int w = 0;
                    int wMin = 0;
                    int chosenPerceptron = 0;
                    
                    for (int j = 0; j < K; j++) {
                        
                        for (int k = 0; k < M; k++) {
                            
                            // Getting absolute minimum perceptron weight * input
                            w = abs(attackerWeights[i][j][k] * inputsArray[(j*M)+k]);
                            
                            if ((w < wMin) || ((j == 0) && (k == 0))) {
                                wMin = w;
                                chosenPerceptron = j;
                            }
                            
                        }
                    }
                    
                    // Flipping the sign and assuming output of A
                    outputsAttackers[i].pOutputs[chosenPerceptron] = outputsAttackers[i].pOutputs[chosenPerceptron] * -1;
                    outputsAttackers[i].networkOutput = networkAoutput;
                    
                    // Applying learning rule
                    attackerWeights[i] = changeWeights(K, L, M, outputsAttackers[i].networkOutput, outputsAttackers[i].pOutputs, attackerWeights[i], inputsArray);
                }
                
                S_attacker[i] = 0;
            }
        }
        
        steps++;
        
        MPI_Bcast(&S, 1, MPI_INT, 0, MPI_COMM_WORLD);
    }

    
    if (state == 0) {
        printf("\n.........................................\n");
        printf("\nFINAL STATE OF NETWORK AFTER ATTACK\n\n");

        // Printing the final network state and outputs
        printOutputs(K, M, weights_of_A, weights_of_B, networkAoutput, networkBoutput);

        printf("\n...........................................");

        if (S == 50) {
            printf("\n NETWORKS SYNCED SUCCESSFULLY!\n");
            printf("Synced steps: %d\n", S);
            printf("Total steps taken: %d", steps);

            // Take ending clock time and print time taken
            end = clock();
            time_taken = ((double)(end - begin) / CLOCKS_PER_SEC)*1000;
            printf("\nTime Taken: %.3f ms\n", time_taken);
        }
        else {
            printf("\n*** NETWORKS WAS UNABLE TO SYNC ***\n");
            printf("Total Steps Taken: %d\n", steps);
        }

        printf("...............................................\n");
        
        printf("ATTACKERS SYNCED WITH NETWORK A:\n");
    }
    MPI_Barrier(MPI_COMM_WORLD);
    int offset = 0;
    if (state < remainder) {
        offset = state * localSize;
    }
    else {
        offset = (state * localSize) + remainder;
    }
    
    int localSynced = 0;
    int attackSynced = 0;
    for (int i = 0; i < localSize; i++) {
        
        if (S_attacker[i] >= 50) {
            printf("--- Attacker No. %d (Synced for '%d' steps)\n", i+1+offset, S_attacker[i]);
            localSynced++;
        }
    }
    MPI_Reduce(&localSynced, &attackSynced, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    
    MPI_Barrier(MPI_COMM_WORLD);
    
    if (state == 0) {
        // If no attackers synchronised then print 'None'.
        if (attackSynced == 0) {
            printf("None\n");
        }
    }
    // Releasing resources aquired for attacks
    if (state == 0) {
        free(*weights_of_A);
        free(weights_of_A);
        free(*weights_of_B);
        free(weights_of_B);
       
    }
    // Releasing resources aquired for attacks
    free(inputsArray);
    free(pOutputsA);
    free(pOutputsB);
    free(pOutputsC);
    free(**attackerWeights);
    free(*attackerWeights);
    free(attackerWeights);
    free(S_attacker);
    MPI_Finalize();
    return 0;
}
