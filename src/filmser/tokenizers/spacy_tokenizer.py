# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Spacy tokenizer.
"""

import spacy

from .clean_noise import clean_noise


SIZE2SPACY = {"small": "sm", 
              "middle": "md", 
              "large": "lg",
              "transformer": "trf",
              "big": "lg",
              "transformers": "trf"}

LANG2BIGSPACY = {"ca": "trf",
                 "da": "trf",
                 "de": "trf",
                 "el": "lg",
                 "en": "trf",
                 "es": "trf",
                 "fi": "lg",
                 "fr": "trf",
                 "hr": "lg",
                 "it": "lg",
                 "ja": "trf",
                 "ko": "lg",
                 "lt": "lg",
                 "mk": "lg",
                 "nb": "lg",
                 "nl": "lg",
                 "pl": "lg",
                 "pt": "lg",
                 "ro": "lg",
                 "ru": "lg",
                 "sl": "trf",
                 "sv": "lg",
                 "uk": "trf",
                 "zh": "trf"}



def load_pipeline(lang="en", pipe_size="sm"):
    """
    Loads a spacy pipeline.

    Parameters
    ----------
    lang : str, optional
        The language of the necessary spacy model. The default is "en".
    pipe_size : str, optional
        The size of the necessary spacy model. 
        Options: sm (small), md (middle), lg (large), trf (transformer)
        The default is "sm" (small).
        
    Returns
    -------
    spacy_pipe : spacy pipeline
        A loaded spacy pipeline for the provided / default model.

    """
    # Convert to the correct size name if necessary
    if len(pipe_size) > 3 or pipe_size == "big":
        pipe_size = SIZE2SPACY[pipe_size]
    
    # For spacy transformer models
    if pipe_size == "trf":
        # Get the largest spacy model in case trf isn't available for the language
        pipe_size = LANG2BIGSPACY[pipe_size]
        

    pipe_genre = "web" if lang in ["en", "zh"] else "news"
    pipe_name = f"{lang}_core_{pipe_genre}_{pipe_size}"
    
    disable_pipes=["ner", "parser", "textcat"]
    
    # Install necessary model if it's not been installed
    try:
        spacy_pipe = spacy.load(pipe_name, disable=disable_pipes)
    except OSError:
        print(f"{pipe_name} not found. Downloading now...")
        spacy.cli.download(pipe_name)
        spacy_pipe = spacy.load(pipe_name, disable=disable_pipes)
    
    # Handle hyphenated words
    # Get existing infix patterns
    infix_patterns = list(spacy_pipe.Defaults.infixes) 
    
    # Remove the rule that splits on hyphens
    infix_patterns = [p for p in infix_patterns if "-|" not in p]
    
    # Compile the modified patterns
    infix_re = spacy.util.compile_infix_regex(infix_patterns)
    
    # Update the infix rules within the tokenizer
    spacy_pipe.tokenizer.infix_finditer = infix_re.finditer
        
    return spacy_pipe



def spacy_tokenizer(text, lang="en", pipe_size="sm", pipeline=None,
                    ling_info=True, stats=False):
    """
    A tokenizer that uses teh spacy model as basis for the tokenization.

    Parameters
    ----------
    text : str
        A string of text to be tokenized.
    lang : str, optional
        The language of the necessary spacy model. The default is "en".
    pipe_size : str, optional
        The size of the spacy model to be used if the pipeline is to be loaded. 
        Options: sm (small), md (middle), lg (large), trf (transformer)
        The default is "sm" (small).
    pipeline : spacy pipeline, optional
        A loaded spacy pipeline to be used. If None, a pipeline will be loaded
            according to the lang and pipe_size. The default is None.
    ling_info : bool, optional
        Set to True if the linguistic information is to be added.
        Spacy page: https://spacy.io/usage/spacy-101#annotations
        The default is True.
        The information will include (if applicable to the language):
            - Lemma
            - Part of speeach tags (simple and detailed) 
            - Morphological information
            - If the given token is a stop word
    stats : bool, optional
        Set to True to have some statistical information about the corpus 
            be collected. The default is False.

    Returns
    -------
    tokens : list of strings
        A list of cleaned-up tokens from the line.
    removed : set
        A set of removed characters.

    """
    # Load the necessary pipeline if one wasn't provided    
    if not pipeline:
        pipeline = load_pipeline(lang=lang, pipe_size=pipe_size)
    
    processed = pipeline(text)
    tokens = []
    
    # Keep track of deleted characters
    removed = set()
    
    for token in processed:
        token_text = token.text.lower()
        
        # Clean noisy chracters from the token if possible
        if (not token_text.isalpha()):
            token_text, removed = clean_noise(token_text, lang=lang, stats=stats)
            if not token_text:
                continue
        
        if ling_info:
            final_tok = (token_text, token.lemma_.lower(), token.pos_, token.tag_, str(token.morph), token.is_stop)
        else:
            final_tok = token_text
        
        tokens.append(final_tok)
        
    return tokens, removed

