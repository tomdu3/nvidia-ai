import os
import unittest
from unittest.mock import MagicMock, patch
from chat import stream_chat


class MockDelta:
    def __init__(self, content=None, reasoning=None, reasoning_content=None):
        self.content = content
        self.reasoning = reasoning
        self.reasoning_content = reasoning_content


class MockChoice:
    def __init__(self, delta):
        self.delta = delta


class MockChunk:
    def __init__(self, choices):
        self.choices = choices


class TestChatModule(unittest.TestCase):
    def setUp(self):
        # Save original environment variable
        self.orig_api_key = os.environ.get("NVIDIA_API_KEY")
        # Ensure NVIDIA_API_KEY is set for normal tests
        os.environ["NVIDIA_API_KEY"] = "mock-api-key-12345"
        self.created_files = []

    def tearDown(self):
        # Restore environment variable
        if self.orig_api_key is not None:
            os.environ["NVIDIA_API_KEY"] = self.orig_api_key
        elif "NVIDIA_API_KEY" in os.environ:
            del os.environ["NVIDIA_API_KEY"]

        # Clean up any created output files
        for f in self.created_files:
            if os.path.exists(f):
                os.remove(f)
        # Scan workspace for output_*.md files created during tests and clean them up
        for f in os.listdir("."):
            if f.startswith("output_") and f.endswith(".md"):
                try:
                    os.remove(f)
                except OSError:
                    pass

    @patch("chat.OpenAI")
    def test_stream_chat_success(self, mock_openai):
        # Arrange
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Prepare mock stream chunks
        chunks = [
            MockChunk([MockChoice(MockDelta(reasoning_content="Thinking..."))]),
            MockChunk([MockChoice(MockDelta(reasoning="More thinking..."))]),
            MockChunk([MockChoice(MockDelta(content="Hello "))]),
            MockChunk([MockChoice(MockDelta(content="world!"))]),
        ]
        mock_client.chat.completions.create.return_value = chunks

        # Act
        result = stream_chat(
            prompt="Test prompt",
            model="nvidia/nemotron-3-super-120b-a12b",
            temperature=0.7,
            top_p=0.9,
            max_tokens=1000,
            enable_thinking=True,
            reasoning_budget=1000,
            save_file=False,
        )

        # Assert
        self.assertEqual(result, "Hello world!")
        mock_openai.assert_called_once_with(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key="mock-api-key-12345",
        )
        mock_client.chat.completions.create.assert_called_once_with(
            model="nvidia/nemotron-3-super-120b-a12b",
            messages=[{"role": "user", "content": "Test prompt"}],
            temperature=0.7,
            top_p=0.9,
            max_tokens=1000,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": True},
                "reasoning_budget": 1000,
            },
            stream=True,
        )

    @patch("chat.OpenAI")
    def test_stream_chat_save_file(self, mock_openai):
        # Arrange
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        chunks = [
            MockChunk([MockChoice(MockDelta(reasoning_content="Reasoning here."))]),
            MockChunk([MockChoice(MockDelta(content="File response content."))]),
        ]
        mock_client.chat.completions.create.return_value = chunks

        # Act
        result_file = stream_chat(prompt="Save to file test", save_file=True)

        # Assert
        self.assertTrue(result_file.startswith("output_"))
        self.assertTrue(result_file.endswith(".md"))
        self.assertTrue(os.path.exists(result_file))
        self.created_files.append(result_file)

        # Verify content saved
        with open(result_file, "r") as f:
            content = f.read()
        self.assertIn("Reasoning here.", content)
        self.assertIn("File response content.", content)

    @patch("chat.OpenAI")
    def test_missing_api_key(self, mock_openai):
        # Arrange
        if "NVIDIA_API_KEY" in os.environ:
            del os.environ["NVIDIA_API_KEY"]

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            stream_chat(prompt="Test prompt")

        self.assertIn("NVIDIA_API_KEY is not set", str(context.exception))

    @patch("chat.OpenAI")
    def test_api_exception(self, mock_openai):
        # Arrange
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception(
            "API connection failed"
        )

        # Act & Assert
        with self.assertRaises(Exception) as context:
            stream_chat(prompt="Test prompt", save_file=False)

        self.assertIn("API connection failed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
