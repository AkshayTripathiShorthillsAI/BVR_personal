# pip install -U transformers datasets accelerate peft trl bitsandbytes wandb

#  check gpu compatibility

# Load model
import gc
import os
import torch 
import wandb
from datasets import load_dataset
from google.colab import userdata
from peft import LoraConfig, PeftModel, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
)
from trl import ORPOConfig, ORPOTrainer,  setup_chat_format

import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoConfig

wb_token = userdata.get('wandb')
wandb.login(key= wb_token)

# Prepare Dataset
dataset_name = 'mlabonne/orpo-dpo-mix-40k'
dataset = load_dataset(dataset_name, split="all")
dataset = dataset.shuffle(seed=42).select(range(1000))

def format_chat_template(row):
    row["chosen"] = tokenizer.apply_chat_template(row["chosen"], tokenize= False)
    row["rejected"] = tokenizer.apply_chat_template(row["rejected"], tokenize= False)
    return row

dataset = dataset.map(
    format_chat_template,
    num_proc = os.cpu_count(),
)

dataset = dataset.train_test_split(test_size=0.01)


model_name = "meta-llama/Meta-Llama-3-8B-Instruct"

# Model configuration
model_config = AutoConfig.from_pretrained(
                    model_name,
            use_auth_token=hf_auth
        )

# Quantization configuration
bnb_config = BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16
        )
# Load model
model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            config=model_config,
            # attn_implementation="flash_attention_2",
            quantization_config=bnb_config,
            device_map='auto',
            token=hf_auth
        )

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=hf_auth
        )

# Train the model
orpo_args = ORPOConfig(
    learing_rate = 8e-6,
    beta = 0.1,
    lr_scheduler_type = "linear",
    max_length = 1024,
    max_prompt_length = 512,
    per_device_train_batch_size = 2,
    per_device_eval_batch_size = 2,
    gradient_accumulation_steps = 2,
    optim = "paged_adam_8bit",
    num_train_epochs =1,
    evaluation_strategy = "steps",
    eval_steps = 0.2,
    logging_steps = 1,
    warmup_steps = 10,
    report_to = "wandb",
    output_dir = "./results/",
)

trainer = ORPOTrainer(
    model= model,
    args = orpo_args,
    train_dataset = dataset["train"],
    peft_config = peft_config,
    tokenizer= tokenizer,
)

trainer.train()
trainer.save_model(new_model)