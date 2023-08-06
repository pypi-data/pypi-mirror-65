# Asphodel Library

## About
The Asphodel Library supports communication with USB and TCP devices communicating through the Asphodel communication protocol.

The Asphodel communication protocol was developed by Suprock Technologies (http://www.suprocktech.com)

## License
The Apshodel Library is licensed under the ISC license.

The ISC license is a streamlined version of the BSD license, and permits usage in both open source and propretary projects.

## Dependencies
### libusb-1.0
libusb-1.0: http://libusb.info/ 

libusb-1.0 is the only runtime dependency.

Asphodel has been tested with libusb-1.0 version 1.0.20.

### CMake
CMake: http://www.cmake.org/

CMake 3.1 is the minimum supported version for Linux/Unix.
CMake 3.3 or later should be used on Windows, as there are bugs with the 64-bit Visual Studio generators on earlier versions.

The following examples assume that CMake has been added to the PATH.

### Git (Optional)
Git: http://www.git-scm.com/

If git is used to download the Asphodel Library source code, then the git version information will be built into the library, which can aid in debugging.

If git is not available at build time then this version information will be omitted.

## Building From Source (Linux)
To get started, CMake must be run from a build directory. For example, inside the asphodel source directory:

    $ mkdir build
    $ cd build
    $ cmake -DCMAKE_BUILD_TYPE=Release ..

Other build types that CMake supports are Debug, RelWithDebInfo and MinSizeRel. Each of these build types will apply different compiler flags.

After CMake has been run to setup the build directory, the library and example programs can be compiled:

    $ make

NOTE: the unpack shared library can take a long time to build, especially on virtual machines. A parallel build (passing -j4 or -j8 to make) can help to speed up the build process.

When debugging it is sometimes helpful to see the full compiler calls. This can be accomplished by running make in verbose mode:

    $ make VERBOSE=1

Once the library and example programs have been built, they can be installed with:

    $ sudo make install

Which will install files into /usr/local. This prefix can be changed by passing -DCMAKE_INSTALL_PREFIX=/path/to/install to cmake.

## Using Other Compilers (Linux)
Other compilers can be used with CMake by setting the CC flag while calling CMake. For example, to configure the build to use Clang:

    $ mkdir build_clang
    $ cd build_clang
    $ CC=/usr/bin/clang cmake -DCMAKE_BUILD_TYPE=Release ..

## Building From Source (Windows)
CMake supports generating Visual Studio projects directly. 

CMake can only generate visual studio solutions for one architecture at a time. The preferred solution is to create two seperate build directories; one for x86 and one for x86_64. From a command line in the asphodel source folder:

    $ mkdir build32
    $ cd build32
    $ cmake -G"Visual Studio 14 2015" ..

    $ mkdir build64
    $ cd build64
    $ cmake -G"Visual Studio 14 2015 Win64" ..

The Visual Studio .sln files are then contained in the build32 and build64 folders. The solution files contain configurations for Release, Debug, etc.

For other versions of Visual Studio, see CMake's complete list of generators:

    $ cmake --help

### Finding Libusb (Windows)
If CMake cannot find libusb, then the path can be specified manually using the CMake settings PC_LIBUSB_INCLUDEDIR (for the path to libusb.h) and PC_LIBUSB_LIBDIR (for the path to libusb-1.0.lib).

    $ cmake -G"Visual Studio 14 2015" -DPC_LIBUSB_INCLUDEDIR=C:\path\to\libusb\include -DPC_LIBUSB_LIBDIR=C:\path\to\libusb\lib ..

## Building as a Static Library
Asphodel can be built as a static library by setting the STATIC_LIB option in cmake. For example:

    $ cmake -DSTATIC_LIB=ON ..

## Asphodel Devices and udev
By default on most Linux distributions, USB devices require root priveledges to access. The included udev rule file "asphodel-usb.rules" can be placed in /etc/udev/rules.d/ (or similar) to allow unpriveledged access to any Asphodel USB devices.

udev may need to be restarted after adding the rule file, and additionally any attached Asphodel compatible devices should be unplugged and then reattached.
