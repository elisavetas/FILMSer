# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for the ICU tokenizer."""

from src.filmser.tokenizers.icu_tokenizer import icu_tokenizer


class TestIcuTokenizer:
    """Tests for the ICU tokenizer functionality."""

    def test_icu_tokenizer_basic(self):
        """Test ICU tokenizer on basic English text with punctuation."""
        text = "Hello, world! This is a test."
        tokens, removed = icu_tokenizer(text, lang="en", stats=True)
        expected_tokens = ["hello", "world", "this", "is", "a", "test"]
        assert tokens == expected_tokens, f"ICU basic tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'!'}, f"ICU basic removed tokens mismatch: expected {{',', '!', '.'}}, got {removed}"

    def test_icu_tokenizer_non_whitespace(self):
        """Test ICU tokenizer on text with non-whitespace tokenization (Japanese)."""
        text = "これはテストです。"
        tokens, removed = icu_tokenizer(text, lang="ja", stats=True)
        expected_tokens = ["これ", "は", "テスト", "です"]
        assert tokens == expected_tokens, f"ICU Japanese tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'。'}, f"ICU Japanese removed tokens mismatch: expected {{'。'}}, got {removed}"

    def test_icu_tokenizer_thai(self):
        """Test ICU tokenizer on a Thai text."""
        text = "สวัสดีครับ นี่คือการทดสอบ."
        tokens, removed = icu_tokenizer(text, lang="th", stats=True)
        expected_tokens = ['สวัสดี', 'ครับ', 'นี่', 'คือ', 'การ', 'ทดสอบ']
        assert tokens == expected_tokens, f"ICU Thai tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == set(), f"ICU Thai removed tokens mismatch: expected empty set, got {removed}"

    def test_icu_tokenizer_thai_dirty(self):
        """Test ICU tokenizer on a Thai text."""
        text = "นี่คือประโยคทดสอบที่ยาวมาก!!! มีสัญลักษณ์แปลกๆ เช่)น @#$% และตั1วเลข 1234."
        tokens, removed = icu_tokenizer(text, lang="th", stats=True)
        expected_tokens = ['นี่', 'คือ', 'ประโยค', 'ทดสอบ', 'ที่', 'ยาว', 'มาก', 'มี', 
                           'สัญลักษณ์', 'แปลกๆ', 'เช่', 'น', 'และ']
        assert tokens == expected_tokens, f"ICU Thai dirty tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {')', '!', '@', '#', '$', '%', '1', '2', '3', '4', 'ตั1วเลข'}, f"ICU Thai dirty removed tokens mismatch: expected {{'!', '@', '#', '$', '%', '1', '2', '3', '4', 'ตั1วเลข'}}, got {removed}"

    def test_icu_tokenizer_stats(self):
        """Test ICU tokenizer with stats collection."""
        text = "Hello!!! Thᩰis isौ a t3st."
        tokens, removed = icu_tokenizer(text, lang="en", stats=True)
        expected_tokens = ["hello", "thᩰis", "isौ", "a"]
        assert tokens == expected_tokens, f"ICU stats collection tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'!', 't3st'}, f"ICU stats collection removed tokens mismatch: expected {{'!', 't3st'}}, got {removed}"

    def test_icu_tokenizer_no_stats(self):
        """Test ICU tokenizer without stats collection."""
        text = "Hello!!! Thᩰis isौ a t3st."
        tokens, removed = icu_tokenizer(text, lang="en", stats=False)
        expected_tokens = ["hello", "thᩰis", "isौ", "a"]
        assert tokens == expected_tokens, f"ICU no stats tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == set(), f"ICU no stats should have empty removed set, got {removed}"

    def test_icu_tokenizer_unusual_postfix(self):
        """Test ICU tokenizer on Japanese with unusual postfix."""
        text = "これはテストです。"
        tokens, removed = icu_tokenizer(text, lang="ja_XX", stats=True)
        expected_tokens = ["これ", "は", "テスト", "です"]
        assert tokens == expected_tokens, f"ICU Japanese tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'。'}, f"ICU Japanese removed tokens mismatch: expected {{'。'}}, got {removed}"

    def test_icu_tokenizer_lowercase_postfix(self):
        """Test ICU tokenizer on Japanese with lowercase postfix."""
        text = "これはテストです。"
        tokens, removed = icu_tokenizer(text, lang="ja_jp", stats=True)
        expected_tokens = ["これ", "は", "テスト", "です"]
        assert tokens == expected_tokens, f"ICU Japanese tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'。'}, f"ICU Japanese removed tokens mismatch: expected {{'。'}}, got {removed}"
        