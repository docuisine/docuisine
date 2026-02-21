import sys

from loguru import logger

from docuisine.core.config import env

LOG_BUFFER: list[str] = []


def memory_sink(message):
    record = message.record
    formatted_time = record["time"].strftime("%Y-%m-%d %H:%M:%S")

    formatted = f"{formatted_time} | {record['level'].name} | {record['message']}"

    LOG_BUFFER.append(formatted)

    # prevent memory explosion
    if len(LOG_BUFFER) > env.MAX_LOG_LINES:
        LOG_BUFFER.pop(0)


def setup_logging():
    logger.remove()

    # Always log to stdout (serverless safe)
    logger.add(sys.stdout, level=env.LOG_LEVEL)

    # If file logging is explicitly enabled
    if env.LOG_FILE_PATH:
        logger.add(env.LOG_FILE_PATH, level=env.LOG_LEVEL)

    # Always keep memory buffer for UI logs
    logger.add(memory_sink, level=env.LOG_LEVEL)
