import logging
import pickle
import argparse
import math

from tokenizer import tokenize

def calculate_token_probability(mail_tokens, word, probability):
    if word in mail_tokens:
        return probability
    else:
        return 1 - probability

def classify(mail_path, training_data):

    # Tokenize mail
    mail_tokens = tokenize(mail_path, token_type="r1cw")

    # Calculate conditional probabilities
    p_ham_list  = [calculate_token_probability(mail_tokens, word, probability) for (word, probability) in training_data["dict-ham" ].items()]
    p_spam_list = [calculate_token_probability(mail_tokens, word, probability) for (word, probability) in training_data["dict-spam"].items()]

    # Apply Bayes' theorem
    log_p_ham  = math.log(training_data["p-ham" ])
    log_p_spam = math.log(training_data["p-spam"])
    log_p_ham_list  = [math.log(h) for h in p_ham_list ]
    log_p_spam_list = [math.log(s) for s in p_spam_list]

    exponent = log_p_spam + sum(log_p_spam_list) - log_p_ham - sum(log_p_ham_list)

    p_ham_mail = 1 / (1 + math.pow(math.e, exponent))

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

    # Classify the file
    result = classify(args.input_file, training_data)

    # Print result
    print("This file is classified as {}".format(result))

if __name__ == "__main__":
    main()
