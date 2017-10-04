# -*- coding: utf-8 -*-
"""
PARSE_LEXICA:

    Contains a class for parsing a language-to-Blissymbols
    dictionary from plaintext (.txt) and Excel (.xls) files.

    Allows ease of changing Bliss dictionaries, including
    adding languages beyond English.

    Alphabetical list of part-of-speech tags used in the
    Penn Treebank Project:

    Number  Tag     Description
    1.      CC      Coordinating conjunction
    2.      CD	    Cardinal number
    3.	    DT	    Determiner
    4.	    EX	    Existential there
    5.	    FW	    Foreign word
    6.	    IN	    Preposition or subordinating conjunction
    7.	    JJ	    Adjective
    8.	    JJR	    Adjective, comparative
    9.	    JJS	    Adjective, superlative
    10.	    LS	    List item marker
    11.	    MD	    Modal
    12.	    NN	    Noun, singular or mass
    13.	    NNS	    Noun, plural
    14.	    NNP	    Proper noun, singular
    15.	    NNPS	Proper noun, plural
    16.	    PDT	    Predeterminer
    17.	    POS	    Possessive ending
    18.	    PRP	    Personal pronoun
    19.	    PRP$	Possessive pronoun
    20.	    RB	    Adverb
    21.	    RBR	    Adverb, comparative
    22.	    RBS	    Adverb, superlative
    23.	    RP	    Particle
    24.	    SYM	    Symbol
    25.	    TO	    to
    26.	    UH	    Interjection
    27.	    VB	    Verb, base form
    28.	    VBD	    Verb, past tense
    29.	    VBG	    Verb, gerund or present participle
    30.	    VBN	    Verb, past participle
    31.	    VBP	    Verb, non-3rd person singular present
    32.	    VBZ	    Verb, 3rd person singular present
    33.	    WDT	    Wh-determiner
    34.	    WP	    Wh-pronoun
    35.	    WP$	    Possessive wh-pronoun
    36.	    WRB	    Wh-adverb
"""
import os
from resources import omw_tabs
from xlrd import open_workbook
from PIL import Image
import re

