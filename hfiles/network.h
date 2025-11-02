#ifndef NETWORK_H
#define NETWORK_H

#include "types.h"
#include "buffer.h"
#include "logger.h"

// Network protocol types
typedef enum
{
    PROTOCOL_TCP = 0,
    PROTOCOL_UDP = 1,
    PROTOCOL_ICMP = 2,
    PROTOCOL_RAW = 3
} NetworkProtocol;

// Connection states
typedef enum
{
    CONN_STATE_CLOSED = 0,
    CONN_STATE_LISTENING = 1,
    CONN_STATE_SYN_SENT = 2,
    CONN_STATE_ESTABLISHED = 3,
    CONN_STATE_CLOSING = 4,
    CONN_STATE_ERROR = 5
} ConnectionState;

// Network interface
typedef struct
{
    uint32_t ip_address;
    uint32_t port;
    NetworkProtocol protocol;
    ConnectionState state;
    Buffer *rx_buffer;
    Buffer *tx_buffer;
} NetworkConnection;

NetworkConnection *net_connect(uint32_t ip, uint32_t port);
void net_send(NetworkConnection *conn, uint8_t *data, uint32_t len);
uint32_t net_receive(NetworkConnection *conn, uint8_t *data, uint32_t max_len);

#endif // NETWORK_H
