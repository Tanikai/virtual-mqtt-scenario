#FROM gitpod/workspace-full-vnc

#USER gitpod

#RUN apt-get -q update && apt-get install -yq \
#        tk-dev \
#        python3-tk \
#        python-tk \
#        && sudo rm -rf /var/lib/apt/lists/*

FROM gitpod/workspace-full-vnc

USER root

RUN sudo apt-get update \
    && sudo apt-get install -y libgtk-3-dev \
    && sudo apt-get clean \
    && sudo rm -rf /var/cache/apt/* \
    && sudo rm -rf /var/lib/apt/lists/* \
    && sudo rm -rf /tmp/*