# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for file processing utilities."""

import pytest

from src.filmser.file_processors.extract_data import extract_from_gz
from src.filmser.file_processors.read_freq_file import read_frequency_file


class TestExtractFromGz:
    """Tests for extract_from_gz function."""

    def test_extract_gz_file(self, tmp_path):
        """Test extracting lines from a gzipped file."""
        import gzip
        
        # Create a gzipped file
        gz_file = tmp_path / "test.txt.gz"
        content = "Test line 1 is like noone\nText line 2 what can you do\nTest line 3 we got into the debris\n"
        with gzip.open(gz_file, mode="wt", encoding="utf-8") as f:
            f.write(content)
        
        result = extract_from_gz(str(gz_file))
        
        assert len(result) == 3, f"Expected 3 lines, got {len(result)}"
        assert result[0] == "Test line 1 is like noone\n", f"Line 1 mismatch: {result[0]}"
        assert result[1] == "Text line 2 what can you do\n", f"Line 2 mismatch: {result[1]}"
        assert result[2] == "Test line 3 we got into the debris\n", f"Line 3 mismatch: {result[2]}"

    def test_extract_japanese_gz_file(self, tmp_path):
        """Test extracting lines from a gzipped file."""
        import gzip
        
        # Create a gzipped file
        gz_file = tmp_path / "test.txt.gz"
        content = "テスト行 1 は誰もいないようです\nテキスト行 2 あなたは何ができますか\nテスト行 3 私たちは破片に入りました\n"
        with gzip.open(gz_file, mode="wt", encoding="utf-8") as f:
            f.write(content)
        
        result = extract_from_gz(str(gz_file))
        
        assert len(result) == 3, f"Expected 3 Japanese lines, got {len(result)}"
        assert result[0] == "テスト行 1 は誰もいないようです\n", f"Japanese line 1 mismatch: {result[0]}"
        assert result[1] == "テキスト行 2 あなたは何ができますか\n", f"Japanese line 2 mismatch: {result[1]}"
        assert result[2] == "テスト行 3 私たちは破片に入りました\n", f"Japanese line 3 mismatch: {result[2]}"

    def test_extract_arabic_gz_file(self, tmp_path):
        """Test extracting lines from a gzipped file."""
        import gzip
        
        # Create a gzipped file
        gz_file = tmp_path / "test.txt.gz"
        content = "سطر الاختبار 1 مثل لا أحد\nسطر النص 2 ماذا يمكنك أن تفعل\nسطر الاختبار 3 دخلنا في الحطام\n"
        with gzip.open(gz_file, mode="wt", encoding="utf-8") as f:
            f.write(content)
        
        result = extract_from_gz(str(gz_file))
        
        assert len(result) == 3, f"Expected 3 Arabic lines, got {len(result)}"
        assert result[0] == "سطر الاختبار 1 مثل لا أحد\n", f"Arabic line 1 mismatch: {result[0]}"
        assert result[1] == "سطر النص 2 ماذا يمكنك أن تفعل\n", f"Arabic line 2 mismatch: {result[1]}"
        assert result[2] == "سطر الاختبار 3 دخلنا في الحطام\n", f"Arabic line 3 mismatch: {result[2]}"

    def test_extract_nonexistent_file(self, tmp_path):
        """Test that FileNotFoundError is raised for missing file."""
        gz_file = tmp_path / "nonexistent.gz"
        
        with pytest.raises(FileNotFoundError):
            extract_from_gz(str(gz_file))

    def test_extract_with_path_object(self, tmp_path):
        """Test that Path objects work as input."""
        import gzip
        
        gz_file = tmp_path / "test.txt.gz"
        with gzip.open(gz_file, mode="wt", encoding="utf-8") as f:
            f.write("This test is the best\n")
        
        result = extract_from_gz(gz_file)
        
        assert len(result) == 1, f"Expected 1 line from Path object, got {len(result)}"
        assert result[0] == "This test is the best\n", f"Path object test line mismatch: {result[0]}"


