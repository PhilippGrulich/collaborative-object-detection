#include "util.h"

#if defined(_MSC_VER)
     /* Microsoft C/C++-compatible compiler */
     #include <intrin.h>
#elif defined(__GNUC__) && (defined(__x86_64__) || defined(__i386__))
     /* GCC-compatible compiler, targeting x86/x86-64 */
     #include <x86intrin.h>
#elif defined(__GNUC__) && defined(__ARM_NEON__)
     /* GCC-compatible compiler, targeting ARM with NEON */
     #include <arm_neon.h>
#elif defined(__GNUC__) && defined(__IWMMXT__)
     /* GCC-compatible compiler, targeting ARM with WMMX */
     #include <mmintrin.h>
#elif (defined(__GNUC__) || defined(__xlC__)) && (defined(__VEC__) || defined(__ALTIVEC__))
     /* XLC or GCC-compatible compiler, targeting PowerPC with VMX/VSX */
     #include <altivec.h>
#elif defined(__GNUC__) && defined(__SPE__)
     /* GCC-compatible compiler, targeting PowerPC with SPE */
     #include <spe.h>
#endif

uint32_t bits(const uint32_t v) {
#ifdef _MSC_VER
    unsigned long answer;
    if (v == 0) {
        return 0;
    }
    _BitScanReverse(&answer, v);
    return answer + 1;
#else
    return v == 0 ? 0 : 32 - __builtin_clz(v); /* assume GCC-like compiler if not microsoft */
#endif
}

static uint32_t orasint(const __m128i accumulator) {
    const __m128i _tmp1 = _mm_or_si128(_mm_srli_si128(accumulator, 8), accumulator); /* (A,B,C,D) xor (0,0,A,B) = (A,B,C xor A,D xor B)*/
    const __m128i _tmp2 = _mm_or_si128(_mm_srli_si128(_tmp1, 4), _tmp1); /*  (A,B,C xor A,D xor B) xor  (0,0,0,C xor A)*/
    return  _mm_cvtsi128_si32(_tmp2);
}

uint32_t maxbits_length(const uint32_t * in,uint32_t length) {
    uint32_t k;
    uint32_t lengthdividedby4 = length / 4;
    uint32_t offset = lengthdividedby4 * 4;
    uint32_t bigxor = 0;
    if(lengthdividedby4 > 0) {
        const __m128i* pin = (const __m128i*)(in);
        __m128i accumulator = _mm_loadu_si128(pin);
        k = 1;
        for(; 4*k < 4*lengthdividedby4; ++k) {
            __m128i newvec = _mm_loadu_si128(pin+k);
            accumulator = _mm_or_si128(accumulator,newvec);
        }
        bigxor = orasint(accumulator);
    }
    for(k = offset; k < length; ++k)
        bigxor |= in[k];
    return bits(bigxor);
}
