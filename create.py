# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Creates frequency list(s) from the given data.
"""

from count_freq import count_freq
from extract_data import extract_from_gz
from order_data import order_data

from lang_abbr import FULL2ABBR



def create_new_list(data_path, lang="english", spell_check=False, ipa_file="", 
                    count_character=False, count_bigram=False, stats=False,
                    progress_bar=False):
    
    # Extract the raw data from the file depending on its extension
    if data_path.endswith("gz"):
        data_lines = extract_from_gz(data_path)
    else:
        with open(data_path) as f:
            data_lines = f.readlines()
    
    # Extract the frequencies for each word in the data
    word_freq, character_freq, bigram_freq = count_freq(data_lines, 
                                                count_character=count_character,
                                                count_bigram=count_bigram,
                                                stats=stats, progress_bar=progress_bar)

    freq_lists = {"word": word_freq}
    
    if count_character:
        freq_lists["character"] = character_freq
        
    if count_bigram:
        freq_lists["bigram"] = bigram_freq
        
        
    for data_type in freq_lists:
        spell_filter = FULL2ABBR[lang] if spell_check and data_type == "word" else False
        ipa_info = ipa_file if data_type == "word" else ""
        
        # Organize the data into a dateframe
        ordered_freq = order_data(freq_lists[data_type], ipa_file=ipa_info, 
                                  unit_name=data_type.capitalize(),
                                  spell_check=spell_filter, stats=stats,
                                  progress_bar=progress_bar)
        
        # Replace the dictionary with a cleaned up dataframe
        freq_lists[data_type] = ordered_freq
    
    return freq_lists
    
    