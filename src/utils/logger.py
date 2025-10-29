"""
Logging utility

This module provides a centralized logging system for the application.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class AppLogger:
    """Centralized application logger"""

    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls, name: str = "가송장생성기", level: int = logging.INFO) -> logging.Logger:
        """
        Get or create application logger

        Args:
            name: Logger name
            level: Logging level (default: INFO)

        Returns:
            logging.Logger: Configured logger instance
        """
        if cls._instance is None:
            cls._instance = cls._create_logger(name, level)

        return cls._instance

    @classmethod
    def _create_logger(cls, name: str, level: int) -> logging.Logger:
        """
        Create and configure logger

        Args:
            name: Logger name
            level: Logging level

        Returns:
            logging.Logger: Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        # Optional: File handler (uncomment if needed)
        # log_dir = Path("logs")
        # log_dir.mkdir(exist_ok=True)
        # log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        #
        # file_handler = logging.FileHandler(log_file, encoding='utf-8')
        # file_handler.setLevel(logging.DEBUG)
        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

        return logger


# Convenience function
def get_logger(name: str = "가송장생성기") -> logging.Logger:
    """
    Get application logger instance

    Args:
        name: Logger name

    Returns:
        logging.Logger: Logger instance
    """
    return AppLogger.get_logger(name)
