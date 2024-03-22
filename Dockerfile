# Base: This is a non-root container image 
FROM nvcr.io/nvidia/rapidsai/base:24.02-cuda12.0-py3.10

# If the steps of a `Dockerfile` use files that are different from the `context` file, COPY the
# file of each step separately; and RUN the file immediately after COPY
WORKDIR /app
COPY .devcontainer/requirements.txt /app

# pip
RUN pip install --upgrade pip && conda install -n base --file requirements.txt && mkdir /app/warehouse

# Specific COPY
COPY src /app/src
COPY resources /app/resources
COPY config.py /app/config.py

# Port
EXPOSE 8050

# Create mount point
VOLUME [ "/app/warehouse" ]

# ENTRYPOINT
ENTRYPOINT ["python"]

# CMD
CMD ["src/main.py"]