import logging
import re

regexs = {
    "basic"    : re.compile("\w+"),
    "word2"    : re.compile("\w\w+"),
    "alphnum2" : re.compile("\w*[a-z_]{2}\w*"),
    "alphnum3" : re.compile("\w*[a-z_]{3}\w*"),
    "alph3"    : re.compile("[a-z_]{3}[a-z_]*"),
    }

def tokenize(file_path, token_type):
    try:
        with open(file_path, "rb") as file:
            mail = file.read().decode("utf8", "ignore")
            mail = mail.replace("\n", " ").lower()
            return list(set(regexs[token_type].findall(mail)))
    except Exception as e:
        logging.error(e)
        exit(-1)
