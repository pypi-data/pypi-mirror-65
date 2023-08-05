import maya

from logger import logging


def publish(info):
    m = maya.now().local_datetime()
    print("")
    print(m)
    print("Now playing:", info["now"])


def register():
    logging.info("[stdout] writer registered.")
    return publish
