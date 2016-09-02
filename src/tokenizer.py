import logging
import re

regexs = {
    "basic": re.compile("\w+"),
    "r1cw"  : re.compile("\w\w+")
    }

def tokenize(file_path, token_type):
    try:
        with open(file_path, "rb") as file:
            mail = file.read().decode("utf8", "ignore")
            mail = mail.replace("\n", "").lower()
            return list(set(regexs[token_type].findall(mail)))
    except Exception as e:
        logging.error(e)
        exit(-1)
