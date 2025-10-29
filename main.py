#!/usr/bin/env python3
"""
가송장 생성기 (Gyeongdong Tracking Number Generator)

Main application entry point.
This desktop application generates unique tracking numbers for Gyeongdong Express
and assigns them to orders from Excel files.

Author: ChangHee Lee
Version: 1.0.0
"""

import sys
from PyQt5.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utils.logger import get_logger
from src.utils.constants import APP_NAME, APP_VERSION

logger = get_logger(__name__)


def main():
    """
    Main entry point for the application

    Returns:
        int: Exit code (0 for success)
    """
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")

    try:
        # Create Qt Application
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setApplicationVersion(APP_VERSION)

        # Create and show main window
        window = MainWindow()
        window.show()

        logger.info("Application window displayed")

        # Start event loop
        exit_code = app.exec_()

        logger.info(f"Application exiting with code {exit_code}")
        return exit_code

    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
