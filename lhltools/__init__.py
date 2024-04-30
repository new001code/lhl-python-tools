import sys
from pathlib import Path

from loguru import logger

logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")

conf_path = Path.joinpath(Path.cwd(), "conf")

if Path.exists(conf_path):
    logger.info("conf path exists")
    ini_glob = Path.rglob(conf_path, "*.ini")
    while True:
        try:
            print(next(ini_glob))
        except StopIteration:
            break
