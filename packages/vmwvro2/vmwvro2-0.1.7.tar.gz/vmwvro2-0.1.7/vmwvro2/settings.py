"""
Manage configuration and credentials file
"""

import logging
import os
import yaml

logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)


def init():
    global demo
    demo = False


def loadConfig():

    global config

    configPath = ".secrets/vro.yml"

    #Read config/credentials files
    dirname = os.path.expanduser("~")
    configFile = os.path.join(dirname, configPath)
    logger.info("Credential File: " + configPath)
    with open(configFile, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            logger.error(exc)

    logger.debug("Config/Credentials " + str(config))


def loadNet():
    global config

    configPath = ".secrets/vro.yml"

    #Read config/credentials files
    dirname = os.path.expanduser("~")
    configFile = os.path.join(dirname, configPath)
    configFile = "./sample-config/vro.yml"
    logger.info("Credential File: " + configPath)
    with open(configFile, 'r') as stream:
        try:
            netInput = yaml.load(stream)
        except yaml.YAMLError as exc:
            logger.error(exc)

    logger.debug("Config/Credentials " + str(config))

    sessionList = []

    for item in netInput:

        if item == "default":
            continue

        print(item)
        print(netInput[item]['url'])
        



class dummy:

    def __init__(self):
        demo = 0