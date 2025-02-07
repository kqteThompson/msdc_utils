import os
import csv


current_folder=os.getcwd()
# gold_path = '/home/kate/minecraft_utils/synthetic/corrections/correction_synth_nebulipa_SHORT_with_structure.csv'
# pred_path = current_folder + '/nebula_narr_corrsynth_SHORT_output.csv'
# save_path = current_folder + '/SHORT_narr_merge.csv'

gold_path = '/home/kate/minecraft_utils/synthetic/corrections/correction_synth_nebulipa_LONG_without_structure.csv'
pred_path = current_folder + '/nebulipa_full_corrsynth_LONG_nostruct_output.csv'
save_path = current_folder + '/LONG_NOstruct_merge_FULL.csv'

# gold_path = '/home/kate/minecraft_utils/synthetic/corrections/correction_synth_nebulipa_LONG_with_structure.csv'
# pred_path = current_folder + '/nebula_narr_corrsynth_LONG_output.csv'
# save_path = current_folder + '/LONG_narr_merge.csv'

with open(gold_path) as csvfile:
    samples = csv.reader(csvfile)
    gold_rows = [s for s in samples]

with open(pred_path) as csvfile:
    samples = csv.reader(csvfile)
    pred_rows = [s for s in samples]


merge_data = []

for i, r in enumerate(gold_rows):
    if i != 0:
        merge_row = [i]
        if r[1].strip() == pred_rows[i][1].strip():
            merge_row.append('correct')
            # print('correct')
        elif [n.strip() for n in r[1].split('\n')] == [n.strip() for n in pred_rows[i][1].split('\n')]:
            merge_row.append('correct')
            # print('correct')
        else:
            # print(i)
            # print([n.strip() for n in r[1].split('\n')])
            # print([n.strip() for n in pred_rows[i][1].split('\n')])
            # print(r[1].strip())
            # print(pred_rows[i][1].strip())
            merge_row.append('ERROR')
            # print('error')
        merge_row.extend(r)
        merge_row.append(pred_rows[i][1])

        merge_data.append(merge_row)

print(len(merge_data), ' rows')

fields = ['snum', 'correct', 'dial_with_actions', 'action_seq', 'pred_seq']
with open(save_path, 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    for m in merge_data:
        write.writerow(m)

print('csv saved.')
