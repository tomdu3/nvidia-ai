# NVIDIA AI Tutor Chatbot

An AI-powered terminal chatbot designed to act as a senior software developer tutor, providing clear, beginner-friendly explanations with streaming output and automated response saving.

---

## 💡 Project Idea

The **NVIDIA AI Tutor Chatbot** provides an interactive command-line interface tailored for coding beginners. It uses reasoning-capable AI models to break down complex programming and machine learning concepts into easy-to-understand, non-intimidating explanations.

Key Features:

- **Senior Developer Tutor Persona**: Formats explanations with simple structures, numbered headings, and bullet points suited for beginners.
- **Real-Time Streaming**: Live terminal rendering of model reasoning steps and final response output.
- **Automatic Output Archiving**: Automatically formats and saves responses as formatted Markdown files.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **API Integration**: OpenAI Python SDK (`openai`), customized for the NVIDIA API endpoint (`integrate.api.nvidia.com`)
- **Package & Dependency Management**: `uv` / standard virtualenv (`venv`)
- **Environment Management**: `python-dotenv`
- **Testing**: `pytest`

---

## ⚙️ Implementation Details

- **`main.py`**: Entry point for launching the CLI prompt session.
- **`chat.py`**: Handles API requests, system persona framing, and response streaming using NVIDIA's `nvidia/nemotron-3-super-120b-a12b` model (with thinking mode/reasoning budget enabled).
- **`config.py`**: Validates environment configurations and sets up client parameters.
- **`output_format.py`**: `OutputFormatter` class managing real-time terminal output formatting and writing responses to timestamped `.md` files.

---

## 🚀 Local Deployment

### 1. Prerequisites

- Python 3.10 or higher installed.
- An **NVIDIA API Key** (Get one from [NVIDIA Build](https://build.nvidia.com/)).

### 2. Clone & Setup Workspace

```bash
git clone https://github.com/tomdu3/nvidia-ai
cd nvidia
```

### 3. Set Up Virtual Environment & Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or standard Python `venv`:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install openai python-dotenv pytest
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your NVIDIA API key:

```env
NVIDIA_API_KEY=your_nvidia_api_key_here
```

### 5. Run the Application

```bash
python main.py
```

---

## 📜 Licensing & Copyright

Copyright (c) 2026 Tomislav Dukez.

This project is open-source software licensed under the [MIT License](LICENSE).
