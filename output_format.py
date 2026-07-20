import datetime
import sys

# ANSI Color Codes
LIGHT_GREEN = "\033[92m"
WHITE = "\033[97m"
RED = "\033[91m"
RESET = "\033[0m"


class OutputFormatter:
    """Formatter to handle styled terminal output and saving output to a file."""

    def __init__(self, save_file: bool = True):
        self.save_file = save_file
        self.reasoning_buffer = []
        self.content_buffer = []
        self.current_mode = None  # "reasoning", "content", or None

    def print_reasoning(self, text: str):
        """Prints reasoning tokens in light green."""
        if not text:
            return
        self.reasoning_buffer.append(text)
        if self.current_mode != "reasoning":
            sys.stdout.write(LIGHT_GREEN)
            self.current_mode = "reasoning"
        sys.stdout.write(text)
        sys.stdout.flush()

    def print_content(self, text: str):
        """Prints final response tokens in white."""
        if not text:
            return
        self.content_buffer.append(text)
        if self.current_mode != "content":
            # Extra newline between reasoning and content if transitioning
            if self.current_mode == "reasoning":
                sys.stdout.write("\n\n")
            sys.stdout.write(WHITE)
            self.current_mode = "content"
        sys.stdout.write(text)
        sys.stdout.flush()

    def print_error(self, message: str):
        """Prints error messages in red."""
        sys.stdout.write(RESET)
        sys.stdout.write(f"\n{RED}ERROR: {message}{RESET}\n")
        sys.stdout.flush()

    def finish(self) -> str:
        """Resets terminal style and saves the final result into an output_date_time.md file."""
        sys.stdout.write(RESET)
        sys.stdout.flush()

        full_content = "".join(self.content_buffer)
        full_reasoning = "".join(self.reasoning_buffer)

        if self.save_file and (full_content or full_reasoning):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"output_{timestamp}.md"

            with open(filename, "w", encoding="utf-8") as f:
                if full_reasoning:
                    f.write("<!-- Thinking Process -->\n")
                    f.write("<details>\n<summary>Reasoning</summary>\n\n")
                    f.write(full_reasoning)
                    f.write("\n\n</details>\n\n")
                f.write(full_content)

            print(f"\n\n{WHITE}Output saved to {filename}{RESET}\n")
            return filename
        return ""
