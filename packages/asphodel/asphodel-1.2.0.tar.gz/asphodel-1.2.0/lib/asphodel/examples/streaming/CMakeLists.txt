set(STREAMING_SOURCES asphodel_streaming.c)
set(STREAMING_HEADERS snprintf.h)

if(MSVC)
	list(APPEND STREAMING_HEADERS inttypes.h)
endif()

add_executable(asphodel_streaming ${STREAMING_SOURCES} ${STREAMING_HEADERS})

target_link_libraries(asphodel_streaming asphodel)

if(MSVC)
	target_compile_definitions(asphodel_streaming PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()

install(TARGETS asphodel_streaming RUNTIME DESTINATION ${INSTALL_BIN_DIR} COMPONENT bin)
