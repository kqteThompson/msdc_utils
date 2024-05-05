from datasets import load_dataset
from transformers import AutoTokenizer
import numpy as np

train_dataset = load_dataset("json", data_files={'train':'/home/kate/minecraft_utils/llm_annotator/parser_train.jsonl'})["train"]
# def formatting_prompts_func(example):
#      output_texts = []
#      for i in range(len(example['dial_with_actions'])):
#          text = f"Predict the action sequence (AS) for the Minecraft excerpt:\n {example['dial_with_actions'][i]}\n ### AS:\n {example['action_seq'][i]}"
#          output_texts.append(text)
#      return output_texts

def formatting_prompts_func(example):
     output_texts = []
     for i in range(len(example['sample'])):
         text = f"Identify the discourse structure (DS) for the new turn in the following excerpt :\n {example['sample'][i]}\n ### DS: {example['PS'][i]}"
         output_texts.append(text)
     return output_texts

train_texts = formatting_prompts_func(train_dataset)

tokenizer = AutoTokenizer.from_pretrained("/home//llama-2-7b-hf")

l = []
for text in train_texts:
    l.append(len(tokenizer(text)["input_ids"]))

print(f"Max seq length {np.max(l)}")

