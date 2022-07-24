from application import App
import configparser
import sys
from os.path import exists
from os import getcwd
from sample_scenario import init_sample_scenario


def read_config_file(path: str) -> dict:
    parser = configparser.ConfigParser()
    parser.read(path)

    config = {}
    section = "mqtt broker"
    config["host"] = parser.get(section, "host")
    config["port"] = int(parser.get(section, "port"))
    config["keepalive"] = int(parser.get(section, "keepalive"))

    return config


def get_config_dict() -> dict:
    if len(sys.argv) >= 2:  # If env file is passed
        config_name = sys.argv[1]
    else:
        config_name = getcwd() + "/default.ini"
        if not exists(config_name):
            config_name = getcwd() + "/localhost.ini"

    return read_config_file(config_name)


if __name__ == '__main__':

    c = get_config_dict()
    # init_sample_scenario creates a sample scenario with some devices. If you
    # want to create your own virtual smart home scenario, remove/comment out
    # the function and use app.add_device(...).
    app = App(c)
    init_sample_scenario(app, c)
    app.run()
