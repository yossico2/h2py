#ifndef CONFIG_H
#define CONFIG_H

#include "types.h"
#include "logger.h"

// Configuration management
#define CONFIG_VERSION "1.0.0"
#define MAX_CONFIG_ENTRIES 100

// Configuration value types
typedef enum
{
    CONFIG_TYPE_STRING = 0,
    CONFIG_TYPE_INTEGER = 1,
    CONFIG_TYPE_FLOAT = 2,
    CONFIG_TYPE_BOOLEAN = 3,
    CONFIG_TYPE_ENUM = 4
} ConfigType;

// Configuration scope
typedef enum
{
    CONFIG_SCOPE_SYSTEM = 0,
    CONFIG_SCOPE_USER = 1,
    CONFIG_SCOPE_SESSION = 2,
    CONFIG_SCOPE_TEMPORARY = 3
} ConfigScope;

typedef struct
{
    char key[64];
    char value[256];
    ConfigType type;
    ConfigScope scope;
    Boolean is_read_only;
} ConfigEntry;

void config_load(const char *filename);
const char *config_get(const char *key);
void config_set(const char *key, const char *value);

#endif // CONFIG_H
