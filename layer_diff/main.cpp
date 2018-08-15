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
#include "lib/FastPFor/headers/codecfactory.h"
#include "lib/FastPFor/headers/deltautil.h"
#include <cmath>
void printB(unsigned u) {
    for (int i = 0; i < 32; i++) {
        if (u & (1 << i)) {
            std::cout << 1;
        } else {
            std::cout << 0;
        }
    }
    std::cout << std::endl;
}

unsigned int toBinary(float num) {
    unsigned u;
    std::memcpy(&u, &num, sizeof num);
    //printB(u);
    return u;
}

unsigned int xorFloat(float num, float num2) {
    unsigned int u1;
    std::memcpy(&u1, &num, sizeof num);
    unsigned int u2;
    std::memcpy(&u2, &num2, sizeof num2);
    //std::cout << std::hex << u1 << "\n";
    //std::cout << std::hex << u2 << "\n";
    unsigned int temp = (u1 & u2) | (~(u1 | u2));
    //printB(temp);
    temp = ~temp;
    //  printB(temp);
    // std::cout << std::endl << std::endl;
    return temp;
}

unsigned int diff(unsigned int u1, unsigned int u2) {

    //std::cout << std::hex << u1 << "\n";
    //std::cout << std::hex << u2 << "\n";
    unsigned int temp = (u1 & u2) | (~(u1 | u2));
    //printB(temp);
    temp = ~temp;
    //  printB(temp);
    // std::cout << std::endl << std::endl;
    return temp;
}

unsigned int getExponentBits(unsigned int floatBits) {
    unsigned int exponentMask = ((1 << 8) - 1) << 23;
    return (floatBits & exponentMask) << 1;
}

unsigned int getMantisseBits(unsigned int floatBits) {
    unsigned int exponentMask = ((1 << 23) - 1);
    return (floatBits & exponentMask);
}


unsigned int getSignBits(unsigned int floatBits) {
    unsigned int exponentMask = 1 << 31;
    return (floatBits & exponentMask);
}


vector<uint32_t> compressPFor(std::vector<uint32_t> mydata) {
    using namespace FastPForLib;


    // We pick a CODEC
    IntegerCODEC &codec = *CODECFactory::getFromName("simdfastpfor256");
    // could use others, e.g., "simdbinarypacking", "varintg8iu"

    //
    // the vector mydata could contain anything, really
    //
    ///////////
    //
    // You need some "output" container. You are responsible
    // for allocating enough memory.
    //

    std::vector<uint32_t> compressed_output(100000000);
    // N+1024 should be plenty
    //
    //
    size_t compressedsize = compressed_output.size();
    codec.encodeArray(mydata.data(), mydata.size(), compressed_output.data(),
                      compressedsize);
    //
    // if desired, shrink back the array:
    compressed_output.resize(compressedsize);
    compressed_output.shrink_to_fit();
    // display compression rate:
    std::cout << std::setprecision(3);
    std::cout << "You are using "
              << 32.0 * static_cast<double>(compressed_output.size()) /
                 static_cast<double>(mydata.size())
              << " bits per integer. " << compressed_output.size() << std::endl;

    // If you do use differential coding a lot, you might want
    // to check out these other libraries...
    // https://github.com/lemire/FastDifferentialCoding
    // and
    // https://github.com/lemire/SIMDCompressionAndIntersection
    return compressed_output;
}

std::vector<uint32_t> compressExponentBits(std::vector<uint32_t> mantisseBits) {
    std::vector<uint32_t> resultVector(0);
    uint32_t currentValue = mantisseBits[0];
    for (int i = 1; i < mantisseBits.size(); i++) {
        int index = i % 4;
        if (index != 0) {
            currentValue = currentValue | (mantisseBits[i] >> (index * 8));


        } else if (i != 0) {
            resultVector.push_back(currentValue);
            //    printB(currentValue);
            currentValue = mantisseBits[i];
        }
    }
    resultVector.push_back(currentValue);
    return compressPFor(resultVector);
}


