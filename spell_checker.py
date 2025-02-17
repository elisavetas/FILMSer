# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
Spell check a given word using Aspell.

You can find the Aspell spell checker at aspell.net as well as the dictionaries 
for different languages used here at ftp.gnu.org/gnu/aspell/dict/0index.html.

Version of Aspell used: 
    International Ispell Version 3.1.20 (but really Aspell 0.60.8.1)
"""
import subprocess



def run_aspell(word, lang="en"):
    """
    Runs the pipeline to check a word in the Aspell spell checker.

    Parameters
    ----------
    word : string
        The word to be checked by Aspell.
    lang : string, optional
        The abbreviation of the necessary language to be used in Aspell.
            The default is "en".

    Returns
    -------
    word_exists : bool
        Returns True if the word is in the Aspell dictionary for the given 
            language lang. Case-sensitive.

    """
    # Check for missing string
    if not word:
        return False
    
    
    # Pipeline for Aspell check
    echo_word = subprocess.run([f'echo "{word}"'], stdout=subprocess.PIPE, shell=True)
    aspell = subprocess.run([f'aspell -l {lang} -a'], input=echo_word.stdout, 
                           stdout=subprocess.PIPE, shell=True)
    
    # Decode the resulting output of the Aspell command
    res = aspell.stdout.decode()[70]
    
    # Words existing in the dictionary are marked by an asterisk *
    word_exists = True if res == "*" else False
    
    return word_exists


def check_aspell(word, lang="en"):
    """
    Checks if a word is spelled correctly based on a specific languages
    using Aspell spell checker.
    You can find the Aspell spell checker at aspell.net.

    Parameters
    ----------
    word : string
        The word to be checked by Aspell.
    lang : string, optional
        The abbreviation of the necessary language to be used in Aspell.
            The default is "en".

    Returns
    -------
    word_exist : bool
        Returns True if the word exists (= spelled correctly) in the Aspell 
            dictionary for the given language lang. Case-sensitive.

    """    
    # Check if the word exist in Aspell
    word_exists = run_aspell(word, lang=lang)
    
    # Aspell tends to not recognise contractions with apostrophes in front,
    # e.g. 'cause, 'bout, etc. --> In such cases, try the word without '
    if not word_exists and word.startswith("'"):
        # Run Aspell on the word without the asterisk
        word_exists = run_aspell(word[1:], lang=lang)
    
    return word_exists
    

def caseless_check(word, lang="en"):
    """
    Performs a word check in Aspell using the check_aspell functions, but
    ignores the case of the word (e.g. america will be accepted as a word
                                  despite not being capitalized).

    Parameters
    ----------
    word : string
        The word to be checked by Aspell.
    lang : string, optional
        The abbreviation of the necessary language to be used in Aspell.
            The default is "en".

    Returns
    -------
    word_exists : bool
        Returns True if the word exists (= spelled correctly, not checking 
            the case) in the Aspell dictionary for the given language lang.

    """
    # Check if lower-cased word exists
    word_exists = check_aspell(word.lower(), lang=lang)
    
    if not word_exists:
        # Check if capitalized word exists
        word_exists = check_aspell(word.capitalize(), lang=lang)
        
        if not word_exists:
            # Check if upper-cased word exists
            word_exists = check_aspell(word.upper(), lang=lang)
    
    return word_exists

