# Carl Shotwel
# CSE5522 hw2
# 10-12-12

import sys
import math

global_goal = set()
global_attributes = dict()
global_train = []

# initializing the dataset and train/test sets ==================
# Build the attribute dataset
# ugly formatting codes
def initialize(infile):
    fin = open(infile)
    lines = [i for i in fin]
    # handle the last line which contains goal states
    last = lines.pop(-1)
    last = last.split(':')[1].split(',')
    [global_goal.add(i.strip()) for i in last]
    # handle the attribute lines
    for i in lines:
        line = i.split(':')
        #need to remove the string from the list.
        line = iter(line)
        attrib = line.next().strip()
        values = line.next().split(',')
        values = [i.strip() for i in values]
        global_attributes[attrib] = values

#place the training data into lists.  essentially run the same code for test
def train_set(infile):
    fin = open(infile)
    train = [i.split(',') for i in fin]
    # gotta get that whitespace from the end of each list
    for i in range(len(train)):
        train[i][-1] = train[i][-1].strip()
    return train
# ====================================================================

# functions to find importance =======================================
#list of possible values, find how many times each is in the learning set.
def entropy(A, examples):
    entropy_total = 0.0
    #loop through each attribute value
    for i in A:
        count = 0.0
        for e in examples:
            if i in e:
                count += 1
        Pa = (count / len(examples))        
        if Pa == 0:
            entropy_total += 0
        else:
            entropy_total += -Pa * math.log(Pa, 2)
    return entropy_total
        
#accepts a list of goals, a list of attributes, and the learning data
def gain(goals, attrib, examples):
    return entropy(goals,examples) - entropy(attrib,examples)

# this will loop through the availale attributes, returning the name of the max important one.
def max_importance(attributes, examples, goals):
    curr_max = -100.0
    temp = ""
    for i in attributes:
        g = gain(goals, attributes[i], examples)
        if g > curr_max:
            temp = i
            curr_max = g
    return temp
# ===================================================================
# return only examples where v_k is one of the deciders
def get_examples(examples, v_k):
    exs = []
    for i in examples:
        if v_k in i:
            exs.append(i)
    return exs

def plurality_value(examples, goals):
    temp = dict()
    #sum up the endings to each specific goal
    for i in goals:
        temp[i] = 0
        for e in examples:
            if i in e:
                temp[i] += 1
    temp_name = ""
    max_val = 0
    for i in temp:
        if temp[i] > max_val:
            temp_name = i
    return temp_name

#this returns true if they all lead to the same result.
def classification(examples):
    last = examples[0][-1]
    for i in range(len(examples)):
        if not last == examples[i][-1]:
            return False
    return True
    
def decision_tree_learning(examples, attributes, goals):
    if not examples:
        return plurality_value(examples,goals)
    elif classification(examples):
        return examples[0][-1]
    elif not attributes:
        return plurality_value(examples,goals)
    else:
        node = max_importance(attributes, examples, goals)
        tree = dict()
        tree[node] = dict()
        for v_k in attributes[node]:
            if node in attributes:
                attributes.pop(node)
            exs = get_examples(examples, v_k)
            subtree = decision_tree_learning(
                exs,
                attributes,
                goals)
            tree[node][v_k] = subtree
        return tree

#================TESTING====================
def run_test(tree, test, attributes):
    if type(tree) == str:
        return tree
    else:
        guess = tree.keys()[0]
        for i in attributes[guess]:
            for t in test:
                if i == t:
                    return run_test(tree[guess][t], test, attributes)
            

def main():
    #====initializations====
    #build attribute and goal set
    initialize(sys.argv[1]) 
    #build training set
    train = train_set(sys.argv[2])
    #build test set
    test = train_set(sys.argv[3])


    attributes = global_attributes
    goals = global_goal
    #=======================
    #produced tree.
    tree = decision_tree_learning(train, attributes, goals) 
    
    #run tests on the tree
    #reinitialize attributes
    initialize(sys.argv[1])
    for row in test:
        correct = row[-1]
        answer = run_test(tree,row,global_attributes)
        print correct + ' compare: ' + answer

if __name__ == '__main__':
    main()
