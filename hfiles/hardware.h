#ifndef HARDWARE_H
#define HARDWARE_H

#include "types.h"
#include "device.h" // Circular dependency with device.h
#include "memory.h"

// Hardware abstraction layer
#define GPIO_PIN_COUNT 32

// GPIO pin modes
typedef enum
{
    GPIO_MODE_INPUT = 0,
    GPIO_MODE_OUTPUT = 1,
    GPIO_MODE_ALTERNATE = 2,
    GPIO_MODE_ANALOG = 3
} GPIOMode;

// GPIO pull configuration
typedef enum
{
    GPIO_PULL_NONE = 0,
    GPIO_PULL_UP = 1,
    GPIO_PULL_DOWN = 2
} GPIOPull;

// Interrupt trigger types
typedef enum
{
    IRQ_TRIGGER_NONE = 0,
    IRQ_TRIGGER_RISING = 1,
    IRQ_TRIGGER_FALLING = 2,
    IRQ_TRIGGER_BOTH = 3,
    IRQ_TRIGGER_LEVEL_HIGH = 4,
    IRQ_TRIGGER_LEVEL_LOW = 5
} IRQTrigger;

void hw_init(void);
void hw_gpio_set(uint8_t pin, uint8_t value);
uint8_t hw_gpio_get(uint8_t pin);
void hw_gpio_configure(uint8_t pin, GPIOMode mode, GPIOPull pull);
void hw_register_device(Device *dev);

#endif // HARDWARE_H
