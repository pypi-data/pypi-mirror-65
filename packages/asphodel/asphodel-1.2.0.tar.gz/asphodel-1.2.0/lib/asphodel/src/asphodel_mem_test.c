/*
* Copyright (c) 2016, Suprock Technologies
*
* Permission to use, copy, modify, and/or distribute this software for any
* purpose with or without fee is hereby granted, provided that the above
* copyright notice and this permission notice appear in all copies.
*
* THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
* WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
* MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
* SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
* WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
* OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
* CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/

#include <stdlib.h>

#include "asphodel.h"

#ifdef ASPHODEL_MEM_TEST

#undef malloc
#undef free

static int malloc_limit = -1;

ASPHODEL_API int asphodel_mem_test_supported(void)
{
	return 1;
}

ASPHODEL_API void asphodel_mem_test_set_limit(int limit)
{
	malloc_limit = limit;
}

ASPHODEL_API int asphodel_mem_test_get_limit(void)
{
	return malloc_limit;
}

ASPHODEL_LOCAL void *asphodel_mem_test_malloc(size_t size)
{
	if (malloc_limit < 0)
	{
		// no limit
		return malloc(size);
	}
	else if (malloc_limit == 0)
	{
		// limit reached
		return NULL;
	}
	else
	{
		// decrease count
		malloc_limit -= 1;
		return malloc(size);
	}
}

ASPHODEL_LOCAL void asphodel_mem_test_free(void *ptr)
{
	free(ptr);
}

#else // ASPHODEL_MEM_TEST

ASPHODEL_API int asphodel_mem_test_supported(void)
{
	return 0;
}

ASPHODEL_API void asphodel_mem_test_set_limit(int limit)
{
	(void)limit; // suppress unused parameter warning

	return;
}

ASPHODEL_API int asphodel_mem_test_get_limit(void)
{
	return -1; // i.e. no limit
}

#endif // ASPHODEL_MEM_TEST
