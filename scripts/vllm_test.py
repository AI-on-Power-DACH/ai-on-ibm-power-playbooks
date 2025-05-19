#!/usr/bin/env python
import os

from openai import OpenAI

def test_predict():

    # Modify OpenAI's API key and API base to use vLLM's API server.
    openai_api_key = os.getenv("VLLM_API_KEY") or "examplekey01"
    openai_api_base = os.getenv("VLLM_URL") or "http://localhost:8080/v1"
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )
    completion = client.completions.create(model="ibm-granite/granite-3.3-8b-instruct",
                                        prompt="San Francisco is a")
    print("Completion result:", completion)
    

if __name__ == "__main__":
    test_predict()