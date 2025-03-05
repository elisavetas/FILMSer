# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Updates a given frequency list with additional information.
"""

import pandas as pd

from .create import create_new_list
from .data_extenders.extend_data import extend_data



def upd_exist_list(freq_list_path, lang="en", add_data_file="", 
                   spell_check=False, ipa_file="", count_character=False, 
                   count_bigram=False, stats=False, progress_bar=False):
    """
    Updates an existing frequency list with necessary information.

    Parameters
    ----------
    freq_list_path : str
        The path to the existing frequency list file.
    lang : str, optional
        The language of the data as a full name (e.g. "English", not 
            case-sensitive) or abbreviation (e.g. "en").
        The default is "english".
    add_data_file : str, optional
        Path to a raw data file to calculate new frequency information from and
        add it to an already existing frequency list. 
        The default is "" (= no new data to be added).
    spell_check : bool, optional
        Set to True to filter the words using Aspell spell checker. It is 
            important to set the lang value correct for the correct dictionary
            to be used. The default is False.
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
    freq_lists : dict of pandas DataFrames
        Contains DataFrames for different types of data (word, character, bigram).
        Form {data type name : DataFrame}

    """
    # Extract the frequency data from the file depending on its extension
    if freq_list_path.endswith("xlsx"):
        freq_list_df = pd.read_excel(freq_list_path, converters={'Word' : str})
    else:
        freq_list_df = pd.read_table(freq_list_path, converters={'Word' : str})
        
    # Add information from a new file
    if add_data_file:
        new_dfs = create_new_list(add_data_file, lang=lang, stats=stats, 
                                 progress_bar=progress_bar)
                
        if ("Stop word" in freq_list_df.columns and 
            "word_extended" in new_dfs):
            new_df = new_dfs["word_extended"]
            group_list = ["Word", "Lemma", "PoS (simple)", "PoS (detailed)", 
                          "Morphology", "Stop word"]
        else:
            new_df = new_dfs["word"]
            group_list = ["Word"]

        # Merge the existing list with the new one
        df_concat = pd.concat([freq_list_df, new_df])
        df_concat = df_concat.fillna("")
        
        freq_list_df = df_concat.groupby(group_list, 
                                         as_index=False)['Frequency'].sum()

        
    if spell_check or ipa_file or count_character or count_bigram:
        freq_lists = extend_data(freq_list_df, lang=lang, unit_name="Word", 
                      spell_check=spell_check, ipa_file=ipa_file, 
                      count_character=count_character, count_bigram=count_bigram,
                      stats=stats, progress_bar=progress_bar)
    else:
        freq_lists = {"word": freq_list_df}
    
    # Mark the data as extended if it has extended info like stop word
    if "Stop word" in freq_lists["word"].columns:
        freq_lists["word_extended"] = freq_lists["word"]
        del freq_lists["word"]

    return freq_lists
    