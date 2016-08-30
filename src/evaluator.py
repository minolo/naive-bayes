from classifier import classify

def evaluate(ham_mails, spam_mails, training_data):
    cmat = {"ham" :{"ham":0, "spam":0},
            "spam":{"ham":0, "spam":0}}

    for mail in ham_mails:
        if clasify(mail, training_data) == "ham":
            cmat["ham"]["ham"]  += 1
        else:
            cmat["ham"]["spam"] += 1

    for mail in spam_mails:
        if clasify(mail, training_data) == "ham":
            cmat["spam"]["ham"]  += 1
        else:
            cmat["spam"]["spam"] += 1

    sum = cmat["ham"]["ham"] + cmat["ham"]["spam"] +\
          cmat["spam"]["ham"] + cmat["spam"]["spam"]

    cmat["ham"]["ham"]   /= sum
    cmat["ham"]["spam"]  /= sum
    cmat["spam"]["ham"]  /= sum
    cmat["spam"]["spam"] /= sum

    return cmat
