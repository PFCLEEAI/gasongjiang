"""
Main Window UI

This module contains the main application window built with PyQt5.
Follows shadcn/ui + Tailwind CSS design principles for modern, professional appearance.

Architecture:
- Main window with centered layout
- Worker thread for background number generation (prevents UI freezing)
- Three-step workflow: Upload → Generate → Download
- Progress tracking with real-time updates
- Professional error handling with user-friendly messages

UI Components:
- Title label with company name
- Status label with dynamic messaging
- Progress bar for generation tracking
- Three action buttons with enabled/disabled states
- File dialogs for input/output file selection
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QFileDialog,
    QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QCloseEvent

import pandas as pd

from src.core.tracking_generator import TrackingNumberGenerator
from src.core.uniqueness_checker import get_uniqueness_checker
from src.handlers.excel_uploader import ExcelUploadHandler, ExcelUploadError
from src.handlers.excel_exporter import ExcelExportHandler, ExcelExportError
from src.utils.constants import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    MSG_INITIAL,
    MSG_FILE_LOADED,
    MSG_GENERATING,
    MSG_GENERATION_COMPLETE,
    MSG_FILE_SAVED,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GenerationWorker(QThread):
    """
    Worker thread for tracking number generation to prevent UI freezing.

    This thread runs number generation in the background, allowing the UI
    to remain responsive and update progress in real-time.

    Signals:
        progress(int, int): Emits (current_count, total_count) for progress updates
        finished(list): Emits list of generated tracking numbers on completion
        error(str): Emits error message if generation fails
    """

    progress = pyqtSignal(int, int)  # current, total
    finished = pyqtSignal(list)  # generated numbers
    error = pyqtSignal(str)  # error message

    def __init__(self, count: int, parent: Optional[QWidget] = None):
        """
        Initialize worker thread

        Args:
            count: Number of tracking numbers to generate
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.count = count

    def run(self) -> None:
        """
        Generate tracking numbers in background thread.

        This method runs in a separate thread and should not access UI components directly.
        All UI updates must be done via signal emissions.
        """
        try:
            generator = TrackingNumberGenerator()
            uniqueness_checker = get_uniqueness_checker()

            # Generate with progress updates
            numbers = generator.generate_with_progress(
                self.count,
                used_numbers=uniqueness_checker.used_numbers,
                callback=lambda current, total: self.progress.emit(current, total)
            )

            # Register all generated numbers
            uniqueness_checker.register_batch(numbers)

            self.finished.emit(numbers)

        except Exception as e:
            logger.error(f"Generation error in worker: {e}", exc_info=True)
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """
    Main application window for 가송장 생성기
    """

    def __init__(self):
        """
        Initialize main application window.

        Sets up UI components, loads styles, and initializes state variables.
        """
        super().__init__()

        # Application state
        self.current_df: Optional[pd.DataFrame] = None
        self.special_codes: Optional[List[str]] = None
        self.generated_numbers: Optional[List[str]] = None
        self.generation_worker: Optional[GenerationWorker] = None

        # Initialize UI
        self.init_ui()
        self.load_stylesheet()

        logger.info("MainWindow initialized")

    def init_ui(self) -> None:
        """Initialize user interface"""

        # Window properties
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(32, 24, 32, 24)
        main_layout.setSpacing(24)

        # ===== Title =====
        self.title_label = QLabel(f"{APP_NAME} (경동택배)")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # ===== Status Label =====
        self.status_label = QLabel(MSG_INITIAL)
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        main_layout.addWidget(self.status_label)

        # ===== Progress Bar =====
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        main_layout.addWidget(self.progress_bar)

        # ===== Button Layout =====
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        # Button 1: Upload File
        self.upload_btn = QPushButton("📂 파일 선택")
        self.upload_btn.clicked.connect(self.handle_upload)
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(self.upload_btn)

        # Button 2: Generate Numbers
        self.generate_btn = QPushButton("🔄 송장 생성")
        self.generate_btn.setEnabled(False)
        self.generate_btn.clicked.connect(self.handle_generate)
        self.generate_btn.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(self.generate_btn)

        # Button 3: Download Excel
        self.download_btn = QPushButton("💾 Excel 다운로드")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.handle_download)
        self.download_btn.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(self.download_btn)

        main_layout.addLayout(button_layout)

        # ===== Spacer =====
        main_layout.addStretch()

        # Set layout
        central_widget.setLayout(main_layout)

    def load_stylesheet(self) -> None:
        """Load QSS stylesheet"""
        try:
            stylesheet_path = Path(__file__).parent.parent.parent / "resources" / "styles.qss"
            if stylesheet_path.exists():
                with open(stylesheet_path, 'r', encoding='utf-8') as f:
                    stylesheet = f.read()
                    self.setStyleSheet(stylesheet)
                logger.info("Stylesheet loaded successfully")
            else:
                logger.warning(f"Stylesheet not found at {stylesheet_path}")
        except Exception as e:
            logger.error(f"Failed to load stylesheet: {e}")

    def handle_upload(self) -> None:
        """Handle file upload button click"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Excel 파일 선택",
                "",
                "Excel Files (*.xls *.xlsx);;All Files (*)"
            )

            if not file_path:
                logger.info("File selection cancelled")
                return

            logger.info(f"Selected file: {file_path}")

            # Read Excel file
            self.current_df = ExcelUploadHandler.read_excel(file_path)

            # Detect format and validate required column
            try:
                ExcelUploadHandler.detect_format(self.current_df)
            except ExcelUploadError as e:
                self.show_error("파일 형식 오류", str(e))
                logger.error(f"Format detection error: {e}")
                return

            # Extract special codes from the input
            self.special_codes = ExcelUploadHandler.extract_special_codes(self.current_df)

            # Update UI
            row_count = len(self.current_df)
            self.status_label.setText(MSG_FILE_LOADED.format(row_count))
            self.status_label.setObjectName("statusLabelSuccess")
            self.status_label.setStyleSheet("")  # Reset style, let QSS handle it

            # Enable generate button
            self.generate_btn.setEnabled(True)

            # Disable download button (reset state)
            self.download_btn.setEnabled(False)
            self.generated_numbers = None

            logger.info(f"File loaded: {row_count} rows with special codes")

        except ExcelUploadError as e:
            self.show_error("파일 로드 실패", str(e))
            logger.error(f"Upload error: {e}")

        except Exception as e:
            self.show_error("오류", f"예상치 못한 오류가 발생했습니다: {str(e)}")
            logger.error(f"Unexpected error during upload: {e}")

    def handle_generate(self) -> None:
        """Handle generate button click"""
        if self.current_df is None:
            self.show_warning("경고", "파일을 먼저 선택하세요.")
            return

        try:
            row_count = len(self.current_df)

            # Disable buttons during generation
            self.upload_btn.setEnabled(False)
            self.generate_btn.setEnabled(False)
            self.download_btn.setEnabled(False)

            # Show progress bar
            self.progress_bar.setVisible(True)
            self.progress_bar.setMaximum(row_count)
            self.progress_bar.setValue(0)

            # Update status
            self.status_label.setText(MSG_GENERATING.format(0, row_count))
            self.status_label.setObjectName("statusLabel")
            self.status_label.setStyleSheet("")

            logger.info(f"Starting generation for {row_count} rows")

            # Start worker thread
            self.generation_worker = GenerationWorker(row_count)
            self.generation_worker.progress.connect(self.on_generation_progress)
            self.generation_worker.finished.connect(self.on_generation_finished)
            self.generation_worker.error.connect(self.on_generation_error)
            self.generation_worker.start()

        except Exception as e:
            self.show_error("생성 실패", f"송장 생성 중 오류가 발생했습니다: {str(e)}")
            logger.error(f"Generation error: {e}")
            self.reset_ui_after_generation()

    def on_generation_progress(self, current: int, total: int) -> None:
        """Update progress bar"""
        self.progress_bar.setValue(current)
        self.status_label.setText(MSG_GENERATING.format(current, total))

    def on_generation_finished(self, numbers: list) -> None:
        """Handle generation completion"""
        self.generated_numbers = numbers

        # Update UI
        self.progress_bar.setVisible(False)
        self.status_label.setText(MSG_GENERATION_COMPLETE.format(len(numbers)))
        self.status_label.setObjectName("statusLabelSuccess")
        self.status_label.setStyleSheet("")

        # Enable buttons
        self.upload_btn.setEnabled(True)
        self.download_btn.setEnabled(True)

        logger.info(f"Generation complete: {len(numbers)} numbers")

        self.show_success("완료", f"{len(numbers)} 개의 송장번호가 생성되었습니다!")

    def on_generation_error(self, error_message: str) -> None:
        """Handle generation error"""
        self.show_error("생성 실패", error_message)
        self.reset_ui_after_generation()

    def reset_ui_after_generation(self) -> None:
        """Reset UI after generation (error or cancel)"""
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        self.generate_btn.setEnabled(True if self.current_df is not None else False)
        self.download_btn.setEnabled(False)

    def handle_download(self) -> None:
        """Handle download button click"""
        if self.special_codes is None or self.generated_numbers is None:
            self.show_warning("경고", "먼저 송장을 생성하세요.")
            return

        try:
            # Generate default filename
            default_filename = ExcelExportHandler.generate_filename()

            # Show save dialog
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "파일 저장",
                default_filename,
                "Excel Files (*.xlsx);;All Files (*)"
            )

            if not file_path:
                logger.info("Save cancelled")
                return

            # Ensure .xlsx extension
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'

            logger.info(f"Saving to: {file_path}")

            # Export with 3-column format (special codes, delivery company, tracking numbers)
            ExcelExportHandler.create_output(
                self.special_codes,
                self.generated_numbers,
                file_path
            )

            # Success message
            self.show_success("저장 완료", MSG_FILE_SAVED.format(file_path))
            logger.info(f"File saved successfully: {file_path}")

            # Reset for next operation
            self.reset_for_new_operation()

        except ExcelExportError as e:
            self.show_error("저장 실패", str(e))
            logger.error(f"Export error: {e}")

        except Exception as e:
            self.show_error("오류", f"파일 저장 중 오류가 발생했습니다: {str(e)}")
            logger.error(f"Unexpected error during export: {e}")

    def reset_for_new_operation(self) -> None:
        """Reset application for next operation"""
        self.current_df = None
        self.special_codes = None
        self.generated_numbers = None
        self.status_label.setText(MSG_INITIAL)
        self.status_label.setObjectName("statusLabel")
        self.status_label.setStyleSheet("")
        self.generate_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        logger.info("UI reset for new operation")

    def show_success(self, title: str, message: str) -> None:
        """Show success message box"""
        QMessageBox.information(self, title, message)

    def show_error(self, title: str, message: str) -> None:
        """Show error message box"""
        QMessageBox.critical(self, title, message)

    def show_warning(self, title: str, message: str) -> None:
        """Show warning message box"""
        QMessageBox.warning(self, title, message)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Handle window close event.

        Args:
            event: Close event from Qt

        Note:
            Always accepts the close event. Add confirmation dialog here if needed.
        """
        logger.info("Application closing")
        event.accept()


def main():
    """Main entry point for UI testing"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
