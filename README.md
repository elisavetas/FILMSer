# Word <ins>F</ins>requency <ins>I</ins>PA <ins>M</ins>ulti<ins>L</ins>ingual <ins>S</ins>ubtitles Corpus (FILMS Corpus)

Word <ins>F</ins>requency <ins>I</ins>PA <ins>M</ins>ulti<ins>L</ins>ingual <ins>S</ins>ubtitles Corpus (FILMS Corpus) is a frequency corpus based on the movie subtitles data taken from [OpenSubtitles corpus](https://opus.nlpl.eu/OpenSubtitles/corpus/version/OpenSubtitles) (v2024).
FILMS includes a full length version of all frequency count, as well as a smaller subset of the data contianing only words for which IPA transcriptions were avaliabe in Wikipedia [Wikipron corpus](https://github.com/CUNY-CL/wikipron/tree/master/data/scrape/tsv).

A preprint of the paper can be found on OSF Preprints.  
https://doi.org/10.31219/osf.io/zy5qf

Sara Chilson, Elizaveta Sineva, Xenia Schmalz (2024). 

## Data

The corpus contain frequency data in `txt` and Excel (`xlsx`) formats:
- Old version: 52 languages, OpenSubtitles corpus v2018
- New version: 90 languages, OpenSubtitles corpus v2024

The data can be found in [OSF](https://osf.io/rd7p6/).

## Code

Run [`main.py`](https://github.com/sarachilson/FILMS-Corpus/blob/main/main.py) as a package to produce frequency file(s). When running outside of the `src` directory:
```
python -m src.filmser.main -f /path/to/file/
```

`main.py` takes the following arguments that allow you to modify the frequency data output:

| Argument | Full argument name | Description |
| --- | --- | --- |
| `-h` | `--help` | List available arguments. |
| `-f FILE` | `--file FILE` | The path to the raw data file (when creating a new frequency list) / an existing frequency list file (when using update mode to update the file with necessary information) (required). |
| `-u` | `--update` | Use to update the provided frequency list with new information. |
| `-n NEW_DATA` | `--new-data NEW_DATA` | The path to a raw data file to calculate new frequency information from and add it to an already existing frequency list. Only works in update mode. The default is "" (no data to be added). |
| `-l LANGUAGE` | `--language LANGUAGE` | The language of the data as a full name (e.g. "English", not case-sensitive) or abbreviation (e.g. "en"). Note that it is especially important to provide the correct language when using Aspell. Default: "english". |
| `-x EXTENSION [EXTENSION ...]` | `--extension EXTENSION [EXTENSION ...]` | The extension of the file to export the data into (`txt` (tab-separated)/`xlsx`/`csv`/`tsv`). You can provide several data types (default: `txt xlsx`). |
|  | `--spacy-size SPACY_SIZE` | Set the size of the spacy model used (if used) for tokenization. Options: "sm" (small), "md" (middle), "lg" (large), "trf" (transformer). The default is "sm" (small). |
| `-a` | `--aspell` | Use to filter the words via the [Aspell](http://aspell.net/) spell checker. |
| `-i IPA [IPA ...]` | `--ipa IPA [IPA ...]` | The path to the file with the IPA information if the information is to be added. You can provide more than one file. The IPA information will only be added to the data if the directory is provided. |
| `-c` | `--character` | Use to extract word character frequency information. |
| `-b` | `--bigram` | Use to extract bigram frequency information. |
| `-s` | `--stats` | Use to print out statistics about the data. |
| `-p` | `--progress-bar` | Use for a progress bar to be displayed (from [alive-progress](https://github.com/rsalmei/alive-progress/) package). |
| `-d OUTPUT_DIRECTORY` | `--output-directory OUTPUT_DIRECTORY` | The path to the directory where the created / updated frequency list should be saved. The default is "data/". |

_Usage_ _example_: 
If you would like to get the frequency data for German with IPA only in Excel format and have the statistics information printed out as well as a progress bar to be displayed, you can run the following in the command line:

```
python -m src.filmser.main -f PathToFile -x xlsx --ipa PathToIPAFile --stats -p
```
