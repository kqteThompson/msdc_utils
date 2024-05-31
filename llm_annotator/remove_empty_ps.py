import os
import jsonlines


"""
This is just to remove empty PS's for training
"""

# current_folder=os.getcwd()

# data_path = current_folder + '/parser_stac_linguistic_test_15.jsonl'
# save_path = current_folder + '/parser_stac_linguistic_test_15_checked.jsonl'

# checked_data = []

# remove_count = 0
# with jsonlines.open(data_path) as reader:
#     for obj in reader:
#         if obj['PS'] == "":
#             remove_count += 1
#         else:
#             checked_data.append(obj)


# with jsonlines.open(save_path, mode='w') as writer:
#     for l in checked_data:
#         writer.write(l)

# print('json l checked and saved, {} removed'.format(remove_count))

"""
This is to check how many times the parser generator script will
detect a new dialogue head. 
Should be == the number of dialgues in the set
"""

def is_first_moves(sample):
    answer = 0
    slist = sample.split('\n')
    if slist[0].startswith('Context: 0'):
        struct = [i for i in slist if i.startswith('Structure:')]
        rels = struct[0].split(':')[1].strip()
        if len(rels) == 0:
            answer = 1
    return answer

current_folder=os.getcwd()

data_path = current_folder + '/parser_stac_linguistic_test_15_checked.jsonl'

head_count = 0
heads = []
with jsonlines.open(data_path) as reader:
    for i, obj in enumerate(reader):
        if is_first_moves(obj['sample']):
            head_count += 1
            heads.append((head_count, i))

print('heads: ', head_count)
print(heads)
       