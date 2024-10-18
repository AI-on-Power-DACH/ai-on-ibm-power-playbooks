import os
import time

import fastapi
import fastapi.middleware
import fastapi.middleware.cors
import onnxruntime
import pydantic

from optimum.onnxruntime import ORTModelForCausalLM
from transformers import AutoTokenizer

options = onnxruntime.SessionOptions()
options.intra_op_num_threads = 12
model_id = os.environ.get("MODEL_ID", "/app/model_onnx/")
model = ORTModelForCausalLM.from_pretrained(model_id, session_options=options)
tokenizer = AutoTokenizer.from_pretrained(model_id)

origins = [
    "*",
]

app = fastapi.FastAPI()
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerationRequest(pydantic.BaseModel):
    text: str
    max_tokens: int = 256
    stream: bool = False


class GenerationResponse(pydantic.BaseModel):
    generated_text: str
    generated_token_count: int
    input_token_count: int


def get_tokens(generated_tokens) -> int:
    num_generated_tokens = generated_tokens.shape[1]
    print(f"Number of tokens in generated text: {num_generated_tokens}")
    return num_generated_tokens


@app.post("/generate")
def generate(request: GenerationRequest) -> GenerationResponse:
    inputs = tokenizer(request.text, return_tensors="pt").input_ids

    start = time.time()
    outputs = model.generate(inputs, max_new_tokens=request.max_tokens)  # max_length will also include the input tokens!
    end = time.time()
    
    generated_text = tokenizer.batch_decode(outputs)[0]
    print(generated_text)
    seconds = end - start
    number_tokens = get_tokens(outputs)
    print(f"Running at ~{number_tokens/seconds:.2f} tokens/second")

    return GenerationResponse(
        generated_text=generated_text,
        generated_token_count=number_tokens,
        input_token_count=inputs.shape[1],
    )
