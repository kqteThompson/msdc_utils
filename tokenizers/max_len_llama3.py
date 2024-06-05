from datasets import load_dataset
from transformers import AutoTokenizer
import numpy as np

tokenizer_path = '/home/kate/minecraft_utils/tokenizers/llama3/'

print("loading dataset....")
train_dataset = load_dataset("json", data_files={'train':'/home/kate/minecraft_utils/llm_annotator/local_model_train.jsonl'})["train"]
# def formatting_prompts_func(example):
#      output_texts = []
#      for i in range(len(example['dial_with_actions'])):
#          text = f"Predict the action sequence (AS) for the Minecraft excerpt:\n {example['dial_with_actions'][i]}\n ### AS:\n {example['action_seq'][i]}"
#          output_texts.append(text)
#      return output_texts

# def formatting_prompts_func(example):
#      output_texts = []
#      for i in range(len(example['sample'])):
#          text = f"Identify the discourse structure (DS) for the new turn in the following excerpt :\n {example['sample'][i]}\n ### DS: {example['PS'][i]}"
#          output_texts.append(text)
#      return output_texts

def formatting_prompts_func(example):
     output_texts = []
     for i in range(len(example['sample'])):
         if i%1000==0:
             print(i)
         text = f"<|begin_of_text|>Identify the discourse relation (DR) between the following EDUs :\n {example['sample'][i]}\n ### DR: {example['PS'][i]}<|end_of_text|>"
         output_texts.append(text)
     return output_texts


print("creating train texts")
print(len(train_dataset), " texts total")
max_seq_lengths = []
n = 0
for seg in range(0, 85):
    train_texts = formatting_prompts_func(train_dataset[n:n+1000])

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, add_eos_token=True) ##special tokens?
    tokenizer.pad_token_id = tokenizer.eos_token_id + 1
    tokenizer.padding_side = "right" # Fix weird overflow issue with fp16 training

    print("getting lens of tokenized")
    l = []
    # count = 0
    for text in train_texts:
        l.append(len(tokenizer(text)["input_ids"]))
        # count += 1

        # if count%100 == 0:
        #     print('count: ', count)
    max_seq_lengths.append(np.max(l))
    print(f"Max seq length {np.max(l)}")

    n += 1000

print('max of max: {}'.format(np.max(max_seq_lengths)))
