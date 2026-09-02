# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for export_data function with large datasets."""

import pandas as pd
from pathlib import Path
from src.filmser.file_processors.export_data import export_data


class TestExportDataLongXLSX:
    """Tests for export_data function - performance with large datasets."""

    def test_export_long_xlsx_format(self, tmp_path):
        """Test exporting a long DataFrame to XLSX format."""
        # Create a long DataFrame
        long_df = pd.DataFrame({
            "Rank": range(1, 1_200_000),
            "Word": [f"word{i}" for i in range(1, 1_200_000)],
            "Frequency": [1] * 1_199_999,
            "Frequency per million": [1000.0] * 1_199_999,
            "Zipf value": [3.0] * 1_199_999
        })
        
        file_name = str(tmp_path / "long_output")
        export_data(long_df, file_name, file_types="xlsx")
        
        output_file = Path(f"{file_name}.xlsx")
        assert output_file.exists(), "XLSX output file was not created."

        # Read and verify
        result = pd.read_excel(output_file)
        # Should be truncated to Excel limit; -1 for the header
        assert len(result) == 1_048_576-1, "XLSX file length does not match Excel limit."
        assert "Word" in result.columns, "Expected column 'Word' not found in XLSX."

        result_short_file = Path(f"{file_name}.100000.xlsx")
        assert result_short_file.exists(), "Shortened file not created."

        # Read and verify the shortened file
        result_short = pd.read_excel(result_short_file)
        assert len(result_short) == 100_000, "Shortened XLSX file length does not match expected length."
        assert "Word" in result_short.columns, "Expected column 'Word' not found in shortened XLSX."
