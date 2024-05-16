import os
import torch
import gc
from datasets import load_dataset, concatenate_datasets
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
    EarlyStoppingCallback,
)
from peft import LoraConfig, PeftModel
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM

# The model that you want to train from the Hugging Face hub
#model_name = "NousResearch/Llama-2-7b-chat-hf"
model_name = "llama-3-8b-hf"

# Fine-tuned model name
#new_model = "llama-2-7b-miniguanaco"
new_model = "/tmpdir/chaturve/llama-3-8b-minecraft-actseq-narr-V3"

################################################################################
# QLoRA parameters
################################################################################

# LoRA attention dimension
lora_r = 64

# Alpha parameter for LoRA scaling
lora_alpha = 16

# Dropout probability for LoRA layers
lora_dropout = 0.1

################################################################################
# bitsandbytes parameters
################################################################################

# Activate 4-bit precision base model loading
use_4bit = True

# Compute dtype for 4-bit base models
bnb_4bit_compute_dtype = "float16"

# Quantization type (fp4 or nf4)
bnb_4bit_quant_type = "nf4"

# Activate nested quantization for 4-bit base models (double quantization)
use_nested_quant = False

################################################################################
# TrainingArguments parameters
################################################################################

# Output directory where the model predictions and checkpoints will be stored
output_dir = "./results"

# Number of training epochs
#num_train_epochs = 1
num_train_epochs = 3

# Enable fp16/bf16 training (set bf16 to True with an A100)
fp16 = False
bf16 = False

# Batch size per GPU for training
#per_device_train_batch_size = 4
per_device_train_batch_size = 1

# Batch size per GPU for evaluation
#per_device_eval_batch_size = 4
per_device_eval_batch_size = 2

# Number of update steps to accumulate the gradients for
gradient_accumulation_steps = 1

# Enable gradient checkpointing
gradient_checkpointing = True

# Maximum gradient normal (gradient clipping)
max_grad_norm = 0.3

# Initial learning rate (AdamW optimizer)
learning_rate = 2e-4

# Weight decay to apply to all layers except bias/LayerNorm weights
weight_decay = 0.001

# Optimizer to use
optim = "paged_adamw_32bit"

# Learning rate schedule
lr_scheduler_type = "cosine"

# Number of training steps (overrides num_train_epochs)
max_steps = -1

# Ratio of steps for a linear warmup (from 0 to learning rate)
warmup_ratio = 0.03

# Group sequences into batches with same length
# Saves memory and speeds up training considerably
group_by_length = True

# Save checkpoint every X updates steps
save_steps = 0

# Log every X updates steps
logging_steps = 25

################################################################################
# SFT parameters
################################################################################

# Maximum sequence length to use
#max_seq_length = None
max_seq_length = 4096
#max_seq_length = 2048

# Pack multiple short examples in the same input sequence to increase efficiency
packing = False

# Load the entire model on the GPU 0
#device_map = {"": 0}
device_map = "auto"

# Load dataset (you can process it here)
# The instruction dataset to use
#dataset = load_dataset("json","/tmpdir/chaturve/FOLIO/folio_v2_train.jsonl",split="train")
#dataset = load_dataset("csv", data_files={'train':'/tmpdir/chaturve/minecraft_data/actseq-train.csv'})["train"]
dataset = load_dataset("csv", data_files={'train':'/tmpdir/chaturve/minecraft_data/narration/actseq-train-narr-V3.csv'})["train"]
#dataset = load_dataset("csv", data_files={'train':'/tmpdir/chaturve/minecraft_data/actseq-train-new.csv'})["train"]
#dataset = dataset.select(range(1000))
#dataset = dataset.select([i for i in range(len(dataset)) if i not in range(2972,2981)])

# Load tokenizer and model with QLoRA configuration
compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=use_4bit,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=use_nested_quant,
)

# Check GPU compatibility with bfloat16
if compute_dtype == torch.float16 and use_4bit:
    major, _ = torch.cuda.get_device_capability()
    if major >= 8:
        print("=" * 80)
        print("Your GPU supports bfloat16: accelerate training with bf16=True")
        print("=" * 80)

# Load base model
#model = AutoModelForCausalLM.from_pretrained(
#    model_name,
#    quantization_config=bnb_config,
#    device_map=device_map
#)
model = AutoModelForCausalLM.from_pretrained("/tmpdir/chaturve/llama-3-8b-hf/",quantization_config=bnb_config,device_map=device_map)
model.config.use_cache = False
model.config.pretraining_tp = 1

# Load LLaMA tokenizer
#tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("/tmpdir/chaturve/llama-3-8b-hf/",add_eos_token=True)
#tokenizer.pad_token = tokenizer.eos_token
# this should be set for finutning and batched inference
#tokenizer.add_special_tokens({"pad_token": "<PAD>"})
#model.resize_token_embeddings(len(tokenizer))
#tokenizer.pad_token_id = 18610 
tokenizer.pad_token_id = tokenizer.eos_token_id + 1
tokenizer.padding_side = "right" # Fix weird overflow issue with fp16 training
print("Model embedding shape:",model.model.embed_tokens.weight.shape)
print("Model lm_head shape:",model.lm_head.weight.shape)
#with torch.no_grad():
#    mean_cutoff = 128000
#    dtype = torch.bfloat16
#    for token_id in range(mean_cutoff, mean_cutoff+3):
#        token = tokenizer.decode(token_id)
#        print (f"Token {token} ID {token_id}")
#        print("Before:")
#        print(model.model.embed_tokens.weight[token_id])
#        print(model.lm_head.weight[token_id])
#        model.model.embed_tokens.weight[token_id] = torch.mean(model.model.embed_tokens.weight[:mean_cutoff].to(torch.float32), dim=0).to(dtype)
#        model.lm_head.weight[token_id] = torch.mean(model.lm_head.weight[:mean_cutoff].to(torch.float32), dim=0).to(dtype)
#        print("After:")
#        print(model.model.embed_tokens.weight[token_id])
#        print(model.lm_head.weight[token_id])

