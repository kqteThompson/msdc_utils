import csv
import jsonlines
import os
import random
import numpy as np


current_folder=os.getcwd()
old_long = current_folder + "/synthetic_corrections_long_test_freeze.jsonl"
old_short = current_folder + "/synthetic_corrections_short_test_freeze.jsonl"

new_long = current_folder + "/synthetic_corrections_long_FREEZE_ablation.jsonl"
new_short = current_folder + "/synthetic_corrections_short_FREEZE_ablation.jsonl"

new_dial = []

texts = []

with jsonlines.open(old_short) as reader:
    context = [] #keep track of old context
    structure = "Structure: "
    for obj in reader:
        new = {}
        if obj["PS"] == "RES(8,9) CORR(3,9)":
            sample = obj["sample"].split("\n")
            new_sample = []
            follow = []
            new_sample.append("Context: 12 <Arch>" + sample[2].split("<Arch>")[1])
            new_sample.append("13 <Buil>" + sample[3].split("<Buil>")[1])
            new_sample.append("14 <Arch>" + sample[4].split("<Arch>")[1])
            new_sample.append("15 <Buil>" + sample[5].split("<Buil>")[1])
            new_sample.append("16 <Arch>" + sample[6].split("<Arch>")[1])
            new_sample.append("17 <Buil>" + sample[7].split("<Buil>")[1])
            follow.extend(new_sample)
            new_sample.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15) CONTIN(14,16) RES(16,17)")
            new_sample.append("New turn: 18 <Arch>" + sample[8].split("<Arch>")[1])
            moves = '\n'.join(new_sample)
            new["PS"] = "CORR(13,18)"
            new["sample"] = moves
            new_dial.append(new)
            new = {}

            follow.append("18 <Arch>" + sample[8].split("<Arch>")[1])
            follow.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15) CONTIN(14,16) RES(16,17) CORR(13,18)")
            follow.append("New turn: 19 <Buil>" + sample[10].split("<Buil>")[1])
            
            moves = '\n'.join(follow)
            new["PS"] = "RES(18,19) CORR(13,19)"
            new["sample"] = moves
            new_dial.append(new)

        elif obj["PS"] == "RES(8,9) CORR(5,9)":
            sample = obj["sample"].split("\n")
            new_sample = []
            follow = []
            new_sample.append("Context: 12 <Arch>" + sample[2].split("<Arch>")[1])
            new_sample.append("13 <Buil>" + sample[3].split("<Buil>")[1])
            new_sample.append("14 <Arch>" + sample[4].split("<Arch>")[1])
            new_sample.append("15 <Buil>" + sample[5].split("<Buil>")[1])
            new_sample.append("16 <Arch>" + sample[6].split("<Arch>")[1])
            new_sample.append("17 <Buil>" + sample[7].split("<Buil>")[1])
            follow.extend(new_sample)
            new_sample.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15) CONTIN(14,16) RES(16,17)")
            new_sample.append("New turn: 18 <Arch>" + sample[8].split("<Arch>")[1])
            moves = '\n'.join(new_sample)
            new["PS"] = "CORR(15,18)"
            new["sample"] = moves
            new_dial.append(new)
            new = {}

            follow.append("18 <Arch>" + sample[8].split("<Arch>")[1])
            follow.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15) CONTIN(14,16) RES(16,17) CORR(15,18)")
            follow.append("New turn: 19 <Buil>" + sample[10].split("<Buil>")[1])
            
            moves = '\n'.join(follow)
            new["PS"] = "RES(18,19) CORR(15,19)"
            new["sample"] = moves
            new_dial.append(new)

        elif obj["PS"] == "RES(8,9) CORR(7,9)":
            sample = obj["sample"].split("\n")
            new_sample = []
            follow = []
            new_sample.append("Context: 12 <Arch>" + sample[2].split("<Arch>")[1])
            new_sample.append("13 <Buil>" + sample[3].split("<Buil>")[1])
            new_sample.append("14 <Arch>" + sample[4].split("<Arch>")[1])
            new_sample.append("15 <Buil>" + sample[5].split("<Buil>")[1])
            new_sample.append("16 <Arch>" + sample[6].split("<Arch>")[1])
            new_sample.append("17 <Buil>" + sample[7].split("<Buil>")[1])
            follow.extend(new_sample)
            new_sample.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15) CONTIN(14,16) RES(16,17)")
            new_sample.append("New turn: 18 <Arch>" + sample[8].split("<Arch>")[1])
            moves = '\n'.join(new_sample)
            new["PS"] = "CORR(17,18)"
            new["sample"] = moves
            new_dial.append(new)
            new = {}

            follow.append("18 <Arch>" + sample[8].split("<Arch>")[1])
            follow.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15) CONTIN(14,16) RES(16,17) CORR(17,18)")
            follow.append("New turn: 19 <Buil>" + sample[10].split("<Buil>")[1])
            
            moves = '\n'.join(follow)
            new["PS"] = "RES(18,19) CORR(17,19)"
            new["sample"] = moves
            new_dial.append(new)
        
        elif obj["PS"] == "RES(6,7) CORR(3,7)":
            sample = obj["sample"].split("\n")
            new_sample = []
            follow = []
            new_sample.append("Context: 12 <Arch>" + sample[2].split("<Arch>")[1])
            new_sample.append("13 <Buil>" + sample[3].split("<Buil>")[1])
            new_sample.append("14 <Arch>" + sample[4].split("<Arch>")[1])
            new_sample.append("15 <Buil>" + sample[5].split("<Buil>")[1])
            follow.extend(new_sample)
            new_sample.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15)")
            new_sample.append("New turn: 16 <Arch>" + sample[6].split("<Arch>")[1])
            moves = '\n'.join(new_sample)
            new["PS"] = "CORR(13,16)"
            new["sample"] = moves
            new_dial.append(new)
            new = {}

            follow.append("16 <Arch>" + sample[6].split("<Arch>")[1])
            follow.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15) CORR(13,16)")
            follow.append("New turn: 17 <Buil>" + sample[8].split("<Buil>")[1])
            
            moves = '\n'.join(follow)
            new["PS"] = "RES(16,17) CORR(13,17)"
            new["sample"] = moves
            new_dial.append(new)
        
        elif obj["PS"] == "RES(6,7) CORR(5,7)":
            sample = obj["sample"].split("\n")
            new_sample = []
            follow = []
            new_sample.append("Context: 12 <Arch>" + sample[2].split("<Arch>")[1])
            new_sample.append("13 <Buil>" + sample[3].split("<Buil>")[1])
            new_sample.append("14 <Arch>" + sample[4].split("<Arch>")[1])
            new_sample.append("15 <Buil>" + sample[5].split("<Buil>")[1])
            follow.extend(new_sample)
            new_sample.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15)")
            new_sample.append("New turn: 16 <Arch>" + sample[6].split("<Arch>")[1])
            moves = '\n'.join(new_sample)
            new["PS"] = "CORR(15,16)"
            new["sample"] = moves
            new_dial.append(new)
            new = {}

            follow.append("16 <Arch>" + sample[6].split("<Arch>")[1])
            follow.append("Structure: RES(12,13) CONTIN(12,14) RES(14,15) CORR(15,16)")
            follow.append("New turn: 17 <Buil>" + sample[8].split("<Buil>")[1])
            
            moves = '\n'.join(follow)
            new["PS"] = "RES(16,17) CORR(15,17)"
            new["sample"] = moves
            new_dial.append(new)
        

# f = open(current_folder + "/synthetic_corrections_long_freeze_ablations.txt","w")
# for d in texts:
#     print(d, file=f)
#     print('----------------------------\n', file=f)
# print("dialogues printed")


#make llamipa jsonl
#convert the dicts into json dicts for json_l
with jsonlines.open(new_short, mode='w') as writer:
    for s in new_dial:
        # sample = {}
        # sample['PS'] = l[1]
        # sample['sample'] = l[0]
        writer.write(s)
print('jsonl saved for {} samples'.format(len(new_dial)))