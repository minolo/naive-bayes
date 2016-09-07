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

def classify(mail_path, training_data, tk_type):

    # Tokenize mail
    mail_tokens = tokenize(mail_path, token_type=tk_type)

    # Calculate conditional probabilities
    #p_ham_list  = [calculate_token_probability(mail_tokens, word, probability) for (word, probability) in training_data["dict-ham" ].items()]
    #p_spam_list = [calculate_token_probability(mail_tokens, word, probability) for (word, probability) in training_data["dict-spam"].items()]

    p_ham_list  = [training_data["dict-ham" ][token] for token in mail_tokens if token in training_data["dict-ham" ]]
    p_spam_list = [training_data["dict-spam"][token] for token in mail_tokens if token in training_data["dict-spam"]]

    # Apply Bayes' theorem
    log_p_ham  = math.log(training_data["p-ham" ])
    log_p_spam = math.log(training_data["p-spam"])
    log_p_ham_list  = [math.log(h) for h in p_ham_list ]
    log_p_spam_list = [math.log(s) for s in p_spam_list]

    exponent = log_p_spam + sum(log_p_spam_list) - log_p_ham - sum(log_p_ham_list)

    # If the exponent has a low absolute value, use the formula directly
    if abs(exponent) < 100:
        p_ham_mail = 1 / (1 + math.pow(math.e, exponent))

    # Otherwise, set p_ham_mail to 0 if it is positive and to 1 if it is negative (avoids range errors with math.pow)
    else:
        p_ham_mail = max(min(-exponent, 1), 0)

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
    argpar.add_argument("-k", "--tk-type"      , type=str, required=True, help="Tokenize method")

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
    result = classify(args.input_file, training_data, args.tk_type)

    # Print result
    print("This file is classified as {}".format(result))

if __name__ == "__main__":
    main()
