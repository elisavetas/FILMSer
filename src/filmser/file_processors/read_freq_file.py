# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""Reads frequency list files produced by FILMSer."""

from typing import Union
from pathlib import Path

import pandas as pd


def read_frequency_file(file_path: Union[str, Path]) -> dict:
    """
    Read frequency list from xlsx or tab-separated file 
        produced by FILMSer.

    Parameters
    ----------
    file_path : str or Path
        Path to the frequency list file.

    Returns
    -------
    dict
        Dictionary containing the frequency list categorized by data type.
    """
    # Get the correct function to read the file based on its extension
    read_func = None
    if str(file_path).endswith("xlsx"):
        read_func = pd.read_excel
    else:
        read_func = pd.read_table

    freq_lst = read_func(file_path, converters={'Word': str}, keep_default_na=False)
    
    if freq_lst.empty:
        raise ValueError("The frequency list file is empty or could not be read.")
    
    if len(freq_lst.columns) == 1:
        raise ValueError("The frequency list file appears to have only one column. "
                         "Please check the file format and delimiters.")

    # Find the data type based on the columns present in the DataFrame
    data_type = None
    for col_name in ["Word", "Character", "Bigram", "Trigram"]:
        if col_name in freq_lst.columns:
            data_type = col_name.lower()
            break

    # Check if the file contains linguistic information
    if data_type == "word":
        if "Stop word" in freq_lst.columns:
            data_type = "word_extended"

    elif data_type is None:
        for col_name in freq_lst.columns:
            if "gram" in col_name.lower():
                data_type = col_name.lower()
                break
        if data_type is None:
            data_type = "word"

    freq_lists = {data_type: freq_lst}

    return freq_lists