import logging
import argparse
import pickle
import itertools
import collections

from tokenizer import tokenize

def train(ham_files, spam_files, tk_type):
    result = {}

    # Tokenize files
    ham_files_generator  = (tokenize(f, token_type=tk_type) for f in ham_files)
    spam_files_generator = (tokenize(f, token_type=tk_type) for f in spam_files)

    # Flatten lists
    ham_files_all_tokens  = list(itertools.chain.from_iterable(ham_files_generator))
    spam_files_all_tokens = list(itertools.chain.from_iterable(spam_files_generator)) 

    # Count word occurrences
    ham_tokens_counter  = collections.Counter(ham_files_all_tokens)
    spam_tokens_counter = collections.Counter(spam_files_all_tokens)

    # Fill result
    number_ham  = len(ham_files )
    number_spam = len(spam_files)
    total_files = number_ham + number_spam
    result["p-ham"]  = number_ham  / total_files
    result["p-spam"] = number_spam / total_files
    result["dict-ham"]  = dict([(word, occurrences / number_ham ) for (word, occurrences) in dict(ham_tokens_counter ).items()])
    result["dict-spam"] = dict([(word, occurrences / number_spam) for (word, occurrences) in dict(spam_tokens_counter).items()])

    # Remove words with probability 1
    result["dict-ham" ] = dict([(word, probability) for (word, probability) in result["dict-ham" ].items() if probability < 1])
    result["dict-spam"] = dict([(word, probability) for (word, probability) in result["dict-spam"].items() if probability < 1])

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
