import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments
)
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM

torch.cuda.empty_cache()

print("1. Cargando modelo y tokenizer...")

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
new_model_name = "qwen_tutor_algoritmos_v2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

dataset = load_dataset(
    "json",
    data_files="tutor_programacion.jsonl",
    split="train"
)


def formatting_prompts_func(example):
    texts = []
    for i in range(len(example["prompt"])):
        text = (
            f"### Pregunta:\n{example['prompt'][i]}\n\n"
            f"### Respuesta esperada:\n{example['response'][i]}{tokenizer.eos_token}"
        )
        texts.append(text)
    return texts


data_collator = DataCollatorForCompletionOnlyLM(
    response_template="### Respuesta esperada:\n",
    tokenizer=tokenizer
)

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.0,   
    bias="none",
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    task_type="CAUSAL_LM"
)

training_args = TrainingArguments(
    output_dir="./resultados_qwen",
    num_train_epochs=12,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=1e-4,   
    bf16=True,
    logging_steps=5,
    save_strategy="no",
    report_to="none",
    optim="adamw_torch"
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    formatting_func=formatting_prompts_func,
    data_collator=data_collator,   
    peft_config=peft_config,
    args=training_args,
    max_seq_length=256,             
    packing=False
)

print("2. Entrenando...")
trainer.train()

print("3. Guardando modelo...")
trainer.model.save_pretrained(new_model_name)
tokenizer.save_pretrained(new_model_name)

print(" Entrenamiento terminado")
