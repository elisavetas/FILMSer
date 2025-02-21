# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Updates a given frequency list with additional information.
"""

import math

import pandas as pd

from count_ngram import count_ngram
from create import create_new_list
from spell_checker import caseless_check
from extract_ipa import extract_ipa


from lang_abbr import FULL2ABBR



def upd_exist_list(freq_list_path, lang="english", add_data_file="", 
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
    spell_check : string, optional
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
    freq_lists : dict of pandas DataFrames
        Contains DataFrames for different types of data (word, character, bigram).
        Form {data type name : DataFrame}

    """
    
    # Extract the frequency data from the file depending on its extension
    if freq_list_path.endswith("xlsx"):
        freq_list_df = pd.read_excel(freq_list_path, converters={'Word' : str})
    else:
        freq_list_df = pd.read_table(freq_list_path, converters={'Word' : str})
    
    freq_lists = {}
    
    # New word information
    if add_data_file or spell_check or ipa_file:
        freq_lists["word"] = freq_list_df
    # Character frequencies
    if count_character:
        freq_lists["character"] = {}
    # Bigram frequencies
    if count_bigram:
        freq_lists["bigram"] = {}
    
    
    def calc(row):
        """
        Helper function for calculating frequency per million and 
        Zipf values.
        """
        nonlocal prev_freq, rank
        freq = row[1]["Frequency"]
        
        # Update rank
        if freq != prev_freq:
            # If the frequency of the current word is different from the
            # previous, increase its rank
            rank += 1
            prev_freq = freq
            
        freq_df.loc[row[0], "Rank"] = rank
    
        # Calculate frequency per million
        freq_mil = round(10**6 * freq / total_units, 4)
        freq_df.loc[row[0], "Frequency per million"] = freq_mil
        
        # Calculate Zipf value
        zipf_val = round(math.log10(freq_mil)+3, 4)
        freq_df.loc[row[0], "Zipf value"] = zipf_val
    
     
    # Add information from a new file
    if add_data_file:
        new_df = create_new_list(add_data_file, lang=lang, stats=stats, 
                                 progress_bar=progress_bar)["word"]
        
        
        def merge(row):
            """
            Helper function for merging the rows of two frequency lists.
            """
            nonlocal freq_lists
            main_df = freq_lists["word"]
            
            word = row[1]["Word"]
            word_freq = row[1]["Frequency"]
            
            # If the word exists in the previous list, add the frequencies
            if (main_df["Word"] == word).any():
                main_row = main_df.loc[main_df["Word"] == word]
                main_row_freq = main_row.iloc[0]["Frequency"]
                main_df.loc[main_df["Word"] == word, "Frequency"] = main_row_freq + word_freq
                
            # If the word didn't exist in the list already, add it to the list
            else:
                freq_lists["word"] = pd.concat([main_df, row[1].to_frame().T], ignore_index=True)
            
            
        # Progress bar
        if progress_bar:
            from alive_progress import alive_bar
            print("Updating the frequency list with new frequency information...")
            with alive_bar(new_df.shape[0], theme="scuba") as bar:
                # Merge with existing frequency list
                for row in new_df.iterrows():
                    merge(row)
                    bar() # Show progress
        else:
            # Merge with existing frequency list
            for row in new_df.iterrows():
                merge(row)
        
        freq_lists["word"].sort_values(by=["Frequency", "Word"], 
                                       ascending=[False,True], inplace=True)
        
        # Re-calculate
        freq_df = freq_lists["word"]
        total_units = freq_df["Frequency"].sum()

        rank = 0
        prev_freq = 0
        
        # Progress bar
        if progress_bar:
            from alive_progress import alive_bar
            print("Re-calculating values for new data...")
            with alive_bar(freq_df.shape[0], theme="scuba") as bar:
                # Update the information
                for row in freq_df.iterrows():
                    calc(row)
                    bar() # Show progress
        else:
            for row in freq_df.iterrows():
                calc(row)
        
    
    if ipa_file:
        freq_lists["word"]["IPA"] = None
        # Extract the IPA information
        ipa_dict = extract_ipa(ipa_file)
    
    
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
    
    def process_row(row):
        """
        Helper function for processong a word in a given row and
        updating necessary information.
        """        
        word = row[1]["Word"]
        word_freq = row[1]["Frequency"]
        
        # Filter using a spell checker
        if spell_check:
            zipf = row[1]["Zipf value"]
            
            # Don't filter out high frequency words
            if zipf < 4.5:
                word_exists = caseless_check(word, lang=FULL2ABBR[lang])
                
                # Remove the word if the spell checker does not recognise it
                if not word_exists:
                    freq_lists["word"].drop([row[0]], inplace=True)
                    return
        
        # Add IPA information
        if ipa_file:
            ipa_info = None
            
            if word in ipa_dict:
                ipa_info = ipa_dict[word]
            elif "ß" in word:
                # Rewrite ß as ss to search for IPA
                # to account for German spelling versions
                ssword = word.replace("ß", "ss")
                if ssword in ipa_dict:
                    ipa_info = ipa_dict[ssword]
            
            # If the ipa info is available, include the word
            if ipa_info:
                freq_lists["word"].loc[row[0], "IPA"] = ipa_info
            # If the ipa info isn't available, exclude the word
            else:
                freq_lists["word"].drop([row[0]], inplace=True)
                return
        
        # Generate character frequencies
        if count_character:
            char_freqs = count_ngram(word, n=1, ngram_freq={})
            update_dict("character", char_freqs, word_freq)
        
        # Generate bigram frequencies
        if count_bigram:
            bigram_freqs = count_ngram(word, n=2, ngram_freq={})
            update_dict("bigram", bigram_freqs, word_freq)
    
    
    # Progress bar
    if progress_bar:
        from alive_progress import alive_bar
        print("Adding new information...")
        with alive_bar(freq_lists.get("word", freq_list_df).shape[0], theme="scuba") as bar:
            for row in freq_lists.get("word", freq_list_df).iterrows():
                process_row(row)
                bar() # Show progress
    else:
        for row in freq_lists.get("word", freq_list_df).iterrows():
            process_row(row)


    # (Re-)calculate rank, frequency per million and Zipf value
    for data_type in freq_lists:
        if data_type != "word":
            freq_lists[data_type] = pd.DataFrame(
                        {"Rank": None, data_type.capitalize(): freq_lists[data_type].keys(), 
                         "Frequency": freq_lists[data_type].values(), 
                         "Frequency per million": None, "Zipf value": None})
            freq_lists[data_type].sort_values(by=["Frequency", data_type.capitalize()], 
                                              ascending=[False,True],
                                              inplace=True)
        # Don't update values if the list wasn't filtered via Aspell
        elif not spell_check:
            continue

        
        freq_df = freq_lists[data_type]
        total_units = freq_df["Frequency"].sum()

        rank = 0
        prev_freq = 0


        # Progress bar
        if progress_bar:
            from alive_progress import alive_bar
            if data_type == "word":
                print("Re-calculating values for filtered frequencies...")
            else:
                print(f"Calculating values for {data_type}s")
            with alive_bar(freq_df.shape[0], theme="scuba") as bar:
                # Update the information
                for row in freq_df.iterrows():
                    calc(row)
                    bar() # Show progress
        else:
            for row in freq_df.iterrows():
                calc(row)

    return freq_lists
    