# -*- coding: utf-8 -*-
"""
Extracts the given data.
Tokenizes the data according to the language.
Collects frequencies from the tokenized data.
"""

from ..file_processors.extract_data import extract_from_gz
from .count_freq import count_freq

from ..tokenizers.icu_tokenizer import icu_tokenizer
from ..tokenizers.spacy_tokenizer import load_pipeline, spacy_tokenizer
from ..tokenizers.regex_tokenizer import regex_tokenizer 


from ..tokenizers.icu_tokenizer import NON_WHITESPACE
from ..tokenizers.spacy_tokenizer import LANG2BIGSPACY



def collect_frequencies(data_path, lang="en", spacy_size="sm", 
                        count_character=False, count_bigram=False,
                        stats=False, progress_bar=False):
    """
    Collects frequencies from raw data in the provided data file.

    Parameters
    ----------
    data_path : str
        The path to the file with the raw data.
    lang : str, optional
        The language of the data as a full name (e.g. "English", not 
            case-sensitive) or abbreviation (e.g. "en").
        The default is "en".
    spacy_size : str, optional
        The size of the spacy model if spacy is used. 
        Options: sm (small), md (middle), lg (large), trf (transformer)
        The default is "sm" (small).
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
    freq_lists : dict of dicts {data type : frequency dictionary}
        Dictionary for each data type (word, word_extended, bigram, character)
            with a frequency dictionary

    """
    print("Extracting data...")
    # Extract the raw data from the file depending on its extension
    if data_path.endswith("gz"):
        data_lines = extract_from_gz(data_path)
    else:
        with open(data_path, encoding="utf-8") as f:
            data_lines = f.readlines()
    
    # Adapt the language name to find the right tokenizer
    # Use spacy's Chinese tokenizer for Cantonese
    lang_spacy = "zh" if lang == "yue" else lang
    lang_spacy = lang_spacy.split("_")[0]  # Only use the main part for checking

    if lang_spacy in LANG2BIGSPACY:
        print("Loading the spacy model...")
        # For spacy transformer models
        if spacy_size == "trf":
            # Get the largest spacy model in case trf isn't available for the language
            spacy_size = LANG2BIGSPACY[lang_spacy]
        pipeline = load_pipeline(lang=lang_spacy, pipe_size=spacy_size)
    
    all_tokens = []
    all_removed = set()

    def tokenize(line):
        """
        Helper function for tokenization.
        """
        nonlocal all_tokens
        if lang_spacy in LANG2BIGSPACY:  # Use spacy when possible
            tokens, removed = spacy_tokenizer(line, pipeline=pipeline,
                                              ling_info=True, stats=stats)
        elif lang in NON_WHITESPACE:
            tokens, removed = icu_tokenizer(line, lang=lang, stats=stats) 
        else:
            tokens, removed = regex_tokenizer(line, lang=lang, stats=stats)
        
        all_tokens += tokens
        all_removed.update(removed)


    print("Tokenizing the data...")
    if progress_bar:
        from alive_progress import alive_bar
        with alive_bar(len(data_lines), theme="scuba") as bar:
            # Tokenize the data
            for line in data_lines:
                tokenize(line)
                bar() # Show progress
    else:
        # Tokenize the data
        for line in data_lines:
            tokenize(line)
    
    if stats:
        print()
        print("The following characters have been removed:")
        print(all_removed)
        print()
        
    # Extract the frequencies for each word in the data
    freq_lists = count_freq(all_tokens, 
                            count_character=count_character,
                            count_bigram=count_bigram,
                            progress_bar=progress_bar)
    
    return freq_lists

