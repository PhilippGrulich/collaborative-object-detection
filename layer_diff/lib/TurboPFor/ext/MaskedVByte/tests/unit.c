#include <stdio.h>
#include <stdlib.h>

#include "varintencode.h"
#include "varintdecode.h"

int main() {
	int N = 4096;
	uint32_t * datain = malloc(N * sizeof(uint32_t));
	uint8_t * compressedbuffer = malloc(2 * N * sizeof(uint32_t));
	uint32_t * recovdata = malloc(N * sizeof(uint32_t));

	for (int length = 0; length <= N; ) {
		printf("length = %d \n",length);
		printf("Regular VByte \n");
		for (uint32_t gap = 1; gap <= 387420489; gap *= 3) {
			for (int k = 0; k < length; ++k)
				datain[k] = gap;
			size_t compsize = vbyte_encode(datain, length, compressedbuffer);
			size_t usedbytes = masked_vbyte_decode(compressedbuffer, recovdata,
					length);
			if (compsize != usedbytes) {
				printf("[masked_vbyte_decode] code is buggy gap = %d, size mismatch %d %d \n",(int) gap, (int) compsize, (int) usedbytes);
				return -1;
			}
			for (int k = 0; k < length; ++k) {
				if (recovdata[k] != datain[k]) {
					printf("[masked_vbyte_decode] code is buggy gap = %d\n", (int) gap);
					return -1;
				}
			}
			size_t decodedints = masked_vbyte_decode_fromcompressedsize(compressedbuffer, recovdata,
					compsize);
			if (decodedints != (size_t) length) {
				printf("[masked_vbyte_decode_fromcompressedsize] code is buggy gap = %d, size mismatch %d %d \n",(int) gap, (int) compsize, (int) usedbytes);
				return -1;
			}
			for (int k = 0; k < length; ++k) {
				if (recovdata[k] != datain[k]) {
					printf("[masked_vbyte_decode_fromcompressedsize] code is buggy gap = %d\n",(int) gap);
					return -1;
				}
			}

		}
		printf("Delta VByte \n");
		for (size_t gap = 1; gap <= 531441; gap *= 3) {
			for (int k = 0; k < length; ++k)
				datain[k] = gap * k;
			size_t compsize = vbyte_encode_delta(datain, length, compressedbuffer,0);
			size_t usedbytes = masked_vbyte_decode_delta(compressedbuffer, recovdata,
					length,0);
			if (compsize != usedbytes) {
				printf("[masked_vbyte_decode_delta] code is buggy gap = %d, size mismatch %d %d \n",(int) gap, (int) compsize, (int) usedbytes);
				return -1;
			}
			for (int k = 0; k < length; ++k) {
				if (recovdata[k] != datain[k]) {
					printf("[masked_vbyte_decode_delta] code is buggy gap = %d\n", (int) gap);
					return -1;
				}
			}
			size_t decodedints = masked_vbyte_decode_fromcompressedsize_delta(compressedbuffer, recovdata,
					compsize,0);
			if (decodedints != (size_t) length) {
				printf("[masked_vbyte_decode_fromcompressedsize_delta] code is buggy gap = %d, size mismatch %d %d \n",(int) gap, (int) compsize, (int) usedbytes);
				return -1;
			}
			for (int k = 0; k < length; ++k) {
				if (recovdata[k] != datain[k]) {
					printf("[masked_vbyte_decode_fromcompressedsize_delta] code is buggy gap = %d\n",(int) gap);
					return -1;
				}
			}

		}


		if(length < 128)
			++length;
		else {
			length *= 2;
		}
	}
	free(datain);
	free(compressedbuffer);
	free(recovdata);
	printf("Code looks good.\n");
	return 0;
}