class LexiconParser:
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    IMG_PATH = FILE_PATH + "/symbols/png/full/"
    LEXICA_PATH = FILE_PATH + "/resources/lexica/"
    LEX_PATH = LEXICA_PATH + "universal bliss lexicon.xls"
    LANGUAGES = set(["English",
                     "Swedish",
                     "Norwegian",
                     "Hungarian",
                     "German",
                     "Dutch",
                     "Afrikaans",
                     "Russian",
                     "Latvian",
                     "Polish",
                     "French",
                     "Spanish",
                     "Portuguese",
                     "Italian",
                     "Danish"])

    def __init__(self):
        """
        Initializes this LexiconParser.
        """

    def parseLexicon(self, filename):
        """
        Parses plaintext file with given filename.
        Returns a dict with all words in lexicon
        as keys and corresponding lemma forms as values.
        ~
        Each new lexical entry should be separated by "\n",
        while inflected forms should be separated by ",".
        ~
        Assumes first word on every line is the lemma form
        of all subsequent words on the same line.
        ~
        N.B. The same lemma value will often belong to multiple keys.

        e.g. "kota, kocie, kot" -> {"kota":"kota", "kocie":"kota", "kot":"kota"}

        :param filename: str, filename of .txt file for lexicon
        :return: dict, where...
            keys (str) - inflected form of a word
            vals (str) - lemma form of inflected word
        """
        lemma_dict = {}

        with open(self.FILE_PATH + filename, "rb") as lexicon:
            for entry in lexicon:
                entry = entry.decode("utf-8")
                entry = entry.strip("\n")
                entry = entry.strip("\r")
                inflexions = entry.split(",")
                lemma = inflexions[0]

                for inflexion in inflexions:
                    lemma_dict[inflexion.strip()] = lemma

        return lemma_dict

    def cleanDefn(self, defn):
        """
        Cleans the input ILI definition line.

        :param defn: str, line in ILI
        :return: List[WordEntry], list of word concepts
        """
        word_entries = []
        idx = re.search(pattern="i[0-9]{1,8}", string=defn).group(0)
        code = re.search(pattern="[0-9]{8}-[a|n|r|s|v]", string=defn).group(0)
        word = re.search(pattern="#\s.+", string=defn).group(0)
        word = str(word[2:])
        words = word.split(",")
        for word in words:
            word = word.strip()
            entry = WordEntry(int(idx[1:]), str(code), word)
            word_entries.append(entry)
        return word_entries

    def cleanWordEntry(self, entry):
        """
        Returns string representation of given WordEntry.

        :param entry: WordEntry, word entry to turn to string
        :return: str, string representation of given WordEntry
        """
        return "index: " + str(entry.idx) + "\t" + \
               "address: " + str(entry.address) + "\t" + \
               "word: " + str(entry.word) + "\n"

    def readILIMapping(self):
        """
        Reads plaintext file with mapping from Princeton WordNet
        to ILI (Interlingual Language Index), a conceptual dictionary.
        ~
        Used for cross-lingual translation.

        :return: None
        """
        with open(self.LEXICA_PATH + "ili-wn-mapping.txt", "r") as ili:
            cili = ili.readlines()[10:]
            for defn in cili:
                self.writeILIMapping(self.cleanDefn(defn))

    def writeILIMapping(self, clean_defns):
        """
        Writes to plaintext file with mapping from Princeton WordNet
        to ILI (Interlingual Language Index), a conceptual dictionary.
        ~
        Used for cross-lingual translation.

        :param clean_defns: List[WordEntry], list of word entries to write
        :return: None
        """
        out = self.LEXICA_PATH + "ili-wn-mapping-cleaned.txt"
        #open(out, 'w').close()  # wipe file before writing

        with open(out, "a") as ili:
            for defn in clean_defns:
                ili.write(self.cleanWordEntry(defn))

    def getBlissEncodings(self, filename):
        """
        Reads list of Blissymbol names from plaintext file with given
        filename and returns a dict linking hex values to Blissymbol names.
        ~
        Output conforms to encoding suggested here:
        http://std.dkuug.dk/JTC1/SC2/WG2/docs/n1866.pdf
        ~
        N.B. Each dict key follows the regex:
            x[0-3]-([A-F]|[0-9]){2}
            e.g. x0-00
                 x3-FF
                 x1-E6

        :param filename: str, .txt file with Blissymbol names
        :return: dict, where...
            keys (str) - hexadecimal value for Blissymbol
            vals (str) - Blissymbol name
        """
        encodings = {}

        with open(self.FILE_PATH + filename, "rb") as bliss_names:
            dec = 0
            row = 0
            prefix = 32

            for name in bliss_names:
                hx = (hex(dec)[-2:]).upper()     # fetch last 2 hex digits
                hx = hx.replace("X", "0")
                idx = "x" + str(row) + "-" + hx  # make hex encoding key
                uni = "U+" + str(prefix) + hx    # make unicode key
                encodings[name[11:-1].lower()] = (idx, uni)

                if dec < (16**2)-1:
                    # stay below 2 hex digits
                    dec += 1
                else:
                    # above 2 hex digits,
                    # reset hex & inc row
                    dec = 0
                    row += 1
                    prefix += 1

        return encodings

    def parseAlphabetic(self, word):
        """
        Parses the given non-alphabetic word into an
        alphabetic-only version of the word.
        ~
        String cuts off at end of the first predicted lexeme.

        e.g. parseAlphabetic("English (language)") -> "English"

        :param word: str, non-alphabetic word
        :return: str, alphabetic version of input word
        """
        new_word = []
        remove = False

        for char in word:
            if remove == False and char != "(":
                new_word.append(char)
            elif char == "(":
                remove = True
            elif char == ")":
                remove = False

        return ("".join(new_word)).strip()

    def getTabFile(self, lang_code):
        """
        Retrieves a multilingual WordNet tab file for the
        given language.
        ~
        If no such tab file exists, returns None.

        :param lang_code: str, 3-character ISO language code
        :return: tab file, WordNet file for given language
        """
        try:
            return open(self.FILE_PATH + "/resources/omw_tabs/" +
                        "wn-cldr-" + lang_code + ".tab")
        except Exception:
            return None

    def getImgFilenames(self, filename):
        """
        Reads the given XLS file for a cross-lingual Bliss
        dictionary and returns a list of image filenames.

        :param filename: str, name of XLS file
        :return: List[str], image filenames
        """
        book = open_workbook(filename)
        sheets = book.sheets()
        sheet = sheets[0]

        rows = sheet.col_values(1)[1:]
        imgs = [row + ".png" for row in rows]

        return imgs

    def getDefns(self, filename, language):
        """
        Reads the given XLS file for a cross-lingual Bliss
        dictionary and returns a list of the given language's
        words shared by the Bliss lexicon.

        :param filename: str, name of XLS file
        :param language: str, output list's desired language
        :return: List[str], given language's Bliss words
        """
        assert language in self.LANGUAGES

        book = open_workbook(filename)
        sheets = book.sheets()
        sheet = sheets[0]
        header = sheet.row_values(0)

        defns = []

        for head in range(1, len(header), 2):
            if header[head] == language:
                defns = sheet.col_values(head)[1:]

        if len(defns) == 0:
            raise IOError

        return defns

    def pairLists(self, defns, imgs):
        """
        Creates a dict with defns supplying keys (as words in
        chosen language) and imgs supplying vals (as Blissymbol
        images).
        ~
        This function assumes defns and imgs to be ordered
        and paired.
        ~
        If a definition contains multiple words, this function
        splits the definition and adds each word to the dict as
        separate entries linking to the same Blissymbol.
        ~
        If a word in the file has no corresponding Blissymbol,
        the {key,val} pair is not added to the output dict.

        :param defns: List[str], chosen language's lexicon
        :param imgs: List[str], image filenames for defns
        :return: dict, where...
            keys (str) - words in chosen language
            vals (str) - corresponding image filenames
        """
        # TODO: parse parenthetical endings more gracefully
        lang_bliss_dict = {}

        idx = 0

        for defn in defns:
            words = []  # allows for synonyms

            if defn[-5:] != "(OLD)":
                for word in defn.split(","):
                    if "_" in word:
                        word = word.replace("_", " ")
                    if "-" in word:
                        word = word.replace("-", " ")
                    if "!" in word:
                        word = word.replace("!", "")
                    if len(word) > 0:
                        words.append(word)

            try:
                Image.open(self.IMG_PATH + imgs[idx])
            except IOError:
                continue
            else:
                for word in words:
                    if imgs[idx][-11:] == "ercase).png":
                        # don't translate pure alphabet characters
                        continue
                    if word[:9] != "indicator":
                        word = self.parseAlphabetic(word)

                    if word in lang_bliss_dict:
                        if type(lang_bliss_dict[word]) != list:
                            lang_bliss_dict[word] = [lang_bliss_dict[word]]
                        lang_bliss_dict[word].append(imgs[idx])
                    elif len(word) > 0:
                        lang_bliss_dict[word] = imgs[idx]
            finally:
                idx += 1

        return lang_bliss_dict

    def getDefnImgDict(self, filename, language="English"):
        """
        Reads the given XLS file for a cross-lingual Bliss
        dictionary and returns a word-image dict in the given
        language.
        ~
        If no language specified, produce English dict by
        default.

        :param filename: str, name of XLS file
        :param language: str, output list's desired language
        :return: dict, where...
            keys (str) - words in chosen language
            vals (str) - corresponding image filenames
        """
        return self.pairLists(self.getDefns(filename, language),
                              self.getImgFilenames(filename))

    def printDict(self, d):
        """
        Prints the given dictionary as if it were written in code.
        Used for visualizing dict contents.

        :param d: dict, input dictionary to print
        :return: None
        """
        print("{")
        for key in d:
            print('    "' + key + '": ' + '"' + str(d[key]) + '",')
        print("}")


