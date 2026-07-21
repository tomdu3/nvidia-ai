import os
from dotenv import load_dotenv
from openai import OpenAI
from output_format import OutputFormatter

# import environment variables
load_dotenv(override=True)
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

formatter = OutputFormatter(save_file=True)

try:
    if not NVIDIA_API_KEY:
        raise ValueError("NVIDIA_API_KEY is not set in environment or .env file.")

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY,
    )

    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=[
            {
                "role": "user",
                "content": "Can you tell me what is the best way to learn machine learning with ai. Give me some online references, youtube tutorials and ai tools I can use for free.",
            }
        ],
        temperature=1,
        top_p=0.95,
        max_tokens=16384,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": True},
            "reasoning_budget": 16384,
        },
        stream=True,
    )

    for chunk in completion:
        if not chunk.choices:
            continue

        reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None) or getattr(
            chunk.choices[0].delta, "reasoning", None
        )
        if reasoning:
            formatter.print_reasoning(reasoning)

        if chunk.choices[0].delta.content is not None:
            formatter.print_content(chunk.choices[0].delta.content)

    formatter.finish()

except Exception as e:
    formatter.print_error(str(e))
