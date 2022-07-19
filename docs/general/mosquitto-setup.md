# Setting up a private MQTT server for development

A privately hosted MQTT server is recommend when you test the Virtual MQTT
Scenario, as you can prevent unnecessary traffic to public ones. The following
guide describes a MQTT server installation using Docker.

## Prerequisites

- Working Docker installation

## Setting up the docker container

Before creating the Docker container, replicate the following folder hierarchy:

``` 
mqtt_container
   ├─ config/
   |  └─ mosquitto.conf
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

After you've replicated the folder structure, set the contents of the
docker-compose.yml file to the following:

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

Pull the docker image and start the container with `docker compose up -d`.

After that, you can setup your MQTT user. Your password is hashed and stored in
the `mosquitto_passwords` file. 

1. Open a shell session inside the docker container with the following command:
   ``` sh
   docker exec -it mosquitto sh
   ```
2. Execute the The `-c` argument overwrites any existing password file. If you
   want to add a new user to the password file, run the same command **without**
   the `-c` argument.
   ``` sh
   cd /mosquitto/config
   mosquitto_passwd -c mosquitto_passwords your_mqtt_username
   > Password:
   > Reenter Password:
   exit
   ```
   
After you've set up your mosquitto user, you can add the following line to the
bottom of your `mosquitto.conf` file:

```
password_file mosquitto_passwords
```

Restart your docker container with `docker restart mosquitto`