unsigned int encode(unsigned int bits) {

    unsigned int bits7 = (1 << 7) - 1;
    unsigned int bits6 = (1 << 6) - 1;
    unsigned int bits5 = (1 << 5) - 1;
    unsigned int bits4 = (1 << 4) - 1;
    unsigned int bits3 = (1 << 3) - 1;
    unsigned int bits2 = (1 << 2) - 1;
    unsigned int bits1 = 1;

    if ((bits & bits7) == bits7) {
        return 7;
    } else if ((bits & bits6) == bits6) {
        return 6;
    } else if ((bits & bits5) == bits5) {
        return 5;
    } else if ((bits & bits4) == bits4) {
        return 4;
    } else if ((bits & bits3) == bits3) {
        return 3;
    } else if ((bits & bits2) == bits2) {
        return 2;
    } else if ((bits & bits1) == bits1) {
        return 1;
    }
}


void runlengthEncoding(std::vector<uint32_t> bits) {

    int run = 0;
    int state = 0;
    std::bitset<32> currentBitset(bits[0]);
    for (std::size_t i = 0; i < currentBitset.size(); ++i) {
        //std::cout << "b1[" << i << "]: " << currentBitset[i] << '\n';
        if (currentBitset.test(i) == state && run < 7) {
            // increment run
            run++;
        } else if (currentBitset.test(i) == state && run == 7) {
            // add run to counter && new run with same state

        } else {
            //change state
            state = !state;

        }
    }
}

vector<uint32_t> compressSignBits(std::vector<uint32_t> signBits) {
    std::vector<uint32_t> resultVector(0);
    uint32_t currentValue = 0;
    for (int i = 0; i < signBits.size(); i++) {
        int index = i % 30;
        if (index != 0) {
            currentValue = currentValue | (signBits[i] >> index);


        } else if (i != 0) {
            resultVector.push_back(currentValue);

            // printB(currentValue);
            currentValue = signBits[i];
        }
    }
    resultVector.push_back(currentValue);
    return compressPFor(resultVector);
}


void compress(char **argv) {
    FILE *pFile;
    FILE *pFile2;
    float *buffer, *buffer2, *resultBuffer;
    size_t result;


    int size = atoi(argv[2]);
    float trashholdFloat = atof(argv[3]);


    auto imageOriginal = argv[4];
    auto imageNew = argv[5];
    auto layer = argv[6];
    char str[300];
    sprintf(str, "/home/philipp/usb/projects/yolo2_light_partitioned/data/%s/%s", imageOriginal, layer);
    pFile = fopen(str, "rb");
    sprintf(str, "/home/philipp/usb/projects/yolo2_light_partitioned/data/%s/%s", imageNew, layer);
    pFile2 = fopen(str, "rb");


    rewind(pFile);
    rewind(pFile2);

    // allocate memory to contain the whole file:
    buffer = (float *) malloc(sizeof(float) * size);
    buffer2 = (float *) malloc(sizeof(float) * size);
    resultBuffer = (float *) malloc(sizeof(float) * size);

    //fread(buffer, 1, l.outputs*sizeof(*state.input), filePtr);
    // copy the file into the buffer:
    result = fread(buffer, 1, sizeof(float) * size, pFile);


    result = fread(buffer2, 1, sizeof(float) * size, pFile2);


    int outputSize = 0;
    for (int i = 0; i < size; i++) {
        float oldValue = buffer[i];
        float newValue = buffer2[i];
        if (std::abs(oldValue - newValue) > trashholdFloat) {
            resultBuffer[i] = newValue;
            outputSize++;
        }else{
            buffer2[i] = oldValue;
        }
    }

    FILE *filePtr;
    char output[300];
    sprintf(output, "/home/philipp/usb/projects/yolo2_light_partitioned/diff_trash/%s_%s_%f_%d", imageNew, layer,
            trashholdFloat, outputSize);
    filePtr = fopen(output, "w");
    rewind(filePtr);
    fwrite(resultBuffer, sizeof(float), size, filePtr);
    fclose(filePtr);

    sprintf(output, "/home/philipp/usb/projects/yolo2_light_partitioned/diff/%s_%s_%f_%d", imageNew, layer,
            trashholdFloat, outputSize);
    filePtr = fopen(output, "w");
    rewind(filePtr);
    fwrite(buffer2, sizeof(float), size, filePtr);
    fclose(filePtr);
}


