import sys
from loguru import logger

from loguru_config.loguru_config import LoguruConfig


def __init_default_logger():
    # logger config
    logger.level("DEBUG", no=1, color="<green>", icon="🐞")
    logger.level("INFO", no=2, color="<blue>", icon="ℹ️")
    logger.level("WARNING", no=3, color="<yellow>", icon="⚠️")
    logger.level("ERROR", no=4, color="<red>", icon="❌")
    logger.add(
        sink=sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> \
<level>{level: ^6}</level> {level.icon} \
<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        enqueue=True,
        backtrace=True,
        diagnose=True,
        catch=True,
    )


def __init_default_config():
    __init_default_logger()


def __init_file_config(conf_path):
    from yaml import safe_load

    with open(conf_path, "r") as f:
        conf = safe_load(f)
        if conf["logger"] is not None:
            LoguruConfig.load(dict(conf["logger"]))
        else:
            pass


def __init_lhl_python_tools():
    logger.info("Start initializing `lhl-python-tools` configuration")
    logger.remove()
    from time import perf_counter_ns

    from pathlib import Path
    all_start_time = perf_counter_ns()
    conf_path = Path.joinpath(Path.cwd(), "conf/lhl_tools_config.yml")
    if Path.exists(conf_path):
        logger.info("Profile detected.")
        __init_file_config(conf_path)
    else:
        __init_default_config()
    all_end_time = perf_counter_ns()
    timeout = all_end_time - all_start_time
    logger.info(f"Initialization completed, total time: {timeout / 1000000 : .2f} ms")


# init
__init_lhl_python_tools()
