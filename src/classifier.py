import logging
import pickle
import argparse
import math

from tokenizer import tokenize

def classify(mail_path, training_data, threshold):

    # Tokenize mail
    mail_tokens = tokenize(mail_path, token_type=training_data["tk_type"])

    # Gather logarithms
    difflogs = [training_data["difflogs"][token] for token in mail_tokens if token in training_data["difflogs"]]

    # Calculate exponent
    exponent = sum(difflogs)

    # If the exponent has a low absolute value, use the formula directly
    if abs(exponent) < 100:
        probability = 1 / (1 + math.pow(math.e, exponent))

    # Otherwise, set p_ham_mail to 0 if it is positive and to 1 if it is negative (avoids range errors with math.pow)
    else:
        probability = max(min(-exponent, 1), 0)

    # Classify the mail
    if probability > threshold:
        return "spam"
    else:
        return "ham"

def main():

    # Define the program arguments for the parser
    argpar = argparse.ArgumentParser()
    argpar.add_argument("-i", "--input-file",    type=str,   required=True, help="Input file to classify")
    argpar.add_argument("-t", "--training-data", type=str,   required=True, help="Training data file")
    argpar.add_argument("-u", "--threshold",     type=float, required=True, help="Threshold to considerate a mail spam")

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
    result = classify(args.input_file, training_data, args.threshold)

    # Print result
    print("This file is classified as {}".format(result))

if __name__ == "__main__":
    main()
