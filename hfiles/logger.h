#ifndef LOGGER_H
#define LOGGER_H

#include "types.h"
#include "utils.h"
#include "buffer.h"

// Logging system
typedef enum
{
    LOG_DEBUG,
    LOG_INFO,
    LOG_WARN,
    LOG_ERROR
} LogLevel;

void log_init(void);
void log_message(LogLevel level, const char *msg);
void log_buffer(Buffer *buf);

#endif // LOGGER_H
