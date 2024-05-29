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
    # EarlyStoppingCallback,
)
from peft import LoraConfig, PeftModel
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM


# The model that you want to train from the Hugging Face hub
# model_name = "llama-2-13b-hf"
model_name = "Meta-Llama-3-8B"

# Fine-tuned model name
new_model = "/tmpdir/thompson/llama-trois-parser_stac"

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
num_train_epochs = 4

# Enable fp16/bf16 training (set bf16 to True with an A100)
fp16 = False
bf16 = False

# Batch size per GPU for training
per_device_train_batch_size = 1

# Batch size per GPU for evaluation
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
max_seq_length = 4096
# max_new_tokens = 100 

# Pack multiple short examples in the same input sequence to increase efficiency
packing = False

# Load the entire model on the GPU 0
# device_map = {"": 0}
device_map = "auto"
# Load dataset (you can process it here)
# The instruction dataset to use
dataset = load_dataset("json", data_files={'train':'/tmpdir/thompson/parser_data/parser_stac_train_15.jsonl'})["train"]
#val_dataset = load_dataset("json", data_files={'val':'/tmpdir/thompson/parser_data/parser_val_stacsquish_15.jsonl'})["val"]

#dataset = dataset.select(range(300))

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
# model = AutoModelForCausalLM.from_pretrained("/tmpdir/thompson/llama-2-13b-hf/",quantization_config=bnb_config,device_map=device_map)
model = AutoModelForCausalLM.from_pretrained("/tmpdir/thompson/Meta-Llama-3-8B/",quantization_config=bnb_config,device_map=device_map)
model.config.use_cache = False
model.config.pretraining_tp = 1

# Load LLaMA tokenizer
#tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
# tokenizer = AutoTokenizer.from_pretrained("/tmpdir/thompson/llama-2-13b-hf/",add_eos_token=True)
tokenizer = AutoTokenizer.from_pretrained("/tmpdir/thompson/Meta-Llama-3-8B/",add_eos_token=True) ##special tokens?
#tokenizer.pad_token = tokenizer.eos_token
# this should be set for finutning and batched inference
#tokenizer.add_special_tokens({"pad_token": "<PAD>"})
#model.resize_token_embeddings(len(tokenizer))
# tokenizer.pad_token_id = 18610 
tokenizer.pad_token_id = tokenizer.eos_token_id + 1
tokenizer.padding_side = "right" # Fix weird overflow issue with fp16 training
print("Model embedding shape:",model.model.embed_tokens.weight.shape)
print("Model lm_head shape:",model.lm_head.weight.shape)

def formatting_prompts_func(example):
     output_texts = []
     for i in range(len(example['sample'])):
         text = f"<|begin_of_text|>Identify the discourse structure (DS) for the new turn in the following excerpt :\n {example['sample'][i]}\n ### DS: {example['PS'][i]}<|end_of_text|>"
         output_texts.append(text)
     return output_texts
#response_template = "\n ### Answer:"
#collator = DataCollatorForCompletionOnlyLM(response_template, tokenizer=tokenizer)
response_template_with_context = "\n ### DS:"  # We added context here: "\n". This is enough for this tokenizer
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
    # metric_for_best_model="eval_loss", 
    # load_best_model_at_end=True, 
    # evaluation_strategy="epoch", 
    # save_strategy="epoch",
)

# Set supervised fine-tuning parameters
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    # eval_dataset=val_dataset,
    formatting_func=formatting_prompts_func,
    data_collator=collator,
    peft_config=peft_config,
    max_seq_length=max_seq_length, 
    tokenizer=tokenizer,
    args=training_arguments,
    packing=packing,
    # callbacks=[EarlyStoppingCallback(3, 0.0)],
)

# Train model
trainer.train()

# Save trained model
trainer.model.save_pretrained(new_model)

# print("evaluating")
# result = trainer.evaluate()
# print(result)
# print("evaluation done")

# Ignore warnings
logging.set_verbosity(logging.CRITICAL)

# Run text generation pipeline with our next model
prompt = "<|begin_of_text|>Identify the discourse structure (DS) for the new turn in the following excerpt:\n Context: 0 <Server> It's Tyrant Lord's turn to roll the dice.\n1 <Server> Tyrant Lord rolled a 2 and a 4.\n2 <Server> nelsen gets 1 wood. sparkles gets 1 ore. Tyrant Lord gets 1 wood.\n3 <UI> nelsen has 7 resources. Kersti has 3 resources. sparkles has 3 resources. Tyrant Lord has 6 resources.\nStructure: RES(0,1) RES(1,2) RES(2,3)\nNew Turn: 4 <Tyrant> my wood or wheat for caly or ore anyone? \n ### DS:"
#prompt = "<|begin_of_text|>Identify the discourse structure (DS) for the new turn in the following excerpt:\n Context: 0 <Buil> Mission has started .\n1 <Arch> alright ,\n2 <Arch> start with a row of 5 orange ones on the ground\n3 <Arch> any direction\n4 <Arch> near the center preferably\nStructure: ACK(0,1) CONTIN(0,2) ELAB(2,3) ELAB(3,4)\nNew Turn: 5 <Buil> I was just about to ask \n ### DS:"
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
    # "/tmpdir/thompson/llama-2-13b-hf/",
    "/tmpdir/thompson/Meta-Llama-3-8B/",
    #low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map=device_map,
    # device_map={"": "cpu"},
)
# model = PeftModel.from_pretrained(base_model, new_model, device_map={"": "cpu"})
model = PeftModel.from_pretrained(base_model, new_model, device_map=device_map)
model = model.merge_and_unload()
model.config.pad_token_id = tokenizer.pad_token_id
print("Device:",model.hf_device_map)
print("Pad token:", (model.config.pad_token_id, tokenizer.pad_token_id))

# output_merged_dir = "/tmpdir/thompson/llama-2-13b-parser"
output_merged_dir = "/tmpdir/thompson/llama-trois-parser_stac"
os.makedirs(output_merged_dir, exist_ok=True)
model.save_pretrained(output_merged_dir, safe_serialization=True)


# Reload tokenizer to save it
# tokenizer = AutoTokenizer.from_pretrained("/tmpdir/thompson/llama-2-13b-hf/", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("/tmpdir/thompson/Meta-Llama-3-8B/", trust_remote_code=True)
#tokenizer.pad_token = tokenizer.eos_token
# tokenizer.pad_token_id = 18610 
tokenizer.pad_token = tokenizer.eos_token + 1
#tokenizer.add_special_tokens({"pad_token": "<PAD>"})
#tokenizer.padding_side = "right"
tokenizer.save_pretrained(output_merged_dir)
