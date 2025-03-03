# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Tokenizer based on regular expressions. 
"""

import re

from .clean_noise import clean_noise


SPLIT_CHARS = ' \t?!\"\\\.,:;\\/\\(\\)\\[\\]\\{\\}৷'



def regex_tokenizer(text, lang="en", stats=False):
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
    quote_pattern = fr"(^|[{SPLIT_CHARS}])(?P<quote>'.*?')($|[{SPLIT_CHARS}])"
    quote_matches = re.finditer(quote_pattern, text)
    
    apo_quote_pos = []
    
    # Find positions of the apostrophes used as quotation marks
    for quote_match in quote_matches:
        start_pos = quote_match.start("quote")   # Position of opening apostrophe
        end_pos = quote_match.end("quote") - 1   # Position of closing apostrophe
        apo_quote_pos += [start_pos, end_pos]
    
    # Remove apostrophes used as quotation marks
    for apo_pos in apo_quote_pos[::-1]:
        text = text[:apo_pos] + text[apo_pos+1:]
    
    # Split tokens
    split_tokens = re.split(fr"[{SPLIT_CHARS}]+", text)
        
    clean_tokens = []
    all_removed = set()
    
    # Clean the noisy characters from the token
    for token in split_tokens:
        clean_token, removed = clean_noise(token, lang=lang, stats=stats)
        all_removed.update(removed)
        if clean_token:
            clean_tokens.append(clean_token)
    
    return clean_tokens, all_removed

