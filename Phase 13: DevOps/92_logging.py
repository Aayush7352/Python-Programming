import logging
import logging.handlers
import sys
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_data"):
            log_entry["extra"] = record.extra_data
        return json.dumps(log_entry)


def setup_basic_logging():
    """Basic logging configuration."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def setup_file_logging(log_file: str):
    """File logging with rotation."""
    logger = logging.getLogger("file_logger")
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1024 * 1024, backupCount=5
    )
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
    ))
    logger.addHandler(handler)
    return logger


def setup_json_logging():
    """JSON structured logging."""
    logger = logging.getLogger("json_logger")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    return logger


def log_examples():
    """Demonstrate various logging patterns."""
    logger = logging.getLogger(__name__)

    logger.debug("Debug message - detailed information")
    logger.info("Info message - general information")
    logger.warning("Warning message - something unexpected")
    logger.error("Error message - a problem occurred")
    logger.critical("Critical message - serious problem")

    # Logging with exception info
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Exception occurred with traceback")

    # Logging with extra data
    extra = {"extra_data": {"user_id": 123, "action": "login"}}
    logger.info("User action logged", extra=extra)


def demonstrate_logging_levels():
    """Show different logging levels."""
    print("=== Logging Levels ===")
    levels = [
        (logging.DEBUG, "DEBUG"),
        (logging.INFO, "INFO"),
        (logging.WARNING, "WARNING"),
        (logging.ERROR, "ERROR"),
        (logging.CRITICAL, "CRITICAL"),
    ]
    for level, name in levels:
        print(f"  {level:3} - {name}")
    print(f"\n  Default level: {logging.root.level}")
    print(f"  Default level name: {logging.getLevelName(logging.root.level)}")


def main():
    print("=== Basic Logging ===")
    setup_basic_logging()

    logger = logging.getLogger("main")
    logger.info("Starting logging demonstration")

    log_examples()

    print("\n=== File Logging with Rotation ===")
    file_logger = setup_file_logging("/tmp/app.log")
    for i in range(10):
        file_logger.info(f"Log entry {i + 1}")

    print("\n=== JSON Structured Logging ===")
    json_logger = setup_json_logging()
    json_logger.info("JSON formatted log entry")
    json_logger.warning("Warning with structured data")

    demonstrate_logging_levels()

    print("\n=== Logging Best Practices ===")
    print("  1. Use appropriate log levels")
    print("  2. Include context in log messages")
    print("  3. Use structured logging (JSON)")
    print("  4. Implement log rotation")
    print("  5. Avoid logging sensitive data")
    print("  6. Use logger per module")
    print("  7. Configure via dictConfig for complex setups")


if __name__ == "__main__":
    main()