class TestReadFrequencyFile:
    """Tests for read_frequency_file function."""

    def test_read_valid_frequency_file(self, tmp_path):
        """Test reading a valid frequency file."""
        freq_file = tmp_path / "freq.txt"
        freq_file.write_text(
            "Word\tFrequency\tFrequency per million\tZipf value\n"
            "apple\t3\t500000.0\t8.699\n"
            "banana\t2\t333333.3333\t8.5229\n"
            "orange\t1\t166666.6667\t8.2218\n",
            encoding="utf-8"
        )
      
        freq_lists = read_frequency_file(str(freq_file))

        unit_type, df = next(iter(freq_lists.items()))
        
        assert unit_type == "word", f"Expected unit_type 'word', got '{unit_type}'"
        assert len(df) == 3, f"Expected 3 rows in frequency file, got {len(df)}"
        assert list(df.columns) == ["Word", "Frequency", "Frequency per million", "Zipf value"], f"Column mismatch: {list(df.columns)}"

    def test_read_6_gram_file(self, tmp_path):
        """Test reading a valid frequency file."""
        freq_file = tmp_path / "freq.txt"
        freq_file.write_text(
            "6-gram\tFrequency\tFrequency per million\tZipf value\n"
            "^indef\t3\t500000.0\t8.699\n"
            "defini\t2\t333333.3333\t8.5229\n"
            "inite$\t1\t166666.6667\t8.2218\n",
            encoding="utf-8"
        )
      
        freq_lists = read_frequency_file(str(freq_file))

        unit_type, df = next(iter(freq_lists.items()))
        
        assert unit_type == "6-gram", f"Expected unit_type '6-gram', got '{unit_type}'"
        assert len(df) == 3, f"Expected 3 rows in 6-gram file, got {len(df)}"
        assert list(df.columns) == ["6-gram", "Frequency", "Frequency per million", "Zipf value"], f"6-gram column mismatch: {list(df.columns)}"

    def test_read_word_extended_file(self, tmp_path):
        """Test reading a valid frequency file."""
        freq_file = tmp_path / "freq.txt"
        freq_file.write_text(
            "Rank	Word	Frequency	Frequency per million	Zipf value	Lemma	PoS (simple)	PoS (detailed)	Morphology	Stop word\n"
            "3712	apple	103856	15.6095	4.1934	apple	NOUN	NN	Number=Sing	False\n"
            "6206	banana	52774	7.9319	3.8994	banana	NOUN	NN	Number=Sing	False\n"
            "8757	orange	32921	4.948	3.6944	orange	NOUN	NN	Number=Sing	False\n",
            encoding="utf-8"
        )
      
        freq_lists = read_frequency_file(str(freq_file))

        unit_type, df = next(iter(freq_lists.items()))
        
        assert unit_type == "word_extended", f"Expected unit_type 'word_extended', got '{unit_type}'"
        assert len(df) == 3, f"Expected 3 rows in word_extended file, got {len(df)}"
        assert list(df.columns) == ["Rank", "Word", "Frequency", "Frequency per million", "Zipf value", 
                                    "Lemma", "PoS (simple)", "PoS (detailed)", "Morphology", "Stop word"], f"word_extended column mismatch: {list(df.columns)}"

    def test_read_missing_file_raises(self, tmp_path):
        """Test that FileNotFoundError is raised for missing frequency file."""
        freq_file = tmp_path / "missing_freq.txt"
        
        with pytest.raises(FileNotFoundError):
            read_frequency_file(str(freq_file))

    def test_read_one_col_raises(self, tmp_path):
        """Test that invalid format raises error."""
        freq_file = tmp_path / "invalid_freq.txt"
        freq_file.write_text(
            "This is not a valid frequency file format.",
            encoding="utf-8"
        )
        
        with pytest.raises(ValueError):
            read_frequency_file(str(freq_file))

    def test_read_empty_raises(self, tmp_path):
        """Test that invalid format raises error."""
        freq_file = tmp_path / "invalid_freq.txt"
        freq_file.write_text(
            "",
            encoding="utf-8"
        )
        
        with pytest.raises(ValueError):
            read_frequency_file(str(freq_file))
