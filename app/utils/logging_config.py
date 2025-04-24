import logging

# Configure logger
log_formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')

# Stream handler for sending logs to stdout
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.DEBUG)

# Create and configure the logger
logger = logging.getLogger("audit_logger")
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)  # Write to stdout
