"""
Modules to perform a source time function inversion.
"""

# Setup the Logger
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = 0

ch = logging.StreamHandler()

# Add formatter
FORMAT = "%(name)s - %(module)s - %(levelname)s:   %(message)s"
formatter = logging.Formatter(FORMAT)
ch.setFormatter(formatter)
logger.addHandler(ch)