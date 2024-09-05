import os
import jsonlines


def get_links(sample_string, sample_index):
    """
    takes a sample string and returns a list of attach tuples
    and a list of rel type strings
    """
    #MINECRAFT labels
    labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
              'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ']
    

    split_list = [st.strip() for st in sample_string.split(' ')]
   
    rel_list = []
    attach_list = []
    for a in split_list:
        s_tuple = None
        rel = None
        try:
            s = a.split('(')[1].split(')')[0].split(',')
            r = a.split('(')[0].strip()
        except IndexError:
            print('split error at ', sample_index)
        else:
            try:
                s_tuple = (int(s[0]), int(s[1]))
            except IndexError:
                print('split error at ', sample_index)
            except ValueError:
                print('value error at ', sample_index)
            if r in labels:
                #make sure the label is well-formed 
                rel = r
    
        # if rel != None and s_tuple != None and (s_tuple[1] - s_tuple[0]) >= 10:
        if rel != None and s_tuple != None:
            attach_list.append((int(s[0]), int(s[1])))
            rel_list.append(r)
    
    #re-construct the full list 
    #a list of tuples (rel, x, y)
    #but don't allow doubles!!
    full_list = []
    endpoints = [] 
    for i, r in enumerate(attach_list):
        if r not in endpoints:
            endpoints.append(r)
            full_list.append((rel_list[i], r[0], r[1]))   
    return endpoints, full_list
    
#MINECRAFT LABELS
# labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
#               'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ','NULL']


def amend_samp(gs, struct):
    """
    add structures to gold samples
    """
    new_elements = []
    elems = gs.split('\n')
    for elem in elems:
        if 'Structure:' in elem:
            newstruct = 'Structure:'
            newstruct += struct
            new_elements.append(newstruct)
        else:
            new_elements.append(elem)
    new_elements_str = '\n'.join(new_elements)
    return new_elements_str


def triangle_check(sources, structure):
    changes = 0
    rel_list = []
    for rel in structure.split(' '):
        if rel.split('(')[0] in ['CORR']:
            #check for source
            t = int(rel.split(',')[0].split('(')[1])
            if t not in sources:
                rel_list.append(rel.strip())
            else:
                #change to ACK
                nrel = 'ACK(' + rel.split('(')[1]
                rel_list.append(nrel)
                changes += 1
        else:
            rel_list.append(rel.strip())
    rel_list_str = ' '.join(rel_list)
    return rel_list_str, changes

current_folder=os.getcwd()

gold_path = current_folder + '/parser_val_moves_15.jsonl'
pred_path = current_folder + '/val-output-generate-file-llama3.txt'
# pred_path = current_folder + '/val-output-file.txt'
save_path = current_folder + '/parser_val_moves_15_correction_abl.jsonl'


#get pred output list
with open(pred_path, 'r') as txt:
    text = txt.read().split('\n')

pred_outputs = []
pred_structures = []

for t in text:
    if '### DS:' in t:
        sample = t.split('### DS:')[1].strip()
        pred_outputs.append(sample)
    elif 'Structure:' in t:
        s = t.split('Structure:')[1]
        pred_structures.append(s)

assert len(pred_outputs) == len(pred_structures)

#get gold sample list
gold_outputs = []
gold_samples = []

with jsonlines.open(gold_path) as reader:
    for obj in reader:
        gold_outputs.append(obj['PS'])
        gold_samples.append(obj['sample'])

assert len(gold_outputs) == len(gold_samples)

# fulljson = []

# with jsonlines.open(gold_path) as reader:
#     for obj in reader:
#         fulljson.append(obj)

#list of indexes for QAP
total_changed = 0
total_corrections_found = 0
new_json = []
for i, s in enumerate(pred_outputs):
    #first do attachments
    pred_att, pred_all = get_links(s, i)
    gold_att, gold_all = get_links(gold_outputs[i], i)

    # print("GOLD:", gold_all)
    # print("PRED:", pred_all)
    # print('-------')
    CORR_sources = []
    pst = pred_structures[i]
 
    for s in pred_all:
        if 'CORR' in s:
            if s in gold_all:
                # print('correct correction: ', i)
                #then we have a correct correction
                total_corrections_found += 1
                source = int(s[1]) #this will be the source shared by the CORR in the structure. 
                CORR_sources.append(source)
    if len(CORR_sources) > 0:
        new_st, num_changes = triangle_check(CORR_sources, pst)
        total_changed += num_changes
        # print(total_changed)
        # print(new_st)
        # print('----------------------------')
        new_samp = amend_samp(gold_samples[i], new_st)
        sampj = {}
        sampj['PS'] = gold_outputs[i]
        sampj['sample'] = new_samp
        new_json.append(sampj)
    else:
        new_samp = amend_samp(gold_samples[i], pst)
        sampj = {}
        sampj['PS'] = gold_outputs[i]
        sampj['sample'] = new_samp
        new_json.append(sampj)
                

print('len orig. json: ', len(gold_samples))
print('len new json: ', len(new_json))

print('total changed: ', total_changed)
print('total corrections found: ', total_corrections_found)
#convert the dicts into json dicts for json_l
with jsonlines.open(save_path, mode='w') as writer:
    for l in new_json:
        writer.write(l)

#total corrections found: 280
#total corrections changed to ack: 139