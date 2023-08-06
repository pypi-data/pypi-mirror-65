/*
 * Copyright (c) 2017, Suprock Technologies
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

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include "asphodel.h"
#include "serialize.h"


typedef struct RemoteDeviceListNode_t {
	uint32_t serial_number;
	struct RemoteDeviceListNode_t * next;
} RemoteDeviceListNode_t;


static void delay_ms(unsigned int delay)
{
#ifdef _WIN32
	Sleep(delay);
#else
	usleep(delay * 1000);
#endif
}

static void print_utf8(const char *string)
{
#ifndef _WIN32
	// Linux supports UTF-8 in printf() natively
	printf("%s", string);
#else
	int ret;
	int len = MultiByteToWideChar(CP_UTF8, 0, string, -1, NULL, 0);
	wchar_t *tempWstr = (wchar_t*)malloc(sizeof(wchar_t) * len);
	if (tempWstr == NULL)
	{
		printf("<OUT OF MEMORY>");
		return;
	}

	ret = MultiByteToWideChar(CP_UTF8, 0, string, -1, tempWstr, len);
	if (ret == 0)
	{
		DWORD err = GetLastError();
		printf("<ERROR %lu>", err);
	}
	else
	{
		wprintf(L"%s", tempWstr);
	}

	free(tempWstr);
#endif
}

static char to_ascii(uint8_t value)
{
	if ((value >= 0x09 && value <= 0x0D) || value == 0x20)
	{
		// whitespace
		return ' ';
	}
	else if (value >= 0x21 && value <= 0x7E)
	{
		return (char)value;
	}
	else
	{
		return '.';
	}
}

static void print_nvm(uint8_t *data, size_t size, const char * prefix)
{
#define LINE_WIDTH 16 // bytes per line
	size_t i;
	char ascii_line[LINE_WIDTH + 1];

	for (i = 0; i < size; i++)
	{
		if (i % LINE_WIDTH == 0)
		{
			// beginning a line
			printf("%s", prefix);
		}

		// process the byte
		printf("%02x ", data[i]);
		ascii_line[i % LINE_WIDTH] = to_ascii(data[i]);

		if (i == size - 1)
		{
			// add padding to the end of the line
			size_t missing_bytes = (LINE_WIDTH - 1) - (i % LINE_WIDTH);
			size_t j;
			for (j = 0; j < missing_bytes; j++)
			{
				printf("   ");
			}
		}

		if (i % LINE_WIDTH == LINE_WIDTH - 1 || i == size - 1)
		{
			// ending a line
			ascii_line[i % LINE_WIDTH + 1] = '\0'; // null terminate
			printf("%s\n", ascii_line);
		}
	}
#undef LINE_WIDTH
}

static int print_nvm_info(AsphodelDevice_t *device)
{
	int ret;
	size_t nvm_size;
	size_t locations[6];
	char *user_tag_1;
	char *user_tag_2;
	uint8_t *data;
	uint8_t *nvm_data;
	int i;

	ret = asphodel_get_nvm_size_blocking(device, &nvm_size);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_nvm_size_blocking()\n", ret);
		return ret;
	}
	printf("NVM Size: %d\n", (int)nvm_size);

	ret = asphodel_get_user_tag_locations_blocking(device, locations);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_user_tag_locations_blocking()\n", ret);
		return ret;
	}
	printf("  User Tag Locations: [");
	for (i = 0; i < 6; i++)
	{
		if (i != 0)
		{
			printf(", ");
		}
		printf("%d", (int)locations[i]);
	}
	printf("]\n");

	user_tag_1 = (char *)malloc(locations[1] + 1);
	if (user_tag_1 == NULL)
	{
		printf("Out of Memory in print_nvm_info()!\n");
		return 1;
	}
	user_tag_1[locations[1]] = '\0'; // force null termination
	ret = asphodel_read_user_tag_string_blocking(device, locations[0], locations[1], user_tag_1);
	if (ret != 0)
	{
		printf("Error %d in 1st asphodel_read_user_tag_string_blocking()\n", ret);
		return ret;
	}
	printf("  User Tag 1: ");
	print_utf8(user_tag_1);
	printf("\n");

	free(user_tag_1);

	user_tag_2 = (char *)malloc(locations[3] + 1);
	if (user_tag_2 == NULL)
	{
		printf("Out of Memory in print_nvm_info()!\n");
		return 1;
	}
	user_tag_2[locations[3]] = '\0'; // force null termination
	ret = asphodel_read_user_tag_string_blocking(device, locations[2], locations[3], user_tag_2);
	if (ret != 0)
	{
		printf("Error %d in 2nd asphodel_read_user_tag_string_blocking()\n", ret);
		return ret;
	}
	printf("  User Tag 2: ");
	print_utf8(user_tag_2);
	printf("\n");

	free(user_tag_2);

	data = (uint8_t *)malloc(locations[5]);
	if (data == NULL)
	{
		printf("Out of Memory in print_nvm_info()!\n");
		return 1;
	}
	ret = asphodel_read_nvm_section_blocking(device, locations[4], data, locations[5]);
	if (ret != 0)
	{
		printf("Error %d in asphodel_read_nvm_section_blocking()\n", ret);
		return ret;
	}
	printf("  General Bytes:\n");
	print_nvm(data, locations[5], "    ");
	free(data);

	nvm_data = (uint8_t*)malloc(nvm_size);
	if (nvm_data == NULL)
	{
		printf("Out of Memory in print_nvm_info()!\n");
		return 1;
	}
	ret = asphodel_read_nvm_section_blocking(device, 0, nvm_data, nvm_size);
	if (ret != 0)
	{
		printf("Error %d in asphodel_read_nvm_section_blocking()\n", ret);
		return ret;
	}
	printf("  NVM Data:\n");
	print_nvm(nvm_data, nvm_size, "    ");
	free(nvm_data);

	return 0;
}

static int print_led_info(AsphodelDevice_t *device)
{
	int ret;
	int count;
	int i;

	ret = asphodel_get_rgb_count_blocking(device, &count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_rgb_count_blocking()\n", ret);
		return ret;
	}
	printf("RGB Count: %d\n", count);

	for (i = 0; i < count; i++)
	{
		uint8_t values[3];
		ret = asphodel_get_rgb_values_blocking(device, i, values);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_rgb_values_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("  RGB %d value: %d, %d, %d\n", i, values[0], values[2], values[2]);
	}

	ret = asphodel_get_led_count_blocking(device, &count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_led_count_blocking()\n", ret);
		return ret;
	}
	printf("LED Count: %d\n", count);

	for (i = 0; i < count; i++)
	{
		uint8_t value;
		ret = asphodel_get_led_value_blocking(device, i, &value);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_led_value_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("  LED %d value: %d\n", i, value);
	}

	return 0;
}

static int print_stream_info(AsphodelDevice_t *device)
{
	int ret;
	int count;
	int i;
	uint8_t filler_bits;
	uint8_t id_bits;

	ret = asphodel_get_stream_count_blocking(device, &count, &filler_bits, &id_bits);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_stream_count_blocking()\n", ret);
		return ret;
	}
	printf("Stream Count: %d (filler_bits=%d, id_bits=%d)\n", count, filler_bits, id_bits);

	for (i = 0; i < count; i++)
	{
		uint8_t channels[255];
		uint8_t channels_length = 255;
		AsphodelStreamInfo_t stream_info;
		int available;
		int channel_index;
		int invert;
		float scale;
		float offset;
		int enable;
		int warm_up;
		int j;

		printf("  Stream %d\n", i);

		ret = asphodel_get_stream_channels_blocking(device, i, channels, &channels_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_stream_channels_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    channels: [");
		for (j = 0; j < channels_length; j++)
		{
			if (j != 0)
			{
				printf(", ");
			}
			printf("%d", channels[j]);
		}
		printf("]\n");

		ret = asphodel_get_stream_format_blocking(device, i, &stream_info);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_stream_format_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    filler_bits=%d, counter_bits=%d\n", stream_info.filler_bits, stream_info.counter_bits);
		printf("    rate=%g, rate_error=%g%%\n", stream_info.rate, stream_info.rate_error * 100.0);
		printf("    warm_up_delay=%g\n", stream_info.warm_up_delay);

		ret = asphodel_get_stream_rate_info_blocking(device, i, &available, &channel_index, &invert, &scale, &offset);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_stream_rate_info_blocking(%d)\n", ret, i);
			return ret;
		}

		if (available)
		{
			printf("    rate_channel_index=%d, invert=%d, scale=%g, offset=%g\n", channel_index, invert, scale, offset);
		}
		else
		{
			printf("    no rate channel\n");
		}

		ret = asphodel_get_stream_status_blocking(device, i, &enable, &warm_up);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_stream_status_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    enable=%d, warm_up=%d\n", enable, warm_up);
	}

	return 0;
}

static int print_channel_info(AsphodelDevice_t *device)
{
	int ret;
	int count;
	int i;

	ret = asphodel_get_channel_count_blocking(device, &count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_channel_count_blocking()\n", ret);
		return ret;
	}
	printf("Channel Count: %d\n", count);

	for (i = 0; i < count; i++)
	{
		char channel_name[255];
		uint8_t channel_name_length = 255;
		AsphodelChannelInfo_t channel_info;
		float coefficients[255];
		uint8_t coefficients_length = 255;
		int available;
		AsphodelChannelCalibration_t calibration;
		int j;

		printf("  Channel %d\n", i);

		ret = asphodel_get_channel_name_blocking(device, i, channel_name, &channel_name_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_channel_name_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    name: ");
		print_utf8(channel_name);
		printf("\n");

		ret = asphodel_get_channel_info_blocking(device, i, &channel_info);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_channel_info_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    channel_type=%d (%s)\n", channel_info.channel_type, asphodel_channel_type_name(channel_info.channel_type));
		printf("    unit_type=%d (%s)\n", channel_info.unit_type, asphodel_unit_type_name(channel_info.unit_type));
		printf("    filler_bits=%d, data_bits=%d\n", channel_info.filler_bits, channel_info.data_bits);
		printf("    samples=%d, bits_per_sample=%d\n", channel_info.samples, channel_info.bits_per_sample);
		printf("    minimum=%g, maximum=%g, resolution=%g\n", channel_info.minimum, channel_info.maximum, channel_info.resolution);

		ret = asphodel_get_channel_coefficients_blocking(device, i, coefficients, &coefficients_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_channel_coefficients_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    coefficients: [");
		for (j = 0; j < coefficients_length; j++)
		{
			if (j != 0)
			{
				printf(", ");
			}
			printf("%g", coefficients[j]);
		}
		printf("]\n");

		printf("    chunk_count=%d\n", channel_info.chunk_count);
		for (j = 0; j < channel_info.chunk_count; j++)
		{
			uint8_t chunk[255];
			uint8_t chunk_length = 255;
			int k;

			ret = asphodel_get_channel_chunk_blocking(device, i, j, chunk, &chunk_length);
			if (ret != 0)
			{
				printf("Error %d in asphodel_get_channel_chunk_blocking(%d, %d)\n", ret, i, j);
				return ret;
			}
			printf("      Chunk %d: [", j);
			for (k = 0; k < chunk_length; k++)
			{
				if (k != 0)
				{
					printf(",");
				}
				printf("%02x", chunk[k]);
			}
			printf("]\n");
		}

		ret = asphodel_get_channel_calibration_blocking(device, i, &available, &calibration);
		if (ret == ERROR_CODE_UNIMPLEMENTED_COMMAND)
		{
			available = 0;
		}
		else if (ret != 0)
		{
			printf("Error %d in asphodel_get_channel_calibration_blocking(%d)\n", ret, i);
			return ret;
		}

		if (available)
		{
			printf("    calibration base setting=%d, calibration resolution setting=%d\n", calibration.base_setting_index, calibration.resolution_setting_index);
			printf("    calibration scale=%g, calibration offset=%g\n", calibration.scale, calibration.offset);
			printf("    calibration minimum=%g, calibration maximum=%g\n", calibration.minimum, calibration.maximum);
		}
		else
		{
			printf("    no calibration info\n");
		}
	}

	return 0;
}

static int print_channel_specific_info(AsphodelDevice_t *device)
{
	int ret;
	int count;
	int i;

	ret = asphodel_get_channel_count_blocking(device, &count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_channel_count_blocking()\n", ret);
		return ret;
	}

	if (count == 0)
	{
		// no channels
		return 0;
	}

	printf("Channel Specifics for %d Channels:\n", count);

	for (i = 0; i < count; i++)
	{
		AsphodelChannelInfo_t *channel_info;

		ret = asphodel_get_channel_blocking(device, i, &channel_info);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_channel_blocking(%d)\n", ret, i);
			return ret;
		}

		if (channel_info->channel_type == CHANNEL_TYPE_SLOW_STRAIN ||
			channel_info->channel_type == CHANNEL_TYPE_FAST_STRAIN ||
			channel_info->channel_type == CHANNEL_TYPE_COMPOSITE_STRAIN)
		{
			// do strain channel specific functions
			int bridge_count;
			int bridge_index;

			printf("  Channel %d Strain Specific:\n", i);

			ret = asphodel_get_strain_bridge_count(channel_info, &bridge_count);
			if (ret != 0)
			{
				printf("Error %d in asphodel_get_strain_bridge_count() for channel %d\n", ret, i);
				return ret;
			}

			for (bridge_index = 0; bridge_index < bridge_count; bridge_index++)
			{
				size_t subchannel_index;
				float bridge_values[5];

				ret = asphodel_get_strain_bridge_subchannel(channel_info, bridge_index, &subchannel_index);
				if (ret != 0)
				{
					printf("Error %d in asphodel_get_strain_bridge_subchannel() for channel %d\n", ret, i);
					return ret;
				}

				ret = asphodel_get_strain_bridge_values(channel_info, bridge_index, bridge_values);
				if (ret != 0)
				{
					printf("Error %d in asphodel_get_strain_bridge_values() for channel %d\n", ret, i);
					return ret;
				}

				printf("    Bridge %d (subchannel_index=%d):\n", bridge_index, (int)subchannel_index);
				printf("      positive sense=%g\n", bridge_values[0]);
				printf("      negative sense=%g\n", bridge_values[1]);
				printf("      bridge element nominal=%g\n", bridge_values[2]);
				printf("      bridge element minimum=%g\n", bridge_values[3]);
				printf("      bridge element maximum=%g\n", bridge_values[4]);
			}
		}
		else if (channel_info->channel_type == CHANNEL_TYPE_SLOW_ACCEL || channel_info->channel_type == CHANNEL_TYPE_PACKED_ACCEL || channel_info->channel_type == CHANNEL_TYPE_LINEAR_ACCEL)
		{
			// do accel channel specific functions
			float limits[6];
			AsphodelUnitFormatter_t *formatter;

			ret = asphodel_get_accel_self_test_limits(channel_info, limits);
			if (ret != 0)
			{
				printf("Error %d in asphodel_get_accel_self_test_limits() for channel %d\n", ret, i);
				return ret;
			}

			printf("  Channel %d Accel Specific:\n", i);

			formatter = asphodel_create_unit_formatter(channel_info->unit_type, channel_info->minimum, channel_info->maximum, channel_info->resolution, 1);

			if (formatter == NULL)
			{
				printf("    X axis self test difference: min=%g, max=%g\n", limits[0], limits[1]);
				printf("    Y axis self test difference: min=%g, max=%g\n", limits[2], limits[3]);
				printf("    Z axis self test difference: min=%g, max=%g\n", limits[4], limits[5]);
			}
			else
			{
				char min_buffer[64];
				char max_buffer[64];

				formatter->format_ascii(formatter, min_buffer, sizeof(min_buffer), limits[0] * formatter->conversion_scale + formatter->conversion_offset);
				formatter->format_ascii(formatter, max_buffer, sizeof(max_buffer), limits[1] * formatter->conversion_scale + formatter->conversion_offset);
				printf("    X axis self test difference: min=%s, max=%s\n", min_buffer, max_buffer);

				formatter->format_ascii(formatter, min_buffer, sizeof(min_buffer), limits[2] * formatter->conversion_scale + formatter->conversion_offset);
				formatter->format_ascii(formatter, max_buffer, sizeof(max_buffer), limits[3] * formatter->conversion_scale + formatter->conversion_offset);
				printf("    Y axis self test difference: min=%s, max=%s\n", min_buffer, max_buffer);

				formatter->format_ascii(formatter, min_buffer, sizeof(min_buffer), limits[4] * formatter->conversion_scale + formatter->conversion_offset);
				formatter->format_ascii(formatter, max_buffer, sizeof(max_buffer), limits[5] * formatter->conversion_scale + formatter->conversion_offset);
				printf("    Z axis self test difference: min=%s, max=%s\n", min_buffer, max_buffer);

				formatter->free(formatter);
			}
		}
		else
		{
			printf("  Channel %d No Specifics\n", i);
		}

		asphodel_free_channel(channel_info);
	}

	return 0;
}

static int print_decoder_info(AsphodelDevice_t *device)
{
	int ret;
	int count;
	int i;
	uint8_t filler_bits;
	uint8_t id_bits;
	AsphodelDeviceDecoder_t *decoder;
	AsphodelStreamAndChannels_t *info_array;

	ret = asphodel_get_stream_count_blocking(device, &count, &filler_bits, &id_bits);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_stream_count_blocking()\n", ret);
		return ret;
	}

	if (count == 0)
	{
		// no streams
		return 0;
	}

	info_array = (AsphodelStreamAndChannels_t*)malloc(sizeof(AsphodelStreamAndChannels_t) * count);
	if (info_array == NULL)
	{
		printf("Out of memory!\n");
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

		return ret;
	}

	printf("Device Decoder: streams=%d, id_byte_offset=%d\n", (int)decoder->streams, (int)decoder->id_byte_offset);

	for (i = 0; i < (int)decoder->streams; i++)
	{
		int j;
		AsphodelStreamDecoder_t *stream_decoder = decoder->decoders[i];

		printf("  Stream Decoder %d:\n", i);
		printf("    id=%d, counter_byte_offset=%d, channels=%d\n", decoder->stream_ids[i], (int)stream_decoder->counter_byte_offset, (int)stream_decoder->channels);

		for (j = 0; j < (int)stream_decoder->channels; j++)
		{
			int k;
			AsphodelChannelDecoder_t *channel_decoder = stream_decoder->decoders[j];

			printf("    Channel Decoder %d:\n", j);
			printf("      name=");
			print_utf8(channel_decoder->channel_name);
			printf("\n");
			printf("      channel_bit_offset=%d, samples=%d, subchannels=%d\n", channel_decoder->channel_bit_offset, (int)channel_decoder->samples, (int)channel_decoder->subchannels);

			for (k = 0; k < (int)channel_decoder->subchannels; k++)
			{
				printf("        subchannel %d name=", k);
				print_utf8(channel_decoder->subchannel_names[k]);
				printf("\n");
			}
		}
	}

	decoder->free_decoder(decoder);

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

	return 0;
}

static int print_supply_info(AsphodelDevice_t *device)
{
	int ret;
	int count;
	int i;

	ret = asphodel_get_supply_count_blocking(device, &count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_supply_count_blocking()\n", ret);
		return ret;
	}
	printf("Supply Count: %d\n", count);

	for (i = 0; i < count; i++)
	{
		char supply_name[255];
		uint8_t supply_name_length = 255;
		AsphodelSupplyInfo_t supply_info;
		int32_t measurement;
		uint8_t result;
		double converted_measurement;
		const char * passfail;
		char formatted_buffer[255];

		printf("  Supply %d\n", i);

		ret = asphodel_get_supply_name_blocking(device, i, supply_name, &supply_name_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_supply_name_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    name: ");
		print_utf8(supply_name);
		printf("\n");

		ret = asphodel_get_supply_info_blocking(device, i, &supply_info);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_supply_info_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    unit_type=%d (%s)\n", supply_info.unit_type, asphodel_unit_type_name(supply_info.unit_type));
		printf("    is_battery=%d, nominal=%d\n", supply_info.is_battery, supply_info.nominal);
		printf("    scale=%g, offset=%g\n", supply_info.scale, supply_info.offset);

		ret = asphodel_check_supply_blocking(device, i, &measurement, &result, 20);
		if (ret != 0)
		{
			printf("Error %d in asphodel_check_supply_blocking(%d)\n", ret, i);
			return ret;
		}
		converted_measurement = measurement * supply_info.scale + supply_info.offset;
		if (result == 0)
		{
			passfail = "pass";
		}
		else
		{
			passfail = "FAIL";
		}
		printf("    measurement=%d (%g), result=0x%02x (%s)\n", measurement, converted_measurement, result, passfail);

		asphodel_format_value_ascii(formatted_buffer, 255, supply_info.unit_type, supply_info.scale, 1, converted_measurement);
		printf("    formatted (use_metric=1): %s\n", formatted_buffer);
		asphodel_format_value_ascii(formatted_buffer, 255, supply_info.unit_type, supply_info.scale, 0, converted_measurement);
		printf("    formatted (use_metric=0): %s\n", formatted_buffer);
	}

	return 0;
}

static int print_ctrl_var_info(AsphodelDevice_t *device)
{
	int ret;
	int count;
	int i;

	ret = asphodel_get_ctrl_var_count_blocking(device, &count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_ctrl_var_count_blocking()\n", ret);
		return ret;
	}
	printf("Control Variable Count: %d\n", count);

	for (i = 0; i < count; i++)
	{
		char var_name[255];
		uint8_t var_name_length = 255;
		AsphodelCtrlVarInfo_t ctrl_var_info;
		int32_t value;
		double converted_value;
		char formatted_buffer[255];

		printf("  Control Variable %d\n", i);

		ret = asphodel_get_ctrl_var_name_blocking(device, i, var_name, &var_name_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_ctrl_var_name_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    name: ");
		print_utf8(var_name);
		printf("\n");

		ret = asphodel_get_ctrl_var_info_blocking(device, i, &ctrl_var_info);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_ctrl_var_info_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    unit_type=%d (%s)\n", ctrl_var_info.unit_type, asphodel_unit_type_name(ctrl_var_info.unit_type));
		printf("    minimum=%d, maximum=%d\n", ctrl_var_info.minimum, ctrl_var_info.maximum);
		printf("    scale=%g, offset=%g\n", ctrl_var_info.scale, ctrl_var_info.offset);

		ret = asphodel_get_ctrl_var_blocking(device, i, &value);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_ctrl_var_blocking(%d)\n", ret, i);
			return ret;
		}
		converted_value = value * ctrl_var_info.scale + ctrl_var_info.offset;
		printf("    value=%d (%g)\n", value, converted_value);

		asphodel_format_value_ascii(formatted_buffer, 255, ctrl_var_info.unit_type, ctrl_var_info.scale, 1, converted_value);
		printf("    formatted (use_metric=1): %s\n", formatted_buffer);
		asphodel_format_value_ascii(formatted_buffer, 255, ctrl_var_info.unit_type, ctrl_var_info.scale, 0, converted_value);
		printf("    formatted (use_metric=0): %s\n", formatted_buffer);
	}

	return 0;
}

static int print_setting_info(AsphodelDevice_t *device)
{
	int ret;
	int count;
	int i;
	size_t nvm_size;
	uint8_t *nvm_data;

	ret = asphodel_get_setting_count_blocking(device, &count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_setting_count_blocking()\n", ret);
		return ret;
	}
	printf("Setting Count: %d\n", count);

	if (count == 0)
	{
		return 0;
	}

	ret = asphodel_get_nvm_size_blocking(device, &nvm_size);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_nvm_size_blocking()\n", ret);
		return ret;
	}

	nvm_data = (uint8_t*)malloc(nvm_size);
	if (nvm_data == NULL)
	{
		printf("Out of Memory in print_setting_info()!\n");
		return 1;
	}
	ret = asphodel_read_nvm_section_blocking(device, 0, nvm_data, nvm_size);
	if (ret != 0)
	{
		printf("Error %d in asphodel_read_nvm_section_blocking()\n", ret);
		return ret;
	}

	for (i = 0; i < count; i++)
	{
		char setting_name[255];
		uint8_t setting_name_length = 255;
		AsphodelSettingInfo_t setting_info;
		uint8_t default_bytes[255];
		uint8_t default_bytes_length = 255;
		int j;

		printf("  Setting %d\n", i);

		ret = asphodel_get_setting_name_blocking(device, i, setting_name, &setting_name_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_setting_name_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    name: ");
		print_utf8(setting_name);
		printf("\n");

		ret = asphodel_get_setting_info_blocking(device, i, &setting_info);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_setting_info_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    setting_type=%d (%s)\n", setting_info.setting_type, asphodel_setting_type_name(setting_info.setting_type));

		ret = asphodel_get_setting_default_blocking(device, i, default_bytes, &default_bytes_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_setting_default_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    default_bytes=[");
		for (j = 0; j < default_bytes_length; j++)
		{
			if (j != 0)
			{
				printf(",");
			}
			printf("%02x", default_bytes[j]);
		}
		printf("]\n");

		switch (setting_info.setting_type)
		{
		case SETTING_TYPE_BYTE:
			{
				size_t byte_offset;
				uint8_t value;
				if (default_bytes_length == 1)
				{
					printf("    default=%d\n", default_bytes[0]);
				}
				else
				{
					printf("    default=<ERROR>\n");
				}
				printf("    nvm_word=%d, nvm_word_byte=%d\n", setting_info.u.byte_setting.nvm_word, setting_info.u.byte_setting.nvm_word_byte);
				byte_offset = (setting_info.u.byte_setting.nvm_word * 4) + setting_info.u.byte_setting.nvm_word_byte;
				value = nvm_data[byte_offset];
				printf("    value=%d\n", value);
			}
			break;
		case SETTING_TYPE_BOOLEAN:
			{
				size_t byte_offset;
				uint8_t value;
				const char *truefalse;
				if (default_bytes_length == 1)
				{
					if (default_bytes[0])
					{
						truefalse = "TRUE";
					}
					else
					{
						truefalse = "FALSE";
					}
					printf("    default=%d (%s)\n", default_bytes[0], truefalse);
				}
				else
				{
					printf("    default=<ERROR>\n");
				}
				printf("    nvm_word=%d, nvm_word_byte=%d\n", setting_info.u.byte_setting.nvm_word, setting_info.u.byte_setting.nvm_word_byte);
				byte_offset = (setting_info.u.byte_setting.nvm_word * 4) + setting_info.u.byte_setting.nvm_word_byte;
				value = nvm_data[byte_offset];
				if (value)
				{
					truefalse = "TRUE";
				}
				else
				{
					truefalse = "FALSE";
				}
				printf("    value=%d (%s)\n", value, truefalse);
			}
			break;
		case SETTING_TYPE_UNIT_TYPE:
			{
				size_t byte_offset;
				uint8_t value;
				if (default_bytes_length == 1)
				{
					printf("    default=%d (%s)\n", default_bytes[0], asphodel_unit_type_name(default_bytes[0]));
				}
				else
				{
					printf("    default=<ERROR>\n");
				}
				printf("    nvm_word=%d, nvm_word_byte=%d\n", setting_info.u.byte_setting.nvm_word, setting_info.u.byte_setting.nvm_word_byte);
				byte_offset = (setting_info.u.byte_setting.nvm_word * 4) + setting_info.u.byte_setting.nvm_word_byte;
				value = nvm_data[byte_offset];
				printf("    value=%d (%s)\n", value, asphodel_unit_type_name(value));
			}
			break;
		case SETTING_TYPE_CHANNEL_TYPE:
			{
				size_t byte_offset;
				uint8_t value;
				if (default_bytes_length == 1)
				{
					printf("    default=%d (%s)\n", default_bytes[0], asphodel_channel_type_name(default_bytes[0]));
				}
				else
				{
					printf("    default=<ERROR>\n");
				}
				printf("    nvm_word=%d, nvm_word_byte=%d\n", setting_info.u.byte_setting.nvm_word, setting_info.u.byte_setting.nvm_word_byte);
				byte_offset = (setting_info.u.byte_setting.nvm_word * 4) + setting_info.u.byte_setting.nvm_word_byte;
				value = nvm_data[byte_offset];
				printf("    value=%d (%s)\n", value, asphodel_channel_type_name(value));
			}
			break;
		case SETTING_TYPE_BYTE_ARRAY:
			{
				size_t length_byte_offset;
				uint8_t length;
				int j;

				printf("    default=[");
				for (j = 0; j < default_bytes_length; j++)
				{
					if (j != 0)
					{
						printf(",");
					}
					printf("%02x", default_bytes[j]);
				}
				printf("]\n");

				printf("    nvm_word=%d, maximum_length=%d\n", setting_info.u.byte_array_setting.nvm_word, setting_info.u.byte_array_setting.maximum_length);
				printf("    length_nvm_word=%d, length_nvm_word_byte=%d\n", setting_info.u.byte_array_setting.length_nvm_word,
						setting_info.u.byte_array_setting.length_nvm_word_byte);
				length_byte_offset = (setting_info.u.byte_array_setting.length_nvm_word * 4) + setting_info.u.byte_array_setting.length_nvm_word_byte;
				length = nvm_data[length_byte_offset];
				if (length > setting_info.u.byte_array_setting.maximum_length)
				{
					length = setting_info.u.byte_array_setting.maximum_length;
				}
				printf("    value=[");
				for (j = 0; j < length; j++)
				{
					if (j != 0)
					{
						printf(",");
					}
					printf("%02x", nvm_data[setting_info.u.byte_array_setting.nvm_word * 4 + j]);
				}
				printf("]\n");
			}
			break;
		case SETTING_TYPE_STRING:
			{
				int j;
				char string_value[256];

				memcpy(string_value, default_bytes, default_bytes_length);
				string_value[default_bytes_length] = '\0';
				printf("    default=");
				print_utf8(string_value);
				printf("\n");

				printf("    nvm_word=%d, maximum_length=%d\n", setting_info.u.string_setting.nvm_word, setting_info.u.string_setting.maximum_length);
				memcpy(string_value, &nvm_data[setting_info.u.byte_array_setting.nvm_word * 4], setting_info.u.string_setting.maximum_length);
				string_value[setting_info.u.string_setting.maximum_length] = '\0';
				for (j = 0; j < setting_info.u.string_setting.maximum_length; j++)
				{
					if ((uint8_t)string_value[j] == 0xFF)
					{
						string_value[j] = '\0';
					}
				}
				printf("    value=");
				print_utf8(string_value);
				printf("\n");
			}
			break;
		case SETTING_TYPE_INT32:
			{
				int32_t value;

				if (default_bytes_length == 4)
				{
					value = read_32bit_value(default_bytes);
					printf("    default=%d\n", value);
				}
				else
				{
					printf("    default=<ERROR>\n");
				}

				printf("    nvm_word=%d\n", setting_info.u.int32_setting.nvm_word);
				printf("    minimum=%d, maximum=%d\n", setting_info.u.int32_setting.minimum, setting_info.u.int32_setting.maximum);
				value = read_32bit_value(&nvm_data[setting_info.u.int32_setting.nvm_word * 4]);
				printf("    value=%d\n", value);
			}
			break;
		case SETTING_TYPE_INT32_SCALED:
			{
				int32_t value;
				double scaled_value;

				if (default_bytes_length == 4)
				{
					value = read_32bit_value(default_bytes);
					scaled_value = (double)value * (double)setting_info.u.int32_scaled_setting.scale + (double)setting_info.u.int32_scaled_setting.offset;
					printf("    default=%d, default_scaled=%g\n", value, scaled_value);
				}
				else
				{
					printf("    default=<ERROR>\n");
				}

				printf("    nvm_word=%d\n", setting_info.u.int32_scaled_setting.nvm_word);
				printf("    minimum=%d, maximum=%d\n", setting_info.u.int32_scaled_setting.minimum, setting_info.u.int32_scaled_setting.maximum);
				printf("    unit_type=%d (%s)\n", setting_info.u.int32_scaled_setting.unit_type, asphodel_unit_type_name(setting_info.u.int32_scaled_setting.unit_type));
				printf("    scale=%g, offset=%g\n", setting_info.u.int32_scaled_setting.scale, setting_info.u.int32_scaled_setting.offset);
				value = read_32bit_value(&nvm_data[setting_info.u.int32_scaled_setting.nvm_word * 4]);
				scaled_value = (double)value * (double)setting_info.u.int32_scaled_setting.scale + (double)setting_info.u.int32_scaled_setting.offset;
				printf("    value=%d, scaled=%g\n", value, scaled_value);
			}
			break;
		case SETTING_TYPE_FLOAT:
			{
				float value;
				double scaled_value;

				if (default_bytes_length == 4)
				{
					value = read_float_value(default_bytes);
					scaled_value = (double)value * (double)setting_info.u.float_setting.scale + (double)setting_info.u.float_setting.offset;
					printf("    default=%g, default_scaled=%g\n", value, scaled_value);
				}
				else
				{
					printf("    default=<ERROR>\n");
				}

				printf("    nvm_word=%d\n", setting_info.u.float_setting.nvm_word);
				printf("    minimum=%g, maximum=%g\n", setting_info.u.float_setting.minimum, setting_info.u.float_setting.maximum);
				printf("    unit_type=%d (%s)\n", setting_info.u.float_setting.unit_type, asphodel_unit_type_name(setting_info.u.float_setting.unit_type));
				printf("    scale=%g, offset=%g\n", setting_info.u.float_setting.scale, setting_info.u.float_setting.offset);
				value = read_float_value(&nvm_data[setting_info.u.float_setting.nvm_word * 4]);
				scaled_value = (double)value * (double)setting_info.u.float_setting.scale + (double)setting_info.u.float_setting.offset;
				printf("    value=%g, scaled=%g\n", value, scaled_value);
			}
			break;
		case SETTING_TYPE_FLOAT_ARRAY:
			{
				size_t length_byte_offset;
				uint8_t length;
				int j;

				if (default_bytes_length % 4 == 0)
				{
					printf("    default=[");
					for (j = 0; j < default_bytes_length / 4; j++)
					{
						float value;
						double scaled_value;

						value = read_float_value(&default_bytes[j * 4]);
						scaled_value = (double)value * (double)setting_info.u.float_array_setting.scale + (double)setting_info.u.float_array_setting.offset;

						if (j != 0)
						{
							printf(",");
						}
						printf("%g", scaled_value);
					}
					printf("]\n");
				}
				else
				{
					printf("    default=<ERROR>\n");
				}

				printf("    nvm_word=%d\n", setting_info.u.float_array_setting.nvm_word);
				printf("    minimum=%g, maximum=%g\n", setting_info.u.float_array_setting.minimum, setting_info.u.float_array_setting.maximum);
				printf("    unit_type=%d (%s)\n", setting_info.u.float_array_setting.unit_type, asphodel_unit_type_name(setting_info.u.float_array_setting.unit_type));
				printf("    scale=%g, offset=%g\n", setting_info.u.float_array_setting.scale, setting_info.u.float_array_setting.offset);
				printf("    maximum_length=%d\n", setting_info.u.float_array_setting.maximum_length);
				printf("    length_nvm_word=%d, length_nvm_word_byte=%d\n", setting_info.u.float_array_setting.length_nvm_word,
						setting_info.u.float_array_setting.length_nvm_word_byte);
				length_byte_offset = (setting_info.u.float_array_setting.length_nvm_word * 4) + setting_info.u.float_array_setting.length_nvm_word_byte;
				length = nvm_data[length_byte_offset];
				if (length > setting_info.u.float_array_setting.maximum_length)
				{
					length = setting_info.u.float_array_setting.maximum_length;
				}
				printf("    value=[");
				for (j = 0; j < length; j++)
				{
					float value;
					double scaled_value;

					value = read_float_value(&nvm_data[setting_info.u.float_array_setting.nvm_word * 4 + j * 4]);
					scaled_value = (double)value * (double)setting_info.u.float_array_setting.scale + (double)setting_info.u.float_array_setting.offset;

					if (j != 0)
					{
						printf(",");
					}
					printf("%g", scaled_value);
				}
				printf("]\n");
			}
			break;
		case SETTING_TYPE_CUSTOM_ENUM:
			{
				char value_name[255];
				uint8_t value_name_length = 255;
				size_t byte_offset;
				uint8_t index;
				uint8_t value;

				index = setting_info.u.custom_enum_setting.custom_enum_index;

				if (default_bytes_length == 1)
				{
					ret = asphodel_get_custom_enum_value_name_blocking(device, index, default_bytes[0], value_name, &value_name_length);
					if (ret == 0)
					{
						printf("    default=%d (", default_bytes[0]);
						print_utf8(value_name);
						printf(")\n");
					}
					else if (ret == ERROR_CODE_BAD_INDEX)
					{
						printf("    default=%d (<ERROR>)\n", default_bytes[0]);
					}
					else
					{
						printf("Error %d in asphodel_get_custom_enum_value_name_blocking()\n", ret);
						return ret;
					}
				}
				else
				{
					printf("    default=<ERROR>\n");
				}

				printf("    nvm_word=%d, nvm_word_byte=%d\n", setting_info.u.custom_enum_setting.nvm_word, setting_info.u.custom_enum_setting.nvm_word_byte);
				printf("    custom_enum_index=%d\n", setting_info.u.custom_enum_setting.custom_enum_index);
				byte_offset = (setting_info.u.custom_enum_setting.nvm_word * 4) + setting_info.u.custom_enum_setting.nvm_word_byte;
				value = nvm_data[byte_offset];

				value_name_length = 255; // needs to be reset after last call
				ret = asphodel_get_custom_enum_value_name_blocking(device, index, value, value_name, &value_name_length);
				if (ret == 0)
				{
					printf("    value=%d (", value);
					print_utf8(value_name);
					printf(")\n");
				}
				else if (ret == ERROR_CODE_BAD_INDEX)
				{
					printf("    value=%d (<ERROR>)\n", value);
				}
				else
				{
					printf("Error %d in asphodel_get_custom_enum_value_name_blocking()\n", ret);
					return ret;
				}
			}
			break;
		default:
			printf("    unknown setting type!");
			break;
		}
	}

	free(nvm_data);

	return 0;
}

static int print_custom_enum_info(AsphodelDevice_t *device)
{
	int ret;
	uint8_t counts[255];
	uint8_t counts_length = 255;
	int i;

	ret = asphodel_get_custom_enum_counts_blocking(device, counts, &counts_length);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_custom_enum_counts_blocking()\n", ret);
		return ret;
	}
	printf("Custom Enum Count: %d\n", counts_length);

	for (i = 0; i < counts_length; i++)
	{
		int j;

		printf("  Custom Enum %d\n", i);

		for (j = 0; j < counts[i]; j++)
		{
			char value_name[255];
			uint8_t value_name_length = 255;

			ret = asphodel_get_custom_enum_value_name_blocking(device, i, j, value_name, &value_name_length);
			if (ret != 0)
			{
				printf("Error %d in asphodel_get_custom_enum_value_name_blocking()\n", ret);
				return ret;
			}

			printf("    %d: ", j);
			print_utf8(value_name);
			printf("\n");
		}
	}

	return 0;
}

static int print_setting_category_info(AsphodelDevice_t *device)
{
	int ret;
	int count;
	int i;

	ret = asphodel_get_setting_category_count_blocking(device, &count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_setting_category_count_blocking()\n", ret);
		return ret;
	}
	printf("Setting Category Count: %d\n", count);

	for (i = 0; i < count; i++)
	{
		char setting_category_name[255];
		uint8_t setting_category_name_length = 255;
		uint8_t settings[255];
		uint8_t settings_length = 255;
		int j;

		printf("  Setting Category %d\n", i);

		ret = asphodel_get_setting_category_name_blocking(device, i, setting_category_name, &setting_category_name_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_gpio_port_name_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    name: ");
		print_utf8(setting_category_name);
		printf("\n");

		ret = asphodel_get_setting_category_settings_blocking(device, i, settings, &settings_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_setting_category_settings_blocking(%d)\n", ret, i);
			return ret;
		}

		printf("    settings: [");
		for (j = 0; j < settings_length; j++)
		{
			if (j != 0)
			{
				printf(", ");
			}
			printf("%d", settings[j]);
		}
		printf("]\n");
	}

	return 0;
}

static int print_low_level_info(AsphodelDevice_t *device)
{
	int ret;
	int i;
	int gpio_port_count;
	int spi_count;
	int i2c_count;
	int info_region_count;
	uint32_t stack_info[2];

	ret = asphodel_get_gpio_port_count_blocking(device, &gpio_port_count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_gpio_port_count_blocking()\n", ret);
		return ret;
	}
	printf("GPIO Port Count: %d\n", gpio_port_count);

	for (i = 0; i < gpio_port_count; i++)
	{
		char port_name[255];
		uint8_t port_name_length = 255;
		AsphodelGPIOPortInfo_t gpio_port_info;
		uint32_t pin_values;

		printf("  GPIO Port %d\n", i);

		ret = asphodel_get_gpio_port_name_blocking(device, i, port_name, &port_name_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_gpio_port_name_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    name: ");
		print_utf8(port_name);
		printf("\n");

		ret = asphodel_get_gpio_port_info_blocking(device, i, &gpio_port_info);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_gpio_port_info_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    input_pins=0x%08x\n", gpio_port_info.input_pins);
		printf("    output_pins=0x%08x\n", gpio_port_info.output_pins);
		printf("    floating_pins=0x%08x\n", gpio_port_info.floating_pins);
		printf("    loaded_pins=0x%08x\n", gpio_port_info.loaded_pins);
		printf("    overridden_pins=0x%08x\n", gpio_port_info.overridden_pins);

		ret = asphodel_get_gpio_port_values_blocking(device, i, &pin_values);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_gpio_port_values_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    pin_values=0x%08x\n", pin_values);
	}

	ret = asphodel_get_bus_counts_blocking(device, &spi_count, &i2c_count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_bus_counts_blocking()\n", ret);
		return ret;
	}
	printf("SPI Bus Count: %d\n", spi_count);
	printf("I2C Bus Count: %d\n", i2c_count);

	ret = asphodel_get_info_region_count_blocking(device, &info_region_count);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_info_region_count_blocking()\n", ret);
		return ret;
	}
	printf("Info Region Count: %d\n", info_region_count);

	for (i = 0; i < info_region_count; i++)
	{
		char info_region_name[255];
		uint8_t info_region_name_length = 255;
		uint8_t data[255];
		uint8_t data_length = 255;
		int j;

		printf("  Info Region %d\n", i);

		ret = asphodel_get_info_region_name_blocking(device, i, info_region_name, &info_region_name_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_info_region_name_blocking(%d)\n", ret, i);
			return ret;
		}
		printf("    name: ");
		print_utf8(info_region_name);
		printf("\n");

		ret = asphodel_get_info_region_blocking(device, i, data, &data_length);
		if (ret != 0)
		{
			printf("Error %d in asphodel_get_info_region_blocking(%d)\n", ret, i);
			return ret;
		}

		printf("    values: [");
		for (j = 0; j < data_length; j++)
		{
			if (j != 0)
			{
				printf(",");
			}
			printf("%02x", data[j]);
		}
		printf("]\n");
	}

	ret = asphodel_get_stack_info_blocking(device, stack_info);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_stack_info_blocking()\n", ret);
		return ret;
	}
	printf("Stack Info: free=%u, used=%u\n", stack_info[0], stack_info[1]);

	return 0;
}

static int print_rf_power_info(AsphodelDevice_t *device)
{
	uint8_t rf_ctrl_vars[255];
	uint8_t rf_ctrl_vars_length = 255;
	int ret;
	int supported = asphodel_supports_rf_power_commands(device);
	const char * supported_str;
	int enabled;
	int i;

	if (supported)
	{
		supported_str = "Yes";
	}
	else
	{
		supported_str = "No";
	}
	printf("RF Power Commands Supported: %s\n", supported_str);

	if (!supported)
	{
		return 0;
	}

	ret = asphodel_get_rf_power_status_blocking(device, &enabled);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_rf_power_status_blocking()\n", ret);
		return ret;
	}
	printf("  RF Power Enabled: %s\n", enabled ? "Yes" : "No");

	ret = asphodel_get_rf_power_ctrl_vars_blocking(device, rf_ctrl_vars, &rf_ctrl_vars_length);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_rf_power_ctrl_vars_blocking()\n", ret);
		return ret;
	}
	printf("  RF Power Control Variables: [");
	for (i = 0; i < rf_ctrl_vars_length; i++)
	{
		if (i != 0)
		{
			printf(", ");
		}
		printf("%d", rf_ctrl_vars[i]);
	}
	printf("]\n");

	return 0;
}

static int print_radio_info(AsphodelDevice_t *device)
{
	uint8_t radio_ctrl_vars[255];
	uint8_t radio_ctrl_vars_length = 255;
	int connected;
	uint32_t serial_number;
	uint8_t protocol_type;
	int scanning;
	int ret;
	int supported = asphodel_supports_radio_commands(device);
	const char * supported_str;
	int i;

	if (supported)
	{
		supported_str = "Yes";
	}
	else
	{
		supported_str = "No";
	}
	printf("Radio Commands Supported: %s\n", supported_str);

	if (!supported)
	{
		return 0;
	}

	ret = asphodel_get_radio_status_blocking(device, &connected, &serial_number, &protocol_type, &scanning);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_radio_status_blocking()\n", ret);
		return ret;
	}
	printf("  Radio Status: connected=%d, serial_number=%u, protocol_type=0x%02x\n", connected, serial_number, protocol_type);
	printf("  Scanning: %s\n", scanning ? "Yes" : "No");

	ret = asphodel_get_radio_ctrl_vars_blocking(device, radio_ctrl_vars, &radio_ctrl_vars_length);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_radio_ctrl_vars_blocking()\n", ret);
		return ret;
	}
	printf("  Radio Control Variables: [");
	for (i = 0; i < radio_ctrl_vars_length; i++)
	{
		if (i != 0)
		{
			printf(", ");
		}
		printf("%d", radio_ctrl_vars[i]);
	}
	printf("]\n");

	ret = asphodel_get_radio_default_serial_blocking(device, &serial_number);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_radio_default_serial_blocking()\n", ret);
		return ret;
	}
	printf("  default_serial=%u\n", serial_number);

	return 0;
}

static int print_remote_info(AsphodelDevice_t *device)
{
	int connected;
	uint32_t serial_number;
	uint8_t protocol_type;
	int ret;
	int supported = asphodel_supports_remote_commands(device);
	const char * supported_str;

	if (supported)
	{
		supported_str = "Yes";
	}
	else
	{
		supported_str = "No";
	}
	printf("Remote Commands Supported: %s\n", supported_str);

	if (!supported)
	{
		return 0;
	}

	ret = asphodel_get_remote_status_blocking(device, &connected, &serial_number, &protocol_type);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_remote_status_blocking()\n", ret);
		return ret;
	}
	printf("  Remote Status: connected=%d, serial_number=%u, protocol_type=0x%02x\n", connected, serial_number, protocol_type);

	return 0;
}

static int print_bootloader_info(AsphodelDevice_t *device)
{
	uint32_t page_info[255];
	uint8_t page_info_length = 255;
	uint16_t block_sizes[255];
	uint8_t block_sizes_length = 255;
	int ret;
	int supported = asphodel_supports_bootloader_commands(device);
	const char * supported_str;
	int i;

	if (supported)
	{
		supported_str = "Yes";
	}
	else
	{
		supported_str = "No";
	}
	printf("Bootloader Commands Supported: %s\n", supported_str);

	if (!supported)
	{
		return 0;
	}

	ret = asphodel_get_bootloader_page_info_blocking(device, page_info, &page_info_length);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_bootloader_page_info_blocking()\n", ret);
		return ret;
	}
	printf("  Bootloader page info:\n");
	for (i = 0; i < page_info_length / 2; i++)
	{
		printf("    page_count=%u, page_size=%u\n", page_info[2 * i], page_info[2 * i + 1]);
	}

	ret = asphodel_get_bootloader_block_sizes_blocking(device, block_sizes, &block_sizes_length);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_bootloader_block_sizes_blocking()\n", ret);
		return ret;
	}
	printf("  Bootloader block sizes: [");
	for (i = 0; i < block_sizes_length; i++)
	{
		if (i != 0)
		{
			printf(", ");
		}
		printf("%d", block_sizes[i]);
	}
	printf("]\n");

	return 0;
}

static int print_device_info(AsphodelDevice_t *device)
{
	int ret = 0;
	char string_buffer[256];
	uint8_t rev;

	printf("Location String: ");
	print_utf8(device->location_string);
	printf("\n");

	ret = device->get_serial_number(device, string_buffer, sizeof(string_buffer));
	if (ret != 0)
	{
		printf("Error %d in get_serial_number()\n", ret);
		return ret;
	}
	printf("Serial Number: ");
	print_utf8(string_buffer);
	printf("\n");

	printf("Max Incoming Param Len: %d\n", (int)device->get_max_incoming_param_length(device));
	printf("Max Outgoing Param Len: %d\n", (int)device->get_max_outgoing_param_length(device));
	printf("Stream Packet Len: %d\n", (int)device->get_stream_packet_length(device));

	ret = asphodel_get_protocol_version_string_blocking(device, string_buffer, sizeof(string_buffer));
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_protocol_version_string_blocking()\n", ret);
		return ret;
	}
	printf("Protocol Version: ");
	print_utf8(string_buffer);
	printf("\n");

	ret = asphodel_get_board_info_blocking(device, &rev, string_buffer, sizeof(string_buffer));
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_board_info_blocking()\n", ret);
		return ret;
	}
	printf("Board Info: ");
	print_utf8(string_buffer);
	printf(" Rev %d\n", rev);

	ret = asphodel_get_build_info_blocking(device, string_buffer, sizeof(string_buffer));
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_build_info_blocking()\n", ret);
		return ret;
	}
	printf("Build Info: ");
	print_utf8(string_buffer);
	printf("\n");

	ret = asphodel_get_build_date_blocking(device, string_buffer, sizeof(string_buffer));
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_build_date_blocking()\n", ret);
		return ret;
	}
	printf("Build Date: ");
	print_utf8(string_buffer);
	printf("\n");

	ret = asphodel_get_chip_family_blocking(device, string_buffer, sizeof(string_buffer));
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_chip_family_blocking()\n", ret);
		return ret;
	}
	printf("Chip Family: ");
	print_utf8(string_buffer);
	printf("\n");

	ret = asphodel_get_chip_model_blocking(device, string_buffer, sizeof(string_buffer));
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_chip_model_blocking()\n", ret);
		return ret;
	}
	printf("Chip Model: ");
	print_utf8(string_buffer);
	printf("\n");

	ret = asphodel_get_chip_id_blocking(device, string_buffer, sizeof(string_buffer));
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_chip_id_blocking()\n", ret);
		return ret;
	}
	printf("Chip ID: ");
	print_utf8(string_buffer);
	printf("\n");

	ret = asphodel_get_bootloader_info_blocking(device, string_buffer, sizeof(string_buffer));
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_bootloader_info_blocking()\n", ret);
		return ret;
	}
	printf("Bootloader Info: ");
	print_utf8(string_buffer);
	printf("\n");

	ret = print_nvm_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_led_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_stream_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_channel_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_channel_specific_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_decoder_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_supply_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_ctrl_var_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_setting_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_custom_enum_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_setting_category_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_low_level_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_rf_power_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_radio_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_remote_info(device);
	if (ret != 0)
	{
		return ret;
	}

	ret = print_bootloader_info(device);
	if (ret != 0)
	{
		return ret;
	}

	return 0;
}

int print_remote_device_info(AsphodelDevice_t *radio_device, uint32_t serial)
{
	int ret;
	AsphodelDevice_t *remote_device;

	ret = radio_device->get_remote_device(radio_device, &remote_device);
	if (ret != 0)
	{
		printf("Error %d in radio_device->get_remote_device()\n", ret);
		return ret;
	}

	ret = remote_device->open_device(remote_device);
	if (ret != 0)
	{
		printf("Error %d in remote_device->open_device()\n", ret);
		return ret;
	}

	// connect to the device
	ret = asphodel_connect_radio_blocking(radio_device, serial);
	if (ret != 0)
	{
		printf("Error %d in asphodel_connect_radio_blocking()\n", ret);
		goto cleanup;
	}

	// wait for it to connect (1 second timeout)
	ret = remote_device->wait_for_connect(remote_device, 1000);
	if (ret != 0)
	{
		printf("Error %d in remote_device->wait_for_connect()\n", ret);
		goto cleanup;
	}

	ret = print_device_info(remote_device);

cleanup:
	// don't bother checking the return value
	asphodel_stop_radio_blocking(radio_device);

	remote_device->close_device(remote_device);
	remote_device->free_device(remote_device);

	return ret;
}

static int compare_serial_numbers(const void *a, const void *b) // used with qsort
{
	uint32_t *x = (uint32_t*)a;
	uint32_t *y = (uint32_t*)b;

	if (*x > *y)
	{
		return 1;
	}
	else if (*x < *y)
	{
		return -1;
	}
	else
	{
		return 0;
	}
}

int do_radio_scan(AsphodelDevice_t *device, uint32_t **serials, size_t *serials_length)
{
	int ret;

	printf("Scanning for remote devices... ");

	ret = asphodel_start_radio_scan_blocking(device);
	if (ret != 0)
	{
		printf("Error %d in asphodel_start_radio_scan_blocking()\n", ret);
		return ret;
	}

	// wait 2 seconds
	delay_ms(2000);

	ret = asphodel_stop_radio_blocking(device);
	if (ret != 0)
	{
		printf("Error %d in asphodel_stop_radio_blocking()\n", ret);
		return ret;
	}

	ret = asphodel_get_radio_scan_results_blocking(device, serials, serials_length);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_radio_scan_results_blocking()\n", ret);
		return ret;
	}

	// sort the results
	qsort(*serials, *serials_length, sizeof(uint32_t), compare_serial_numbers);

	if (*serials_length == 0)
	{
		printf("None\n");
	}
	else
	{
		size_t i;

		for (i = 0; i < *serials_length; i++)
		{
			if (i != 0)
			{
				printf(", ");
			}

			printf("%u", (*serials)[i]);
		}

		printf("\n");
	}

	return 0;
}

int main(void)
{
	int ret;
	size_t first_pass_usb_devices = 0;
	size_t first_pass_tcp_devices = 0;
	size_t second_pass_usb_devices;
	size_t second_pass_tcp_devices;
	size_t array_size;
	AsphodelDevice_t **device_array;
	size_t i;
	const char *s;
	RemoteDeviceListNode_t *remote_devices = NULL;

	s = asphodel_get_library_protocol_version_string();
	printf("Library Protocol Version: ");
	print_utf8(s);
	printf("\n");

	s = asphodel_get_library_build_info();
	printf("Library Build Info: ");
	print_utf8(s);
	printf("\n");

	s = asphodel_get_library_build_date();
	printf("Library Build Date: ");
	print_utf8(s);
	printf("\n");

	s = asphodel_usb_get_backend_version();
	printf("Library USB Backend Version: ");
	print_utf8(s);
	printf("\n");

	// initialize the library
	ret = asphodel_usb_init();
	if (ret != 0)
	{
		printf("Error %d in asphodel_usb_init()\n", ret);
		return ret;
	}
	ret = asphodel_tcp_init();
	if (ret != 0)
	{
		printf("Error %d in asphodel_tcp_init()\n", ret);
		return ret;
	}

	// get the number of devices available
	ret = asphodel_usb_find_devices(NULL, &first_pass_usb_devices);
	if (ret != 0)
	{
		printf("Error %d in 1st asphodel_usb_find_devices()\n", ret);
		return ret;
	}
	ret = asphodel_tcp_find_devices(NULL, &first_pass_tcp_devices);
	if (ret != 0)
	{
		printf("Error %d in 1st asphodel_tcp_find_devices()\n", ret);
		return ret;
	}

	// early exit if there are no devices
	if (first_pass_usb_devices == 0 && first_pass_tcp_devices == 0)
	{
		printf("No Devices Found!\n");
		return 0;
	}

	// allocate the array
	array_size = first_pass_usb_devices + first_pass_tcp_devices;
	device_array = (AsphodelDevice_t**)malloc(sizeof(AsphodelDevice_t *) * array_size);
	if (device_array == NULL)
	{
		printf("Out of Memory!\n");
		return 1;
	}

	// populate array with usb devices
	second_pass_usb_devices = first_pass_usb_devices;
	if (first_pass_usb_devices != 0)
	{
		ret = asphodel_usb_find_devices(device_array, &second_pass_usb_devices);
		if (ret != 0)
		{
			printf("Error %d in 2nd asphodel_usb_find_devices()\n", ret);
			free(device_array);
			return ret;
		}
	}

	// take the minimum of first and second passes
	array_size = (first_pass_usb_devices < second_pass_usb_devices) ? first_pass_usb_devices : second_pass_usb_devices;

	// populate array with tcp devices
	second_pass_tcp_devices = first_pass_tcp_devices;
	if (first_pass_tcp_devices != 0)
	{
		ret = asphodel_tcp_find_devices(&device_array[array_size], &second_pass_tcp_devices);
		if (ret != 0)
		{
			printf("Error %d in 2nd asphodel_tcp_find_devices()\n", ret);
			free(device_array);
			return ret;
		}
	}

	// take the minimum of array_size and list_size
	array_size += (first_pass_tcp_devices < second_pass_tcp_devices) ? first_pass_tcp_devices : second_pass_tcp_devices;

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

		printf("------------------------------------------------------------\n");

		// open
		ret = device->open_device(device);
		if (ret != 0)
		{
			printf("Error %d in open_device()\n", ret);
			break;
		}

		print_device_info(device);

		if (asphodel_supports_radio_commands(device))
		{
			size_t j;
			uint32_t *serials = NULL;
			size_t serials_length = 0;

			do_radio_scan(device, &serials, &serials_length);

			for (j = 0; j < serials_length; j++)
			{
				RemoteDeviceListNode_t *node;
				int found;

				printf("------------------------------------------------------------\n");

				// see if it's already in the printed devices
				found = 0;
				node = remote_devices;
				while (node != NULL)
				{
					if (node->serial_number == serials[j])
					{
						found = 1;
						break;
					}

					node = node->next;
				}

				if (found)
				{
					printf("Already printed %u through another radio.\n", serials[j]);
					continue;
				}
				else
				{
					// add the device to the beginning of the list
					node = (RemoteDeviceListNode_t*)malloc(sizeof(RemoteDeviceListNode_t));
					if (node == NULL)
					{
						printf("Out of memory\n");
						break;
					}
					node->serial_number = serials[j];
					node->next = remote_devices;
					remote_devices = node;

					print_remote_device_info(device, serials[j]);
				}
			}

			if (serials != NULL)
			{
				asphodel_free_radio_scan_results(serials);
			}
		}

		device->close_device(device);
		device->free_device(device);
	}

	free(device_array);

	// free the list of remote devices
	while (remote_devices != NULL)
	{
		RemoteDeviceListNode_t *next = remote_devices->next;

		free(remote_devices);

		remote_devices = next;
	}

	// close the library
	asphodel_usb_deinit();

	return 0;
}
