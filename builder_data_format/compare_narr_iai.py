"""
A sanity check on the iai csvs 
compare to narr csvs for:
-number of samples
-relative length of context
"""

import os
import csv
from collections import Counter

current_folder=os.getcwd()

narr = current_folder + '/actseq-test-narr-worldstate.csv'
iai = current_folder + '/actseq-test-narr-worldstate_attenuated.csv'

with open(iai, 'r') as obj:
    csv_reader = csv.reader(obj)
    iai_list = list(csv_reader)

with open(narr, 'r') as obj:
    csv_reader = csv.reader(obj)
    narr_list = list(csv_reader)


assert len(narr_list) == len(iai_list), 'different lengths'

narr_contexts = []
iai_contexts = []

for n in narr_list[1:]:
    nlist = n[0].split('\n')
    narr_contexts.append(len(nlist[1:]))

for n in iai_list[1:]:
    nlist = n[0].split('\n')
    iai_contexts.append(len(nlist[1:]))

iai_longer = 0
iai_strictly_longer = 0
for i, c in enumerate(iai_contexts):
    if c >= narr_contexts[i]:
        iai_longer += 1
    if c > narr_contexts[i]:
        iai_strictly_longer += 1

print('{} samples out of {} : iai > narr, and {} iai > = narr'.format(iai_strictly_longer, len(iai_contexts), iai_longer))


narr_mean = sum(narr_contexts)/len(narr_contexts)
narr_max = max(narr_contexts)
narr_mode = Counter(narr_contexts).most_common(1)

iai_mean = sum(iai_contexts)/len(iai_contexts)
iai_max = max(iai_contexts)
iai_mode = Counter(iai_contexts).most_common(1)

print('Narr chunks')
print('Max context: {}'.format(narr_max))
print('Avg context len: {}'.format(narr_mean))
print('Mode len: {}'.format(narr_mode))
print('IAI chunks')
print('Max context: {}'.format(iai_max))
print('Avg context len: {}'.format(iai_mean))
print('Mode len: {}'.format(iai_mode))