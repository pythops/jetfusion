import io
import os
import sys

import torch
from diffusers import AutoPipelineForText2Image
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address


class Prompt(BaseModel):
    prompt: str


api = FastAPI()
limiter = Limiter(key_func=get_remote_address)


@api.on_event("startup")
async def startup():
    global pipe

    diffusion_model_dir = os.getenv("DIFFUSION_MODEL_DIR")
    if not diffusion_model_dir:
        print("You need to set the DIFFUSION_MODEL_DIR env variable")
        sys.exit(1)

    pipe = AutoPipelineForText2Image.from_pretrained(
        diffusion_model_dir, torch_dtype=torch.float16, variant="fp16"
    )
    pipe.to("cuda")


@api.post("/generate")
@limiter.limit(os.getenv("RATE_LIMIT", "100/minute"))
async def generate(request: Request, prompt: Prompt):
    image = pipe(
        prompt=prompt.prompt, num_inference_steps=1, guidance_scale=0.0
    ).images[0]
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    return Response(buf.getvalue(), media_type="image/jpeg")
