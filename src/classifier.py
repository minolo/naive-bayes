import logging
from functools import reduce
import operator
import pickle
import argparse

from tokenizer import tokenize

def calculate_token_probability(mail_tokens, word, probability):
    if word in mail_tokens:
        return probability
    else:
        return 1 - probability

def classify(mail_path, training_data):
    
    # Tokenize mail
    mail_tokens = tokenize(mail_path)
    
    # Calculate conditional probabilities
    p_ham_list  = [calculate_token_probability(mail_tokens, word, probability) for (word, probability) in training_data["dict-ham" ].items()]
    p_spam_list = [calculate_token_probability(mail_tokens, word, probability) for (word, probability) in training_data["dict-spam"].items()]
    p_mail_ham  = reduce(operator.mul, p_ham_list,  1)
    p_mail_spam = reduce(operator.mul, p_spam_list, 1)

    # Apply Bayes' theorem
    p_mail = p_mail_ham * training_data["p-ham"] + p_mail_spam * training_data["p-spam"]
    p_ham_mail = (p_mail_ham * training_data["p-ham" ]) / p_mail

    print(mail_path)
    print(p_ham_mail)

    # Classify the mail
    if p_ham_mail > 0.5:
        return "ham"
    else:
        return "spam"

def main():
    
    # Define the program arguments for the parser
    argpar = argparse.ArgumentParser()
    argpar.add_argument("-i", "--input-file",    type=str, required=True, help="Input file to classify")
    argpar.add_argument("-t", "--training-data", type=str, required=True, help="Training data file"    )

    # Parse the arguments
    args = argpar.parse_args()

    # Load training data
    try:
        with open(args.training_data, "rb") as training_data_file:
            training_data = pickle.load(training_data_file)
    
    except Exception as e:
        logging.error(e)
        exit(-1)

    print([w for (w, p) in training_data["dict-spam"].items() if p == 1])

    # Classify the file
    result = classify(args.input_file, training_data)

    # Print result
    print("This file is classified as {}".format(result))

if __name__ == "__main__":
    main()
