/*
	COMPILED_INDEX.CPP
	------------------
	Copyright (c) 2017 Andrew Trotman
	Released under the 2-clause BSD license (See:https://en.wikipedia.org/wiki/BSD_licenses)
*/
#include <algorithm>
#include <exception>

#include <stdint.h>

#include "query.h"
#include "strings.h"
#include "channel_file.h"
#include "parser_query.h"
#include "allocator_pool.h"
#include "accumulator_2d.h"
#include "JASS_vocabulary.h"

/*
	If the line below is enabled then the global operator new and operator delete methods are overwridden
	to check whether any memory is allocated during the processing of a query.  If the line is commented
	out then the checks are disabled and the global operators are not overridden. 
*/
//#define ENSURE_NO_ALLOCATIONS false				// uncomment this line to check for spurious memory allocations

#ifdef ENSURE_NO_ALLOCATIONS
	#include "global_new_delete.h"
#endif

/*
	Table that converts internal document IDs to external primary keys.
*/
extern std::vector<std::string> primary_key;

/*
	MAIN()
	------
*/
int main(int argc, char *argv[])
	{
	try
		{
		/*
			Sort the dictionary - because it was probably generated in the
			order of the hash-table which isn't alphabetical.
		*/
		std::sort(&dictionary[0], &dictionary[dictionary_length]);

		/*
			Use a JASS channel to read the input query
		*/
		JASS::channel_file input;							// read from here
		JASS::channel_file output;							// write to here.

		while (1)
			{
			/*
				If we're checking to make sure that no memory allocation (outside JASS custom allocation) then turn
				off checking for the sole purpose of allocating the arena.
			*/
			#ifdef ENSURE_NO_ALLOCATIONS
				global_new_delete_return();					// disable checking
				JASS::allocator_pool memory;				// allocate memory
				global_new_delete_replace();				// enable checking
			#else
				JASS::allocator_pool memory;				// allocate memory
			#endif
			
			JASS::string query(memory);					// allocate a string to read into
			JASS::query<uint16_t, 10'000'000, 10> jass_query(primary_key, 1024, 10);	// allocate a JASS query object

			/*
				Read a query from a user
			*/
			std::cout << "]";
			input.gets(query);

			/*
				Check to see if we're at the end of the query stream
			*/
			if (query.compare(0, 5, ".quit") == 0)
				break;

			/*
				Echo the query
			*/
			output << query;

			/*
				Parse the query then iterate over the terms
			*/
			jass_query.parse(query);
			for (const auto &term : jass_query.terms())
				{
				/*
					Search the vocabulary for the query term and if we find it all the attached method to process the postings.
				*/
				auto low = std::lower_bound (&dictionary[0], &dictionary[dictionary_length], JASS_ci_vocab(term.token()));
				if ((low != &dictionary[dictionary_length] && !(JASS_ci_vocab(term.token()) < *low)))
					low->method(jass_query);
				}

			/*
				Dump the top-k to the output channel
			*/
			for (const auto &element : jass_query)
				{
				std::cout << element.document_id << ":" <<element.document_id << "::" << element.rsv << "\n";
				//output << element.document_id << ":" << element.rsv << "\n";
				}
			}
		}
	catch (std::exception &error)
		{
		printf("CAUGHT AN EXCEPTION OF TYPE std::exception (%s)\n", error.what());
		}
	catch (...)
		{
		printf("CAUGHT AN EXCEPTION OF UNKNOEN TYPE)\n");
		}

	#ifdef ENSURE_NO_ALLOCATIONS
		global_new_delete_return();					// disable memorty checking (so that the memory object can be deallocated without fuss).
	#endif
	return 0;
	}

