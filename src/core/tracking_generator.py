"""
Tracking Number Generator

This module generates unique 14-digit tracking numbers for Gyeongdong Express.
Uses cryptographically secure random number generation for maximum uniqueness.

Format: YYYY + RRR + MM + RRR + DD
- YYYY: Current year (4 digits)
- RRR: Random 3-digit number (100-999)
- MM: Current month (2 digits, 01-12)
- RRR: Random 3-digit number (100-999)
- DD: Current day (2 digits, 01-31)

Example: 20253291170804 = 2025 + 329 + 11 + 708 + 04
"""

import secrets
from datetime import datetime
from typing import List, Set, Optional, Callable

from src.utils.constants import (
    TRACKING_NUMBER_LENGTH,
    MAX_RETRY_ATTEMPTS,
)
from src.utils.validators import validate_tracking_number
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TrackingNumberGenerator:
    """
    Generates unique tracking numbers with format: YYYY + RRR + MM + RRR + DD
    - YYYY: Current year (4 digits)
    - RRR: Random1 (3 digits, 100-999)
    - MM: Current month (2 digits, 01-12)
    - RRR: Random2 (3 digits, 100-999)
    - DD: Current day (2 digits, 01-31)

    Total: 14 digits
    Example: 20253291170804 = 2025 + 329 + 11 + 708 + 04
    """

    def __init__(self):
        """Initialize generator"""
        logger.info("Initialized TrackingNumberGenerator with date-based format")

    @staticmethod
    def _generate_random_3digits() -> int:
        """
        Generate random 3-digit number (100-999)

        Returns:
            int: Random 3-digit number
        """
        return secrets.randbelow(900) + 100

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
        # Get current date components
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        # Generate two random 3-digit numbers
        random1 = self._generate_random_3digits()
        random2 = self._generate_random_3digits()

        # Format: YYYY + RRR + MM + RRR + DD
        tracking_number = f"{year}{random1:03d}{month:02d}{random2:03d}{day:02d}"

        # Validate before returning
        if not validate_tracking_number(tracking_number):
            logger.error(f"Generated invalid tracking number: {tracking_number}")
            raise ValueError(f"Generated invalid tracking number: {tracking_number}")

        return tracking_number

    def generate_batch(self, count: int, used_numbers: Optional[Set[str]] = None) -> List[str]:
        """
        Generate a batch of unique tracking numbers

        Args:
            count: Number of tracking numbers to generate
            used_numbers: Set of already-used numbers to avoid (optional)

        Returns:
            List[str]: List of unique tracking numbers

        Raises:
            RuntimeError: If unable to generate unique numbers after max retries
            ValueError: If count is negative or zero

        Example:
            >>> generator = TrackingNumberGenerator()
            >>> numbers = generator.generate_batch(100)
            >>> len(numbers) == len(set(numbers))  # All unique
            True
        """
        if count <= 0:
            raise ValueError(f"Count must be positive, got {count}")

        # Delegate to generate_with_progress without callback (DRY principle)
        return self.generate_with_progress(count, used_numbers, callback=None)

    def generate_with_progress(
        self,
        count: int,
        used_numbers: Optional[Set[str]] = None,
        callback: Optional[Callable[[int, int], None]] = None
    ) -> List[str]:
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
