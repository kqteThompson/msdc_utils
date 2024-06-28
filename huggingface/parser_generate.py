import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from datasets import load_dataset
from tqdm import tqdm

device_map = "auto"
model = AutoModelForCausalLM.from_pretrained(
    "/path/to/meta-llama3-8b/",
    return_dict=True,
    torch_dtype=torch.float16,
    device_map=device_map)


tokenizer = AutoTokenizer.from_pretrained("/path/to/meta-llama3-8b/",add_eos_token=True) 

tokenizer.pad_token_id = tokenizer.eos_token_id + 1
tokenizer.padding_side = "right" 

pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, pad_token_id=tokenizer.pad_token_id, max_new_tokens=100)

test_dataset = load_dataset("json", data_files={'test':'/path/to/parser_test_moves_15.jsonl'})["test"]

def is_first_moves(sample):
    answer = 0
    slist = sample.split('\n')
    if slist[0].startswith('Context: 0 <Buil> Mission has started.'):
        struct = [i for i in slist if i.startswith('Structure:')]
        rels = struct[0].split(':')[1].strip()
        if len(rels) == 0:
            answer = 1
    return answer


def check_endpoints(struct, head):
    """
    takes a struct string and a head int and returns only 
    the struct rels with sources that are >= head
    """
    new_rels_list = []
    new_rels = None
    if struct:
        rels = struct.split(' ')
        for rel in rels:
            if len(rel) > 0:
                source = int(rel.split('(')[1].split(',')[0].strip())
                if source >= head:
                    new_rels_list.append(rel)
        if len(new_rels_list) > 0:
            new_rels = ' '.join(new_rels_list)
    return new_rels

def add_previous(sample, previous, predictions):
    new_output = []
    keep_str = None
    #get head
    slist = sample.split('\n')
    head = int(slist[0].split('Context:')[1].split('<')[0].strip())
    # check current structure
    for s in slist:
        if s.startswith('Structure:'):
            new_structure = check_endpoints(previous, head)
            if new_structure:
                s = 'Structure: ' + new_structure + ' ' + predictions
                keep_str = new_structure + ' ' + predictions
            else:
                s = 'Structure: ' + predictions
                keep_str = predictions
        new_output.append(s)
    new_output_string = '\n'.join(new_output)
    return keep_str, new_output_string

def format_gen(preds):
    labels = ['COM','CONTR','CORR','QAP','ACK','ELAB','CLARIFQ','COND','CONTIN',
              'RES','EXPL','QELAB','ALT','NARR','CONFQ','SEQ']
    split_list = [st.strip() for st in preds.split(' ')]
    clean_list = []
    for a in split_list:
        s_tuple = None
        rel = None
        try:
            s = a.split('(')[1].split(')')[0].split(',')
            r = a.split('(')[0].strip()
        except IndexError:
            print('split error one')
        else:
            try:
                s_tuple = (int(s[0]), int(s[1]))
            except IndexError:
                print('split error two')
            except ValueError:
                print('value error three')
            if r in labels:
                #make sure the label is well-formed 
                rel = r
        if rel != None and s_tuple != None:
            clean_list.append(rel + '(' + str(s_tuple[0]) + ',' + str(s_tuple[1]) + ')')
    clean_preds = ' '.join(clean_list)
    return clean_preds


def formatting_prompts_func(example):
    output_text = '<|begin_of_text|>Identify the discourse structure (DS) for the new turn in the following excerpt :\n' + example + '\n ### DS:'
    return output_text


f = open("/path/to/val-output-file.txt","w")

new_generations = None
previous_generations = None
for datum in tqdm(test_dataset['sample']):

    #figure out if it's a first example
    if is_first_moves(datum):
        text = formatting_prompts_func(datum)
        previous_generations = None
    else:
        #need to make sure head edu and relations match up
        update_prev, amended_text = add_previous(datum, previous_generations, new_generations)
        previous_generations = update_prev
        text = formatting_prompts_func(amended_text)
    generated = pipe(text)[0]['generated_text']
    print(generated, file=f)
    new_generations = format_gen(generated.split('### DS:')[1])

f.close()

