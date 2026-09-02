# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""
Picks the best tokenizer for a given language based on available options.
"""

from ..config import LANG2SPACYLANG, NON_WORD_BOUND_IN_ICU, SPACY_LANG


def pick_tokenizer(lang) -> str:
    """
    Picks the best tokenizer for the provided language.

    Parameters
    ----------
    lang : str
        The language code (e.g. "en" for English).

    Returns
    -------
    tokenizer : str
        The name of the best tokenizer for the language.
    """
    # Make sure the name is lowercase for consistent checking
    lang = lang.lower()

    # Adapt the language name to find the right tokenizer
    lang_spacy = LANG2SPACYLANG.get(lang.split("_")[0], lang.split("_")[0]) # Only use the main part for checking

    if lang_spacy in SPACY_LANG:  # Use spacy when possible
        tokenizer = "spacy"
    elif lang in NON_WORD_BOUND_IN_ICU:  # Use ICU for non-word-boundary languages
        tokenizer = "icu"
    else:
        tokenizer = "regex"
    
    return tokenizer