# Base: This is a non-root container image 
FROM nvcr.io/nvidia/rapidsai/base:24.12-cuda12.0-py3.12

# If the steps of a `Dockerfile` use files that are different from the `context` file, COPY the
# file of each step separately; and RUN the file immediately after COPY
WORKDIR /app
COPY .devcontainer/requirements.txt /app

# pip
RUN pip install --upgrade pip && \
    pip install --requirement /app/requirements.txt --no-cache-dir && mkdir /app/warehouse

# Specific COPY
COPY src /app/src
COPY config.py /app/config.py

# Port
EXPOSE 8050

# Create mount point
VOLUME [ "/app/warehouse" ]

# ENTRYPOINT
ENTRYPOINT ["python"]

# CMD
CMD ["src/main.py"]
