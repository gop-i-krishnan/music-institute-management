import logging


# Configure application-wide logging system
logging.basicConfig(
    level=logging.INFO,

    # Standardized log message structure
    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(name)s "
        "%(message)s"
    ),

    # Persist logs into application log file
    filename="app.log",

    # Append logs instead of overwriting file
    filemode="a"
)


# Shared logger instance used across backend modules
logger = logging.getLogger(__name__)