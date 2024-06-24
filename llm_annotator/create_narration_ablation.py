"""
Takes llama parser data (for structureless training) and replaces all relations
that are not Narration (or whatever relation type you want)
"""
import os
import jsonlines

current_folder=os.getcwd()


data_path = current_folder + '/parser_val_moves_15_nostructure.jsonl'
ablation_path = current_folder + '/parser_val_moves_15_corr+narr_ablation.jsonl'

ablation = []

sample_count = 0

with jsonlines.open(data_path) as reader:
    for obj in reader:
        sample_count += 1
        new_obj = {}
        rels = obj['PS'].split(' ')
        new_rels = []
        for rel in rels:
            if 'CORR' in rel or 'NARR' in rel:
                new_rels.append(rel)
        if len(new_rels) > 0:
            join_rels = ' '.join(new_rels)
            new_obj['PS'] = join_rels
        else:
            new_obj['PS'] = 'NONE'

        #fix backwards newline in original data
        split = obj['sample'].split('/n')
        new_sample = []
        join_sample = '\n'.join(split)
        new_obj['sample'] = join_sample
        ablation.append(new_obj)

with jsonlines.open(ablation_path, mode='w') as writer:
    for a in ablation:
        writer.write(a)

# with open(save_path, 'w') as outfile:
#     json.dump(turn_version, outfile)

assert len(ablation) == sample_count
print('jsonl saved for {} samples'.format(len(ablation)))


        