# require CMake version >= 3.2
cmake_minimum_required(VERSION 3.2)

if(NOT CMAKE_BUILD_TYPE)
	set(CMAKE_BUILD_TYPE Release)
endif()

project(Asphodel C)

option(STATIC_LIB "STATIC_LIB" OFF)
option(ASPHODEL_USB_DEVICE "ASPHODEL_USB_DEVICE" ON)
option(ASPHODEL_TCP_DEVICE "ASPHODEL_TCP_DEVICE" ON)
option(ASPHODEL_MEM_TEST "ASPHODEL_MEM_TEST" OFF)
option(ASPHODEL_BUILD_EXAMPLES "ASPHODEL_BUILD_EXAMPLES" ON)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules/")

# Offer the user the choice of overriding the installation directories
if(NOT MSVC)
	set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
	set(INSTALL_BIN_DIR bin CACHE PATH "Installation directory for executables")
	set(INSTALL_INCLUDE_DIR include/asphodel CACHE PATH "Installation directory for header files")
else()
	set(INSTALL_LIB_DIR "." CACHE PATH "Installation directory for libraries")
	set(INSTALL_BIN_DIR "." CACHE PATH "Installation directory for executables")
	set(INSTALL_INCLUDE_DIR "include" CACHE PATH "Installation directory for header files")
endif()

if((${CMAKE_C_COMPILER_ID} MATCHES GNU) OR (${CMAKE_C_COMPILER_ID} MATCHES Clang))
	set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra")
endif()

if(MSVC)
	set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /W3")
	add_definitions(-D_UNICODE -DUNICODE)
endif()

IF(UNIX)
	SET(MATH_LIB m)
ELSE(UNIX)
	SET(MATH_LIB)
ENDIF(UNIX)

# check if building with memory test support
if (ASPHODEL_MEM_TEST)
	add_definitions(-DASPHODEL_MEM_TEST)
endif ()

# Add unpack library
add_subdirectory(unpack)

set(VER_HEADER_IN "${CMAKE_CURRENT_SOURCE_DIR}/src/version_autogen.h.in")
set(VER_HEADER_OUT "${CMAKE_CURRENT_BINARY_DIR}/version_autogen.h")

set(ASPHODEL_SOURCES src/asphodel_api.c src/asphodel_decode.c src/asphodel_device.c src/asphodel_device_type.c
	src/asphodel_mem_test.c src/asphodel_unit_format.c src/asphodel_usb.c src/asphodel_tcp.c src/asphodel_version.c
	${VER_HEADER_OUT} src/clock.c)
set(ASPHODEL_INTERNAL_HEADERS src/clock.h src/mutex.h src/serialize.h src/snprintf.h)
set(ASPHODEL_EXTERNAL_HEADERS inc/asphodel.h inc/asphodel_api.h inc/asphodel_bootloader.h
	inc/asphodel_channel_specific.h inc/asphodel_ctrl_var.h inc/asphodel_decode.h inc/asphodel_device.h
	inc/asphodel_device_type.h inc/asphodel_low_level.h inc/asphodel_mem_test.h inc/asphodel_protocol.h
	inc/asphodel_radio.h inc/asphodel_rf_power.h inc/asphodel_setting.h inc/asphodel_stream.h inc/asphodel_supply.h
	inc/asphodel_unit_format.h inc/asphodel_usb.h inc/asphodel_tcp.h inc/asphodel_version.h)

if (STATIC_LIB)
	add_library(asphodel STATIC ${ASPHODEL_SOURCES} ${ASPHODEL_INTERNAL_HEADERS} ${ASPHODEL_EXTERNAL_HEADERS})
	add_definitions(-DUNPACK_STATIC_LIB -DASPHODEL_STATIC_LIB)
else ()
	add_library(asphodel SHARED ${ASPHODEL_SOURCES} ${ASPHODEL_INTERNAL_HEADERS} ${ASPHODEL_EXTERNAL_HEADERS})
endif ()

# check if building with USB support
if (ASPHODEL_USB_DEVICE)
	# find libusb
	find_package(LibUSB REQUIRED)

	# add compiler definition
	add_definitions(-DASPHODEL_USB_DEVICE)

	# add libusb-1.0.dll to the install directory (if it exists)
	if (WIN32)
		string(REGEX REPLACE "\.lib$" ".dll" LIBUSB_DLL ${LIBUSB_LIBRARIES})
		if (EXISTS ${LIBUSB_DLL})
			install(FILES ${LIBUSB_DLL} DESTINATION ${INSTALL_LIB_DIR} COMPONENT lib)
		endif ()
	endif ()
