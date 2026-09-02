# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""
PyICU-based tokenizer.
PyICU: https://pypi.org/project/PyICU/
"""

import icu
from typing import Tuple, List, Set

from .clean_noise import clean_noise

from ..config import FULL2ISO, ICU_LANG2POSTFIX


# Translation table for replacing punctuation with spaces (faster than multiple replace calls)
_PUNCT_TO_SPACE = str.maketrans(".,", "  ")


def icu_tokenizer(text: str, lang: str = "en", stats: bool = False) -> Tuple[List[str], Set[str]]:
    """
    A tokenizer that uses the PyICU module as basis for the tokenization.
    PyICU: https://pypi.org/project/PyICU/

    Parameters
    ----------
    text : str
        A string of text to be tokenized.
    lang : str, optional
        The language of the text as a full name (e.g. "English", not 
            case-sensitive) or abbreviation (e.g. "en").
        The default is "en".
    stats : bool, optional
        Set to True to have some statistical information about the corpus 
            be collected. The default is False.

    Returns
    -------
    tokens : list of strings
        A list of cleaned-up tokens from the line.
    removed : set
        A set of removed characters.
        
    """
    
    # Get the ISO code for the language if the full name was provided
    if lang.lower() in FULL2ISO:
        lang = FULL2ISO[lang.lower()]
    
    if "_" in lang:
        lang_base, postfix = lang.split("_", 1)
    else:
        lang_base, postfix = lang, ""

    if lang_base in ICU_LANG2POSTFIX and postfix.upper() not in ICU_LANG2POSTFIX[lang_base]:
        lang = lang_base  # Use base language if specific postfix not supported

    # Set up the ICU tokenizer
    locale = icu.Locale(lang)
    break_iterator = icu.BreakIterator.createWordInstance(locale)
    
    # Replace comma and period with a space
    text = text.translate(_PUNCT_TO_SPACE)
    
    # Process the given line
    break_iterator.setText(text)
    
    # Collect words from the output word boundaries
    tokens = []
    removed = set()
    
    start = break_iterator.first()
    for end in break_iterator:
        token = text[start:end]
        
        # Check for noise / clean the token
        token, removed_symb = clean_noise(token, lang=lang, stats=stats)
        if stats:
            removed.update(removed_symb)
                
        # Add non-noisy tokens (noisy: punctuation, random symbols, words with symbols inside)
        if token:
            tokens.append(token.lower())
            
        start = end  

    return tokens, removed
