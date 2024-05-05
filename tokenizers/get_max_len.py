from datasets import load_dataset
from transformers import AutoTokenizer
import numpy as np

tokenizer_path = '/home/kate/minecraft_utils/tokenizers/llama_2_tokenizer/'

print("loading dataset....")
train_dataset = load_dataset("json", data_files={'train':'/home/kate/minecraft_utils/llm_annotator/parser_test_moves_15.jsonl'})["train"]
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

print("creating train texts")
train_texts = formatting_prompts_func(train_dataset)

tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

print("getting lens of tokenized")
l = []
# count = 0
for text in train_texts:
    l.append(len(tokenizer(text)["input_ids"]))
    # count += 1

    # if count%100 == 0:
    #     print('count: ', count)

print(f"Max seq length {np.max(l)}")