else ()
	# make empty variables for the libusb libs and include directories
	SET(LIBUSB_LIBRARIES)
	SET(LIBUSB_INCLUDE_DIR)
endif ()

# check if building with TCP support
if (ASPHODEL_TCP_DEVICE)
	if (WIN32)
		# add winsock on windows systems
		target_link_libraries(asphodel ws2_32 iphlpapi)
	endif ()

	# add compiler definition
	add_definitions(-DASPHODEL_TCP_DEVICE)
endif ()

target_link_libraries(asphodel ${LIBUSB_LIBRARIES} unpack ${MATH_LIB})
# use relative path to the binary directory so it doesn't get mistaken for a system directory
file(RELATIVE_PATH BINARY_REL_DIR ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/.)
target_include_directories(asphodel PRIVATE ${LIBUSB_INCLUDE_DIR} ${BINARY_REL_DIR})
target_include_directories(asphodel PUBLIC "inc")
target_include_directories(asphodel PRIVATE "src")
set_target_properties(asphodel PROPERTIES PUBLIC_HEADER "${ASPHODEL_EXTERNAL_HEADERS}")
set_target_properties(asphodel PROPERTIES DEFINE_SYMBOL "ASPHODEL_API_EXPORTS")

# add pthread library to non-windows systems
if(NOT WIN32)
	set(CMAKE_THREAD_PREFER_PTHREAD TRUE)
	set(THREADS_PREFER_PTHREAD_FLAG TRUE)
	find_package(Threads REQUIRED)
	target_link_libraries(asphodel Threads::Threads)
endif()

# the DLLs get a special name on windows depending on 32/64 bit
if(WIN32)
	math(EXPR BITS "8*${CMAKE_SIZEOF_VOID_P}")
	set_target_properties(asphodel PROPERTIES OUTPUT_NAME Asphodel${BITS})
endif()

# include the example directories
if (ASPHODEL_BUILD_EXAMPLES)
	add_subdirectory(examples)
endif ()

# create version_autogen.h
find_package(Git QUIET)
if(NOT GIT_FOUND)
	message(WARNING "Could not generate build info string. Could not find git.")
	set(BUILD_INFO_STR "<UNKNOWN>")
	message(STATUS "Build Info String: ${BUILD_INFO_STR}")
	string(TIMESTAMP BUILD_DATE_STR "%Y-%m-%dT%H:%M:%SZ" UTC)
	message(STATUS "Build Date String: ${BUILD_DATE_STR}")
	configure_file("${VER_HEADER_IN}" "${VER_HEADER_OUT}" @ONLY)
else()
	add_custom_target(githeader COMMAND ${CMAKE_COMMAND}
		-DGIT_EXECUTABLE=${GIT_EXECUTABLE}
		-DVER_HEADER_IN=${VER_HEADER_IN}
		-DVER_HEADER_OUT=${VER_HEADER_OUT}
		-DVER_SUFFIX=${VER_SUFFIX}
		-P ${CMAKE_CURRENT_SOURCE_DIR}/GitHeader.cmake
		WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
		BYPRODUCTS ${VER_HEADER_OUT})
	add_dependencies(asphodel githeader)
endif()
set_source_files_properties(${VER_HEADER_OUT} PROPERTIES GENERATED TRUE HEADER_FILE_ONLY TRUE)

install(TARGETS asphodel
	RUNTIME DESTINATION ${INSTALL_BIN_DIR} COMPONENT bin
	LIBRARY DESTINATION ${INSTALL_LIB_DIR} COMPONENT lib
	ARCHIVE DESTINATION ${INSTALL_LIB_DIR} COMPONENT lib
	PUBLIC_HEADER DESTINATION ${INSTALL_INCLUDE_DIR} COMPONENT include)

if (MSVC AND NOT STATIC_LIB)
	install(FILES $<TARGET_PDB_FILE:asphodel> DESTINATION ${INSTALL_LIB_DIR} CONFIGURATIONS Debug RelWithDebInfo COMPONENT lib)
endif()