#ifndef TYPES_H
#define TYPES_H

// Basic type definitions
typedef unsigned int uint32_t;
typedef unsigned char uint8_t;
typedef int int32_t;

#define MAX_BUFFER_SIZE 1024

// Common status codes
typedef enum
{
    STATUS_OK = 0,
    STATUS_ERROR = -1,
    STATUS_BUSY = -2,
    STATUS_TIMEOUT = -3,
    STATUS_INVALID_PARAM = -4,
    STATUS_NO_MEMORY = -5
} Status;

// Priority levels
typedef enum
{
    PRIORITY_LOW = 0,
    PRIORITY_NORMAL = 1,
    PRIORITY_HIGH = 2,
    PRIORITY_CRITICAL = 3
} Priority;

// Boolean type
typedef enum
{
    FALSE = 0,
    TRUE = 1
} Boolean;

#endif // TYPES_H
