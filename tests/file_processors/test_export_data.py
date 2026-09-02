# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for file export functionality."""

import pytest
import pandas as pd
from pathlib import Path

from src.filmser.file_processors.export_data import export_data


class TestExportData:
    """Tests for export_data function."""

    @pytest.fixture
    def sample_df(self):
        """Create a sample DataFrame."""
        return pd.DataFrame({
            "Rank": [1, 2, 3],
            "Word": ["apple", "banana", "orange"],
            "Frequency": [3, 2, 1],
            "Frequency per million": [500000.0, 333333.3333, 166666.6667],
            "Zipf value": [8.699, 8.5229, 8.2218]
        })

    def test_export_txt_format(self, sample_df, tmp_path):
        """Test exporting to TSV format."""
        file_name = str(tmp_path / "test_output")
        export_data(sample_df, file_name, file_types="txt")
        
        output_file = Path(f"{file_name}.txt")
        assert output_file.exists(), f"TXT output file not created: {output_file}"
        
        # Read and verify
        result = pd.read_csv(output_file, sep="\t")
        assert len(result) == 3, f"Expected 3 rows in TXT export, got {len(result)}"
        assert "Word" in result.columns, f"'Word' column missing in TXT export. Columns: {list(result.columns)}"

    def test_export_csv_format(self, sample_df, tmp_path):
        """Test exporting to CSV format."""
        file_name = str(tmp_path / "test_output")
        export_data(sample_df, file_name, file_types="csv")
        
        output_file = Path(f"{file_name}.csv")
        assert output_file.exists(), f"CSV output file not created: {output_file}"

        # Read and verify
        result = pd.read_csv(output_file)
        assert len(result) == 3, f"Expected 3 rows in CSV export, got {len(result)}"
        assert "Word" in result.columns, f"'Word' column missing in CSV export. Columns: {list(result.columns)}"

    def test_export_tsv_format(self, sample_df, tmp_path):
        """Test exporting to TSV format."""
        file_name = str(tmp_path / "test_output")
        export_data(sample_df, file_name, file_types="tsv")
        
        output_file = Path(f"{file_name}.tsv")
        assert output_file.exists(), f"TSV output file not created: {output_file}"

        # Read and verify
        result = pd.read_csv(output_file, sep="\t")
        assert len(result) == 3, f"Expected 3 rows in TSV export, got {len(result)}"
        assert "Word" in result.columns, f"'Word' column missing in TSV export. Columns: {list(result.columns)}"

    def test_export_json_format(self, sample_df, tmp_path):
        """Test exporting to JSON format."""
        file_name = str(tmp_path / "test_output")
        export_data(sample_df, file_name, file_types="json")
        
        output_file = Path(f"{file_name}.json")
        assert output_file.exists(), f"JSON output file not created: {output_file}"

        # Read and verify
        result = pd.read_json(output_file, orient="records", lines=True)
        assert len(result) == 3, f"Expected 3 rows in JSON export, got {len(result)}"
        assert "Word" in result.columns, f"'Word' column missing in JSON export. Columns: {list(result.columns)}"

    def test_export_xlsx_format(self, sample_df, tmp_path):
        """Test exporting to XLSX format."""
        file_name = str(tmp_path / "test_output")
        export_data(sample_df, file_name, file_types="xlsx")
        
        output_file = Path(f"{file_name}.xlsx")
        assert output_file.exists(), f"XLSX output file not created: {output_file}"

        # Read and verify
        result = pd.read_excel(output_file)
        assert len(result) == 3, f"Expected 3 rows in XLSX export, got {len(result)}"
        assert "Word" in result.columns, f"'Word' column missing in XLSX export. Columns: {list(result.columns)}"

    def test_export_multiple_formats_list(self, sample_df, tmp_path):
        """Test exporting to multiple formats."""
        file_name = str(tmp_path / "test_output")
        export_data(sample_df, file_name, file_types=["txt", "csv"])
        
        assert Path(f"{file_name}.txt").exists(), f"Multiple format export: TXT file not created"
        assert Path(f"{file_name}.csv").exists(), f"Multiple format export: CSV file not created"

        # Read and verify TXT
        result_txt = pd.read_csv(Path(f"{file_name}.txt"), sep="\t")
        assert len(result_txt) == 3, f"Expected 3 rows in multi-format TXT, got {len(result_txt)}"
        assert "Word" in result_txt.columns, f"'Word' column missing in multi-format TXT. Columns: {list(result_txt.columns)}"

        # Read and verify CSV
        result_csv = pd.read_csv(Path(f"{file_name}.csv"))
        assert len(result_csv) == 3, f"Expected 3 rows in multi-format CSV, got {len(result_csv)}"
        assert "Word" in result_csv.columns, f"'Word' column missing in multi-format CSV. Columns: {list(result_csv.columns)}"

    def test_export_multiple_formats_string(self, sample_df, tmp_path):
        """Test exporting to multiple formats."""
        file_name = str(tmp_path / "test_output")
        export_data(sample_df, file_name, file_types="txt|csv")
        
        assert Path(f"{file_name}.txt").exists(), f"Multiple format export: TXT file not created"
        assert Path(f"{file_name}.csv").exists(), f"Multiple format export: CSV file not created"

        # Read and verify TXT
        result_txt = pd.read_csv(Path(f"{file_name}.txt"), sep="\t")
        assert len(result_txt) == 3, f"Expected 3 rows in multi-format TXT, got {len(result_txt)}"
        assert "Word" in result_txt.columns, f"'Word' column missing in multi-format TXT. Columns: {list(result_txt.columns)}"

        # Read and verify CSV
        result_csv = pd.read_csv(Path(f"{file_name}.csv"))
        assert len(result_csv) == 3, f"Expected 3 rows in multi-format CSV, got {len(result_csv)}"
        assert "Word" in result_csv.columns, f"'Word' column missing in multi-format CSV. Columns: {list(result_csv.columns)}"

    def test_export_creates_directory(self, sample_df, tmp_path):
        """Test that output directory is created if it doesn't exist."""
        file_name = str(tmp_path / "nested" / "deep" / "output")
        export_data(sample_df, file_name, file_types="txt")
        
        assert Path(f"{file_name}.txt").exists(), f"Directory creation failed: nested output file not created at {file_name}.txt"

    def test_export_empty_dataframe_raises(self, tmp_path):
        """Test that exporting empty DataFrame raises error."""
        df = pd.DataFrame()
        file_name = str(tmp_path / "output")
        
        with pytest.raises(ValueError, match="empty"):
            export_data(df, file_name)

    def test_export_invalid_type(self, sample_df, tmp_path):
        """Test that invalid file types are detected and default to txt."""
        file_name = str(tmp_path / "output")
        
        export_data(sample_df, file_name, file_types="pdf")

        # Check that default .txt file is created
        assert Path(f"{file_name}.tsv").exists(), f"Invalid type test: default .txt file not created"
        assert not Path(f"{file_name}.pdf").exists(), f"Invalid type test: .pdf file should not be created"


    def test_export_mixed_invalid_types_list(self, sample_df, tmp_path):
        """Test that valid types are detected among invalid file types."""
        file_name = str(tmp_path / "output")
        
        export_data(sample_df, file_name, file_types=["pdf", "json", "docx"])
        # Check that valid types are exported
        assert Path(f"{file_name}.json").exists(), f"Invalid types test: valid .json file not created"
        assert not Path(f"{file_name}.pdf").exists(), f"Invalid types test: invalid .pdf file should not be created"
        assert not Path(f"{file_name}.docx").exists(), f"Invalid types test: invalid .docx file should not be created"
        assert not Path(f"{file_name}.txt").exists(), f"Invalid types test: default .txt should not be created when valid types provided"

    def test_export_mixed_invalid_types_string(self, sample_df, tmp_path):
        """Test that valid types are detected among invalid file types."""
        file_name = str(tmp_path / "output")
        
        export_data(sample_df, file_name, file_types="pdf|json|docx")

        # Check that valid types are exported
        assert Path(f"{file_name}.json").exists(), f"Invalid types test: valid .json file not created"
        assert not Path(f"{file_name}.pdf").exists(), f"Invalid types test: invalid .pdf file should not be created"
        assert not Path(f"{file_name}.docx").exists(), f"Invalid types test: invalid .docx file should not be created"
        assert not Path(f"{file_name}.txt").exists(), f"Invalid types test: default .txt should not be created when valid types provided"

    def test_export_list_input(self, tmp_path):
        """Test that list input is converted to DataFrame and exported."""
        data = [
            {"Word": "apple", "Frequency": 3},
            {"Word": "banana", "Frequency": 2},
            {"Word": "orange", "Frequency": 1}
        ]
        file_name = str(tmp_path / "output")

        export_data(data, file_name, file_types="csv")
        assert Path(f"{file_name}.csv").exists(), f"List input export: CSV file not created"

        result_text = pd.read_csv(Path(f"{file_name}.csv"))
        assert len(result_text) == 3, f"List input: Expected 3 rows, got {len(result_text)}"
        assert "Word" in result_text.columns, f"List input: 'Word' column missing. Columns: {list(result_text.columns)}"

    def test_export_dict_cols_input(self, tmp_path):
        """Test that dict input is converted to DataFrame and exported."""
        data = {
            "Word": ["apple", "banana", "orange"],
            "Frequency": [3, 2, 1]
        }
        file_name = str(tmp_path / "output")

        export_data(data, file_name, file_types=["csv"])
        assert Path(f"{file_name}.csv").exists(), f"Dict cols input export: CSV file not created"

        result_text = pd.read_csv(Path(f"{file_name}.csv"))
        assert len(result_text) == 3, f"Dict cols input: Expected 3 rows, got {len(result_text)}"
        assert "Word" in result_text.columns, f"Dict cols input: 'Word' column missing. Columns: {list(result_text.columns)}"

    def test_export_dict_row_input(self, tmp_path):
        """Test that dict input is converted to DataFrame and exported."""
        data = {
            "Word": "apple",
            "Frequency": 3,
        }
        file_name = str(tmp_path / "output")

        export_data(data, file_name, file_types="csv")
        assert Path(f"{file_name}.csv").exists(), f"Dict row input export: CSV file not created"

        result_text = pd.read_csv(Path(f"{file_name}.csv"))
        assert len(result_text) == 1, f"Dict row input: Expected 1 row, got {len(result_text)}"
        assert "Word" in result_text.columns, f"Dict row input: 'Word' column missing. Columns: {list(result_text.columns)}"

    def test_export_invalid_input_raises(self, tmp_path):
        """Test that non-DataFrame input raises error."""
        file_name = str(tmp_path / "output")
        
        with pytest.raises(TypeError):
            export_data(("Invalid", "Type"), file_name)
