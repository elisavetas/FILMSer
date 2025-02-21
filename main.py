# -*- coding: utf-8 -*-
# Authors: Elizaveta Sineva, Sara Chilson
"""
The main file for running the code for gathering
the frequency information from the data.
"""

import argparse
import time

from create import create_new_list
from export_data import export_data

                                                 
from lang_abbr import ABBR2FULL, FULL2ABBR

NOT_IN_ASPELL = ['albanian', 'basque', 'georgian', 'icelandic', 'kazakh',
                 'norwegian', 'urdu']

ABBR2ASPELL = {'pt':    'pt_PT', 
               'pt_br': 'pt_BR'}



def main(file_path, lang="english", spell_check=False,
         ipa_file="", count_character=False, count_bigram=False, 
         output_type="txt|xlsx", output_dir="data/", stats=False,
         progress_bar=False):
    """
    Extract word frequencies for a given languages from raw data.
    
    Parameters
    ----------
    file_path : str
        The path to the raw data file.
    lang : str, optional
        The language of the data as a full name (e.g. "English", not 
            case-sensitive) or abbreviation (e.g. "en").
        The default is "english".
    spell_check : string, optional
        Provide the language abbreviation of the necessary Aspell dictionary 
            to filter the words using Aspell spell checker.
        You can find the Aspell spell checker at aspell.net as well as the
            dictionaries for different languages used here at 
            ftp.gnu.org/gnu/aspell/dict/0index.html.
    ipa_file : str, optional
        The path to the file(s) with the IPA information if the information 
        is to be added. Use | to add several files. 
        The default is "" (= no IPA).
    count_character : bool, optional
        Set to True if the information about word character frequency is to 
        be added. The default is False.
    count_bigram : bool, optional
        Set to True if the information about bigram frequency within a word
            is to be added. The default is False.
    output_type : str, optional
        The extension of the file to export the data into. 
        The available extensions: "txt","csv", "xlsx".
        To export data into more than one file type, use | to separate
           extensions.
         The default is "txt|xlsx".
    output_dir : TYPE, optional
        DESCRIPTION. The default is "data/".
    stats : bool, optional
        Set to True to have some statistical information about the corpus 
            printed out. The default is False.

    Returns
    -------
    None.

    """
    # Process language name
    lang = lang.lower()
    # If an abbreviation was used to identify the language in lang,
    # extract the full name
    if len(lang) == 2 or lang.startswith("pt_"):
        lang = ABBR2FULL[lang]
    lang_print = lang.capitalize().replace('_p', ' - P').replace('_b', ' - B')
    
    # Check if there is a spell checker for the chosen language
    if spell_check:
        assert lang not in NOT_IN_ASPELL, f"You have added the option of using a spell checker; however, there is no spell checker for {lang_print}"
        spell_check = FULL2ABBR[lang]
    
    # Print the chosen options
    print(f"Language: {lang_print}")
    print(f"Filter via Aspell: {'Yes' if spell_check else 'No'}")
    print(f"Add IPA: {'Yes' if ipa_file else 'No'}")
    print(f"Count the character frequency: {'Yes' if count_character else 'No'}")
    print(f"Count the bigram frequency: {'Yes' if count_bigram else 'No'}")
    print(f"Print out statistics: {'Yes' if stats else 'No'}")
    
    # Create a frequency list from the given data
    freq_lists = create_new_list(file_path, lang=lang, spell_check=spell_check, 
                                 ipa_file=ipa_file, count_character=count_character, 
                                 count_bigram=count_bigram, stats=stats, 
                                 progress_bar=progress_bar)
    
    # Write data into file(s)
    for data_type in freq_lists:
        freq_list_df = freq_lists[data_type]
        
        # Add the slash to the output directory if it was not provided
        if output_dir[-1] != "/":
            output_dir += "/"
        folder_name = f"{output_dir}{data_type}_freq/"
        
        # Create the name of the file
        file_name = folder_name + lang + f".{data_type}.freq"

        if spell_check:
            file_name += ".spell_checked"
        if ipa_file:
            file_name += ".ipa"
        
        # Write the data into file(s)
        export_data(freq_list_df, file_name, file_types=output_type)



if __name__ == "__main__":
    ### Run the code using arguments
    argdesc = "The script for extracting word frequencies from raw data."
    argparser = argparse.ArgumentParser(description=argdesc)

    argparser.add_argument("-f", "--file", type=str, required=True,
                            help="the path to the data file (required)")
    argparser.add_argument("-l", "--language", type=str, default="english",
                            help='the language of the data as a full name (e.g. "English", not case-sensitive) or abbreviation (e.g. "en"); default: english')    
    argparser.add_argument("-x", "--extension", type=str, default="txt|xlsx",
                            help="the extension of the file to export the data into (txt/xlsx/csv); use | for several data types; default: txt|xlsx")    
    argparser.add_argument("-a", "--aspell", default=False,
                            action=argparse.BooleanOptionalAction,
                            help="filter the words using the Aspell spell checker")
    argparser.add_argument("-i", "--ipa", type=str, default="",
                            help="the path to the file with the IPA information if the information is to be added; use | to add more than one file")
    argparser.add_argument("-c", "--character", default=False,
                            action=argparse.BooleanOptionalAction,
                            help="use to extract word character frequency information")
    argparser.add_argument("-b", "--bigram", default=False,
                            action=argparse.BooleanOptionalAction,
                            help="use to extract bigram frequency information (bigrams within a word)")
    argparser.add_argument("-s", "--stats", default=False,
                            action=argparse.BooleanOptionalAction,
                            help="use to print out statistics about the data")
    argparser.add_argument("-p", "--progress-bar", default=False,
                            action=argparse.BooleanOptionalAction,
                            help="use for a progress bar to be displayed (from alive-progress package)")
    
    args = argparser.parse_args()

    
    ### Run the script with the given arguments
    time_start = time.time()  # keep track of the time to report on the runtime
    
    data_file = args.file
    main(data_file, lang=args.language, spell_check=args.aspell, 
         ipa_file=args.ipa, count_character=args.character,
         count_bigram=args.bigram, stats=args.stats, 
         progress_bar=args.progress_bar)

    ### Run the script without using arguments
    # data_file = "opensubs/br.txt.gz"
    # main(data_file, count_character=False, count_bigram=False, 
    #      ipa_file="IPA/bre_latn_broad.tsv", stats=True)
    
    ### Calculate the runtime
    time_end = time.time()
    
    total_time = time_end - time_start
    
    time_hrs = int(total_time/60//60)
    time_min = int(total_time//60 - time_hrs*60)
    time_sec = "{:02d}".format(int(total_time - time_min*60 - time_hrs*60*60))
    
    time_min = "{:02d}".format(time_min)
    
    print(f"The total runtime is {time_hrs}:{time_min}:{time_sec}.")
    
    