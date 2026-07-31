from chat import stream_chat


def main():

    prompt = input("I am your chatbot. Tell me what do you need from me?\n>: ") or (
        "Can you tell me what is the best way to learn machine learning with ai. "
        "Give me some online references, youtube tutorials and ai tools I can use for free. "
    )
    print("Starting chat stream...")
    output_file = stream_chat(task=prompt)
    if output_file:
        print(f"Response successfully saved to: {output_file}")


if __name__ == "__main__":
    main()
