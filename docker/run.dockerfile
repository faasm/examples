ARG EXAMPLES_VERSION
ARG FAASM_VERSION
ARG SGX_IMAGE_SUFFIX
FROM faasm/examples-build:${EXAMPLES_VERSION} as build

# Prepare shared data for the tests
RUN cd /code/examples \
    && source venv/bin/activate \
    && inv data

FROM faasm/cli${SGX_IMAGE_SUFFIX}:${FAASM_VERSION}

COPY --from=build /code/examples /code/examples
COPY --from=build /usr/local/faasm/wasm /usr/local/faasm/wasm
