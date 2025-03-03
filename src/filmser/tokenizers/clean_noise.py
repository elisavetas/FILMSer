# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Removes unnecessary characters from tokens
"""

import unicodedata


SPLIT_CHARS = '\t[]()?!"/\\.,:;৷'



def is_allowed_on_border(char):
    """
    Check if a character is not part of the noisy characters
    and should be kept (is allowed) at the border of the token.
    Allowed characters:
        - alphabetic
        - space
        - apostrophe
        - some combining non-alpahbetic characters
        - some formatting characters

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
    if char.isalpha() or char in "' ":
        return True
    else:
        # Check for combining non-alphabetic characters
        uni_cat = unicodedata.category(char)
        uni_hex = hex(ord(char))
                
        # Remove if the character isn't combining  or formatting
        if uni_cat != "Mn" and uni_cat != "Mc" and uni_cat != "Cf":
            return False
        
        # Remove if the combining character is...
        elif (uni_hex.startswith("0x1d1") or  # musical
              uni_hex.startswith("0x1d2") or  # Greek musical
              uni_hex.startswith("0x1da")     # sign writing
              ):
                return False

    return True




def is_allowed_inside(char):
    """
    Check if a character is not part of the noisy characters
    and should be kept (is allowed) within the token.
    Allowed characters:
        - alphabetic
        - space
        - apostrophe
        - hyphen ! - not allowed at the border, but allowed inside
        - some combining non-alpahbetic characters
        - some formatting characters

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
    # Characters allowed at the birder of the word are allowed inside the word
    if is_allowed_on_border(char):
        return True
    # Hyphens is also allowed
    elif char == "-":
        return True
    return False



def clean_noise(token, lang="en", stats=False):
    """
    Removes noise from the borders of the given token, removes the whole token
        if the noise is inside of it / the token consists of noise.
    Noise - any non-alphabetic character with the exception of:
        - space
        - apostrophe
        - hyphen ! - not allowed at the border, but allowed inside
        - some combining non-alpahbetic characters
        - some formatting characters

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
    clean_token.strip(), str
        The cleaned version of the token stripped of leading / trailing spaces.
    removed : set
        A set of removed characters.

    """
    
    clean_token = token
    
    # Replace the splitting chars with a space to keep a token that way
    for char in SPLIT_CHARS:
        clean_token.replace(char, " ")
    
    removed = set()
    
    # If there are non-alphabetic parts in the token, check if it's only ' and -
    # Keep the ' and -
    if not token.isalpha():
        
        # If the token is one character, remove
        if len(token) <= 1:
            if stats and token:
                removed.add(token)
            return "", removed
        
        # Check if the only non-alphy characters are apostrophes (then keep)
        stripped_token = token.replace("'", "")
        
        # If there are additional non-alpha characters
        if not stripped_token.isalpha():
            
            # Remove non-alphabetic characters from the beginning excluiding apostrophe
            begginning_char = clean_token[0]
            while clean_token and not is_allowed_on_border(begginning_char):
                if stats:    
                    removed.add(clean_token[0])
                clean_token = clean_token[1:]
                # If there are no more characters left, return
                if not clean_token:
                    return "", removed
                begginning_char = clean_token[0]
                    
            # Remove non-alphabetic characters from the end excluiding apostrophe
            end_char = clean_token[-1]
            while clean_token and not is_allowed_on_border(end_char):
                if stats:
                    removed.add(clean_token[-1])
                clean_token = clean_token[:-1]
                # If there are no more characters left, return
                if not clean_token:
                    return "", removed
                end_char = clean_token[-1]
            
            # Check if the characters left in the middle are only apostrophes and hyphens
            stripped_token = clean_token.replace("'", "").replace("-", "")
            
            # If there are non-alpha characters in the middle of the word
            if not stripped_token.isalpha():
                remove_word = False
                # Check if they are noise or not
                for char in stripped_token:
                    # If one of the character inside of the word is noisy,
                    # remove the whole word
                    if not char.isalpha() and not is_allowed_inside(char):
                        if stats:
                            remove_word = True
                            removed.add(char)
                        else:
                            return "", removed
                
                if remove_word:
                    return "", removed
        
    if lang == "en":
        # Replace double apostrophes with a single one for English
        clean_token = clean_token.replace("''", "'")
    
    return clean_token.strip(), removed

