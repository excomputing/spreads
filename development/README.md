<br>

Notes

<br>

## Remote Development Environment

The environment's image is built via

```shell
docker build . --file .devcontainer/Dockerfile -t gpu-compute
```

which names the new image `gpu-compute`.  Subsequently, use a container/instance of the image `gpu-compute` as a development environment via the command

```shell
docker run --rm --gpus all -i -t -p 127.0.0.1:10000:8050 -w /app --mount 
  type=bind,src="$(pwd)",target=/app gpu-compute
```

or

```shell
docker run --rm --gpus all -i -t -p 127.0.0.1:10000:8050 -w /app --mount 
  type=bind,src="$(pwd)",target=/app -v ~/.aws:/home/rapids/.aws gpu-compute
```

For an explanatory note of a `docker run` option visit [docker](https://docs.docker.com/reference/cli/docker/container/run/).  Examples:

* [--rm](https://docs.docker.com/engine/reference/commandline/run/#:~:text=a%20container%20exits-,%2D%2Drm,-Automatically%20remove%20the)
* [-i](https://docs.docker.com/engine/reference/commandline/run/#:~:text=and%20reaps%20processes-,%2D%2Dinteractive,-%2C%20%2Di)
* [-t](https://docs.docker.com/get-started/02_our_app/#:~:text=Finally%2C%20the-,%2Dt,-flag%20tags%20your)
* [-p](https://docs.docker.com/engine/reference/commandline/run/#:~:text=%2D%2Dpublish%20%2C-,%2Dp,-Publish%20a%20container%E2%80%99s)

Herein, `-p 10000:8050` maps the host port `10000` to container port `8050`.  Note, the container's working environment, i.e., `-w`, must be inline with this project's top directory.  The second `docker run` option is important for interactions with Amazon Web Services.  Get the name of the running instance of ``gpu-compute`` via

```shell
docker ps --all
```

A developer may attach an IDE (integrated development environment) application to a running container.  In the case of IntelliJ IDEA

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

## References

* [RAPIDS Base](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/rapidsai/containers/base)
* [Development Containers](https://containers.dev)
  * [Development Containers & Dockerfile](https://containers.dev/guide/dockerfile)
  * [Development Containers & Features](https://containers.dev/features)
* [GitHub Actions](https://docs.github.com/en/actions)
    * [build & test](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration): [Java + Maven](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-java-with-maven), [Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
    * [syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
    * [contexts](https://docs.github.com/en/actions/learn-github-actions/contexts)
    * [variables](https://docs.github.com/en/actions/learn-github-actions/variables)
* [pip & requirements](https://pip.pypa.io/en/stable/reference/requirements-file-format/)
* [Air Pollution by Gary Fuller](https://www.theguardian.com/global/2024/feb/23/eu-countries-could-save-238000-lives-a-year-by-meeting-who-air-pollution-guidelines)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
