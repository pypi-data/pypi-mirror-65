set(RECONNECT_MANUAL_SOURCES asphodel_reconnect_manual.c)
set(RECONNECT_MANUAL_HEADERS snprintf.h)

if(MSVC)
	list(APPEND RECONNECT_MANUAL_HEADERS inttypes.h)
endif()

add_executable(asphodel_reconnect_manual ${RECONNECT_MANUAL_SOURCES} ${RECONNECT_MANUAL_HEADERS})

target_link_libraries(asphodel_reconnect_manual asphodel)

if(MSVC)
	target_compile_definitions(asphodel_reconnect_manual PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()

install(TARGETS asphodel_reconnect_manual RUNTIME DESTINATION ${INSTALL_BIN_DIR} COMPONENT bin)
