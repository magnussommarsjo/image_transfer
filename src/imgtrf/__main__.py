"""Application entrypoint"""
from imgtrf.cli import app
from imgtrf import logger

logger.configure_logger()
app()
