#ifndef DEVICE_H
#define DEVICE_H

#include "types.h"
#include "utils.h"
#include "memory.h"
#include "config.h"
// #include "hardware.h" // This will create a circular dependency!

// Device types
typedef enum
{
    DEVICE_TYPE_UNKNOWN = 0,
    DEVICE_TYPE_SENSOR = 1,
    DEVICE_TYPE_ACTUATOR = 2,
    DEVICE_TYPE_CONTROLLER = 3,
    DEVICE_TYPE_DISPLAY = 4,
    DEVICE_TYPE_STORAGE = 5,
    DEVICE_TYPE_COMMUNICATION = 6
} DeviceType;

// Device states
typedef enum
{
    DEVICE_STATE_UNINITIALIZED = 0,
    DEVICE_STATE_INITIALIZING = 1,
    DEVICE_STATE_READY = 2,
    DEVICE_STATE_ACTIVE = 3,
    DEVICE_STATE_SUSPENDED = 4,
    DEVICE_STATE_ERROR = 5,
    DEVICE_STATE_SHUTDOWN = 6
} DeviceState;

// Power modes
typedef enum
{
    POWER_MODE_OFF = 0,
    POWER_MODE_SLEEP = 1,
    POWER_MODE_LOW_POWER = 2,
    POWER_MODE_NORMAL = 3,
    POWER_MODE_HIGH_PERFORMANCE = 4
} PowerMode;

// Device management
typedef struct
{
    uint32_t device_id;
    char name[32];
    DeviceType type;
    DeviceState state;
    PowerMode power_mode;
    Priority priority;
    void *driver_data;
} Device;

Device *device_init(uint32_t id);
void device_configure(Device *dev);
void device_shutdown(Device *dev);

#endif // DEVICE_H
