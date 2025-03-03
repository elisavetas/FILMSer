# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Extract IPA information.
"""

import pandas as pd


def extract_ipa(ipa_file_path):
    """
    Extract the IPA information from a file for a given language.

    Parameters
    ----------
    ipa_file_path : str / list
        The path to the file(s) with the IPA information if the information 
        is to be added. Provide a list of files to add several of them. 
        Expected data format:
                "word \tab IPA" per line

    Returns
    -------
    ipa_dict : dict
        A dictionary that provides an IPA transkription for available words.

    """
    if type(ipa_file_path) == str:
        ipa_file_path = [ipa_file_path]
    
    ipa_dict = {}
    
    # Go through every IPA file that exists for the given language
    for lang_file in ipa_file_path:
        # Extract the IPA data
        data = pd.read_csv(lang_file, sep='\t',
                            names=["Word", "IPA"], header=None)

        for index, row in data.iterrows():
            word, ipa = row["Word"], row["IPA"]
            
            # Add the new word to the dictionary
            if word not in ipa_dict:
                ipa_dict[word] = ipa
            
            # Add the new IPA to the word if it is already in the dictionary
            else:
                ipa_dict[word] = ipa_dict[word] + "  |  " + ipa
    
    return ipa_dict

