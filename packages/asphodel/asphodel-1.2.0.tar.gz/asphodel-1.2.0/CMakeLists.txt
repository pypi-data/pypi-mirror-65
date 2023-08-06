cmake_minimum_required(VERSION 3.2)

if(MSVC)
    # download and install libusb
    set(LIBUSB_DOWNLOAD_URL https://s3.us-east-2.amazonaws.com/suprock-public-software/libusb-1.0.22.zip)
    set(LIBUSB_DOWNLOAD_PATH "${CMAKE_CURRENT_BINARY_DIR}/libusb.zip")
    set(LIBUSB_OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/libusb-1.0.22")
    if (NOT EXISTS "${LIBUSB_DOWNLOAD_PATH}")
        message(STATUS "Downloading libusb.zip")
        file(DOWNLOAD "${LIBUSB_DOWNLOAD_URL}" "${LIBUSB_DOWNLOAD_PATH}")
    endif ()
    message(STATUS "Extracting libusb.zip")
    execute_process(COMMAND "${CMAKE_COMMAND}" -E remove_directory "${LIBUSB_OUTPUT_DIR}")
    execute_process(COMMAND "${CMAKE_COMMAND}" -E tar xzf "${LIBUSB_DOWNLOAD_PATH}")
    
    math(EXPR BITS "8*${CMAKE_SIZEOF_VOID_P}")
    if (BITS EQUAL 64)
        message(STATUS "Using 64-bit library from libusb.zip")
        set(PC_LIBUSB_INCLUDEDIR "${LIBUSB_OUTPUT_DIR}/include/libusb-1.0")
        set(PC_LIBUSB_LIBDIR "${LIBUSB_OUTPUT_DIR}/MS64/dll")
    else ()
        message(STATUS "Using 32-bit library from libusb.zip")
        set(PC_LIBUSB_INCLUDEDIR "${LIBUSB_OUTPUT_DIR}/include/libusb-1.0")
        set(PC_LIBUSB_LIBDIR "${LIBUSB_OUTPUT_DIR}/MS32/dll")
    endif ()
endif ()

# force the install location of the libraries to the top level (rather than lib/)
set(INSTALL_LIB_DIR "." CACHE PATH "" FORCE)

# disable examples
set(ASPHODEL_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)

add_subdirectory(lib/asphodel)
