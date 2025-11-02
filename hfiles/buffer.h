#ifndef BUFFER_H
#define BUFFER_H

#include "types.h"
#include "memory.h"

// Buffer access modes
typedef enum
{
    BUFFER_MODE_READ_ONLY = 0,
    BUFFER_MODE_WRITE_ONLY = 1,
    BUFFER_MODE_READ_WRITE = 2
} BufferMode;

// Buffer flags
typedef enum
{
    BUFFER_FLAG_NONE = 0x00,
    BUFFER_FLAG_CIRCULAR = 0x01,
    BUFFER_FLAG_LOCKED = 0x02,
    BUFFER_FLAG_DIRTY = 0x04,
    BUFFER_FLAG_OVERFLOW = 0x08
} BufferFlags;

// Buffer management
typedef struct
{
    uint8_t *data;
    uint32_t size;
    uint32_t capacity;
    BufferMode mode;
    uint8_t flags;
    Status status;
} Buffer;

Buffer *buffer_create(uint32_t capacity);
void buffer_destroy(Buffer *buf);
void buffer_append(Buffer *buf, uint8_t *data, uint32_t len);

#endif // BUFFER_H
