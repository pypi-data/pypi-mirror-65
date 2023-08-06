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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>
#include <time.h>

#if defined(_MSC_VER) && _MSC_VER < 1900 // NOTE: 1900 is VS2015
	#include "inttypes.h"
#else
	#include <inttypes.h>
#endif

#include "snprintf.h" // for msvc++ compatability

#include "asphodel.h"

#ifdef _WIN32
	#include <conio.h>
#else
	#include <termios.h>
	#include <unistd.h>
	#include <fcntl.h>

	int _kbhit(void)
	{
		struct termios oldt, newt;
		int ch;
		int oldf;

		tcgetattr(STDIN_FILENO, &oldt);
		newt = oldt;
		newt.c_lflag &= ~(ICANON | ECHO);
		tcsetattr(STDIN_FILENO, TCSANOW, &newt);
		oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
		fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

		ch = getchar();

		tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
		fcntl(STDIN_FILENO, F_SETFL, oldf);

		if(ch != EOF)
		{
			ungetc(ch, stdin);
			return 1;
		}

		return 0;
	}

#endif


typedef struct {
	AsphodelDeviceDecoder_t *decoder;
	int stream_count;
	AsphodelStreamAndChannels_t *info_array;
	FILE *packet_file;
	char serial_number[100];
} DeviceInfo_t;

typedef struct {
	FILE *csv_file;
	AsphodelUnitFormatter_t *unit_formatter;
	double counter_time_scale;
	double sample_time_scale;
} ChannelClosure_t;

int file_exists(const char *filename) // NOTE: this function is not UTF-8 compliant (on windows, at least)
{
	FILE *file;
	if ((file = fopen(filename, "r")))
	{
		fclose(file);
		return 1;
	}
	return 0;
}

FILE * create_unique_file(const char *serial_number, const char *channel_name) // NOTE: this function is not UTF-8 compliant (on windows, at least)
{
	int i;
	char filename[FILENAME_MAX];
	char datename[32];
	struct tm *now;
	time_t t = time(NULL);
	now = localtime(&t);
	if (strftime(datename, 32, "%Y%m%d.%H%M", now) == 0)
	{
		printf("Error with strftime()\n");
		return NULL;
	}

	i = 1;
	snprintf(filename, sizeof(filename), "%s-%s-%s.csv", serial_number, datename, channel_name);

	// check if filename exists
	while (file_exists(filename))
	{
		i++;
		if (i > 10)
		{
			return NULL;
		}
		snprintf(filename, sizeof(filename), "%s-%s-%s(%d).csv", serial_number, datename, channel_name, i);
	}

	return fopen(filename, "w");
}

static int create_channel_closure(const char *serial_number, AsphodelStreamInfo_t *stream_info, AsphodelChannelInfo_t *channel_info,
		AsphodelChannelDecoder_t *channel_decoder, ChannelClosure_t **closure)
{
	ChannelClosure_t *c;

	c = (ChannelClosure_t*)malloc(sizeof(ChannelClosure_t));
	if (c == NULL)
	{
		return ASPHODEL_NO_MEM;
	}

	if (stream_info->rate != 0.0 && channel_decoder->samples != 0)
	{
		c->counter_time_scale = 1 / (stream_info->rate);
		c->sample_time_scale = c->counter_time_scale / (double)channel_decoder->samples;
	}
	else
	{
		// setting to zero will force only indexes to be written to the file
		c->counter_time_scale = 0.0;
		c->sample_time_scale = 0.0;
	}

	c->unit_formatter = asphodel_create_unit_formatter(channel_info->unit_type, channel_info->minimum, channel_info->maximum, channel_info->resolution, 1);
	if (c->unit_formatter == NULL)
	{
		printf("Error in asphodel_create_unit_formatter()\n");
		free(c);
		return 1;
	}

	c->csv_file = create_unique_file(serial_number, (char*)channel_info->name);
	if (c->csv_file == NULL)
	{
		printf("Error in create_unique_file(%s, %s)\n", serial_number, channel_info->name);
		c->unit_formatter->free(c->unit_formatter);
		free(c);
		return 1;
	}

	*closure = c;
	return 0;
}

