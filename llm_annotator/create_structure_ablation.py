"""
Takes llama parser data and removes the structure from the sample prompt
"""
import os
import jsonlines

current_folder=os.getcwd()


data_path = current_folder + '/parser_test_moves_15.jsonl'
ablation_path = current_folder + '/parser_test_moves_15_struct-two.jsonl'

ablation = []

sample_count = 0

with jsonlines.open(data_path) as reader:
    for obj in reader:
        sample_count += 1
        new_obj = {}
        new_obj['PS'] = obj['PS']
        split = obj['sample'].split('\n')
        new_sample = []
        for s in split:
            if 'Structure:' not in s:
                new_sample.append(s)
            else:
                new_sample.append('Structure:')
        join_sample = '\n'.join(new_sample)
        new_obj['sample'] = join_sample
        ablation.append(new_obj)

with jsonlines.open(ablation_path, mode='w') as writer:
    for a in ablation:
        writer.write(a)

# with open(save_path, 'w') as outfile:
#     json.dump(turn_version, outfile)

assert len(ablation) == sample_count
print('jsonl saved for {} games'.format(len(ablation)))


        