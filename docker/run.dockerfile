ARG EXAMPLES_VERSION
ARG FAASM_VERSION
FROM faasm.azurecr.io/examples-build:${EXAMPLES_VERSION} as build

# Prepare shared data for the tests
RUN cd /code/examples \
    && source venv/bin/activate \
    && inv data

FROM faasm.azurecr.io/cli:${FAASM_VERSION}

COPY --from=build /code/examples /code/examples
COPY --from=build /usr/local/faasm/wasm /usr/local/faasm/wasm
