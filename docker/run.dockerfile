ARG EXAMPLES_VERSION
ARG FAASM_VERSION
FROM faasm/examples-build:${EXAMPLES_VERSION} as build

# Prepare shared data for the tests
RUN cd /code/examples \
    && source venv/bin/activate \
    && inv data

FROM faasm/cli:${FAASM_VERSION}

COPY --from=build /usr/local/faasm/wasm /usr/local/faasm/wasm

# Prepare bashrc
SHELL ["/bin/bash", "-c"]
WORKDIR /usr/local/code/faasm
RUN echo ". /usr/local/code/faasm/bin/workon.sh" >> ~/.bashrc
CMD ["/bin/bash", "-l"]
