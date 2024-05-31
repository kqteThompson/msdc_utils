import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from datasets import load_dataset
from tqdm import tqdm

device_map = "auto"
model = AutoModelForCausalLM.from_pretrained("/tmpdir/thompson/llama-trois-local",return_dict=True,torch_dtype=torch.float16,device_map=device_map)


# tokenizer = AutoTokenizer.from_pretrained("/tmpdir/thompson/llama-trois-parser")
tokenizer = AutoTokenizer.from_pretrained("/tmpdir/thompson/Meta-Llama-3-8B/",add_eos_token=True) ##special tokens?
# print("Pad token id:",(tokenizer.pad_token_id,model.config.pad_token_id))
# model.config.pad_token_id = tokenizer.pad_token_id

tokenizer.pad_token_id = tokenizer.eos_token_id + 1
tokenizer.padding_side = "right" # Fix weird overflow issue with fp16 training

pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, pad_token_id=tokenizer.pad_token_id, max_new_tokens=100)
print("Padding side:",tokenizer.padding_side)
val_dataset = load_dataset("json", data_files={'val':'/tmpdir/thompson/parser_data/local_model_val.jsonl'})["val"]  
test_dataset = load_dataset("json", data_files={'test':'/tmpdir/thompson/parser_data/local_model_test.jsonl'})["test"]

# def formatting_prompts_func(example):
#      output_texts = []
#      for i in range(len(example['dial_with_actions'])):
#          text = f"Predict the action sequence (AS) for the Minecraft excerpt:\n {example['dial_with_actions'][i]}\n ### AS:"
#          output_texts.append(text)
#      return output_texts

def formatting_prompts_func(example):
     output_texts = []
     for i in range(len(example['sample'])):
         text = f"<|begin_of_text|>Identify the discourse relation (DR) between the following EDUs :\n {example['sample'][i]}\n ### DR:"
         output_texts.append(text)
     return output_texts

val_texts = formatting_prompts_func(val_dataset)
test_texts = formatting_prompts_func(test_dataset)
#train_texts = formatting_prompts_func(train_dataset)

#print("Train Length", len(train_texts))
print("Val Length:", len(val_texts))
print("Test Length:", len(test_texts))

f = open("/tmpdir/thompson/llama-trois-local/val-output-file.txt","w")

for text in tqdm(val_texts):
    print(text)
    print(pipe(text)[0]["generated_text"], file=f)

f.close()

f = open("/tmpdir/thompson/llama-trois-local/test-output-file.txt","w")

for text in tqdm(test_texts):
    print(text)
    print(pipe(text)[0]["generated_text"], file=f)

f.close()

#f = open("/tmpdir/thompson/adapters/train-output-file.txt", "w")
#for text in train_texts:
#	print(text)
#	print(pipe(text)[0]["generated_text"], file=f)
#f.close()
