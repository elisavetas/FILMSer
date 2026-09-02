# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for tokenizer selection and token cleaning."""

import pytest

from src.filmser.tokenizers.pick_tokenizer import pick_tokenizer
from src.filmser.tokenizers.clean_noise import _unicode_category, _is_allowed_on_border, _is_allowed_inside, _strip_borders, clean_noise


class TestPickTokenizer:
    """Tests for pick_tokenizer function."""

    def test_pick_tokenizer_english(self):
        """Test tokenizer selection for English."""
        result = pick_tokenizer("en")
        assert result == "spacy", f"Expected 'spacy' for English, got '{result}'"

    def test_pick_tokenizer_breton(self):
        """Test tokenizer selection for Breton."""
        result = pick_tokenizer("br")
        assert result == "regex", f"Expected 'regex' for Breton, got '{result}'"

    def test_pick_tokenizer_norwegian(self):
        """Test tokenizer selection for Norwegian."""
        result = pick_tokenizer("no")
        assert result  == "spacy", f"Expected 'spacy' for Norwegian, got '{result}'"

    def test_pick_tokenizer_yue(self):
        """Test tokenizer selection for Yue Chinese."""
        result = pick_tokenizer("yue")
        assert result  == "spacy", f"Expected 'spacy' for Yue Chinese, got '{result}'"

    def test_pick_tokenizer_khmer(self):
        """Test tokenizer selection for Khmer."""
        result = pick_tokenizer("km")
        assert result  == "icu", f"Expected 'icu' for Khmer, got '{result}'"

    def test_pick_tokenizer_uppercase(self):
        """Test tokenizer selection for English."""
        result = pick_tokenizer("EN")
        assert result == "spacy", f"Expected 'spacy' for English, got '{result}'"

    def test_pick_tokenizer_returns_string(self):
        """Test that pick_tokenizer returns a string."""
        result = pick_tokenizer("en")
        assert isinstance(result, str), f"Expected string type, got {type(result)}"

    def test_pick_tokenizer_unknown_language(self):
        """Test tokenizer selection for an unknown language."""
        result = pick_tokenizer("xx")
        assert result == "regex", f"Expected 'regex' for unknown language, got '{result}'"

    def test_pick_tokenizer_empty_string(self):
        """Test tokenizer selection for empty language code."""
        result = pick_tokenizer("")
        assert result == "regex", f"Expected 'regex' for empty language code, got '{result}'"


