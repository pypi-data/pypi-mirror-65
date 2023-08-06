execute_process(COMMAND "${GIT_EXECUTABLE}" rev-parse --abbrev-ref HEAD
	RESULT_VARIABLE GIT_REV_PARSE_RESULT
	OUTPUT_VARIABLE GIT_BRANCH_STR
	OUTPUT_STRIP_TRAILING_WHITESPACE)

if(GIT_REV_PARSE_RESULT EQUAL 0)
	message(STATUS "Git Branch: ${GIT_BRANCH_STR}")

	execute_process(COMMAND "${GIT_EXECUTABLE}" describe --match InvalidTag --long --always --dirty=-x --abbrev=10
	RESULT_VARIABLE GIT_DESCRIBE_RESULT
	OUTPUT_VARIABLE GIT_DESCRIBE_STR
	OUTPUT_STRIP_TRAILING_WHITESPACE)

	if(GIT_DESCRIBE_RESULT EQUAL 0)
		message(STATUS "Git Hash: ${GIT_DESCRIBE_STR}")

		# check master
		if(GIT_BRANCH_STR STREQUAL "master")
			# master branch

			execute_process(COMMAND "${GIT_EXECUTABLE}" describe --abbrev=0 --tags
				RESULT_VARIABLE GIT_TAG_RESULT
				OUTPUT_VARIABLE GIT_TAG_STR
				OUTPUT_STRIP_TRAILING_WHITESPACE)

			if(GIT_TAG_RESULT EQUAL 0)
				set(BUILD_INFO_STR "${GIT_TAG_STR}-${GIT_DESCRIBE_STR}${VER_SUFFIX}")
			else()
				message(WARNING "Could not generate build info string. Git returned error ${GIT_TAG_STR}.")
				set(BUILD_INFO_STR "<UNKNOWN>")
			endif()
		elseif(GIT_BRANCH_STR MATCHES "^release")
			# release candidate branch
			string(REGEX REPLACE "release[/-]" "" GIT_RELEASE "${GIT_BRANCH_STR}")
			set(BUILD_INFO_STR "${GIT_RELEASE}rc-${GIT_DESCRIBE_STR}${VER_SUFFIX}")
		elseif(GIT_BRANCH_STR STREQUAL "HEAD")
			# detached head; probably in a submodule
			# see if we can find a release tag for this exact commit
			execute_process(COMMAND "${GIT_EXECUTABLE}" describe --exact-match --tags --match [0-9].[0-9]*
				RESULT_VARIABLE GIT_TAG_RESULT
				OUTPUT_VARIABLE GIT_TAG_STR
				OUTPUT_STRIP_TRAILING_WHITESPACE
				ERROR_QUIET)

			if(GIT_TAG_RESULT EQUAL 0)
				# found a version tag, so use that
				set(BUILD_INFO_STR "${GIT_TAG_STR}-${GIT_DESCRIBE_STR}${VER_SUFFIX}")
			else()
				# no tag, assume develop branch
				set(BUILD_INFO_STR "dev-${GIT_DESCRIBE_STR}${VER_SUFFIX}")
			endif()
		else()
			# develop and others
			set(BUILD_INFO_STR "dev-${GIT_DESCRIBE_STR}${VER_SUFFIX}")
		endif()
	else()
		message(WARNING "Could not generate build info string. Git returned error ${GIT_DESCRIBE_STR}.")
		set(BUILD_INFO_STR "<UNKNOWN>")
	endif()
else()
	message(WARNING "Could not generate build info string. Git returned error ${GIT_BRANCH_STR}.")
	set(BUILD_INFO_STR "<UNKNOWN>")
endif()

message(STATUS "Build Info String: ${BUILD_INFO_STR}")

string(TIMESTAMP BUILD_DATE_STR "%Y-%m-%dT%H:%M:%SZ" UTC)
message(STATUS "Build Date String: ${BUILD_DATE_STR}")

configure_file("${VER_HEADER_IN}" "${VER_HEADER_OUT}" @ONLY)
