"""
Uniqueness Checker

This module ensures tracking number uniqueness across all sessions by maintaining
a persistent history of used numbers.
"""

import json
import os
from pathlib import Path
from typing import Set, List

from src.utils.constants import HISTORY_FILE
from src.utils.logger import get_logger

logger = get_logger(__name__)


class UniquenessChecker:
    """
    Maintains history of used tracking numbers and validates uniqueness.
    Uses file-based persistence to ensure uniqueness across application sessions.
    """

    def __init__(self, history_file: str = None):
        """
        Initialize uniqueness checker

        Args:
            history_file: Path to history file (default: number_history.json)
        """
        self.history_file = history_file or HISTORY_FILE
        self.used_numbers: Set[str] = self._load_history()
        logger.info(f"Initialized UniquenessChecker with {len(self.used_numbers)} existing numbers")

    def _load_history(self) -> Set[str]:
        """
        Load used numbers from history file

        Returns:
            Set[str]: Set of previously used tracking numbers
        """
        if not os.path.exists(self.history_file):
            logger.info(f"No history file found at {self.history_file}, starting fresh")
            return set()

        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                numbers = json.load(f)
                logger.info(f"Loaded {len(numbers)} numbers from history file")
                return set(numbers)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load history file: {e}. Starting with empty history.")
            return set()

    def _save_history(self) -> bool:
        """
        Persist used numbers to history file

        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            # Ensure directory exists
            history_path = Path(self.history_file)
            history_path.parent.mkdir(parents=True, exist_ok=True)

            # Save as JSON
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.used_numbers), f, indent=2, ensure_ascii=False)

            logger.debug(f"Saved {len(self.used_numbers)} numbers to history file")
            return True
        except IOError as e:
            logger.error(f"Failed to save history file: {e}")
            return False

    def is_unique(self, number: str) -> bool:
        """
        Check if tracking number has been used before

        Args:
            number: Tracking number to check

        Returns:
            bool: True if number is unique, False if already used
        """
        return number not in self.used_numbers

    def register_number(self, number: str) -> bool:
        """
        Register a tracking number as used

        Args:
            number: Tracking number to register

        Returns:
            bool: True if registered successfully, False if already existed

        Example:
            >>> checker = UniquenessChecker()
            >>> checker.register_number("20251234567890")
            True
            >>> checker.register_number("20251234567890")
            False
        """
        if not self.is_unique(number):
            logger.warning(f"Attempt to register duplicate number: {number}")
            return False

        self.used_numbers.add(number)
        self._save_history()
        logger.debug(f"Registered new number: {number}")
        return True

    def register_batch(self, numbers: List[str]) -> int:
        """
        Register multiple tracking numbers at once

        Args:
            numbers: List of tracking numbers to register

        Returns:
            int: Number of successfully registered numbers

        Example:
            >>> checker = UniquenessChecker()
            >>> numbers = ["20251111111111", "20252222222222", "20253333333333"]
            >>> checker.register_batch(numbers)
            3
        """
        initial_count = len(self.used_numbers)

        for number in numbers:
            if self.is_unique(number):
                self.used_numbers.add(number)
            else:
                logger.warning(f"Skipped duplicate in batch: {number}")

        registered_count = len(self.used_numbers) - initial_count
        self._save_history()

        logger.info(f"Registered {registered_count} new numbers from batch of {len(numbers)}")
        return registered_count

    def check_batch(self, numbers: List[str]) -> tuple[List[str], List[str]]:
        """
        Check a batch of numbers for uniqueness

        Args:
            numbers: List of numbers to check

        Returns:
            tuple[List[str], List[str]]: (unique_numbers, duplicate_numbers)

        Example:
            >>> checker = UniquenessChecker()
            >>> checker.register_number("20251111111111")
            True
            >>> unique, dupes = checker.check_batch(["20251111111111", "20252222222222"])
            >>> len(dupes)
            1
            >>> len(unique)
            1
        """
        unique = []
        duplicates = []

        for number in numbers:
            if self.is_unique(number):
                unique.append(number)
            else:
                duplicates.append(number)

        logger.debug(f"Batch check: {len(unique)} unique, {len(duplicates)} duplicates")
        return unique, duplicates

    def get_count(self) -> int:
        """
        Get total count of used numbers

        Returns:
            int: Total number of used tracking numbers
        """
        return len(self.used_numbers)

    def clear_history(self) -> bool:
        """
        Clear all history (use with caution!)

        Returns:
            bool: True if successful
        """
        logger.warning("Clearing all tracking number history!")
        self.used_numbers.clear()
        return self._save_history()

    def export_history(self, output_file: str) -> bool:
        """
        Export history to a different file

        Args:
            output_file: Path to export file

        Returns:
            bool: True if successful
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.used_numbers), f, indent=2, ensure_ascii=False)
            logger.info(f"Exported {len(self.used_numbers)} numbers to {output_file}")
            return True
        except IOError as e:
            logger.error(f"Failed to export history: {e}")
            return False


# Singleton instance for application-wide use
_checker_instance = None


def get_uniqueness_checker() -> UniquenessChecker:
    """
    Get singleton instance of UniquenessChecker

    Returns:
        UniquenessChecker: Global uniqueness checker instance
    """
    global _checker_instance
    if _checker_instance is None:
        _checker_instance = UniquenessChecker()
    return _checker_instance