class TestCleanNoiseHelpers:
    """Tests for helper functions in clean_noise module."""

    def text_unicode_category(self):
        """Test _unicode_category function."""
        assert _unicode_category("a") == "Ll", f"Expected 'Ll' for lowercase 'a', got '{_unicode_category('a')}'"
        assert _unicode_category("A") == "Lu", f"Expected 'Lu' for uppercase 'A', got '{_unicode_category('A')}'"
        assert _unicode_category("1") == "Nd", f"Expected 'Nd' for digit '1', got '{_unicode_category('1')}'"
        assert _unicode_category(" ") == "Zs", f"Expected 'Zs' for space, got '{_unicode_category(' ')}'"
        assert _unicode_category("!") == "Po", f"Expected 'Po' for '!', got '{_unicode_category('!')}'"
        assert _unicode_category("\u200d") == "Cf", f"Expected 'Cf' for Zero Width Joiner, got '{_unicode_category(chr(0x200d))}'"
        assert _unicode_category("ᩰ") == "Mc", f"Expected 'Mc' for Tai Tham Vowel Sign Oo, got '{_unicode_category('ᩰ')}'"
        assert _unicode_category("ौ") == "Mc", f"Expected 'Mc' for Devanagari Vowel Sign Au, got '{_unicode_category('ौ')}'"
        assert _unicode_category("֧") == "Mn", f"Expected 'Mn' for Hebrew Accent Darga, got '{_unicode_category('֧')}'"
        assert _unicode_category("ؘ") == "Mn", f"Expected 'Mn' for Arabic Small Fatha, got '{_unicode_category('ؘ')}'"
        assert _unicode_category("ۨ") == "Mn", f"Expected 'Mn' for Arabic Small High Noon, got '{_unicode_category('ۨ')}'"

    def test_is_allowed_on_border(self):
        """Test _is_allowed_on_border function."""
        assert _is_allowed_on_border("a") is True, "Letter 'a' should be allowed on border"
        assert _is_allowed_on_border("Щ") is True, "Cyrillic letter 'Щ' should be allowed on border"
        assert _is_allowed_on_border("'") is True, "Apostrophe should be allowed on border"
        assert _is_allowed_on_border("-") is False, "Hyphen should not be allowed on border"
        assert _is_allowed_on_border("1") is False, "Digit '1' should not be allowed on border"
        assert _is_allowed_on_border(" ") is False, "Space should not be allowed on border"
        assert _is_allowed_on_border("!") is False, "Exclamation mark should not be allowed on border"
        assert _is_allowed_on_border(".") is False, "Period should not be allowed on border"
        assert _is_allowed_on_border("\u200d") is False, "Zero Width Joiner should not be allowed on border"
        assert _is_allowed_on_border("\u2060") is False, "Word Joiner should not be allowed on border"
        assert _is_allowed_on_border("ᩰ") is True, "Tai Tham Vowel Sign Oo should be allowed on border"
        assert _is_allowed_on_border("ौ") is True, "Devanagari Vowel Sign Au should be allowed on border"
        assert _is_allowed_on_border("֧") is True, "Hebrew Accent Darga should be allowed on border"
        assert _is_allowed_on_border("ؘ") is True, "Arabic Small Fatha should be allowed on border"
        assert _is_allowed_on_border("ۨ") is True, "Arabic Small High Noon should be allowed on border"
        assert _is_allowed_on_border("𝅾") is False, "Musical Symbol Combining Staccatissimo should not be allowed on border"
        assert _is_allowed_on_border("𝉃") is False, "Combining Greek Musical Tetraseme should not be allowed on border"
        assert _is_allowed_on_border("𝨞") is False, "Signwriting Eyelashes Up should not be allowed on border"
        assert _is_allowed_on_border("\U0001da1c") is False, "Signwriting Eyes Widening Movement should not be allowed on border"

    def test_is_allowed_inside(self):
        """Test _is_allowed_inside function."""
        assert _is_allowed_inside("a") is True, "Letter 'a' should be allowed inside"
        assert _is_allowed_inside("Щ") is True, "Cyrillic letter 'Щ' should be allowed inside"
        assert _is_allowed_inside("'") is True, "Apostrophe should be allowed inside"
        assert _is_allowed_inside("-") is True, "Hyphen should be allowed inside"
        assert _is_allowed_inside("1") is False, "Digit '1' should not be allowed inside"
        assert _is_allowed_inside(" ") is True, "Space should be allowed inside"
        assert _is_allowed_inside("!") is False, "Exclamation mark should not be allowed inside"
        assert _is_allowed_inside(".") is False, "Period should not be allowed inside"
        assert _is_allowed_inside("\u200d") is True, "Zero Width Joiner should be allowed inside"
        assert _is_allowed_inside("\u2060") is True, "Word Joiner should be allowed inside"
        assert _is_allowed_inside("ᩰ") is True, "Tai Tham Vowel Sign Oo should be allowed inside"
        assert _is_allowed_inside("ौ") is True, "Devanagari Vowel Sign Au should be allowed inside"
        assert _is_allowed_inside("֧") is True, "Hebrew Accent Darga should be allowed inside"
        assert _is_allowed_inside("ؘ") is True, "Arabic Small Fatha should be allowed inside"
        assert _is_allowed_inside("ۨ") is True, "Arabic Small High Noon should be allowed inside"
        assert _is_allowed_inside("𝅾") is False, "Musical Symbol Combining Staccatissimo should not be allowed inside"
        assert _is_allowed_inside("𝉃") is False, "Combining Greek Musical Tetraseme should not be allowed inside"
        assert _is_allowed_inside("𝨞") is False, "Signwriting Eyelashes Up should not be allowed inside"
        assert _is_allowed_inside("\U0001da1c") is False, "Signwriting Eyes Widening Movement should not be allowed inside"

    def test_strip_borders(self):
        """Test _strip_borders function."""
        removed_chars = set()
        assert _strip_borders("!!!hello!!!", stats=True, removed=removed_chars) == "hello", f"Expected 'hello', got '{_strip_borders('!!!hello!!!', stats=True, removed=removed_chars)}'"
        assert removed_chars == {'!',}, f"Expected {{'!',}}, got {removed_chars}"

        removed_chars.clear()
        assert _strip_borders("-3-wor4d◌.---", stats=True, removed=removed_chars) == "wor4d", f"Expected 'wor4d', got '{_strip_borders('-3-wor4d◌.---', stats=True, removed=removed_chars)}'"
        assert removed_chars == {'-', '3', '.', '◌',}, f"Expected {{'-', '3', '.', '◌',}}, got {removed_chars}"

        removed_chars.clear()
        assert _strip_borders("   spaced  $ ", stats=True, removed=removed_chars) == "spaced", f"Expected 'spaced', got '{_strip_borders('   spaced   ', stats=True, removed=removed_chars)}'"
        assert removed_chars == {"$"}, f"Expected {'$'} for spaces, got {removed_chars}"


class TestCleanNoise:
    """Tests for clean_noise function."""

    def test_clean_noise_basic(self):
        """Test basic cleaning of noise from token."""
        token, removed = clean_noise("!!!hello! !!", stats=True)
        assert token == "hello", f"Expected 'hello', got '{token}'"
        assert removed == {'!',}, f"Expected {{'!',}}, got {removed}"

    def test_clean_noise_hyphen_inside(self):
        """Test cleaning of token with hyphen inside."""
        token, removed = clean_noise("---well-done---", stats=True)
        assert token == "well-done", f"Expected 'well-done', got '{token}'"
        assert removed == {'-',}, f"Expected {{'-',}}, got {removed}"

    def test_clean_noise_invalid_inside(self):
        """Test cleaning of token with invalid characters inside."""
        token, removed = clean_noise("---wel3l-done---", stats=True)
        assert token == "", f"Expected empty string after removing invalid inside, got '{token}'"
        assert removed == {'-', 'wel3l-done'}, f"Expected {{'-', 'wel3l-done'}}, got {removed}"

        token, removed = clean_noise("-3-wor4d◌.---", stats=True)
        assert token == "", f"Expected empty string for heavily invalid token, got '{token}'"
        assert removed == {'-', '3', '.', '◌', "wor4d"}, f"Expected {{'-', '3', '.', '◌', 'wor4d'}}, got {removed}"

    def test_clean_noise_only_noise(self):
        """Test cleaning of token that is only noise."""
        token, removed = clean_noise("!!! @@@ ###", stats=True)
        assert token == "", f"Expected empty string for noise-only token, got '{token}'"
        assert removed == {'!', '@', '#',}, f"Expected {{'!', '@', '#',}}, got {removed}"

    def test_clean_noise_no_stats(self):
        """Test cleaning of noise without stats collection."""
        token, removed = clean_noise("!!!hello!!!", stats=False)
        assert token == "hello", f"Expected 'hello' without stats, got '{token}'"
        assert removed == set(), f"Expected empty set without stats, got {removed}"
