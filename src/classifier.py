from functools import reduce
import operator

def tokenize(mail_path):
    return []

def calculate_token_probability(mail_tokens, word, probability):
    if word in mail_tokens:
        return probability
    else
        return 1 - probability

def classify(mail_path, training_data):

    # Tokenize mail
    mail_tokens = tokenize(mail_path)
    
    # Calculate conditional probabilities
    p_ham_list  = [calculate_token_probability(mail_tokens, word, probability) for (word, probability) in training_data["dict-ham" ].items()]
    p_spam_list = [calcualte_token_probability(mail_tokens, word, probability) for (word, probability) in training_data["dict-spam"].items()]

    p_mail_ham  = reduce(operator.mul, p_ham_list,  1)
    p_mail_spam = reduce(operator.mul, p_spam_list, 1)

    # Apply Bayes' theorem
    p_mail = p_mail_ham * training_data["p-ham"] + p_mail_spam * training_data["p-spam"]
    p_ham_mail  = (p_mail_ham  * training_data["p-ham" ]) / p_mail
    #p_spam_mail = (p_mail_spam * training_data["p-spam"]) / p_mail

    # Classify the mail
    if p_ham_mail > 0.5:
        return "ham"
    else:
        return "spam"


def main():
    pass

if __name__ == "__main__":
    main()