def formatting_prompts_func(example):
     output_texts = []
     for i in range(len(example['dial_with_actions'])):
         text = f"<|begin_of_text|>Predict the action sequence (AS) for the Minecraft excerpt:\n {example['dial_with_actions'][i]}\n ### AS: {example['action_seq'][i]}<|end_of_text|>" 
         output_texts.append(text)
     return output_texts
#response_template = "\n ### Answer:"
#collator = DataCollatorForCompletionOnlyLM(response_template, tokenizer=tokenizer)
response_template_with_context = "\n ### AS:"  # We added context here: "\n". This is enough for this tokenizer
response_template_ids = tokenizer.encode(response_template_with_context, add_special_tokens=False)[2:] 
collator = DataCollatorForCompletionOnlyLM(response_template_ids, tokenizer=tokenizer)

# Load LoRA configuration
peft_config = LoraConfig(
    lora_alpha=lora_alpha,
    lora_dropout=lora_dropout,
    r=lora_r,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj"],
#    modules_to_save= ["embed_tokens", "lm_head"],
)

# Set training parameters
training_arguments = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=num_train_epochs,
    per_device_train_batch_size=per_device_train_batch_size,
    gradient_accumulation_steps=gradient_accumulation_steps,
    optim=optim,
    save_steps=save_steps,
    logging_steps=logging_steps,
    learning_rate=learning_rate,
    weight_decay=weight_decay,
    fp16=fp16,
    bf16=bf16,
    max_grad_norm=max_grad_norm,
    max_steps=max_steps,
    warmup_ratio=warmup_ratio,
    group_by_length=group_by_length,
    lr_scheduler_type=lr_scheduler_type,
)

# Set supervised fine-tuning parameters
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    formatting_func=formatting_prompts_func,
    data_collator=collator,
    peft_config=peft_config,
    max_seq_length=max_seq_length,
    tokenizer=tokenizer,
    args=training_arguments,
    packing=packing,
)

# Train model
trainer.train()

# Save trained model
trainer.model.save_pretrained(new_model)

# Ignore warnings
logging.set_verbosity(logging.CRITICAL)

# Run text generation pipeline with our next model
prompt = "<|begin_of_text|>Predict the action sequence (AS) for the following Minecraft excerpt:\n <Builder> Mission has started.\n<Architect> this one looks like a bridge\n<Architect> it will be 10 block long and 4 blocks wide so make sure to leave enough space\n<Architect> start by building a row of 2 red blocks even with the edge at one edge of the base\n ### AS:"
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
result = pipe(f"{prompt}")
print(result[0]['generated_text'])

# Empty VRAM
del model
del pipe
del trainer
gc.collect()
gc.collect()


# Reload model in FP16 and merge it with LoRA weights
base_model = AutoModelForCausalLM.from_pretrained(
    "/tmpdir/chaturve/llama-3-8b-hf/",
    #low_cpu_mem_usage=True,
    return_dict=True,
    #load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map=device_map,
    #device_map={"": "cpu"},
)

#with torch.no_grad():
#    mean_cutoff = 128000
#    dtype = torch.bfloat16
#    for token_id in range(mean_cutoff, mean_cutoff+3):
#        token = tokenizer.decode(token_id)
#        print (f"Token {token} ID {token_id}")
#        base_model.model.embed_tokens.weight[token_id] = torch.mean(base_model.model.embed_tokens.weight[:mean_cutoff].to(torch.float32), dim=0).to(dtype)
#        base_model.lm_head.weight[token_id] = torch.mean(base_model.lm_head.weight[:mean_cutoff].to(torch.float32), dim=0).to(dtype)

model = PeftModel.from_pretrained(base_model, new_model,  device_map=device_map)
model = model.merge_and_unload()
model.config.pad_token_id = tokenizer.pad_token_id
print("Device:",model.hf_device_map)
print("Pad token:", (model.config.pad_token_id, tokenizer.pad_token_id))
#model = model.to("cpu")
#print("Device now:",model.hf_device_map)

output_merged_dir = "/tmpdir/chaturve/llama-3-8b-minecraft-actseq-narr-V3"
os.makedirs(output_merged_dir, exist_ok=True)
model.save_pretrained(output_merged_dir, safe_serialization=True)


# Reload tokenizer to save it
tokenizer = AutoTokenizer.from_pretrained("/tmpdir/chaturve/llama-3-8b-hf/", trust_remote_code=True)
#tokenizer.pad_token = tokenizer.eos_token
#tokenizer.pad_token_id = 18610 
tokenizer.pad_token_id = tokenizer.eos_token_id + 1
#tokenizer.add_special_tokens({"pad_token": "<PAD>"})
#tokenizer.padding_side = "right"
tokenizer.save_pretrained(output_merged_dir)
