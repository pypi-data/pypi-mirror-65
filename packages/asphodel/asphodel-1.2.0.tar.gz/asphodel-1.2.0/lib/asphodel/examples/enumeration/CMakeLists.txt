set(ENUMERATION_SOURCES asphodel_enumeration.c)
set(ENUMERATION_HEADERS serialize.h)

add_executable(asphodel_enumeration ${ENUMERATION_SOURCES} ${ENUMERATION_HEADERS})

target_link_libraries(asphodel_enumeration asphodel)

install(TARGETS asphodel_enumeration RUNTIME DESTINATION ${INSTALL_BIN_DIR} COMPONENT bin)
