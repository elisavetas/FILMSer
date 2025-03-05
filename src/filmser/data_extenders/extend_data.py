# -*- coding: utf-8 -*-
"""
Adds necessary information to the given frequencies.
"""

import math

import pandas as pd

from .spell_checker import caseless_check 
from .extract_ipa import extract_ipa
from ..freq_counters.count_ngram import count_ngram


from ..iso2lang import FULL2ISO



def extend_data(freq_df, lang="en", unit_name="Word", spell_check=False, 
               ipa_file="", count_character=False, count_bigram=False,
               stats=False, progress_bar=False):
    """
    Adds additional information to an existing frequency list.

    Parameters
    ----------
    freq_df : pandas DataFrame
        A dataframe containg frequency information.
    lang : str, optional
        The language of the data. The default is "en".
    unit_name : str, optional
        The unit, for which the frequency was measured, as a title 
            ("Word", "Bigram", "Character"). The default is "Word".
    spell_check : bool, optional
        Set to True to filter the words using Aspell spell checker. It is 
            important to set the lang value correct for the correct dictionary
            to be used. The default is False.
        You can find the Aspell spell checker at aspell.net as well as the
            dictionaries for different languages used here at 
            ftp.gnu.org/gnu/aspell/dict/0index.html.
    ipa_file : str, optional
        Provide the path to the file(s) with the IPA information if the information 
        is to be added. Provide a list of files to add several of them. 
        Expected data format:
                "word \tab IPA" per line.
        The default is "".
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
    freq_lists : dict {unit name : pandas DataFrame}
        A dictionary contaning DataFrames with word (, bigram, character) 
            frequencies and new information added.

    """
    # Get the ISO code of the language if the full name is provided
    if lang in FULL2ISO:
        lang = FULL2ISO[lang]
    
    if progress_bar:
        from alive_progress import alive_bar
    
    # Initialize counters for word statistics
    if stats and unit_name == "Word":
            token_len = 0
            type_len = 0

    freq_lists = {unit_name.lower(): freq_df}
    
    # Character frequencies
    if count_character and unit_name == "Word":
        freq_lists["character"] = {}
    # Bigram frequencies
    if count_bigram and unit_name == "Word":
        freq_lists["bigram"] = {}
    
    
    if ipa_file and unit_name == "Word":
        if "IPA" not in freq_lists[unit_name.lower()].columns:
            freq_lists[unit_name.lower()]["IPA"] = None
        # Extract the IPA information
        ipa_dict = extract_ipa(ipa_file)


    total_units = freq_df["Frequency"].sum()

    
    def update_dict(data_type, ngram_freqs, word_freq):
        """
        Updates the frequency dictionary with new n-gram frequency information 
        within the function. Takes into account the word frequency.
        """
        for ngram, ngram_freq in ngram_freqs.items():
            freq_lists[data_type].setdefault(ngram, 0)
            # Multiply the ngram frequency within a word by 
            # thetotal word frequency
            freq_lists[data_type][ngram] += ngram_freq*word_freq
    
    def add_ngrams(row):
        """
        Helper function for processong a word in a given row and
        updating necessary information.
        """
        unit = row[1][unit_name]
        unit_freq = row[1]["Frequency"]
        
        # Generate character frequencies
        if count_character:
            char_freqs = count_ngram(unit, n=1, ngram_freq={})
            update_dict("character", char_freqs, unit_freq)
        
        # Generate bigram frequencies
        if count_bigram:
            bigram_freqs = count_ngram(unit, n=2, ngram_freq={})
            update_dict("bigram", bigram_freqs, unit_freq)

    
    if ipa_file and unit_name == "Word":
        print("Adding IPA...")
        if lang == "de":
            freq_lists["word"]["IPA"] = freq_df.apply(lambda row: ipa_dict.get(row["Word"], ipa_dict.get(row["Word"].replace("ß", "ss"), None)), axis=1)
        else:
            freq_lists["word"]["IPA"] = freq_df.apply(lambda row: ipa_dict.get(row["Word"], None), axis=1)
    
    if spell_check and unit_name == "Word":
        
        if "Frequency per million" not in freq_df.columns:
            freq_df["Frequency per million"] = freq_df["Frequency"].apply(lambda freq: round(10**6 * freq / total_units, 4)) 
            freq_df["Zipf value"] = freq_df["Frequency per million"].apply(lambda freq_mil: round(math.log10(freq_mil)+3, 4))
        
        print("Spell-checking...")
        freq_df = freq_lists["word"]
        
        if "IPA" in freq_lists["word"].columns:
            freq_df["Aspell"] = freq_df.apply(lambda row: caseless_check(row["Word"], lang=lang) if row["Zipf value"] < 4.5 and pd.isna(row["IPA"]) else True, axis=1)
        else:
            freq_df["Aspell"] = freq_df.apply(lambda row: caseless_check(row["Word"], lang=lang) if row["Zipf value"] < 4.5 else True, axis=1)
       
        freq_lists["word"] = freq_df.loc[freq_df["Aspell"] == True]
        freq_lists["word"] = freq_lists["word"].drop(columns=['Aspell'])


    # Go into the add info loop if there is info to add
    if (count_character or count_bigram) and unit_name == "Word":
        freq_df = freq_lists[unit_name.lower()]
        
        print("Adding n-gram information...")
        if progress_bar:
            with alive_bar(freq_lists[unit_name.lower()].shape[0], theme="scuba") as bar:
                for row in freq_lists[unit_name.lower()].iterrows():
                    add_ngrams(row)
                    bar() # Show progress
        else:
            for row in freq_lists[unit_name.lower()].iterrows():
                add_ngrams(row)

    # (Re-)calculate rank, frequency per million and Zipf value
    for data_type, freq_list in freq_lists.items():
        
        if type(freq_list) != pd.DataFrame:
            freq_lists[data_type] = pd.DataFrame(
                        {data_type.capitalize(): freq_lists[data_type].keys(), 
                         "Frequency": freq_lists[data_type].values()})

        # Calculate word information for statistics
        if stats and data_type ==  "word":
            
            # Get total units / tokens and types
            total_units = freq_df["Frequency"].sum()
            total_types = freq_df.shape[0]
            
            # token_len = freq_df["Word"].apply(lambda word: len(word)*word.Frequency).sum()
            token_len = freq_df[["Word", "Frequency"]].apply(lambda row: len(row["Word"])*row["Frequency"], axis=1).sum()
            type_len = freq_df["Word"].apply(lambda word: len(word)).sum()
        
        # Print out the statistics
        if stats:
            corpus_size = "raw" if not spell_check else "filtered (spell-checked)"
            corpus_size += ", extended" if "PoS (simple)" in freq_df else ""
            
            print()
            print(f"The total number of {unit_name.lower()}s in the {corpus_size} corpus is {total_units}.")
            print(f"The total number of {unit_name.lower()} types in the {corpus_size} corpus is {total_types}.")
            
            if data_type == "word":
                token_len_av = round(token_len/total_units, 2)
                type_len_av = round(type_len/total_types, 2)
                print()
                print(f"The average word length within the {corpus_size} corpus text is {token_len_av}.")
                print(f"The average unique word length within the {corpus_size} corpus {type_len_av}.")
    
                if "IPA" in freq_lists[data_type].columns:
                    ipa_count = freq_lists[data_type]['IPA'].count()
                    print(f"The IPA transcription is provided for {ipa_count} {unit_name.lower()}s in the {corpus_size} corpus.")
            print()


    return freq_lists

