"""
Tracking Number Generator

This module generates unique 14-digit tracking numbers for Gyeongdong Express.
Uses cryptographically secure random number generation for maximum uniqueness.
"""

import secrets
from datetime import datetime
from typing import List

from src.utils.constants import (
    TRACKING_NUMBER_LENGTH,
    SESSION_ID_MIN,
    SESSION_ID_MAX,
    SEQUENCE_MAX,
    MAX_RETRY_ATTEMPTS,
)
from src.utils.validators import validate_tracking_number
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TrackingNumberGenerator:
    """
    Generates unique tracking numbers with format: YYYY + XXXX + XXXXXX
    - YYYY: Current year (4 digits)
    - XXXX: Session ID (4 digits, random)
    - XXXXXX: Sequence number (6 digits, random)
    """

    def __init__(self):
        """Initialize generator with unique session ID"""
        self.session_id = self._generate_session_id()
        logger.info(f"Initialized TrackingNumberGenerator with session_id={self.session_id}")

    @staticmethod
    def _generate_session_id() -> int:
        """
        Generate unique session ID (4 digits: 1000-9999)

        Returns:
            int: Random session ID
        """
        return secrets.randbelow(SESSION_ID_MAX - SESSION_ID_MIN) + SESSION_ID_MIN

    def generate(self) -> str:
        """
        Generate a single tracking number

        Returns:
            str: 14-digit tracking number

        Example:
            >>> generator = TrackingNumberGenerator()
            >>> number = generator.generate()
            >>> len(number)
            14
            >>> number.isdigit()
            True
        """
        # Get current year
        year = datetime.now().year

        # Generate random sequence (6 digits: 000000-999999)
        sequence = secrets.randbelow(SEQUENCE_MAX + 1)

        # Format: YYYY + XXXX + XXXXXX
        tracking_number = f"{year}{self.session_id:04d}{sequence:06d}"

        # Validate before returning
        if not validate_tracking_number(tracking_number):
            logger.error(f"Generated invalid tracking number: {tracking_number}")
            raise ValueError(f"Generated invalid tracking number: {tracking_number}")

        return tracking_number

    def generate_batch(self, count: int, used_numbers: set = None) -> List[str]:
        """
        Generate a batch of unique tracking numbers

        Args:
            count: Number of tracking numbers to generate
            used_numbers: Set of already-used numbers to avoid (optional)

        Returns:
            List[str]: List of unique tracking numbers

        Raises:
            RuntimeError: If unable to generate unique numbers after max retries

        Example:
            >>> generator = TrackingNumberGenerator()
            >>> numbers = generator.generate_batch(100)
            >>> len(numbers) == len(set(numbers))  # All unique
            True
        """
        # Delegate to generate_with_progress without callback (DRY principle)
        return self.generate_with_progress(count, used_numbers, callback=None)

    def generate_with_progress(self, count: int, used_numbers: set = None, callback=None) -> List[str]:
        """
        Generate batch with progress callback for UI updates

        Args:
            count: Number of tracking numbers to generate
            used_numbers: Set of already-used numbers to avoid
            callback: Function(current, total) called on progress updates

        Returns:
            List[str]: List of unique tracking numbers
        """
        if used_numbers is None:
            used_numbers = set()

        generated = []
        attempts = 0
        max_total_attempts = count * MAX_RETRY_ATTEMPTS

        logger.info(f"Starting batch generation with progress: count={count}")

        while len(generated) < count and attempts < max_total_attempts:
            number = self.generate()

            if number not in generated and number not in used_numbers:
                generated.append(number)

                # Call progress callback
                if callback:
                    callback(len(generated), count)

            attempts += 1

        if len(generated) < count:
            error_msg = f"Failed to generate {count} unique numbers. Only generated {len(generated)}."
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        logger.info(f"Batch generation complete: {len(generated)} numbers")
        return generated


# Convenience function for single-use generation
def generate_tracking_numbers(count: int) -> List[str]:
    """
    Generate tracking numbers without maintaining generator state

    Args:
        count: Number of tracking numbers to generate

    Returns:
        List[str]: List of unique tracking numbers

    Example:
        >>> numbers = generate_tracking_numbers(10)
        >>> len(numbers)
        10
    """
    generator = TrackingNumberGenerator()
    return generator.generate_batch(count)
