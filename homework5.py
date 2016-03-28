############################################################
# CIS 521: Homework 5
############################################################

student_name = "Zhengxuan Wu"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
import os
import Queue
import heapq
############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    f = open(email_path)
    m = email.message_from_file(f)
    token_list = []
    for line in email.iterators.body_line_iterator(m):
        line = line.strip()
        li = line.split()
        for element in li:
            if element != "":
                token_list.append(element)
    return token_list

# test

def log_probs(email_paths, smoothing):
    freq = dict()
    for path in email_paths:
        tokens = []
        tokens = load_tokens(path)
        for element in tokens:
            freq[element] = freq.get(element,0) + 1
    # get counts
    total_count = 0
    vocab_length = 0
    for i in freq:
        total_count += freq[i]
        vocab_length += 1
    # get the frequency table
    for key in freq.keys():
        freq[key] = math.log((freq[key]+smoothing)/(total_count + (smoothing*(vocab_length+1.0))))
    freq["<UNK>"] = math.log((smoothing/(total_count + (smoothing*(vocab_length+1.0)))))
    #print freq
    return freq

#paths = ["data/train/ham/ham%d" % i for i in range(1, 11)]
#paths = ["data/train/spam/spam%d" % i for i in range(1, 11)]
#p = log_probs(paths, 1e-5)
#a = p["the"]
#print a

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        _spam = [item for item in os.listdir(spam_dir) if os.path.isfile(os.path.join(spam_dir, item))]
        _ham = [item for item in os.listdir(ham_dir) if os.path.isfile(os.path.join(ham_dir, item))]
        number_of_ham = len(_ham)
        number_of_spam = len(_spam)
        paths_spam = [spam_dir+'/'+i for i in _spam]
        paths_ham = [ham_dir+'/'+i for i in _ham]
        self.spam_freq = log_probs(paths_spam, smoothing)
        self.ham_freq = log_probs(paths_ham, smoothing)
        self.not_spam_prob = math.log(number_of_ham*1.0/(number_of_spam*1.0+number_of_ham*1.0))
        self.spam_prob = math.log(number_of_spam*1.0/(number_of_spam*1.0+number_of_ham*1.0))
    
    def is_spam(self, email_path):
        test_tokens = load_tokens(email_path)
        spam_cond_prob = self.spam_prob
        not_spam_cond_prob = self.not_spam_prob
        spam_set = set(self.spam_freq.keys())
        ham_set = set(self.ham_freq.keys())
        for element in test_tokens:
            if element in spam_set:
                spam_cond_prob += self.spam_freq[element]
            else:
                spam_cond_prob += self.spam_freq["<UNK>"]

            if element in ham_set:
                not_spam_cond_prob += self.ham_freq[element]
            else:
                not_spam_cond_prob += self.ham_freq["<UNK>"]
        if spam_cond_prob >= not_spam_cond_prob:
            return True
        else:
            return False

    def most_indicative_spam(self, n):
        spam_set = set(self.spam_freq.keys())
        ham_set = set(self.ham_freq.keys())
        ind = [((self.spam_freq[element] - math.log(math.exp(self.spam_freq[element])*math.exp(self.spam_prob) + math.exp(self.ham_freq[element])*math.exp(self.not_spam_prob))),element) for element in self.spam_freq if element in ham_set]
        result = heapq.nlargest(n,ind)
        return [b for (a,b) in result]

    def most_indicative_ham(self, n):
        spam_set = set(self.spam_freq.keys())
        ham_set = set(self.ham_freq.keys())
        ind = [((self.ham_freq[element] - math.log(math.exp(self.spam_freq[element])*math.exp(self.spam_prob) + math.exp(self.ham_freq[element])*math.exp(self.not_spam_prob))),element) for element in self.ham_freq if element in spam_set]
        result = heapq.nlargest(n,ind)
        return [b for (a,b) in result]


#spam_dir = "data/train/spam"
#ham_dir = "data/train/ham"
#ham_test = "data/dev/ham"
#spam_test = "data/dev/spam"
#_spam = [item for item in os.listdir(spam_dir) if os.path.isfile(os.path.join(spam_dir, item))]
#_ham = [item for item in os.listdir(ham_dir) if os.path.isfile(os.path.join(ham_dir, item))]
#_ham_test = [item for item in os.listdir(ham_test) if os.path.isfile(os.path.join(ham_test, item))]
#_spam_test = [item for item in os.listdir(spam_test) if os.path.isfile(os.path.join(spam_test, item))]
#sf = SpamFilter(spam_dir,ham_dir, 1e-5)
#
#print sf.most_indicative_spam(5)
#print sf.most_indicative_ham(5)
# wrong = 0
#for element in _spam_test:
#    if not sf.is_spam("data/dev/spam/"+element):
#        wrong += 1
#        print "Spam Wrong!!!!!!"
#    print "Spam Correct!!!!!!"
#print wrong


#for element in _ham_test:
#    if sf.is_spam("data/dev/ham/"+element):
#        wrong += 1
#        print "Ham Wrong!!!!!!"
#    print "Ham Correct!!!!!!"
#
#print wrong


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
10 hrs
"""

feedback_question_2 = """
the last part! problem 5
"""

feedback_question_3 = """
Practice the knowledge in a real world situation
"""
