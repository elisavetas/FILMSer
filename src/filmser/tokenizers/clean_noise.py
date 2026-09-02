# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""
Removes unnecessary characters from tokens
"""

import unicodedata
from functools import lru_cache


@lru_cache(maxsize=512)
def _unicode_category(char: str) -> str:
    """Cache unicode category lookups for performance."""
    return unicodedata.category(char)


def _is_allowed_on_border(char: str) -> bool:
    """
    Check if a character is not part of the noisy characters
    and should be kept (is allowed) at the border of the token.
    Allowed characters:
        - alphabetic
        - apostrophe
        - some combining non-alphabetic characters

    Parameters
    ----------
    char : str
        A character to be checked.

    Returns
    -------
    bool    
        True if the character is to be kept at the border of a token,
            False if not.

    """
    # Apostrophes are allowed
    if char.isalpha() or char == "'":
        return True
    
    # Remove if the character isn't combining
    uni_cat = _unicode_category(char)
    if uni_cat not in {"Mn", "Mc"}:
        return False
    
    # Remove if the combining character is...
    uni_hex = hex(ord(char))
    if (uni_hex.startswith("0x1d1") or  # musical
        uni_hex.startswith("0x1d2") or  # Greek musical
        uni_hex.startswith("0x1da")):   # sign writing
        return False

    return True


def _is_allowed_inside(char):
    """
    Check if a character is not part of the noisy characters
    and should be kept (is allowed) within the token.
    Allowed characters:
        - alphabetic
        - space
        - apostrophe
        - hyphen ! - not allowed at the border, but allowed inside
        - some combining non-alphabetic characters
        - some formatting characters ! - not allowed at the border, but allowed inside

    Parameters
    ----------
    char : str
        A character to be checked.

    Returns
    -------
    bool    
        True if the character is to be kept at the within a token,
            False if not.

    """
    # Characters allowed at the border of the word + hyphen and space are allowed inside the word
    if _is_allowed_on_border(char) or char in "- ":
        return True
    
    # Characters that are formatting are allowed inside the word (Characters of Category “Format”)
    uni_cat = _unicode_category(char)
    return uni_cat == "Cf"


def _strip_borders(token: str, stats: bool = False, removed: set = None) -> str:
    """
    Strip non-allowed characters from both ends of the token.

    Parameters
    ----------
    token : str
        The token to strip.
    stats : bool, optional
        Whether to collect removed characters for statistics. The default is False.
    removed : set, optional
        A set to store removed characters (if stats is enabled). If None, a new set is created.

    Returns
    -------
    str
        The token with non-allowed border characters removed.
    """
    if removed is None:
        removed = set()
        
    # Strip from beginning
    while token and not _is_allowed_on_border(token[0]):
        if stats and token[0] != " ":
            removed.add(token[0])
        token = token[1:]
    
    # Strip from end
    while token and not _is_allowed_on_border(token[-1]):
        if stats and token[-1] != " ":
            removed.add(token[-1])
        token = token[:-1]
    
    return token


def clean_noise(token, lang="en", stats=False):
    """
    Removes noise from the borders of the given token, removes the whole token
        if the noise is inside of it / the token consists of noise.
    Noise - any non-alphabetic character with the exception of:
        - space
        - apostrophe
        - hyphen ! - not allowed at the border, but allowed inside
        - some combining non-alphabetic characters
        - some formatting characters ! - not allowed at the border, but allowed inside

    Parameters
    ----------
    token : str
        The token to clean.
    lang : str, optional
        The language of the token as a full name (e.g. "English", not 
            case-sensitive) or abbreviation (e.g. "en").
        The default is "en".
    stats : bool, optional
        Set to True to have some statistical information about the corpus 
            be collected. The default is False.

    Returns
    -------
    clean_token, str
        The cleaned version of the token stripped of leading / trailing spaces.
        Returns an empty string if the token is to be removed as noise.
    removed : set
        A set of removed characters.

    """
    clean_token = token
    
    removed = set()
    
    # If there are non-alphabetic parts in the token, check if it's only ' and -
    if not token.isalpha():
        
        # If the token is one character, remove
        if len(token) <= 1:
            if stats and token and token != " ":
                removed.add(token)
            return "", removed
        
        # Check if the only non-alpha characters are apostrophes (then keep)
        stripped_token = token.replace("'", "")
        
        # If there are additional non-alpha characters
        if not stripped_token.isalpha():
            
            # Remove non-alphabetic characters from borders
            clean_token = _strip_borders(clean_token, stats, removed)
            if not clean_token:
                return "", removed
            
            # Check if remaining middle characters are valid
            for char in clean_token:
                if not char.isalpha() and not _is_allowed_inside(char):
                    if stats:
                        removed.add(clean_token)
                    return "", removed
    
    if lang == "en":
        # Replace double apostrophes with a single one for English
        clean_token = clean_token.replace("''", "'")
    
    return clean_token, removed
