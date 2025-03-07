from PIL import Image
import os
from transformers import AutoModelForCausalLM, AutoProcessor
import torch

model_id = "microsoft/Phi-3-vision-128k-instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    device_map="cpu",  # probar GPU
    trust_remote_code=True, 
    torch_dtype="auto", 
    _attn_implementation="eager"
 
)
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

messages = [
    {"role": "user", "content": "<|image_1|>\nQue se muestra en la imagen?"},
]

image_path = "./images/page_7.png"  
if not os.path.exists(image_path):
    raise FileNotFoundError(f"La imagen no existe en la ruta: {image_path}")

image = Image.open(image_path)


prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# Procesar los inputs (prompt + imagen)
inputs = processor(prompt, [image], return_tensors="pt").to("cpu")


generation_args = {
    "max_new_tokens": 500,
    "temperature": 0.0,
    "do_sample": False,
}

generate_ids = model.generate(**inputs, eos_token_id=processor.tokenizer.eos_token_id, **generation_args)

generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

print("Respuesta generada:")
print(response)
