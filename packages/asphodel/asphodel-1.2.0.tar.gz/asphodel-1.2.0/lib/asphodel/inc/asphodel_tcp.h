/*
 * Copyright (c) 2015, Suprock Technologies
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

#ifndef ASPHODEL_TCP_H_
#define ASPHODEL_TCP_H_

#include <stdint.h>
#include <stddef.h>
#include "asphodel_api.h"
#include "asphodel_device.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
	uint8_t tcp_version;
    uint8_t connected;
	size_t max_incoming_param_length;
	size_t max_outgoing_param_length;
    size_t stream_packet_length;
    int protocol_type;
    char* serial_number;
    uint8_t board_rev;
    char* board_type;
    char* build_info;
    char* build_date;
    char* user_tag1;
    char* user_tag2;
	size_t remote_max_incoming_param_length;
	size_t remote_max_outgoing_param_length;
	size_t remote_stream_packet_length;
} Asphodel_TCPAdvInfo_t;

// returns a pointer to the advertisement structure
ASPHODEL_API Asphodel_TCPAdvInfo_t* asphodel_tcp_get_advertisement(AsphodelDevice_t* device);

// returns 1 if the library has been build with TCP device support (-DASPHODEL_TCP_DEVICE), and 0 otherwise.
ASPHODEL_API int asphodel_tcp_devices_supported(void);

// initialize the TCP portion of the library. MUST be called before asphodel_tcp_find_devices()
ASPHODEL_API int asphodel_tcp_init(void);

// close down the TCP portion of the library. asphodel_tcp_init() can be called afterwards, if needed later.
ASPHODEL_API void asphodel_tcp_deinit(void);

// Find any Asphodel devices attached to the local network. The device_list parameter should be an array of
// AsphodelDevice_t pointers, with the array size pointed to by list_size. The array will be filled with pointers
// to AsphodelDevice_t structs, up to the array length. The total number of found TCP devices will be written into
// the address pointed to by list_size. ALL returned devices must be freed (either immediately or at a later point)
// by the calling code by calling the AsphodelDevice_t free_device function pointer.
ASPHODEL_API int asphodel_tcp_find_devices(AsphodelDevice_t **device_list, size_t *list_size);

// Poll all TCP devices at once.
ASPHODEL_API int asphodel_tcp_poll_devices(int milliseconds);

#ifdef __cplusplus
}
#endif

#endif /* ASPHODEL_TCP_H_ */
