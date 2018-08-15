#ifndef INCLUDE_STREAMVBYTEDELTA_H_
#define INCLUDE_STREAMVBYTEDELTA_H_

#if defined(__cplusplus)
extern "C" {
#endif

#include <inttypes.h>
#include <stdint.h>// please use a C99-compatible compiler
#include <stddef.h>


// Encode an array of a given length read from in to bout in StreamVByte format.
// Returns the number of bytes written.
// The number of values being stored (length) is not encoded in the compressed stream,
// the caller is responsible for keeping a record of this length.
// The pointer "in" should point to "length" values of size uint32_t
// there is no alignment requirement on the out pointer
// this version uses differential coding (coding differences between values) starting at prev (you can often set prev to zero)
// For safety, the out pointer should point to at least streamvbyte_max_compressedbyte(length)
// bytes ( see streamvbyte.h )
size_t streamvbyte_delta_encode(uint32_t *in, uint32_t length, uint8_t *out, uint32_t prev);

// Read "length" 32-bit integers in StreamVByte format from in, storing the result in out.
// Returns the number of bytes read.
// The caller is responsible for knowing how many integers ("length") are to be read: 
// this information ought to be stored somehow.
// There is no alignment requirement on the "in" pointer.
// The out pointer should point to length * sizeof(uint32_t) bytes.
// this version uses differential coding (coding differences between values) starting at prev (you can often set prev to zero)
size_t streamvbyte_delta_decode(const uint8_t *in, uint32_t *out, uint32_t length, uint32_t prev);

#if defined(__cplusplus)
};
#endif

#endif /* INCLUDE_STREAMVBYTEDELTA_H_ */
