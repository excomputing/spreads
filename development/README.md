<br>

Notes

<br>

## Remote & Local Environments

### Remote

Development within a container.  The environment's image is built via

```shell
docker build . --file .devcontainer/Dockerfile -t gpu-compute
```

which names the new image `gpu-compute`.  Subsequently, use a container/instance of the image `gpu-compute` as a development environment via the command

> docker run [--rm](https://docs.docker.com/engine/reference/commandline/run/#:~:text=a%20container%20exits-,%2D%2Drm,-Automatically%20remove%20the) --gpus all [-i](https://docs.docker.com/engine/reference/commandline/run/#:~:text=and%20reaps%20processes-,%2D%2Dinteractive,-%2C%20%2Di) [-t](https://docs.docker.com/get-started/02_our_app/#:~:text=Finally%2C%20the-,%2Dt,-flag%20tags%20your) [-p](https://docs.docker.com/engine/reference/commandline/run/#:~:text=%2D%2Dpublish%20%2C-,%2Dp,-Publish%20a%20container%E2%80%99s) 127.0.0.1:10000:8888 -w /app --mount \
> &nbsp; &nbsp; type=bind,src="$(pwd)",target=/app gpu-compute

wherein   `-p 10000:8888` maps the host port `10000` to container port `8888`.  Note, the container's working environment, i.e., -w, must be inline with this project's top directory.  Get the name of the running instance of ``gpu-compute`` via

```shell
docker ps --all
```

A developer may attach an IDE (independent development environment) application to a running container.  In the case of IntelliJ IDEA

> Connect to the Docker [daemon](https://www.jetbrains.com/help/idea/docker.html#connect_to_docker)
> * **Settings** $\rightarrow$ **Build, Execution, Deployment** $\rightarrow$ **Docker** $\rightarrow$ **WSL:** `operating system`
> * **View** $\rightarrow$ **Tool Window** $\rightarrow$ **Services** <br>Within the **Containers** section connect to the running instance of interest, or ascertain connection to the running instance of interest.

Similarly, Visual Studio Code as its container attachment instructions; study [Attach Container](https://code.visualstudio.com/docs/devcontainers/attach-container).

<br>


## Development Notes

The directive

```shell
pylint --generate-rcfile > .pylintrc
```

generates the dotfile `.pylintrc` of the static code analyser [pylint](https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html).  Subsequently, analyse via

```shell
python -m pylint --rcfile .pylintrc ...
```

<br>

## Simple Storage Service

About [list_objects_v2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html)

```python
# ResponseMetadata
pattern = {
    'RequestId': '...', 
    'HostId': '...', 
    'HTTPStatusCode': 200, 
    'HTTPHeaders': {
        'x-amz-id-2': '...', 
        'x-amz-request-id': '...', 
        'date': 'Thu, 15 Feb 2024 21:30:43 GMT', 
        'x-amz-bucket-region': 'eu-west-1', 
        'content-type': 'application/xml', 
        'transfer-encoding': 'chunked', 
        'server': 'AmazonS3'}, 
    'RetryAttempts': 0}
```

<br>

## References

* [Air Pollution by Gary Fuller](https://www.theguardian.com/global/2024/feb/23/eu-countries-could-save-238000-lives-a-year-by-meeting-who-air-pollution-guidelines)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