static void free_channel_closure(ChannelClosure_t *c)
{
	fclose(c->csv_file);

	c->unit_formatter->free(c->unit_formatter);

	free(c);
}

static void channel_decode_callback(uint64_t counter, double *data, size_t samples, size_t subchannels, void * closure)
{
	size_t i;

	ChannelClosure_t *c = (ChannelClosure_t*)closure;

	for (i = 0; i < samples; i++)
	{
		// each sample is a line
		size_t j;
		if (c->counter_time_scale == 0.0)
		{
			fprintf(c->csv_file, "%" PRIu64, counter);
		}
		else
		{
			double time = (double)counter * c->counter_time_scale + (double)i * c->sample_time_scale;
			fprintf(c->csv_file, "%" PRIu64 ", %f", counter, time);
		}

		for (j = 0; j < subchannels; j++)
		{
			char buffer[256];
			c->unit_formatter->format_bare(c->unit_formatter, buffer, sizeof(buffer), data[i * subchannels + j]);
			fprintf(c->csv_file, ", %s", buffer);
		}
		fprintf(c->csv_file, "\n");
	}
}

static void write_csv_header(AsphodelChannelDecoder_t *decoder, ChannelClosure_t *c)
{
	size_t i;
	char unit_str[256];

	if (c->counter_time_scale == 0.0)
	{
		fprintf(c->csv_file, "Index");
	}
	else
	{
		fprintf(c->csv_file, "Index, Time (s)");
	}

	// create a unit string
	if (c->unit_formatter->unit_utf8 == NULL || *c->unit_formatter->unit_utf8 == '\0')
	{
		// no unit
		unit_str[0] = '\0';
	}
	else
	{
		snprintf(unit_str, sizeof(unit_str), " (%s)", c->unit_formatter->unit_utf8);
	}

	for (i = 0; i < decoder->subchannels; i++)
	{
		if (decoder->subchannel_names[i][0] != '\0')
		{
			fprintf(c->csv_file, ", %s%s", decoder->subchannel_names[i], unit_str);
		}
		else
		{
			if (decoder->subchannels == 1)
			{
				fprintf(c->csv_file, ", Channel%s", unit_str);
			}
			else
			{
				fprintf(c->csv_file, ", Subchannel %d%s", (int)i, unit_str);
			}
		}
	}

	fprintf(c->csv_file, "\n");
}

static void lost_packet_callback(uint64_t current, uint64_t last, void * closure)
{
	char *info_str = (char*)closure;
	uint64_t lost = (current - last) - 1;

	fprintf(stderr, "Lost %" PRIu64 " packets on %s\n", lost, info_str);
}

static void unknown_id_callback(uint8_t id, void * closure)
{
	DeviceInfo_t *device_info = (DeviceInfo_t*)closure;
	fprintf(stderr, "Unknown stream id %d on %s\n", id, device_info->serial_number);
}

