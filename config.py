from random import sample
'''
	Number Definitons
'''
general_nos = list(range(1,11))
easy_nos = list(range(1,6))
tougher_nos = list(range(11,16))

easy_pairs = list()
random_pairs = list()
safety_pairs = list()

'''
	Worksheet Arithmetic
'''
operator = '+'
exercise_name = 'Addition'

'''
	Number Generator
'''
sheet_number = 3
# Easy Pairings
for i in easy_nos:
	easy_pairs.extend(list(map(lambda x: [i,x] , general_nos)))
# Tough Safety Pairs	
for i in range(0,10):
	safety_pairs.append(sample(tougher_nos, k=2))
for i in range(0,10):
	safety_pairs.append(sample(tougher_nos, k=2))
# Random Pairings
for i in range(0,50):
	random_pairs.append(sample(general_nos, k=2))

'''
	Numbers Pairs Passed to Generator
'''
all_pairs = easy_pairs + random_pairs + safety_pairs