class WordEntry:
    """
    A class to representing word entries in the Interlingual Language Index (ILI).
    In ILI, each entry is a unique cross-lingual concept.
    """
    PARTS_OF_SPEECH = set(["a", "n", "r", "s", "v"])
    LEX_PARSER = LexiconParser()
    BLISS_DICT = LEX_PARSER.getDefnImgDict(LEX_PARSER.LEX_PATH, "English")

    def __init__(self, idx, address, word):
        """
        Represents a word entry in ILI.
        ~
        Each WordEntry has an index tying it to Princeton WordNet (PWN),
        a PWN address, and a corresponding PWN English word.

        :param idx: int, index of synset definition from 0 to 117,659
        :param address: str, PWN address of form [0-9]{8}-[a|n|r|s|v]
        :param word: str, English PWN name for ILI concept
        :param bliss_word: str, Bliss filename
        """
        self.idx = idx
        self.address = address
        self.word = word
        self.pos = self.address[-1]
        self.bliss_defn = str
        self.setBlissDefn()

    def setBlissDefn(self):
        """
        Sets this ILI concept's bliss_defn to the lookup value in
        given bliss_dict.

        :return: None
        """
        try:
            self.BLISS_DICT[self.word]
        except KeyError:
            self.bliss_defn = None
        else:
            self.bliss_defn = self.BLISS_DICT[self.word]