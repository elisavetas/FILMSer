# Word <ins>F</ins>requency <ins>I</ins>PA <ins>M</ins>ulti<ins>L</ins>ingual <ins>S</ins>ubtitles Corpus (FILMS Corpus)

Word <ins>F</ins>requency <ins>I</ins>PA <ins>M</ins>ulti<ins>L</ins>ingual <ins>S</ins>ubtitles Corpus (FILMS Corpus) is a frequency corpus based on the movie subtitles data taken from [OpenSubtitles corpus](https://opus.nlpl.eu/OpenSubtitles/corpus/version/OpenSubtitles) (v2018).
FILMS includes a full length version of all frequency count, as well as a smaller subset of the data contianing only words for which IPA transcriptions were avaliabe in Wikipedia [Wikipron corpus](https://github.com/CUNY-CL/wikipron/tree/master/data/scrape/tsv).

Sara Chilson, Elizaveta Sineva, Xenia Schmalz (2024). 

## Data

The corpus contain frequency data for 52 languages in `txt` and Excel (`xlsx`) formats. Note that for languages that have more than 100k unique words, the Excel version is reduced to the top 100k. You can see the full version in the corresponding `txt` file. All `txt` files are tab separated.  

The data is organised into three main directories in the following way:

* [`data/word_freq`](https://github.com/sarachilson/FILMS-Corpus/tree/main/data/word_freq): contians four files for each language in the corpus. 

1) txt file of the full-length unfiltered version (named `[language name].word.freq.txt`)
2) txt file of the IPA filtered data (named `[language name].word.freq.ipa.txt`)
3) excel file of the full-length unfiltered version (named `[language name].word.freq.xlsx`)
4) excel file of the IPA filtered data  (named `[language name].word.freq.ipa.xlsx`)

* [`data/character_freq`](https://github.com/sarachilson/FILMS-Corpus/tree/main/data/character_freq): the word character frequencies for all languages (named `[language name].character.freq`) both as a `txt` file and as a `xlsx` file
* [`data/bigram_freq`](https://github.com/sarachilson/FILMS-Corpus/tree/main/data/bigram_freq): the bigram frequencies for all languages (named `[language name].bigram.freq`). Note that the bigrams were extracted from within the word and not from within the sentence.

The files contain the frequency rank, the raw frequency, the frequency per million and the Zipf value of each word, as well as their IPA transcription in the IPA files. 
Note that different IPA transcriptions for the same word are separated by double-space | double-space rather than a single space for the sake of improving readability.

You can also find statistics information about each language in the directory [`stats`](https://github.com/sarachilson/FILMS-Corpus/tree/main/stats).

The statistics information includes:
- the average word length within the text of the corpus
- the average word length of unique words in the corpus
- the total number of words (word characters, bigrams) in the text
- the total number of unique words (word characters, bigrams)
- A set of characters that were removed after the dataset pre-processing.


## Code

Run [`main.py`](https://github.com/sarachilson/FILMS-Corpus/blob/main/main.py) to produce frequency files.
`main.py` takes the following arguments that allow you to modify the frequency data output:

| Argument | Full argument name | Description |
| --- | --- | --- |
| `-h` | `--help` | List available arguments. |
| `-f FILE` | `--file FILE` | The path to the raw data file (when creating a new frequency list) / an existing frequency list file (when using update mode to update the file with necessary information) (required). |
| `-u` | `--update` | Use to update the provided frequency list with new information. |
| `-n NEW_DATA` | `--new-data NEW_DATA` | The path to a raw data file to calculate new frequency information from and add it to an already existing frequency list. Only works in update mode. The default is "" (no data to be added). |
| `-l LANGUAGE` | `--language LANGUAGE` | The language of the data as a full name (e.g. "English", not case-sensitive) or abbreviation (e.g. "en"). Note that it is especially important to provide the correct language when using Aspell. Default: "english". |
| `-x EXTENSION [EXTENSION ...]` | `--extension EXTENSION [EXTENSION ...]` | The extension of the file to export the data into (`txt` (tab-separated)/`xlsx`/`csv`/`tsv`). You can provide several data types (default: `txt xlsx`). |
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
python main.py -f PathToFile -x xlsx --ipa PathToIPAFile --stats -p
```
