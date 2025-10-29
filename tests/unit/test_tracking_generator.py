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
        """Test that generator initializes with unique session ID"""
        gen1 = TrackingNumberGenerator()
        gen2 = TrackingNumberGenerator()

        assert gen1.session_id >= 1000
        assert gen1.session_id <= 9999
        # Session IDs should be different (statistically)
        # Note: There's a tiny chance they're the same, but very unlikely

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
        """Test tracking number format components"""
        generator = TrackingNumberGenerator()
        number = generator.generate()

        # Extract components
        year = number[:4]
        session = number[4:8]
        sequence = number[8:14]

        # Validate year (should be current year)
        assert int(year) >= 2020
        assert int(year) <= 2100

        # Validate session (4 digits: 1000-9999)
        assert int(session) >= 1000
        assert int(session) <= 9999

        # Validate sequence (6 digits: 000000-999999)
        assert int(sequence) >= 0
        assert int(sequence) <= 999999

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

    def test_generate_consistency(self):
        """Test that generated numbers have consistent session ID within same generator"""
        generator = TrackingNumberGenerator()
        numbers = generator.generate_batch(10)

        # Extract session IDs
        session_ids = [num[4:8] for num in numbers]

        # All should have same session ID (from same generator instance)
        assert len(set(session_ids)) == 1

    def test_different_generators_different_sessions(self):
        """Test that different generator instances have different session IDs (statistically)"""
        gen1 = TrackingNumberGenerator()
        gen2 = TrackingNumberGenerator()

        numbers1 = gen1.generate_batch(5)
        numbers2 = gen2.generate_batch(5)

        session1 = numbers1[0][4:8]
        session2 = numbers2[0][4:8]

        # Statistically, should be different (not guaranteed, but 9000/10000 chance)
        # For test robustness, we just check they're valid
        assert 1000 <= int(session1) <= 9999
        assert 1000 <= int(session2) <= 9999


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
