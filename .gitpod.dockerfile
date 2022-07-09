#FROM gitpod/workspace-full-vnc

#USER gitpod

#RUN apt-get -q update && apt-get install -yq \
#        tk-dev \
#        python3-tk \
#        python-tk \
#        && sudo rm -rf /var/lib/apt/lists/*

FROM gitpod/workspace-full-vnc

USER root

RUN sudo apt-get update
RUN sudo apt-get install -y libgtk-3-dev 
RUN sudo apt-get clean 
RUN sudo rm -rf /var/cache/apt/* 
RUN sudo rm -rf /var/lib/apt/lists/* 
RUN sudo rm -rf /tmp/*
