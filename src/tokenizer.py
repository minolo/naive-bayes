import logging
import re

regexs = {
    "basic": re.compile("\w+")
    }

def tokenize(file_path, token_type="basic"):
    try:
        with open(file_path, "rb") as file:
            mail = file.read().decode("utf8", "ignore")
            mail = mail.replace("\n", "").lower()
            return list(set(regexs[token_type].findall(mail)))
    except Exception as e:
        logging.error(e)
        exit(-1)
