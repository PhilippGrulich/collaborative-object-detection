/*
	SERIALISE_INTEGERS.CPP
	----------------------
	Copyright (c) 2017 Andrew Trotman
	Released under the 2-clause BSD license (See:https://en.wikipedia.org/wiki/BSD_licenses)
*/
#include <ostream>

#include "reverse.h"
#include "checksum.h"
#include "serialise_integers.h"
#include "index_manager_sequential.h"

namespace JASS
	{
	/*
		SERIALISE_INTEGERS::OPERATOR()()
		--------------------------------
	*/
	void serialise_integers::operator()(const slice &term, const index_postings &postings_list)
		{
		/*
			Impact order the postings list.
		*/
		memory.rewind();
		const auto &impact_ordered = postings_list.impact_order(memory);

		for (const auto &header : reverse(impact_ordered))
			{
			uint32_t length = header.size();
			postings_file.write(&length, sizeof(length));
			for (const auto &posting : header)
				{
				/*
					uncompressed is an array of uint32_t integers counting from 0 (but the indexer counts from 1 so we subtract 1).
				*/
				uint32_t document_id = static_cast<uint32_t>(posting - 1);
				postings_file.write(&document_id, sizeof(document_id));
				}
			}
		}

	/*
		SERIALISE_INTEGERS::UNITTEST_ONE_COLLECTION()
		---------------------------------------------
	*/
	void serialise_integers::unittest_one_collection(const std::string &document_collection, uint32_t expected_checksum)
		{
		/*
			Build an index of the standard 10 documents
		*/
		index_manager_sequential index;
		index_manager_sequential::unittest_build_index(index, document_collection);

		/*
			Serialise the index.
		*/
		{
		serialise_integers serialiser;
		index.iterate(serialiser);
		}

		/*
			Checksum the index to make sure its correct.
		*/
		auto checksum = checksum::fletcher_16_file("postings.bin");
//		std::cout << "postings.bin:" << checksum << '\n';
		JASS_assert(checksum == expected_checksum);
		}

	/*
		SERIALISE_INTEGERS::UNITTEST()
		------------------------------
	*/
	void serialise_integers::unittest(void)
		{
		unittest_one_collection(unittest_data::ten_documents, 42937);
		unittest_one_collection(unittest_data::three_documents_asymetric, 7698);

		puts("serialise_integers::PASSED");
		}
	}
