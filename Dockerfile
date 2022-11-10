ARG CPP_VERSION
FROM faasm/cpp-sysroot:${CPP_VERSION}

SHELL ["/bin/bash", "-c"]
ENV IN_DOCKER="on"

# Install APT dependencies
RUN apt update \
    && apt upgrade -y

# Fetch the code and update submodules
ARG EXAMPLES_VERSION
RUN mkdir -p code \
    && git clone -b v${EXAMPLES_VERSION} \
        https://github.com/faasm/examples \
        /code/examples \
    && cd /code/examples \
    && git submodule update --init -f examples/LAMMPS

# Build the examples and demo functions
RUN cd /code/examples \
    && ./bin/create_venv.sh \
    && source venv/bin/activate \
    && inv lammps