void decompress(char **argv) {
    FILE *pFile;
    FILE *pFile2;
    float *compBuffer, *refBuffer;
    size_t result;


    int size = atoi(argv[2]);
    float trashholdFloat = atof(argv[3]);


    auto imageOriginal = argv[4];
    auto imageNew = argv[5];
    auto layer = argv[6];
    auto name = argv[7];

    char str[300];
    sprintf(str, "/home/philipp/usb/projects/yolo2_light_partitioned/data/%s/%s", imageOriginal, layer);
    pFile = fopen(str, "rb");
    sprintf(str, "/home/philipp/usb/projects/yolo2_light_partitioned/diff_comp/%s", name);
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


    result = fread(compBuffer, 1, sizeof(float) * size, pFile2);


    for (int i = 0; i < size; i++) {
        if (compBuffer[i] == 0) {
            compBuffer[i] = refBuffer[i];
        }
    }

    FILE *filePtr;
    char output[300];
    sprintf(output, "/home/philipp/usb/projects/yolo2_light_partitioned/diff_result/%s_result", name);
    filePtr = fopen(output, "w");
    rewind(filePtr);
    fwrite(compBuffer, sizeof(float), size, filePtr);
    fclose(filePtr);

}

int main(int argc, char **argv) {

    if (argv[1][0] == 'c') {
        compress(argv);
    } else {
        printf("decompress\n");
        decompress(argv);
    }



    /* the whole file is now loaded in the memory buffer. */
/*
    float trashhold = 1e-1;
    int sameExponent = 0;
    int sameSign = 0;
    int sameMantisse = 0;
    std::vector<unsigned int> diffSignBits(0);
    std::vector<unsigned int> diffExponentBits(0);
    std::vector<unsigned int> diffMattissBits(0);
    for (int i = 0; i < size; i++) {

        auto binOriginal = toBinary(buffer[i]);
        auto binNew = toBinary(buffer2[i]);

        auto exponentOriginal = getExponentBits(binOriginal);
        auto signOriginal = getSignBits(binOriginal);
        auto mantisseOriginal = getMantisseBits(binOriginal);

        auto exponentNew = getExponentBits(binNew);
        auto signNew = getSignBits(binNew);
        auto mantissenew = getMantisseBits(binNew);
        auto diffMantisse = diff(mantisseOriginal, mantissenew);
        auto diffExponent = diff(exponentOriginal, exponentNew);
        auto diffSign = diff(signOriginal, signNew);
        diffSignBits.push_back(diffSign);
        diffExponentBits.push_back(diffExponent);
        diffMattissBits.push_back(diffMantisse);
        //printB(diffExponent);
        if (exponentOriginal == exponentNew) {
            sameExponent++;
        } else {

            //printB(exponentOriginal);
            //printB(exponentNew);

        }
        if (signOriginal == signNew) {
            sameSign++;
        }

        if (mantisseOriginal == mantissenew) {
            sameMantisse++;
        }

       // /*
        if (buffer[i] - trashhold < buffer2[i] && buffer[i] + trashhold > buffer2[i]) {
            printf("%.5f - %.5f \n", buffer[i], buffer2[i]);
            toBinary(buffer[i]);
            toBinary(buffer2[i]);
            xorFloat(buffer[i], buffer2[i]);

            count++;
        }
        // */
    /*  }

     printf("%.d - %d - %d\n", sameSign, sameExponent, sameMantisse);
     printf("%d\n", diffSignBits.size());

     const vector<uint32_t> &signBits = compressSignBits(diffSignBits);

     //compressPFor(diffExponentBits);
     const vector<uint32_t> &exponentBits = compressExponentBits(diffExponentBits);
     const vector<uint32_t> &mattissBits = compressPFor(diffMattissBits);

     int resSize = 3 + signBits.size() + exponentBits.size() + mattissBits.size();
     vector<uint32_t> resultBuffer(0);


     resultBuffer.push_back(signBits.size());
     resultBuffer.push_back(exponentBits.size());
     resultBuffer.push_back(mattissBits.size());

     std::copy(signBits.begin(), signBits.end(), std::back_inserter(resultBuffer));
     std::copy(exponentBits.begin(), exponentBits.end(), std::back_inserter(resultBuffer));
     std::copy(mattissBits.begin(), mattissBits.end(), std::back_inserter(resultBuffer));


     FILE *filePtr;
     char output[200];
     sprintf(output, "/home/philipp/usb/projects/yolo2_light_partitioned/compMe/%s/%s", image, layer);
     filePtr = fopen(str, "w");
     fwrite(&buffer[0], sizeof(uint32_t), resSize, filePtr);
     fclose(filePtr);



     // terminate
     fclose(pFile);
     free(buffer);
      */
    return 0;
}

