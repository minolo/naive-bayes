from classifier import classify
import argparse
import logging
import pickle
from functools import partial

def evaluate(ham_mails, spam_mails, training_data, threshold):

    # Initialize confusion matrix
    cmat = {"ham" :{"ham":0, "spam":0},
            "spam":{"ham":0, "spam":0}}

    # Classify mails
    ham_mails_classified  = map(partial(classify, training_data=training_data, threshold=threshold), ham_mails )
    spam_mails_classified = map(partial(classify, training_data=training_data, threshold=threshold), spam_mails)

    # Fill confusion matrix
    for classification in ham_mails_classified:
        cmat["ham" ][classification] += 1

    for classification in spam_mails_classified:
        cmat["spam"][classification] += 1

    # Normalize results
    s = len(ham_mails) + len(spam_mails)
    cmat["ham" ]["ham" ] /= s
    cmat["ham" ]["spam"] /= s
    cmat["spam"]["ham" ] /= s
    cmat["spam"]["spam"] /= s

    return cmat

def main():

    # Define the program arguments for the parser
    argpar = argparse.ArgumentParser(description='Evaluator')
    argpar.add_argument("-a", "--ham_path_list",
                        required=True,
                        help="Path to file with a list of paths to ham mails")
    argpar.add_argument("-s", "--spam_path_list",
                        required=True,
                        help="Path to file with a list of paths to spam mails")
    argpar.add_argument("-d", "--training_data",
                        required=True,
                        help="Path to file with the training data")
    argpar.add_argument("-m", "--machine",
                        action="store_true",
                        help="Output in machine format")
    argpar.add_argument("-u", "--threshold",
                        type=float, required=True, help="Threshold")

    # Parse the arguments
    args = argpar.parse_args()

    # Read file lists and remove empty lines
    try:
        with open(args.ham_path_list, "rb") as ham_list:
            ham_files = ham_list.read().splitlines()
            ham_files = [line for line in ham_files if line]

        with open(args.spam_path_list, "rb") as spam_list:
            spam_files = spam_list.read().splitlines()
            spam_files = [line for line in spam_files if line]

    except Exception as e:
        logging.error(e)
        exit(-1)

    # Load training data
    try:
        with open(args.training_data, "rb") as training_data_file:
            training_data = pickle.load(training_data_file)

    except Exception as e:
        logging.error(e)
        exit(-1)

    # Compute the confusion matrix
    cmat = evaluate(ham_files, spam_files, training_data, args.threshold)

    # Print performance data
    if args.machine:
        print("{};{};{};{}".format(cmat["ham"]["ham"], cmat["ham"]["spam"],
                                   cmat["spam"]["ham"], cmat["spam"]["spam"]))
    else:
        print("     ham      spam\n"
              "ham  {:.2f}%   {:.2f}%\n"
              "spam {:.2f}%   {:.2f}%".format(cmat["ham"]["ham"]*100,
                                           cmat["ham"]["spam"]*100,
                                           cmat["spam"]["ham"]*100,
                                           cmat["spam"]["spam"]*100))
        print()
        print("Correctly classified: {:.2f}%".format((cmat["ham"]["ham"] + cmat["spam"]["spam"]) * 100))


if __name__ == "__main__":
    main()
