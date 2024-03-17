# Base: This is a non-root container image 
FROM nvcr.io/nvidia/rapidsai/base:24.02-cuda12.0-py3.10

# If the steps of a `Dockerfile` use files that are different from the `context` file, COPY the
# file of each step separately; and RUN the file immediately after COPY
WORKDIR /app
COPY /.devcontainer/requirements.txt /app

# pip
RUN pip install --upgrade pip && conda install -n base --file requirements.txt

# Port
EXPOSE 8050

# ENTRYPOINT
ENTRYPOINT ["bash"]