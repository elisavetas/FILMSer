# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for filmser package.

Test organization:
- conftest.py: Shared fixtures (raw_en_data, en_ipa_test)
- file_processors: Tests for file I/O (export_data, extract_from_gz, read_frequency_file)

Run tests with: pytest tests/
Run with coverage: pytest --cov=src/filmser tests/
Run a single file: pytest tests/file_processors/test_export_data.py
"""
