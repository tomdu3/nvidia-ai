import os
from dotenv import load_dotenv
from openai import OpenAI
from output_format import OutputFormatter

# Load environment variables
load_dotenv(override=True)


def stream_chat(
    task: str,
    model: str = "nvidia/nemotron-3-super-120b-a12b",
    temperature: float = 1.0,
    top_p: float = 0.95,
    max_tokens: int = 16384,
    enable_thinking: bool = True,
    reasoning_budget: int = 16384,
    save_file: bool = True,
) -> str:
    """
    Sends a prompt to the NVIDIA OpenAI-compatible API and streams the response.
    Saves the reasoning and final content to a file using OutputFormatter.
    Returns the path to the saved file (if save_file is True) or the generated response content.
    """
    nvidia_api_key = os.getenv("NVIDIA_API_KEY")
    if not nvidia_api_key:
        raise ValueError("NVIDIA_API_KEY is not set in environment or .env file.")

    formatter = OutputFormatter(save_file=save_file)
    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=nvidia_api_key,
        )

        persona = "Act as a senior software developer who is working as a tutor. "
        # task is defined by the user
        context = "Bare in mind that the students you are giving answers are coding beginners. "
        format = "Please, don't overcomplicate explanations. Don't use markdown. Try do have titles, subtitles, short explanations and bulleted point. The titles should be in caps, but subtitles in normal font. All titles and subtitles should be numbered."

        prompt = persona + task + " " + context + format
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": enable_thinking},
                "reasoning_budget": reasoning_budget,
            },
            stream=True,
        )

        for chunk in completion:
            if not chunk.choices:
                continue

            reasoning = getattr(
                chunk.choices[0].delta, "reasoning_content", None
            ) or getattr(chunk.choices[0].delta, "reasoning", None)
            if reasoning:
                formatter.print_reasoning(reasoning)

            if chunk.choices[0].delta.content is not None:
                formatter.print_content(chunk.choices[0].delta.content)

        saved_filename = formatter.finish()
        if saved_filename:
            return saved_filename
        return "".join(formatter.content_buffer)

    except Exception as e:
        formatter.print_error(str(e))
        raise e
