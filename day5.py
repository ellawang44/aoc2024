import numpy as np

rules = []
updates = []
with open('data/input_day5.txt') as f:
    for line in f:
        if '|' in line:
            rules.append([int(i) for i in line.strip().split('|')])
        elif line == '\n':
            continue
        else:
            updates.append([int(i) for i in line.strip().split(',')])

def check_update(update):
    for rule in rules:
        if rule[0] in update and rule[1] in update: # rule applicable
            if update.index(rule[0]) > update.index(rule[1]): # break rule
                return False
    return True

tot = 0
for update in updates:
    if check_update(update):
        tot += update[len(update)//2]

print('challenge 1', tot)

##############################

def all_broken_rules(update):
    '''find all broken rules'''
    broken_rules = []
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            if update.index(rule[0]) > update.index(rule[1]): # break rule
                broken_rules.append(rule)
    return broken_rules

def fix_one(update, rule):
    '''fix one of the rules'''
    val = update.pop(update.index(rule[0]))
    ind = update.index(rule[1])
    update.insert(ind, val)

def fix_iter(update):
    '''one iteration of fixing the broken rules'''
    broken_rules = all_broken_rules(update)
    unique_page = np.unique(np.array(broken_rules)[:,0])
    for page in unique_page:
        rule_set = [rule for rule in broken_rules if rule[0] == page]
        ind = np.argmin([update.index(rule[1]) for rule in rule_set])
        fix_one(update, rule_set[ind])

tot = 0
for update in updates:
    if not check_update(update):
        while not check_update(update):
            fix_iter(update)
        tot += update[len(update)//2]

print('challenge 2', tot)