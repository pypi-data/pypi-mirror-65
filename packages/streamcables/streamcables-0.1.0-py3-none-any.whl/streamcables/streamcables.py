#!/usr/bin/env python3.6
import importlib
import time

import arg
import logger
import settings


def main():
    settings.init()
    args = arg.parse()
    logger.init(args.loglevel)

    print("StreamCables 0.1")

    config = settings.config

    reader_name = config["main"]["reader"]
    writer_names = config["main"]["writers"]
    refresh_rate = config["main"]["refresh-rate"]

    rs = [reader_name + ".register"]
    reader = plugins(rs)[0]

    ws = []
    for name in writer_names:
        ws.append(name + ".register")
    writers = plugins(ws)

    logger.logging.info("-------START----------")
    last_hash = ""
    try:
        while True:
            info = reader()

            if last_hash != info["hash"]:
                for writer in writers:
                    writer(info)
                last_hash = info["hash"]

            for i in range(refresh_rate * 2):
                print("/-\|"[i % 4], end="\b", flush=True)
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("")
        pass

    print("Bye!")


def plugins(fetch_handlers):
    plugin_list = []
    for handler_name in fetch_handlers:
        package, classname = handler_name.rsplit(".", 1)
        try:
            handler_class = getattr(importlib.import_module(package), classname)
            plugin_list.append(handler_class())
        except NotImplementedError:
            # Skip missing plugins so that they can be ommitted from
            # installation if desired
            logger.logging.warning("FetchHandler {} not found, skipping plugin".format(handler_name))
    return plugin_list


if __name__ == "__main__":
    main()
