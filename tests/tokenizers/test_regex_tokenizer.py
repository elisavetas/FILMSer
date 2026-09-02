# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for the Regex tokenizer."""

from src.filmser.tokenizers.regex_tokenizer import regex_tokenizer


class TestRegexTokenizer:
    """Tests for the Regex tokenizer functionality."""

    def test_regex_tokenizer_basic(self):
        """Test Regex tokenizer on basic English text."""
        text = "Hello, world! This is a test with some ice-cream on t0p 'cause I felt liкe 1t."
        tokens, removed = regex_tokenizer(text, lang="en", stats=True)
        expected_tokens = ["hello", "world", "this", "is", "a", "test", "with", "some", "ice-cream", 
                           "on", "'cause", "i", "felt", "liкe", "t"]
        assert tokens == expected_tokens, f"Regex basic tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'1', 't0p'}, f"Regex basic removed tokens mismatch: expected {{',', '!', '.', '1', 't0p'}}, got {removed}"

    def test_regex_tokenizer_russian(self):
        """Test Regex tokenizer on Russian text."""
        text = "Шла бабkа с тестом, у!пала у*пала мягким-местом."
        tokens, removed = regex_tokenizer(text, lang="ru", stats=True)
        expected_tokens = ["шла", "бабkа", "с", "тестом", "у", "пала", "мягким-местом"]
        assert tokens == expected_tokens, f"Regex Russian tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'у*пала'}, f"Regex Russian removed tokens mismatch: expected {{'.', ',', '!', 'у*пала'}}, got {removed}"

    def test_regex_tokenizer_apos_as_quotes(self):
        """Test Regex tokenizer handling apostrophes used as quotation marks."""
        text = "He said 'hello' and then 'goodbye'."
        tokens, removed = regex_tokenizer(text, lang="en", stats=True)
        expected_tokens = ["he", "said", "hello", "and", "then", "goodbye"]
        assert tokens == expected_tokens, f"Regex apostrophes as quotes tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == set(), f"Regex apostrophes as quotes removed tokens mismatch: expected empty set, got {removed}"

        text = "'What a day,' he said 'cause why not."
        tokens, removed = regex_tokenizer(text, lang="en", stats=True)
        expected_tokens = ["what", "a", "day", "he", "said", "'cause", "why", "not"]
        assert tokens == expected_tokens, f"Regex apostrophes as quotes tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == set(), f"Regex apostrophes as quotes removed tokens mismatch: expected empty set, got {removed}"


    def test_regex_tokenizer_stats(self):
        """Test Regex tokenizer with stats collection."""
        text = "Hello!!! Thᩰis isौ a t3st."
        tokens, removed = regex_tokenizer(text, lang="en", stats=True)
        expected_tokens = ["hello", "thᩰis", "isौ", "a"]
        assert tokens == expected_tokens, f"Regex stats collection tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'t3st'}, f"Regex stats collection removed tokens mismatch: expected {{'!', 't3st'}}, got {removed}"

    def test_regex_tokenizer_no_stats(self):
        """Test Regex tokenizer without stats collection."""
        text = "Hello!!! Thᩰis isौ a t3st."
        tokens, removed = regex_tokenizer(text, lang="en", stats=False)
        expected_tokens = ["hello", "thᩰis", "isौ", "a"]
        assert tokens == expected_tokens, f"Regex no stats tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == set(), f"Regex no stats should have empty removed set, got {removed}"