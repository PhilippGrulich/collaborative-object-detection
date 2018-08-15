//
// Created by philipp on 2/14/18.
//

#include <cstdio>
#include <cstdlib>
#include <ios>
#include <iostream>
#include <cstring>
#include <bitset>
#include "stdlib.h"
#include <cmath>

void compress(char **argv) {

    float *buffer, *buffer2, *resultBuffer;
    size_t result;


    int size = atoi(argv[2]);
    printf("sieze %d \n", size);
    float trashholdFloat = atof(argv[3]);
    printf("trash %f \n", trashholdFloat);
    char str[300];
    sprintf(str, "./data/edgePartition");
    FILE *oldFile = fopen(str, "rb");
    sprintf(str, "./data/edgePartition_old");
    FILE *newFile = fopen(str, "rb");


    rewind(oldFile);
    rewind(newFile);

    // allocate memory to contain the whole file:
    buffer = (float *) malloc(sizeof(float) * size);
    buffer2 = (float *) malloc(sizeof(float) * size);
    resultBuffer = (float *) malloc(sizeof(float) * size);

    //fread(buffer, 1, l.outputs*sizeof(*state.input), filePtr);
    // copy the file into the buffer:
    result = fread(buffer, 1, sizeof(float) * size, oldFile);
    printf("result for load oldFile: %d \n", result);


    result = fread(buffer2, 1, sizeof(float) * size, newFile);
    printf("result for load newFile: %d \n", result);


    int zeroedValued = 0;
    for (int i = 0; i < size; i++) {
        //printf("index %d\n", i);
        float oldValue = buffer[i];
        float newValue = buffer2[i];
        if (std::abs(oldValue - newValue) > trashholdFloat) {
            resultBuffer[i] = newValue;
        } else {
            zeroedValued++;
            buffer2[i] = 0;
        }
    }

    printf("zeroed: %d", zeroedValued);
    FILE *filePtr;
    char output[300];
    sprintf(output, "./data/zeroed");
    filePtr = fopen(output, "w");
    rewind(filePtr);
    fwrite(resultBuffer, sizeof(float), size, filePtr);
    fclose(filePtr);

    //sprintf(output, "/home/philipp/usb/projects/yolo2_light_partitioned/diff/%s_%s_%f_%d", imageNew, layer,
    //        trashholdFloat, outputSize);
    //filePtr = fopen(output, "w");
    //rewind(filePtr);
    //fwrite(buffer2, sizeof(float), size, filePtr);
    //fclose(filePtr);
}


void decompress(char **argv) {
    FILE *pFile;
    FILE *pFile2;
    float *compBuffer, *refBuffer;
    size_t result;


    int size = atoi(argv[2]);
    printf("sieze %d \n", size);
//    auto name = argv[7];
    printf("a\n");
    char str[300];
    sprintf(str, "./data/edgePartition_old");
    pFile = fopen(str, "rb");
    sprintf(str, "./data/zeroed");
    printf(str);
    pFile2 = fopen(str, "rb");


    rewind(pFile);
    rewind(pFile2);

    // allocate memory to contain the whole file:
    refBuffer = (float *) malloc(sizeof(float) * size);
    compBuffer = (float *) malloc(sizeof(float) * size);


    //fread(buffer, 1, l.outputs*sizeof(*state.input), filePtr);
    // copy the file into the buffer:
    result = fread(refBuffer, 1, sizeof(float) * size, pFile);

    printf("result for load zero: %d \n", result);
    result = fread(compBuffer, 1, sizeof(float) * size, pFile2);

    printf("result for load oldFile: %d \n", result);
    for (int i = 0; i < size; i++) {
        if (compBuffer[i] == 0) {
            compBuffer[i] = refBuffer[i];
        }
    }

    FILE *filePtr;
    char output[300];
    sprintf(output, "./data/final");
    filePtr = fopen(output, "w");
    rewind(filePtr);
    fwrite(compBuffer, sizeof(float), size, filePtr);
    fclose(filePtr);

}

int main(int argc, char **argv) {

    if (argv[1][0] == 'c') {
        printf("compress\n");
        compress(argv);
    } else {
        printf("decompress\n");
        decompress(argv);
    }
    return 0;
}

