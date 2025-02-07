import os

current_folder=os.getcwd()


# pred_path = current_folder + '/synthetic/test-output-SHORTGEN-nostruct-amended.txt'
# save_results = current_folder + '/synthetic/SHORTGEN-nostruct-amended-anal.txt'

# pred_path = current_folder + '/synthetic/test-output-LONGGEN-nostruct-amended.txt'
# save_results = current_folder + '/synthetic/LONGGEN-nostruct-amended-anal.txt'

# pred_path = current_folder + '/synthetic/synth_correction_SHORT_GEN_test.txt'
# save_results = current_folder + '/synthetic/SHORTGEN-llampia-anal.txt'

pred_path = current_folder + '/synthetic/synth_correction_LONG_GEN_test.txt'
save_results = current_folder + '/synthetic/LONGGEN-llampia-anal.txt'

#get pred output list
with open(pred_path, 'r') as txt:
    text = txt.read().split('\n')

# pred_outputs = []
f = open(save_results,"w")

sample_no = 1
for i, t in enumerate(text):
    if '8 <Arch>' in t and '### DS:' in text[i+1]:
        sample = text[i+1].split('### DS:')[1].strip()
        #pred_outputs.append(str(sample_no) + ' ' + sample)

        print(str(sample_no) + ' ' + sample, file=f)
    # elif '6 <Arch>' in t and 'New turn:' in text[i+1]:
    #     sample = text[i+2].split('### DS:')[1].strip()
    elif '8 <Arch>' in t and 'Structure:' in text[i+1]:
        sample = text[i+3].split('### DS:')[1].strip()

        print(str(sample_no) + ' ' + sample, file=f)
        print('----------------------', file=f)
        # pred_outputs.append(str(sample_no) + ' ' + sample)
        # pred_outputs.append('----------------------')
        sample_no += 1
    