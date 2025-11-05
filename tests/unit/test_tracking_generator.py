"""
Unit tests for TrackingNumberGenerator

Tests tracking number generation logic, format validation, and uniqueness guarantees.
"""

import pytest
from src.core.tracking_generator import TrackingNumberGenerator, generate_tracking_numbers
from src.utils.validators import validate_tracking_number


class TestTrackingNumberGenerator:
    """Test suite for TrackingNumberGenerator class"""

    def test_generator_initialization(self):
        """Test that generator initializes successfully"""
        gen1 = TrackingNumberGenerator()
        gen2 = TrackingNumberGenerator()

        # Both generators should initialize without error
        assert gen1 is not None
        assert gen2 is not None

    def test_generate_single_number(self):
        """Test single tracking number generation"""
        generator = TrackingNumberGenerator()
        number = generator.generate()

        # Check format
        assert isinstance(number, str)
        assert len(number) == 14
        assert number.isdigit()

        # Validate using validator
        assert validate_tracking_number(number)

    def test_generate_number_format(self):
        """Test tracking number format components: YYYY + RRR + MM + RRR + DD"""
        generator = TrackingNumberGenerator()
        number = generator.generate()

        # Extract components: YYYY (4) + RRR (3) + MM (2) + RRR (3) + DD (2) = 14
        year = number[:4]
        random1 = number[4:7]
        month = number[7:9]
        random2 = number[9:12]
        day = number[12:14]

        # Validate year (should be current year)
        assert int(year) >= 2020
        assert int(year) <= 2100

        # Validate random1 (3 digits: 100-999)
        assert int(random1) >= 100
        assert int(random1) <= 999

        # Validate month (2 digits: 01-12)
        assert int(month) >= 1
        assert int(month) <= 12

        # Validate random2 (3 digits: 100-999)
        assert int(random2) >= 100
        assert int(random2) <= 999

        # Validate day (2 digits: 01-31)
        assert int(day) >= 1
        assert int(day) <= 31

    def test_generate_batch_uniqueness(self):
        """Test that batch generation produces unique numbers"""
        generator = TrackingNumberGenerator()
        count = 100
        numbers = generator.generate_batch(count)

        # Check count
        assert len(numbers) == count

        # Check uniqueness
        assert len(set(numbers)) == count

        # Check format for all
        for number in numbers:
            assert validate_tracking_number(number)

    def test_generate_large_batch(self):
        """Test generation of large batch (1000+ numbers)"""
        generator = TrackingNumberGenerator()
        count = 1000
        numbers = generator.generate_batch(count)

        # Check count
        assert len(numbers) == count

        # Check uniqueness
        assert len(set(numbers)) == count

        # Verify all are valid
        invalid_count = sum(1 for num in numbers if not validate_tracking_number(num))
        assert invalid_count == 0

    def test_generate_with_used_numbers(self):
        """Test generation avoids already-used numbers"""
        generator = TrackingNumberGenerator()

        # Generate first batch
        batch1 = generator.generate_batch(50)
        used = set(batch1)

        # Generate second batch, avoiding first batch
        batch2 = generator.generate_batch(50, used_numbers=used)

        # Check no overlap
        overlap = set(batch1) & set(batch2)
        assert len(overlap) == 0

    def test_generate_with_progress_callback(self):
        """Test generation with progress callback"""
        generator = TrackingNumberGenerator()
        progress_calls = []

        def callback(current, total):
            progress_calls.append((current, total))

        count = 10
        numbers = generator.generate_with_progress(count, callback=callback)

        # Check result
        assert len(numbers) == count

        # Check progress was called
        assert len(progress_calls) > 0

        # Check progress increments correctly
        assert progress_calls[-1] == (count, count)

    def test_convenience_function(self):
        """Test convenience function generate_tracking_numbers()"""
        count = 20
        numbers = generate_tracking_numbers(count)

        assert len(numbers) == count
        assert len(set(numbers)) == count

        for number in numbers:
            assert validate_tracking_number(number)

    def test_generate_date_consistency(self):
        """Test that generated numbers contain current date components"""
        from datetime import datetime

        generator = TrackingNumberGenerator()
        numbers = generator.generate_batch(10)

        # Get current date
        now = datetime.now()
        expected_year = str(now.year)
        expected_month = f"{now.month:02d}"
        expected_day = f"{now.day:02d}"

        # All numbers should have same date components (generated at same time)
        for num in numbers:
            assert num[:4] == expected_year  # YYYY
            assert num[7:9] == expected_month  # MM
            assert num[12:14] == expected_day  # DD

    def test_random_components_vary(self):
        """Test that random components vary across generated numbers"""
        generator = TrackingNumberGenerator()
        numbers = generator.generate_batch(100)

        # Extract random components
        random1_values = [num[4:7] for num in numbers]
        random2_values = [num[9:12] for num in numbers]

        # Should have multiple different values (statistically very likely)
        # With 900 possible values each and 100 samples, we expect high diversity
        assert len(set(random1_values)) > 10
        assert len(set(random2_values)) > 10


@pytest.mark.parametrize("count", [1, 10, 100, 500])
def test_various_batch_sizes(count):
    """Parametrized test for various batch sizes"""
    numbers = generate_tracking_numbers(count)
    assert len(numbers) == count
    assert len(set(numbers)) == count


def test_batch_generation_error_handling():
    """Test that batch generation handles errors appropriately"""
    generator = TrackingNumberGenerator()

    # This test verifies that generation doesn't hang indefinitely
    # We'll generate a reasonable batch and ensure it completes
    try:
        numbers = generator.generate_batch(100)
        assert len(numbers) == 100
    except RuntimeError:
        pytest.fail("Batch generation failed unexpectedly")
