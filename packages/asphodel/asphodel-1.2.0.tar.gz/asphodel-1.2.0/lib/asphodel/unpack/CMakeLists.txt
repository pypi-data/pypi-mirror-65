set(UNPACK_SOURCES src/unpack.c src/unpack_id.c src/unwrap.c)
set(UNPACK_INTERNAL_HEADERS src/unpack_all_sizes.h src/unpack_id.h src/unwrap.h)
set(UNPACK_EXTERNAL_HEADERS inc/unpack.h)

foreach(index RANGE 0 32)
	list(APPEND UNPACK_SOURCES "src/unpack${index}.c")
	list(APPEND UNPACK_INTERNAL_HEADERS "src/unpack${index}.h")
endforeach(index)

if (STATIC_LIB)
	add_library(unpack STATIC ${UNPACK_SOURCES} ${UNPACK_INTERNAL_HEADERS} ${UNPACK_EXTERNAL_HEADERS})
	add_definitions(-DUNPACK_STATIC_LIB)
else ()
	add_library(unpack SHARED ${UNPACK_SOURCES} ${UNPACK_INTERNAL_HEADERS} ${UNPACK_EXTERNAL_HEADERS})
endif ()

target_include_directories(unpack PUBLIC "inc")
target_include_directories(unpack PRIVATE "src")

set_target_properties(unpack PROPERTIES PUBLIC_HEADER "${UNPACK_EXTERNAL_HEADERS}")
set_target_properties(unpack PROPERTIES DEFINE_SYMBOL "UNPACK_API_EXPORTS")

# unpack should be built with high optimizations even in debug
if((${CMAKE_C_COMPILER_ID} MATCHES GNU) OR (${CMAKE_C_COMPILER_ID} MATCHES Clang))
	set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -O3")
endif()
if(MSVC)
	# remove the /RTC1 as it's incompatible with /O2, and can't be unset
	STRING (REGEX REPLACE "/RTC(su|[1su])" "" CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG}")
    set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} /O2 /Ob2")
endif()

# the DLLs get a special name on windows depending on 32/64 bit
if(MSVC)
	math(EXPR BITS "8*${CMAKE_SIZEOF_VOID_P}")
	set_target_properties(unpack PROPERTIES OUTPUT_NAME Unpack${BITS})
endif()

install(TARGETS unpack
	RUNTIME DESTINATION ${INSTALL_BIN_DIR} COMPONENT bin
	LIBRARY DESTINATION ${INSTALL_LIB_DIR} COMPONENT lib
	ARCHIVE DESTINATION ${INSTALL_LIB_DIR} COMPONENT lib
	PUBLIC_HEADER DESTINATION ${INSTALL_INCLUDE_DIR} COMPONENT include)
