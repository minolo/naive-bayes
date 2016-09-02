import logging
from functools import partial
import re

def apply_regex(regex_type, mail):
    return list(set(regexs[regex_type].findall(mail)))

def m_only_regex(regex_type, mail):
    return apply_regex(regex_type, mail)

def m_group_words(regex_type, mail):
    for sw, sym in group_words.items():
        mail = regexs[sw].sub(sym, mail)
    return apply_regex(regex_type, mail)

regexs = {
    "basic"     : re.compile("\w+"),
    "word2"     : re.compile("\w\w+"),
    "alphnum2"  : re.compile("\w*[a-z_]{2}\w*"),
    "alphnum3"  : re.compile("\w*[a-z_]{3}\w*"),
    "alph3"     : re.compile("[a-z_]{3}[a-z_]*"),
    "number"    : re.compile("[0-9]+" ),
    "spamwords" : re.compile("(\w )+\w( |\n)" ),
    "url"       : re.compile("(?:(?:https?|ftp|file) *: *\/\/|www\.|ftp\.) *(?:[-A-Z0-9+&@# %=~_|$?!:,.]* \/ *)*[-A-Z0-9+&@#%=~_|$?!:,.]*"),
    }

strategies = {
        "basic"            : partial(m_only_regex,  "basic"),
        "word2"            : partial(m_only_regex,  "word2"),
        "alphnum2"         : partial(m_only_regex,  "alphnum2"),
        "alphnum3"         : partial(m_only_regex,  "alphnum3"),
        "alph3"            : partial(m_only_regex,  "alph3"),
        "groupwords+alph3" : partial(m_group_words, "alph3"),
        }

group_words = {
        "url"       : " ___url___ ",
        "spamwords" : " ___spam_word___ ",
        "number"    : " ___number___ ",
        }

def tokenize(file_path, token_type):
    try:
        with open(file_path, "rb") as file:
            mail = file.read().decode("utf8", "ignore").replace("\n", " ").lower()
            return strategies[token_type](mail)
    except Exception as e:
        logging.error(e)
        exit(-1)
