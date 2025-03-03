# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
PyICU-based tokenizer.
"""

import icu

from .clean_noise import clean_noise
from ..iso2lang import ISO2FULL, FULL2ISO


# from .lang_abbr import ISO2FULL
NON_WHITESPACE = ["th", "km", "my"]
NOT_IN_ICU = ['an', 'zh_CN', 'zh_TW']



def icu_tokenizer(text, lang="en", stats=False):
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
    
    # Check that tokenizer is available
    assert lang not in NOT_IN_ICU, f"ICU tokenizer for locale '{ISO2FULL[lang]}' does not exist."
    
    # Set the locale and iterator
    locale = icu.Locale(lang)
    break_iterator = icu.BreakIterator.createWordInstance(locale)
    
    # Replace comma and period with a space to make sure it splits on them
    for char in ",.":
        text = text.replace(char, " ")
    
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

