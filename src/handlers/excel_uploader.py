"""
Excel Upload Handler

This module handles Excel file uploads, validation, and parsing.
Supports .xls and .xlsx formats with comprehensive error handling.

Supported file formats:
- .xlsx (Office Open XML format)
- .xls (Legacy Excel format)

Expected file structure:
- Must contain '주문고유코드' column (order unique code)
- Additional columns are optional and preserved
"""

import os
from typing import Optional, List, Tuple, Dict, Any
import pandas as pd

from src.utils.constants import (
    SUPPORTED_FORMATS,
    MAX_FILE_SIZE,
    ERR_FILE_FORMAT,
    ERR_FILE_TOO_LARGE,
    ERR_FILE_EMPTY,
    ERR_FILE_READ,
    ERR_PERMISSION_DENIED,
)
from src.utils.validators import validate_file_path, validate_dataframe_not_empty
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ExcelUploadError(Exception):
    """Custom exception for Excel upload errors"""
    pass


class FileFormat:
    """Enum-like class for different Excel file formats"""
    STANDARD_FORMAT = "standard"  # Multiple columns with data
    TRACKING_ONLY_FORMAT = "tracking_only"  # Two columns: code + output


class ExcelUploadHandler:
    """
    Handles Excel file validation and upload operations
    Supports multiple Excel formats:
    - Standard format: Multiple columns with order data
    - Tracking only format: Just code column and output column
    """

    @staticmethod
    def detect_format(df: pd.DataFrame) -> str:
        """
        Auto-detect Excel file format based on structure and columns

        Args:
            df: DataFrame to analyze

        Returns:
            str: Format type (TRACKING_ONLY_FORMAT)

        Raises:
            ExcelUploadError: If required column is not found
        """
        columns = [str(col).strip() for col in df.columns]
        columns_lower = [col.lower() for col in columns]

        # Check for "주문고유코드" column (required)
        has_special_code = any('주문고유코드' in col for col in columns_lower)

        if not has_special_code:
            logger.error(f"Required column '주문고유코드' not found. Columns: {columns}")
            raise ExcelUploadError("파일에 '주문고유코드' 컬럼이 없습니다. 올바른 형식의 파일을 선택해주세요.")

        logger.info(f"Detected TRACKING_ONLY format with columns: {columns}")
        return FileFormat.TRACKING_ONLY_FORMAT

    @staticmethod
    def extract_special_codes(df: pd.DataFrame) -> List[str]:
        """
        Extract special codes from the DataFrame

        Args:
            df: DataFrame containing '주문고유코드' column

        Returns:
            list: List of special codes
        """
        columns = [str(col).strip() for col in df.columns]

        # Find the exact column name with "주문고유코드"
        special_code_col = None
        for col in columns:
            if '주문고유코드' in col:
                special_code_col = col
                break

        if special_code_col is None:
            logger.error(f"Could not find special code column in: {columns}")
            raise ExcelUploadError("'주문고유코드' 컬럼을 찾을 수 없습니다.")

        # Extract and convert to list
        codes = df[special_code_col].astype(str).tolist()
        logger.info(f"Extracted {len(codes)} special codes from column '{special_code_col}'")
        return codes

    @staticmethod
    def validate_file(file_path: str) -> None:
        """
        Validate Excel file before reading

        Args:
            file_path: Path to Excel file

        Raises:
            ExcelUploadError: If validation fails
        """
        is_valid, error_message = validate_file_path(file_path)

        if not is_valid:
            logger.error(f"File validation failed: {error_message}")
            raise ExcelUploadError(error_message)

        logger.info(f"File validation passed: {file_path}")

    @staticmethod
    def read_excel(file_path: str, return_format: bool = False) -> Tuple[pd.DataFrame, Optional[str]]:
        """
        Read Excel file and return DataFrame

        Args:
            file_path: Path to Excel file
            return_format: If True, return (df, format_type) tuple

        Returns:
            pd.DataFrame: Parsed Excel data
            OR
            tuple: (pd.DataFrame, format_type) if return_format=True

        Raises:
            ExcelUploadError: If file cannot be read

        Example:
            >>> handler = ExcelUploadHandler()
            >>> df = handler.read_excel("orders.xlsx")
            >>> len(df) > 0
            True
        """
        # Validate file first
        ExcelUploadHandler.validate_file(file_path)

        try:
            # Determine file extension
            file_ext = os.path.splitext(file_path)[1].lower()

            # Read based on extension
            if file_ext == '.xlsx':
                df = pd.read_excel(file_path, engine='openpyxl')
            elif file_ext == '.xls':
                df = pd.read_excel(file_path, engine='xlrd')
            else:
                raise ExcelUploadError(ERR_FILE_FORMAT)

            logger.info(f"Successfully read Excel file: {len(df)} rows, {len(df.columns)} columns")

            # Validate DataFrame
            is_valid, error_message = validate_dataframe_not_empty(df)
            if not is_valid:
                raise ExcelUploadError(error_message)

            # Detect format if requested
            if return_format:
                detected_format = ExcelUploadHandler.detect_format(df)
                return df, detected_format

            return df

        except PermissionError:
            error_msg = ERR_PERMISSION_DENIED
            logger.error(f"Permission error: {file_path}")
            raise ExcelUploadError(error_msg)

        except pd.errors.EmptyDataError:
            error_msg = ERR_FILE_EMPTY
            logger.error(f"Empty data error: {file_path}")
            raise ExcelUploadError(error_msg)

        except Exception as e:
            logger.error(f"Failed to read Excel file: {e}", exc_info=True)
            # Generic message to user (no internal details for security)
            raise ExcelUploadError("파일을 읽을 수 없습니다. 파일이 손상되었거나 형식이 올바르지 않습니다.")

    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """
        Get information about Excel file without fully reading it

        Args:
            file_path: Path to Excel file

        Returns:
            dict: File information (size, extension, etc.)
        """
        try:
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file_path)[1]
            file_name = os.path.basename(file_path)

            info = {
                'name': file_name,
                'path': file_path,
                'size_bytes': file_size,
                'size_mb': round(file_size / (1024 * 1024), 2),
                'extension': file_ext,
                'is_supported': file_ext.lower() in SUPPORTED_FORMATS,
            }

            logger.debug(f"File info: {info}")
            return info

        except Exception as e:
            logger.error(f"Failed to get file info: {e}")
            return {}

    @staticmethod
    def preview_excel(file_path: str, rows: int = 5) -> Optional[pd.DataFrame]:
        """
        Preview first N rows of Excel file

        Args:
            file_path: Path to Excel file
            rows: Number of rows to preview (default: 5)

        Returns:
            Optional[pd.DataFrame]: Preview data or None if error
        """
        try:
            df = ExcelUploadHandler.read_excel(file_path)
            preview = df.head(rows)
            logger.info(f"Preview generated: {len(preview)} rows")
            return preview
        except Exception as e:
            logger.error(f"Failed to generate preview: {e}")
            return None
