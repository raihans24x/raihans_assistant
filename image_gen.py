# ai_core/image_gen.py

import torch
from diffusers import StableDiffusionPipeline

# লোড করা ১ বারই যথেষ্ট
def load_pipeline():
    model_id = "CompVis/stable-diffusion-v1-4"  # lightweight model
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe = pipe.to("cpu")  # CPU-এ রান করবে
    return pipe

pipe = load_pipeline()

def generate_image(prompt, filename="ai_core/generated.png"):
    image = pipe(prompt).images[0]
    image.save(filename)
    return filename
