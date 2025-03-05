# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Function to add additional frequency values and sort the frequency list.
"""

import math


def add_freq_measures(freq_df, data_type):
    """
    Sorts a frequency list by frequency first, alphabetically second.
    Adds rank, frequency per million and Zipf value to the list.

    Parameters
    ----------
    freq_df : pandas DataFrame
        A frequency list as a dtaframe with columns [capitalized data_type]
            and "Frequency"
    data_type : str
        The type of data for which the values are calculated, 
            e.g. word, character, bigram.

    Returns
    -------
    freq_df : pandas DataFrame
        A frequency list with all new information added, 
        sorted by frequency, then alphabetically.

    """
    freq_df.sort_values(by=["Frequency", data_type.capitalize()], 
                                         ascending=[False,True],
                                         inplace=True)
        
    total_units = freq_df["Frequency"].sum()
    
    print(f"Calculating rank for {data_type}s...")
    freq_df['Rank'] = freq_df["Frequency"].rank(method="dense", ascending=False).astype(int)
    
    print(f"Calculating frequency per million for {data_type}s...")
    freq_df["Frequency per million"] = freq_df["Frequency"].apply(lambda freq: round(10**6 * freq / total_units, 4))
    
    print(f"Calculating Zipf value for {data_type}s...")
    freq_df["Zipf value"] = freq_df["Frequency per million"].apply(lambda freq_mil: round(math.log10(freq_mil)+3, 4)) 
    
    return freq_df