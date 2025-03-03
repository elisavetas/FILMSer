# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Counting different types of frequencies.
"""

from .count_ngram import count_ngram



def count_freq(tokens, count_character=False, count_bigram=False,
               progress_bar=False):
    """
    Counts the frequency of every word in the data.
    Optionally counts the frequency of every character in the data.

    Parameters
    ----------
    tokens : list of strings or tuples
        A list of tokens to count the frequencies from.
    count_character : bool, optional
        Set to True if the information about word character frequency is to be added. 
        The default is False.
    count_bigram : bool, optional
        Set to True if the information about bigram frequency within a word
            is to be added. The default is False.
    progress_bar : bool, optional
        Set to True to display a progress bar of the running processes.
        The default is False.

    Returns
    -------
    freqs : dict of dicts {data type : frequency dictionary}
        Dictionary for each data type (word, word_extended, bigram, character)
            with a frequency dictionary
    """
    freqs = {"word": {}}
    
    def count(token):
        """
        Helper function for processing lines of data.
        """
        if not token:
            return
        
        # Count the tokens with additional info separately
        if type(token) == tuple:
            type_name = "word_extended"
            freqs.setdefault(type_name, {})
            freqs[type_name].setdefault(token, 0)
            freqs[type_name][token] += 1
            token = token[0]

        # Create an entry for the token in the frequency dictionary
        # if it doesn't exist yet
        freqs["word"].setdefault(token, 0)
        # Count the token
        freqs["word"][token] += 1
            
        if count_character:
            freqs.setdefault("character", {})
            count_ngram(token, n=1, ngram_freq=freqs["character"])
        
        if count_bigram:
            freqs.setdefault("bigram", {})
            count_ngram(token, n=2, ngram_freq=freqs["bigram"])
    

    print("Calculating frequencies...")
    if progress_bar:
        from alive_progress import alive_bar
        with alive_bar(len(tokens), theme="scuba") as bar:
            # Go through every sentence in the data
            for token in tokens:
                count(token)
                bar() # Show progress
    else:
        # Go through every sentence in the data
            for token in tokens:
                count(token)
    
    return freqs

