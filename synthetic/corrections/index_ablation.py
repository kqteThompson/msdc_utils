import csv
import jsonlines
import os
import random
import numpy as np


current_folder=os.getcwd()
old_long = current_folder + "/synthetic_corrections_LONG_GEN_test.jsonl"
old_short = current_folder + "/synthetic_corrections_SHORT_GEN_test.jsonl"

new_long = current_folder + "/synthetic_corrections_long_test_ablation.jsonl"
new_short = current_folder + "/synthetic_corrections_short_ablation.jsonl"

new_dial = []

texts = []

with jsonlines.open(old_long) as reader:
    context = [] #keep track of old context
    structure = "Structure: "
    for obj in reader:
        new = {}
        if obj["PS"] == "RES(2,3)":
            assert len(context) == 0
            assert structure == "Structure: "

            sample = obj["sample"].split("\n")
            new_sample = []
            new_sample.append("Context: 12 <Arch>" + sample[2].split("<Arch>")[1])
            context.append("Context: 12 <Arch>" + sample[2].split("<Arch>")[1])
            new_sample.append("Structure: ")
            new_sample.append("New turn: 13 <Buil>" + sample[4].split("<Buil>")[1])
            context.append("13 <Buil>" + sample[4].split("<Buil>")[1])
            new["PS"] = "RES(12,13)"
            structure += "RES(12,13)"
            moves = '\n'.join(new_sample)
            
            new["sample"] = moves
            #add to list
            new_dial.append(new)

        elif obj["PS"] == "CONTIN(2,4)":
            sample = obj["sample"].split("\n")
            new_sample = []
            new_sample.extend(context)
            new_sample.append(structure)
            new_sample.append("New turn: 14 <Arch>" + sample[-1].split("<Arch>")[1])
            context.append("14 <Arch>" + sample[-1].split("<Arch>")[1])
            new["PS"] = "CONTIN(12,14)"
            structure += " CONTIN(12,14)"
            moves = '\n'.join(new_sample)

            new["sample"] = moves
            #add to list
            new_dial.append(new)

        elif obj["PS"] == "RES(4,5)":
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 15 <Buil>" + sample[-1].split("<Buil>")[1]) #add new turn
            context.append("15 <Buil>" + sample[-1].split("<Buil>")[1])
            new["PS"] = " RES(14,15)" #add new prediction
            structure += " RES(14,15)"  #update structure
            moves = '\n'.join(new_sample)

            new["sample"] = moves
            #add to list
            new_dial.append(new)

        elif obj["PS"] == "CORR(3,6)": #short
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 16 <Arch>" + sample[-1].split("<Arch>")[1]) #add new turn
            context.append("16 <Arch>" + sample[-1].split("<Arch>")[1])
            new["PS"] = "CORR(13,16)" #add new prediction
            structure += " CORR(13,16)"  #update structure
            moves = '\n'.join(new_sample)

            new["sample"] = moves
            #add to list
            new_dial.append(new)
        elif obj["PS"] == "CORR(5,6)": #short
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 16 <Arch>" + sample[-1].split("<Arch>")[1]) #add new turn
            context.append("16 <Arch>" + sample[-1].split("<Arch>")[1])
            new["PS"] = "CORR(15,16)" #add new prediction
            structure += " CORR(15,16)"  #update structure
            moves = '\n'.join(new_sample)

            new["sample"] = moves
            #add to list
            new_dial.append(new)
        elif obj["PS"] == "CORR(3,8)": #long
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 18 <Arch>" + sample[-1].split("<Arch>")[1]) #add new turn
            context.append("18 <Arch>" + sample[-1].split("<Arch>")[1])
            new["PS"] = "CORR(13,18)" #add new prediction
            structure += " CORR(13,18)"  #update structure
            moves = '\n'.join(new_sample)

            new["sample"] = moves
            #add to list
            new_dial.append(new)

        elif obj["PS"] == "CORR(5,8)": #long
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 18 <Arch>" + sample[-1].split("<Arch>")[1]) #add new turn
            context.append("18 <Arch>" + sample[-1].split("<Arch>")[1])
            new["PS"] = "CORR(15,18)" #add new prediction
            structure += " CORR(15,18)"  #update structure
            moves = '\n'.join(new_sample)

            new["sample"] = moves
            #add to list
            new_dial.append(new)

        elif obj["PS"] == "CORR(7,8)": #long
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 18 <Arch>" + sample[-1].split("<Arch>")[1]) #add new turn
            context.append("18 <Arch>" + sample[-1].split("<Arch>")[1])
            new["PS"] = "CORR(17,18)" #add new prediction
            structure += " CORR(17,18)"  #update structure
            moves = '\n'.join(new_sample)

            new["sample"] = moves
            #add to list
            new_dial.append(new)

        elif obj["PS"] == "RES(6,7) CORR(3,7)": #short
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 17 <Buil>" + sample[-1].split("<Buil>")[1]) #add new turn
            #make text chck
            text_check = []
            text_check.extend(context)
            text_check.append("17 <Buil>" + sample[-1].split("<Buil>")[1])
            structure += " RES(16,17) CORR(13,17)"
            text_check.append(structure)
            texts.append("\n".join(text_check))

            context = [] #reset context
            structure = "Structure: "  #reset structure

            new["PS"] = "RES(16,17) CORR(13,17)" #add new prediction
            moves = '\n'.join(new_sample)
            new["sample"] = moves
            #add to list
            new_dial.append(new)
           
        elif obj["PS"] == "RES(6,7) CORR(5,7)": #short
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 17 <Buil>" + sample[-1].split("<Buil>")[1]) #add new turn
            #make text chck
            text_check = []
            text_check.extend(context)
            text_check.append("17 <Buil>" + sample[-1].split("<Buil>")[1])
            structure += " RES(16,17) CORR(15,17)"
            text_check.append(structure)
            texts.append("\n".join(text_check))
          
            context = [] #reset context
            structure = "Structure: "  #reset structure
           
            new["PS"] = "RES(16,17) CORR(15,17)" #add new prediction
            moves = '\n'.join(new_sample)
            new["sample"] = moves
            #add to list
            new_dial.append(new)

        elif obj["PS"] == "RES(8,9) CORR(3,9)": #long
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 19 <Buil>" + sample[-1].split("<Buil>")[1]) #add new turn
            #make text chck
            text_check = []
            text_check.extend(context)
            text_check.append("19 <Buil>" + sample[-1].split("<Buil>")[1])
            structure += " RES(18,19) CORR(13,19)"
            text_check.append(structure)
            texts.append("\n".join(text_check))

            context = [] #reset context
            structure = "Structure: "  #reset structure

            new["PS"] = "RES(18,19) CORR(13,19)" #add new prediction
            moves = '\n'.join(new_sample)
            new["sample"] = moves
            #add to list
            new_dial.append(new)
           
        elif obj["PS"] == "RES(8,9) CORR(5,9)": #long
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 19 <Buil>" + sample[-1].split("<Buil>")[1]) #add new turn
            #make text chck
            text_check = []
            text_check.extend(context)
            text_check.append("19 <Buil>" + sample[-1].split("<Buil>")[1])
            structure += " RES(18,19) CORR(15,19)"
            text_check.append(structure)
            texts.append("\n".join(text_check))

            context = [] #reset context
            structure = "Structure: "  #reset structure

            new["PS"] = "RES(18,19) CORR(15,19)" #add new prediction
            moves = '\n'.join(new_sample)
            new["sample"] = moves
            #add to list
            new_dial.append(new)
        elif obj["PS"] == "RES(8,9) CORR(7,9)": #long
            sample = obj["sample"].split("\n") #pull sample
            new_sample = []
            new_sample.extend(context) #pull in old context
            new_sample.append(structure)
            new_sample.append("New turn: 19 <Buil>" + sample[-1].split("<Buil>")[1]) #add new turn
             #make text chck
            text_check = []
            text_check.extend(context)
            text_check.append("19 <Buil>" + sample[-1].split("<Buil>")[1])
            structure += " RES(18,19) CORR(17,19)"
            text_check.append(structure)
            texts.append("\n".join(text_check))

            context = [] #reset context
            structure = "Structure: "  #reset structure

            new["PS"] = "RES(18,19) CORR(17,19)" #add new prediction
            moves = '\n'.join(new_sample)
            new["sample"] = moves
            #add to list
            new_dial.append(new)



f = open(current_folder + "/synthetic_corrections_long_check_ablations.txt","w")
for d in texts:
    print(d, file=f)
    print('----------------------------\n', file=f)
print("dialogues printed")


#make llamipa jsonl
#convert the dicts into json dicts for json_l
with jsonlines.open(new_long, mode='w') as writer:
    for s in new_dial:
        # sample = {}
        # sample['PS'] = l[1]
        # sample['sample'] = l[0]
        writer.write(s)
print('jsonl saved for {} samples'.format(len(new_dial)))