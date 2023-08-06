"""
Manage configuration and credentials file
"""

import logging
import os
import yaml

from vmwvro2.config import VRO_CONFIG_FILE, VRO_CREDENTIALS_FILE



logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)



class ConfigVMWvro:

    config = None
    credentials = None

    @classmethod
    def __init__(cls, path=None):
        cls.load(path)    

    @classmethod
    def load(cls, path=None):

        if cls.config:
            return 

        #Read config/credentials files
        #path = ".secrets/vro-credentials.yml"
        #dirname = os.path.expanduser("~")
        #configFile = os.path.join(dirname, path)
        #configFile = "/etc/vmwvro2/vro-credentials.yml"
        configFile = VRO_CREDENTIALS_FILE

        logger.debug("Reading credentias from %s",configFile)
        with open(configFile, 'r') as stream:
            try:
                cls.credentials = yaml.load(stream, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                logger.error(exe)


        #Read the node list
        configFile = VRO_CONFIG_FILE
        logger.debug("Reading config from %s",configFile)

        with open(configFile, 'r') as stream:
            try:
                cls.config = yaml.load(stream, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                logger.error(exe)

