/*
	COMPRESS_INTEGER_SIMPLE_16_PACKED.H
	------------------------------------
	Copyright (c) 2014-2017 Blake Burgess and Andrew Trotman
	Released under the 2-clause BSD license (See:https://en.wikipedia.org/wiki/BSD_licenses)
	
	This code is from ATIRE, where it was written by Blake Burgess.
*/
/*!
	@file
	@brief Optimally packed Simple-16 Compression.
	@author Blake Burgess, Andrew Trotman
	@copyright 2016 Andrew Trotman
*/
#pragma once

#include "compress_integer.h"

namespace JASS
	{
	/*
		CLASS COMPRESS_INTEGER_SIMPLE_16_PACKED
		---------------------------------------
	*/
	/*!
		@brief Optimally packed Simple-16 Compression
	*/
	class compress_integer_simple_16_packed : public compress_integer
		{
		protected:
			int64_t *blocks_needed;								///< The optimal number of blocks needed to encode from here to the end of the sequence
			uint8_t *masks;										///< Possible ways to encode this integer in the sequence
			size_t blocks_length;								///< Length of the block_needed and masks dynamic arrays

			static const size_t ints_packed_table[];			///< Number of integers packed into a word, given its mask type
			static const size_t can_pack_table[];				///< Bitmask map for valid masks at an offset (column) for some num_bits_needed (row)
			static const size_t row_for_bits_needed[];			///< Translates the 'bits_needed' to the appropriate 'row' offset for use with can_pack table
			static const size_t invalid_masks_for_offset[];		///< We AND out masks for offsets where we don't know if we can fully pack for that offset
			static const size_t simple16_shift_table[];			///< Number of bits to shift across when packing - is sum of prior packed ints (see above)

		public:
			/*
				COMPRESS_INTEGER_SIMPLE_16_PACKED::COMPRESS_INTEGER_SIMPLE_16_PACKED()
				----------------------------------------------------------------------
			*/
			/*!
				@brief Consructor
			*/
			compress_integer_simple_16_packed() :
				blocks_needed(nullptr),
				masks(nullptr),
				blocks_length(0)
				{
				/* Nothing */
				}
			
			/*
				COMPRESS_INTEGER_SIMPLE_16_PACKED::~COMPRESS_INTEGER_SIMPLE_16_PACKED()
				-----------------------------------------------------------------------
			*/
			/*!
				@brief Destructor
			*/
			virtual ~compress_integer_simple_16_packed()
				{
				delete [] blocks_needed;
				delete [] masks;
				}
			
			/*
				COMPRESS_INTEGER_SIMPLE_16_PACKED::ENCODE()
				-------------------------------------------
			*/
			/*!
				@brief Encode a sequence of integers returning the number of bytes used for the encoding, or 0 if the encoded sequence doesn't fit in the buffer.
				@param encoded [out] The sequence of bytes that is the encoded sequence.
				@param encoded_buffer_length [in] The length (in bytes) of the output buffer, encoded.
				@param source [in] The sequence of integers to encode.
				@param source_integers [in] The length (in integers) of the source buffer.
				@return The number of bytes used to encode the integer sequence, or 0 on error (i.e. overflow).
			*/
			virtual size_t encode(void *encoded, size_t encoded_buffer_length, const integer *source, size_t source_integers);

			/*
				COMPRESS_INTEGER_SIMPLE_16_PACKED::DECODE()
				-------------------------------------------
			*/
			/*!
				@brief Decode a sequence of integers encoded with this codex.
				@param decoded [out] The sequence of decoded integers.
				@param integers_to_decode [in] The minimum number of integers to decode (it may decode more).
				@param source [in] The encoded integers.
				@param source_length [in] The length (in bytes) of the source buffer.
			*/
			virtual void decode(integer *decoded, size_t integers_to_decode, const void *source, size_t source_length);

			/*
				COMPRESS_INTEGER_SIMPLE_16_PACKED::UNITTEST()
				---------------------------------------------
			*/
			/*!
				@brief Unit test this class
			*/
			static void unittest(void);
		};
	}
