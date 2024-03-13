FROM ubuntu:22.04 as base

RUN apt update \
    && apt install -y \
        bzip2 \
        gcc \
        g++ \
        make \
        wget

# Download and build MPI
ARG OPENMPI_VERSION
ARG OPENMPI_VERSION_NOPATCH
RUN mkdir -p /tmp \
    && cd /tmp \
    && wget https://download.open-mpi.org/release/open-mpi/v${OPENMPI_VERSION_NOPATCH}/openmpi-${OPENMPI_VERSION}.tar.bz2 \
    && tar xf openmpi-${OPENMPI_VERSION}.tar.bz2 \
    && cd /tmp/openmpi-${OPENMPI_VERSION} \
    && ./configure --prefix=/usr/local \
    && make -j `nproc`
