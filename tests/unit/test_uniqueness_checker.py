"""
Unit tests for UniquenessChecker

Tests uniqueness validation, history persistence, and collision detection.
"""

import pytest
import os
import tempfile
from src.core.uniqueness_checker import UniquenessChecker, get_uniqueness_checker


class TestUniquenessChecker:
    """Test suite for UniquenessChecker class"""

    @pytest.fixture
    def temp_history_file(self):
        """Create temporary history file for testing"""
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        # Cleanup
        if os.path.exists(path):
            os.remove(path)

    def test_initialization(self, temp_history_file):
        """Test checker initialization"""
        checker = UniquenessChecker(history_file=temp_history_file)
        assert checker.used_numbers == set()
        assert checker.get_count() == 0

    def test_is_unique_new_number(self, temp_history_file):
        """Test that new numbers are unique"""
        checker = UniquenessChecker(history_file=temp_history_file)
        assert checker.is_unique("20251234567890")

    def test_is_unique_used_number(self, temp_history_file):
        """Test that used numbers are not unique"""
        checker = UniquenessChecker(history_file=temp_history_file)
        number = "20251234567890"

        checker.register_number(number)
        assert not checker.is_unique(number)

    def test_register_number_success(self, temp_history_file):
        """Test registering new number"""
        checker = UniquenessChecker(history_file=temp_history_file)
        number = "20251234567890"

        result = checker.register_number(number)
        assert result is True
        assert checker.get_count() == 1
        assert not checker.is_unique(number)

    def test_register_number_duplicate(self, temp_history_file):
        """Test registering duplicate number fails"""
        checker = UniquenessChecker(history_file=temp_history_file)
        number = "20251234567890"

        checker.register_number(number)
        result = checker.register_number(number)

        assert result is False
        assert checker.get_count() == 1

    def test_register_batch(self, temp_history_file):
        """Test registering batch of numbers"""
        checker = UniquenessChecker(history_file=temp_history_file)
        numbers = [
            "20251111111111",
            "20252222222222",
            "20253333333333"
        ]

        count = checker.register_batch(numbers)
        assert count == 3
        assert checker.get_count() == 3

        for number in numbers:
            assert not checker.is_unique(number)

    def test_register_batch_with_duplicates(self, temp_history_file):
        """Test batch registration handles duplicates"""
        checker = UniquenessChecker(history_file=temp_history_file)

        # Register first batch
        batch1 = ["20251111111111", "20252222222222"]
        checker.register_batch(batch1)

        # Register second batch with one duplicate
        batch2 = ["20252222222222", "20253333333333"]
        count = checker.register_batch(batch2)

        # Only 1 new number registered (one was duplicate)
        assert count == 1
        assert checker.get_count() == 3

    def test_check_batch(self, temp_history_file):
        """Test checking batch for uniqueness"""
        checker = UniquenessChecker(history_file=temp_history_file)

        # Register some numbers
        checker.register_number("20251111111111")
        checker.register_number("20252222222222")

        # Check batch
        to_check = [
            "20251111111111",  # duplicate
            "20253333333333",  # unique
            "20254444444444",  # unique
        ]

        unique, duplicates = checker.check_batch(to_check)

        assert len(unique) == 2
        assert len(duplicates) == 1
        assert "20251111111111" in duplicates

    def test_persistence_save_load(self, temp_history_file):
        """Test that history is persisted and loaded correctly"""
        numbers = [
            "20251111111111",
            "20252222222222",
            "20253333333333"
        ]

        # Create checker and register numbers
        checker1 = UniquenessChecker(history_file=temp_history_file)
        checker1.register_batch(numbers)

        # Create new checker instance (should load history)
        checker2 = UniquenessChecker(history_file=temp_history_file)

        # Verify history was loaded
        assert checker2.get_count() == 3
        for number in numbers:
            assert not checker2.is_unique(number)

    def test_clear_history(self, temp_history_file):
        """Test clearing history"""
        checker = UniquenessChecker(history_file=temp_history_file)
        checker.register_batch(["20251111111111", "20252222222222"])

        assert checker.get_count() == 2

        checker.clear_history()

        assert checker.get_count() == 0
        assert checker.is_unique("20251111111111")

    def test_export_history(self, temp_history_file):
        """Test exporting history to different file"""
        checker = UniquenessChecker(history_file=temp_history_file)
        numbers = ["20251111111111", "20252222222222"]
        checker.register_batch(numbers)

        # Export to new file
        export_path = temp_history_file + "_export.json"
        result = checker.export_history(export_path)

        assert result is True
        assert os.path.exists(export_path)

        # Verify exported content
        checker2 = UniquenessChecker(history_file=export_path)
        assert checker2.get_count() == 2

        # Cleanup
        os.remove(export_path)

    def test_singleton_get_uniqueness_checker(self):
        """Test singleton pattern for get_uniqueness_checker()"""
        checker1 = get_uniqueness_checker()
        checker2 = get_uniqueness_checker()

        # Should be same instance
        assert checker1 is checker2

    def test_large_batch_performance(self, temp_history_file):
        """Test performance with large number of entries"""
        checker = UniquenessChecker(history_file=temp_history_file)

        # Generate 1000 unique numbers
        numbers = [f"2025{i:010d}" for i in range(1000)]

        # Register all
        count = checker.register_batch(numbers)

        assert count == 1000
        assert checker.get_count() == 1000

        # Check lookup performance (should be fast - O(1))
        assert not checker.is_unique(numbers[0])
        assert not checker.is_unique(numbers[500])
        assert not checker.is_unique(numbers[999])

    def test_concurrent_registration_simulation(self, temp_history_file):
        """Simulate concurrent registration (same file, different instances)"""
        # Instance 1 registers numbers
        checker1 = UniquenessChecker(history_file=temp_history_file)
        checker1.register_batch(["20251111111111", "20252222222222"])

        # Instance 2 loads and tries to register overlapping numbers
        checker2 = UniquenessChecker(history_file=temp_history_file)
        result = checker2.register_number("20251111111111")

        # Should detect duplicate
        assert result is False

        # Register new number
        result = checker2.register_number("20253333333333")
        assert result is True

        # Verify total count
        assert checker2.get_count() == 3


def test_history_file_corruption_handling(temp_history_file):
    """Test handling of corrupted history file"""
    # Create corrupted JSON file
    with open(temp_history_file, 'w') as f:
        f.write("{invalid json content")

    # Should handle gracefully and start with empty history
    checker = UniquenessChecker(history_file=temp_history_file)
    assert checker.get_count() == 0


def test_history_file_missing_directory():
    """Test handling when history directory doesn't exist"""
    non_existent_path = "/tmp/non_existent_dir/history.json"

    checker = UniquenessChecker(history_file=non_existent_path)
    checker.register_number("20251111111111")

    # Directory should be created automatically
    assert os.path.exists(os.path.dirname(non_existent_path))

    # Cleanup
    import shutil
    if os.path.exists("/tmp/non_existent_dir"):
        shutil.rmtree("/tmp/non_existent_dir")
