# -*- coding: utf-8 -*-
# Author: Elizaveta Sineva
"""
Tokenizer that uses spaCy models for tokenization. 
This module provides functions to load spaCy pipelines and perform tokenization 
    with optional linguistic information and statistics collection.
"""

import gc
import os

from typing import Tuple, List, Set, Union
from functools import lru_cache

from .clean_noise import clean_noise

from ..config import SIZE2SPACY, SPACY_LANG, LANG2SPACYLANG

FALLBACK_ORDER = ["trf", "lg", "md", "sm"]

# Cache for loaded pipelines
_PIPELINE_CACHE = {}
# Store original CUDA_VISIBLE_DEVICES for restoration
_ORIGINAL_CUDA_VISIBLE_DEVICES = os.environ.get("CUDA_VISIBLE_DEVICES")


@lru_cache(maxsize=8)
def _get_pipeline_key(lang: str, pipe_size: str, ling_info: bool) -> str:
    """Generate cache key for pipeline."""
    return f"{lang}_{pipe_size}_{ling_info}"


def load_pipeline(lang: str = "en", pipe_size: str = "sm", ling_info: bool = False):
    """
    Load a spaCy pipeline for the specified language and model size, with optional linguistic information.
    
    This function attempts to load the requested spaCy model, falling back to smaller models if necessary.
    The loaded pipeline is cached for future use.
    
    Parameters
    ----------
    lang : str, optional
        The language of the necessary spacy model. The default is "en".
    pipe_size : str, optional
        The size of the necessary spacy model. 
        Options: sm (small), md (middle), lg (large), trf (transformer)
        The default is "sm" (small).
    ling_info : bool, optional
        Whether to include linguistic information (i.e. lemma, POS tags, morphological information) in the pipeline.
        The default is False.

    Returns
    -------
    spacy_pipe : spacy pipeline
        A loaded spacy pipeline for the provided / default model.
    """
    # Lazy import spaCy to avoid triggering torch/CUDA initialization unnecessarily
    from spacy import load as load_pipe
    from spacy.cli import download as download_pipe
    from spacy.util import is_package, compile_infix_regex
    
    # Convert to the correct size name if necessary
    pipe_size = SIZE2SPACY.get(pipe_size, pipe_size)
    lang = LANG2SPACYLANG.get(lang, lang).split("_")[0]  # Use only the first part of the language code

    if lang not in SPACY_LANG:
        # Use multilingual model for 'xx' language code
        lang = "xx"
        pipe_size = "sm"

    # Build the fallback chain starting from requested size
    sizes = FALLBACK_ORDER[FALLBACK_ORDER.index(pipe_size):] if pipe_size in FALLBACK_ORDER else [pipe_size]
    
    pipe_genre = "web" if lang in ["en", "zh"] else "news"  # According to spaCy's model naming conventions
    
    # Disable all components except tokenizer if linguistic info not needed
    if ling_info:
        disable_pipes = ["ner", "parser", "textcat", "senter"]
    else:
        disable_pipes = ["tagger", "parser", "ner", "lemmatizer", "textcat", "morphologizer", "attribute_ruler", "senter"]

    for size in sizes:
        # Get the cached pipeline if it exists
        cache_key = _get_pipeline_key(lang, size, ling_info)
        if cache_key in _PIPELINE_CACHE:
            return _PIPELINE_CACHE[cache_key]

        pipe_name = f"{lang}_core_{pipe_genre}_{size}" if lang != "xx" else f"xx_ent_wiki_sm"

        # Download if published and not present
        if not is_package(pipe_name):
            try:
                download_pipe(pipe_name)
            except SystemExit:
                # Download failed (model doesn't exist), try next size
                continue

        spacy_pipe = load_pipe(pipe_name, disable=disable_pipes)
        
        if size != pipe_size:
            print(f"Warning: Requested spaCy model size '{pipe_size}' not found for language '{lang}'. "
                  f"Using '{size}' model instead.")

        # Handle hyphenated words - no splitting on hyphens
        infix_patterns = list(spacy_pipe.Defaults.infixes)
        infix_patterns = [p for p in infix_patterns if "-|" not in p]
        infix_re = compile_infix_regex(infix_patterns)
        spacy_pipe.tokenizer.infix_finditer = infix_re.finditer

        spacy_pipe._filmser_cache_key = cache_key
        spacy_pipe._filmser_package_name = pipe_name

        _PIPELINE_CACHE[cache_key] = spacy_pipe
        return spacy_pipe

    raise OSError(f"No spaCy model published for {lang} in sizes {sizes}")


def unload_pipeline(pipeline=None):
    """Remove a loaded pipeline from the cache and release its memory."""
    if pipeline is None:
        return

    cache_key = getattr(pipeline, "_filmser_cache_key", None)
    if cache_key is not None:
        _PIPELINE_CACHE.pop(cache_key, None)

    del pipeline
    gc.collect() # Release memory


def spacy_tokenizer(text: str, lang: str = "en", pipe_size: str = "sm", 
                    pipeline = None, ling_info: bool = False, 
                    stats: bool = False) -> Tuple[List[Union[str, Tuple]], Set[str]]:
    """
    A tokenizer that uses a spaCy model as basis for the tokenization.

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
        The default is False.
        The information will include (if applicable to the language):
            - Lemma
            - Part of speech tags (UPOS and language-specific) 
            - Morphological information
            - If the given token is a stop word
    stats : bool, optional
        Set to True to have some statistical information about the data 
            be collected. The default is False.

    Returns
    -------
    tokens : list of strings
        A list of cleaned-up tokens from the text.
    removed : set
        A set of removed characters.

    """
    # Load the necessary pipeline if one wasn't provided    
    if not pipeline:
        pipeline = load_pipeline(lang=lang, pipe_size=pipe_size, ling_info=ling_info)

    processed = pipeline(text)
    tokens = []
    
    # Keep track of deleted characters
    removed = set()

    for token in processed:
        token_text = token.text.lower()
        
        # Clean noisy characters from the token if possible
        if not token_text.isalpha():
            token_text, removed_chars = clean_noise(token_text, lang=lang, stats=stats)
            if stats:
                removed.update(removed_chars)
            if not token_text:
                continue
        
        if ling_info:
            final_tok = (token_text, token.lemma_.lower(), token.pos_, 
                        token.tag_, str(token.morph), token.is_stop)
        else:
            final_tok = token_text
        
        tokens.append(final_tok)
        
    return tokens, removed
