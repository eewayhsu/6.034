from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.

    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False


    """X = state.get_current_variable()

    if X is not None:
        x = X.get_assigned_value()
        constraints = state.get_constraints_by_name(X.get_name())

        for constraint in constraints:
            if state.get_variable_by_name(constraint.get_variable_i_name()) == X:
                Y_name = constraint.get_variable_j_name()
            else:
                Y_name = constraint.get_variable_i_name()"""

            
                
        


    X = state.get_current_variable()
   
#THIS IS BEYOND FRUSTRATING
 
    if X is not None:  
        x = X.get_assigned_value()
        constraints = state.get_constraints_by_name(X.get_name())
        for constraint in constraints:
            if state.get_variable_by_name(constraint.get_variable_i_name()) == X:
                Y_name = constraint.get_variable_j_name()
            else:
                Y_name = constraint.get_variable_i_name()           
    
            Y = state.get_variable_by_name(Y_name)

            for y in Y.get_domain():
                if constraint.check(state, x, y) is False:
                    Y.reduce_domain(y)
                if Y.domain_size() is 0:
                    return False
    return True

    
            

""" TRY 1
    yIndex = 0
    x = X.get_assigned_value()
    constraints = state.get_constraints_by_name(X.get_name())

    for constraint in constraints:
        if state.get_variable_by_name(constraint.get_variable_i_name()) == X:
                Y = state.get_variable_by_name(constraint.get_variable_j_name())
    else:
        Y = state.get_variable_by_name(constraint.get_variable_i_name())

                for value in Y.get_domain():
            if check(state, x, value):
                Y.set_value(value)
            
                while yIndex < len(state.variable_map):
                    if state.get_variable_by_index(yIndex) == Y:
                        state.variable_index = yIndex
                    yIndex += 1
                yIndex = 0 
            print (Y, state.get_current_variable())
        return forward_check(state, verbose=False)

        elif not check(state, x, value):
            Y.reduce_domain(value)
    return False
"""
    # Add your forward checking logic here.
 

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    # Queue, first in first out. pop(0) 
    

    singletons = []
    visited = []

    for variable in state.get_all_variables():
        if variable.domain_size() == 1:
             singletons.append(variable)

    while singletons:
        X = singletons.pop(0)
        visited.append(X)
        
        x = X.get_domain()[0]
        
        for constraint in state.get_constraints_by_name(X.get_name()):
            if state.get_variable_by_name(constraint.get_variable_j_name()) == X:
                Y_name = constraint.get_variable_i_name()
            else:
                Y_name = constraint.get_variable_j_name()

            Y = state.get_variable_by_name(Y_name)
            
            for y in Y.get_domain():
                if not constraint.check(state, x, y):
                    Y.reduce_domain(y)
                if Y.domain_size() == 0:
                    return False
                elif Y.domain_size() == 1 and Y not in visited and Y not in singletons:
                    singletons.append(Y)
    return True


## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
    total = 0
    for i in range(len(list1)):
        total += (list1[i] - list2[i])**2

    total = math.sqrt(total)
     
    return total

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

#3 errors d >= td + 1.  Correct t errors d>= 2t + 1

my_classifier = nearest_neighbors(hamming_distance, 4)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    
    nYes = float(len(yes))
    nNo = float(len(no))
    nTotal = nYes + nNo

    dYes, dNo = 0, 0
    yesDic, noDic = {}, {}


    for datum in yes:
        if datum in yesDic:
            yesDic[datum] += 1
        else:
            yesDic[datum] = 1

    for count in yesDic.itervalues():
        probability = float(count)/nYes
        dYes += -probability * math.log(probability, 2)
            

    for datum in no:
        if datum in noDic:
            noDic[datum] += 1
        else:
            noDic[datum] = 1

    for count in noDic.itervalues():
        probability = float(count)/nNo
        dNo += -probability * math.log(probability, 2) 
    
    disorder = nYes/nTotal * dYes + nNo/nTotal * dNo

    return disorder
    
        

#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 45
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 67
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "5"
WHAT_I_FOUND_INTERESTING = "Learning about senators"
WHAT_I_FOUND_BORING = "That last part, did I not understand right or was it guess and check?"


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