static int create_device_info(AsphodelDevice_t *device, DeviceInfo_t **device_info)
{
	int ret;
	int count;
	int i;
	uint8_t filler_bits;
	uint8_t id_bits;
	AsphodelDeviceDecoder_t *decoder;
	AsphodelStreamAndChannels_t *info_array;
	DeviceInfo_t *allocated_device_info;

	allocated_device_info = (DeviceInfo_t*)malloc(sizeof(DeviceInfo_t));
	if (allocated_device_info == NULL)
	{
		printf("Out of memory!\n");
		return 1;
	}

	ret = device->get_serial_number(device, allocated_device_info->serial_number, sizeof(allocated_device_info->serial_number));
	if (ret != 0)
	{
		printf("Error %d in device->get_serial_number()\n", ret);
		free(allocated_device_info);
		return ret;
	}

	ret = asphodel_get_stream_count_blocking(device, &count, &filler_bits, &id_bits);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_stream_count_blocking()\n", ret);
		free(allocated_device_info);
		return ret;
	}

	if (count == 0)
	{
		// no streams
		allocated_device_info->decoder = NULL;
		allocated_device_info->info_array = NULL;
		allocated_device_info->stream_count = 0;
		*device_info = allocated_device_info;
		return 0;
	}

	info_array = (AsphodelStreamAndChannels_t*)malloc(sizeof(AsphodelStreamAndChannels_t) * count);
	if (info_array == NULL)
	{
		printf("Out of memory!\n");
		free(allocated_device_info);
		return 1;
	}

	for (i = 0; i < count; i++)
	{
		int j;

		info_array[i].stream_id = i;

		ret = asphodel_get_stream_blocking(device, i, &info_array[i].stream_info);
		if (ret != 0)
		{
			int m;

			printf("Error %d in asphodel_get_stream_blocking(%d)\n", ret, i);

			// free the partially filled info array
			for (m = 0; m < i; m++)
			{
				int n;
				for (n = 0; n < info_array[m].stream_info->channel_count; n++)
				{
					asphodel_free_channel(info_array[m].channel_info[n]);
				}
				free(info_array[m].channel_info);
				asphodel_free_stream(info_array[m].stream_info);
			}
			free(info_array);

			free(allocated_device_info);

			return ret;
		}

		if (info_array[i].stream_info->channel_count == 0)
		{
			int m;

			printf("Error: stream %d has 0 channels!\n", i);

			asphodel_free_stream(info_array[i].stream_info);

			// free the partially filled info array
			for (m = 0; m < i; m++)
			{
				int n;
				for (n = 0; n < info_array[m].stream_info->channel_count; n++)
				{
					asphodel_free_channel(info_array[m].channel_info[n]);
				}
				free(info_array[m].channel_info);
				asphodel_free_stream(info_array[m].stream_info);
			}
			free(info_array);

			free(allocated_device_info);

			return 1;
		}

		info_array[i].channel_info = (AsphodelChannelInfo_t**)malloc(sizeof(AsphodelChannelInfo_t*) * info_array[i].stream_info->channel_count);
		if (info_array[i].channel_info == NULL)
		{
			int m;

			printf("Out of memory!\n");

			asphodel_free_stream(info_array[i].stream_info);

			// free the partially filled info array
			for (m = 0; m < i; m++)
			{
				int n;
				for (n = 0; n < info_array[m].stream_info->channel_count; n++)
				{
					asphodel_free_channel(info_array[m].channel_info[n]);
				}
				free(info_array[m].channel_info);
				asphodel_free_stream(info_array[m].stream_info);
			}
			free(info_array);

			free(allocated_device_info);

			return 1;
		}

		for (j = 0; j < info_array[i].stream_info->channel_count; j++)
		{
			uint8_t channel_index = info_array[i].stream_info->channel_index_list[j];
			ret = asphodel_get_channel_blocking(device, channel_index, &info_array[i].channel_info[j]);
			if (ret != 0)
			{
				int m;

				printf("Error %d in asphodel_get_channel_blocking(%d)\n", ret, j);

				// free partially filled channel array
				for (m = 0; m < j; m++)
				{
					asphodel_free_channel(info_array[i].channel_info[m]);
				}
				free(info_array[i].channel_info);

				asphodel_free_stream(info_array[i].stream_info);

				// free the partially filled info array
				for (m = 0; m < i; m++)
				{
					int n;
					for (n = 0; n < info_array[m].stream_info->channel_count; n++)
					{
						asphodel_free_channel(info_array[m].channel_info[n]);
					}
					free(info_array[m].channel_info);
					asphodel_free_stream(info_array[m].stream_info);
				}
				free(info_array);

				free(allocated_device_info);

				return ret;
			}
		}
	}

	ret = asphodel_create_device_decoder(info_array, count, filler_bits, id_bits, &decoder);
	if (ret != 0)
	{
		printf("Error %d in asphodel_create_device_decoder(%d)\n", ret, i);

		// free info_array
		for (i = 0; i < count; i++)
		{
			int j;
			for (j = 0; j < info_array[i].stream_info->channel_count; j++)
			{
				asphodel_free_channel(info_array[i].channel_info[j]);
			}
			free(info_array[i].channel_info);
			asphodel_free_stream(info_array[i].stream_info);
		}
		free(info_array);

		free(allocated_device_info);

		return ret;
	}

	allocated_device_info->decoder = decoder;
	allocated_device_info->stream_count = count;
	allocated_device_info->info_array = info_array;

	decoder->unknown_id_callback = unknown_id_callback;
	decoder->unknown_id_closure = allocated_device_info;

	for (i = 0; i < (int)decoder->streams; i++)
	{
		size_t j;
		AsphodelStreamDecoder_t *stream_decoder = decoder->decoders[i];
		AsphodelStreamInfo_t *stream_info = info_array[i].stream_info;
		char *info_str;

		info_str = (char*)malloc(256);
		if (info_str == NULL)
		{
			printf("Out of memory!\n");
			// NOTE: returning without freeing things; this will leak memory
			return 1;
		}
		snprintf(info_str, 256, "%s stream %d", allocated_device_info->serial_number, i);

		stream_decoder->lost_packet_callback = lost_packet_callback;
		stream_decoder->lost_packet_closure = info_str;

		for (j = 0; j < stream_decoder->channels; j++)
		{
			AsphodelChannelDecoder_t *channel_decoder = stream_decoder->decoders[j];
			AsphodelChannelInfo_t *channel_info = info_array[i].channel_info[j];
			ChannelClosure_t *c;

			ret = create_channel_closure(allocated_device_info->serial_number, stream_info, channel_info, channel_decoder, &c);
			if (ret != 0)
			{
				// error has already been printed
				// NOTE: returning without freeing things; this will leak memory
				return ret;
			}

			channel_decoder->callback = channel_decode_callback;
			channel_decoder->closure = c;

			// set the conversion factors from the unit formatter
			channel_decoder->set_conversion_factor(channel_decoder, c->unit_formatter->conversion_scale, c->unit_formatter->conversion_offset);

			write_csv_header(channel_decoder, c);
		}
	}

	allocated_device_info->packet_file = create_unique_file(allocated_device_info->serial_number, "Packets");
	if (allocated_device_info->packet_file == NULL)
	{
		printf("Error in create_unique_file(%s, Packets)\n", allocated_device_info->serial_number);
		// NOTE: returning without freeing things; this will leak memory
		return 1;
	}

	*device_info = allocated_device_info;
	return 0;
}

