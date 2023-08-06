# Overview

The Asphodel library supports devices that conform to the Asphodel protocol. The Asphodel protocol is used to provide a high degree of self-description for sensors and related devices.

The host can inquire about the presence and properties of the following attributes:

* RGB LEDs
* Single Color LEDs
* Streams
* Channels
* Supplies
* Control Variables

Additionally, more specialized devices can declare that they support an extended set of commands. Currently supported extensions are:

* RF Power Commands
* Radio Commands (for discovering and communicating with wireless devices)

# Device Attributes

## LEDs (RGB and Single Color)

Any LEDs on the device can have their value set and read back.

## Streams and Channels

Streams and channels are tightly coupled concepts. A stream represents a data packet that is transmitted periodically by the device. Streams can be enabled and disabled. A stream has at least one channel. 

A channel represents a set of measurements taken on the device, corresponding to a group of bits in the stream's packet. Channels can provide multiple samples (taken in time) in one packet, to provide better throughput for a fast sensor.

Some channels define multiple subchannels. All subchannel data shares the same output unit (i.e. they can be graphed together in a single plot). An example of subchannels is a 3-axis accelerometer, which provides data in X, Y and Z axes.

NOTE: while all streams require a channel, it is possible for a device to declare a channel without a stream. No data can be read from this channel (as only streams carry data).

## Supplies

The power supplies on the device can be measured to verify correct operation.

## Control Variables

Some devices need extra information from the host before they can operate properly. An example of a control variable is a Radio device which needs to have a channel selected before it can operate.

# Library Concepts

## Device Decoders

A device decoder can be created for a device. The device decoder will contain stream decoders, which will in turn contain channel decoders. Callbacks can be set on channel decoders, and then when a packet is passed to the device decoder, the callback will be called on the appropriate channel, with the packet data transformed into a `double` array.

In this way, a program using the Asphodel library is completely insulated from the low-level bit manipulations required to decode an arbitrary stream packet into usable channel values.

## Unit Formatters

Unit formatters encapsulate all of the functionality to take a value with a given unit type and display it to a user in the appropriate way. 

The formatter takes into account metric vs. non-metric. It will use metric prefixes where applicable (e.g. mV for millivolts).

The formatter also displays the correct number of digits after the decimal point, for the given data resolution.

Unit formatters have 4 output modes: bare, ascii, unicode and html. The bare output simply outputs the formatted number, with no unit string. The ascii output provides a string using only ASCII characters. The unicode output provides a string encoded with UTF-8 using the most appropriate symbols. The html output provides a string using only ASCII characters, but with special symbols escaped using HTML escape codes.

For example, a reading of 25.000 with a unit type of Celsius and a resolution of 0.1 would be rendered as the following ways:

* bare: `"25.0"`
* ascii: `"25.0 deg C"`
* unicode: `"25.0 °C"` (with escape codes this is rendered `"25.0 \xc2\xb0C"`)
* html: `"25.0 &\#176;C"`

