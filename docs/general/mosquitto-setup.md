# Setting up a private MQTT server for development

When you test the virtual MQTT scenario, a privately hosted broker is
recommended to prevent unnecessary traffic to public ones. The following guide
describes a MQTT server installation using Docker.

## Prerequisites

For this guide, you need the following tools:

- Working Docker installation
- Docker-Compose command line application

## Setting up the docker container

Before creating the Docker container, replicate the following folder hierarchy:

``` 
mqtt_container
   ├─ config/
   │  └─ mosquitto.conf
   ├─ data/
   ├─ log/
   └─ docker-compose.yml
```

The set mosquitto configuration to the following:

``` sh
persistence true
persistence_location /mosquitto/data
log_dest file /mosquitto/log/mosquitto.log
log_dest stdout
listener 1883
allow_anonymous true
connection_messages true
```

After you've replicated the directory structure and configured mosquitto, set
the contents of the docker-compose.yml file to the following:

``` yml
version: "3"

services:
  mosquitto:
    container_name: mosquitto
    image: eclipse-mosquitto:2.0.14
    restart: unless-stopped
    ports:
     - "1883:1883"
     - "9001:9001"
    volumes:
     - './config:/mosquitto/config'
     - './data:/mosquitto/data'
     - './log:/mosquitto/log'
```

Finally, you can go into the base directory and execute `docker-compose`

``` sh
cd mqtt_container
docker-compose up -d
```

When you check the docker container with `docker ps -a`, you should see a
container with the name mosquitto running. If it doesn't, check the logs with
`docker logs mosquitto`.
