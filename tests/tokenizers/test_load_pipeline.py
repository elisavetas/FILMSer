# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Tests for loading Spacy pipelines."""

from src.filmser.tokenizers.spacy_tokenizer import _get_pipeline_key, load_pipeline, unload_pipeline


class TestSpacyPipelineLoading:
    """Tests for Spacy pipeline loading functionality."""

    def test_get_pipeline_key(self):
        """Test getting the correct pipeline key."""
        assert _get_pipeline_key("en", "sm", True) == "en_sm_True", f"English sm pipeline with ling_info key mismatch: {_get_pipeline_key('en', 'sm', True)}"
        assert _get_pipeline_key("pl", "trf", False) == "pl_trf_False", f"Polish trf pipeline without ling_info key mismatch: {_get_pipeline_key('pl', 'trf', False)}"
        assert _get_pipeline_key("", "lg", True) == "_lg_True", f"Empty language lg pipeline with ling_info key mismatch: {_get_pipeline_key('', 'lg', True)}"
        assert _get_pipeline_key("no", "", False) == "no__False", f"Norwegian empty size pipeline without ling_info key mismatch: {_get_pipeline_key('no', '', False)}"
        assert _get_pipeline_key("", "", True) == "__True", f"Empty pipeline with ling_info key mismatch: {_get_pipeline_key('', '', True)}"

    def test_load_pipeline_english(self):
        """Test loading Spacy pipeline for English."""
        nlp = load_pipeline("en", "sm")
        assert nlp is not None, "English sm pipeline failed to load"
        assert nlp.lang == "en", f"Expected language 'en', got '{nlp.lang}'"
        assert nlp.meta["name"] == "core_web_sm", f"Expected pipeline name 'core_web_sm', got '{nlp.meta['name']}'"

    def test_load_pipeline_russian(self):
        """Test loading Spacy pipeline for Russian."""
        nlp = load_pipeline("ru", "sm")
        assert nlp is not None, "Russian sm pipeline failed to load"
        assert nlp.lang == "ru", f"Expected language 'ru', got '{nlp.lang}'"
        assert nlp.meta["name"] == "core_news_sm", f"Expected pipeline name 'core_news_sm', got '{nlp.meta['name']}'"

    def test_load_pipeline_japanese(self):
        """Test loading Spacy pipeline for Japanese."""
        nlp = load_pipeline("ja", "lg")
        assert nlp is not None, "Japanese lg pipeline failed to load"
        assert nlp.lang == "ja", f"Expected language 'ja', got '{nlp.lang}'"
        assert nlp.meta["name"] == "core_news_lg", f"Expected pipeline name 'core_news_lg', got '{nlp.meta['name']}'"

    def test_load_pipeline_polish_downgrade(self):
        """Test loading Spacy pipeline for Polish. Downgrade from trf to lg."""
        nlp = load_pipeline("pl", "trf")
        assert nlp is not None, "Polish lg downgrade pipeline failed to load"
        assert nlp.lang == "pl", f"Expected language 'pl', got '{nlp.lang}'"
        assert nlp.meta["name"] == "core_news_lg", f"Expected pipeline name 'core_news_lg', got '{nlp.meta['name']}'"

    def test_load_pipeline_code_no(self):
        """Test loading Spacy pipeline for Norwegian (general)."""
        nlp = load_pipeline("no", "md")
        assert nlp is not None, "Norwegian md pipeline failed to load"
        assert nlp.lang == "nb", f"Expected language 'nb', got '{nlp.lang}'"
        assert nlp.meta["name"] == "core_news_md", f"Expected pipeline name 'core_news_md', got '{nlp.meta['name']}'"

    def test_load_pipeline_code_yue(self):
        """Test loading Spacy pipeline for Yue Chinese."""
        nlp = load_pipeline("yue", "sm")
        assert nlp is not None, "Yue Chinese sm pipeline failed to load"
        assert nlp.lang == "zh", f"Expected language 'zh', got '{nlp.lang}'"
        assert nlp.meta["name"] == "core_web_sm", f"Expected pipeline name 'core_web_sm', got '{nlp.meta['name']}'"

    def test_load_pipeline_unavailable_language(self):
        """Test loading Spacy pipeline for an unavailable language (Breton)."""
        nlp = load_pipeline("br", "sm")
        assert nlp is not None, "Breton sm pipeline failed to load (should fallback to xx)"
        assert nlp.lang == "xx", f"Expected fallback language 'xx', got '{nlp.lang}'"
        assert nlp.meta["name"] == "ent_wiki_sm", f"Expected fallback pipeline name 'ent_wiki_sm', got '{nlp.meta['name']}'"

    def test_load_pipeline_unknown_language(self):
        """Test loading Spacy pipeline for an unknown language."""
        nlp = load_pipeline("xx", "sm")
        assert nlp is not None, "Unknown language xx pipeline failed to load"
        assert nlp.lang == "xx", f"Expected language 'xx', got '{nlp.lang}'"
        assert nlp.meta["name"] == "ent_wiki_sm", f"Expected pipeline name 'ent_wiki_sm', got '{nlp.meta['name']}'"

    def test_unload_pipeline(self):
        """Test unloading a Spacy pipeline."""
        # Load a pipeline first
        nlp = load_pipeline("en", "sm", ling_info=False)
        assert nlp is not None, "Pipeline failed to load"
        
        cache_key = _get_pipeline_key("en", "sm", False)
        
        # Import the cache to verify state
        from src.filmser.tokenizers.spacy_tokenizer import _PIPELINE_CACHE
        assert cache_key in _PIPELINE_CACHE, f"Pipeline should be in cache after loading"
        
        # Unload the pipeline
        unload_pipeline(nlp)
        
        # Verify it's removed from cache
        assert cache_key not in _PIPELINE_CACHE, f"Pipeline should be removed from cache after unloading"

    def test_unload_pipeline_none(self):
        """Test unloading with None pipeline (should handle gracefully)."""
        # Should not raise any exception
        unload_pipeline(None)
