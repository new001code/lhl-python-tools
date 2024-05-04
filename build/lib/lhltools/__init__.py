from loguru import logger


def __init_default_logger():
    format_ = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
              '| <magenta>{process}</magenta>:<yellow>{thread}</yellow> ' \
              '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>'
    import sys
    # logger config
    # logger.level("debug", no=1, color="green", icon="🐞")
    # logger.level("info", no=2, color="blue", icon="ℹ️")
    # logger.level("warning", no=3, color="yellow", icon="⚠️")
    # logger.level("error", no=4, color="red", icon="❌")
    logger.add(
        sink=sys.stdout,
        format=format_,
        colorize=True,
        enqueue=True,
        level="DEBUG",
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
        try:
            logger.remove()
            if conf and conf["logger"] is not None:
                from loguru_config.loguru_config import LoguruConfig
                LoguruConfig.load(conf["logger"])
            else:
                __init_default_logger()
        except Exception as e:
            logger.error(f"Error: {e}")
            logger.remove()
            __init_default_logger()


def __init_lhl_python_tools():
    logger.info("Start initializing `lhl-python-tools` configuration")
    from time import perf_counter_ns

    from pathlib import Path
    all_start_time = perf_counter_ns()
    conf_path = Path.joinpath(Path.cwd(), "conf/lhl_tools_config.yml")
    if Path.exists(conf_path):
        logger.info("Profile detected.")
        __init_file_config(conf_path)
    else:
        logger.remove()
        __init_default_config()
    all_end_time = perf_counter_ns()
    timeout = all_end_time - all_start_time
    logger.info(f"Initialization completed, total time: {timeout / 1000000 : .2f} ms")


# init
__init_lhl_python_tools()
