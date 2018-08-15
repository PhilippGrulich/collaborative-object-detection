#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <time.h>

#include "streamvbyte.h"
//static inline void rdtsc(unsigned long long *destination) {
//  uint64_t t;
  //  __asm__ volatile(".byte 0x0f, 0x31" : "=A"(t));
//  *destination = 0;
//}

int main() {
  int N = 500000;
  int NTrials = 200;
  uint32_t datain[N];
  uint8_t compressedbuffer[N * 5];
  uint32_t recovdata[N];

  for (int k = 0; k < N; ++k)
    datain[k] = rand() >> (31 & rand());

  size_t compsize = 0;

  compsize = streamvbyte_encode(datain, N, compressedbuffer); // encoding
  //  uint64_t tsc, tsc2;
  //  rdtsc(&tsc);
  struct rusage before;
  getrusage(RUSAGE_SELF, &before);

  size_t compsize2;
  for (int i = 0; i < NTrials; i++)
    compsize2 = streamvbyte_decode(compressedbuffer, recovdata,
                                        N); // decoding (fast)
  struct rusage after;
  getrusage(RUSAGE_SELF, &after);

  float t = (after.ru_utime.tv_usec-before.ru_utime.tv_usec)/1000000.0;
  printf("time = %f  %f uints/sec\n", t, N*NTrials/t); 

  //  rdtsc(&tsc2);
  //tsc2 -= tsc;
  //printf("cycles/quadword %llu\n", (4 * tsc2) / (N * 200));
  // here the result is stored in compressedbuffer using compsize bytes


  printf("compsize=%zu compsize2 = %zu\n", compsize, compsize2);
  //  assert(compsize == compsize2);

  int k;
  for (k = 0; k < N && datain[k] == recovdata[k]; k++) 
    ;
 
  if(k < N)
    printf("mismatch at %d before=%d after=%d\n", k, datain[k], recovdata[k]);

  assert( k >= N );

  //  free(datain);
  //free(compressedbuffer);
  //free(recovdata);
  printf("Compressed %d integers down to %d bytes.\n", N, (int)compsize);
  return 0;
}
