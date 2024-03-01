ARG CPP_VERSION
ARG EXAMPLES_VERSION
FROM faasm.azurecr.io/examples-base:${EXAMPLES_VERSION} as base
FROM faasm.azurecr.io/cpp-sysroot:${CPP_VERSION}

SHELL ["/bin/bash", "-c"]
ENV IN_DOCKER="on"

# Copy built OpenMPI from previous step
COPY --from=base /tmp/openmpi-4.1.0/ /tmp/openmpi-4.1.0/

# Install OpenMPI
RUN cd /tmp/openmpi-4.1.0 \
    && make install \
    && cd /tmp \
    && rm -rf /tmp/openmpi-4.1.0 /tmp/openmpi-4.1.0.tar.bz2

# Install OpenMP
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update \
    && apt install -y libomp-17-dev

# Fetch the code and update submodules
ARG EXAMPLES_VERSION
RUN mkdir -p code \
    && git clone -b v${EXAMPLES_VERSION} \
        https://github.com/faasm/examples \
        /code/examples \
    && cd /code/examples \
    && git submodule update --init -f cpp \
    && git submodule update --init -f python \
    # Fetch all the example submodules
    && git submodule update --init -f examples/FFmpeg \
    && git submodule update --init -f examples/ImageMagick \
    && git submodule update --init -f examples/Kernels \
    && git submodule update --init -f examples/lammps \
    && git submodule update --init -f examples/lammps-migration \
    && git submodule update --init -f examples/LULESH \
    && git submodule update --init -f examples/libpng \
    && git submodule update --init -f examples/polybench \
    && git submodule update --init -f examples/tensorflow

# Build the examples and demo functions
RUN cd /code/examples \
    && ./bin/create_venv.sh
    && source venv/bin/activate \
    # Build the native versions of the examples that support it
    && inv \
        kernels --native \
        lammps --native \
        lammps --migration --native \
        lammps --migration-net --native \
        lulesh --native \
        polybench --native \
    && inv \
        ffmpeg \
        # ImageMagick needs libpng
        libpng imagemagick \
        kernels \
        lammps \
        lammps --migration \
        lammps --migration-net \
        lulesh \
        polybench \
        tensorflow \
    # These demo functions link with the cross-compiled static libraries
    && inv \
        func ffmpeg check \
        func lammps chain \
        func mpi migrate \
        func tf check

# Prepare bashrc
WORKDIR /code/examples
RUN echo ". /code/examples/bin/workon.sh" >> ~/.bashrc
CMD ["/bin/bash", "-l"]
