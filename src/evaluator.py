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
    pass

if __name__ == "__main__":
    main()
