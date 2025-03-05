# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Creates frequency list(s) from the given data.
"""

import pandas as pd

from .freq_counters.collect_frequencies import collect_frequencies
from .data_extenders.extend_data import extend_data

from .iso2lang import FULL2ISO
from .tokenizers.spacy_tokenizer import SIZE2SPACY



def create_new_list(data_path, lang="en", spacy_size="sm", spell_check=False, 
                    ipa_file="", count_character=False, count_bigram=False, 
                    stats=False, progress_bar=False):
    """
    Creates a frequency list from the given data.

    Parameters
    ----------
    data_path : str
        The path to the raw data file.
    lang : str, optional
        The language of the data as a full name (e.g. "English", not 
            case-sensitive) or abbreviation (e.g. "en").
        The default is "english".
    spacy_size : str, optional
        The size of the spacy model if spacy is used. 
        Options: sm (small), md (middle), lg (large), trf (transformer)
        The default is "sm" (small).
    spell_check : bool, optional
        Set to True to filter the words using Aspell spell checker. It is 
            important to set the lang value correct for the correct dictionary
            to be used. Default is False.
        You can find the Aspell spell checker at aspell.net as well as the
            dictionaries for different languages used here at 
            ftp.gnu.org/gnu/aspell/dict/0index.html.
    ipa_file : str, optional
        The path to the file(s) with the IPA information if the information 
        is to be added. Provide a list of files to add several of them. 
        The default is "" (= no IPA).
    count_character : bool, optional
        Set to True if the information about word character frequency is to 
        be added. The default is False.
    count_bigram : bool, optional
        Set to True if the information about bigram frequency within a word
            is to be added. The default is False.
    stats : bool, optional
        Set to True to have some statistical information about the corpus 
            printed out. The default is False.
    progress_bar : bool, optional
        Set to True to display a progress bar of the running processes.
        The default is False.

    Returns
    -------
    freq_dfs : dict of pandas DataFrames
        Contains DataFrames for different types of data (word, character, bigram).
        Form {data type name : DataFrame}

    """
    # Set the language to be an ISO code
    if len(lang) > 3  and "_" not in lang:
        lang = FULL2ISO[lang]

    if len(spacy_size) > 3 or spacy_size == "big":
        spacy_size = SIZE2SPACY[spacy_size]

    # Count the bigram and character frequencies here if don't have to spell-check
    count_c = count_character if not spell_check else False
    count_b = count_bigram if not spell_check else False
    
    freq_lists = collect_frequencies(data_path, lang=lang, stats=stats,
                                     spacy_size=spacy_size,
                                     count_character=count_c, 
                                     count_bigram=count_b, 
                                     progress_bar=progress_bar)

    freq_dfs = {}

    info_names = ["Lemma", "PoS (simple)", "PoS (detailed)", 
                  "Morphology", "Stop word"]

    for data_type, freq_list in freq_lists.items():
        
        unit_name = data_type.split("_")[0].capitalize()
        
        # Dictionary to DataFrame
        data_dict = {unit_name: [], "Frequency": freq_list.values()}
        
        for unit in freq_list:
            if type(unit) == str:
                data_dict[unit_name].append(unit)
            else:
                data_dict[unit_name].append(unit[0])
                
                for (info_name, info) in zip(info_names, unit[1:]):
                    data_dict.setdefault(info_name, [])
                    data_dict[info_name].append(info)
        
        freq_df = pd.DataFrame(data_dict)
        
        # Don't count chars and bigrams twice
        count_c = count_character if data_type == "word" and spell_check else False
        count_b = count_bigram if data_type == "word" and spell_check else False
        
        # Add additional data
        extended_dfs = extend_data(freq_df, unit_name=unit_name, lang=lang, 
                                   spell_check=spell_check, ipa_file=ipa_file,
                                   count_character=count_c, count_bigram=count_b, 
                                   stats=stats, progress_bar=progress_bar)
        
        for unit_name, freq_df in extended_dfs.items():
        
            if unit_name == "word" and data_type == "word_extended":
                unit_name = "word_extended"
        
            # Replace the dictionary with a cleaned up dataframe
            freq_dfs[unit_name] = freq_df
            
    return freq_dfs
    
    