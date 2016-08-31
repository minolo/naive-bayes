from classifier import classify

def evaluate(ham_mails, spam_mails, training_data):

    # Initialize confusion matrix
    cmat = {"ham" :{"ham":0, "spam":0},
            "spam":{"ham":0, "spam":0}}

    # Fill confusion matrix
    for mail in ham_mails:
        cmat["ham" ][classify(mail, training_data)] += 1

    for mail in spam_mails:
        cmat["spam"][classify(mail, training_data)] += 1

    # Normalize results
    s = len(ham_mails) + len(spam_mails)
    cmat["ham" ]["ham" ] /= s
    cmat["ham" ]["spam"] /= s
    cmat["spam"]["ham" ] /= s
    cmat["spam"]["spam"] /= s

    return cmat

def main():
    argpar = argparse.ArgumentParser(description='Evaluator')
    argpar.add_argument("-a", "--ham_path_list",
                        required=True,
                        help="Path to file with a list of paths to ham mails")
    argpar.add_argument("-s", "--spam_path_list",
                        required=True,
                        help="Path to file with a list of paths to spam mails")
    argpar.add_argument("-t", "--training_data",
                        required=True,
                        help="Path to file with the training data")
    argpar.add_argument("-m", "--machine",
                        action="store_true",
                        help="Output in machine format")
    args = argpar.parse_args()

    cmat= evaluate(args.ham_path_list, args.spam_path_list, args.training_data)

    if args.machine:
        print("{} {} {} {}".format(cmat["ham"]["ham"], cmat["ham"]["spam"],
                                   cmat["spam"]["ham"], cmat["spam"]["spam"]))
    else:
        print("     ham   spam\n"
              "ham  {:3d}%  {:3d}%\n"
              "spam {:3d}%  {:3d}%".format(cmat["ham"]["ham"]*100,
                                           cmat["ham"]["spam"]*100,
                                           cmat["spam"]["ham"]*100,
                                           cmat["spam"]["spam"]*100))

if __name__ == "__main__":
    main()
