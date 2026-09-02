# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for the spaCy tokenizer."""

from src.filmser.tokenizers.spacy_tokenizer import spacy_tokenizer


class TestSpacyTokenizer:
    """Tests for the Spacy tokenizer functionality."""

    def test_spacy_tokenizer_basic(self):
        """Test Spacy tokenizer on basic English text with punctuation."""
        text = "Hello, world! This is a test."
        tokens, removed = spacy_tokenizer(text=text, lang="en", pipe_size="sm", ling_info=False, stats=True)
        expected_tokens = ["hello", "world", "this", "is", "a", "test"]
        assert tokens == expected_tokens, f"Basic tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {',', '!', '.'}, f"Removed tokens mismatch: expected {{',', '!', '.'}}, got {removed}"

    def test_spacy_tokenizer_ling_info(self):
        """Test Spacy tokenizer with linguistic information output."""
        text = "This is a foolproof test."
        tokens, removed = spacy_tokenizer(text=text, lang="en", pipe_size="sm", ling_info=True, stats=True)
        expected_tokens = [("this", "this", "DET", "DT", "Number=Sing|PronType=Dem", True), 
                           ("is", "be", "AUX", "VBZ", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin", True), 
                           ("a", "a", "DET", "DT", "Definite=Ind|PronType=Art", True), 
                           ("foolproof", "foolproof", "ADJ", "JJ", "Degree=Pos", False),
                           ("test", "test", "NOUN", "NN", "Number=Sing", False)]
        assert tokens == expected_tokens, f"Linguistic info tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'.'}, f"Removed tokens with ling_info mismatch: expected {{'.'}}, got {removed}"

    def test_spacy_tokenizer_russian(self):
        """Test Spacy tokenizer on text on a Russian sentence."""
        text = "Шла бабkа с тестом, у*пала мягким-местом."
        tokens, removed = spacy_tokenizer(text=text, lang="ru", pipe_size="sm", ling_info=False, stats=True)
        expected_tokens = ["шла", "бабkа", "с", "тестом", "мягким-местом"]
        assert tokens == expected_tokens, f"Russian tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'.', ',', 'у*пала'}, f"Russian removed tokens mismatch: expected {{'.', ',', 'у*пала'}}, got {removed}"

    def test_spacy_tokenizer_russian_ling_info(self):
        """Test Spacy tokenizer on text on a Russian sentence with linguistic info output."""
        text = "Я делаю не1кое тестирование."
        tokens, removed = spacy_tokenizer(text=text, lang="ru", pipe_size="sm", ling_info=True, stats=True)
        expected_tokens = [("я", "я", "PRON", "PRON", "Case=Nom|Number=Sing|Person=First", True), 
                           ("делаю", "делать", "VERB", "VERB", "Aspect=Imp|Mood=Ind|Number=Sing|Person=First|Tense=Pres|VerbForm=Fin|Voice=Act", False), 
                           ("тестирование", "тестирование", "NOUN", "NOUN", "Animacy=Inan|Case=Acc|Gender=Neut|Number=Sing", False)]
        assert tokens == expected_tokens, f"Russian ling_info tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {"не1кое", '.'}, f"Russian ling_info removed tokens mismatch: expected {{'не1кое', '.'}}, got {removed}"

    def test_spacy_tokenizer_non_whitespace(self):
        """Test Spacy tokenizer on text with non-whitespace tokenization (Japanese)."""
        text = "これはテストです。"
        tokens, removed = spacy_tokenizer(text=text, lang="ja", pipe_size="sm", ling_info=True, stats=True)
        expected_tokens = [("これ", "これ", "PRON", "代名詞", "Reading=コレ", True), 
                           ("は", "は", "ADP", "助詞-係助詞", "Reading=ハ", True), 
                           ("テスト", "テスト", "NOUN", "名詞-普通名詞-サ変可能", "Reading=テスト", False), 
                           ("です", "です", "AUX", "助動詞", "Inflection=助動詞-デス;終止形-一般|Reading=デス", True)]
        assert tokens == expected_tokens, f"Japanese non-whitespace tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'。'}, f"Japanese removed tokens mismatch: expected {{'。'}}, got {removed}"

    def test_spacy_tokenizer_unknown_czech(self):
        """Test Spacy tokenizer on text with unknown words (Czech)."""
        text = "Toto je příklad testovacího textu s neznámými slovy."
        tokens, removed = spacy_tokenizer(text=text, lang="cs", pipe_size="sm", ling_info=False, stats=True)
        expected_tokens = ["toto", "je", "příklad", "testovacího", "textu", "s", "neznámými", "slovy"]
        assert tokens == expected_tokens, f"Czech unknown words tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'.'}, f"Czech unknown words removed tokens mismatch: expected {{'.'}}, got {removed}"

    def test_spacy_tokenizer_empty_string(self):
        """Test Spacy tokenizer on an empty string."""
        text = ""
        tokens, removed = spacy_tokenizer(text=text, lang="en", pipe_size="sm", ling_info=False, stats=True)
        expected_tokens = []
        assert tokens == expected_tokens, f"Empty string tokenization should return empty list, got {tokens}"
        assert removed == set(), f"Empty string should have no removed tokens, got {removed}"

    def test_spacy_tokenizer_hyphenated_words(self):
        """Test Spacy tokenizer on text with hyphenated words."""
        text = "State-of-the-art technology is amazing."
        tokens, removed = spacy_tokenizer(text=text, lang="en", pipe_size="sm", ling_info=False, stats=True)
        expected_tokens = ["state-of-the-art", "technology", "is", "amazing"]
        assert tokens == expected_tokens, f"Hyphenated words tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'.'}, f"Hyphenated words removed tokens mismatch: expected {{'.'}}, got {removed}"
    
    def test_spacy_tokenizer_dirty(self):
        """Test Spacy tokenizer on text with noise that needs cleaning."""
        text = "Th1s is a test!!! Visit 'em http://example.com ther3."
        tokens, removed = spacy_tokenizer(text=text, lang="en", pipe_size="sm", ling_info=False, stats=True)
        expected_tokens = ["is", "a", "test", "visit", "'em", "ther"]
        assert tokens == expected_tokens, f"Dirty text tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'th1s', '!', '.', 'http://example.com', '3'}, f"Dirty text removed tokens mismatch: expected {{'th1s', '!', '.', 'http://example.com', '3'}}, got {removed}"
    
    def test_spacy_tokenizer_stats(self):
        """Test Spacy tokenizer with stats collection."""
        text = "Hello!!! Thᩰis isौ a t3st."
        tokens, removed = spacy_tokenizer(text=text, lang="en", pipe_size="sm", ling_info=False, stats=True)
        expected_tokens = ["hello", "thᩰis", "isौ", "a"]
        assert tokens == expected_tokens, f"Stats collection tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == {'.', '!', 't3st'}, f"Stats collection removed tokens mismatch: expected {{'.', '!', 't3st'}}, got {removed}"
    
    def test_spacy_tokenizer_no_stats(self):
        """Test Spacy tokenizer without stats collection."""
        text = "Hello!!! Thᩰis isौ a t3st."
        tokens, removed = spacy_tokenizer(text=text, lang="en", pipe_size="sm", ling_info=False, stats=False)
        expected_tokens = ["hello", "thᩰis", "isौ", "a"]
        assert tokens == expected_tokens, f"No stats tokenization mismatch: expected {expected_tokens}, got {tokens}"
        assert removed == set(), f"No stats should have empty removed set, got {removed}"
