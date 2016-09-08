import logging
import argparse
import pickle
import itertools
import collections
import math

from tokenizer import tokenize

def difflog(p):
    return math.log(1 - p) - math.log(p)

def spamicity(p_ham, p_spam, p_token_ham, p_token_spam):
    return (p_token_spam * p_spam) / (p_token_spam * p_spam + p_token_ham * p_ham)

def probability(occurrences, total, vocabulary_size):
    return (occurrences + 1) / (total + vocabulary_size)

def train(ham_files, spam_files, tk_type):

    # Calculate class probability
    num_mails_ham  = len(ham_files)
    num_mails_spam = len(spam_files)
    num_mails_total = num_mails_ham + num_mails_spam
    p_ham  = num_mails_ham  / num_mails_total
    p_spam = num_mails_spam / num_mails_total

    # Tokenize files
    ham_tokens  = (tokenize(f, token_type=tk_type) for f in ham_files)
    spam_tokens = (tokenize(f, token_type=tk_type) for f in spam_files)

    # Collect all tokens
    ham_all_tokens  = itertools.chain.from_iterable(ham_tokens)
    spam_all_tokens = itertools.chain.from_iterable(spam_tokens)

    # Count token occurrences
    ham_tokens_counter  = collections.Counter(ham_all_tokens)
    spam_tokens_counter = collections.Counter(spam_all_tokens)

    # Build vocabulary
    vocabulary = set(ham_tokens_counter.keys()) | set(spam_tokens_counter.keys())
    vocabulary_size = len(vocabulary)

    # Calculate token probability
    num_tokens_ham  = sum(ham_tokens_counter.values())
    num_tokens_spam = sum(spam_tokens_counter.values())
    probabilities_ham  = dict((token, probability(ham_tokens_counter[token] , num_tokens_ham , vocabulary_size)) for token in vocabulary)
    probabilities_spam = dict((token, probability(spam_tokens_counter[token], num_tokens_spam, vocabulary_size)) for token in vocabulary)

    # Calculate token spamicity
    token_spamicity = dict((token, spamicity(p_ham, p_spam, probabilities_ham[token], probabilities_spam[token])) for token in vocabulary)

    # Precalculate difference of logarithms for classification
    result = dict((token, difflog(token_spamicity[token])) for token in vocabulary)

    return result

def main():

    # Define the program arguments for the parser
    argpar = argparse.ArgumentParser()
    argpar.add_argument("-a", "--ham-list" , type=str, required=True, help="Ham file list" )
    argpar.add_argument("-s", "--spam-list", type=str, required=True, help="Spam file list")
    argpar.add_argument("-o", "--output"   , type=str, required=True, help="Output file"   )
    argpar.add_argument("-t", "--tk-type"  , type=str, required=True, help="Tokenize method")

    # Parse the arguments
    args = argpar.parse_args()

    # Read file lists and remove empty lines
    try:
        with open(args.ham_list, "rb") as ham_list:
            ham_files = ham_list.read().splitlines()
            ham_files = [line for line in ham_files if line]

        with open(args.spam_list, "rb") as spam_list:
            spam_files = spam_list.read().splitlines()
            spam_files = [line for line in spam_files if line]

    except Exception as e:
        logging.error(e)
        exit(-1)

    # Build the dictionary with the training data
    result = train(ham_files, spam_files, args.tk_type)

    # Save the result in the output file
    try:
        with open(args.output, "wb") as output_file:
            pickle.dump(result, output_file)

    except Exception as e:
        logging.error(e)
        exit(-1)

if __name__ == "__main__":
    main()