static void free_device_info(DeviceInfo_t *device_info)
{
	size_t i;

	for (i = 0; i < device_info->decoder->streams; i++)
	{
		size_t j;
		AsphodelStreamDecoder_t *stream_decoder = device_info->decoder->decoders[i];

		free(stream_decoder->lost_packet_closure);

		for (j = 0; j < stream_decoder->channels; j++)
		{
			AsphodelChannelDecoder_t *channel_decoder = stream_decoder->decoders[j];
			ChannelClosure_t *c = (ChannelClosure_t*)channel_decoder->closure;
			free_channel_closure(c);
		}
	}

	device_info->decoder->free_decoder(device_info->decoder);

	for (i = 0; i < (size_t)device_info->stream_count; i++)
	{
		int j;

		for (j = 0; j < device_info->info_array[i].stream_info->channel_count; j++)
		{
			asphodel_free_channel(device_info->info_array[i].channel_info[j]);
		}

		free(device_info->info_array[i].channel_info);
		asphodel_free_stream(device_info->info_array[i].stream_info);
	}

	free(device_info->info_array);
	free(device_info);
}

static void streaming_packet_callback(int status, const uint8_t *stream_data, size_t packet_size, size_t packet_count, void * closure)
{
	if (status == 0)
	{
		size_t i;
		DeviceInfo_t *device_info = (DeviceInfo_t*)closure;
		for (i = 0; i < packet_count; i++)
		{
			size_t j;
			const uint8_t *buffer = &stream_data[i * packet_size];
			device_info->decoder->decode(device_info->decoder, buffer);

			// add the packets to the packet file
			for (j = 0; j < packet_size; j++)
			{
				if (j != 0)
				{
					fprintf(device_info->packet_file, ",");
				}
				fprintf(device_info->packet_file, "0x%02x", buffer[j]);
			}
			fprintf(device_info->packet_file, "\n");
		}
	}
	else
	{
		printf("Bad status %d in streaming_packet_callback()\n", status);
	}
}

