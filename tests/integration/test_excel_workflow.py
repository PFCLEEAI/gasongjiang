"""
Integration tests for Excel workflow

Tests the complete workflow: Upload → Generate → Export
"""

import pytest
import os
import tempfile
import pandas as pd
from src.handlers.excel_uploader import ExcelUploadHandler, ExcelUploadError
from src.handlers.excel_exporter import ExcelExportHandler, ExcelExportError
from src.core.tracking_generator import generate_tracking_numbers
from src.utils.constants import COLUMN_TRACKING_NUMBER, COLUMN_DELIVERY_COMPANY


@pytest.fixture
def sample_excel_file():
    """Create a sample Excel file for testing"""
    # Create sample data
    data = {
        '주문번호': ['ORD001', 'ORD002', 'ORD003'],
        '고객명': ['김철수', '이영희', '박민수'],
        '상품명': ['iPhone 15', 'AirPods', 'MacBook'],
        '배송주소': ['서울시 강남구', '부산시 해운대구', '대전시 유성구']
    }
    df = pd.DataFrame(data)

    # Create temporary file
    fd, path = tempfile.mkstemp(suffix='.xlsx')
    os.close(fd)

    # Write Excel
    df.to_excel(path, index=False)

    yield path

    # Cleanup
    if os.path.exists(path):
        os.remove(path)


class TestExcelWorkflow:
    """Integration tests for complete Excel workflow"""

    def test_upload_valid_file(self, sample_excel_file):
        """Test uploading valid Excel file"""
        df = ExcelUploadHandler.read_excel(sample_excel_file)

        assert df is not None
        assert len(df) == 3
        assert '주문번호' in df.columns
        assert '고객명' in df.columns

    def test_upload_nonexistent_file(self):
        """Test uploading non-existent file raises error"""
        with pytest.raises(ExcelUploadError):
            ExcelUploadHandler.read_excel("/nonexistent/file.xlsx")

    def test_complete_workflow(self, sample_excel_file):
        """Test complete workflow: Upload → Generate → Export"""
        # Step 1: Upload
        df = ExcelUploadHandler.read_excel(sample_excel_file)
        row_count = len(df)

        # Step 2: Generate tracking numbers
        tracking_numbers = generate_tracking_numbers(row_count)
        assert len(tracking_numbers) == row_count
        assert len(set(tracking_numbers)) == row_count

        # Step 3: Export
        output_file = tempfile.mktemp(suffix='.xlsx')
        ExcelExportHandler.create_output(df, tracking_numbers, output_file)

        assert os.path.exists(output_file)

        # Step 4: Verify output
        output_df = pd.read_excel(output_file)

        # Check row count
        assert len(output_df) == row_count

        # Check new columns exist
        assert COLUMN_TRACKING_NUMBER in output_df.columns
        assert COLUMN_DELIVERY_COMPANY in output_df.columns

        # Check tracking numbers
        assert list(output_df[COLUMN_TRACKING_NUMBER]) == tracking_numbers

        # Check delivery company
        assert all(output_df[COLUMN_DELIVERY_COMPANY] == "경동택배")

        # Check original data preserved
        assert list(output_df['주문번호']) == ['ORD001', 'ORD002', 'ORD003']

        # Cleanup
        os.remove(output_file)

    def test_workflow_with_large_dataset(self):
        """Test workflow with larger dataset (100 rows)"""
        # Create large dataset
        data = {
            '주문번호': [f'ORD{i:04d}' for i in range(100)],
            '고객명': [f'고객{i}' for i in range(100)],
            '상품명': [f'상품{i}' for i in range(100)],
        }
        df = pd.DataFrame(data)

        # Generate numbers
        tracking_numbers = generate_tracking_numbers(100)

        # Export
        output_file = tempfile.mktemp(suffix='.xlsx')
        ExcelExportHandler.create_output(df, tracking_numbers, output_file)

        # Verify
        output_df = pd.read_excel(output_file)
        assert len(output_df) == 100
        assert COLUMN_TRACKING_NUMBER in output_df.columns

        # Cleanup
        os.remove(output_file)

    def test_export_mismatch_error(self, sample_excel_file):
        """Test export with mismatched numbers raises error"""
        df = ExcelUploadHandler.read_excel(sample_excel_file)

        # Generate wrong number of tracking numbers
        tracking_numbers = generate_tracking_numbers(5)  # df has 3 rows

        output_file = tempfile.mktemp(suffix='.xlsx')

        with pytest.raises(ExcelExportError):
            ExcelExportHandler.create_output(df, tracking_numbers, output_file)

    def test_file_info_retrieval(self, sample_excel_file):
        """Test getting file information"""
        info = ExcelUploadHandler.get_file_info(sample_excel_file)

        assert 'name' in info
        assert 'size_bytes' in info
        assert 'extension' in info
        assert info['is_supported'] is True

    def test_export_with_formatting(self, sample_excel_file):
        """Test export with formatting applied"""
        df = ExcelUploadHandler.read_excel(sample_excel_file)
        tracking_numbers = generate_tracking_numbers(len(df))

        output_file = tempfile.mktemp(suffix='.xlsx')
        result = ExcelExportHandler.create_output(
            df, tracking_numbers, output_file, apply_formatting=True
        )

        assert result is True
        assert os.path.exists(output_file)

        # Cleanup
        os.remove(output_file)

    def test_export_without_formatting(self, sample_excel_file):
        """Test export without formatting"""
        df = ExcelUploadHandler.read_excel(sample_excel_file)
        tracking_numbers = generate_tracking_numbers(len(df))

        output_file = tempfile.mktemp(suffix='.xlsx')
        result = ExcelExportHandler.create_output(
            df, tracking_numbers, output_file, apply_formatting=False
        )

        assert result is True
        assert os.path.exists(output_file)

        # Cleanup
        os.remove(output_file)

    def test_multiple_workflows_sequentially(self, sample_excel_file):
        """Test running multiple workflows sequentially"""
        for i in range(3):
            # Upload
            df = ExcelUploadHandler.read_excel(sample_excel_file)

            # Generate
            tracking_numbers = generate_tracking_numbers(len(df))

            # Export
            output_file = tempfile.mktemp(suffix=f'_{i}.xlsx')
            ExcelExportHandler.create_output(df, tracking_numbers, output_file)

            assert os.path.exists(output_file)

            # Cleanup
            os.remove(output_file)

    def test_filename_generation(self):
        """Test automatic filename generation"""
        filename = ExcelExportHandler.generate_filename()

        assert '가송장_생성기' in filename
        assert filename.endswith('.xlsx')
        assert len(filename) > 20  # Should include timestamp

    def test_output_preserves_original_columns(self, sample_excel_file):
        """Test that output preserves all original columns"""
        df = ExcelUploadHandler.read_excel(sample_excel_file)
        original_columns = list(df.columns)

        tracking_numbers = generate_tracking_numbers(len(df))

        output_file = tempfile.mktemp(suffix='.xlsx')
        ExcelExportHandler.create_output(df, tracking_numbers, output_file)

        # Read output
        output_df = pd.read_excel(output_file)

        # Check all original columns exist
        for col in original_columns:
            assert col in output_df.columns

        # Check data integrity
        for col in original_columns:
            assert list(output_df[col]) == list(df[col])

        # Cleanup
        os.remove(output_file)
