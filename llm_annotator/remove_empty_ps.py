import os
import jsonlines

current_folder=os.getcwd()

data_path = current_folder + '/parser_stac_linguistic_test_15.jsonl'
save_path = current_folder + '/parser_stac_linguistic_test_15_checked.jsonl'

checked_data = []

remove_count = 0
with jsonlines.open(data_path) as reader:
    for obj in reader:
        if obj['PS'] == "":
            remove_count += 1
        else:
            checked_data.append(obj)


with jsonlines.open(save_path, mode='w') as writer:
    for l in checked_data:
        writer.write(l)

print('json l checked and saved, {} removed'.format(remove_count))



