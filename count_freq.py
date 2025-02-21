# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Counting different types of frequencies.
"""

from count_ngram import count_ngram
from process_sent import process_sent



def count_freq(data_lines, count_character=False, count_bigram=False,
               stats=False, progress_bar=False):
    """
    Counts the frequency of every word in the data.
    Optionally counts the frequency of every character in the data.

    Parameters
    ----------
    data_lines : list of strings
        A list of lines (sentences) from the data file.
    count_character : bool, optional
        Set to True if the information about word character frequency is to be added. 
        The default is False.
    count_bigram : bool, optional
        Set to True if the information about bigram frequency within a word
            is to be added. The default is False.
    stats : bool, optional
        Set to True to have some statistical information about the corpus 
            printed out. The default is False.

    Returns
    -------
    word_freq : dictionary
        Dictionary containing word to its frequency.
    character_freq : dictionary
        Dictionary containing word character to its frequency 
            if count_character is True.
    bigram_freq : dictionary
        Dictionary containing bigram to its frequency if count_bigram is True.

    """
    word_freq = {}
    character_freq = {}
    bigram_freq = {}
    
    # Keep track of deleted characters
    deleted = set()
    
    def process_l(line):
        """
        Helper function for processing lines of data.
        """
        processed_sent, del_set = process_sent(line, stats=stats)
        
        deleted.update(del_set)
        
        # Go through every word in the given sentence
        for word in processed_sent:
            
            # Remove empty strings
            if not word:
                continue
            
            # Create an entry for the word in the frequency dictionary
            # if it doesn't exist yet
            word_freq.setdefault(word, 0)
            # Count the word
            word_freq[word] += 1
            
            if count_character:
                count_ngram(word, n=1, ngram_freq=character_freq)
            
            if count_bigram:
                count_ngram(word, n=2, ngram_freq=bigram_freq)
    
    
    
    # Progress bar
    if progress_bar:
        from alive_progress import alive_bar
        print("Calculating frequencies...")
        with alive_bar(len(data_lines), theme="scuba") as bar:
            # Go through every sentence in the data
            for line in data_lines:
                process_l(line)
                bar() # Show progress
    else:
        # Go through every sentence in the data
        for line in data_lines:
            process_l(line)
                
    
    if stats:
        print("Removed characters:\n", deleted, "\n")
    
    return word_freq, character_freq, bigram_freq

