import random
def random_facts(number):
    with open('dashboard/fact_list.txt') as f:
        lines = f.readlines()
    rand_fact = list()
    for i in range(number):
        rand_fact.append(lines[random.randint(0,316)])
    return rand_fact    
    