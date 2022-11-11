ARG CPP_VERSION
FROM faasm/cpp-sysroot:${CPP_VERSION}

SHELL ["/bin/bash", "-c"]
ENV IN_DOCKER="on"

# Install APT dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update

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
    && git submodule update --init -f examples/lammps

# Build the examples and demo functions
RUN cd /code/examples \
    && ./bin/create_venv.sh \
    && source venv/bin/activate \
    && inv \
        ffmpeg \
        lammps \
        lulesh

# Prepare bashrc
WORKDIR /code/examples
RUN echo ". /code/examples/bin/workon.sh" >> ~/.bashrc
CMD ["/bin/bash", "-l"]
