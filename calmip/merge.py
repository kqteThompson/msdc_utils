import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from datasets import load_dataset
from peft import LoraConfig, PeftModel

device_map = "auto"
model = AutoModelForCausalLM.from_pretrained(
    "/tmpdir/thompson/llama-2-13b-hf/",
    return_dict=True,
    torch_dtype=torch.float16,
    device_map=device_map,
)

model = PeftModel.from_pretrained(model, "/tmpdir/thompson/adapters", device_map=device_map)
model = model.merge_and_unload()

tokenizer = AutoTokenizer.from_pretrained("/tmpdir/thompson/llama-2-13b-hf/", trust_remote_code=True)
tokenizer.pad_token_id = 18610

pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=4096, do_sample=False)
print("Padding side:",tokenizer.padding_side)
val_dataset = load_dataset("csv", data_files={'val':'/tmpdir/thompson/minecraft/actseq-val-narr-V3.csv'})["val"]
test_dataset = load_dataset("csv", data_files={'test':'/tmpdir/thompson/minecraft/actseq-test-narr-V3.csv'})["test"]
#train_dataset = load_dataset("csv", data_files={'train':'/tmpdir/thompson/minecraft/actseq-train-narr-small-v2.csv'})["train"]

def formatting_prompts_func(example):
     output_texts = []
     for i in range(len(example['dial_with_actions'])):
         text = f"Predict the action sequence (AS) for the Minecraft excerpt:\n {example['dial_with_actions'][i]}\n ### AS:"
         output_texts.append(text)
     return output_texts

val_texts = formatting_prompts_func(val_dataset)
test_texts = formatting_prompts_func(test_dataset)
#train_texts = formatting_prompts_func(train_dataset)

#print("Train Length", len(train_texts))
print("Val Length:", len(val_texts))
print("Test Length:", len(test_texts))

f = open("/tmpdir/thompson/adapters/val-output-file.txt","w")

for text in val_texts:
    print(text)
    print(pipe(text)[0]["generated_text"], file=f)

f.close()

f = open("/tmpdir/thompson/adapters/test-output-file.txt","w")

for text in test_texts:
    print(text)
    print(pipe(text)[0]["generated_text"], file=f)

f.close()

#f = open("/tmpdir/thompson/adapters/train-output-file.txt", "w")
#for text in train_texts:
#	print(text)
#	print(pipe(text)[0]["generated_text"], file=f)
#f.close()
