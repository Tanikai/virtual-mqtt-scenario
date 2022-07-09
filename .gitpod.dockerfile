FROM gitpod/workspace-full-vnc

USER gitpod

RUN apt-get -q update && apt-get install -yq \
        tk-dev \
        python3-tk \
        python-tk \
        && sudo rm -rf /var/lib/apt/lists/*
