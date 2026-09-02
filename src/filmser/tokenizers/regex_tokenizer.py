# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""
Tokenizer based on regular expressions. 
"""

import re
from typing import Tuple, List, Set

from .clean_noise import clean_noise


SPLIT_CHARS = " \t?!\"\\.,:;/()[]{}"
REGEX_SPLIT_CHARS = re.escape(SPLIT_CHARS)

# Compile regex patterns at module level to load them once and reuse for efficiency
_QUOTE_PATTERN = re.compile(fr"(^|[{REGEX_SPLIT_CHARS}])(?P<quote>'.*?')($|[{REGEX_SPLIT_CHARS}])")
_SPLIT_PATTERN = re.compile(fr"[{REGEX_SPLIT_CHARS}]+")


def regex_tokenizer(text: str, lang: str = "en", stats: bool = False) -> Tuple[List[str], Set[str]]:
    """
    A tokenizer that uses regular expressions as basis for the tokenization.

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
    clean_tokens : list of strings
        A list of cleaned-up tokens from the line.
    all_removed : set
        A set of removed characters.
        
    """
    text = text.lower()
    
    # Find apostrophes used as quotation marks
    quote_matches = list(_QUOTE_PATTERN.finditer(text))
    
    # Remove apostrophes used as quotation marks (build new string to avoid reverse iteration)
    if quote_matches:
        result = []
        last_end = 0
        for match in quote_matches:
            quote_start = match.start("quote")
            quote_end = match.end("quote")
            # Add text before quote, then quote content without apostrophes
            result.append(text[last_end:quote_start])
            result.append(text[quote_start + 1:quote_end - 1])
            last_end = quote_end
        result.append(text[last_end:])
        text = "".join(result)
    
    # Split tokens
    split_tokens = _SPLIT_PATTERN.split(text)
        
    clean_tokens = []
    all_removed = set()
    
    # Clean the noisy characters from the token
    for token in split_tokens:
        clean_token, removed = clean_noise(token, lang=lang, stats=stats)
        if stats:
            all_removed.update(removed)
        if clean_token:
            clean_tokens.append(clean_token)
    
    return clean_tokens, all_removed

