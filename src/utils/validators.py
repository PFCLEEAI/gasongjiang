"""
Input validation utilities

This module provides validation functions for file inputs, tracking numbers,
and other user inputs to ensure data integrity and security.
"""

import os
from typing import Tuple
from src.utils.constants import (
    SUPPORTED_FORMATS,
    MAX_FILE_SIZE,
    TRACKING_NUMBER_LENGTH,
    ERR_FILE_FORMAT,
    ERR_FILE_TOO_LARGE,
    ERR_FILE_EMPTY,
    ERR_PERMISSION_DENIED,
)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_file_path(file_path: str) -> Tuple[bool, str]:
    """
    Validate file path for Excel upload

    Args:
        file_path: Path to file

    Returns:
        Tuple[bool, str]: (is_valid, error_message)

    Raises:
        ValidationError: If validation fails critically
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False, "파일이 존재하지 않습니다."

    # Check if it's a file (not directory)
    if not os.path.isfile(file_path):
        return False, "선택한 경로는 파일이 아닙니다."

    # Check file extension
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in SUPPORTED_FORMATS:
        return False, ERR_FILE_FORMAT

    # Check file size
    try:
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            return False, ERR_FILE_TOO_LARGE

        if file_size == 0:
            return False, ERR_FILE_EMPTY
    except OSError:
        return False, ERR_PERMISSION_DENIED

    # Check read permissions
    if not os.access(file_path, os.R_OK):
        return False, ERR_PERMISSION_DENIED

    return True, ""


def validate_tracking_number(number: str) -> bool:
    """
    Validate tracking number format

    Args:
        number: Tracking number string

    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(number, str):
        return False

    # Check length
    if len(number) != TRACKING_NUMBER_LENGTH:
        return False

    # Check if all digits
    if not number.isdigit():
        return False

    # Check year component (first 4 digits should be reasonable year)
    try:
        year = int(number[:4])
        if year < 2020 or year > 2100:
            return False
    except ValueError:
        return False

    return True


def validate_dataframe_not_empty(df) -> Tuple[bool, str]:
    """
    Validate that DataFrame has data

    Args:
        df: pandas DataFrame

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if df is None:
        return False, "데이터프레임이 None입니다."

    if df.empty:
        return False, ERR_FILE_EMPTY

    if len(df) == 0:
        return False, "데이터가 없습니다."

    return True, ""


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and illegal characters

    Args:
        filename: Original filename

    Returns:
        str: Sanitized filename
    """
    # Remove path separators
    filename = os.path.basename(filename)

    # Replace illegal characters
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        filename = filename.replace(char, '_')

    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')

    # Ensure not empty
    if not filename:
        filename = "output"

    return filename


def validate_output_path(file_path: str) -> Tuple[bool, str]:
    """
    Validate output file path for saving

    Args:
        file_path: Path where file will be saved

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Check directory exists
    directory = os.path.dirname(file_path)

    if directory and not os.path.exists(directory):
        return False, f"디렉토리가 존재하지 않습니다: {directory}"

    # Check write permissions
    if directory:
        if not os.access(directory, os.W_OK):
            return False, f"디렉토리에 쓰기 권한이 없습니다: {directory}"

    # Check if file already exists (warning, not error)
    if os.path.exists(file_path):
        # This is just a warning - user should confirm overwrite
        pass

    return True, ""
