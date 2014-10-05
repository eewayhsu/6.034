from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    """    
#Try 3
    tree = [hypothesis]
    for rule in rules:
        for exp in rule.consequent():
            matching = match(exp, hypothesis)
            if matching !=None:
                antecedent = rule.antecedent()
                if type(antecedent) is str:
                    newHyp = populate(antecedent, matching)
                    tree.append(backchain_to_goal_tree(rules, newHyp))
                    tree.append(newHyp)
                else:
                    statements = [populate(exp, matching) for exp in antecedent]
                    newTree = []
                    for statement in statements:
                        newTree.append(backchain_to_goal_tree(rules, statement))
                    if type(antecedent) == type(OR()):
                        tree.append(OR(newTree))
                    else:
                        tree.append(AND(newTree))
    return simplify(OR(tree))
"""


#Try 2
    tree = [hypothesis]
    for rule in rules:
        for exp in rule.consequent():
            matching = match(exp, hypothesis)
            if matching != None:
                filledAnts = populate(rule.antecedent(), matching)
    
                if type(filledAnts) == type(AND()):
                    andState = AND([backchain_to_goal_tree(rules, state) for state in filledAnts])
                    tree.append(andState)
                elif type(filledAnts) == type(OR()):
                    orState = OR([backchain_to_goal_tree(rules, state) for state in filledAnts])
                    tree.append(orState)
                else:
                    tree.append(backchain_to_goal_tree(rules, filledAnts))
    return simplify(OR(tree))
"""
#Try 1    
    tree = getMatchAnt(rules, hypothesis)
    newTree = []
    newTree.append(tree[0])

#This is not correctly expanding until we reach where we have already been.
    print tree
    for x in range(len(tree)-1):

        if type(tree[x+1]) is not str:
            for y in range(len(tree[x+1])):
                tree[x+1][y] = getMatchAnt(rules, tree[x+1][y])
        else:
            tree[x+1] = getMatchAnt(rules, tree[x+1])
        newTree.append(tree[x+1])

    return simplify(OR(newTree))

#This gets the antecedents that match on one level into an OR

def getMatchAnt(rules, hypothesis):
    branchOr = [hypothesis]
    branchOrFill = []
    for rule in rules:
        for exp in rule.consequent():
            matching = match(exp, hypothesis)
            if matching != None:
                branch = [rule.antecedent()]
                branchFill = [populate(x, matching) for x in branch]
                branchOr.append(branchFill[0])
                
                branchOr.append(rule.antecedent())
                branchFill = [populate(x, matching) for x in branchOr]
                branchOrFill.append(branchFill)

    #branchOrFill = [populate(x, matching) for x in branchOr]

    return OR(branchOr)
   """         

# Here's an example of running the backward chainer - uncomment
# it to see it work:

#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
