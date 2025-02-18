# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Produce n-gram frequencies in a word.
"""

def count_ngram(word, n=1, ngram_freq={}):
    """
    Counts n-gram frequencies in a given word. 
    For n-grams where n > 1 the word boundaries are taken into account,
        with the beginning of the word being denoted as ^ and the end as $.
    Updates the frequencies in an existing dictionary when the dictionary
        is provided as ngram_freq.

    Parameters
    ----------
    word : str
        A word to count the frequencies in.
    n : int, optional
        The value of n in for the n-grams. The default is 1.
        n = 1 - character frequency 
            E.g. banana: {'b': 1, 'a': 3, 'n': 2}
        n = 2 - bigram frequency 
            E.g. banana {'^b': 1, 'ba': 1, 'an': 2, 'na': 2, 'a$': 1}
        n = 3 - trigram frequency etc.
            E.g. banana {'^ba': 1, 'ban': 1, 'ana': 2, 'nan': 1, 'na$': 1}
    ngram_freq : dict, optional
        An existing frequency dictionary in a form of {n-gram : frequency}
            to be updated with new frequencies. The default is {}.

    Returns
    -------
    ngram_freq : dict
        Dictionary containing frequencies for every given n-gram in the word.

    """
    # Add word boundaries for n-grama where n > 1
    if n != 1:
        word = f"^{word}$"
                
    for idx in range(len(word)-(n-1)):
        ngram = word[idx:idx+(n)]
        # Skip spaces and punctuation for 1-grams
        if n == 1 and ngram in " -'":
            continue
        
        # Create an entry for the bigram in the frequency
        # dictionary if it doesn't exist yet
        ngram_freq.setdefault(ngram, 0)
        # Count the bigram
        ngram_freq[ngram] += 1
        
    return ngram_freq