int main(void)
{
	int ret;
	size_t list_size = 0;
	size_t array_size;
	AsphodelDevice_t **device_array;
	DeviceInfo_t **device_info_array;
	size_t i;

	// initialize the library
	ret = asphodel_usb_init();
	if (ret != 0)
	{
		printf("Error %d in asphodel_usb_init()\n", ret);
		return ret;
	}

	// get the number of devices available
	ret = asphodel_usb_find_devices(NULL, &list_size);
	if (ret != 0)
	{
		printf("Error %d in 1st asphodel_usb_find_devices()\n", ret);
		return ret;
	}

	if (list_size == 0)
	{
		printf("No Devices Found!\n");
		return 0;
	}

	array_size = list_size;
	device_array = (AsphodelDevice_t**)malloc(sizeof(AsphodelDevice_t *) * array_size);
	if (device_array == NULL)
	{
		printf("Out of Memory!\n");
		return 1;
	}

	device_info_array = (DeviceInfo_t**)malloc(sizeof(DeviceInfo_t*) * array_size);
	if (device_info_array == NULL)
	{
		printf("Out of Memory!\n");
		free(device_array);
		return 1;
	}

	ret = asphodel_usb_find_devices(device_array, &list_size);
	if (ret != 0)
	{
		printf("Error %d in 2nd asphodel_usb_find_devices()\n", ret);
		free(device_array);
		free(device_info_array);
		return ret;
	}

	// take the minimum of array_size and list_size
	array_size = (array_size < list_size) ? array_size : list_size;

	if (array_size == 1)
	{
		printf("Found %d device!\n", (int)array_size);
	}
	else
	{
		printf("Found %d devices!\n", (int)array_size);
	}

	for (i = 0; i < array_size; i++)
	{
		AsphodelDevice_t *device = device_array[i];

		ret = device->open_device(device);
		if (ret != 0)
		{
			size_t j;

			printf("Error %d in device->open_device()\n", ret);

			for (j = 0; j < i; j++)
			{
				device_array[j]->close_device(device_array[j]);
				free_device_info(device_info_array[j]);
				device_array[j]->free_device(device_array[j]);
			}
			free(device_array);
			free(device_info_array);

			return ret;
		}

		ret = create_device_info(device, &device_info_array[i]);
		if (ret != 0)
		{
			size_t j;

			// already printed error

			device->close_device(device);

			for (j = 0; j < i; j++)
			{
				device_array[j]->close_device(device_array[j]);
				free_device_info(device_info_array[j]);
				device_array[j]->free_device(device_array[j]);
			}
			free(device_array);
			free(device_info_array);

			return ret;
		}
	}

	for (i = 0; i < array_size; i++)
	{
		double response_time;
		double buffer_time;
		int packet_count;
		int transfer_count;
		unsigned int timeout;
		int j;
		AsphodelDevice_t *device = device_array[i];
		DeviceInfo_t *device_info = device_info_array[i];

		if (device_info->stream_count == 1)
		{
			printf("Enabling %d stream from %s\n", device_info->stream_count, device_info->serial_number);
		}
		else
		{
			printf("Enabling %d streams from %s\n", device_info->stream_count, device_info->serial_number);
		}

		response_time = 0.100; // 100 milliseconds
		buffer_time = 0.500; // 500 milliseconds
		timeout = 1000; // 1000 milliseconds

		ret = asphodel_get_streaming_counts(device_info->info_array, device_info->stream_count, response_time, buffer_time, &packet_count, &transfer_count, &timeout);
		if (ret != 0)
		{
			size_t k;

			printf("Error %d in asphodel_get_streaming_counts()\n", ret);

			for (k = 0; k < array_size; k++)
			{
				AsphodelDevice_t *device = device_array[k];
				DeviceInfo_t *device_info = device_info_array[k];

				if (k < i)
				{
					int m;
					for (m = 0; m < device_info->stream_count; m++)
					{
						// ignore any errors; we're already closing the device
						asphodel_enable_stream_blocking(device, device_info->info_array[m].stream_id, 0);
					}

					device->stop_streaming_packets(device);
					device->poll_device(device, 10, NULL); // call poll so the cancelled stream callbacks can complete before closing the device
				}
				device->close_device(device);
				free_device_info(device_info);
				device->free_device(device);
			}
			free(device_array);
			free(device_info_array);

			return ret;
		}

		device->start_streaming_packets(device, packet_count, transfer_count, timeout, streaming_packet_callback, device_info);

		for (j = 0; j < device_info->stream_count; j++)
		{
			ret = asphodel_enable_stream_blocking(device, device_info->info_array[j].stream_id, 1);
			if (ret != 0)
			{
				size_t k;

				printf("Error %d in asphodel_enable_stream_blocking()\n", ret);

				for (k = 0; k < (size_t)j; k++)
				{
					// ignore any errors; we're already closing the device
					asphodel_enable_stream_blocking(device, device_info->info_array[k].stream_id, 0);
				}

				device->stop_streaming_packets(device);
				device->poll_device(device, 10, NULL);  // call poll so the cancelled stream callbacks can complete before closing the device

				for (k = 0; k < array_size; k++)
				{
					AsphodelDevice_t *device = device_array[k];
					DeviceInfo_t *device_info = device_info_array[k];

					if (k < i)
					{
						int m;
						for (m = 0; m < device_info->stream_count; m++)
						{
							// ignore any errors; we're already closing the device
							asphodel_enable_stream_blocking(device, device_info->info_array[m].stream_id, 0);
						}

						device->stop_streaming_packets(device);
						device->poll_device(device, 10, NULL); // call poll so the cancelled stream callbacks can complete before closing the device
					}
					device->close_device(device);
					free_device_info(device_info);
					device->free_device(device);
				}
				free(device_array);
				free(device_info_array);

				return ret;
			}
		}
	}

	printf("Press any key to stop data collection...\n");
	while (_kbhit() == 0)
	{
		asphodel_usb_poll_devices(100);
	}

	for (i = 0; i < array_size; i++)
	{
		int j;
		AsphodelDevice_t *device = device_array[i];
		DeviceInfo_t *device_info = device_info_array[i];

		if (device_info->stream_count == 1)
		{
			printf("Disabling %d stream from %s\n", device_info->stream_count, device_info->serial_number);
		}
		else
		{
			printf("Disabling %d streams from %s\n", device_info->stream_count, device_info->serial_number);
		}

		for (j = 0; j < device_info->stream_count; j++)
		{
			ret = asphodel_enable_stream_blocking(device, device_info->info_array[j].stream_id, 0);
			if (ret != 0)
			{
				printf("Error %d in asphodel_enable_stream_blocking()\n", ret);

				// might as well continue the cleanup process
				continue;
			}
		}
	}

	for (i = 0; i < array_size; i++)
	{
		AsphodelDevice_t *device = device_array[i];
		DeviceInfo_t *device_info = device_info_array[i];

		device->stop_streaming_packets(device);
		device->poll_device(device, 10, NULL); // call poll so the cancelled stream callbacks can complete before closing the device
		device->close_device(device);
		free_device_info(device_info);
		device->free_device(device);
	}

	free(device_array);
	free(device_info_array);

	// close the library
	asphodel_usb_deinit();

	return 0;
}
