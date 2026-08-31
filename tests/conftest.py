# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Test configuration for import paths."""

import sys
from pathlib import Path

import pytest

# Ensure the repository root is on sys.path so 'import src.*' works in tests
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture
def raw_en_data():
    return "tests/fixtures/en_raw_text_test.txt"

@pytest.fixture
def en_ipa_test():
    return "tests/fixtures/en_ipa_test.txt"
