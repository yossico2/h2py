#ifndef MEMORY_H
#define MEMORY_H

#include "types.h"
#include <stdlib.h>

// Memory management
void *mem_alloc(uint32_t size);
void mem_free(void *ptr);
uint32_t mem_available(void);

#endif // MEMORY_H
