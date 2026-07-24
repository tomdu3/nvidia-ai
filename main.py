from chat import stream_chat


def main():
    prompt = (
        "Can you tell me what is the best way to learn machine learning with ai. "
        "Give me some online references, youtube tutorials and ai tools I can use for free. "
        "please, don't use markdown format, but rather a simple text with bulletpoints. "
        "The titles should be in caps."
    )
    print("Starting chat stream...")
    output_file = stream_chat(prompt=prompt)
    if output_file:
        print(f"Response successfully saved to: {output_file}")


if __name__ == "__main__":
    main()

