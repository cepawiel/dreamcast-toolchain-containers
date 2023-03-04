#
# Dockerfile for KallistiOS Toolchain
#

FROM alpine:latest as build-deps
# FROM ghcr.io/jitesoft/alpine as build-deps

# Installing prerequisites
RUN apk --update add --no-cache \
	build-base \
	patch \
	bash \
	texinfo \
	libjpeg-turbo-dev \
	gmp-dev \
	mpfr-dev \
	mpc1-dev \
	libpng-dev \
	curl \
	wget \
	git \
	python3 \
	subversion \
	elfutils-dev \
	&& rm -rf /var/cache/apk/*

FROM build-deps as build-toolchain

ARG BASE_PATH=/opt/toolchains/dc
ARG KOS_PATH=${BASE_PATH}/kos
ARG DCCHAIN_PATH=${KOS_PATH}/utils/dc-chain

# Copy Necessary Data into Container
# By only copying the necessary files to build the toolchain docker
# can cache the toolchain layer as long as none of the files in these directories
# are changed. Doing so would trigger rebuilding the toolchain.
# TODO: More specifically copy includes to avoid rebuilds
COPY KOS/include ${KOS_PATH}/include
COPY KOS/kernel/arch/dreamcast/include/arch ${KOS_PATH}/kernel/arch/dreamcast/include/arch
COPY KOS/kernel/arch/dreamcast/include/dc ${KOS_PATH}/kernel/arch/dreamcast/include/dc
COPY KOS/utils/dc-chain ${DCCHAIN_PATH}

# Build Arg to select either "kos" or "raw" toolchain build
ARG BUILD_TYPE=kos

# name of toolchain config file located in utils/dc-chain
# passed as arg to docker build command
ARG CONFIG_FILE

# Build Sega Dreamcast toolchains
# We copy the specified config to the required config.mk location.
# Also overwrite the default -j2 with the max avalable cores using nproc. 
COPY setup_config.sh ${DCCHAIN_PATH}/setup_config.sh
RUN cd ${DCCHAIN_PATH} \
	&& ls -la \
	&& cp ${CONFIG_FILE} config.mk \
	&& ./setup_config.sh ${BUILD_TYPE} \
	&& echo "Downloading Sources" \
	&& ./download.sh \
	&& echo "Unpacking Sources" \
	&& ./unpack.sh \
	&& echo "Building Toolchain" \
	&& make \
	&& echo "Building GDB" \
	&& make gdb

# Copy Toolchain out of build container into toolchain container.
# This allows the removal of all the remaints of the toolchain build in
# the previous container only keeping the compiled toolchains.
FROM build-deps as toolchain
COPY --from=build-toolchain /opt/toolchains/dc/arm-eabi /opt/toolchains/dc/arm-eabi
COPY --from=build-toolchain /opt/toolchains/dc/sh-elf /opt/toolchains/dc/sh-elf

# build kos and related tools
# TODO: Could probably use a slimmer base image
#		but we need some host build tools for kos anyway
FROM toolchain as kos

# copy entire KOS folder into container
# TODO: copy only folders necessary for build. 
#		Example: Changes to doc/ will trigger a rebuild which might be unwanted
COPY KOS /opt/toolchains/dc/kos

# setup environ.sh file using default
RUN cd /opt/toolchains/dc/kos \
	&& ls -la \
	&& cp doc/environ.sh.sample environ.sh \
	# create link so environ.sh is sourced for interactive shells
	# example: docker run --rm -it $TAG /bin/bash
	&& ln -s /opt/toolchains/dc/kos/environ.sh /etc/profile.d/kos.sh

# pristine (default) is for dreamcast
# naomi can be specified as a build_arg
# overwriting this at runtime could cause issues
# so avoid doing so
# TODO: Give a warning if runtime arg != build arg
ARG KOS_SUBARCH="pristine"
ENV KOS_SUBARCH=${KOS_SUBARCH}

# set BASH_ENV so it works for non interactive as well
# example: docker run --rm $TAG "make"
ENV BASH_ENV="/opt/toolchains/dc/kos/environ.sh"

# Set Shell to Bash so environ.sh will be sourced in every
# following run command
SHELL ["/bin/bash", "-c"]

# set entry point to bash so arg to docker run can be 
# run as a command.
ENTRYPOINT ["/bin/bash", "-c"]

# if run with no parameters just start bash
CMD ["bash"]

# build KOS
RUN cd /opt/toolchains/dc/kos && make

# TODO: Build KOS Debug Lib

FROM kos as kos-ports

COPY PORTS /opt/toolchains/dc/kos-ports
RUN cd /opt/toolchains/dc/kos-ports \
	&& sh utils/build-all.sh
