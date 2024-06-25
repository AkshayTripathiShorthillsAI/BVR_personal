import torch
from datasets import load_dataset
from peft import LoraConfig, PeftModel, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    AutoTokenizer,
    TrainingArguments,
)
from trl import SFTTrainer

import logging
import pandas as pd
from datetime import datetime
import os 

os.environ["TOKENIZERS_PARALLELISM"] = "True"

model_name =  "meta-llama/Meta-Llama-3-8B-Instruct"

log_path = "/home/ankur/projects/llm_test/Akshay/fine_tuning"
finetuned_path = "/home/ankur/projects/llm_test/Akshay/fine_tuning"

train_dataset_json = "/home/ankur/projects/llm_test/Akshay/fine_tuning/bvr_training_set_v3.json"
eval_dataset_json = "/home/ankur/projects/llm_test/Akshay/fine_tuning/bvr_eval_set_v3.json"

# 4 bit quantization 
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
          model_name,
          quantization_config=quant_config,
          device_map="auto",
          attn_implementation="flash_attention_2" # increase gpu inferencing 
        )

tokenizer = AutoTokenizer.from_pretrained(model_name , trust_remote_code=True)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
# tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# peft_model = PeftModel.from_pretrained(model, model_checkpoint)


#Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
# tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"


train_dataset = load_dataset("json", data_files=train_dataset_json, split="train")

train_dataset = train_dataset.map(lambda x: {"formatted_chat": tokenizer.apply_chat_template(x['messages'], tokenize=False, add_generation_prompt=False)})

eval_dataset = load_dataset("json", data_files=eval_dataset_json, split="train")

eval_dataset = eval_dataset.map(lambda x: {"formatted_chat": tokenizer.apply_chat_template(x['messages'], tokenize=False, add_generation_prompt=False)})

train_token = (tokenizer(train_dataset['formatted_chat'])).get('input_ids')
train_token_max = max(len(token) for token in train_token)
# print("\n\n Train max_token_length",max(len(token) for token in train_token))
test_token = (tokenizer(eval_dataset['formatted_chat'])).get('input_ids')
test_token_max = max(len(token) for token in test_token)
# print("\n\n Test max_token_length",max(len(token) for token in test_token))
max_token = max(test_token_max, train_token_max)
print(max_token)#1536


# # Calculate test size based on a percentage of the dataset size
# test_size_percentage = 0.2  # For example, 20% of the dataset
# total_dataset_size = len(dataset)
# test_size = int(total_dataset_size * test_size_percentage)

# split_dataset = dataset.train_test_split(test_size=test_size, seed=42).shuffle()
# print(split_dataset)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
#Load the model and quantize it on the fly
model = AutoModelForCausalLM.from_pretrained(
          model_name,
          quantization_config=bnb_config,
          device_map="auto",
          attn_implementation="flash_attention_2")

#Cast some modules of the model to fp32 
model = prepare_model_for_kbit_training(model)

#Configure the pad token in the model
model.config.pad_token_id = tokenizer.pad_token_id
model.config.use_cache = False # Gradient checkpointing is used by default but not compatible with caching


peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.05,
        r=16,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules= ['k_proj', 'q_proj', 'v_proj', 'o_proj', "gate_proj", "down_proj", "up_proj"]
)


training_arguments = TrainingArguments(
        output_dir=f"{finetuned_path}/llama_3_snippets_v3",
        logging_dir = f"{log_path}/llama_3_snippets_v3",
        num_train_epochs= 4, # 5756 steps 1 hr approx for 4 epochs 
        max_steps = -1 , 
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        gradient_accumulation_steps=6,
        eval_accumulation_steps = 4,
        optim="paged_adamw_8bit",
        save_strategy="epoch",
        logging_strategy="epoch",
        evaluation_strategy="epoch",
        learning_rate= 2e-4,
        fp16= False,
        bf16=  True,
        group_by_length= True,
        disable_tqdm=False,
        # save_total_limit=1,
        overwrite_output_dir =True,
        save_total_limit = 2,
        load_best_model_at_end = True,
        report_to="tensorboard"
        )


trainer = SFTTrainer(
        model=model,
        dataset_text_field="formatted_chat",
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=peft_config,
        max_seq_length=max_token,
        tokenizer=tokenizer,
        args=training_arguments,
)

# trainer.state.best_model_checkpoint
trainer.train()
trainer.save_model()


# trainer.model.save_pretrained(new_model)
# trainer.tokenizer.save_pretrained(new_model)


from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model, AutoPeftModelForCausalLM
del model
del trainer
import gc
gc.collect()
gc.collect()
torch.cuda.empty_cache() # PyTorch thing
gc.collect()
device_map = {"": 0}

# Load the saved model
model = AutoPeftModelForCausalLM.from_pretrained(
    training_arguments.output_dir,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map=device_map,    
)

# Merge LoRA and base model
merged_model = model.merge_and_unload()

# Save the merged model
merged_model.save_pretrained(f"{finetuned_path}/llama3-8b_bvr_v3",safe_serialization=True)
tokenizer.save_pretrained(f"{finetuned_path}/llama3-8b_bvr_v3")