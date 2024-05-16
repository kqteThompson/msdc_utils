import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from datasets import load_dataset
from tqdm import tqdm

#device_map = {"": 0}
device_map = "auto"
model = AutoModelForCausalLM.from_pretrained("/tmpdir/chaturve/llama-3-8b-minecraft-actseq-narr-V3",low_cpu_mem_usage=True, return_dict=True,torch_dtype=torch.float16,device_map=device_map)
tokenizer = AutoTokenizer.from_pretrained("/tmpdir/chaturve/llama-3-8b-minecraft-actseq-narr-V3")
print("Pad token id:",(tokenizer.pad_token_id,model.config.pad_token_id))
model.config.pad_token_id = tokenizer.pad_token_id
#pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, pad_token_id=tokenizer.pad_token_id, max_length=4096)
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, pad_token_id=tokenizer.pad_token_id, max_new_tokens=100)
print("Padding side:",tokenizer.padding_side)
#val_dataset = load_dataset("csv", data_files={'val':'/tmpdir/chaturve/minecraft_data/narration/actseq-val-narr-new2.csv'})["val"]
#val_dataset = load_dataset("csv", data_files={'val':'/tmpdir/chaturve/minecraft_data/narration/actseq-val-narr-V3.csv'})["val"]
test_dataset = load_dataset("csv", data_files={'test':'/tmpdir/chaturve/minecraft_data/narration/actseq-test-narr-V3.csv'})["test"]


def formatting_prompts_func(example):
     output_texts = []
     for i in range(len(example['dial_with_actions'])):
         text = f"<|begin_of_text|>Predict the action sequence (AS) for the Minecraft excerpt:\n {example['dial_with_actions'][i]}\n ### AS:"
         output_texts.append(text)
     return output_texts


#val_texts = formatting_prompts_func(val_dataset)
test_texts = formatting_prompts_func(test_dataset)

#print("Val Length:", len(val_texts))
print("Test Length:", len(test_texts))

#f = open("/tmpdir/chaturve/llama-3-8b-minecraft-actseq-narr-V3/llama_val_output.txt","w")

#for text in tqdm(val_texts):
#    print(text)
#    s = pipe(text)[0]["generated_text"]
#    s_trunc = s.split("### AS:")[1]
#    print("Length:",len(tokenizer(s_trunc)["input_ids"]))
#    print(s, file=f)

#f.close()

f = open("/tmpdir/chaturve/llama-3-8b-minecraft-actseq-narr-V3/llama_test_output.txt","w")

for text in tqdm(test_texts):
    print(text)
    print(pipe(text)[0]["generated_text"], file=f)

f.close()
