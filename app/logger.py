"""
logger.py

Sets up logging configuration.
"""
import logging

def setup_logger():
    logging.basicConfig(filename='logs/activity.log',
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
