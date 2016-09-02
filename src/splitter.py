import os
import logging
import threading
import argparse
import random
import re

def check_args(args):
    # Check splitting methods
    if (args.eval_percent is None or args.train_percent is None) and args.enron is None:
        logging.error("You must provide almost one splitting method: percentages or \"enron\" division")
        exit(-1)

    # Check percentages
    if not args.enron:
        total_perc = args.eval_percent + args.train_percent
        if total_perc <= 0 or total_perc > 1:
            logging.error("Total percentages must be between 0 and 1")
            exit(-1)

    # Check data directory
    directories = [dir for dir in os.listdir(args.data_dir)
                   if os.path.isdir(os.path.join(args.data_dir, dir))]
    if not all(enron in directories for enron in
               ["enron%d" % n for n in range(1, 7)]):
        logging.error("Missing some \"enron\" directory. Please check the path \"%s\"" % args.data_dir)
        exit(-1)


def parse_args():
    argpar = argparse.ArgumentParser(description='Tokenizer')
    split_group = argpar.add_argument_group(title="Splitting options",
            description="You must provide at least one splitting method: percentages or \"enron\" division")

    split_group.add_argument("-e", "--eval_percent",
                              type=float,
                              help="Evaluation percentage between 0 and 1")
    split_group.add_argument("-t", "--train_percent",
                              type=float,
                              help="Training percentage between 0 and 1")
    split_group.add_argument("--enron",
                              action="store_true",
                              help="Selects \"enron{1..5}\" for training and \"enron6\" for evaluation\"")
    argpar.add_argument("-d", "--data_dir",
                        required=True,
                        help="Data directory")
    argpar.add_argument("evaluation_set_ham",
                        help="Output ham evaluation set file name")
    argpar.add_argument("evaluation_set_spam",
                        help="Output spam evaluation set file name")
    argpar.add_argument("training_set_ham",
                        help="Output ham training set file name")
    argpar.add_argument("training_set_spam",
                        help="Output spam training set file name")

    args = argpar.parse_args()
    check_args(args)

    return args

def split_enron(ddir):
    ev_dirs = [os.path.join(ddir, "enron6")]
    tr_dirs = [os.path.join(ddir, enron) for enron in
               ["enron%d" % n for n in range(1, 6)]]

    ev_ham =  [d + "/ham/"  + f for d in ev_dirs for f in os.listdir(d + "/ham")]
    tr_ham =  [d + "/ham/"  + f for d in tr_dirs for f in os.listdir(d + "/ham")]
    ev_spam = [d + "/spam/" + f for d in ev_dirs for f in os.listdir(d + "/spam")]
    tr_spam = [d + "/spam/" + f for d in tr_dirs for f in os.listdir(d + "/spam")]

    return [ev_ham, ev_spam, tr_ham, tr_spam]

def split_perc(ddir, evp, trp):
    ham  = [os.path.join(d, f) for d, ds, fs in os.walk(ddir) for f in fs if
            re.search("enron./ham", d)]
    spam = [os.path.join(d, f) for d, ds, fs in os.walk(ddir) for f in fs if
            re.search("enron./spam", d)]

    random.shuffle(ham)
    random.shuffle(spam)

    ev_ham_idx  = int((len(ham)  + 1) * evp)
    ev_spam_idx = int((len(spam) + 1) * evp)
    tr_ham_idx  = int((len(ham)  + 1) * trp)
    tr_spam_idx = int((len(spam) + 1) * trp)

    ev_ham  =  ham[0:ev_ham_idx]
    ev_spam = spam[0:ev_spam_idx]
    tr_ham  =  ham[-tr_ham_idx: -1]
    tr_spam = spam[-tr_spam_idx:-1]

    return [ev_ham, ev_spam, tr_ham, tr_spam]

def write_list(lst, path):
    try:
        with open(path, "w") as f:
            f.writelines("\n".join(lst))
    except Exception as e:
        logging.error(e)
        exit(-1)

def main():
    args = parse_args()

    out_files = [args.evaluation_set_ham, args.evaluation_set_spam,
                 args.training_set_ham, args.training_set_spam]

    if args.enron:
        lists = split_enron(args.data_dir)
    else:
        lists = split_perc(args.data_dir, args.eval_percent, args.train_percent)

    threads=[]
    for (l, f) in zip(lists, out_files):
        t = threading.Thread(target=write_list, args=[l, f])
        threads.append(t)
        t.start()

if __name__ == "__main__":
    main()
